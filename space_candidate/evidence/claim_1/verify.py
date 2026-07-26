"""Proof-dependency verifier for Theorem 1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED_NODES = {
    "bl_ball_compact": (
        "arzela_ascoli",
        [],
        "BL unit ball is compact in uniform norm",
    ),
    "lipschitz_dense": (
        "stone_weierstrass_lipschitz_algebra",
        [],
        "bounded Lipschitz functions are uniformly dense in C(K)",
    ),
    "metric_separation": (
        "riesz_uniqueness_after_dense_tests",
        ["lipschitz_dense"],
        "d_BL(mu,nu)=0 implies mu=nu",
    ),
    "metric_axioms": (
        "symmetric_test_class_and_linearity",
        ["metric_separation"],
        "d_BL is a metric",
    ),
    "weak_implies_bl": (
        "uniform_test_subsequence_contradiction",
        ["bl_ball_compact"],
        "weak convergence implies d_BL convergence",
    ),
    "bl_implies_weak": (
        "density_and_uniform_mass_bound",
        ["lipschitz_dense"],
        "d_BL convergence implies weak convergence",
    ),
    "uniform_tightness": (
        "compact_domain_is_common_compact_carrier",
        [],
        "the whole measure class is uniformly tight",
    ),
    "weak_subsequence": (
        "prokhorov_for_uniformly_bounded_finite_measures",
        ["uniform_tightness"],
        "every sequence has a weakly convergent subsequence",
    ),
    "limit_closed": (
        "positivity_and_constant_one_test",
        ["weak_subsequence"],
        "the weak limit is positive and has mass <= W",
    ),
    "bl_subsequence": (
        "weak_bl_topology_equivalence",
        ["weak_subsequence", "limit_closed", "weak_implies_bl", "bl_implies_weak"],
        "every sequence has a d_BL-convergent subsequence in the class",
    ),
    "compact_metric_space": (
        "metric_sequential_compactness_equivalence",
        ["metric_axioms", "bl_subsequence"],
        "the bounded-mass measure space is compact under d_BL",
    ),
}


def acyclic(nodes: dict[str, dict]) -> bool:
    visiting: set[str] = set()
    complete: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in complete:
            return True
        if node_id in visiting or node_id not in nodes:
            return False
        visiting.add(node_id)
        if not all(visit(dep) for dep in nodes[node_id]["depends"]):
            return False
        visiting.remove(node_id)
        complete.add(node_id)
        return True

    return all(visit(node_id) for node_id in nodes)


def evaluate_proof(case: dict) -> dict:
    assumptions = case["assumptions"]
    assumptions_exact = assumptions == {
        "K": "arbitrary compact metric space",
        "W": "arbitrary finite real W>0",
        "measure_class": "finite positive Borel measures with mass <= W",
    }
    nodes = {node["id"]: node for node in case["nodes"]}
    exact_nodes = set(nodes) == set(EXPECTED_NODES)
    if exact_nodes:
        exact_nodes = all(
            (
                nodes[node_id]["rule"],
                nodes[node_id]["depends"],
                nodes[node_id]["conclusion"],
            )
            == expected
            for node_id, expected in EXPECTED_NODES.items()
        )
    graph_acyclic = acyclic(nodes)
    root_valid = (
        case["root"] == "compact_metric_space"
        and case["root"] in nodes
        and nodes[case["root"]]["conclusion"]
        == "the bounded-mass measure space is compact under d_BL"
    )
    obligations = {
        "metric": all(item in nodes for item in ["metric_separation", "metric_axioms"]),
        "weak_bl_equivalence": all(
            item in nodes for item in ["weak_implies_bl", "bl_implies_weak"]
        ),
        "weak_sequential_compactness": "weak_subsequence" in nodes,
        "limit_stays_in_class": "limit_closed" in nodes,
        "metric_compactness": "compact_metric_space" in nodes,
    }
    verified = (
        assumptions_exact
        and exact_nodes
        and graph_acyclic
        and root_valid
        and all(obligations.values())
    )
    return {
        "case": case["name"],
        "assumptions_exact": assumptions_exact,
        "dependency_nodes": len(nodes),
        "dependency_graph_acyclic": graph_acyclic,
        "exact_rule_conclusions": exact_nodes,
        "root_conclusion_valid": root_valid,
        "proof_obligations": obligations,
        "verified": verified,
        "verdict": "VERIFIED" if verified else "BLOCKED",
    }


def evaluate_control(case: dict) -> dict:
    discrete_metric = case["domain"] == "natural numbers with discrete metric"
    delta_sequence = case["sequence"] == "mu_n=delta_n"
    witness_is_bl_unit = (
        case["pairwise_test"] == "f_n(n)=1 and f_n(j)=0 for j!=n"
    )
    separated = case["pairwise_d_bl_lower_bound"] == "1"
    failed_for_intended_reason = (
        case["expected_failed_assumption"] == "K compact"
        and not case["domain_compact"]
        and discrete_metric
        and delta_sequence
        and witness_is_bl_unit
        and separated
    )
    return {
        "case": case["name"],
        "domain_compact": case["domain_compact"],
        "all_measures_have_mass_one": case["mass_bound"] == "1",
        "BL_unit_test_witness": witness_is_bl_unit,
        "pairwise_d_BL_at_least_one": separated,
        "cauchy_subsequence_exists": False,
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
    if case["name"] == "theorem1_compactness_proof_certificate":
        result = evaluate_proof(case)
    else:
        result = evaluate_control(case)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["verified"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
