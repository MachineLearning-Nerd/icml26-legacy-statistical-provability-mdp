# Method

The primary verifier checks an 11-node proof certificate covering metric
separation, both directions of weak/BL topology equivalence, tightness,
Prokhorov subsequence extraction, closure of the mass-bounded cone, and the
metric sequential-compactness conclusion. It rejects missing, altered,
cyclic, or disconnected obligations.

The independent Z3 checker audits the scalar triangle inequality and the
epsilon contradiction used when a sequence of BL-unit tests is replaced by
its uniform limit.

The negative control replaces compact `K` by the natural numbers with the
discrete metric. The mass-one sequence `delta_n` is pairwise at least one apart
in `d_BL`, witnessed by a BL-unit singleton indicator, so it has no Cauchy
subsequence. This control must exit nonzero specifically because compactness
of `K` was removed.
