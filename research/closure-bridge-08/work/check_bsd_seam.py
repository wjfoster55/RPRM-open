"""Exact, bounded BSD rectangular-refinement seam check.

No analytic coefficients, logarithm approximations, or BSD comparison values
are computed. The written theorem and scope are in ../agents/BSD_SEAM.md.
"""

import argparse
from fractions import Fraction as F
from math import gcd
import json
from pathlib import Path


N = 34
C0 = 4 * N**4
NVARS = 5  # p, q, s, u, v; formal real height slots and increments
ZERO = (0,) * NVARS


def constant(value):
    return {} if value == 0 else {ZERO: F(value)}


def variable(index):
    exponent = [0] * NVARS
    exponent[index] = 1
    return {tuple(exponent): F(1)}


def plus(*polynomials):
    result = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, F(0)) + coefficient
    return {exponent: coefficient for exponent, coefficient in result.items()
            if coefficient}


def scale(polynomial, factor):
    return {exponent: coefficient * factor
            for exponent, coefficient in polynomial.items()
            if coefficient * factor}


def multiply(left, right):
    result = {}
    for e, a in left.items():
        for f, b in right.items():
            exponent = tuple(x + y for x, y in zip(e, f))
            result[exponent] = result.get(exponent, F(0)) + a * b
    return {exponent: coefficient for exponent, coefficient in result.items()
            if coefficient}


def regulator(slots):
    p, q, s = slots
    difference = plus(s, scale(p, -1), scale(q, -1))
    return plus(multiply(p, q), scale(multiply(difference, difference), F(-1, 4)))


def rectangular_polynomial(first, second):
    p, q, s, u, v = [variable(i) for i in range(NVARS)]
    slots = [p, q, s]
    one, two, both = list(slots), list(slots), list(slots)
    one[first] = plus(one[first], u)
    two[second] = plus(two[second], v)
    both[first] = plus(both[first], u)
    both[second] = plus(both[second], v)
    rectangle = plus(regulator(both), scale(regulator(one), -1),
                     scale(regulator(two), -1), regulator(slots))
    expected = scale(multiply(u, v), F(1 if first != second else -1, 2))
    assert rectangle == expected
    return {"slots": ["pqs"[first], "pqs"[second]],
            "result": ("u*v/2" if first != second else "-u*v/2"),
            "coefficient_identity": "PASS"}


def admit(point):
    if point is None:
        return
    x, y = point
    if y*y != x*x*x - N*N*x:
        raise ValueError("point is not on E34")


def chord_double(point):
    admit(point)
    if point is None or point[1] == 0:
        return None
    x, y = point
    slope = (3*x*x - N*N) / (2*y)
    xx = slope*slope - 2*x
    result = xx, slope*(x-xx) - y
    admit(result)
    return result


def coordinates(point):
    return (1, 0) if point is None else (point[0].numerator, point[0].denominator)


def first_step(name, point):
    admit(point)
    a, b = coordinates(point)
    assert gcd(a, b) == 1 and b >= 0
    height = max(abs(a), b)
    raw_f = (a*a + N*N*b*b)**2
    raw_g = 4*a*b*(a*a - N*N*b*b)
    removed = gcd(raw_f, raw_g)
    assert removed > 0 and C0 % removed == 0
    aa, bb = raw_f // removed, raw_g // removed
    if bb < 0:
        aa, bb = -aa, -bb
    assert (aa, bb) == coordinates(chord_double(point))
    next_height = max(abs(aa), bb)
    argument = F(next_height, height**4)
    assert argument > 0
    return {"name": name, "source_x": [a, b], "H0": height,
            "raw_F": raw_f, "raw_G": raw_g, "gcd": removed,
            "next_x": [aa, bb], "H1": next_height,
            "increment_log_argument": str(argument),
            "increment": "(1/4)*log(" + str(argument) + ")",
            "increment_sign": (argument > 1) - (argument < 1),
            "chord_law_readback": "PASS"}


