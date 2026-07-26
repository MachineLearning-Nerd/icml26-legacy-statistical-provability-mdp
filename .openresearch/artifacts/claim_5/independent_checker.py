"""Independent SMT check of the Theorem 5 counterexample and control."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import And, Real, Solver, sat, unsat


def counterexample_status(selected_value: int):
    q_opt = Real("q_opt")
    q_bad = Real("q_bad")
    q_third = Real("q_third")
    epsilon = Real("epsilon")
    regret = Real("regret")
    rhs = Real("rhs")
    solver = Solver()
    solver.add(
        And(
            q_opt == 1,
            q_bad == 0,
            q_third == 0,
            epsilon == 0,
            q_opt - q_third == 1,
            regret == q_opt - selected_value,
            rhs == 0,
            regret > rhs,
        )
    )
    return solver.check()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    primary = counterexample_status(selected_value=0)
    control = counterexample_status(selected_value=1)
    passed = primary == sat and control == unsat
    result = {
        "engine": "z3",
        "primary_model_with_suboptimal_top_k_selection": str(primary),
        "negative_control_with_optimal_selection": str(control),
        "passed": passed,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if passed else 4


if __name__ == "__main__":
    raise SystemExit(main())
