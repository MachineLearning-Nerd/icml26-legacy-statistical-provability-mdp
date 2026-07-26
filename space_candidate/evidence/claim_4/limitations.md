# Limitations and deviations

- This is a proof-level reconstruction of the mathematical theorem, not an
  empirical planner benchmark. A universally quantified theorem cannot be
  established by a parameter sweep.
- The proof relies on the paper's domain clause covering all actions used in
  each greedy comparison and every continuation state reached by the policy.
- The certificate establishes the stated worst-case upper bound. It makes no
  claim that ordinary learned scores attain worst-case equality.
- The proof does not validate the paper's separate top-k/beam fast-rate claim;
  Claim 5 is audited independently.
