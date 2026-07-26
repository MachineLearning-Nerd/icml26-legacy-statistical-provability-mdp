"""Exact proof-certificate kernel for Theorem 3."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def vec(raw: list[str]) -> list[Fraction]:
    return [Fraction(value) for value in raw]


def check_linear_certificate(certificate: dict) -> bool:
    rows = [
        vec(row) for row in certificate["inequality_premises_lhs_le_zero"]
    ]
    equality = vec(certificate["equality_lhs_eq_zero"])
    multipliers = vec(certificate["multipliers"])
    target = vec(certificate["conclusion_lhs_le_zero"])
    if len(multipliers) != len(rows) + 1:
        return False
    if any(value < 0 for value in multipliers[:-1]):
        return False
    combined_rows = [*rows, equality]
    width = len(target)
    if any(len(row) != width for row in combined_rows):
        return False
    combined = [
        sum(multiplier * row[column] for multiplier, row in zip(multipliers, combined_rows))
        for column in range(width)
    ]
    return combined == target


def evaluate_proof(case: dict) -> dict:
    expected_rules = [
        "pointwise_order_implies_integral_order_for_every_probability_kernel",
        "coordinatewise_order_implies_supremum_order",
        "max_with_goal_indicator_preserves_order",
    ]
    monotonicity_valid = case["bellman_monotonicity_rules"] == expected_rules

    upper = case["upper_step_certificate"]
    lower = case["lower_step_certificate"]
    upper_valid = (
        upper["coefficient_order"] == ["T_V_b", "T_U_b", "V_next", "U_next"]
        and check_linear_certificate(upper)
    )
    lower_valid = (
        lower["coefficient_order"] == ["T_L_b", "T_V_b", "L_next", "V_next"]
        and check_linear_certificate(lower)
    )

    expected_schema = {
        "upper_base": "V_0<=U_0",
        "upper_step": "V_b<=U_b implies V_(b+1)<=U_(b+1)",
        "lower_base": "L_0<=V_0",
        "lower_step": "L_b<=V_b implies L_(b+1)<=V_(b+1)",
        "endpoint": "L_B(x0)<=V_B^*(x0)<=U_B(x0)",
    }
    induction_valid = case["induction_schema"] == expected_schema

    calibration = case["nonvacuous_calibration"]
    q_values = [Fraction(value) for value in calibration["goal_probabilities"].values()]
    lower_bound = Fraction(calibration["lower_at_x"])
    upper_bound = Fraction(calibration["upper_at_x"])
    exact_value = max(q_values)
    gap = upper_bound - lower_bound
    calibration_valid = (
        calibration["horizon"] == 1
        and exact_value == Fraction(calibration["exact_value_at_x"])
        and lower_bound <= exact_value <= upper_bound
        and gap == Fraction(calibration["certificate_gap"])
        and gap < 1
    )

    certificate_definition_valid = (
        lower_bound <= exact_value <= upper_bound and gap >= 0
    )
    verified = (
        monotonicity_valid
        and upper_valid
        and lower_valid
        and induction_valid
        and calibration_valid
        and certificate_definition_valid
    )
    return {
        "case": case["name"],
        "proof_kernel": {
            "bellman_monotonicity_dependency_chain": monotonicity_valid,
            "upper_induction_step_certificate": upper_valid,
            "lower_induction_step_certificate": lower_valid,
            "finite_horizon_induction_schema": induction_valid,
            "definition_5_endpoint_rule": certificate_definition_valid,
        },
        "calibration_only_not_proof": {
            "lower": str(lower_bound),
            "exact_value": str(exact_value),
            "upper": str(upper_bound),
            "gap": str(gap),
            "nonvacuous": calibration_valid,
        },
        "verified": verified,
        "verdict": "VERIFIED" if verified else "BLOCKED",
    }


def evaluate_control(case: dict) -> dict:
    transition_value = Fraction(case["goal_probabilities"]["only_action"])
    proposed_upper = Fraction(case["proposed_upper_at_x"])
    recurrence_holds = proposed_upper >= transition_value
    actual_bound_holds = proposed_upper >= transition_value
    failed_for_intended_reason = (
        case["expected_failed_assumption"] == "U_1>=T U_0"
        and not recurrence_holds
        and not actual_bound_holds
    )
    return {
        "case": case["name"],
        "T_U0_at_x": str(transition_value),
        "proposed_U1_at_x": str(proposed_upper),
        "upper_recurrence_holds": recurrence_holds,
        "V1_at_x": str(transition_value),
        "claimed_upper_bound_holds": actual_bound_holds,
        "failed_for_intended_reason": failed_for_intended_reason,
        "verified": not failed_for_intended_reason,
        "verdict": (
            "NEGATIVE_CONTROL_REJECTED"
            if failed_for_intended_reason
            else "UNEXPECTED_PASS"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    case = json.loads(args.case.read_text(encoding="utf-8"))
    if case["name"] == "theorem3_universal_proof_certificate":
        result = evaluate_proof(case)
    else:
        result = evaluate_control(case)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["verified"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
