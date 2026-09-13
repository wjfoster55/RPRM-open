"""Exact local-input replay for E_34; no curve database or rank routine.

This is a special-case Tate-branch certificate, not a general Tate algorithm.
The handwritten justification and theorem boundary are LOCAL_ANALYTIC_INPUTS.md.
Run: python -I -B research/bsd-rank-two-01/work/local_inputs.py --limit 1000
"""

import argparse
import json
from math import isqrt
from pathlib import Path

MODEL = (0, 0, 0, -1156, 0)
BAD_PRIMES = (2, 17)
CONDUCTOR = 18496
ROOT_NUMBER = 1  # Congruent-number family sign theorem; not inferred from rank.


def invariants(a):
    a1, a2, a3, a4, a6 = a
    b2 = a1*a1 + 4*a2
    b4 = a1*a3 + 2*a4
    b6 = a3*a3 + 4*a6
    b8 = a1*a1*a6 + 4*a2*a6 - a1*a3*a4 + a2*a3*a3 - a4*a4
    c4 = b2*b2 - 24*b4
    c6 = -b2**3 + 36*b2*b4 - 216*b6
    delta = -b2*b2*b8 - 8*b4**3 - 27*b6*b6 + 9*b2*b4*b6
    assert c4**3 - c6*c6 == 1728*delta
    return dict(b2=b2, b4=b4, b6=b6, b8=b8, c4=c4, c6=c6, delta=delta)


def valuation(x, p):
    if x == 0:
        raise ValueError("valuation(0) is infinite; do not encode it as an integer")
    k = 0
    while x % p == 0:
        k += 1
        x //= p
    return k


def translate(a, r=0, t=0):
    """x_old=x_new+r, y_old=y_new+t; no scaling or xy shear."""
    a1, a2, a3, a4, a6 = a
    return (
        a1,
        a2 + 3*r,
        a3 + a1*r + 2*t,
        a4 + 2*a2*r + 3*r*r - a1*t,
        a6 + a4*r + a2*r*r + r**3 - a3*t - a1*r*t - t*t,
    )


