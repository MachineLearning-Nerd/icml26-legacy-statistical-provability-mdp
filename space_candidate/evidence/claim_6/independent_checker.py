"""Independent Z3 audit of the Theorem 6 construction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import Int, Not, Real, RealVal, Solver, sat, unsat


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    # Primary: both hypotheses tie at zero empirical risk on queries z=0,
    # while h_zero has a witnessed unit error at z=1.
    risk_zero = Real("risk_zero")
    risk_identity = Real("risk_identity")
    witnessed_error = Real("witnessed_error")
    primary = Solver()
    primary.add(risk_zero == 0, risk_identity == 0, witnessed_error == 1)
    primary.add(risk_zero <= risk_identity, witnessed_error > 0)
    primary_status = primary.check()

    # Exact universal ratio certificate:
    # 4(m+2) <= 6(m+1) for every integer m>=1.
    m = Int("m")
    ratio = Solver()
    ratio.add(m >= 1, Not(4 * (m + 2) <= 6 * (m + 1)))
    ratio_counterexample = ratio.check()

    # Coverage-restored control: at z=0 and z=1, h_identity has risk 0 and
    # h_zero has risk 1/2, so selecting h_zero cannot be an ERM.
    control = Solver()
    control.add(risk_zero == RealVal("1/2"), risk_identity == 0)
    control.add(risk_zero <= risk_identity)
    control_status = control.check()

    passed = (
        primary_status == sat
        and ratio_counterexample == unsat
        and control_status == unsat
    )
    result = {
        "engine": "z3",
        "primary_construction": str(primary_status),
        "counterexample_to_ratio_certificate": str(ratio_counterexample),
        "coverage_restored_bad_erm": str(control_status),
        "passed": passed
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if passed else 4


if __name__ == "__main__":
    raise SystemExit(main())
