"""rho on a published reduced model: the Ehrenfest lumping.

The Ehrenfest urn chain on the hypercube {0,1}^d is strongly lumpable by Hamming
weight; this is textbook (Kemeny-Snell) and predates everything here. The lumping
is a genuine published state-space reduction whose block shape is binomial and
therefore strongly non-uniform, which is exactly the regime where shape matters.

WHAT THIS COMPUTES. For the shape of that lumping, the fraction

    rho = sigma_E / sigma_blind

of successor-compatible operations that also satisfy the block-saturated domain
condition. Both counts are over the ambient space of operations compatible with
the partition, under the uniform prior.

WHAT THIS DOES NOT COMPUTE. Anything about the Ehrenfest dynamics. The Ehrenfest
chain is one operation; rho describes the space it sits in. Nothing here says the
model is fragile, robust, or otherwise. The published lumping is used only as a
source of a real non-uniform partition shape that nobody chose to make a point.
"""

import sys
from fractions import Fraction
from math import comb

sys.stdout.reconfigure(encoding="utf-8")


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


def sigma_E(p):
    return prod(1 + sum(nj ** ni for nj in p) for ni in p)


def sigma_blind(p):
    return prod(1 + sum((nj + 1) ** ni - 1 for nj in p) for ni in p)


def tau(p):
    return prod(sum(nj ** ni for nj in p) for ni in p)


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


def balanced(n, m):
    q, r = divmod(n, m)
    return tuple(sorted([q + 1] * r + [q] * (m - r), reverse=True))


print("=" * 78)
print("rho on the Ehrenfest lumping (Kemeny-Snell), by hypercube dimension d")
print("=" * 78)
print()
print("| d | states n | blocks m | shape (binomial) | rho = sigma_E/sigma_blind |")
print("|---:|---:|---:|---|---:|")
rows = []
for d in range(2, 7):
    n = 2 ** d
    m = d + 1
    p = tuple(sorted((comb(d, k) for k in range(m)), reverse=True))
    r = Fraction(sigma_E(p), sigma_blind(p))
    rows.append((d, n, m, p, r))
    shape = ",".join(str(x) for x in p)
    print(f"| {d} | {n} | {m} | ({shape}) | {float(r):.6g} |")

print()
print("Read: at d = 6, roughly %.4g%% of the successor-only operations on that"
      % (float(rows[-1][4]) * 100))
print("partition also satisfy the domain condition. The condition is not a mild")
print("extra requirement on this shape; it discards almost everything.")

print()
print("=" * 78)
print("Where the binomial shape sits, and how much shape is worth")
print("=" * 78)
print()
print("For each d, all shapes of n into m parts are enumerated and the published")
print("binomial shape is located among them by |T(X,P)|.")
print()
print("| d | n | m | #shapes | rank of binomial (1 = max) | tau(binom)/tau(min) | tau(max)/tau(min) |")
print("|---:|---:|---:|---:|---:|---:|---:|")
for d in (2, 3, 4):
    n, m = 2 ** d, d + 1
    p = tuple(sorted((comb(d, k) for k in range(m)), reverse=True))
    ps = list(parts(n, m))
    vals = sorted(((tau(q), q) for q in ps), reverse=True)
    rank = next(i for i, (v, q) in enumerate(vals, 1) if q == p)
    tmax, tmin = vals[0][0], vals[-1][0]
    tbin = tau(p)
    print(f"| {d} | {n} | {m} | {len(ps)} | {rank} | "
          f"{tbin/tmin:.4g} | {tmax/tmin:.4g} |")

print()
print("=" * 78)
print("The same d = 5 cell, three shapes, to show the theorem is not a small effect")
print("=" * 78)
print()
d = 5
n, m = 2 ** d, d + 1
binom = tuple(sorted((comb(d, k) for k in range(m)), reverse=True))
mx = (n - m + 1,) + (1,) * (m - 1)
mn = balanced(n, m)
print("| shape | provenance | `|T(X,P)|` | rho |")
print("|---|---|---:|---:|")
for q, name in ((mx, "dominance maximum"),
                (binom, "**the published Ehrenfest lumping**"),
                (mn, "dominance minimum")):
    r = Fraction(sigma_E(q), sigma_blind(q))
    print(f"| `{q}` | {name} | {tau(q):.6g} | {float(r):.4g} |")
print()
print("All three have the same 32 states and the same 6 blocks. Only the shape")
print("differs, and the order of the monoid differs across them by a factor of")
print(f"{tau(mx)/tau(mn):.4g}.")