def local_certificate():
    inv = invariants(MODEL)
    assert inv["c4"] == 55488 and inv["c6"] == 0
    assert inv["delta"] == 64*34**6 == 2**12*17**6
    vd2, vd17 = valuation(inv["delta"], 2), valuation(inv["delta"], 17)
    # At 17 a minimality-reducing scale would subtract 12 from valuation 6.
    assert vd17 == 6 < 12
    # At 2 scale=2 gives impossible integral-model c4: even but not 16-divisible.
    scaled_c4 = inv["c4"] // 2**4
    assert scaled_c4 == 3468 and scaled_c4 % 2 == 0 and scaled_c4 % 16 == 12

    # Early Tate branches fail for each prime; preliminary translations are zero.
    for p in BAD_PRIMES:
        assert inv["c4"] % p == 0
        assert MODEL[4] % (p*p) == 0
        assert inv["b8"] % (p**3) == 0
        assert inv["b6"] % (p**3) == 0
        assert all(x % (p**k) == 0 for x, k in zip(MODEL, (1, 1, 2, 2, 3)))

    # At 17 the auxiliary cubic is T^3 - 4T, squarefree and fully split.
    roots17 = [z for z in range(17) if (z**3 - 4*z) % 17 == 0]
    assert roots17 == [0, 2, 15]
    assert all((3*z*z - 4) % 17 for z in roots17)

    # At 2 cubic T^3-289T = T(T+1)^2 modulo 2; move double root 1 by x += 2.
    assert all((z**3 - 289*z - z*(z+1)**2) % 2 == 0 for z in range(2))
    shifted = translate(MODEL, r=2)
    assert shifted == (0, 6, 0, -1144, -2304)
    assert invariants(shifted)["delta"] == inv["delta"]
    a1, a2, a3, a4, a6 = shifted
    xa_odd = (a2//2, a3//4, a4//8, a6//16)
    assert xa_odd == (3, 0, -143, -144)
    odd_discriminant = xa_odd[1]**2 + 4*xa_odd[3]
    assert odd_discriminant == -576 and odd_discriminant % 2 == 0
    # Required t/4 == xa6 mod 2 is 0; choose t=0, then increase my from 4 to 8.
    assert xa_odd[3] % 2 == 0 and a3 % 8 == 0 and a6 % 32 == 0
    xa_even = (a2//2, a3//8, a4//8, a6//32)
    assert xa_even == (3, 0, -143, -72)
    even_discriminant = xa_even[2]**2 - 4*xa_even[0]*xa_even[3]
    assert even_discriminant == 21313 and even_discriminant % 2 == 1
    roots2 = [z for z in range(2) if (3*z*z - 143*z - 72) % 2 == 0]
    assert roots2 == [0, 1]
    f2, f17 = vd2 - 2 - 4, vd17 - 4
    assert (f2, f17) == (6, 2)
    assert 2**f2 * 17**f17 == CONDUCTOR == 16*34**2
    assert 34 == 2*17 and 34 % 8 == 2
    return {
        "model": MODEL, "invariants": inv,
        "global_minimal_model": MODEL,
        "local": {
            "2": {"v_delta": vd2, "type": "I2*", "f": f2, "tamagawa": 4,
                  "shifted_model": shifted, "odd_auxiliary": xa_odd,
                  "even_auxiliary": xa_even, "even_discriminant": even_discriminant,
                  "terminal_quadratic_roots": roots2, "Euler_polynomial": [1]},
            "17": {"v_delta": vd17, "type": "I0*", "f": f17, "tamagawa": 4,
                   "auxiliary_cubic_roots": roots17, "Euler_polynomial": [1]},
        },
        "conductor": CONDUCTOR,
        "root_number": ROOT_NUMBER,
        "root_number_basis": "Elkies family theorem: positive squarefree n=34, n mod 8=2",
        "status": "exact arithmetic replay using the cited Tate and root-number theorems",
    }


def sieve(limit):
    if type(limit) is not int or limit < 1:
        raise ValueError("limit must be a positive integer")
    spf = list(range(limit+1))
    for p in range(2, isqrt(limit)+1):
        if spf[p] == p:
            for m in range(p*p, limit+1, p):
                if spf[m] == m:
                    spf[m] = p
    return spf, [p for p in range(2, limit+1) if spf[p] == p]


def prime_trace(p):
    """Exact point count on the good reduction; additive traces supplied separately."""
    if p in BAD_PRIMES:
        return 0
    if p < 3 or any(p % q == 0 for q in range(2, isqrt(p)+1)):
        raise ValueError("p must be prime")
    square_multiplicity = [0]*p
    for y in range(p):
        square_multiplicity[y*y % p] += 1
    points = 1 + sum(square_multiplicity[(x*x*x-1156*x) % p] for x in range(p))
    ap = p+1-points
    assert ap*ap <= 4*p  # Finite consistency check; Hasse supplies universal validity.
    return ap


def coefficients(limit):
    """Return a[0..limit] with unused sentinel a[0]=0 and a[1]=1."""
    spf, primes = sieve(limit)
    ap = {p: prime_trace(p) for p in primes}
    a = [0]*(limit+1)
    a[1] = 1
    for m in range(2, limit+1):
        p = spf[m]
        if p in BAD_PRIMES:
            a[m] = 0
            continue
        q, exp = m, 0
        while q % p == 0:
            q //= p
            exp += 1
        prev, curr = 1, ap[p]
        for _ in range(2, exp+1):
            prev, curr = curr, ap[p]*curr - p*prev
        a[m] = curr*a[q]
    return a, ap


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = local_certificate()
    a, ap = coefficients(args.limit)
    # Independent character-sum method checks small-prime point-count implementation.
    for p, value in ap.items():
        if p not in BAD_PRIMES and p <= 101:
            trace = 0
            for x in range(p):
                legendre = pow((x**3-1156*x) % p, (p-1)//2, p)
                trace -= -1 if legendre == p-1 else legendre
            assert trace == value
    for m in range(1, args.limit+1):
        assert abs(a[m]) <= 2*m
        if m % 2 == 0 or m % 17 == 0:
            assert a[m] == 0
    result["finite_coefficients"] = {
        "limit": args.limit, "primes": ap,
        "a_n_including_unused_zero_sentinel": a,
        "checks": ["good prime Hasse inequalities", "independent character sums through 101",
                   "bad-prime multiples vanish", "finite consistency with universal bound |a_n|<=2n"],
    }
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(json.dumps({"status": "PASS", "conductor": CONDUCTOR, "root_number": ROOT_NUMBER,
                          "limit": args.limit, "output": str(args.output)}, indent=2))
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
