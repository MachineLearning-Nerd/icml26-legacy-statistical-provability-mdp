# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_408e1f12e435", "created_at": "2026-07-23T01:55:47+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Theorem 1 establishes that the space of finite measures with bounded mass forms a compact metric space under the bounded Lipschitz metric, providing the topological foundation for the measure-valued goal encoding of the reachability MDP (Theorem 1, Section 3).
2. Theorem 2 proves that under mild Feller-type continuity conditions on the transition kernel, optimal deterministic Markov policies exist for the finite-horizon time-bounded reachability MDP (Theorem 2).
3. Theorem 3 shows that sequences of functions satisfying Bellman sub-/super-solution inequalities yield provability certificates (upper and lower bounds on the optimal value function) without requiring the full MDP to be solved, with the certificate gap defined as UB(x0) - LB(x0) (Theorem 3, Definition 5, Section 5).
4. Theorem 4 bounds the worst-case regret of score-guided planning under uniform score-approximation error εb as 0 ≤ V*_B(x0) - V^{πh}_B(x0) ≤ 2∑_{b=1}^{B} εb, showing performance degrades linearly with accumulated approximation error (Theorem 4, Section 6).
5. Theorem 5 shows that under a margin condition on action-value separation, the expected regret improves to O(Bε^{β+1}) for β>0, i.e., faster than the worst-case linear-in-B rate of Theorem 4 (Theorem 5).
6. Theorem 6 derives a high-probability estimation-error bound of order O(L H d_D/(d_D+2) (log(n/δ)/n)^{1/(d_D+2)}) under a doubling-dimension assumption on the relevant problem domain, formalizing how statistical complexity of a biased real-world problem distribution governs sample efficiency (Theorem 6, Section 7).
