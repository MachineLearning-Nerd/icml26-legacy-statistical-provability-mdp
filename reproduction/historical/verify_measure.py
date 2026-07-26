"""Historical six-claim toy checker from the judged Space.

The code is preserved as a regression control. Its PASS labels are legacy
labels and must not be interpreted as VERIFIED theorem claims.
"""

from __future__ import annotations

import json
import os

import numpy as np

from reproduction.historical import measure_mdp as M


def banner(text: str) -> None:
    print("\n" + "=" * 78 + f"\n{text}\n" + "=" * 78, flush=True)


def main() -> int:
    out = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
    os.makedirs(out, exist_ok=True)
    results: dict[str, dict] = {}

    rng = np.random.default_rng(42)
    states, actions, horizon, gamma = 6, 3, 10, 0.9
    goal = {5}
    transition = np.zeros((states, actions, states))
    for state in range(states):
        for action in range(actions):
            transition[state, action] = rng.dirichlet(np.ones(states))
    reward = np.zeros((states, actions))
    reward[5, :] = 1.0
    value_opt, policy_opt = M.solve_mdp_backward(
        transition, reward, gamma, goal, horizon
    )
    print(
        f"MDP: S={states}, A={actions}, H={horizon}, gamma={gamma}, "
        f"goal={goal}, V*={np.round(value_opt, 3)}"
    )

    banner("CLAIM 1: finite measures with bounded mass form compact metric space")
    measures = [rng.dirichlet(np.ones(states)) for _ in range(20)]
    distances = [
        np.sum(np.abs(measures[i] - measures[j]))
        for i in range(len(measures))
        for j in range(i + 1, len(measures))
    ]
    claim_1 = bool(np.max(distances) < 5.0)
    print(
        f"  TV-proxy range: [{np.min(distances):.4f}, "
        f"{np.max(distances):.4f}]"
    )
    print(f"  -> {'PASS' if claim_1 else 'FAIL'} (legacy proxy label)")
    results["c1_compact"] = {
        "passed": claim_1,
        "max_dist": float(np.max(distances)),
    }

    banner("CLAIM 2: optimal deterministic Markov policies exist")
    claim_2 = bool(
        np.all(np.isfinite(value_opt))
        and np.all(np.isfinite(policy_opt))
        and len(policy_opt) == states
    )
    print(f"  -> {'PASS' if claim_2 else 'FAIL'} (finite toy only)")
    results["c2_policy_exists"] = {
        "passed": claim_2,
        "value": value_opt.tolist(),
    }

    banner("CLAIM 3: Bellman sub/super-solution certificates")
    lower_funcs = [
        np.maximum(value_opt - 0.1 * (horizon - depth), 0)
        for depth in range(horizon)
    ]
    upper_funcs = [
        np.minimum(value_opt + 0.1 * (horizon - depth), 1.0)
        for depth in range(horizon)
    ]
    lower_ok, upper_ok = M.bellman_certificate(
        transition,
        reward,
        gamma,
        goal,
        horizon,
        lower_funcs,
        upper_funcs,
    )
    claim_3 = lower_ok or upper_ok
    print(f"  sub={lower_ok}, super={upper_ok}")
    print(f"  -> {'PASS' if claim_3 else 'FAIL'} (constructed around V*)")
    results["c3_bellman_cert"] = {
        "passed": bool(claim_3),
        "lower": lower_ok,
        "upper": upper_ok,
    }

    banner("CLAIM 4: regret <= 2*sum(eps_b)")
    scores = np.random.default_rng(1).standard_normal((states, actions))
    error_sets = [[error] * horizon for error in [0.01, 0.02, 0.05, 0.1]]
    regret_data = []
    for errors in error_sets:
        _, _, regret, _ = M.score_guided_planning(
            transition, reward, gamma, goal, horizon, scores, errors
        )
        regret_data.append((sum(errors), float(np.max(regret)), 2 * sum(errors)))
    claim_4 = all(regret <= bound + 0.5 for _, regret, bound in regret_data)
    print(f"  (sum_eps, max_regret, bound): {regret_data}")
    print(f"  -> {'PASS' if claim_4 else 'FAIL'} (+0.5 legacy tolerance)")
    results["c4_regret_linear"] = {
        "passed": bool(claim_4),
        "data": [
            {"sum_eps": eps, "regret": regret, "bound": bound}
            for eps, regret, bound in regret_data
        ],
    }

    banner("CLAIM 5: margin condition fast rate")
    eps_values = [0.01, 0.02, 0.05, 0.1]
    regrets = []
    for error in eps_values:
        _, _, regret, _ = M.score_guided_planning(
            transition,
            reward,
            gamma,
            goal,
            horizon,
            scores,
            [error] * horizon,
        )
        regrets.append(float(np.max(regret)))
    slope, _ = np.polyfit(
        np.log(eps_values), np.log(np.maximum(regrets, 1e-6)), 1
    )
    claim_5 = bool(slope > 0.5)
    print(f"  eps={eps_values}, regret={regrets}, slope={slope:.6f}")
    print(f"  -> {'PASS' if claim_5 else 'FAIL'}")
    results["c5_margin"] = {"passed": claim_5, "slope": float(slope)}

    banner("CLAIM 6: displayed estimation formula decreases")
    dimension, lipschitz, delta = 3, 1.0, 0.1
    sample_sizes = [50, 200, 1000, 5000]
    displayed_bounds = [
        lipschitz
        * horizon
        * dimension
        / (dimension + 2)
        * (np.log(sample_size / delta) / sample_size)
        ** (1.0 / (dimension + 2))
        for sample_size in sample_sizes
    ]
    slope_6, _ = np.polyfit(np.log(sample_sizes), np.log(displayed_bounds), 1)
    claim_6 = bool(slope_6 < -0.1)
    print(
        f"  N={sample_sizes}, formula={displayed_bounds}, slope={slope_6:.6f}"
    )
    print(f"  -> {'PASS' if claim_6 else 'FAIL'} (formula by construction)")
    results["c6_estimation"] = {
        "passed": claim_6,
        "slope": float(slope_6),
        "bounds": displayed_bounds,
    }

    banner("LEGACY SUMMARY")
    passed = sum(1 for result in results.values() if result.get("passed"))
    print(f"  Legacy script labels: {passed}/{len(results)} PASS")
    print("  Live judge: claims 1-4 TOY; claims 5-6 INCONCLUSIVE; score 4/12")
    with open(os.path.join(out, "verdict.json"), "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
