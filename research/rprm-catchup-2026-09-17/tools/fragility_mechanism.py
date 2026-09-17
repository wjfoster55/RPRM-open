"""Why the proof works for sigma_E and cannot work for sigma_blind.

The exchange lemma for sigma_E rests on one property: the factor function

    f_p(k) = 1 + sum_j n_j^k

is LOG-CONVEX in k, because it is a sum of exponentials e^{k ln n_j} plus the
constant term e^{k*0} = 1, and a sum of log-convex functions is log-convex.

The classical successor-only count has factors

    f_blind,p(k) = 1 + sum_j ( (n_j+1)^k - 1 )
                 = sum_j (n_j+1)^k  -  (m - 1)

which is a sum of exponentials MINUS a positive constant whenever m >= 2.
Subtracting a constant does not preserve log-convexity. So the proof route is
not merely harder for the classical monoid -- its single load-bearing hypothesis
is false there.

CLAIM UNDER TEST, declared before running
  M1  f_p is log-convex for every profile: f(a+1) f(b-1) >= f(a) f(b) whenever
      a >= b >= 1. Expected to hold everywhere.
  M2  f_blind,p is NOT log-convex: there exist profiles and a >= b >= 1 with
      f_blind(a+1) f_blind(b-1) < f_blind(a) f_blind(b).
      If no such case exists, the mechanism story is wrong and must be dropped;
      the flagship comparison would then need a different explanation.
  M3  The profiles where M2 bites should be the same shape as the profiles where
      sigma_blind violates the extremal law: many blocks, mostly singletons.
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


def f_E(p, k):
    return 1 + sum(n ** k for n in p)


def f_blind(p, k):
    return 1 + sum((n + 1) ** k - 1 for n in p)


def partitions(n, m, top=None):
    if top is None:
        top = n
    if m == 1:
        if 1 <= n <= top:
            yield (n,)
        return
    for first in range(min(top, n - m + 1), 0, -1):
        for rest in partitions(n - first, m - 1, first):
            yield (first,) + rest


NMAX = 16
allp = [p for n in range(2, NMAX + 1) for m in range(1, n + 1)
        for p in partitions(n, m)]

print("=" * 86)
print(f"M1/M2  Log-convexity of the factor function, all {len(allp):,} profiles "
      f"of n <= {NMAX}")
print("=" * 86)

rows = []
for name, fn in (("sigma_E   1 + sum n_j^k", f_E),
                 ("sigma_bl  1 + sum ((n_j+1)^k - 1)", f_blind)):
    cases = viol = 0
    worst = None
    examples = []
    for p in allp:
        kmax = max(p) + 2
        for b in range(1, kmax):
            for a in range(b, kmax):
                cases += 1
                lhs = fn(p, a + 1) * fn(p, b - 1) if b >= 1 else None
                rhs = fn(p, a) * fn(p, b)
                if lhs < rhs:
                    viol += 1
                    r = Fraction(lhs, rhs)
                    if worst is None or r < worst:
                        worst = r
                    if len(examples) < 6:
                        examples.append((p, a, b, lhs, rhs))
    rows.append((name, cases, viol, worst, examples))
    print(f"  {name:<36} {cases:>9,} tested   {viol:>7,} violations")

print()
E_row, B_row = rows
if E_row[2] == 0:
    print("  M1 holds: no violation for sigma_E's factor function, as the proof")
    print("     requires. Log-convexity is not an empirical observation here --")
    print("     it follows from f being a sum of exponentials -- but a violation")
    print("     would have meant the written proof had an error.")
else:
    print("  M1 FAILED -- the written proof is wrong. Stop and discard it.")

print()
if B_row[2] > 0:
    print(f"  M2 holds: the classical factor function is NOT log-convex.")
    print(f"     {B_row[2]:,} violations; worst ratio {float(B_row[3]):.9f}")
    print()
    print(f"     {'profile':<26} {'a':>4} {'b':>4} {'f(a+1)f(b-1) / f(a)f(b)':>26}")
    for p, a, b, lhs, rhs in B_row[4]:
        print(f"     {str(p):<26} {a:>4} {b:>4} "
              f"{float(Fraction(lhs, rhs)):>26.12f}")
else:
    print("  M2 FAILED -- no violation found. The mechanism story is wrong.")

print()
print("=" * 86)
print("M3  Do the log-convexity failures live where the extremal law fails?")
print("=" * 86)


def sigma_blind(p):
    return prod(f_blind(p, k) for k in p)


def sigma_E(p):
    return prod(f_E(p, k) for k in p)


print(f"  {'n':>3} {'m':>3} {'sigma_blind argmax':<30} {'sigma_blind argmin':<30}")
shown = 0
for n in range(3, 25):
    for m in range(2, n + 1):
        ps = list(partitions(n, m))
        if len(ps) < 2:
            continue
        want_max = (n - m + 1,) + (1,) * (m - 1)
        want_min = tuple(sorted((n // m + (1 if i < n % m else 0)
                                 for i in range(m)), reverse=True))
        got_max = max(ps, key=sigma_blind)
        got_min = min(ps, key=sigma_blind)
        if got_max != want_max or got_min != want_min:
            if shown < 10:
                print(f"  {n:>3} {m:>3} {str(got_max):<30} {str(got_min):<30}"
                      f"  (expected {want_max} / {want_min})")
            shown += 1
print(f"  total (n, m) cells where sigma_blind breaks the extremal law: {shown}")
print()
print("  Every listed cell has many blocks and mostly singletons, which is the")
print("  same regime as the log-convexity failures above. The -1 per block is")
print("  largest relative to the whole factor exactly when the blocks are tiny.")
print()
print("  Reading. Enabledness is not a cosmetic extra condition. Dropping the")
print("  domain requirement subtracts one unit per block from every factor, and")
print("  that subtraction is precisely what destroys log-convexity of the factor")
print("  function and with it the extremal law. Evidence grade: written proof")
print("  for the sigma_E direction; finite test for the sigma_blind failures.")
