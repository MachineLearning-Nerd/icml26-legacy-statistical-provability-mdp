# Claim 6 source audit

Displayed Theorem 6 in arXiv v1 assumes a compact doubling domain, a uniformly
Lipschitz hypothesis class, bounded conditionally unbiased targets available at
each point, and squared-loss ERM (or Lemma 4's uniform-deviation guarantee). It
does not state any sampling-distribution lower bound, eta-net design, or target
Lipschitz condition.

Appendix F materially strengthens the setup: it requires an eta-net, replicated
conditionally independent labels at every net point, target Lipschitzness, and
a Lipschitz extension estimator. Those added assumptions prevent the
concentrated-query counterexample, but they are not assumptions of the displayed
Theorem 6 judged here.

The counterexample family uses `D=[0,1]`, `Q(z)=z`,
`H={h_zero(z)=0,h_identity(z)=z}`, and deterministic unbiased targets `Y(z)=z`.
Every training query is `z=0`. Both hypotheses are empirical risk minimizers, so
choosing `h_zero` is valid, yet its uniform error is one for every sample size.
The claimed statistical term tends to zero. Therefore no finite big-O constant
can make the displayed result true.
