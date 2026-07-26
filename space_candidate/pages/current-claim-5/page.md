# Claim 5 — current verification

## Result: FALSIFIED

This page supersedes the old six-state margin sweep, which remains preserved as
**Historical rejected baseline**. The current verifier targets the exact
arXiv-v1 top-k theorem at source anchor `Thmtheorem5`.

The theorem says that uniform score error plus a small-margin occupancy tail
gives expected top-k regret bounded by a finite constant times
`sum_b epsilon_b^(beta+1)`. The paper defines the top-k candidate set but does
not require a policy to choose the best member or exhaustively verify every
member.

## Assumptions and Quantifiers

The displayed theorem quantifies over score-guided top-`k` policies meeting its
uniform score-error and margin-tail conditions and asserts a finite-constant
bound for all sufficiently small errors. The literal contract therefore
allows any selected action in the defined top-`k` set; the witness satisfies
every stated premise at `epsilon=0` yet contradicts the bound.

## Assumption audit and contradiction

| Quantity | Exact value |
| --- | ---: |
| Horizon | 1 |
| State/action spaces | finite, hence compact |
| Optimal action values | `[1, 0, 0]` |
| Scores | `[1, 0, 0]` |
| Uniform error `epsilon` | 0 |
| Top-2 set | `[a_opt, a_bad]` |
| Selected action | `a_bad` |
| `(k+1)` gap | 1 |
| Margin tail for every `0<t<1` | 0 |
| Expected regret | 1 |
| Claimed RHS for any finite `C` | 0 |

All stated assumptions hold, but `1 <= 0` is false. This is a complete finite
counterexample to the universal statement, not toy corroboration.

## Reproduce

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

Accepted commit:
`73a1ac12198435251a8dc602f405a9eb42339283` on Hugging Face
`cpu-upgrade`, which allocates 8 vCPUs. Python exposed 64 host logical CPUs to
the container; the deterministic checker used one process. Cumulative
verification took 0.870154 seconds; full job
duration was 21 seconds.

Primary exact-rational verifier: exit `0`. Independent Z3 checker:
counterexample `sat`, optimal-action control `unsat`, exit `0`. Negative-control
primary verifier: exit `3` as required.

## Raw output

```json
{
  "uniform_error": "0",
  "top_k": ["a_opt", "a_bad"],
  "selected_action": "a_bad",
  "k_plus_one_gap": "1",
  "regret": "1",
  "claimed_rhs_for_every_finite_C": "0",
  "contradiction": true,
  "verdict": "FALSIFIED"
}
```

Downloadable evidence:

- [claim contract](../../evidence/claim_5/claim_contract.json)
- [source audit](../../evidence/claim_5/source_audit.md)
- [primary verifier](../../evidence/claim_5/verify.py) and
  [its JSON output](../../evidence/claim_5/verifier_output.json)
- [raw combined primary/checker/control output](../../evidence/claim_5/raw_output.txt)
- [independent checker](../../evidence/claim_5/independent_checker.py) and
  [its JSON output](../../evidence/claim_5/independent_checker_output.json)
- [counterexample input](../../evidence/claim_5/counterexample.json)
- [negative-control input](../../evidence/claim_5/negative_control.json) and
  [output](../../evidence/claim_5/negative_control_output.json)
- [method](../../evidence/claim_5/method.md),
  [limitations](../../evidence/claim_5/limitations.md), and
  [accepted evaluation](../../evidence/claim_5/EVAL.md)

## Limitations

The result falsifies the literal displayed top-k theorem. It does not falsify
the appendix's narrower plug-in greedy (`k=1`) derivation or a strengthened
beam theorem that explicitly requires exhaustive verification of preserved
candidates.
