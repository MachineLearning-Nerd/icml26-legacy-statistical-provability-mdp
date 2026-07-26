# Limitations and deviations

- This is a proof-level reproduction of a universal existence theorem, not a
  finite backward-induction benchmark.
- The machine checker validates the dependency structure and symbolic
  implications while trusting Portmanteau, the upper maximum theorem, and
  Arsenin–Kunugui under their explicitly audited hypotheses.
- The theorem ensures existence of a Borel stage-dependent deterministic
  Markov policy; it does not provide a computationally efficient selector.
- The non-Feller construction deliberately violates one assumption and is a
  sensitivity control, not a falsification.
