"""Bounded exact replay of logarithmic height-series telescoping for E34.

No previous script or receipt is imported. No L-value, logarithm approximation,
Sha order, or BSD identity is computed. Mathematical scope: EXPLICIT_IDENTITY_TARGET.md.
"""

import argparse
from fractions import Fraction as F
from math import gcd
import json
from pathlib import Path

N = 34
C0 = 4*N**4
C1 = (1+N*N)**2
STEPS = 4


def admit(point):
    if point is None:
        return
    x, y = point
    if y*y != x*x*x - N*N*x:
        raise ValueError("point is not on the declared E34")


def add(p, q):
    admit(p)
    admit(q)
    if p is None:
        return q
    if q is None:
        return p
    x, y = p
    z, w = q
    if x == z and y == -w:
        return None
    slope = (3*x*x-N*N)/(2*y) if p == q else (w-y)/(z-x)
    xx = slope*slope-x-z
    result = xx, slope*(x-xx)-y
    admit(result)
    return result


def coords(point):
    return (1, 0) if point is None else (point[0].numerator, point[0].denominator)


def v(integer, p):
    assert integer > 0
    result = 0
    while integer % p == 0:
        integer //= p
        result += 1
    return result


def replay(point):
    admit(point)
    a, b = coords(point)
    first_height = max(abs(a), b)
    heights, corrections, rows = [first_height], [], []
    for j in range(STEPS):
        assert b >= 0 and gcd(a, b) == 1
        height = max(abs(a), b)
        raw_f = (a*a+N*N*b*b)**2
        raw_g = 4*a*b*(a*a-N*N*b*b)
        maximum = max(raw_f, abs(raw_g))
        removed = gcd(raw_f, raw_g)
        assert removed > 0 and C0 % removed == 0
        assert height**4 <= maximum <= C1*height**4
        aa, bb = raw_f//removed, raw_g//removed
        if bb < 0:
            aa, bb = -aa, -bb
        assert gcd(aa, bb) == 1 and bb >= 0
        next_height = max(abs(aa), bb)
        rho = F(maximum, height**4)
        correction = rho/removed
        assert correction == F(next_height, height**4)
        assert F(1, C0) <= correction <= C1
        g2, g17 = v(removed, 2), v(removed, 17)
        assert removed == 2**g2*17**g17
        assert g2 <= 6 and g17 <= 4
        next_point = add(point, point)
        assert (aa, bb) == coords(next_point)
        corrections.append(correction)
        heights.append(next_height)
        rows.append({"j": j, "H_j": hex(height), "gcd": removed,
                     "gcd_v2": g2, "gcd_v17": g17,
                     "raw_height_ratio_rho": str(rho),
                     "exp_delta_j": str(correction),
                     "weight": str(F(1, 4**(j+1))),
                     "H_next": hex(next_height)})
        a, b, point = aa, bb, next_point
    # Exp(4^k times the finite logarithmic series) is exactly H_k.
    for k in range(STEPS+1):
        product = F(first_height**(4**k))
        for j in range(k):
            product *= corrections[j]**(4**(k-j-1))
        assert product == heights[k]
    return {"initial_H": first_height, "steps": STEPS, "rows": rows,
            "multiplicative_telescoping": "PASS for every cutoff 0..4",
            "independent_chord_doubling": "PASS", "last_x": [hex(a), hex(b)]}


def gram(p, q, b):
    return p*q-b*b


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    p, q = (F(-2), F(48)), (F(-16), F(120))
    s = add(p, q)
    assert s == (F(2178, 49), F(65472, 343))
    points = {"P": p, "Q": q, "P+Q": s, "O": None,
              "T0": (F(0), F(0)), "Tplus": (F(34), F(0)), "Tminus": (F(-34), F(0))}
    evidence = {name: replay(point) for name, point in points.items()}
    assert evidence["Tplus"]["rows"][0]["gcd"] == C0
    for name in ("O", "T0", "Tplus", "Tminus"):
        assert evidence[name]["last_x"] == ["0x1", "0x0"]
    gram_cases = 0
    for k in range(-5, 6):
        pp, qq, bb = F(k, 3), F(2*k+1, 5), F(3-k, 7)
        uu, vv, ww = F(k+2, 11), F(1-2*k, 13), F(k-4, 17)
        increment = pp*vv+qq*uu+uu*vv-2*bb*ww-ww*ww
        assert gram(pp+uu, qq+vv, bb+ww)-gram(pp, qq, bb) == increment
        gram_cases += 1
    result = {"status": "PASS", "curve": "y^2=x^3-1156x", "C0": C0, "C1": C1,
              "point_ledgers": evidence, "gram_increment_cases": gram_cases,
              "evidence_ceiling": "Exact finite arithmetic for logarithmic telescoping and determinant increments; universal bounds and target status are in the written note"}
    output = json.dumps(result, indent=2)+"\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(json.dumps({"status": "PASS", "points": len(points), "steps_each": STEPS,
                          "output": str(args.output)}, indent=2))
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
