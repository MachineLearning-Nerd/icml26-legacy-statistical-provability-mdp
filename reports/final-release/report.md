# Final release record — exact six-claim reproduction

- Previous live judged score: `4/12`
- Conservative projected score range after the change: `8–12/12`
- Best-supported possible new score: `12/12` (**forecast, not judge result**)

The current total remains `4/12` until the live evaluator records a new
verdict. The published artifact is awaiting that evaluation.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | VERIFIED | Universal BL/weak compactness derivation, independent SMT algebra, and noncompact control; named classical topology results remain a review dependency. |
| 2 | 1 | 2 | MEDIUM | VERIFIED | USC/maximum/Borel-selector proof and isolating non-Feller control; measurable uniformization is review-sensitive. |
| 3 | 1 | 2 | HIGH | VERIFIED | Universal Bellman monotonicity and exact upper/lower induction certificates; broken recurrence control rejects. |
| 4 | 1 | 2 | HIGH | VERIFIED | Universal exact regret proof and an actual MDP attaining the factor two; no numerical tolerance. |
| 5 | 0 | 2 | MEDIUM | FALSIFIED | Exact zero-error top-k counterexample satisfies the displayed assumptions; Appendix D's narrower `k=1` greedy result is not contradicted. |
| 6 | 0 | 2 | MEDIUM | FALSIFIED | Exact missing-coverage ERM counterexample refutes displayed Theorem 6; Appendix F's coverage-refined theorem is not contradicted. |

All six claims changed relative to the previous judge record. No claim is
BLOCKED. The previous TOY checks for Claims 1–4 and INCONCLUSIVE checks for
Claims 5–6 remain preserved as **Historical rejected baseline**.

## Publication state

- Baseline HF Head and Judge Head:
  `2989d916e16dce116af776d60d13246aa18eb73f`
- Winning experiment branch: `orx/correct-cpu-allocation-provenance`
- Winning Git SHA: `96c58352e261af9dc9baf9c5a2b4603b8a30f948`
- Winning run: `108aed56-72e0-4616-984b-0723801e811f`
- Published existing Space: `DineshAI/hAQZl57Nvx`
- Published Space revision:
  `54205ae698e82f5b7ff82ec9b493535d1580df37`
- GitHub `main` publication SHA:
  `bc1651ad02527adcbe04444182b029165c301868`

The upload used the Hugging Face commit API and only the 109 UTF-8 files in
`release/space-upload-allowlist.txt`, with hashes in
`release/space-upload-sha256.txt`. A fresh download of the exact published
revision matched all 109 hashes.

The old Space had 16 protected paths. The published tree has 124 repository
files; every old path remains present. All historical files other than the
intentionally superseded `README.md` and `logbook.json` retain their exact old
SHA-256 values. The complete published revision is mirrored byte-for-byte on
GitHub under `published_space/<Space path>`.

## Experiment tree

The tree is a single descending lineage:

```text
judged baseline
└── Claim 5 counterexample
    └── Claim 6 counterexample
        └── Claim 4 proof
            └── Claim 3 proof
                └── Claim 1 proof
                    └── Claim 2 proof
                        └── evaluator-visible release
                            └── CPU-provenance correction (winner)
```

Every child reran every previously accepted claim. No completed experiment
branch was merged or rebased.

## Commands and evidence

The immutable experiment command on every node was:

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Every formal launch used:

```bash
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade \
  --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1800
orx exp wait <experiment-id> --timeout 480
orx logs <run-id> --bytes <sufficient-full-log-size>
```

The release checks were:

```bash
uv run --frozen python -m reproduction.release_audit --write-manifests
uv run --frozen marimo check notebooks/statistical_provability_reproduction.py
uv run --frozen python -m reproduction.release_audit \
  --tree <fresh-candidate-or-published-tree> --assembled
git ls-remote origin refs/heads/main
```

Startup and source-audit commands included `orx skill`, the named ORX skill
reads, `orx projects --json`, `orx runs`, `orx exp status`, `orx exp desc`,
`git status --short`, `git branch -a`, disk and environment-name audits,
explicit-User-Agent paper retrieval, exact Space checkout, and the live
verdict filter on `space_id == "DineshAI/hAQZl57Nvx"`.

Durable evidence is available at:

- GitHub: `.openresearch/artifacts/claim_1` through `claim_6`
- Published Space: `evidence/claim_1` through `claim_6`
- Canonical Space entry: `logbook.json` →
  `pages/current-verification/page.md`
- Illustrated report:
  `reports/exact-claims/report.md`
- Tutorial notebook:
  `notebooks/statistical_provability_reproduction.py`
- Visibility and blind review:
  `pages/visibility-matrix/page.md` and
  `evidence/audit/evaluator_blind_review.md`

## Compute and cost

Scientific requirement was estimated as one core and under one minute per
checker, but fresh environment setup was uncertain, so all formal work used
Hugging Face `cpu-upgrade`. Its hardware contract allocates 8 vCPUs; Python
reported 64 host logical CPUs visible inside the container. The verifier used
one process and no GPU.

- Accepted HF jobs: 9, total ORX duration 194 seconds.
- One environment failure: 10 seconds.
- Total HF job duration: 204 seconds across 10 jobs.
- Winning runner: 1.973698 seconds; winning full job: 21 seconds.
- Official list rate used for the estimate: `$0.0005/min`.
- Nominal per-job minute-billing ceiling before credits: `$0.005`.
- Local work: short interactive validation only, no accepted scientific
  result; local monetary compute cost `0`.

## Post-publication verification

A fresh empty directory downloaded exactly
`54205ae698e82f5b7ff82ec9b493535d1580df37`. The audit found:

- 109/109 uploaded hashes matched;
- 16/16 navigation entries resolved;
- all six exact claim bundles were present;
- no broken current links, invalid JSON, stale copied verifier source,
  binary upload addition, or secret-like material;
- current verification was the canonical root;
- the historical weak verifier appeared only beneath **Historical rejected
  baseline**;
- evaluator-blind second-pass unresolved conclusions: none.

No score increase is claimed. The paper is awaiting the live judge on the
published revision.
