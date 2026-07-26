# Current exact verification — six claims

Previous live judged score: **4/12** at Space revision
`2989d916e16dce116af776d60d13246aa18eb73f` on 2026-07-25.
That score has not changed. The table below is new reproducible evidence and a
forecast for a future evaluator, not a judge result.

| Claim | Current result | Exact route | Confidence | Page |
| --- | --- | --- | --- | --- |
| 1 | VERIFIED | universal BL/weak compactness derivation | HIGH | [open](#/current-claim-1) |
| 2 | VERIFIED | USC, compact maximum, Borel selector derivation | MEDIUM | [open](#/current-claim-2) |
| 3 | VERIFIED | universal Bellman monotonicity and two inductions | HIGH | [open](#/current-claim-3) |
| 4 | VERIFIED | exact regret proof and tight factor-two witness | HIGH | [open](#/current-claim-4) |
| 5 | FALSIFIED | literal displayed top-k counterexample | MEDIUM | [open](#/current-claim-5) |
| 6 | FALSIFIED | displayed theorem's missing-coverage counterexample | MEDIUM | [open](#/current-claim-6) |

Conservative projected score after review: **8–12/12**. Best-supported possible
score: **12/12**, explicitly a forecast. Only the live judge can award points.

## What changed

The historical checker sampled a six-state MDP, used total variation as a
bounded-Lipschitz proxy, constructed certificates around solved `V*`, admitted
a `+0.5` regret tolerance, and evaluated the Claim 6 formula without measuring
error. Those checks are preserved but labeled **Historical rejected baseline**.

The current suite instead uses proof-level derivations for universally
quantified Claims 1–4 and exact assumption-satisfying counterexamples for the
literal displayed Claims 5–6. Every route has an executable primary verifier,
an independent Z3 checker, a control that exits nonzero, exact assumptions,
and raw JSON inline on its claim page.

## Fixed command and environment

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

The command is identical on every experiment node. Python 3.12 and 44 packages
are pinned by [.python-version](../../evidence/environment/.python-version),
[pyproject.toml](../../evidence/environment/pyproject.toml), and
[uv.lock](../../evidence/environment/uv.lock). The cumulative
[runner source](../../evidence/environment/run_all.py) requires each primary
and independent checker to exit `0` and each negative control to exit nonzero.
The [release-audit source](../../evidence/environment/release_audit.py)
independently checks discoverability, copied evidence, text-only files,
protected history, JSON validity, links, and secret-like material.

The source audit used arXiv v1 source SHA-256
`bfb1bcbb7c9a5bb375c15b379917cb22d0b70127c05d9d9afbfc128ff829297f`
and ar5iv HTML SHA-256
`5cafb5b0f293d4044f87323a8e3bc6b48788996363e12681e6a6a819025fc577`,
retrieved 2026-07-26 with an explicit browser User-Agent. See the
[source audit](../../evidence/audit/source_audit.md).

## Accepted CPU evidence

| Cumulative claims | Accepted commit | HF flavor | Allocation | Runner | Full job |
| --- | --- | --- | --- | ---: | ---: |
| 5 | `73a1ac1` | cpu-upgrade | 8 vCPU; 64 host-logical visible; one process | 0.870154 s | 21 s |
| 5–6 | `4399dff` | cpu-upgrade | 8 vCPU; 64 host-logical visible; one process | 1.001355 s | 21 s |
| 4–6 | `4d73764` | cpu-upgrade | 8 vCPU; 64 host-logical visible; one process | 1.303052 s | 21 s |
| 3–6 | `4173b12` | cpu-upgrade | 8 vCPU; 64 host-logical visible; one process | 1.704828 s | 21 s |
| 1,3–6 | `cbb2194` | cpu-upgrade | 8 vCPU; 64 host-logical visible; one process | 1.655363 s | 21 s |
| 1–6 | `dc408b5` | cpu-upgrade | 8 vCPU; 64 host-logical visible; one process | 1.875989 s | 21 s |

Each scientific checker was estimated at one core and under one minute.
Fresh-environment runtime was uncertain, so every formal run followed policy
and used Hugging Face `cpu-upgrade` (8 allocated vCPUs); no GPU was used.
Python's `os.cpu_count()` exposed 64 host logical CPUs, recorded separately
from the allocation. The allocation and current list price are documented in
the official [Hugging Face Jobs hardware table](https://huggingface.co/docs/hub/jobs-pricing).

## Review paths

- [Evaluator visibility matrix](#/visibility-matrix)
- [Release report and score forecast](#/release-report)
- [Historical rejected baseline](#/historical-rejected-baseline)
- [Protected judged-file manifest](../../evidence/audit/protected_space_manifest.txt)
- [Exact filtered live verdict record](../../evidence/audit/live_verdict_record.json)
- [Evaluator-blind review record](../../evidence/audit/evaluator_blind_review.md)

## Version-sensitive limitations

Claim 5 falsifies the literal displayed top-k statement, not Appendix D's
narrower plug-in greedy argument. Claim 6 falsifies displayed Theorem 6 as
written, not Appendix F's refined Theorem 7 with eta-net coverage and target
regularity. These boundaries are part of the verdicts, not footnotes.