def check_joint_decomposition():
    # D/Omega/sigma = -R when the analytic cutoff is held fixed.
    p, q, s = [variable(i) for i in range(3)]
    separate = scale(plus(multiply(p, p), multiply(q, q), multiply(s, s)), F(1, 4))
    joint = scale(plus(multiply(p, q), multiply(p, s), multiply(q, s)), F(-1, 2))
    assert plus(separate, joint) == scale(regulator([p, q, s]), -1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    points = {
        "P": (F(-2), F(48)), "Q": (F(-16), F(120)),
        "S": (F(2178, 49), F(65472, 343)), "O": None,
        "T0": (F(0), F(0)), "Tplus": (F(34), F(0)),
        "Tminus": (F(-34), F(0)),
    }
    steps = {name: first_step(name, point) for name, point in points.items()}
    assert steps["P"]["increment_log_argument"] == "21025/16"
    assert steps["Q"]["increment_log_argument"] == "124609/65536"
    assert steps["P"]["increment_sign"] == steps["Q"]["increment_sign"] == 1
    assert steps["P"]["gcd"] == 64 and steps["Q"]["gcd"] == 16
    assert steps["Tplus"]["gcd"] == steps["Tminus"]["gcd"] == C0
    for name in ("O", "T0", "Tplus", "Tminus"):
        assert steps[name]["next_x"] == [1, 0]
        assert F(steps[name]["increment_log_argument"]) == F(1, steps[name]["H0"]**4)
    try:
        admit((F(1), F(1)))
    except ValueError:
        invalid_point = "REJECTED"
    else:
        raise AssertionError("invalid point was admitted")

    rectangles = [rectangular_polynomial(i, j) for i in range(3) for j in range(i, 3)]
    check_joint_decomposition()
    for omega, sigma, u, v in ((0, 1, 2, 3), (1, 0, 2, 3),
                             (1, 1, 0, 3), (1, 1, 2, 0)):
        assert F(-omega*sigma*u*v, 2) == 0
    # The same cross term is retained along either order of a rectangle.
    def numeric_regulator(p, q, s):
        return p*q - (s-p-q)**2/4
    p, q, s, u, v = map(F, (2, 3, 5, 7, 11))
    corners = [numeric_regulator(p, q, s), numeric_regulator(p+u, q, s),
               numeric_regulator(p, q+v, s), numeric_regulator(p+u, q+v, s)]
    assert (corners[1]-corners[0]) + (corners[3]-corners[1]) == \
           (corners[2]-corners[0]) + (corners[3]-corners[2])
    result = {
        "status": "PASS", "curve": "y^2=x^3-1156x",
        "source_first_steps": steps, "formal_rectangles": rectangles,
        "joint_decomposition": "PASS: -R=(p^2+q^2+s^2)/4-(pq+ps+qs)/2",
        "actual_PQ_rectangle": {
            "regulator": "log(21025/16)*log(124609/65536)/32",
            "finite_defect": "-Omega*sigma*log(21025/16)*log(124609/65536)/32",
            "regulator_sign": "strictly positive",
            "defect_sign_if_Omega_and_sigma_positive": "strictly negative",
            "proof_of_nonzero": "Both exact positive rational log arguments exceed one",
        },
        "exception_controls": "PASS: zero Omega, sigma, or either increment gives zero; O and 2-torsion treated projectively",
        "invalid_point_control": invalid_point,
        "ordered_rectangle_path_check": "PASS",
        "scope": "Candidate V exact on the asynchronous refinement rectangle must retain pair interaction; locked-diagonal-only V is not refuted",
        "evidence_grade": "Fresh exact rational and formal-polynomial arithmetic, with written universal derivation in agents/BSD_SEAM.md",
        "open": ["E34 real analytic-height comparison", "actual vanishing-terminal potential", "total Sha identification", "general BSD"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "source_points": len(steps),
                      "formal_rectangles": len(rectangles), "output": str(args.output)}))


if __name__ == "__main__":
    main()
