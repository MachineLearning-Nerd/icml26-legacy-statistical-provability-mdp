"""Audit the evaluator-visible Hugging Face Space candidate.

This checker deliberately starts from ``logbook.json`` and follows only files
reachable from the candidate tree.  It does not use experiment descriptions or
run logs as evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_RES = [
    re.compile(r"hf_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
REQUIRED_CLAIM_FILES = {
    "claim_contract.json",
    "source_audit.md",
    "method.md",
    "verify.py",
    "verifier_output.json",
    "independent_checker.py",
    "independent_checker_output.json",
    "negative_control.json",
    "negative_control_output.json",
    "raw_output.txt",
    "exact_command.md",
    "limitations.md",
    "EVAL.md",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_protected_manifest(path: Path) -> dict[str, str]:
    protected: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match:
            protected[match.group(2)] = match.group(1)
    if len(protected) != 16:
        raise ValueError(f"expected 16 protected files, found {len(protected)}")
    return protected


def walk_logbook(node: dict) -> list[str]:
    files = [node["file"]]
    for child in node.get("children", []):
        files.extend(walk_logbook(child))
    return files


def relative_target(source: Path, raw_target: str, tree: Path) -> str | None:
    target = unquote(raw_target.split("#", 1)[0].split("?", 1)[0])
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    resolved = (source.parent / target).resolve()
    try:
        return resolved.relative_to(tree.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"link escapes candidate tree: {source}: {raw_target}") from error


def audit(
    tree: Path,
    protected_manifest: Path,
    internal_artifacts: Path,
    assembled: bool = False,
) -> dict:
    errors: list[str] = []
    protected = parse_protected_manifest(protected_manifest)
    if assembled:
        for relative, expected_hash in protected.items():
            path = tree / relative
            if not path.is_file():
                errors.append(f"protected judged path missing: {relative}")
            elif relative not in {"README.md", "logbook.json"}:
                observed_hash = sha256(path)
                if observed_hash != expected_hash:
                    errors.append(
                        f"protected historical file changed: {relative} "
                        f"({observed_hash} != {expected_hash})"
                    )
    logbook_path = tree / "logbook.json"
    try:
        logbook = json.loads(logbook_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid canonical logbook: {error}") from error

    if logbook.get("space_id") != "DineshAI/hAQZl57Nvx":
        errors.append("logbook space_id is not the protected existing Space")
    root = logbook.get("root", {})
    if root.get("slug") != "current-verification":
        errors.append("current verification is not the canonical logbook root")

    navigation_files = walk_logbook(root)
    for relative in navigation_files:
        if not (tree / relative).is_file() and relative not in protected:
            errors.append(f"navigation target missing: {relative}")

    candidate_files = sorted(
        path for path in tree.rglob("*") if path.is_file() and ".git" not in path.parts
    )
    for path in candidate_files:
        relative = path.relative_to(tree).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            if assembled and relative in protected:
                continue
            errors.append(f"non-text file in upload candidate: {relative}")
            continue
        for secret_re in SECRET_RES:
            if secret_re.search(text):
                errors.append(f"secret-like material found: {relative}")
        if path.suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as error:
                errors.append(f"invalid JSON {relative}: {error}")
        if path.suffix == ".md":
            for raw_target in LINK_RE.findall(text):
                target = relative_target(path, raw_target, tree)
                if target and not (tree / target).is_file() and target not in protected:
                    errors.append(f"broken link {relative} -> {target}")

    expected_verdicts = {
        1: "VERIFIED",
        2: "VERIFIED",
        3: "VERIFIED",
        4: "VERIFIED",
        5: "FALSIFIED",
        6: "FALSIFIED",
    }
    for claim, verdict in expected_verdicts.items():
        claim_dir = tree / "evidence" / f"claim_{claim}"
        present = {path.name for path in claim_dir.iterdir()} if claim_dir.is_dir() else set()
        missing = REQUIRED_CLAIM_FILES - present
        if missing:
            errors.append(f"claim {claim} missing files: {sorted(missing)}")
            continue
        contract = json.loads((claim_dir / "claim_contract.json").read_text(encoding="utf-8"))
        primary = json.loads((claim_dir / "verifier_output.json").read_text(encoding="utf-8"))
        control = json.loads(
            (claim_dir / "negative_control_output.json").read_text(encoding="utf-8")
        )
        if contract.get("claim") != claim:
            errors.append(f"claim {claim} contract claim number mismatch")
        if contract.get("target_verdict") != verdict:
            errors.append(f"claim {claim} contract verdict mismatch")
        if primary.get("verdict") != verdict:
            errors.append(f"claim {claim} primary output is not accepted {verdict}")
        if verdict == "VERIFIED" and primary.get("verified") is not True:
            errors.append(f"claim {claim} primary proof is not verified")
        if verdict == "FALSIFIED" and primary.get("contradiction") is not True:
            errors.append(f"claim {claim} primary counterexample has no contradiction")
        if verdict == "VERIFIED":
            control_rejects = (
                control.get("verified") is False
                and control.get("failed_for_intended_reason") is True
            )
        else:
            control_rejects = (
                control.get("contradiction") is False
                and control.get("verdict") == "NO_COUNTEREXAMPLE"
            )
        if not control_rejects:
            errors.append(f"claim {claim} negative control does not reject as intended")
        internal_dir = internal_artifacts / f"claim_{claim}"
        for filename in REQUIRED_CLAIM_FILES:
            internal_path = internal_dir / filename
            candidate_path = claim_dir / filename
            if internal_path.is_file() and sha256(internal_path) != sha256(candidate_path):
                errors.append(f"claim {claim} copied evidence differs: {filename}")

        page = (tree / "pages" / f"current-claim-{claim}" / "page.md").read_text(
            encoding="utf-8"
        )
        required_page_terms = [
            verdict,
            "Quantifiers",
            "Assumptions",
            "Raw",
            "negative-control",
            "Accepted commit",
            "cpu-upgrade",
            "Limitations",
        ]
        for term in required_page_terms:
            if term not in page:
                errors.append(f"claim {claim} page omits evaluator-visible term: {term}")

    matrix = (tree / "pages" / "visibility-matrix" / "page.md").read_text(
        encoding="utf-8"
    )
    required_header = (
        "| Claim | Canonical page | Code visible | Data inline | Raw link | "
        "Checker | Control | Exact claim tested | Reviewer verdict |"
    )
    if required_header not in matrix:
        errors.append("visibility matrix header is incomplete")
    for claim in range(1, 7):
        if f"| {claim} |" not in matrix:
            errors.append(f"visibility matrix omits claim {claim}")

    for source, visible in [
        (ROOT / "reproduction" / "run_all.py", tree / "evidence" / "environment" / "run_all.py"),
        (
            ROOT / "reproduction" / "release_audit.py",
            tree / "evidence" / "environment" / "release_audit.py",
        ),
    ]:
        if not visible.is_file():
            errors.append(f"evaluator-visible runner source missing: {visible.name}")
        elif sha256(source) != sha256(visible):
            errors.append(f"evaluator-visible runner source is stale: {visible.name}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "canonical_entrypoint": "logbook.json -> pages/current-verification/page.md",
        "space_id": logbook.get("space_id"),
        "navigation_files_checked": len(navigation_files),
        "candidate_text_files_checked": len(candidate_files),
        "protected_paths_available_or_manifested": len(protected),
        "claims_checked": 6,
        "errors": errors,
    }


def write_manifests(tree: Path, release_dir: Path) -> None:
    release_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in tree.rglob("*") if path.is_file())
    allowlist = "\n".join(path.relative_to(tree).as_posix() for path in files) + "\n"
    hashes = "\n".join(
        f"{sha256(path)}  {path.relative_to(tree).as_posix()}" for path in files
    ) + "\n"
    (release_dir / "space-upload-allowlist.txt").write_text(
        allowlist, encoding="utf-8"
    )
    (release_dir / "space-upload-sha256.txt").write_text(hashes, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, default=ROOT / "space_candidate")
    parser.add_argument(
        "--protected-manifest",
        type=Path,
        default=ROOT / "reproduction" / "audit" / "protected_space_manifest.txt",
    )
    parser.add_argument(
        "--internal-artifacts",
        type=Path,
        default=ROOT / ".openresearch" / "artifacts",
    )
    parser.add_argument("--write-manifests", action="store_true")
    parser.add_argument(
        "--assembled",
        action="store_true",
        help="Require the protected judged tree to be a subset of this tree.",
    )
    parser.add_argument("--release-dir", type=Path, default=ROOT / "release")
    arguments = parser.parse_args()

    result = audit(
        arguments.tree,
        arguments.protected_manifest,
        arguments.internal_artifacts,
        assembled=arguments.assembled,
    )
    if arguments.write_manifests and result["status"] == "PASS":
        write_manifests(arguments.tree, arguments.release_dir)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
