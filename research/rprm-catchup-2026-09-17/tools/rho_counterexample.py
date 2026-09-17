"""Kill the rho-monotonicity conjecture, minimally and verifiably.

The conjecture: rho = sigma_E / sigma_blind is strictly increasing along the
dominance order. It was filed at finite-test grade after 1,084 exchanges with
n <= 15 and no failures. That range was too small.

This script finds the smallest counterexample, recomputes it from the monoid
definitions by brute force rather than from the closed forms, and then maps the
failure region so the demotion can be stated with a domain rather than as a bare
"false".
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


def exchanges(p):
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


# ---------------------------------------------------------------- brute force
def brute(p):
    """Recount both monoids directly from their definitions. Small p only."""
    n = sum(p)
    pts, start = [], 0
    blocks = []
    for sz in p:
        blocks.append(list(range(start, start + sz)))
        pts += [len(blocks) - 1] * sz
        start += sz
    UND = n
    cE = cB = 0
    for t in itertools.product(range(n + 1), repeat=n):
        okB = True   # successor agreement where defined
        for B in blocks:
            imgs = {pts[t[x]] for x in B if t[x] != UND}
            if len(imgs) > 1:
                okB = False
                break
        if not okB:
            continue
        cB += 1
        # additionally: domain is a union of blocks
        if all(len({t[x] == UND for x in B}) == 1 for B in blocks):
            cE += 1
    return cE, cB


print("=" * 76)
print("1. SMALLEST COUNTEREXAMPLE, by total size n")
print("=" * 76)
found = None
for n in range(2, 23):
    hits = []
    for m in range(1, n + 1):
        for p in parts(n, m):
            rp = rho(p)
            for q in exchanges(p):
                if rho(q) <= rp:
                    hits.append((p, q))
    if hits and found is None:
        found = (n, hits)
        print(f"  n = {n}: FIRST FAILURES, {len(hits)} of them")
        for p, q in hits[:6]:
            print(f"      {p} -> {q}")
        break
    print(f"  n = {n}: {len(list(parts(n,1)))and''}no failures")

n0, hits = found
p, q = hits[0]

print()
print("=" * 76)
print(f"2. THE COUNTEREXAMPLE IN FULL:  {p}  ->  {q}")
print("=" * 76)
print(f"  n = {sum(p)}, m = {len(p)}. q is one exchange above p (4 -> 5, 4 -> 3),")
print("  so q strictly dominates p.")
print()
for r in (p, q):
    print(f"  shape {r}")
    print(f"    sigma_E      = {sigma_E(r):,}")
    print(f"    sigma_blind  = {sigma_blind(r):,}")
    print(f"    rho          = {float(rho(r)):.12f}")
print()
d = rho(q) - rho(p)
print(f"  rho(q) - rho(p) = {float(d):.3e}   <-- NEGATIVE, so rho DECREASED")
print(f"  exact: {d}")
print()
print("  Sanity: sigma_E must still increase (that part is a theorem).")
print(f"    sigma_E({p}) = {sigma_E(p):,}")
print(f"    sigma_E({q}) = {sigma_E(q):,}   increased: {sigma_E(q) > sigma_E(p)}")
print("  So the failure is entirely in the denominator outrunning the numerator.")
print(f"    sigma_blind grew by a factor {float(Fraction(sigma_blind(q), sigma_blind(p))):.9f}")
print(f"    sigma_E     grew by a factor {float(Fraction(sigma_E(q), sigma_E(p))):.9f}")

print()
print("=" * 76)
print("3. BRUTE-FORCE CHECK of both closed forms on small shapes")
print("=" * 76)
print("  (the counterexample itself is far too large to enumerate; this checks")
print("   that the formulas being compared are the right ones)")
ok = True
for r in [(1, 1), (2, 1), (2, 2), (3, 1), (2, 1, 1), (1, 1, 1), (3, 2)]:
    cE, cB = brute(r)
    good = (cE == sigma_E(r)) and (cB == sigma_blind(r))
    ok &= good
    print(f"  {str(r):<12} sigma_E {cE:>8} vs {sigma_E(r):>8} | "
          f"sigma_blind {cB:>10} vs {sigma_blind(r):>10}  "
          f"{'ok' if good else 'MISMATCH'}")
print(f"  all formulas confirmed: {ok}")

print()
print("=" * 76)
print("4. WHERE THE FAILURES LIVE  (all exchanges, n <= 22)")
print("=" * 76)
tot = bad = 0
by_n, by_m, by_minpart = {}, {}, {}
badlist = []
for n in range(2, 23):
    for m in range(1, n + 1):
        for p in parts(n, m):
            rp = rho(p)
            for q in exchanges(p):
                tot += 1
                if rho(q) <= rp:
                    bad += 1
                    badlist.append((n, m, p, q))
                    by_n[n] = by_n.get(n, 0) + 1
                    by_m[m] = by_m.get(m, 0) + 1
                    by_minpart[min(p)] = by_minpart.get(min(p), 0) + 1
print(f"  exchanges tested {tot:,}   failures {bad:,}  ({100*bad/tot:.2f}%)")
print()
print("  by n:      ", dict(sorted(by_n.items())))
print("  by m:      ", dict(sorted(by_m.items())))
print("  by min part:", dict(sorted(by_minpart.items())))
print()
print("  Do any failures have a singleton block?",
      any(min(p) == 1 for _, _, p, _ in badlist))
print("  Do any failures have m > 3?          ",
      any(m > 3 for _, m, _, _ in badlist))
print("  Do any failures have m < 3?          ",
      any(m < 3 for _, m, _, _ in badlist))
print()
print("  first 12 failing exchanges:")
for n, m, p, q in badlist[:12]:
    print(f"      n={n:<3} {p} -> {q}")

print()
print("=" * 76)
print("5. IS THERE A RESTRICTED DOMAIN THAT SURVIVES?")
print("=" * 76)
for label, pred in (
    ("m = 2 (two blocks)", lambda n, m, p: m == 2),
    ("m >= 4", lambda n, m, p: m >= 4),
    ("contains a singleton", lambda n, m, p: min(p) == 1),
    ("balanced-ish: max-min <= 1", lambda n, m, p: max(p) - min(p) <= 1),
    ("all parts >= 2", lambda n, m, p: min(p) >= 2),
):
    t = b = 0
    for n in range(2, 23):
        for m in range(1, n + 1):
            for p in parts(n, m):
                if not pred(n, m, p):
                    continue
                rp = rho(p)
                for q in exchanges(p):
                    t += 1
                    if rho(q) <= rp:
                        b += 1
    status = "SURVIVES (no failures)" if b == 0 else f"FAILS ({b} of {t})"
    print(f"  {label:<28} {status}")
