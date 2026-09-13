"""Exact new polynomial checks for the connected vacuum coefficients.

Standard library only. No old checker is imported or rerun, and no
eigenvalue approximation or graph simulation is performed. Analytic
convergence and arbitrary-graph coverage are written proof obligations.
"""

from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import comb
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class Poly:
    """Rational polynomial in the three named variables a, b, w."""

    def __init__(self, terms=0):
        if isinstance(terms, Poly):
            terms = terms.terms
        if isinstance(terms, (int, F)):
            terms = {(0, 0, 0): F(terms)}
        self.terms = {p: F(c) for p, c in terms.items() if c}

    def __add__(self, other):
        out = dict(self.terms)
        for p, c in Poly(other).terms.items():
            out[p] = out.get(p, F(0)) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({p: -c for p, c in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = {}
        for p, c in self.terms.items():
            for q, d in Poly(other).terms.items():
                key = tuple(p[i] + q[i] for i in range(3))
                out[key] = out.get(key, F(0)) + c * d
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, value):
        return self * (F(1) / value)

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0,
                "Polynomial power requires a nonnegative integer")
        out = Poly(1)
        for _ in range(exponent):
            out = out * self
        return out

    def __eq__(self, other):
        return self.terms == Poly(other).terms

    def derivative(self, variable):
        out = {}
        for powers, coefficient in self.terms.items():
            if powers[variable]:
                key = list(powers)
                key[variable] -= 1
                out[tuple(key)] = coefficient * powers[variable]
        return Poly(out)

    def at(self, values):
        total = F(0)
        for powers, coefficient in self.terms.items():
            term = coefficient
            for value, power in zip(values, powers):
                term *= F(value) ** power
            total += term
        return total

    def record(self):
        return [{"powers_a_b_w": list(p), "coefficient": str(c)}
                for p, c in sorted(self.terms.items())]


a = Poly({(1, 0, 0): 1})
b = Poly({(0, 1, 0): 1})
w = Poly({(0, 0, 1): 1})
M = (
    (4 * (1 - a*a), w - a*b, 3 * (b - a*w)),
    (w - a*b, 4 * (1 - b*b), 3 * (a - b*w)),
    (3 * (b - a*w), 3 * (a - b*w), 6 * (1 - w*w)),
)


def kinetic(poly):
    # Differentiate the divergence form, including the coefficient drift.
    out = Poly()
    for i in range(3):
        for j in range(3):
            out += (M[i][j] * poly.derivative(j)).derivative(i)
    return -out / 2


def disconnected_kinetic(poly):
    require(all(p[2] == 0 for p in poly.terms),
            "Disconnected control admits only a and b")
    # The (a,b) product half-trace law has semicircle weights, so its
    # drift is -12a,-12b. It is not unweighted two-variable divergence.
    return -(4 * (1-a*a) * poly.derivative(0).derivative(0)
             + 4 * (1-b*b) * poly.derivative(1).derivative(1)
             - 12*a*poly.derivative(0)-12*b*poly.derivative(1)) / 2


@lru_cache(maxsize=None)
def halftrace_moment(exponent):
    if exponent % 2:
        return F(0)
    n = exponent // 2
    return F(comb(2*n, n), (n+1) * 4**n)


