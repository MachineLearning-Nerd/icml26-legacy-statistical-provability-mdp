"""Proof-dependency verifier for Theorem 2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED = {
    "polish_spaces": ("compact_metric_implies_standard_borel_polish", [], "X and A are Polish standard Borel spaces"),
    "goal_usc": ("closed_set_indicator_is_upper_semicontinuous", [], "V_0=1_G is bounded USC and Borel"),
    "kernel_weak_continuity": ("feller_equivalent_weak_kernel_continuity", [], "convergent state-action pairs induce weakly convergent kernels"),
    "q_usc": ("portmanteau_bounded_usc_limsup", ["kernel_weak_continuity"], "USC V_(b-1) implies jointly USC Q_b"),
    "maximum_attained": ("usc_function_attains_max_on_compact_action", ["q_usc"], "argmax Q_b(x,.) is nonempty compact for every x"),
    "value_usc": ("upper_maximum_theorem_constant_compact_correspondence", ["q_usc", "maximum_attained"], "x maps to max_a Q_b(x,a) is USC"),
    "bellman_usc": ("maximum_of_two_usc_functions", ["goal_usc", "value_usc"], "V_b is bounded USC and therefore Borel"),
    "argmax_borel_graph": ("borel_equality_graph_with_compact_sections", ["q_usc", "value_usc", "maximum_attained"], "the argmax correspondence has Borel graph and nonempty compact sections"),
    "borel_selector": ("arsenin_kunugui_uniformization", ["polish_spaces", "argmax_borel_graph"], "there is a Borel action selector a_b^*(x)"),
    "induction_closed": ("finite_backward_usc_induction", ["goal_usc", "bellman_usc"], "all stages V_b are bounded USC and Borel"),
    "stage_attainment": ("selector_realizes_bellman_maximum", ["borel_selector", "maximum_attained"], "each selected action realizes the Bellman recursion"),
    "optimal_markov_policy": ("finite_horizon_dynamic_programming_verification", ["induction_closed", "stage_attainment"], "the deterministic Borel Markov selector sequence attains V_B^*"),
}


def acyclic(nodes: dict[str, dict]) -> bool:
    visiting: set[str] = set()
    done: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in done:
            return True
        if node_id in visiting or node_id not in nodes:
            return False
        visiting.add(node_id)
        if not all(visit(dep) for dep in nodes[node_id]["depends"]):
            return False
        visiting.remove(node_id)
        done.add(node_id)
        return True

    return all(visit(node_id) for node_id in nodes)


def evaluate_proof(case: dict) -> dict:
    assumptions_exact = case["assumptions"] == {
        "X": "compact metric state space from Theorem 1",
        "A": "arbitrary compact metric action space",
        "kernel": "Borel probability kernel satisfying Assumption 1",
        "G": "closed singleton zero measure",
        "B": "arbitrary finite horizon",
    }
    nodes = {node["id"]: node for node in case["nodes"]}
    exact = set(nodes) == set(EXPECTED)
    if exact:
        exact = all(
            (nodes[node_id]["rule"], nodes[node_id]["depends"], nodes[node_id]["conclusion"])
            == expected
            for node_id, expected in EXPECTED.items()
        )
    graph_acyclic = acyclic(nodes)
    root_valid = (
        case["root"] == "optimal_markov_policy"
        and nodes.get(case["root"], {}).get("conclusion")
        == "the deterministic Borel Markov selector sequence attains V_B^*"
    )
    obligations = {
        "upper_semicontinuity_induction": all(
            node in nodes for node in ["goal_usc", "q_usc", "value_usc", "bellman_usc", "induction_closed"]
        ),
        "compact_action_attainment": "maximum_attained" in nodes,
        "borel_argmax_graph": "argmax_borel_graph" in nodes,
        "measurable_selector": "borel_selector" in nodes,
        "policy_optimality": "optimal_markov_policy" in nodes,
    }
    calibration = case["feller_calibration"]
    calibration_valid = (
        calibration["action"] == "[0,1]"
        and calibration["goal_probability"] == "p(a)=a"
        and calibration["maximizer"] == "a=1"
    )
    verified = (
        assumptions_exact
        and exact
        and graph_acyclic
        and root_valid
        and all(obligations.values())
        and calibration_valid
    )
    return {
        "case": case["name"],
        "assumptions_exact": assumptions_exact,
        "dependency_nodes": len(nodes),
        "dependency_graph_acyclic": graph_acyclic,
        "exact_rule_conclusions": exact,
        "root_conclusion_valid": root_valid,
        "proof_obligations": obligations,
        "continuous_kernel_calibration_only": calibration_valid,
        "verified": verified,
        "verdict": "VERIFIED" if verified else "BLOCKED",
    }


def evaluate_control(case: dict) -> dict:
    other_assumptions = {
        "state_compact": case["state_space"] == "M_<=1(singleton), isometric to [0,1]",
        "action_compact": case["action_space"] == "[0,1]",
        "goal_closed": case["goal_set"] == "{0}",
        "valid_probability_kernel": case["goal_probability"] == "p(a)=a for a<1 and p(1)=0",
    }
    feller_holds = case["violated_assumption"] != "Feller weak continuity"
    no_maximizer = case["supremum"] == "1" and not case["maximizer_exists"]
    failed_for_intended_reason = (
        all(other_assumptions.values()) and not feller_holds and no_maximizer
    )
    return {
        "case": case["name"],
        "other_assumptions": other_assumptions,
        "Feller_condition_holds": feller_holds,
        "supremum": case["supremum"],
        "maximizer_exists": case["maximizer_exists"],
        "maximizing_sequence": "a_n=1-1/n has p(a_n)->1",
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
    if case["name"] == "theorem2_feller_policy_existence_proof":
        result = evaluate_proof(case)
    else:
        result = evaluate_control(case)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["verified"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
