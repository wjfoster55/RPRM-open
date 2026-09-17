"""Fragility spectrum: how many unknown operations can a quotient survive?

TYPED CLAIM UNDER TEST
  Carrier      finite set S, |S| = n, elements distinguishable, equality exact.
  Object       a partition C of S into blocks of sizes (n_1, ..., n_m).
  Operation    a DETERMINISTIC PARTIAL unary map g : S -> S (arity 1),
               later a partial binary map g : S x S -> S (arity 2).
  Survival     C survives g  iff  for all x ~_C y:
                 (i)  x in dom g  <=>  y in dom g          [enabledness, O05 cond. 2]
                 (ii) g(x) ~_C g(y) when defined           [successor,   O05 cond. 3]
  Readout      sigma_1(C) = #{ partial unary g that C survives }
               sigma_2(C) = #{ partial binary g that C survives }

CLAIMED CLOSED FORMS (this is what the brute force must confirm or kill)
  sigma_1(C) = prod_{i=1..m} ( 1 + sum_{j=1..m} n_j ^ n_i )
  sigma_2(C) = prod_{i,j=1..m} ( 1 + sum_{l=1..m} n_l ^ (n_i * n_j) )
  ambient_1  = (n+1)^n          ambient_2 = (n+1)^(n^2)
  Fragility  F_a(C) = 1 - sigma_a(C) / ambient_a      (exact rational)

NULL DECLARED BEFORE RUNNING
  The discrete partition (all singletons) must give sigma_1 = (n+1)^n exactly,
  i.e. F = 0: a partition that distinguishes everything cannot be broken.
  If that fails the instrument is wrong and nothing below counts.

EXTREMAL CONJECTURE (declared before the search)
  Fix n and the block count m. Over all profiles (n_1..n_m) with sum n,
    argmax sigma_1 = (n-m+1, 1, 1, ..., 1)   [maximally unequal]
    argmin sigma_1 = the balanced profile     [sizes differ by at most 1]
  Operational reading: if you must compress, lumping one big blob and keeping
  the rest distinct is the MOST robust choice under unknown dynamics, and
  uniform binning is the LEAST robust.  Exhaustive test below.

No floats anywhere. Fraction and int only.
"""

import sys
from fractions import Fraction
from itertools import product

sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- closed forms

def sigma1(profile):
    return prod(1 + sum(nj ** ni for nj in profile) for ni in profile)


def sigma2(profile):
    return prod(1 + sum(nl ** (ni * nj) for nl in profile)
                for ni in profile for nj in profile)


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


# ---------------------------------------------------------------- brute force

def partitions_of_set(n):
    """All set partitions of range(n), as a tuple of block ids per element."""
    if n == 0:
        yield ()
        return
    for rest in partitions_of_set(n - 1):
        mx = max(rest) + 1 if rest else 0
        for b in range(mx + 1):
            yield rest + (b,)


def profile_of(lbl):
    counts = {}
    for b in lbl:
        counts[b] = counts.get(b, 0) + 1
    return tuple(sorted(counts.values(), reverse=True))


def brute_sigma1(lbl):
    """Count partial unary maps on range(n) that the labelled partition survives."""
    n = len(lbl)
    UNDEF = n
    cnt = 0
    for g in product(range(n + 1), repeat=n):
        ok = True
        for x in range(n):
            for y in range(x + 1, n):
                if lbl[x] != lbl[y]:
                    continue
                dx, dy = g[x] != UNDEF, g[y] != UNDEF
                if dx != dy:
                    ok = False
                    break
                if dx and lbl[g[x]] != lbl[g[y]]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            cnt += 1
    return cnt


def brute_sigma2(lbl):
    """Count partial binary maps on range(n)^2 that the labelled partition survives."""
    n = len(lbl)
    UNDEF = n
    cells = [(x, y) for x in range(n) for y in range(n)]
    cnt = 0
    for g in product(range(n + 1), repeat=n * n):
        tab = dict(zip(cells, g))
        ok = True
        for (x, y) in cells:
            for (u, v) in cells:
                if lbl[x] != lbl[u] or lbl[y] != lbl[v]:
                    continue
                a, b = tab[(x, y)], tab[(u, v)]
                if (a != UNDEF) != (b != UNDEF):
                    ok = False
                    break
                if a != UNDEF and lbl[a] != lbl[b]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            cnt += 1
    return cnt


def int_partitions(n, mx=None):
    if mx is None:
        mx = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, mx), 0, -1):
        for rest in int_partitions(n - k, k):
            yield (k,) + rest


def balanced(n, m):
    q, r = divmod(n, m)
    return tuple(sorted([q + 1] * r + [q] * (m - r), reverse=True))


# ---------------------------------------------------------------- reports

print("=" * 94)
print("TABLE F0  NULL CONTROL, declared before the run.")
print("          Discrete partition must survive every partial unary map: F = 0.")
print("=" * 94)
print(f"{'n':>3} {'sigma_1(discrete)':>19} {'(n+1)^n':>12} {'F':>6} {'verdict':>12}")
for n in range(1, 9):
    s = sigma1((1,) * n)
    amb = (n + 1) ** n
    print(f"{n:>3} {s:>19} {amb:>12} {str(Fraction(amb - s, amb)):>6} "
          f"{'NULL HOLDS' if s == amb else 'NULL VIOLATED':>12}")

