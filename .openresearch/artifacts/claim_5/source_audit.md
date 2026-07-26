# Claim 5 source audit

Source: arXiv v1, Section 6.4, anchors `Thmassumption3` and `Thmtheorem5`.

The theorem quantifies over “a top-k policy” but Section 6.1 defines only the
top-k candidate set. It imposes no rule requiring the deployed policy to choose
the best candidate or to exhaustively verify all candidates. Appendix D gives a
complete argument only for the plug-in greedy case (`k=1`) and says the top-k
case is the same. That extension is not valid for an arbitrary policy selecting
inside a top-k set.

The counterexample uses `B=1`, `k=2`, exact scores (`epsilon=0`), and a strict
best-versus-third action gap of one. Thus the occupancy margin tail is zero for
every sufficiently small positive threshold, while a permitted action selected
from the top-2 set has regret one. The displayed right-hand side is zero for
every finite theorem constant.

This falsifies the literal top-k theorem. It does not falsify the separately
derived greedy (`k=1`) result or a strengthened beam theorem that explicitly
requires exhaustive verification of every preserved candidate.