@lru_cache(maxsize=None)
def haar_monomial(i, j, k):
    # Conditional on a,b: w=ab-sqrt(1-a^2)sqrt(1-b^2) z,
    # with z uniform on [-1,1]; only even powers of z survive.
    result = F(0)
    for t in range(k // 2 + 1):
        left = sum(F((-1)**m * comb(t, m))
                   * halftrace_moment(i+k-2*t+2*m)
                   for m in range(t+1))
        right = sum(F((-1)**m * comb(t, m))
                    * halftrace_moment(j+k-2*t+2*m)
                    for m in range(t+1))
        result += F(comb(k, 2*t), 2*t+1) * left * right
    return result


def mean(poly):
    return sum(c * haar_monomial(*p) for p, c in poly.terms.items())


def equal_check(name, actual, expected, checks):
    require(actual == expected, name)
    checks.append({"name": name, "passed": True,
                   "polynomial": Poly(actual).record()})


def build_receipt():
    checks = []
    for name, poly, expected in (
        ("constant_kernel", Poly(1), Poly()),
        ("left_square_eigenvalue", a, 6*a),
        ("right_square_eigenvalue", b, 6*b),
        ("left_centered_square", a*a-F(1,4), 16*(a*a-F(1,4))),
        ("right_centered_square", b*b-F(1,4), 16*(b*b-F(1,4))),
        ("adjacent_product", a*b, 13*a*b-w),
        ("outer_loop", w, 9*w),
    ):
        equal_check(name, kinetic(poly), expected, checks)

    moments = {"a": mean(a), "b": mean(b), "w": mean(w),
               "a2": mean(a*a), "b2": mean(b*b), "ab": mean(a*b),
               "w2": mean(w*w), "abw": mean(a*b*w)}
    require(moments == {"a": F(0), "b": F(0), "w": F(0),
                        "a2": F(1,4), "b2": F(1,4), "ab": F(0),
                        "w2": F(1,4), "abw": F(1,16)},
            "Haar moment normalization changed")

    s = a+b
    u1 = s/6
    u2 = (a*a+b*b-F(1,2))/96+a*b/39+w/351
    e2 = -mean(s*u1)
    require(mean(u1) == 0 and mean(u2) == 0, "Coefficient means")
    require(e2 == F(-1,12), "Energy coefficient")
    require(mean(s*u2) == 0, "Third energy coefficient must vanish")
    equal_check("order_one_eigen_equation", kinetic(u1)-s, 0, checks)
    equal_check("order_two_eigen_equation", kinetic(u2)-s*u1-e2, 0, checks)

    j = (4*w-3*a*b)/702
    log2 = 2*u2-u1*u1
    expected_log2 = -(a*a+b*b)/144-F(1,96)+j
    equal_check("unnormalized_log_second_order", log2, expected_log2, checks)
    norm2 = mean(u1*u1)
    require(norm2 == F(1,72), "Density normalization coefficient")
    log2_normalized = log2-norm2
    expected_normalized = -(a*a+b*b-F(1,2))/144-F(1,36)+j
    equal_check("normalized_log_second_order", log2_normalized,
                expected_normalized, checks)
    require(mean(log2_normalized+s*s/18) == 0,
            "Exponential density normalization through second order")

    pair_free = a*b/36
    pair_adjacent = a*b/39+w/351
    equal_check("disconnected_product_action", disconnected_kinetic(a*b),
                12*a*b, checks)
    equal_check("disconnected_pair_equation", disconnected_kinetic(pair_free),
                a*b/3, checks)
    equal_check("disconnected_log_cross_cancels", 2*pair_free-a*b/18, 0, checks)
    equal_check("adjacent_pair_equation", kinetic(pair_adjacent), a*b/3, checks)
    equal_check("adjacent_log_cross_survives", 2*pair_adjacent-a*b/18, j, checks)
    hostile = kinetic(pair_free)-a*b/3
    require(hostile == (a*b-w)/36 and hostile != 0,
            "Incorrect independent-pair inverse must be rejected")

    delta = 1-a*a-b*b-w*w+2*a*b*w
    witnesses = ((F(0),F(0),F(1,2)), (F(0),F(0),F(-1,2)))
    require(all(delta.at(point) > 0 for point in witnesses),
            "Hostile points must lie in the regular interior")
    separation = log2.at(witnesses[0])-log2.at(witnesses[1])
    require(separation == F(2,351), "Forgotten w second-order separation")
    require(j.at((0,0,1)) == F(2,351)
            and j.at((0,0,-1)) == F(-2,351),
            "Connected coefficient endpoint extrema")

    # Uniform sup norm certificate for u2, used by a separate log-witness proof.
    u2_sup_bound = F(3,2)/96+F(1,39)+F(1,351)
    require(u2_sup_bound < F(1,20), "u2 supremum bound")
    # At r <= 1/10, the squared tail coefficient is 25/162 < (2/5)^2.
    require(F(25,162) < F(4,25), "Small-r rational tail comparison")

    here = Path(__file__).resolve().parent
    reused = (here / "accepted_sources" / "ym2_global_phase_joint" / "GAP_BRIDGE.md",
              here / "accepted_sources" / "ym2_signed_differences" / "NEXT_CONNECTED_OBLIGATION.md")
    sources = list(reused) + [Path(__file__).resolve(), here / "CONNECTED_VACUUM.md"]
    source_records = [{"path": path.relative_to(here).as_posix(),
                       "sha256": sha256(path.read_bytes()).hexdigest(),
                       "role": "reused_written_source" if path in reused else "new_checked_source"}
                      for path in sources]
    return {
        "schema": "ym2_connected_vacuum_exact_polynomials_v1",
        "status": "PASS",
        "evidence_grade": "Exact rational finite checks; written analytic proofs remain separate",
        "carrier": "Q[a,b,w] with accepted SU(2) two-square Haar law",
        "variables_in_order": ["a", "b", "w"],
        "checks": checks,
        "checks_passed": len(checks),
        "haar_moments": {key: str(value) for key, value in moments.items()},
        "coefficients": {"u1": u1.record(), "u2": u2.record(), "e2": str(e2),
                         "e3": "0", "log_psi_squared_r2": log2.record(),
                         "log_rho_r2": log2_normalized.record(),
                         "connected_pair_r2": j.record()},
        "normalization": {"mean_psi": "1", "mean_u1": "0", "mean_u2": "0",
                          "mean_psi_squared_r2": str(norm2)},
        "hostile_control": {"incorrect_disconnected_inverse_on_adjacent_pair": pair_free.record(),
                            "nonzero_residual": hostile.record(), "outcome": "REJECT"},
        "forgotten_w_jet_control": {"points": [[str(v) for v in p] for p in witnesses],
                                   "equal_retained_coordinates": ["a", "b"],
                                   "log_r2_difference": str(separation),
                                   "claim_ceiling": "Exact Taylor coefficient separation; actual-density interval proved separately"},
        "u2_supremum_bound": str(u2_sup_bound),
        "analytic_claims_not_machine_verified": [
            "Rank-one spectral projection and mean-normalized eigenvector analytic on |r|<3/2",
            "Cauchy L2 remainder bound |r|^3/[2 sqrt(2)(1-|r|)] on |r|<1",
            "Fixed-graph Ck log remainder from source elliptic regularity",
            "Arbitrary admitted square/cubic graph second-order connected-support theorem"],
        "not_claimed": ["all-order cluster convergence", "graph-uniform conditional influence",
                        "continuum Yang-Mills mass gap", "new general soundness theorem"],
        "sources": source_records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-results", action="store_true",
                        help="Write only this new checker's RESULTS_CONNECTED.json")
    args = parser.parse_args()
    receipt = build_receipt()
    target = Path(__file__).resolve().with_name("RESULTS_CONNECTED.json")
    if args.write_results:
        target.write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
        print(f"PASS: {receipt['checks_passed']} exact polynomial checks; wrote {target.name}")
    else:
        require(target.is_file(), "Saved RESULTS_CONNECTED.json is missing")
        saved = json.loads(target.read_text(encoding="utf-8"))
        require(saved == receipt, "Saved RESULTS_CONNECTED.json differs from the full recomputed receipt")
        print(f"PASS: {receipt['checks_passed']} exact polynomial checks; full saved receipt matches")


if __name__ == "__main__":
    main()
