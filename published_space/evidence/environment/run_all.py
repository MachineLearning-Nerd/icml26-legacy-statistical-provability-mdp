"""Fixed cumulative entrypoint for every experiment node."""

from __future__ import annotations

import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
HISTORICAL = ARTIFACTS / "historical_rejected_baseline"


def run_command(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def run_claim_verifiers() -> list[dict]:
    results: list[dict] = []
    for claim_dir in sorted(ARTIFACTS.glob("claim_*")):
        verifier = claim_dir / "verify.py"
        checker = claim_dir / "independent_checker.py"
        case = claim_dir / "counterexample.json"
        control = claim_dir / "negative_control.json"
        contract = claim_dir / "claim_contract.json"
        if not all(path.exists() for path in [verifier, checker, case, control, contract]):
            continue
        contract_data = json.loads(contract.read_text(encoding="utf-8"))
        verifier_result = run_command(
            [
                sys.executable,
                str(verifier),
                "--case",
                str(case),
                "--output",
                str(claim_dir / "verifier_output.json"),
            ]
        )
        checker_result = run_command(
            [
                sys.executable,
                str(checker),
                "--output",
                str(claim_dir / "independent_checker_output.json"),
            ]
        )
        control_result = run_command(
            [
                sys.executable,
                str(verifier),
                "--case",
                str(control),
                "--output",
                str(claim_dir / "negative_control_output.json"),
            ]
        )
        combined = (
            "PRIMARY VERIFIER\n"
            + verifier_result.stdout
            + verifier_result.stderr
            + "\nINDEPENDENT CHECKER\n"
            + checker_result.stdout
            + checker_result.stderr
            + "\nNEGATIVE CONTROL\n"
            + control_result.stdout
            + control_result.stderr
        )
        (claim_dir / "raw_output.txt").write_text(combined, encoding="utf-8")
        passed = (
            verifier_result.returncode == 0
            and checker_result.returncode == 0
            and control_result.returncode != 0
        )
        result = {
            "claim": contract_data["claim"],
            "verdict": contract_data["target_verdict"] if passed else "BLOCKED",
            "passed": passed,
            "primary_exit_code": verifier_result.returncode,
            "checker_exit_code": checker_result.returncode,
            "negative_control_exit_code": control_result.returncode,
        }
        results.append(result)
        claim_eval = f"""# Claim {result['claim']} — {result['verdict']}

- Exact claim contract: `claim_contract.json`
- Primary verifier exit: `{verifier_result.returncode}`
- Independent checker exit: `{checker_result.returncode}`
- Negative-control verifier exit: `{control_result.returncode}` (must be nonzero)
- Raw combined output: `raw_output.txt`
- Result accepted: `{str(passed).lower()}`
"""
        (claim_dir / "EVAL.md").write_text(claim_eval, encoding="utf-8")
        print(combined)
        print(claim_eval)
    return results


def main() -> int:
    started = time.perf_counter()
    HISTORICAL.mkdir(parents=True, exist_ok=True)
    process = run_command(
        [sys.executable, "-m", "reproduction.historical.verify_measure"],
    )
    raw = process.stdout + process.stderr
    (HISTORICAL / "raw_output.txt").write_text(raw, encoding="utf-8")
    snapshot_path = (
        ROOT / "reproduction" / "historical" / "judge_verdict_2989d916.json"
    )
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    claim_results = run_claim_verifiers()
    release_audit = run_command(
        [
            sys.executable,
            "-m",
            "reproduction.release_audit",
            "--tree",
            str(ROOT / "space_candidate"),
        ]
    )
    print("EVALUATOR-VISIBLE RELEASE AUDIT")
    print(release_audit.stdout, end="")
    print(release_audit.stderr, end="")
    runtime = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    provenance = {
        "baseline_git_sha": os.environ.get("ORX_COMMIT_SHA", "resolved-by-run"),
        "judged_space_sha": snapshot["sha"],
        "python": platform.python_version(),
        "platform": platform.platform(),
        "logical_cpus_visible": os.cpu_count(),
        "estimated_cores_required": 1,
        "designed_process_threads": 1,
        "max_rss_platform_units": usage.ru_maxrss,
        "runtime_seconds": runtime,
        "historical_exit_code": process.returncode,
        "claim_results": claim_results,
        "release_audit_exit_code": release_audit.returncode,
    }
    (HISTORICAL / "provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    (HISTORICAL / "judge_snapshot.json").write_text(
        json.dumps(snapshot, indent=2) + "\n", encoding="utf-8"
    )

    rows = "\n".join(
        f"| {item['claim']} | {item['verdict'].upper()} | {item['reason']} |"
        for item in snapshot["claims"]
    )
    claim_rows = "\n".join(
        f"| {item['claim']} | {item['verdict']} | {item['passed']} |"
        for item in claim_results
    )
    if not claim_rows:
        claim_rows = "| — | No current exact verifier on this node | — |"
    eval_text = f"""# Cumulative reproduction evaluation

The historical control is preserved below and is **not** current verification.

## Current exact verifiers

| Claim | Evidence verdict | Accepted by cumulative runner |
| --- | --- | --- |
{claim_rows}

## Historical rejected baseline

| Claim | Live verdict | Why the historical check is insufficient |
| --- | --- | --- |
{rows}

- Previous live judged score: **{snapshot['score']}**
- Judged Space revision: `{snapshot['sha']}`
- Historical script exit code: `{process.returncode}`
- Estimated required cores: 1
- Logical CPUs exposed by backend: {os.cpu_count()}
- Designed concurrency: one Python process
- Runtime: {runtime:.6f} s
- Raw output: `historical_rejected_baseline/raw_output.txt`
"""
    (ARTIFACTS / "EVAL.md").write_text(eval_text, encoding="utf-8")
    print(raw, end="")
    print(eval_text)
    if process.returncode != 0:
        return process.returncode
    if any(not result["passed"] for result in claim_results):
        return 1
    if release_audit.returncode != 0:
        return release_audit.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
