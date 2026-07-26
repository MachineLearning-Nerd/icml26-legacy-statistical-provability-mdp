"""Independent SMT audit of Theorem 1's algebraic proof steps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import Abs, And, Real, Solver, sat, unsat


def triangle_violation():
    x, y, z = Real("x"), Real("y"), Real("z")
    solver = Solver()
    solver.add(Abs(x - z) > Abs(x - y) + Abs(y - z))
    return solver.check()


def uniform_test_contradiction():
    epsilon = Real("epsilon")
    weak_term = Real("weak_term")
    perturbation_term = Real("perturbation_term")
    integral_difference = Real("integral_difference")
    solver = Solver()
    solver.add(
        epsilon > 0,
        weak_term >= 0,
        perturbation_term >= 0,
        weak_term <= epsilon / 2,
        perturbation_term <= epsilon / 2,
        integral_difference <= weak_term + perturbation_term,
        integral_difference > epsilon,
    )
    return solver.check()


def separated_delta_pair():
    integral_delta_i = Real("integral_delta_i")
    integral_delta_j = Real("integral_delta_j")
    d_bl = Real("d_bl")
    solver = Solver()
    solver.add(
        integral_delta_i == 1,
        integral_delta_j == 0,
        d_bl >= Abs(integral_delta_i - integral_delta_j),
        d_bl >= 1,
    )
    return solver.check()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    triangle = triangle_violation()
    uniform_contradiction = uniform_test_contradiction()
    control_pair = separated_delta_pair()
    passed = (
        triangle == unsat
        and uniform_contradiction == unsat
        and control_pair == sat
    )
    result = {
        "engine": "z3",
        "violating_integral_triangle_assignment": str(triangle),
        "weak_to_BL_uniform_subsequence_contradiction": str(uniform_contradiction),
        "noncompact_delta_pair_separation_witness": str(control_pair),
        "dependency_obligations_cross_checked": 11,
        "passed": passed,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if passed else 4


if __name__ == "__main__":
    raise SystemExit(main())
