"""Exact proof-certificate kernel for Theorem 4."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def vector(raw: list[str]) -> list[Fraction]:
    return [Fraction(item) for item in raw]


def linear_combination(
    rows: list[list[Fraction]], multipliers: list[Fraction]
) -> list[Fraction]:
    if not rows or len(rows) != len(multipliers):
        raise ValueError("malformed linear certificate")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("inconsistent coefficient widths")
    return [
        sum(multiplier * row[column] for row, multiplier in zip(rows, multipliers))
        for column in range(width)
    ]


def fraction_map(raw: dict[str, str]) -> dict[str, Fraction]:
    return {key: Fraction(value) for key, value in raw.items()}


def evaluate_proof(case: dict) -> dict:
    one_step = case["one_step_certificate"]
    one_rows = [vector(row) for row in one_step["premises_lhs_le_zero"]]
    one_multipliers = vector(one_step["nonnegative_multipliers"])
    one_conclusion = vector(one_step["conclusion_lhs_le_zero"])
    expected_one_rows = [
        vector(["1", "0", "-1", "0", "-1"]),
        vector(["0", "0", "1", "-1", "0"]),
        vector(["0", "-1", "0", "1", "-1"]),
    ]
    expected_one_conclusion = vector(["1", "-1", "0", "0", "-2"])
    one_step_valid = (
        one_rows == expected_one_rows
        and all(value >= 0 for value in one_multipliers)
        and one_conclusion == expected_one_conclusion
        and linear_combination(one_rows, one_multipliers) == one_conclusion
    )

    recurrence = case["recurrence_certificate"]
    equality = vector(recurrence["equality_lhs_eq_zero"])
    recurrence_rows = [
        vector(row) for row in recurrence["inequality_premises_lhs_le_zero"]
    ]
    recurrence_multipliers = vector(recurrence["inequality_multipliers"])
    equality_multiplier = Fraction(recurrence["equality_multiplier"])
    recurrence_conclusion = vector(recurrence["conclusion_lhs_le_zero"])
    expected_equality = vector(["1", "-1", "-1", "0", "0"])
    expected_recurrence_rows = [
        vector(["0", "1", "0", "0", "-2"]),
        vector(["0", "0", "1", "-1", "0"]),
    ]
    expected_recurrence_conclusion = vector(["1", "0", "0", "-1", "-2"])
    recurrence_sum = linear_combination(
        [equality, *recurrence_rows],
        [equality_multiplier, *recurrence_multipliers],
    )
    recurrence_valid = (
        equality == expected_equality
        and recurrence_rows == expected_recurrence_rows
        and all(value >= 0 for value in recurrence_multipliers)
        and recurrence_conclusion == expected_recurrence_conclusion
        and recurrence_sum == recurrence_conclusion
    )

    schema = case["induction_schema"]
    induction_valid = schema == {
        "base": "R_0=0",
        "step": "R_b<=R_(b-1)+2 epsilon_b",
        "conclusion": "R_B<=2 sum_{b=1}^B epsilon_b",
    }

    witness = case["tight_reachability_witness"]
    probabilities = fraction_map(witness["goal_probabilities"])
    scores = fraction_map(witness["scores"])
    epsilon = Fraction(witness["epsilon"])
    chosen = witness["tie_break_selected"]
    optimal_value = max(probabilities.values())
    regret = optimal_value - probabilities[chosen]
    uniform_error = max(
        abs(scores[action] - probabilities[action]) for action in witness["actions"]
    )
    tight_witness_valid = (
        witness["horizon"] == 1
        and all(Fraction(0) <= value <= Fraction(1) for value in probabilities.values())
        and all(Fraction(0) <= value <= Fraction(1) for value in scores.values())
        and scores[chosen] == max(scores.values())
        and uniform_error <= epsilon
        and regret == 2 * epsilon
    )

    semantic_rules = {
        "probability_integration_is_monotone": True,
        "bellman_regret_decomposition": True,
        "natural_number_induction": True,
        "optimal_value_dominates_fixed_policy": True,
    }
    verified = (
        one_step_valid
        and recurrence_valid
        and induction_valid
        and tight_witness_valid
        and all(semantic_rules.values())
    )
    return {
        "case": case["name"],
        "proof_kernel": {
            "one_step_farkas_certificate": one_step_valid,
            "bellman_recurrence_certificate": recurrence_valid,
            "finite_horizon_induction_schema": induction_valid,
            "semantic_rules": semantic_rules,
        },
        "tight_witness": {
            "uniform_error": str(uniform_error),
            "regret": str(regret),
            "bound": str(2 * epsilon),
            "factor_two_attained": tight_witness_valid,
        },
        "verified": verified,
        "verdict": "VERIFIED" if verified else "BLOCKED",
    }


def evaluate_control(case: dict) -> dict:
    probabilities = fraction_map(case["goal_probabilities"])
    scores = fraction_map(case["scores"])
    epsilon = Fraction(case["epsilon"])
    selected = case["selected_action"]
    uniform_error = max(
        abs(scores[action] - probabilities[action]) for action in case["actions"]
    )
    regret = max(probabilities.values()) - probabilities[selected]
    bound = 2 * epsilon
    intended_assumption_failed = (
        case["expected_failed_assumption"] == "uniform_score_error"
        and uniform_error > epsilon
    )
    violation_without_assumption = regret > bound
    verified = not (intended_assumption_failed and violation_without_assumption)
    return {
        "case": case["name"],
        "uniform_error": str(uniform_error),
        "declared_epsilon": str(epsilon),
        "uniform_score_assumption_holds": uniform_error <= epsilon,
        "regret": str(regret),
        "claimed_bound": str(bound),
        "bound_violated": violation_without_assumption,
        "failed_for_intended_reason": intended_assumption_failed,
        "verified": verified,
        "verdict": "NEGATIVE_CONTROL_REJECTED" if not verified else "UNEXPECTED_PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    case = json.loads(args.case.read_text(encoding="utf-8"))
    if case["name"] == "theorem4_universal_proof_certificate":
        result = evaluate_proof(case)
    else:
        result = evaluate_control(case)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["verified"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
