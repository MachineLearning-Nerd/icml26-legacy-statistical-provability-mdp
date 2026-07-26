# Claim 3 — current verification

## Result: VERIFIED

This universal proof supersedes the six-state functions constructed around an
already solved `V*`, which remain preserved as **Historical rejected
baseline**. It targets arXiv-v1 Theorem 3 and Definition 5 exactly.

## Assumptions and Quantifiers

For **every** finite horizon `B`, initial state, and function sequences
obeying the paper's Bellman sub- or super-solution inequalities at **every**
stage and state, the contract requires
`L_B(x0) <= V_B^*(x0) <= U_B(x0)`.

## Universal proof

If `V<=W` pointwise, integration against every probability kernel preserves
order, then supremum over actions preserves order, then maximum with the goal
indicator preserves order. Hence the reachability Bellman operator is
monotone: `TV<=TW`.

For a super-solution:

```text
V_0^* <= U_0
V_b^* <= U_b
=> V_(b+1)^* = T V_b^* <= T U_b <= U_(b+1).
```

For a sub-solution:

```text
L_0 <= V_0^*
L_b <= V_b^*
=> L_(b+1) <= T L_b <= T V_b^* = V_(b+1)^*.
```

Natural-number induction establishes both statements for every finite horizon,
so `L_B(x0)<=V_B^*(x0)<=U_B(x0)` and the Definition 5 gap is
`U_B(x0)-L_B(x0)>=0`.

The exact proof kernel validates linear certificates for both generic steps.
Z3 finds both violating real assignments `unsat`. This is the theorem-level
evidence; no finite MDP enumeration is used to establish the result.

## Control and calibration

The nonvacuous calibration interval `[1/2,3/4]` contains exact value `2/3` and
has gap `1/4`; it illustrates Definition 5 but is explicitly not proof.

The negative control proposes `U_1=1/2` where `T U_0=V_1^*=2/3`. It violates
only the upper recurrence, the claimed bound fails, and the verifier exits `3`.
Z3 finds the bad bound `sat` without the recurrence and `unsat` when the
recurrence is restored.

## Reproduce and provenance

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Accepted commit:
`4173b12b8caeac468eeafb9bde9f8bd37a5f3c4f`. Hugging Face
`cpu-upgrade` (8 allocated vCPUs; 64 host logical CPUs visible),
one-process design, cumulative runner
1.704828 seconds, full job 21 seconds. Primary exit `0`, independent checker
exit `0`, negative control exit `3`.

## Raw result

```json
{
  "bellman_monotonicity_dependency_chain": true,
  "upper_induction_step_certificate": true,
  "lower_induction_step_certificate": true,
  "finite_horizon_induction_schema": true,
  "definition_5_endpoint_rule": true,
  "verdict": "VERIFIED"
}
```

Downloadable evidence:

- [claim contract](../../evidence/claim_3/claim_contract.json)
- [source audit](../../evidence/claim_3/source_audit.md)
- [complete proof](../../evidence/claim_3/proof_certificate.md)
- [primary verifier](../../evidence/claim_3/verify.py) and
  [its JSON output](../../evidence/claim_3/verifier_output.json)
- [raw combined primary/checker/control output](../../evidence/claim_3/raw_output.txt)
- [independent checker](../../evidence/claim_3/independent_checker.py) and
  [its JSON output](../../evidence/claim_3/independent_checker_output.json)
- [negative-control input](../../evidence/claim_3/negative_control.json) and
  [output](../../evidence/claim_3/negative_control_output.json)
- [method](../../evidence/claim_3/method.md),
  [limitations](../../evidence/claim_3/limitations.md), and
  [accepted evaluation](../../evidence/claim_3/EVAL.md)

## Limitations

The proof assumes the Bellman operator is well-defined. Policy-selector
existence and measurability are audited separately under Claim 2. The theorem
guarantees correctness of a supplied certificate, not that learned models
automatically produce a tight one.
