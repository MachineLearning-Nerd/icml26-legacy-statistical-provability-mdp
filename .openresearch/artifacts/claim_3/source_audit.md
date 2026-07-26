# Claim 3 source audit

ArXiv-v1 Theorem 3 at `Thmtheorem3` quantifies over arbitrary `[0,1]`-valued
function sequences for every finite horizon. Its only certificate premises are
the initial upper/lower inequalities and the stagewise Bellman
super-/sub-solution inequalities. Definition 5 at `Thmdefinition5` names the
endpoint interval and its difference.

The theorem is universally quantified, so a finite MDP demonstration cannot
verify it. The current route instead reconstructs Bellman monotonicity from
order preservation of integration, supremum, and maximum, then checks the
generic upper and lower induction steps symbolically. A finite rational example
is retained only to calibrate that the reported interval can be nonvacuous; it
is explicitly not the proof.
