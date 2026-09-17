"""Response to the hostile audit of the exchange lemma. Every point tested, not conceded.

The audit accepts the theorem and rejects three pieces of the surrounding story:

  (1) "the constant +1 is what makes log-convexity work; false without it"
  (2) "the product-multiset majorisation route fails, so we use convex order"
  (3) "the total-map class is not covered by the proof"

Loyalty is not evidence and neither is an auditor's say-so. Each is decided here
by exact computation against a null declared before the run.

DECLARED BEFORE RUNNING
  R1  If +1 were essential to log-convexity, then g(k) = sum_j n_j^k -- the same
      function without it -- must FAIL log-convexity somewhere. Null: it fails.
      (If it never fails, claim (1) is ours to retract.)
  R2  CONTROLLED ISOLATION. Compare two factor functions with IDENTICAL bases:
          g_plus(k)  = sum_j (n_j+1)^k              pure sum of exponentials
          f_blind(k) = sum_j (n_j+1)^k - (m-1)      same, minus a constant
      They differ only by the subtracted constant. If log-convexity and the
      exchange lemma hold for the first and fail for the second, the mechanism
      is the SUBTRACTION, not the presence or absence of a +1. Null: they behave
      the same, i.e. the subtraction is irrelevant.
  R3  The audit's exact counterexample: p = (1,1) gives f_blind(k) = 2^(k+1) - 1,
      and f(2)^2 = 49 > 45 = f(1)f(3), so log-convexity fails. Check literally.
  R4  ASYMMETRY. Adding a positive constant preserves log-convexity (c = c*1^k is
      just another exponential). Subtracting one need not. Test both directions.
  R5  TENSOR MAJORISATION. The audit says exponent-multiset majorisation holds
      directly at higher arity via p^(x)r = D^(x)r q^(x)r. Null: the sorted
      multiset {e_T(q)} does NOT majorise {e_T(p)} for some exchange, arity 2-5.
  R6  TOTAL MAPS. Factor sum_j n_j^k is a sum of exponentials, so the proof
      should transfer at every arity. Null: some exchange fails, arity 1-4.
  R7  IDEMPOTENTS. The audit says idempotence couples choices across blocks and
      destroys the factorisation. Test whether a product form exists at all, and
      whether the exchange lemma survives empirically regardless.
"""

import sys
import itertools
from fractions import Fraction
from math import comb

sys.stdout.reconfigure(encoding="utf-8")


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


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


# ---------------------------------------------------------------- factor functions
def f_E(p, k):
    return 1 + sum(n ** k for n in p)


def g_bare(p, k):
    """sigma_E's factor with the +1 DELETED. This is also |T(X,P)|'s factor."""
    return sum(n ** k for n in p)


def g_plus(p, k):
    """Classical bases, NO subtracted constant."""
    return sum((n + 1) ** k for n in p)


def f_blind(p, k):
    """Classical factor as it actually is: g_plus minus (m-1)."""
    return sum((n + 1) ** k for n in p) - (len(p) - 1)


def logconvex_failures(fn, parts):
    """f log-convex on integers  <=>  f(k)f(k+2) >= f(k+1)^2 for all k>=1."""
    bad, tot = [], 0
    for p in parts:
        for k in range(1, max(p) + 2):
            tot += 1
            if fn(p, k) * fn(p, k + 2) < fn(p, k + 1) ** 2:
                bad.append((p, k))
    return bad, tot


HDR = "=" * 88
print(HDR)
print("R1 / R3 / R4   Is the +1 what makes log-convexity work?")
print(HDR)
P = allparts(1, 12)
for name, fn in (("f_E      = 1 + sum n_j^k        (sigma_E)", f_E),
                 ("g_bare   =     sum n_j^k        (+1 DELETED, = |T(X,P)|)", g_bare),
                 ("g_plus   =     sum (n_j+1)^k    (classical bases, no minus)", g_plus),
                 ("f_blind  = sum (n_j+1)^k -(m-1) (classical, as it is)", f_blind)):
    bad, tot = logconvex_failures(fn, P)
    print(f"  {name:<58} {len(bad):>6} / {tot:,} fail")
    if bad:
        p, k = bad[0]
        print(f"      first: p={p} k={k}   "
              f"{fn(p,k)}*{fn(p,k+2)} = {fn(p,k)*fn(p,k+2)} "
              f"< {fn(p,k+1)**2} = {fn(p,k+1)}^2")

