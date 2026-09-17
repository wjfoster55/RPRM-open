"""Map the boundary of the (now false) rho-monotonicity conjecture.

The conjecture dies at n = 17, (9,4,4) -> (9,5,3). Every failing exchange in the
n <= 22 sweep has m >= 3, and the listed failures all look alike: a LARGE block
sits out while two MEDIUM blocks exchange. This script tests that reading, and
runs the hostile families the brief names.
"""

import sys
import itertools
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


def sigma_E(p):
    return prod(1 + sum(n ** k for n in p) for k in p)


def sigma_blind(p):
    return prod(sum((n + 1) ** k for n in p) - (len(p) - 1) for k in p)


def rho(p):
    return Fraction(sigma_E(p), sigma_blind(p))


def sigma_E_r(p, r):
    es = [prod(t) for t in itertools.product(p, repeat=r)]
    return prod(1 + sum(n ** e for n in p) for e in es)


def sigma_blind_r(p, r):
    es = [prod(t) for t in itertools.product(p, repeat=r)]
    m = len(p)
    return prod(sum((n + 1) ** e for n in p) - (m - 1) for e in es)


def parts(n, m, top=None):
    if top is None:
        top = n
    if m == 1:
        if 1 <= n <= top:
            yield (n,)
        return
    for f in range(min(top, n - m + 1), 0, -1):
        for r in parts(n - f, m - 1, f):
            yield (f,) + r


def exchange_pairs(p):
    """Yield (q, a, b) for each dominance-increasing exchange a>=b>=2."""
    seen = set()
    for i in range(len(p)):
        for j in range(len(p)):
            if i == j:
                continue
            a, b = p[i], p[j]
            if b >= 2 and a >= b:
                q = list(p)
                q[i], q[j] = a + 1, b - 1
                q = tuple(sorted(q, reverse=True))
                if (q, a, b) not in seen:
                    seen.add((q, a, b))
                    yield q, a, b


print("=" * 76)
print("A. THE SPECTATOR READING")
print("   In every failure, is there a block strictly larger than both")
print("   exchanged parts - i.e. a large block sitting out the exchange?")
print("=" * 76)
tot = bad = 0
with_spec = without_spec = 0
for n in range(2, 23):
    for m in range(1, n + 1):
        for p in parts(n, m):
            rp = rho(p)
            for q, a, b in exchange_pairs(p):
                tot += 1
                if rho(q) <= rp:
                    bad += 1
                    # is some OTHER part strictly bigger than a?
                    rest = list(p)
                    rest.remove(a)
                    rest.remove(b)
                    if rest and max(rest) > a:
                        with_spec += 1
                    else:
                        without_spec += 1
print(f"  failures {bad}   with a strictly larger spectator {with_spec}"
      f"   without {without_spec}")
if without_spec == 0:
    print("  CONFIRMED: every failure has a block strictly larger than both")
    print("  exchanged parts. No spectator that big, no failure.")
else:
    print("  NOT confirmed - the reading is wrong.")

print()
print("=" * 76)
print("B. m = 2 pushed hard (no spectators exist at all when m = 2)")
print("=" * 76)
tot = bad = 0
first = None
for n in range(4, 161):
    for p in parts(n, 2):
        rp = rho(p)
        for q, a, b in exchange_pairs(p):
            tot += 1
            if rho(q) <= rp:
                bad += 1
                if first is None:
                    first = (p, q)
print(f"  n up to 160, exchanges {tot:,}   failures {bad}")
print(f"  FIRST FAILURE {first}" if first else
      "  m = 2 survives everywhere tested. Consistent with the spectator reading.")

print()
print("=" * 76)
print("C. m = 3, the smallest m that fails, pushed to larger n")
print("=" * 76)
tot = bad = 0
firsts = []
for n in range(6, 41):
    for p in parts(n, 3):
        rp = rho(p)
        for q, a, b in exchange_pairs(p):
            tot += 1
            if rho(q) <= rp:
                bad += 1
                if len(firsts) < 5:
                    firsts.append((p, q))
print(f"  n up to 40, exchanges {tot:,}   failures {bad:,}  ({100*bad/tot:.2f}%)")
for p, q in firsts:
    print(f"      {p} -> {q}")

print()
print("=" * 76)
print("D. ARITY > 1")
print("=" * 76)
for r in (1, 2):
    tot = bad = 0
    first = None
    hi = 22 if r == 1 else 11
    for n in range(2, hi + 1):
        for m in range(1, min(n, 4) + 1):
            for p in parts(n, m):
                rp = Fraction(sigma_E_r(p, r), sigma_blind_r(p, r))
                for q, a, b in exchange_pairs(p):
                    tot += 1
                    rq = Fraction(sigma_E_r(q, r), sigma_blind_r(q, r))
                    if rq <= rp:
                        bad += 1
                        if first is None:
                            first = (p, q)
    print(f"  arity {r} (n <= {hi}, m <= 4): exchanges {tot:,}  failures {bad:,}"
          f"   first {first}")

print()
print("=" * 76)
print("E. EHRENFEST BINOMIAL SHAPES vs their dominance neighbours")
print("=" * 76)
from math import comb
for d in range(3, 8):
    m = d + 1
    p = tuple(sorted((comb(d, k) for k in range(m)), reverse=True))
    rp = rho(p)
    ups = list(exchange_pairs(p))
    worse = [(q, float(rho(q) - rp)) for q, a, b in ups if rho(q) <= rp]
    print(f"  d={d} shape {p}")
    print(f"      rho = {float(rp):.9f}   upward exchanges {len(ups)}   "
          f"that LOWER rho: {len(worse)}")
    for q, dd in worse[:3]:
        print(f"        {q}  delta rho = {dd:.3e}")

print()
print("=" * 76)
print("F. THE 66 CLASSICAL LOSSES ARE THE EASY CASES, NOT THE HOSTILE ONES")
print("=" * 76)
both = down_blind = 0
for n in range(2, 23):
    for m in range(1, n + 1):
        for p in parts(n, m):
            sb_p, rp = sigma_blind(p), rho(p)
            for q, a, b in exchange_pairs(p):
                if sigma_blind(q) < sb_p:          # classical count went DOWN
                    down_blind += 1
                    if rho(q) > rp:
                        both += 1
print(f"  exchanges where sigma_blind decreases: {down_blind}")
print(f"  of those, rho increased: {both}   ({'all' if both==down_blind else 'NOT all'})")
print("  Expected: when the denominator falls and the numerator provably rises,")
print("  rho must rise. The hostile region is the opposite one - where the")
print("  denominator rises FASTER than the numerator, by a fraction of a percent.")
