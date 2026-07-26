"""Independent SMT reconstruction of Theorem 4's arithmetic obligations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import Abs, And, Real, RealVal, Solver, sat, unsat


def one_step_violation():
    q_opt, q_greedy = Real("q_opt"), Real("q_greedy")
    h_opt, h_greedy = Real("h_opt"), Real("h_greedy")
    epsilon = Real("epsilon")
    solver = Solver()
    solver.add(
        And(
            q_opt >= 0,
            q_opt <= 1,
            q_greedy >= 0,
            q_greedy <= 1,
            h_opt >= 0,
            h_opt <= 1,
            h_greedy >= 0,
            h_greedy <= 1,
            epsilon >= 0,
            q_opt >= q_greedy,
            h_greedy >= h_opt,
            Abs(h_opt - q_opt) <= epsilon,
            Abs(h_greedy - q_greedy) <= epsilon,
            q_opt - q_greedy > 2 * epsilon,
        )
    )
    return solver.check()


def recurrence_violation():
    regret = Real("regret")
    one_step = Real("one_step")
    continuation = Real("continuation")
    previous = Real("previous")
    epsilon = Real("epsilon_b")
    solver = Solver()
    solver.add(
        epsilon >= 0,
        one_step <= 2 * epsilon,
        continuation <= previous,
        regret == one_step + continuation,
        regret > previous + 2 * epsilon,
    )
    return solver.check()


def tight_witness():
    epsilon = Real("witness_epsilon")
    q_opt = Real("witness_q_opt")
    q_bad = Real("witness_q_bad")
    h_opt = Real("witness_h_opt")
    h_bad = Real("witness_h_bad")
    solver = Solver()
    solver.add(
        epsilon == RealVal("1/4"),
        q_opt == RealVal("1/2"),
        q_bad == 0,
        h_opt == RealVal("1/4"),
        h_bad == RealVal("1/4"),
        Abs(h_opt - q_opt) <= epsilon,
        Abs(h_bad - q_bad) <= epsilon,
        h_bad >= h_opt,
        q_opt - q_bad == 2 * epsilon,
    )
    return solver.check()


def removed_assumption_control(require_uniform_error: bool):
    q_opt = Real("control_q_opt")
    q_bad = Real("control_q_bad")
    h_opt = Real("control_h_opt")
    h_bad = Real("control_h_bad")
    epsilon = Real("control_epsilon")
    solver = Solver()
    solver.add(
        q_opt == RealVal("1/2"),
        q_bad == 0,
        h_opt == 0,
        h_bad == 1,
        epsilon == 0,
        h_bad >= h_opt,
        q_opt - q_bad > 2 * epsilon,
    )
    if require_uniform_error:
        solver.add(
            Abs(h_opt - q_opt) <= epsilon,
            Abs(h_bad - q_bad) <= epsilon,
        )
    return solver.check()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    one_step = one_step_violation()
    recurrence = recurrence_violation()
    witness = tight_witness()
    control_without_assumption = removed_assumption_control(False)
    control_with_assumption = removed_assumption_control(True)
    passed = (
        one_step == unsat
        and recurrence == unsat
        and witness == sat
        and control_without_assumption == sat
        and control_with_assumption == unsat
    )
    result = {
        "engine": "z3",
        "violating_one_step_assignment": str(one_step),
        "violating_recurrence_assignment": str(recurrence),
        "tight_factor_two_witness": str(witness),
        "violation_when_uniform_error_omitted": str(control_without_assumption),
        "same_violation_when_uniform_error_restored": str(control_with_assumption),
        "passed": passed,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if passed else 4


if __name__ == "__main__":
    raise SystemExit(main())
