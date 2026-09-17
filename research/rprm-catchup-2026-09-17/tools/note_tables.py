"""Tables for the standalone note on extremal partition shapes for |T(X,P)|."""

import sys
import itertools
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


def T(p):
    return prod(sum(nj ** ni for nj in p) for ni in p)


def sigma_E(p):
    return prod(1 + sum(nj ** ni for nj in p) for ni in p)


def sigma_blind(p):
    return prod(1 + sum((nj + 1) ** ni - 1 for nj in p) for ni in p)


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


print("TABLE 1  all shapes of n = 8 into m = 3 blocks, dominance order descending")
print()
print(f"| shape | `\\|T(X,P)\\|` | `sigma_E` | `sigma_blind` |")
print("|---|---:|---:|---:|")
for p in parts(8, 3):
    print(f"| `{p}` | {T(p):,} | {sigma_E(p):,} | {sigma_blind(p):,} |")

print()
print("TABLE 2  extremal ratio max/min at fixed n, m")
print()
print("| n | m | argmax | argmin | ratio |")
print("|---:|---:|---|---|---:|")
for n, m in ((8, 3), (10, 4), (12, 4), (16, 8), (20, 10)):
    ps = list(parts(n, m))
    vs = [(T(p), p) for p in ps]
    hi = max(vs)
    lo = min(vs)
    print(f"| {n} | {m} | `{hi[1]}` | `{lo[1]}` | {hi[0]/lo[0]:.4g} |")

print()
print("TABLE 3  the classical partial-map count has no such law. First failure cell.")
print()
for n, m in ((11, 9),):
    ps = list(parts(n, m))
    for name, fn in (("T(X,P)", T), ("sigma_E", sigma_E), ("sigma_blind", sigma_blind)):
        vs = [(fn(p), p) for p in ps]
        print(f"  {name:<12} argmax {max(vs)[1]}   argmin {min(vs)[1]}")
    print()
    a, b = (3,) + (1,) * 8, (2, 2) + (1,) * 7
    print(f"  sigma_blind{a} = {sigma_blind(a):,}")
    print(f"  sigma_blind{b} = {sigma_blind(b):,}   <- larger, though less unequal")

print()
print("TABLE 4  higher arity, n = 6 into m = 3, r = 1,2")


def T_r(p, r):
    es = [prod(t) for t in itertools.product(p, repeat=r)]
    return prod(sum(nj ** e for nj in p) for e in es)


print()
print("| shape | r = 1 | r = 2 |")
print("|---|---:|---:|")
for p in parts(6, 3):
    print(f"| `{p}` | {T_r(p,1):,} | {T_r(p,2):,} |")
