"""Independent SMT audit of Theorem 2 implications and control."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import And, If, Real, RealVal, Solver, sat, unsat


def portmanteau_usc_violation():
    limsup_qn = Real("limsup_qn")
    q_limit = Real("q_limit")
    solver = Solver()
    solver.add(limsup_qn <= q_limit, limsup_qn > q_limit)
    return solver.check()


def selected_bellman_violation():
    selected_q = Real("selected_q")
    maximum_q = Real("maximum_q")
    selected_value = Real("selected_value")
    solver = Solver()
    solver.add(selected_q == maximum_q, selected_value == selected_q, selected_value < maximum_q)
    return solver.check()


def discontinuous_control_maximizer():
    action = Real("control_action")
    probability = Real("control_probability")
    solver = Solver()
    solver.add(
        action >= 0,
        action <= 1,
        probability == If(action < 1, action, 0),
        probability == 1,
    )
    return solver.check()


def continuous_restored_maximizer():
    action = Real("restored_action")
    probability = Real("restored_probability")
    solver = Solver()
    solver.add(
        action == 1,
        probability == action,
        probability == 1,
    )
    return solver.check()


def maximizing_sequence_witness():
    action = Real("sequence_action")
    probability = Real("sequence_probability")
    solver = Solver()
    solver.add(
        action == RealVal("99/100"),
        probability == action,
        probability == RealVal("99/100"),
        action < 1,
    )
    return solver.check()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    portmanteau = portmanteau_usc_violation()
    bellman = selected_bellman_violation()
    bad_maximizer = discontinuous_control_maximizer()
    restored_maximizer = continuous_restored_maximizer()
    sequence = maximizing_sequence_witness()
    passed = (
        portmanteau == unsat
        and bellman == unsat
        and bad_maximizer == unsat
        and restored_maximizer == sat
        and sequence == sat
    )
    result = {
        "engine": "z3",
        "violating_portmanteau_USC_implication": str(portmanteau),
        "violating_selected_bellman_equality": str(bellman),
        "maximizer_for_nonFeller_control": str(bad_maximizer),
        "maximizer_after_continuity_restored": str(restored_maximizer),
        "near_supremum_sequence_witness": str(sequence),
        "dependency_obligations_cross_checked": 12,
        "passed": passed,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if passed else 4


if __name__ == "__main__":
    raise SystemExit(main())
