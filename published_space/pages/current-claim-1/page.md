# Claim 1 — current verification

## Result: VERIFIED

This proof-level verification supersedes the old observation that random
six-state measures have bounded total-variation diameter. That page remains
preserved as **Historical rejected baseline**. The current route targets
arXiv-v1 Theorem 1 exactly.

## Assumptions and Quantifiers

For **every** compact metric carrier `K` and **every** finite mass bound
`W>0`, the contract covers the full set of finite positive Borel measures
`mu` satisfying `mu(K)<=W`; it must prove compactness in the exact
bounded-Lipschitz metric.

## Exact universal derivation

For every compact metric `K` and finite `W>0`, the bounded-Lipschitz unit ball
is uniformly bounded and equicontinuous, hence uniformly compact by
Arzelà–Ascoli. This gives the difficult direction of topology equivalence:
when `mu_n` converges weakly, any hypothetical nonvanishing `d_BL` witness has
a uniformly convergent subsequence; the common `2W` mass bound makes its
integral vanish, a contradiction.

In the other direction, bounded Lipschitz functions are uniformly dense in
`C(K)`, and the same `2W` bound transfers `d_BL` test convergence to every
continuous test. Thus `d_BL` exactly metrizes weak convergence. Density and
Riesz uniqueness also give metric separation.

All measures share the compact carrier `K`, so the family is uniformly tight.
Prokhorov gives a weakly convergent subsequence. Positivity survives the limit,
and testing with constant one gives `mu(K)=lim mu_n(K)<=W`. Topology
equivalence converts this to a `d_BL`-convergent subsequence in the same set;
sequential compactness equals compactness for metric spaces.

The primary checker validates all 11 dependencies and rejects altered,
missing, cyclic, or disconnected steps. The independent Z3 route finds the
triangle and uniform-subsequence contradiction negations `unsat`.

## Negative control

On the noncompact natural numbers with discrete metric, `mu_n=delta_n` all
have mass one. A singleton-indicator BL-unit test shows
`d_BL(delta_n,delta_m)>=1` for every `n!=m`, so no subsequence is Cauchy. The
control exits `3` because compactness of `K` was deliberately removed; it is
not presented as a falsification.

## Reproduce and provenance

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Accepted commit:
`cbb2194d1bdd6da64e013ad51505a5ac38ced270`. Hugging Face
`cpu-upgrade` (8 allocated vCPUs; 64 host logical CPUs visible),
one-process design, cumulative runner
1.655363 seconds, full job 21 seconds. Primary exit `0`, independent checker
exit `0`, negative control exit `3`.

## Raw result

```json
{
  "dependency_nodes": 11,
  "dependency_graph_acyclic": true,
  "metric": true,
  "weak_bl_equivalence": true,
  "weak_sequential_compactness": true,
  "limit_stays_in_class": true,
  "metric_compactness": true,
  "verdict": "VERIFIED"
}
```

Downloadable evidence:

- [claim contract](../../evidence/claim_1/claim_contract.json)
- [source audit](../../evidence/claim_1/source_audit.md)
- [complete proof](../../evidence/claim_1/proof_certificate.md)
- [primary verifier](../../evidence/claim_1/verify.py) and
  [its JSON output](../../evidence/claim_1/verifier_output.json)
- [raw combined primary/checker/control output](../../evidence/claim_1/raw_output.txt)
- [independent checker](../../evidence/claim_1/independent_checker.py) and
  [its JSON output](../../evidence/claim_1/independent_checker_output.json)
- [negative-control input](../../evidence/claim_1/negative_control.json) and
  [output](../../evidence/claim_1/negative_control_output.json)
- [method](../../evidence/claim_1/method.md),
  [limitations](../../evidence/claim_1/limitations.md), and
  [accepted evaluation](../../evidence/claim_1/EVAL.md)

## Limitations

The executable checker validates the proof structure and algebraic substeps
while trusting the named classical theorems under their audited hypotheses.
This establishes the full positive-measure theorem, not just integer-valued
goal encodings.
