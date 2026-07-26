# Claim 6 — current verification

## Result: FALSIFIED

This page supersedes the old formula-decreases check, which remains preserved
as **Historical rejected baseline**. The current verifier targets the exact
displayed arXiv-v1 theorem at source anchor `Thmtheorem6`.

The displayed theorem asserts a uniform high-probability estimation rate from
doubling geometry, a uniformly Lipschitz hypothesis class, bounded unbiased
targets, and squared-loss ERM. It does not impose sampling coverage. Appendix F
later adds that missing condition in a refined theorem.

## Assumptions and Quantifiers

For **every** sample size, the displayed theorem claims a high-probability
uniform error bound for a squared-loss ERM under only the displayed compact
doubling-domain, uniform Lipschitz, and bounded unbiased-target assumptions.
The universal claim therefore covers the valid concentrated query
distribution and valid ERM tie-breaking used below.

## Assumption audit and contradiction

| Quantity | Exact value |
| --- | ---: |
| Domain | `[0,1]`, compact, doubling dimension 1 |
| Target | `Q(z)=z` |
| Hypothesis class | `{h_zero(z)=0, h_identity(z)=z}` |
| Lipschitz bound | 1 |
| Target generator | `Y(z)=z` deterministically |
| Training queries | all at `z=0` |
| Selected ERM | `h_zero` (ties at empirical risk 0) |
| Approximation error | 0 |
| Uniform error for every sample size | 1 |
| Claimed estimation term | tends to 0 |

For `delta=1/2` and `n_m=2^m`, the cube of the displayed rate is below
`a_m=(m+1)/2^m`. The exact ratio certificate
`a_(m+1)/a_m=(m+2)/(2m+2)<=3/4` follows from `0<=2m-2` for every integer
`m>=1`. Thus no finite big-O constant independent of `n` can bound the
constant unit error.

## Reproduce

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Accepted commit:
`4399dffdfe1feefffec302be9272376554953254` on Hugging Face
`cpu-upgrade`, which allocates 8 vCPUs. Python exposed 64 host logical CPUs to
the container; the deterministic checker used one process. Cumulative
verification took 1.001355 seconds; full job
duration was 21 seconds.

Primary exact-rational verifier: exit `0`. Independent Z3 checker: construction
`sat`, negation of the infinite ratio certificate `unsat`, coverage-restored
bad ERM `unsat`, exit `0`. Negative-control primary verifier: exit `3` as
required.

## Raw output

```json
{
  "selected_erm": "zero",
  "approximation_error": "0",
  "uniform_sup_error_for_every_n": "1",
  "rate_tends_to_zero": true,
  "contradiction": true,
  "verdict": "FALSIFIED"
}
```

Downloadable evidence:

- [claim contract](../../evidence/claim_6/claim_contract.json)
- [source audit](../../evidence/claim_6/source_audit.md)
- [primary verifier](../../evidence/claim_6/verify.py) and
  [its JSON output](../../evidence/claim_6/verifier_output.json)
- [raw combined primary/checker/control output](../../evidence/claim_6/raw_output.txt)
- [independent checker](../../evidence/claim_6/independent_checker.py) and
  [its JSON output](../../evidence/claim_6/independent_checker_output.json)
- [counterexample input](../../evidence/claim_6/counterexample.json)
- [negative-control input](../../evidence/claim_6/negative_control.json) and
  [output](../../evidence/claim_6/negative_control_output.json)
- [method](../../evidence/claim_6/method.md),
  [limitations](../../evidence/claim_6/limitations.md), and
  [accepted evaluation](../../evidence/claim_6/EVAL.md)

## Limitations

This falsifies the displayed theorem as written. It does not falsify Appendix
F's refined Theorem 7, which requires an eta-net, repeated labels at every net
point, target Lipschitzness, and a Lipschitz extension estimator.