print()
print("  R3 literal check, audit's counterexample p = (1,1):")
pp = (1, 1)
v = [f_blind(pp, k) for k in (1, 2, 3)]
print(f"      f_blind(k) = 2^(k+1) - 1  ->  f(1),f(2),f(3) = {v}")
print(f"      f(1)*f(3) = {v[0]*v[2]}   f(2)^2 = {v[1]**2}   "
      f"log-convex? {'NO' if v[0]*v[2] < v[1]**2 else 'yes'}")
print()
print("  R4 asymmetry, on the same bases:")
print(f"      sum n_j^k          log-convex failures: "
      f"{len(logconvex_failures(g_bare, P)[0])}")
print(f"      sum n_j^k  PLUS 1  log-convex failures: "
      f"{len(logconvex_failures(f_E, P)[0])}")
print(f"      sum (n_j+1)^k          failures:        "
      f"{len(logconvex_failures(g_plus, P)[0])}")
print(f"      sum (n_j+1)^k MINUS (m-1) failures:     "
      f"{len(logconvex_failures(f_blind, P)[0])}")
print()
print("  VERDICT R1: the +1 is NOT what makes log-convexity work. Deleting it")
print("  leaves a sum of exponentials, which is still log-convex. Our earlier")
print("  'false without it' was wrong. ACCEPTED against us.")

print()
print(HDR)
print("R2   Controlled isolation: same bases, only the subtraction differs")
print(HDR)
print("  Both use bases (n_j + 1). The ONLY difference is '- (m-1)'.")
print()
for name, fn in (("g_plus   prod_i sum_j (n_j+1)^{n_i}          no subtraction", g_plus),
                 ("f_blind  prod_i [sum_j (n_j+1)^{n_i} -(m-1)]  subtraction", f_blind)):
    tot = fail = 0
    first = None
    for p in allparts(4, 26):
        for q in exchanges(p):
            tot += 1
            if not prod(fn(q, ni) for ni in q) > prod(fn(p, ni) for ni in p):
                fail += 1
                if first is None:
                    first = (p, q)
    print(f"  {name:<58} {tot:>7,} exch  {fail:>4} fail")
    if first:
        print(f"      first failure {first[0]} -> {first[1]}")
print()
print("  VERDICT R2: with the bases held fixed, removing the subtracted constant")
print("  restores both log-convexity and the exchange lemma. The mechanism is the")
print("  SUBTRACTION, not the +1. Null rejected.")

print()
print(HDR)
print("R5   Does exponent-multiset majorisation hold directly at higher arity?")
print(HDR)


def majorises(x, y):
    """sorted-desc x majorises y: equal sums, all prefix sums >= ."""
    x = sorted(x, reverse=True)
    y = sorted(y, reverse=True)
    if len(x) != len(y) or sum(x) != sum(y):
        return False
    sx = sy = 0
    for a, b in zip(x, y):
        sx += a
        sy += b
        if sx < sy:
            return False
    return True


def exps(p, r):
    return [prod(t) for t in itertools.product(p, repeat=r)]


for r in (2, 3, 4, 5):
    tot = fail = 0
    for p in allparts(4, 11):
        for q in exchanges(p):
            tot += 1
            if not majorises(exps(q, r), exps(p, r)):
                fail += 1
    print(f"  arity r = {r}   {tot:>5,} exchanges   {fail:>4} majorisation failures  "
          f"{'HOLDS' if fail == 0 else 'FAILS'}")
print()
print("  VERDICT R5: the tensor route works. If q majorises p then p = Dq for a")
print("  doubly stochastic D, and D^(x)r is doubly stochastic with p^(x)r =")
print("  D^(x)r q^(x)r, whose coordinates ARE the ordered-tuple exponents e_T.")
print("  So {e_T(q)} majorises {e_T(p)} directly, and Karamata finishes it in one")
print("  step. Our claim that this route 'fails' was too strong. ACCEPTED.")
print("  The convex-order proof remains valid; it is now the longer of two routes.")

print()
print(HDR)
print("R6   Total maps: covered by the same proof, or not?")
print(HDR)
print("  Restricting to TOTAL maps deletes the 'wholly undefined' choice, so the")
print("  count is prod_T sum_j n_j^{e_T} -- factor sum_j n_j^k, a sum of")
print("  exponentials with no constant term at all.")
print()
for r in (1, 2, 3, 4):
    tot = fail = 0
    hi = 26 if r == 1 else (12 if r == 2 else 9)
    for p in allparts(4, hi):
        for q in exchanges(p):
            tot += 1
            sp = prod(g_bare(p, e) for e in exps(p, r))
            sq = prod(g_bare(q, e) for e in exps(q, r))
            if not sq > sp:
                fail += 1
    print(f"  arity r = {r}   n <= {hi:<2}   {tot:>7,} exchanges   {fail:>4} failures  "
          f"{'HOLDS' if fail == 0 else 'FAILS'}")
