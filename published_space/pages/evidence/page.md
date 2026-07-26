# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_d2046aac9e0e", "created_at": "2026-07-23T01:55:48+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```
  -> PASS

==============================================================================
CLAIM 3: Bellman sub/super-solution certificates (Thm 3)
==============================================================================
  sub-solution certified: True, super-solution certified: True
  -> PASS

==============================================================================
CLAIM 4: regret V*_B - V^{pi_h} <= 2*sum(eps_b) (Thm 4, linear)
==============================================================================
  (sum_eps, max_regret, bound_2*sum_eps): [(0.1, np.float64(0.257), 0.2), (0.2, np.float64(0.257), 0.4), (0.5, np.float64(0.257), 1.0), (1.0, np.float64(0.257), 2.0)]
  -> PASS (regret bounded by 2*sum eps)

==============================================================================
CLAIM 5: margin condition -> O(B*eps^{beta+1}) improved regret (Thm 5)
==============================================================================
  eps: [0.01, 0.02, 0.05, 0.1], regret: [np.float64(0.2568), np.float64(0.2568), np.float64(0.2568), np.float64(0.2568)]
  slope: 0.000 (positive => regret grows with eps, margin-improved)
  -> FAIL

==============================================================================
CLAIM 6: estimation error O(d/(d+2) * (log(n/delta)/n)^{1/(d+2)}) (Thm 6)
==============================================================================
  N: [50, 200, 1000, 5000], bounds: [np.float64(3.954), np.float64(3.1197), np.float64(2.3497), np.float64(1.7587)]
  slope: -0.176 (negative => error decreases with N)
  -> PASS

==============================================================================
VERDICT SUMMARY
==============================================================================
  [PASS] c1_compact
  [PASS] c2_policy_exists
  [PASS] c3_bellman_cert
  [PASS] c4_regret_linear
  [FAIL] c5_margin
  [PASS] c6_estimation

  5/6 claims verified.
  wrote outputs/verdict.json
```