print()
print("=" * 94)
print("TABLE F1  Closed form vs exhaustive brute force over ALL set partitions.")
print("          arity 1: every one of the (n+1)^n partial unary maps is tested.")
print("=" * 94)
print(f"{'n':>3} {'set partitions':>15} {'maps tested each':>17} {'formula==brute':>15}")
for n in range(1, 6):
    allp = list(partitions_of_set(n))
    bad = []
    for lbl in allp:
        if sigma1(profile_of(lbl)) != brute_sigma1(lbl):
            bad.append(lbl)
    print(f"{n:>3} {len(allp):>15} {(n+1)**n:>17} "
          f"{'ALL AGREE' if not bad else 'MISMATCH ' + str(bad[:3]):>15}")

print()
print("=" * 94)
print("TABLE F2  arity 2 closed form vs exhaustive brute force.")
print("          every one of the (n+1)^(n^2) partial binary tables is tested.")
print("=" * 94)
print(f"{'n':>3} {'set partitions':>15} {'tables tested each':>19} {'formula==brute':>15}")
for n in range(1, 4):
    allp = list(partitions_of_set(n))
    bad = []
    for lbl in allp:
        if sigma2(profile_of(lbl)) != brute_sigma2(lbl):
            bad.append((lbl, sigma2(profile_of(lbl)), brute_sigma2(lbl)))
    print(f"{n:>3} {len(allp):>15} {(n+1)**(n*n):>19} "
          f"{'ALL AGREE' if not bad else 'MISMATCH ' + str(bad[:2]):>15}")

print()
print("=" * 94)
print("TABLE F3  The fragility spectrum at n = 6: every partition shape, exact rationals.")
print("          F = 1 - sigma_1 / 7^6 = 1 - sigma_1 / 117649")
print("=" * 94)
n = 6
amb = (n + 1) ** n
print(f"{'profile':>18} {'blocks':>7} {'sigma_1':>10} {'F (exact)':>18} {'F approx':>10}")
for p in sorted(int_partitions(n), key=lambda p: (len(p), p)):
    s = sigma1(p)
    F = Fraction(amb - s, amb)
    print(f"{str(p):>18} {len(p):>7} {s:>10} {str(F):>18} {float(F):>10.6f}")

print()
print("=" * 94)
print("TABLE F4  EXTREMAL CONJECTURE, exhaustive over every profile for each (n, m).")
print("          max survival predicted at (n-m+1, 1, ..., 1); min at the balanced profile.")
print("=" * 94)
print(f"{'n':>3} {'m':>3} {'#profiles':>10} {'argmax observed':>22} {'max OK':>7} "
      f"{'argmin observed':>22} {'min OK':>7}")
maxfail = minfail = 0
for n in range(2, 25):
    for m in range(1, n + 1):
        profs = [p for p in int_partitions(n) if len(p) == m]
        if len(profs) < 2:
            continue
        vals = [(sigma1(p), p) for p in profs]
        hi = max(vals)[1]
        lo = min(vals)[1]
        predhi = tuple([n - m + 1] + [1] * (m - 1))
        predlo = balanced(n, m)
        okh = hi == predhi
        okl = lo == predlo
        maxfail += 0 if okh else 1
        minfail += 0 if okl else 1
        if n <= 9 or not (okh and okl):
            print(f"{n:>3} {m:>3} {len(profs):>10} {str(hi):>22} {'OK' if okh else 'FAIL':>7} "
                  f"{str(lo):>22} {'OK' if okl else 'FAIL':>7}")
print(f"  ... n up to 24 searched exhaustively.  argmax counterexamples: {maxfail}   "
      f"argmin counterexamples: {minfail}")

print()
print("=" * 94)
print("TABLE F5  HOSTILE CASE. Does the extremal conjecture survive arity 2?")
print("          Same profiles, sigma_2 instead of sigma_1.")
print("=" * 94)
print(f"{'n':>3} {'m':>3} {'argmax_1':>18} {'argmax_2':>18} {'same?':>7} "
      f"{'argmin_1':>18} {'argmin_2':>18} {'same?':>7}")
h2 = l2 = 0
for n in range(2, 13):
    for m in range(1, n + 1):
        profs = [p for p in int_partitions(n) if len(p) == m]
        if len(profs) < 2:
            continue
        a1 = max((sigma1(p), p) for p in profs)[1]
        b1 = min((sigma1(p), p) for p in profs)[1]
        a2 = max((sigma2(p), p) for p in profs)[1]
        b2 = min((sigma2(p), p) for p in profs)[1]
        h2 += 0 if a1 == a2 else 1
        l2 += 0 if b1 == b2 else 1
        if n <= 7 or a1 != a2 or b1 != b2:
            print(f"{n:>3} {m:>3} {str(a1):>18} {str(a2):>18} "
                  f"{'yes' if a1 == a2 else 'NO':>7} {str(b1):>18} {str(b2):>18} "
                  f"{'yes' if b1 == b2 else 'NO':>7}")
print(f"  ... n up to 12.  argmax disagreements: {h2}   argmin disagreements: {l2}")

print()
print("=" * 94)
print("TABLE F6  The applied readout: a modeller compresses n states to m blocks and")
print("          does NOT know the full operation set. Probability an unknown partial")
print("          unary operation preserves the abstraction, exact rational.")
print("          balanced binning vs one-big-blob, head to head.")
print("=" * 94)
print(f"{'n':>3} {'m':>3} {'P(survive) balanced':>22} {'P(survive) blob':>22} "
      f"{'blob / balanced':>16}")
for n in (6, 8, 10, 12, 16, 20):
    for m in (2, n // 2):
        if m < 2 or m >= n:
            continue
        pb = Fraction(sigma1(balanced(n, m)), (n + 1) ** n)
        pl = Fraction(sigma1(tuple([n - m + 1] + [1] * (m - 1))), (n + 1) ** n)
        ratio = float(pl / pb) if pb else float("inf")
        print(f"{n:>3} {m:>3} {float(pb):>22.10g} {float(pl):>22.10g} {ratio:>16.4g}")
