"""Exact finite certificate for the E5 primitive-generator proof (stdlib only).

The universal gcd/height argument and imported canonical-height theorem are
written in GENERATOR_PROOF.md. This program checks the resulting finite
certificate; its assertions are not an independent proof of those theorems.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path
import platform


Point = tuple[F, F] | None
O: Point = None
P: Point = (F(-4), F(6))
TORSION: tuple[Point, ...] = (O, (F(0), F(0)), (F(5), F(0)), (F(-5), F(0)))


def admit(p: Point) -> None:
    if p is not None and p[1] ** 2 != p[0] ** 3 - 25 * p[0]:
        raise ValueError("admission error: point is not on E5")


def neg(p: Point) -> Point:
    admit(p)
    return None if p is None else (p[0], -p[1])


def add(p: Point, q: Point) -> Point:
    admit(p)
    admit(q)
    if p is None:
        return q
    if q is None:
        return p
    x, y = p
    u, v = q
    if x == u and y == -v:
        return None
    slope = (3 * x * x - 25) / (2 * y) if p == q else (v - y) / (u - x)
    X = slope * slope - x - u
    out = (X, slope * (x - X) - y)
    admit(out)
    return out


def mul(n: int, p: Point) -> Point:
    if n < 0:
        return mul(-n, neg(p))
    out = None
    while n:
        if n & 1:
            out = add(out, p)
        p = add(p, p)
        n >>= 1
    return out


def encoded(p: Point):
    return "O" if p is None else [str(p[0]), str(p[1])]


def height(p: Point) -> int:
    return 1 if p is None else max(abs(p[0].numerator), p[0].denominator)


def duplication_pair(a: int, b: int) -> tuple[int, int]:
    return (a * a + 25 * b * b) ** 2, 4 * a * b * (a * a - 25 * b * b)


def run() -> dict:
    # These are exact integer comparisons, not floating log/exp calculations.
    bound_numerator = 4 ** 3 * 676 * 2500 ** 9
    assert 20 ** 27 < bound_numerator < 21 ** 27
    rows = []
    affine: set[Point] = set()
    for b in range(1, 21):
        for a in range(-20, 21):
            if gcd(a, b) != 1:
                continue
            N = a * b * (a * a - 25 * b * b)
            s = isqrt(N) if N >= 0 else None
            square = s is not None and s * s == N
            rows.append({"a": a, "b": b, "N": N, "integer_sqrt_floor": s,
                         "is_square": square})
            if square:
                for sign in {-1, 1}:
                    candidate = (F(a, b), F(sign * s, b * b))
                    admit(candidate)
                    assert height(candidate) <= 20
                    affine.add(candidate)
    assert len(rows) == 511
    assert len(affine) == 7

    # Identify every enumerated point through exact group arithmetic.
    classes = {}
    for sign in (-1, 1):
        for ti, t in enumerate(TORSION):
            q = add(mul(sign, P), t)
            classes[q] = {"free_coefficient": sign, "torsion_index": ti}
    classified = []
    for q in sorted(affine):
        if q in TORSION:
            result = {"point": encoded(q), "torsion_index": TORSION.index(q)}
        else:
            assert q in classes
            result = {"point": encoded(q), **classes[q]}
        classified.append(result)
    assert add(P, TORSION[2]) == (F(-5, 9), F(-100, 27))

    # Compare the x-only duplication with a separate chord-law doubling,
    # including O and all rational 2-torsion exceptional cases.
    duplication_rows = []
    points_for_duplication = set(TORSION) | affine | {P, mul(2, P), mul(3, P),
                                                   add(P, TORSION[3])}
    for q in sorted(points_for_duplication, key=lambda x: str(encoded(x))):
        a, b = (1, 0) if q is None else (q[0].numerator, q[0].denominator)
        f, g = duplication_pair(a, b)
        d = gcd(f, g)
        new_height = max(abs(f), abs(g)) // d
        doubled = add(q, q)
        assert d <= 2500
        assert new_height == height(doubled)
        assert height(q) ** 4 <= 2500 * new_height
        assert new_height <= 676 * height(q) ** 4
        if g == 0:
            assert doubled is None
        else:
            assert doubled is not None and F(f, g) == doubled[0]
        duplication_rows.append({"point": encoded(q), "F": str(f), "G": str(g),
                                 "gcd": d, "double": encoded(doubled),
                                 "height_double": str(new_height)})

    # Hostile controls: the gcd allowance really can be 2500 on E5;
    # binary quotient coverage alone really cannot reject index three;
    # and rational-looking off-curve input must not enter group operations.
    hostile_point = add(P, TORSION[3])
    assert hostile_point == (F(45), F(-300))
    f, g = duplication_pair(45, 1)
    assert gcd(f, g) == 2500
    binary_coverage = []
    for n in range(1, 9):
        modulus = 2 ** n
        assert {3 * j % modulus for j in range(modulus)} == set(range(modulus))
        binary_coverage.append({"n": n, "index": 3, "surjective": True})
    try:
        add((F(0), F(1)), P)
    except ValueError:
        off_curve_rejected = True
    else:
        raise AssertionError("off-curve point was accepted")

    return {
        "schema": "bsd-e5-generator-certificate-v1",
        "evidence_grade": "EXACT_FINITE_CERTIFICATE_WITH_WRITTEN_THEOREM_DEPENDENCIES",
        "result": {"free_index_of_P": 1,
                   "group": "E(Q) = Z*P direct_sum E[2](Q)",
                   "P": encoded(P), "torsion": [encoded(t) for t in TORSION]},
        "assumed_prior_results": ["rank(E(Q))=1", "E(Q)_tors=E[2](Q)=(Z/2)^2",
                                  "free index of P is odd"],
        "height_contract": {
            "naive": "h_x(Q)=log(max(abs(a),b)), x(Q)=a/b reduced, b>0; h_x(O)=0",
            "canonical": "Hhat_x(Q)=lim_n 4^(-n)*h_x(2^n Q)",
            "lower_difference": "Hhat_x(Q)>=h_x(Q)-log(2500)/3",
            "upper_difference": "Hhat_x(Q)<=h_x(Q)+log(676)/3",
            "index_at_least_three_implies": "H(Q)^27 <= 4^3*676*2500^9 < 21^27",
            "integer_bound_numerator": str(bound_numerator),
            "twenty_to_27": str(20 ** 27), "twenty_one_to_27": str(21 ** 27),
            "enumeration_height_maximum": 20},
        "canonical_height_source": {
            "title": "J. S. Milne, Elliptic Curves (2006), Chapter IV section 4",
            "url": "https://www.jmilne.org/math/Books/ectext6.pdf#page=128",
            "printed_pages": "120-124",
            "passages": ["height definition p.120", "Lemma4.6 and Theorem4.7 pp.121-123",
                         "Proposition4.9 and Lemma4.11 pp.123-124"],
            "claims_used": ["existence of full-x canonical height", "quadraticity"],
            "source_inspected_on": "2026-09-12",
            "normalization_warning": "Hhat_x is twice the alternative half-x canonical height"},
        "enumeration": {"abscissa_count": len(rows), "affine_point_count": len(affine),
                        "identity_added_separately": True,
                        "classified_points": classified, "all_abscissa_rows": rows},
        "duplication_crosscheck": duplication_rows,
        "controls": {"gcd_2500_attained": {"point": encoded(hostile_point), "gcd": 2500},
                     "index_three_binary_coverage": binary_coverage,
                     "off_curve_rejected": off_curve_rejected},
        "metadata": {"python": platform.python_version(),
                     "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest()},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS: exact integer height cutoff H<=20")
    print("PASS: all 511 rational abscissas enumerated; 7 affine points and O")
    print("PASS: every nontorsion point is +/-P plus rational 2-torsion")
    print("PASS: duplication exceptional cases and three hostile controls")
    print("CONCLUSION (with cited and prior theorem inputs): free index of P is ONE(1)")
    print(f"Certificate: {args.output.resolve()}")
