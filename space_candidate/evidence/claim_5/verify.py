"""Exact-rational verifier for the literal Theorem 5 counterexample."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def fraction(value: str | int) -> Fraction:
    return Fraction(str(value))


def check_distribution(distribution: dict[str, str]) -> bool:
    values = [fraction(value) for value in distribution.values()]
    return bool(values) and all(value >= 0 for value in values) and sum(values) == 1


def evaluate(case: dict) -> dict:
    states = case["states"]
    actions = case["actions"]
    goals = set(case["goal_states"])
    x0 = next(iter(case["initial_distribution"]))
    assumptions: dict[str, bool] = {}

    assumptions["finite_state_space_compact"] = len(states) > 0 and len(set(states)) == len(states)
    assumptions["finite_action_space_compact"] = len(actions) > 0 and len(set(actions)) == len(actions)
    assumptions["horizon_one"] = case["horizon"] == 1
    assumptions["initial_distribution_valid"] = check_distribution(
        case["initial_distribution"]
    )

    transition_rows = case["transitions"][x0]
    assumptions["all_transition_distributions_valid"] = all(
        check_distribution(transition_rows[action]) for action in actions
    )
    q_star = {
        action: sum(
            probability
            for state, raw_probability in transition_rows[action].items()
            if state in goals
            for probability in [fraction(raw_probability)]
        )
        for action in actions
    }
    scores = {
        action: fraction(value) for action, value in case["scores"][x0].items()
    }
    epsilon = fraction(case["epsilon"])
    uniform_error = max(abs(scores[action] - q_star[action]) for action in actions)
    assumptions["uniform_error_bound"] = uniform_error <= epsilon

    tie_rank = {action: rank for rank, action in enumerate(case["tie_order"])}
    ranked = sorted(actions, key=lambda action: (-scores[action], tie_rank[action]))
    k = int(case["k"])
    top_k = ranked[:k]
    selected = case["selected_action"]
    assumptions["selected_action_in_top_k"] = selected in top_k

    q_ranked = sorted(
        actions, key=lambda action: (-q_star[action], tie_rank[action])
    )
    best_value = q_star[q_ranked[0]]
    k_plus_one_value = q_star[q_ranked[k]]
    gap = best_value - k_plus_one_value
    t_upper = fraction(case["margin"]["small_t_upper_exclusive"])
    c_delta = fraction(case["margin"]["C_delta"])
    beta = fraction(case["margin"]["beta"])
    assumptions["positive_margin_parameters"] = c_delta > 0 and beta > 0
    assumptions["margin_tail_for_all_small_t"] = (
        t_upper > 0 and t_upper <= gap
    )

    policy_value = q_star[selected]
    regret = best_value - policy_value
    rhs_for_every_finite_constant = Fraction(0) if epsilon == 0 else None
    contradiction = (
        all(assumptions.values())
        and rhs_for_every_finite_constant == 0
        and regret > rhs_for_every_finite_constant
    )
    return {
        "case": case["name"],
        "assumptions": assumptions,
        "q_star": {key: str(value) for key, value in q_star.items()},
        "uniform_error": str(uniform_error),
        "epsilon": str(epsilon),
        "top_k": top_k,
        "selected_action": selected,
        "k_plus_one_gap": str(gap),
        "margin_tail_reason": (
            "Delta=1 almost surely, so P(Delta<=t)=0 for every 0<t<1."
        ),
        "regret": str(regret),
        "claimed_rhs_for_every_finite_C": str(rhs_for_every_finite_constant),
        "contradiction": contradiction,
        "verdict": "FALSIFIED" if contradiction else "NO_COUNTEREXAMPLE"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.case.read_text(encoding="utf-8")))
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["contradiction"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
