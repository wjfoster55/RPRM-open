"""Is rho = sigma_E / sigma_blind monotone along dominance, and if so why?

Candidate mechanism, to be tested rather than assumed. Write

    f_E(p,k) = 1 + sum_j n_j^k                  (numerator factor)
    f_B(p,k) = sum_j (n_j+1)^k - (m-1)          (denominator factor)
    g_p(k)   = f_E(p,k) / f_B(p,k)

so that rho(p) = prod_i g_p(n_i). The main theorem's two-step architecture
should then apply verbatim if both of these hold:

  L1  g_p is log-convex in k.  This would follow from f_E log-convex (proved)
      TOGETHER WITH f_B log-CONCAVE - the exact mirror of the property whose
      failure breaks sigma_blind's own extremal law.
  L2  g_q(k) >= g_p(k) pointwise in k whenever q dominates p.

L2 has a readable equivalent. Since f_B = f_E + D with
D(p,k) = sum_j[(n_j+1)^k - n_j^k] - m, we have g = 1/(1 + D/f_E), so L2 says
exactly that D/f_E DECREASES under dominance. Heuristically f_E ~ max^k while
D ~ k*max^(k-1), so D/f_E ~ k/max, which falls as the largest block grows. That
is a mechanism, not a proof, and it is what the tests below are aimed at.

If L1 and L2 both hold the conclusion is stronger than the main theorem's: the
numerator's exponent step pushes rho up, and the denominator's pushes it up too
(because log-concavity reverses), so rho should be MORE robust than sigma_E.
"""

import sys
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


def f_E(p, k):
    return 1 + sum(n ** k for n in p)


def f_B(p, k):
    return sum((n + 1) ** k for n in p) - (len(p) - 1)


def sigma_E(p):
    return prod(f_E(p, n) for n in p)


def sigma_blind(p):
    return prod(f_B(p, n) for n in p)


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


def allparts(lo, hi):
    for n in range(lo, hi + 1):
        for m in range(1, n + 1):
            yield from parts(n, m)


def exchanges(p):
    """All q strictly above p by one dominance-increasing exchange, a >= b >= 2."""
    out = set()
    for i in range(len(p)):
        for j in range(len(p)):
            if i == j:
                continue
            a, b = p[i], p[j]
            if b >= 2 and a >= b:
                q = list(p)
                q[i], q[j] = a + 1, b - 1
                out.add(tuple(sorted(q, reverse=True)))
    return out


KMAX = 14
NLO, NHI = 2, 20

print("=" * 76)
print("L1a  Is f_B log-CONCAVE in k?   f(k)^2 >= f(k-1)f(k+1)")
print("=" * 76)
bad = tot = 0
first = None
for p in allparts(NLO, 16):
    for k in range(2, KMAX):
        tot += 1
        lhs = f_B(p, k) ** 2
        rhs = f_B(p, k - 1) * f_B(p, k + 1)
        if lhs < rhs:
            bad += 1
            if first is None:
                first = (p, k, lhs, rhs)
print(f"  probes {tot:,}   failures {bad:,}")
if first:
    print(f"  FIRST FAILURE p={first[0]} k={first[1]}: {first[2]} < {first[3]}")
else:
    print("  f_B is log-concave everywhere tested. This is the mirror of f_E.")

print()
print("=" * 76)
print("L1b  Is g_p = f_E/f_B log-CONVEX in k?   g(k)^2 <= g(k-1)g(k+1)")
print("=" * 76)
bad = tot = 0
first = None
for p in allparts(NLO, 16):
    for k in range(2, KMAX):
        tot += 1
        # g(k)^2 <= g(k-1)g(k+1)  <=>  fE(k)^2 fB(k-1)fB(k+1) <= fE(k-1)fE(k+1) fB(k)^2
        lhs = f_E(p, k) ** 2 * f_B(p, k - 1) * f_B(p, k + 1)
        rhs = f_E(p, k - 1) * f_E(p, k + 1) * f_B(p, k) ** 2
        if lhs > rhs:
            bad += 1
            if first is None:
                first = (p, k)
print(f"  probes {tot:,}   failures {bad:,}")
print(f"  FIRST FAILURE {first}" if first else "  L1 holds everywhere tested.")

print()
print("=" * 76)
print("L2  Is g_q(k) >= g_p(k) pointwise, for q one exchange above p?")
print("    equivalently: does D/f_E decrease under dominance?")
print("=" * 76)
bad = tot = 0
first = None
eq1 = 0
for p in allparts(NLO, NHI):
    for q in exchanges(p):
        for k in range(1, KMAX):
            tot += 1
            lhs = f_E(q, k) * f_B(p, k)
            rhs = f_E(p, k) * f_B(q, k)
            if lhs < rhs:
                bad += 1
                if first is None:
                    first = (p, q, k)
            elif lhs == rhs:
                eq1 += 1 if k == 1 else 0
print(f"  probes {tot:,}   failures {bad:,}   (equalities at k=1: {eq1:,})")
print(f"  FIRST FAILURE {first}" if first else "  L2 holds everywhere tested.")

print()
print("=" * 76)
print("CONCLUSION of the two-step architecture, checked directly on rho")
print("=" * 76)
bad = tot = 0
first = None
for p in allparts(NLO, NHI):
    rp_n, rp_d = sigma_E(p), sigma_blind(p)
    for q in exchanges(p):
        tot += 1
        rq_n, rq_d = sigma_E(q), sigma_blind(q)
        if rq_n * rp_d <= rp_n * rq_d:
            bad += 1
            if first is None:
                first = (p, q, Fraction(rp_n, rp_d), Fraction(rq_n, rq_d))
print(f"  exchanges {tot:,}   rho failed to strictly increase {bad:,}")
print(f"  FIRST FAILURE {first}" if first else "  rho strictly increases in every case.")