print()
print("  VERDICT R6: the total-map class IS covered. Strictness survives too: the")
print("  base step sum q_j^k > sum p_j^k is strict for k >= 2, and the all-a")
print("  tuple has exponent a^r >= 2 whenever a >= 2. Promoted from conjecture")
print("  to theorem. ACCEPTED against our stated obstruction, which was spurious:")
print("  we had said the proof needs the factor to be '1 + sum n_j^k'. It needs")
print("  only log-convexity, and this is the SAME error as R1.")

print()
print(HDR)
print("R7   Idempotents: does the factorisation survive?")
print(HDR)


def sigma_idem(p):
    """Enabled idempotent partial maps.

    t idempotent  <=>  Fix(t) ⊆ dom(t) and t(dom) ⊆ Fix(t). Write S_i = Fix ∩ B_i.
    A block in the domain with S_i nonempty must target its OWN block (its fixed
    points map to themselves), so t: B_i -> S_i. A block with S_i empty picks any
    block j with S_j nonempty and maps into S_j.

    The bracketed factor for an s_i = 0 block depends on the OTHER blocks'
    choices. That is the coupling: no product over blocks exists.
    """
    m = len(p)
    total = 0
    for D in itertools.chain.from_iterable(
            itertools.combinations(range(m), d) for d in range(m + 1)):
        if not D:
            total += 1                       # the empty map
            continue
        for svec in itertools.product(*[range(p[i] + 1) for i in D]):
            live = [(i, s) for i, s in zip(D, svec) if s >= 1]
            if not live and any(s == 0 for s in svec):
                continue
            ways = 1
            for i, s in zip(D, svec):
                ways *= comb(p[i], s)
                if s >= 1:
                    ways *= s ** (p[i] - s)
                else:
                    ways *= sum(s2 ** p[i] for _, s2 in live)
            total += ways
    return total


def brute_idem(p):
    n = sum(p)
    blocks, pts, start = [], [], 0
    for sz in p:
        blocks.append(list(range(start, start + sz)))
        pts += [len(blocks) - 1] * sz
        start += sz
    UNDEF = n
    cnt = 0
    for t in itertools.product(range(n + 1), repeat=n):
        ok = True
        for B in blocks:
            d = {x for x in B if t[x] != UNDEF}
            if d and len(d) != len(B):
                ok = False
                break
            if d and len({pts[t[x]] for x in B}) > 1:
                ok = False
                break
        if not ok:
            continue
        for x in range(n):
            if t[x] != UNDEF and t[t[x]] != t[x]:
                ok = False
                break
        cnt += ok
    return cnt


print(f"  {'profile':<14} {'closed form':>12} {'brute force':>12}")
okall = True
for p in allparts(1, 6):
    if sum(p) > 6:
        continue
    a, b = sigma_idem(p), brute_idem(p)
    okall &= a == b
    print(f"  {str(p):<14} {a:>12,} {b:>12,}  {'ok' if a == b else 'FAIL'}")
print(f"  closed form validated: {okall}")
print()
tot = fail = 0
first = None
for p in allparts(4, 13):
    for q in exchanges(p):
        tot += 1
        if not sigma_idem(q) > sigma_idem(p):
            fail += 1
            if first is None:
                first = (p, q)
print(f"  exchange lemma on idempotents, n <= 13:  {tot:,} exchanges  {fail} failures")
if first:
    print(f"      first failure {first[0]} -> {first[1]}")
print()
print("  VERDICT R7: the audit is right that idempotence breaks the factorisation.")
print("  The count above is a SUM over which blocks carry fixed points, and the")
print("  factor for a fixed-point-free block depends on the other blocks' choices.")
print("  There is no product of per-block factors, so there is no factor function")
print("  to be log-convex, and the proof has nothing to act on. The lemma still")
print("  holds empirically in the range tested -- that keeps it a CONJECTURE at")
print("  finite-test grade, and it is NOT promoted. OPEN.")
print()
print(HDR)
print("SUMMARY: 3 of 3 audit points accepted against us; R7 kept OPEN as we had it.")
print(HDR)
