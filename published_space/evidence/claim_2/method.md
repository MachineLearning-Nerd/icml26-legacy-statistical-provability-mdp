# Method

The primary checker validates a complete 12-node dependency certificate from
the Feller assumption and closed goal through USC induction, compact
attainment, Borel graph construction, measurable selection, and policy
optimality. Missing or cyclic dependencies fail.

The independent Z3 route audits the Portmanteau implication algebra, Bellman
attainment equality, and the control's nonattainment.

The negative control keeps compact state/action spaces, a closed goal, and a
valid Borel probability kernel, but uses
`p(a)=a` for `a<1` and `p(1)=0`. Its one-step success supremum is one but no
action attains it, and the Feller condition fails. Restoring the continuous
kernel `p(a)=a` makes `a=1` an exact maximizer. The control must exit nonzero.
