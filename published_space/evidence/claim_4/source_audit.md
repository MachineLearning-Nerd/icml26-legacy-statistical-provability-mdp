# Claim 4 source audit

The displayed arXiv-v1 Theorem 4 is at source anchor `Thmtheorem4`. Under
Assumption 2, each stage score obeys
`sup_(x,a) |h_b(x,a)-Q_b^*(x,a)| <= epsilon_b` on a compact relevant domain.
For every initial state whose relevant trajectories and actions remain in that
domain, the greedy score policy is claimed to satisfy

`0 <= V_B^*(x0)-V_B^pi(x0) <= 2 sum_(b=1)^B epsilon_b`.

The proof needs no finite-state restriction. At a greedy-policy state, uniform
error and score maximality give an optimal-Q one-step loss of at most
`2 epsilon_b`. The remaining difference is the transition-kernel expectation
of the previous-stage policy regret. Monotonicity of integration and induction
over the finite horizon give the sum. Nonnegativity follows because `V^*` is
the supremum over policies.

The phrase "relevant trajectories remain inside D" is interpreted to include
every action compared by the greedy maximization at every policy-reachable
state, exactly as required by Lemma 3.
