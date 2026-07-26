# Claim 2 — current verification

## Result: VERIFIED

This proof-level route supersedes finite backward induction on six states,
which remains preserved as **Historical rejected baseline**. It targets
arXiv-v1 Assumption 1 and Theorem 2, including Borel measurability and selector
existence—not merely finite values.

## Assumptions and Quantifiers

For **every** finite horizon, compact metric state and action spaces, closed
goal set, and transition kernel satisfying Assumption 1's Feller continuity,
the contract requires an optimal deterministic Markov policy and the stated
Borel/upper-semicontinuous Bellman objects for **every** initial state.

## Universal existence proof

The closed-goal indicator `V_0=1_G` is bounded upper semicontinuous (USC).
Assuming `V_(b-1)` is bounded USC, Feller continuity makes convergent
state-action pairs induce weakly convergent kernels. Portmanteau gives

```text
limsup_n integral V_(b-1) dP(.|x_n,a_n)
 <= integral V_(b-1) dP(.|x,a),
```

so `Q_b` is jointly USC. A USC function attains its maximum on compact `A`,
and the upper maximum theorem makes `x -> max_a Q_b(x,a)` USC. Taking the
maximum with `1_G` closes the bounded-USC/Borel induction.

For policy existence, the argmax graph
`{(x,a): Q_b(x,a)=max_a Q_b(x,a)}` is Borel with nonempty compact sections.
Compact metric state/action spaces are standard Borel, so Arsenin–Kunugui
supplies a Borel selector. Selecting one at every finite stage realizes the
Bellman maxima; backward verification proves that the resulting deterministic
Markov policy attains `V_B^*`.

The primary checker validates all 12 dependencies. The independent Z3 route
finds the Portmanteau and selected-Bellman violations `unsat`.

## Negative control

Let both state and action spaces remain compact and keep the goal closed, but
use one-step goal probability `p(a)=a` for `a<1` and `p(1)=0`. This is a valid
Borel kernel that violates Feller continuity. Its success supremum is one, but
no action attains it. The control exits `3`, and Z3 reports no maximizer
(`unsat`). Restoring continuous `p(a)=a` makes `a=1` an exact maximizer
(`sat`).

## Reproduce and provenance

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Accepted commit:
`dc408b512f61e5922a190f55d14efcf4046086f2`. Hugging Face
`cpu-upgrade` (8 allocated vCPUs; 64 host logical CPUs visible),
one-process design, cumulative runner
1.875989 seconds, full job 21 seconds. Primary exit `0`, independent checker
exit `0`, negative control exit `3`.

## Raw result

```json
{
  "dependency_nodes": 12,
  "upper_semicontinuity_induction": true,
  "compact_action_attainment": true,
  "borel_argmax_graph": true,
  "measurable_selector": true,
  "policy_optimality": true,
  "verdict": "VERIFIED"
}
```

Downloadable evidence:

- [claim contract](../../evidence/claim_2/claim_contract.json)
- [source audit](../../evidence/claim_2/source_audit.md)
- [complete proof](../../evidence/claim_2/proof_certificate.md)
- [primary verifier](../../evidence/claim_2/verify.py) and
  [its JSON output](../../evidence/claim_2/verifier_output.json)
- [raw combined primary/checker/control output](../../evidence/claim_2/raw_output.txt)
- [independent checker](../../evidence/claim_2/independent_checker.py) and
  [its JSON output](../../evidence/claim_2/independent_checker_output.json)
- [negative-control input](../../evidence/claim_2/negative_control.json) and
  [output](../../evidence/claim_2/negative_control_output.json)
- [method](../../evidence/claim_2/method.md),
  [limitations](../../evidence/claim_2/limitations.md), and
  [accepted evaluation](../../evidence/claim_2/EVAL.md)

## Limitations

The executable checker validates the dependency structure and symbolic
implications while trusting Portmanteau, the upper maximum theorem, and
Arsenin–Kunugui under their audited hypotheses. The theorem is existential; it
does not promise an efficient selector algorithm.
