# Limitations and deviations

- This is a universal proof-level reconstruction rather than a benchmark.
- The proof assumes the bounded Bellman operator in the paper is well-defined.
  Existence/measurability of optimal selectors is the separate subject of
  Claim 2.
- A valid certificate may have a large gap; Theorem 3 guarantees correctness,
  not tightness. The calibration interval is nonvacuous but is not used as
  universal evidence.
- The verifier establishes the theorem's implication. It does not claim that a
  particular learned model automatically supplies useful sub-/super-solutions.
