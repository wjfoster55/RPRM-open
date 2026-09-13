#!/usr/bin/env python3
"""Exact rational BSD factor enclosures for y^2=x^3-25x and P=(-4,6).

Mathematical justification and source contracts: ../BSD_FACTORS.md.
No database, floating-point special functions, or elliptic-curve backend.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[1]
BITS = 100
D = 1 << BITS


def down(x, d=D):
    x = F(x)
    return F(x.numerator*d//x.denominator, d)


def up(x, d=D):
    x = F(x)
    return -down(-x, d)


def serial(interval):
    return [str(v) for v in interval]


def readable(interval, places):
    d = 10**places
    return down(interval[0], d), up(interval[1], d)


def sqrt_interval(x):
    x = F(x)
    if x < 0:
        raise ValueError("nonnegative radicand required")
    n = isqrt(x.numerator*D*D//x.denominator)
    lo, hi = F(n, D), F(n+1, D)
    assert lo*lo <= x < hi*hi
    return lo, hi


def atan_interval(q, n):
    s = sum((F((-1)**j, (2*j+1)*q**(2*j+1)) for j in range(n)), F(0))
    t = s+F((-1)**n, (2*n+1)*q**(2*n+1))
    return min(s, t), max(s, t)


def pi_interval():
    a, b = atan_interval(5, 64), atan_interval(239, 20)
    return down(16*a[0]-4*b[1]), up(16*a[1]-4*b[0])


def period():
    pi = pi_interval()
    s2, s10 = sqrt_interval(2), sqrt_interval(10)
    a, g = (F(1), F(1)), (down(1/s2[1]), up(1/s2[0]))
    rows = []
    for j in range(7):
        rows.append({"j": j, "arithmetic": serial(a), "geometric": serial(g)})
        a, g = ((down((a[0]+g[0])/2), up((a[1]+g[1])/2)),
                (sqrt_interval(a[0]*g[0])[0], sqrt_interval(a[1]*g[1])[1]))
    rows.append({"j": 7, "arithmetic": serial(a), "geometric": serial(g)})
    agm = (g[0], a[1])
    omega = (down(2*pi[0]/(s10[1]*agm[1])),
             up(2*pi[1]/(s10[0]*agm[0])))
    assert omega[1]-omega[0] < F(1, 10**25)
    return omega, {"differential": "dx/(2y)", "real_components": 2,
                   "formula": "2*pi/(sqrt(10)*AGM(1,1/sqrt(2)))",
                   "pi": serial(pi), "sqrt2": serial(s2), "sqrt10": serial(s10),
                   "agm_iterations": rows, "agm_enclosure": serial(agm),
                   "omega_raw": serial(omega),
                   "omega_readable": serial(readable(omega, 12))}


def log_unit_interval(r, n=96):
    """For 1<=r<=2 use the positive atanh series with an all-term tail."""
    r = F(r)
    assert 1 <= r <= 2
    z = (r-1)/(r+1)
    z2, power, total = z*z, z, F(0)
    for j in range(n):
        total += 2*power/(2*j+1)
        power *= z2
    tail = 2*power/((2*n+1)*(1-z2))
    return down(total), up(total+tail)


def log_integer_interval(n):
    assert isinstance(n, int) and n >= 1
    k = n.bit_length()-1
    if k <= BITS:
        rlo = rhi = F(n, 1 << k)
    else:
        shift = k-BITS
        top = n >> shift
        rlo, rhi = F(top, D), F(top+1, D)
        assert rlo*(1 << k) <= n < rhi*(1 << k)
    ln2 = log_unit_interval(F(2))
    lo, hi = log_unit_interval(rlo)[0], log_unit_interval(rhi)[1]
    return down(k*ln2[0]+lo), up(k*ln2[1]+hi)


def height(steps=8):
    a, b = -4, 1
    rows = []
    for j in range(steps):
        H = max(abs(a), b)
        num, den = (a*a+25*b*b)**2, 4*a*b*(a*a-25*b*b)
        common = gcd(num, den)
        assert 1 <= common <= 2500
        assert H**4 <= max(abs(num), abs(den)) <= 676*H**4
        a, b = num//common, den//common
        if b < 0:
            a, b = -a, -b
        assert b > 0 and gcd(a, b) == 1
        rows.append({"j": j+1, "gcd_removed": common,
                     "numerator_bit_length": abs(a).bit_length(),
                     "denominator_bit_length": b.bit_length()})
    H = max(abs(a), b)
    lH = log_integer_interval(H)
    l2500, l676 = log_integer_interval(2500), log_integer_interval(676)
    scale = 4**steps
    base = (lH[0]/scale, lH[1]/scale)
    bounds = (down(base[0]-l2500[1]/(3*scale)),
              up(base[1]+l676[1]/(3*scale)))
    assert F(1899,1000) < bounds[0] < bounds[1] < F(1900,1000)
    return bounds, {"point": ["-4", "6"], "height_normalization": "lim 4^-n log H_x(2^n P)",
                    "doublings": steps, "duplication_ledger": rows,
                    "last_x_numerator_hex": hex(a), "last_x_denominator_hex": hex(b),
                    "last_height_integer_hex": hex(H),
                    "log_H_interval": serial(lH), "finite_height_interval": serial(base),
                    "log_2500_interval": serial(l2500), "log_676_interval": serial(l676),
                    "tail_lower": str(-l2500[1]/(3*scale)),
                    "tail_upper": str(l676[1]/(3*scale)),
                    "canonical_height_raw": serial(bounds),
                    "canonical_height_readable": serial(readable(bounds, 6)),
                    "regulator_requires": "P primitive in E(Q)/E(Q)_tors; see GENERATOR_PROOF.md"}


def local_factors():
    # Exact specialization of Cremona's Tate algorithm, not a general implementation.
    delta = -16*4*(-25)**3
    assert delta == 2**6*5**6
    # T(1,0,0,1) at 2 gives [0,3,0,-22,-24].
    a2, a4, a6 = 3, -22, -24
    b8 = 4*a2*a6-a4*a4
    assert b8 == -772 and a6 % 4 == 0 and b8 % 8 != 0
    # At 5 no translation is needed. Auxiliary cubic is z^3-z.
    roots = [z for z in range(5) if (z**3-z) % 5 == 0]
    assert roots == [0, 1, 4]
    assert all((3*z*z-1) % 5 != 0 for z in roots)
    return {"minimal_discriminant": delta, "all_bad_primes": [2, 5],
            "p2": {"translation": "T(1,0,0,1)", "model": [0,3,0,-22,-24],
                   "a6": a6, "b8": b8, "valuation_delta": 6,
                   "type": "III", "conductor_exponent": 5, "c2": 2},
            "p5": {"model": [0,0,0,-25,0], "auxiliary_cubic": "z^3-z",
                   "distinct_roots_mod_5": roots, "type": "I0*",
                   "conductor_exponent": 2, "c5": 4},
            "other_cp": 1, "product_cp": 8, "conductor": 800}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT/"evidence"/"bsd_factors.json")
    args = parser.parse_args()
    omega, p = period()
    reg, h = height()
    local = local_factors()
    # Prior verified interval: no rerun of the analytic baseline.
    derivative = (F(556371,250000), F(1114529,500000))
    torsion_order = 4
    rhs = (omega[0]*reg[0]*local["product_cp"]/torsion_order**2,
           omega[1]*reg[1]*local["product_cp"]/torsion_order**2)
    ratio = (derivative[0]/rhs[1], derivative[1]/rhs[0])
    assert F(1,2) < ratio[0] < ratio[1] < F(3,2)
    assert omega[0] > 2 and reg[0] > F(3,2)
    controls = {}
    for name, multiplier in [("only_one_real_component", 2),
                              ("half_height_as_regulator", 2),
                              ("2P_as_primitive_generator", F(1,4))]:
        wrong = (ratio[0]*multiplier, ratio[1]*multiplier)
        assert not (wrong[0] <= 1 <= wrong[1])
        controls[name] = {"wrong_quotient_enclosure": serial(readable(wrong,6)),
                          "excludes_one": True,
                          "scope": "normalization sensitivity, not independent proof of BSD or factors"}
    data = {"model": [0,0,0,-25,0], "bits": BITS,
            "evidence_grade": "exact rational finite calculation plus cited/written analytic bounds",
            "period": p, "height": h, "local_factors": local,
            "torsion_order": torsion_order,
            "torsion_source": "supplied_review/BSD_E5_REVIEW/TORSION_COROLLARY.md",
            "derivative_interval": serial(derivative),
            "derivative_source": "supplied_review/BSD_E5_REVIEW/input/BSD_E5_CODEX_TEST_01_RETURN/INTERVAL_DERIVATION.md",
            "bsd_rhs_without_sha_raw": serial(rhs),
            "bsd_rhs_without_sha_readable": serial(readable(rhs, 6)),
            "quotient_raw": serial(ratio), "quotient_readable": serial(readable(ratio, 6)),
            "quotient_strictly_between": ["1/2", "3/2"],
            "simple_bounds": {"omega_gt": "2", "regulator_gt": "3/2"},
            "normalization_controls": controls,
            "sha_order_conclusion_requires": ["P primitive", "full BSD leading-coefficient theorem"],
            "sha_order_if_dependencies_supplied": 1,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    for key, value in [("Omega", p["omega_readable"]),
                       ("canonical height (full x height)", h["canonical_height_readable"]),
                       ("c2,c5,torsion", [2,4,4]),
                       ("BSD RHS without Sha", data["bsd_rhs_without_sha_readable"]),
                       ("quotient", data["quotient_readable"])]:
        print(f"{key}: {value}")
    print("PASS: exact quotient enclosure contained in (1/2,3/2).")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
