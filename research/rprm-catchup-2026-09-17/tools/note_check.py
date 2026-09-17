"""Verify the coverage-boundary counterexamples quoted in the standalone note.

Everything here is brute force from the definition, so the note's negative rows
do not rest on a formula that could itself be wrong.
"""

import sys
import itertools

sys.stdout.reconfigure(encoding="utf-8")


def setup(p):
    blocks, pts, start = [], [], 0
    for sz in p:
        blocks.append(list(range(start, start + sz)))
        pts += [len(blocks) - 1] * sz
        start += sz
    return blocks, pts


def preserving_perms(p):
    """Partition-preserving bijections X -> X."""
    n = sum(p)
    blocks, pts = setup(p)
    c = 0
    for f in itertools.permutations(range(n)):
        if all(len({pts[f[x]] for x in B}) == 1 for B in blocks):
            c += 1
    return c


def preserving_partial_fixed_domain(p, d):
    """Block-saturated domain of size exactly d, successor agreement."""
    n = sum(p)
    blocks, pts = setup(p)
    m = len(p)
    c = 0
    for r in range(m + 1):
        for D in itertools.combinations(range(m), r):
            if sum(p[i] for i in D) != d:
                continue
            ways = 1
            for i in D:
                ways *= sum(p[j] ** p[i] for j in range(m))
            c += ways
    return c


def brute_partial_fixed_domain(p, d):
    """Independent brute force of the same thing."""
    n = sum(p)
    blocks, pts = setup(p)
    UND = n
    c = 0
    for t in itertools.product(range(n + 1), repeat=n):
        dom = [x for x in range(n) if t[x] != UND]
        if len(dom) != d:
            continue
        ok = True
        for B in blocks:
            ins = [x for x in B if t[x] != UND]
            if ins and len(ins) != len(B):
                ok = False
                break
            if ins and len({pts[t[x]] for x in B}) > 1:
                ok = False
                break
        c += ok
    return c


print("=" * 74)
print("Bijective prior: does the extremal law survive?  n = 4, m = 2")
print("=" * 74)
for p in ((3, 1), (2, 2)):
    print(f"  shape {p}:  {preserving_perms(p)} partition-preserving permutations")
print("  (3,1) dominates (2,2), yet admits FEWER. Minimum half of the law fails.")

print()
print("=" * 74)
print("Fixed domain size: n = 6, m = 3, |dom| = 4")
print("=" * 74)
for p in ((4, 1, 1), (2, 2, 2)):
    a = preserving_partial_fixed_domain(p, 4)
    b = brute_partial_fixed_domain(p, 4)
    print(f"  shape {p}:  formula {a:>5}   brute force {b:>5}  "
          f"{'ok' if a == b else 'MISMATCH'}")
print("  (4,1,1) dominates (2,2,2), yet admits FEWER. Law fails within a slice.")

print()
print("=" * 74)
print("Nullary arity r = 0 is shape-independent")
print("=" * 74)
print("  one input tuple, image anywhere in X: tau_0 = n for every shape.")
print("  So r >= 1 is needed in Theorem 3.1. (Audit's catch.)")
