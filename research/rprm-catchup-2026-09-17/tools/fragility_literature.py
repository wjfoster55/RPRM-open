"""Independent check of the literature reduction, and what it does to the claims.

A literature pass reported that sigma_E is not a new count: it follows in one
line from a PUBLISHED formula. That is a downgrade of our priority position, so
it gets verified here rather than accepted.

THE PUBLISHED RESULT
  Sarkar & Singh, "On certain Semigroups of Transformations that preserve a
  partition", arXiv:2006.04242, Comm. Algebra 49(1) 2021, 331-342, Theorem 6.1.
  For TOTAL maps and an arbitrary finite partition, with m_i blocks of size n_i,

      |T(X,P)| = prod_i ( sum_j  m_j n_j^{n_i} )^{m_i}

  Regrouped over individual blocks rather than size classes this is

      |T(X,P)| = prod_i sum_j n_j^{n_i}          = sigma_E with each "1 +" removed.

THE REDUCTION CLAIMED
  Adjoin a sink * as a new singleton block, P' = P + {{*}} on X + {*}. The usual
  "undefined |-> *" bijection carries our Condition-B partial maps onto exactly
  the total maps in T(X+{*}, P') that fix *. The block {*} has n+1 possible
  images and one of them fixes *, so

      sigma_E(P) = |T(X + {*}, P')| / (n + 1).

  If true, our count is a corollary of a published theorem, and the honest
  description is "apparently unwritten but immediate", not "a new count".

DECLARED BEFORE RUNNING
  L1  The regrouped Sarkar-Singh formula must equal the size-class form. If not,
      we have misread the theorem.
  L2  The adjoin-a-sink identity must hold exactly, for every profile.
  L3  |T(X,P)| must equal a direct brute-force count of total partition-
      preserving maps, so that L2 is anchored to something computed from the
      definition rather than formula-to-formula.
  L4  CONSEQUENCE WORTH KNOWING. Our proof rests only on the factor function
      being a sum of exponentials. |T(X,P)|'s factor function is sum_j n_j^k --
      also a sum of exponentials, with no "1 +". So the SAME proof should give
      the extremal law for the PUBLISHED object. Test the exchange lemma on
      |T(X,P)| directly. If it holds, our theorem is a statement about a monoid
      that is already in the literature, which is a better position than a
      statement about an RPRM-internal count.
  L5  NULL. The same must FAIL for sigma_blind, whose factor function is not a
      sum of exponentials. Already known; repeated here as a control.
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
    return prod(1 + sum(nj ** ni for nj in p) for ni in p)


def T_blocks(p):
    """Sarkar-Singh, regrouped over individual blocks."""
    return prod(sum(nj ** ni for nj in p) for ni in p)


def T_sizeclass(p):
    """Sarkar-Singh Theorem 6.1 as printed, over size classes."""
    sizes = sorted(set(p))
    mult = {s: p.count(s) for s in sizes}
    return prod((sum(mult[s2] * s2 ** s1 for s2 in sizes)) ** mult[s1]
                for s1 in sizes)


def sigma_blind(p):
    return prod(1 + sum((nj + 1) ** ni - 1 for nj in p) for ni in p)


def brute_total(p):
    """Count total maps f with each block mapped into a single block."""
    n = sum(p)
    pts, blocks, start = [], [], 0
    for sz in p:
        blocks.append(list(range(start, start + sz)))
        pts += [len(blocks) - 1] * sz
        start += sz
    cnt = 0
    for f in itertools.product(range(n), repeat=n):
        ok = True
        for B in blocks:
            if len({pts[f[x]] for x in B}) > 1:
                ok = False
                break
        cnt += ok
    return cnt


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


def allparts(lo, hi):
    return [p for n in range(lo, hi + 1) for m in range(1, n + 1)
            for p in partitions(n, m)]


bad = 0
print("=" * 86)
print("L1  Sarkar-Singh Theorem 6.1: size-class form == per-block form")
print("=" * 86)
ps = allparts(1, 16)
fails = [p for p in ps if T_sizeclass(p) != T_blocks(p)]
print(f"  profiles checked {len(ps):,}   mismatches {len(fails)}  "
      f"{'ok' if not fails else 'FAIL'}")
bad += len(fails)

print()
print("=" * 86)
print("L3  |T(X,P)| formula == brute force over all total maps")
print("=" * 86)
print(f"  {'profile':<16} {'formula':>14} {'brute force':>14}  {'':4}")
for p in allparts(1, 6):
    if sum(p) > 6:
        continue
    f_, b_ = T_blocks(p), brute_total(p)
    ok = f_ == b_
    bad += not ok
    print(f"  {str(p):<16} {f_:>14,} {b_:>14,}  {'ok' if ok else 'FAIL'}")

print()
print("=" * 86)
print("L2  Adjoin-a-sink:  sigma_E(P) == |T(X+{*}, P+{{*}})| / (n+1)")
print("=" * 86)
fails = []
for p in allparts(1, 14):
    n = sum(p)
    lhs = sigma_E(p)
    big = T_blocks(tuple(sorted(p + (1,), reverse=True)))
    if big % (n + 1) != 0 or big // (n + 1) != lhs:
        fails.append(p)
print(f"  profiles checked {len(allparts(1,14)):,}   mismatches {len(fails)}  "
      f"{'ok' if not fails else 'FAIL'}")
bad += len(fails)
print()
print("  Worked example, profile (3,3), n = 6:")
p = (3, 3)
print(f"    sigma_E(3,3)                      = {sigma_E(p):,}")
print(f"    |T(X+*, (3,3,1))|                 = {T_blocks((3,3,1)):,}")
print(f"    divided by n+1 = 7                = {T_blocks((3,3,1))//7:,}")
print()
print("  VERDICT on L2: the reduction is real. sigma_E is a point stabiliser")
print("  inside a published, counted object. Our count is a corollary of")
print("  Sarkar-Singh Theorem 6.1, not a new enumeration.")

print()
print("=" * 86)
print("L4/L5  Does our proof also cover the PUBLISHED total-map monoid?")
print("=" * 86)
print("  The proof needs only that the factor function is a sum of exponentials.")
print("    sigma_E    factor  1 + sum_j n_j^k    sum of exponentials   -> works")
print("    |T(X,P)|   factor      sum_j n_j^k    sum of exponentials   -> should work")
print("    sigma_blind factor sum_j (n_j+1)^k - (m-1)   MINUS a constant -> should fail")
print()


def exchanges(p):
    p = tuple(sorted(p, reverse=True))
    seen = set()
    for i, j in itertools.permutations(range(len(p)), 2):
        a, b = p[i], p[j]
        if b < 2 or a < b:
            continue
        rest = tuple(sorted((p[t] for t in range(len(p)) if t not in (i, j)),
                            reverse=True))
        if (a, b, rest) in seen:
            continue
        seen.add((a, b, rest))
        yield tuple(sorted(rest + (a + 1, b - 1), reverse=True))


for name, fn, expect in (("|T(X,P)|  Sarkar-Singh, published", T_blocks, True),
                         ("sigma_E   enabledness enforced", sigma_E, True),
                         ("sigma_bl  successor only (null)", sigma_blind, False)):
    tot = fail = 0
    first = None
    for p in allparts(4, 26):
        for q in exchanges(p):
            tot += 1
            if not fn(q) > fn(p):
                fail += 1
                if first is None:
                    first = (p, q)
    holds = fail == 0
    mark = "ok" if holds == expect else "UNEXPECTED"
    if holds != expect:
        bad += 1
    print(f"  {name:<36} {tot:>8,} exchanges  {fail:>4} failures  {mark}")
    if first:
        print(f"      first failure: {first[0]} -> {first[1]}")

print()
print("  L4 reading. The exchange lemma, and therefore the extremal law, holds")
print("  for |T(X,P)| by the identical argument. That matters for positioning:")
print("  the theorem is a statement about a monoid that is already in the")
print("  literature and already counted, for which the literature pass found NO")
print("  published extremal result -- not a statement about an RPRM-only object.")
print()
print("  It remains a written proof, not a formal one, and 'no published extremal")
print("  result found' is the outcome of one serious search, not a priority claim.")
print()
print("=" * 86)
print("TOTAL FAILURES:", bad)
print("=" * 86)
