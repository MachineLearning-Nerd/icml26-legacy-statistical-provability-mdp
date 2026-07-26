# Claim 4 — current verification

## Result: VERIFIED

This proof-level verifier supersedes the old constant-regret sweep with a
`+0.5` tolerance, which remains preserved as **Historical rejected baseline**.
It targets the exact universal theorem at arXiv-v1 anchor `Thmtheorem4`.

## Assumptions and Quantifiers

For **every** finite horizon, admissible reachability MDP, initial state, and
score family satisfying the stated uniform error bound
`|h_b-Q_b^*|<=epsilon_b` on the relevant domain, the contract requires
`0 <= V_B^*(x0)-V_B^{pi_h}(x0) <= 2 sum_b epsilon_b`.

## Exact derivation

At stage `b`, let `a_*` maximize `Q_b^*` and let `a_g` maximize the score.
Adding the following three audited inequalities gives the one-step result:

```text
Q_b^*(a_*) - h_b(a_*)       <= epsilon_b
h_b(a_*) - h_b(a_g)         <= 0
h_b(a_g) - Q_b^*(a_g)       <= epsilon_b
------------------------------------------------
Q_b^*(a_*) - Q_b^*(a_g)     <= 2 epsilon_b.
```

For `D_b(x)=V_b^*(x)-V_b^pi(x)`, Bellman expansion then gives

```text
D_b(x)
 <= 2 epsilon_b
    + integral D_(b-1)(x') P(dx'|x,a_g).
```

Integration against a probability kernel preserves upper bounds. With
`D_0=0`, natural-number induction proves
`0 <= D_B(x0) <= 2 sum_(b=1)^B epsilon_b` for every finite horizon and every
admissible MDP covered by the theorem. This is a universal symbolic
derivation, not a finite sweep.

## Independent checks and tightness

The exact proof kernel validates the one-step Farkas certificate, Bellman
recurrence certificate, and induction schema. Z3 finds both violating real
assignments `unsat`.

A valid horizon-one reachability MDP has optimal goal probability `1/2`, bad
goal probability `0`, tied scores `1/4`, and `epsilon=1/4`. Greedy tie-breaking
may choose the bad action, attaining `regret=1/2=2 epsilon`; the factor two is
tight. The negative control removes uniform score error, obtains positive
regret at `epsilon=0`, exits `3`, and becomes Z3-`unsat` when that assumption is
restored.

## Reproduce and provenance

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Accepted commit:
`4d737646229a1f9f35996354af2c5b8e2c795833`. Hugging Face
`cpu-upgrade` (8 allocated vCPUs; 64 host logical CPUs visible),
one-process design, cumulative runner
1.303052 seconds, full job 21 seconds. Primary exit `0`, independent checker
exit `0`, negative control exit `3`.

## Raw result

```json
{
  "one_step_farkas_certificate": true,
  "bellman_recurrence_certificate": true,
  "finite_horizon_induction_schema": true,
  "uniform_error": "1/4",
  "regret": "1/2",
  "bound": "1/2",
  "verdict": "VERIFIED"
}
```

Downloadable evidence:

- [claim contract](../../evidence/claim_4/claim_contract.json)
- [source audit](../../evidence/claim_4/source_audit.md)
- [complete proof](../../evidence/claim_4/proof_certificate.md)
- [primary verifier](../../evidence/claim_4/verify.py) and
  [its JSON output](../../evidence/claim_4/verifier_output.json)
- [raw combined primary/checker/control output](../../evidence/claim_4/raw_output.txt)
- [independent checker](../../evidence/claim_4/independent_checker.py) and
  [its JSON output](../../evidence/claim_4/independent_checker_output.json)
- [negative-control input](../../evidence/claim_4/negative_control.json) and
  [output](../../evidence/claim_4/negative_control_output.json)
- [method](../../evidence/claim_4/method.md),
  [limitations](../../evidence/claim_4/limitations.md), and
  [accepted evaluation](../../evidence/claim_4/EVAL.md)

## Limitations

The theorem's domain clause must cover every action in each greedy comparison
and every continuation state reached by the policy. This proof verifies the
stated worst-case guarantee; it does not assert that learned scores usually
attain the worst case.
