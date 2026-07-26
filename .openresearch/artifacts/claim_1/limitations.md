# Limitations and deviations

- This is a proof-level reproduction of a universal topology theorem, not an
  empirical convergence plot.
- The machine checker validates the explicit dependency certificate and
  algebraic substeps; it trusts the named classical theorems under their stated
  compact-metric/finite-measure hypotheses. The complete instantiation of those
  hypotheses is written in `proof_certificate.md`.
- The result concerns all positive Borel measures of bounded mass, not only
  integer-valued empirical goal measures.
- The noncompact control is assumption-violating by design and is evidence for
  sensitivity, not a falsification of the theorem.
