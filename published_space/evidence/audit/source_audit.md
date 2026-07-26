# Paper source and version audit

Retrieval date: 2026-07-26 UTC

The live judge's six claims correspond to the theorem-numbered ar5iv rendering,
not to the substantially rewritten arXiv v3 text returned by alphaXiv. The
campaign therefore treats arXiv v1 as the judged claim contract and records v3
as a separate current-paper interpretation. Results must never mix the two.

## Retrieved sources

| Source | Effective URL | SHA-256 |
| --- | --- | --- |
| ar5iv HTML | `https://ar5iv.labs.arxiv.org/html/2602.10538` | `5cafb5b0f293d4044f87323a8e3bc6b48788996363e12681e6a6a819025fc577` |
| ar5iv HTML with v1 suffix | `https://ar5iv.labs.arxiv.org/html/2602.10538v1` | `5cafb5b0f293d4044f87323a8e3bc6b48788996363e12681e6a6a819025fc577` |
| arXiv source v1 | `https://export.arxiv.org/src/2602.10538v1` | `bfb1bcbb7c9a5bb375c15b379917cb22d0b70127c05d9d9afbfc128ff829297f` |
| arXiv source v3 | `https://export.arxiv.org/src/2602.10538v3` | `ba30962d80ae1725cccd6e2fdba44abdf94485dd63ffb5081e2e5666af6abd9e` |

The HTML requests used the explicit User-Agent
`Mozilla/5.0 (compatible; OpenResearch-Reproduction/1.0; +https://openresearch.dev)`.

## Judged v1 theorem contracts

1. Anchor `#Thmtheorem1`, Section 3.2: for every compact metric goal space
   `G` and finite cap `W`, the positive finite measures with mass at most `W`
   form a compact metric space under `d_BL`.
2. Anchors `#Thmassumption1` and `#Thmtheorem2`, Section 4: for every finite
   horizon `B`, compact state/action spaces, weakly continuous kernel, and
   closed goal set `{0}`, each Bellman action supremum is attained and an
   optimal deterministic Markov policy exists.
3. Anchor `#Thmtheorem3` and Definition 5, Section 5: for every pair of
   `[0,1]`-valued function sequences satisfying the stated base and Bellman
   inequalities at every depth `0,...,B-1`, the upper sequence bounds `V*`
   from above and the lower sequence bounds it from below at every depth.
4. Anchors `#Thmassumption2` and `#Thmtheorem4`, Section 6.2: for every initial
   state whose relevant trajectories stay in the uniform-error domain,
   `0 <= V*_B(x0)-V^pi_h_B(x0) <= 2 sum_b epsilon_b`.
5. Anchors `#Thmassumption3` and `#Thmtheorem5`, Section 6.4: if the uniform
   score error and the occupancy small-margin tail both hold, then a top-k
   policy (and similarly a beam preserving top-k) has expected regret at most
   a constant times `sum_b epsilon_b^(beta+1)`.
6. Anchors `#Thmassumption4`, `#Thmassumption5`, and `#Thmtheorem6`, Section
   7.2: on a compact doubling domain with a uniformly Lipschitz score class,
   bounded conditionally unbiased targets and squared-loss ERM are claimed to
   imply a high-probability uniform error of approximation error plus
   `O(L_H^(d/(d+2)) (log(n/delta)/n)^(1/(d+2)))`.

Appendix F adds material assumptions absent from the displayed Theorem 6:
an explicit eta-net, replicated conditionally independent labels at every net
point, Lipschitz regularity of the target, and a Lipschitz extension estimator.
This discrepancy must be tested directly rather than hidden.
