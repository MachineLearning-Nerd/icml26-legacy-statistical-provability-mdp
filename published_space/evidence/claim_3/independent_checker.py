"""Independent SMT reconstruction of Theorem 3's induction steps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import Real, RealVal, Solver, sat, unsat


def upper_step_violation():
    t_v = Real("upper_T_V")
    t_u = Real("upper_T_U")
    v_next = Real("upper_V_next")
    u_next = Real("upper_U_next")
    solver = Solver()
    solver.add(t_v <= t_u, u_next >= t_u, v_next == t_v, v_next > u_next)
    return solver.check()


def lower_step_violation():
    t_l = Real("lower_T_L")
    t_v = Real("lower_T_V")
    l_next = Real("lower_L_next")
    v_next = Real("lower_V_next")
    solver = Solver()
    solver.add(t_l <= t_v, l_next <= t_l, v_next == t_v, l_next > v_next)
    return solver.check()


def bad_upper_control(require_recurrence: bool):
    t_u = Real("control_T_U")
    u_next = Real("control_U_next")
    v_next = Real("control_V_next")
    solver = Solver()
    solver.add(
        t_u == RealVal("2/3"),
        v_next == RealVal("2/3"),
        u_next == RealVal("1/2"),
        v_next > u_next,
    )
    if require_recurrence:
        solver.add(u_next >= t_u)
    return solver.check()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    upper = upper_step_violation()
    lower = lower_step_violation()
    control_without_recurrence = bad_upper_control(False)
    control_with_recurrence = bad_upper_control(True)
    passed = (
        upper == unsat
        and lower == unsat
        and control_without_recurrence == sat
        and control_with_recurrence == unsat
    )
    result = {
        "engine": "z3",
        "violating_super_solution_induction_step": str(upper),
        "violating_sub_solution_induction_step": str(lower),
        "bad_bound_without_upper_recurrence": str(control_without_recurrence),
        "same_bad_bound_with_upper_recurrence": str(control_with_recurrence),
        "passed": passed,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if passed else 4


if __name__ == "__main__":
    raise SystemExit(main())
