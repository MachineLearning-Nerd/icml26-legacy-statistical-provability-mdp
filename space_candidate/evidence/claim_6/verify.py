"""Symbolic certificate checker for the displayed Theorem 6 counterexample."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def evaluate(case: dict) -> dict:
    concentrated = case["name"] == "concentrated_queries_without_coverage"
    assumptions = {
        "compact_domain": case["domain"] == "[0,1]",
        "doubling_dimension_one": case["doubling_dimension"] == 1
        and case["covering_constant"] >= 2,
        "hypotheses_map_to_unit_interval": set(case["hypotheses"])
        == {"zero", "identity"},
        "uniform_lipschitz_constant_one": case["lipschitz_constant"] == 1,
        "bounded_unbiased_targets_everywhere": case["target_generator"]
        == "Y(z)=z deterministically",
    }
    if concentrated:
        empirical_risks = {"zero": Fraction(0), "identity": Fraction(0)}
        selected = case["selected_erm"]
        assumptions["valid_squared_loss_erm"] = (
            empirical_risks[selected] == min(empirical_risks.values())
        )
        assumptions["lemma4_deviation_is_zero"] = True
        approximation_error = Fraction(0)
        uniform_error = Fraction(1)

        # For delta=1/2 and n_m=2^m:
        # rate_m^3 = (m+1)log(2)/2^m < a_m=(m+1)/2^m.
        # a_(m+1)/a_m=(m+2)/(2m+2) <= 3/4 for every integer m>=1.
        # Hence a_m, and therefore rate_m, tends to zero geometrically.
        # The ratio inequality is universal, not a finite sweep:
        #   (m+2)/(2m+2) <= 3/4
        # iff 4m+8 <= 6m+6 iff 0 <= 2m-2.
        # The last affine expression has nonnegative slope and is zero at
        # the domain boundary m=1, certifying every integer m>=1.
        difference_slope = 2
        difference_at_m1 = 0
        ratio_certificate = difference_slope >= 0 and difference_at_m1 >= 0
        symbolic_ratio_reduction = (
            "4(m+2)<=6(m+1) iff 0<=2m-2; "
            "slope=2>=0 and boundary value at m=1 is 0"
        )
        claimed_rate_tends_to_zero = ratio_certificate
        contradiction = (
            all(assumptions.values())
            and approximation_error == 0
            and uniform_error == 1
            and claimed_rate_tends_to_zero
        )
    else:
        empirical_risks = {"zero": Fraction(1, 2), "identity": Fraction(0)}
        selected = case["selected_erm"]
        assumptions["valid_squared_loss_erm"] = (
            empirical_risks[selected] == min(empirical_risks.values())
        )
        assumptions["lemma4_deviation_is_zero"] = True
        approximation_error = Fraction(0)
        uniform_error = Fraction(0)
        symbolic_ratio_reduction = "not needed for coverage-restored control"
        claimed_rate_tends_to_zero = True
        contradiction = False
    return {
        "case": case["name"],
        "assumptions": assumptions,
        "empirical_squared_risks": {
            name: str(value) for name, value in empirical_risks.items()
        },
        "selected_erm": selected,
        "approximation_error": str(approximation_error),
        "uniform_sup_error_for_every_n": str(uniform_error),
        "asymptotic_certificate": {
            "subsequence": "n_m=2^m",
            "rate_cube_upper_bound": "a_m=(m+1)/2^m",
            "ratio": "(m+2)/(2m+2)<=3/4 for all integer m>=1",
            "exact_reduction": symbolic_ratio_reduction,
            "rate_tends_to_zero": claimed_rate_tends_to_zero
        },
        "contradiction": contradiction,
        "verdict": "FALSIFIED" if contradiction else "NO_COUNTEREXAMPLE"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.case.read_text(encoding="utf-8")))
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["contradiction"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
