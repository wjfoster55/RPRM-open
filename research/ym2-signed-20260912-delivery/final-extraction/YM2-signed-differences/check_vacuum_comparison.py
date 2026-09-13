"""Exact arithmetic support for VACUUM_COMPARISON.md; not an analytic prover."""

import argparse
from fractions import Fraction
import json
from math import factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def positive_taylor(argument, degree):
    return sum((argument**k / factorial(k) for k in range(degree + 1)), Fraction(0))


def certificate():
    taylor = sum((Fraction(3**k, factorial(k)) for k in range(9)), Fraction(0))
    require(taylor > 20, "The finite positive Taylor sum must exceed 20")
    q = Fraction(1, 20)
    tail = (1 + q) / (1 - q)**3 - 1
    require(tail == Fraction(1541, 6859), "Geometric derivative evaluation changed")
    require(0 < tail < Fraction(1, 4), "Complete analytic tail majorant must be below 1/4")
    # Ascending polynomial coefficients: (n-1)(n-2) = n^2-3n+2.
    factors = (-1, 1), (-2, 1)
    product = [0, 0, 0]
    for i, a in enumerate(factors[0]):
        for j, b in enumerate(factors[1]):
            product[i + j] += a * b
    require(product == [2, -3, 1], "Exponent difference factorization changed")
    lower, upper = Fraction(3, 4), Fraction(5, 4)
    heat_ratio = (upper/lower)**7
    require(heat_ratio**2 == Fraction(5, 3)**14, "Seven-factor density exponent mismatch")
    cmix_coefficient, cloc_coefficient = Fraction(1, 4), Fraction(1, 3)
    glue_coefficient = 1 / (2 * cmix_coefficient * cloc_coefficient)
    direct_coefficient = Fraction(12, 2)
    require(glue_coefficient == direct_coefficient == 6, "Spectral coefficient mismatch")
    refined_taylor = []
    for argument, threshold in [
        (Fraction(2), Fraction(73, 10)),
        (Fraction(16, 3), Fraction(200)),
        (Fraction(14, 3), Fraction(100)),
    ]:
        value = positive_taylor(argument, 16)
        require(value > threshold, "Refined positive Taylor lower bound failed")
        refined_taylor.append({
            "argument": rational(argument),
            "degree": 16,
            "positive_taylor_sum": rational(value),
            "strict_threshold": rational(threshold),
            "margin": rational(value - threshold),
        })
    refined_term_ratio = Fraction(16, 9) / 100
    require(refined_term_ratio == Fraction(4, 225), "Refined term ratio mismatch")
    refined_tail = Fraction(40, 73) + Fraction(9, 200) / (1 - refined_term_ratio)
    refined_d = Fraction(3, 5)
    require(refined_tail < refined_d, "Refined complete tail majorant must be below 3/5")
    # These four support sizes are accepted source data, not a new graph census.
    support_sizes = [4, 4, 6, 7]
    eta = sum((refined_d**size for size in support_sizes), Fraction(0))
    require(eta == Fraction(26082, 78125) < 1, "Refined support polynomial mismatch")
    gauge_ratio = (1 + eta) / (1 - eta)
    require(gauge_ratio == Fraction(104207, 52043), "Gauge-averaged kernel ratio mismatch")
    require(gauge_ratio**2 < heat_ratio**2, "Refined density prefactor must improve coarse one")
    require(Fraction(32, 3) < 16, "Refined density exponent must improve coarse one")
    return {
        "status": "PASS",
        "evidence_grade": "exact finite arithmetic supporting a separate written analytic proof",
        "graph_links": 7,
        "normalized_heat_time": 1,
        "taylor_terms_k": [0, 8],
        "exp_3_strict_lower_bound": rational(taylor),
        "exp_3_lower_bound_exceeds_20_by": rational(taylor - 20),
        "all_n_exponent_difference_polynomial_ascending": product,
        "analytic_geometric_tail_majorant": rational(tail),
        "quarter_minus_tail_majorant": rational(Fraction(1, 4) - tail),
        "one_link_heat_interval": {"lower": rational(lower), "upper": rational(upper)},
        "seven_link_heat_ratio_upper_bound": rational(heat_ratio),
        "density_ratio_rational_factor": rational(heat_ratio**2),
        "density_ratio_parameter_factor": "exp(16 r), r=beta/(alpha hbar^2)",
        "physical_C_mix_upper_bound": "R_bar/4",
        "local_C_loc_upper_bound": "R_bar/3",
        "overlap_multiplicity": 1,
        "glue_gap_lower_bound": "6 alpha hbar^2 / R_bar^2",
        "direct_gap_lower_bound": "6 alpha hbar^2 / R_bar",
        "gauge_refinement": {
            "normalized_heat_time": rational(Fraction(2, 3)),
            "strict_exponential_lower_bounds": refined_taylor,
            "successive_tail_term_ratio_upper_bound_n_ge_3": rational(refined_term_ratio),
            "complete_character_tail_majorant": rational(refined_tail),
            "character_tail_upper_bound": rational(refined_d),
            "three_fifths_minus_tail_majorant": rational(refined_d - refined_tail),
            "support_sizes_from_accepted_source": support_sizes,
            "support_provenance": "../ym2_global_phase_joint/RESULTS_QUANTUM.json; old census not rerun",
            "support_polynomial_at_three_fifths": rational(eta),
            "gauge_averaged_heat_ratio_upper_bound": rational(gauge_ratio),
            "density_ratio_rational_factor": rational(gauge_ratio**2),
            "density_ratio_parameter_factor": "exp(32 r/3), r=beta/(alpha hbar^2)",
            "physical_C_mix_upper_bound": "R_gauge/4",
            "local_C_loc_upper_bound": "R_gauge/3",
            "glue_gap_lower_bound": "6 alpha hbar^2 / R_gauge^2",
            "direct_gap_lower_bound": "6 alpha hbar^2 / R_gauge",
        },
        "not_verified_by_this_program": [
            "general heat-kernel character expansion and Peter-Weyl completeness",
            "analytic infinite-series comparison and convergence",
            "Feynman-Kac or Trotter semigroup comparison",
            "all-spin invariant graph-support bound",
            "gauge-averaged residual cancellations and finite support expansion",
            "ground-state existence and source operator/form domains",
            "conditional-variance and Poincare comparison proofs",
            "graph-family uniformity or continuum quantum construction",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    actual = certificate()
    path = Path(__file__).with_name("RESULTS_VACUUM_COMPARISON.json")
    if args.write_results:
        path.write_text(json.dumps(actual, indent=2) + "\n", encoding="utf-8")
        print("PASS: exact vacuum-comparison arithmetic; receipt written")
    else:
        expected = json.loads(path.read_text(encoding="utf-8"))
        require(actual == expected, "Saved vacuum-comparison arithmetic receipt differs")
        print("PASS: exact vacuum-comparison arithmetic; saved receipt matches")


if __name__ == "__main__":
    main()
