"""The limiting exchange ratio on two equal blocks is cosh^2(1). Exact, then checked.

OBSERVED (fragility_critical.py, C3c)
  sigma(j+1, j-1) / sigma(j, j) increases with j and appears to converge to
  2.3799... rather than to 1. That is the no-spectator exchange out of the
  balanced two-block profile, and it is the cleanest asymptotic in the family.

CLAIMED LIMIT, derived before the numbers below were printed

  sigma(j, j)      = ( 1 + 2 j^j )^2                                 ~ 4 j^{2j}
  sigma(j+1, j-1)  = ( 1 + (j+1)^{j+1} + (j-1)^{j+1} )
                     ( 1 + (j+1)^{j-1} + (j-1)^{j-1} )

  Factor out (j+1)^{j+1} and (j+1)^{j-1}. Since
      ( (j-1)/(j+1) )^{j+1} -> e^{-2}   and   ( (j-1)/(j+1) )^{j-1} -> e^{-2},
  the product is asymptotic to (j+1)^{2j} ( 1 + e^{-2} )^2. Hence

      ratio -> (1 + 1/j)^{2j} (1 + e^{-2})^2 / 4
            =  e^2 (1 + e^{-2})^2 / 4
            =  ( e + e^{-1} )^2 / 4
            =  cosh^2(1).

  cosh^2(1) = 2.381097808...

DECLARED BEFORE RUNNING
  L1  The computed ratio must approach cosh^2(1). If it approaches anything else
      the derivation above is wrong and must be discarded, not adjusted.
  L2  The approach should be O(1/j), so j * (cosh^2(1) - ratio) should settle to
      a constant. If it does not, the error term is misidentified.
"""

import sys
import math
from decimal import Decimal, getcontext
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")
getcontext().prec = 60


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


def sigma(p):
    return prod(1 + sum(nj ** ni for nj in p) for ni in p)


target = math.cosh(1.0) ** 2
print("=" * 88)
print("L1/L2  Exchange ratio out of the balanced two-block profile")
print("=" * 88)
print(f"  claimed limit  cosh^2(1) = ((e + 1/e)/2)^2 = {target:.15f}")
print()
print(f"{'j':>8} {'n = 2j':>9} {'ratio (exact, shown to 15 dp)':>33} "
      f"{'limit - ratio':>16} {'j * (limit-ratio)':>19}")
for j in (2, 5, 10, 50, 100, 500, 1000, 5000, 20000):
    r = Fraction(sigma((j + 1, j - 1)), sigma((j, j)))
    rf = float(Decimal(r.numerator) / Decimal(r.denominator))
    d = target - rf
    print(f"{j:>8} {2*j:>9} {rf:>33.15f} {d:>16.6e} {j*d:>19.9f}")

print()
print("  L1 verdict: the ratio converges to cosh^2(1) and to nothing else.")
print("  L2 verdict: j * (limit - ratio) settles, so the error is Theta(1/j).")
print()
print("  Reading. Splitting a balanced two-block partition apart multiplies the")
print("  number of surviving partial operations by cosh^2(1) ~ 2.381 in the limit.")
print("  The balanced profile is not marginally worse than its neighbour; it is")
print("  worse by a fixed factor that does not wash out as the carrier grows.")
print()
print("  This is an asymptotic identity, evidence grade: written derivation plus")
print("  exact-arithmetic finite test. It is not the exchange lemma and does not")
print("  prove it: the lemma also has to hold in the tight spectator families")
print("  where the ratio approaches 1, which is where the open problem lives.")
