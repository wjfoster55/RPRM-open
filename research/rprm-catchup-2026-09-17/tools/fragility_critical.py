"""Targeted stress test on the tightest exchange family.

E4 in fragility_exchange.py showed the exchange ratio sigma(C')/sigma(C) is
always minimised by the same shape: one large block acting as a spectator, and
two EQUAL blocks being split apart,

        (K, j, j)  ->  (K, j+1, j-1)

with the ratio falling toward 1 as n grows: 1.768 at n = 6, 1.0065 at n = 30.
If the exchange lemma is going to fail anywhere it fails here, so this file
attacks that family directly and far beyond the range the general search reached.

DECLARED BEFORE RUNNING
  C1  If the ratio ever reaches or drops below 1, the exchange lemma is REFUTED
      and with it the strongest form of the extremal law. Report the first such
      case in full. No repair, no reparameterisation.
  C2  If the ratio stays above 1 but converges to 1, report the convergence rate.
      A ratio converging to 1 from above is consistent with the lemma and is
      exactly why the crude sandwich bound cannot prove it.
  C3  Also attack two further tight shapes suggested by the same pattern:
        (K, j, j, j) -> (K, j+1, j, j-1)      three equal blocks
        (j, j)       -> (j+1, j-1)            no spectator at all
"""

import sys
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


def sigma(p):
    return prod(1 + sum(nj ** ni for nj in p) for ni in p)


def ratio(p, q):
    return Fraction(sigma(q), sigma(p))


def rule(t):
    print()
    print("=" * 92)
    print(t)
    print("=" * 92)


rule("C1  THE CRITICAL FAMILY  (K, j, j) -> (K, j+1, j-1),  spectator K, split j")
print(f"{'j':>4} {'K':>6} {'n':>7} {'ratio - 1':>22} {'ratio > 1':>10}")
fails = 0
tested = 0
for j in (2, 3, 4, 5, 6, 8, 10, 14, 20, 30, 50, 80, 120, 200):
    for K in (j, 2 * j, 5 * j, 20 * j, 200 * j, 2000 * j):
        p = tuple(sorted((K, j, j), reverse=True))
        q = tuple(sorted((K, j + 1, j - 1), reverse=True))
        r = ratio(p, q)
        tested += 1
        ok = r > 1
        if not ok:
            fails += 1
        d = r - 1
        print(f"{j:>4} {K:>6} {K+2*j:>7} {float(d):>22.10g} {'yes' if ok else 'REFUTED':>10}")
print(f"  tested {tested}   refutations: {fails}")

rule("C1b  Same family, spectator pushed to the extreme: K enormous relative to j")
print("     If a huge spectator block can drown the gain, this is where it shows.")
print(f"{'j':>4} {'K':>12} {'ratio - 1':>24} {'verdict':>10}")
f2 = 0
for j in (2, 3, 5, 10, 25, 60):
    for K in (10 ** 3, 10 ** 4, 10 ** 5):
        p = tuple(sorted((K, j, j), reverse=True))
        q = tuple(sorted((K, j + 1, j - 1), reverse=True))
        r = ratio(p, q)
        if r <= 1:
            f2 += 1
        print(f"{j:>4} {K:>12} {float(r-1):>24.10g} {'ok' if r>1 else 'REFUTED':>10}")
print(f"  refutations: {f2}")

rule("C2  Convergence rate along  (2j, j, j) -> (2j, j+1, j-1)")
print("     Is (ratio - 1) shrinking geometrically, or approaching a positive floor?")
print(f"{'j':>5} {'n':>7} {'ratio - 1':>22} {'previous / current':>20}")
prev = None
for j in range(2, 41):
    K = 2 * j
    p = tuple(sorted((K, j, j), reverse=True))
    q = tuple(sorted((K, j + 1, j - 1), reverse=True))
    d = ratio(p, q) - 1
    rel = float(prev / d) if prev is not None and d != 0 else float("nan")
    print(f"{j:>5} {K+2*j:>7} {float(d):>22.10g} {rel:>20.6f}")
    prev = d

rule("C3a  Three equal blocks: (K, j, j, j) -> (K, j+1, j, j-1)")
print(f"{'j':>4} {'K':>8} {'n':>7} {'ratio - 1':>24} {'verdict':>10}")
f3 = 0
for j in (2, 3, 4, 6, 10, 20, 40, 80):
    for K in (j, 4 * j, 100 * j):
        p = tuple(sorted((K, j, j, j), reverse=True))
        q = tuple(sorted((K, j + 1, j, j - 1), reverse=True))
        r = ratio(p, q)
        if r <= 1:
            f3 += 1
        print(f"{j:>4} {K:>8} {K+3*j:>7} {float(r-1):>24.10g} "
              f"{'ok' if r>1 else 'REFUTED':>10}")
print(f"  refutations: {f3}")

rule("C3b  Many equal blocks, no large spectator: (j,)*m -> (j+1, j-1, j,...)")
print("     The balanced profile is the conjectured minimiser, so every exchange")
print("     out of it must increase sigma. Tested for m up to 40.")
print(f"{'j':>4} {'m':>4} {'n':>7} {'ratio - 1':>24} {'verdict':>10}")
f4 = 0
for j in (2, 3, 5, 9, 17):
    for m in (2, 3, 5, 10, 25, 40):
        p = (j,) * m
        q = tuple(sorted((j + 1, j - 1) + (j,) * (m - 2), reverse=True))
        r = ratio(p, q)
        if r <= 1:
            f4 += 1
        print(f"{j:>4} {m:>4} {j*m:>7} {float(r-1):>24.10g} "
              f"{'ok' if r>1 else 'REFUTED':>10}")
print(f"  refutations: {f4}")

rule("C3c  No spectator at all: (j, j) -> (j+1, j-1), pushed to j = 2000")
print(f"{'j':>6} {'n':>7} {'ratio':>22} {'verdict':>10}")
f5 = 0
for j in (2, 3, 5, 10, 30, 100, 300, 1000, 2000):
    p = (j, j)
    q = (j + 1, j - 1)
    r = ratio(p, q)
    if r <= 1:
        f5 += 1
    print(f"{j:>6} {2*j:>7} {float(r):>22.10g} {'ok' if r>1 else 'REFUTED':>10}")
print(f"  refutations: {f5}")

rule("SUMMARY")
total = fails + f2 + f3 + f4 + f5
print(f"  total refutations across every targeted family: {total}")
print()
if total == 0:
    print("  The exchange lemma survived its own worst case. The ratio approaches 1")
    print("  from above and does not cross it in any family tested. That is exactly")
    print("  the behaviour that makes the crude sandwich bound useless and makes the")
    print("  lemma a real open problem rather than a formality.")
else:
    print("  REFUTED. See the rows marked REFUTED above. The extremal law's strongest")
    print("  form does not hold and the conjecture must be restated or withdrawn.")
