"""Fragility spectrum: hostile cases and prior sensitivity.

Runs the five declared hostile cases against the extremal conjecture recorded in
`fragility.py`. Integers and Fraction only.

CONJECTURE UNDER ATTACK
  For a finite carrier S with |S| = n and a partition C with m blocks of sizes
  (n_1..n_m), let sigma(C) count the deterministic PARTIAL operations that C
  survives under the O05 test (enabledness agreement + successor agreement).
  For fixed (n, m):
      argmax sigma = (n-m+1, 1, ..., 1)        maximally unequal
      argmin sigma = the balanced profile      sizes differ by at most 1

NULLS DECLARED BEFORE RUNNING
  N1  For every operation class below, the DISCRETE partition must survive every
      operation in that class: sigma(discrete) = |class|. A partition that
      distinguishes everything cannot be broken. If this fails the counter for
      that class is wrong and its verdict is void.
  N2  For the TOTAL operation class, the one-block partition must also survive
      everything: with no undefined transitions and one block, both O05
      conditions are vacuous. sigma_total((n,)) = n^n.
  N3  Brute-force counts and closed-form counts must agree wherever both are
      computed.

HOSTILE CASES
  H1  non-uniform priors: total-only, injective-partial, idempotent-total,
      fixed-domain-size partial
  H2  total operations only (drop partiality entirely)
  H3  arity 3
  H4  larger n for the unrestricted arity-1 law
  H5  the degeneracy objection is answered structurally, not computationally:
      the law is stated at FIXED m, and Result 2 (non-monotonicity in m) shows
      the criterion is not degenerate. Re-verified here at n = 6..10.
"""

import sys
import time
from fractions import Fraction
from itertools import product, permutations

sys.stdout.reconfigure(encoding="utf-8")

UNDEF = -1


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


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


def unequal(n, m):
    return tuple([n - m + 1] + [1] * (m - 1))


# ----------------------------------------------------------------- closed forms

def sigma_partial(profile, arity=1):
    idx = range(len(profile))
    tot = 1
    for combo in product(idx, repeat=arity):
        size = prod(profile[i] for i in combo)
        tot *= 1 + sum(nl ** size for nl in profile)
    return tot


def sigma_total(profile, arity=1):
    """Same count but the operation must be total: the '1 +' (undefined) drops."""
    idx = range(len(profile))
    tot = 1
    for combo in product(idx, repeat=arity):
        size = prod(profile[i] for i in combo)
        tot *= sum(nl ** size for nl in profile)
    return tot


# ----------------------------------------------------------------- brute force

def labels_from_profile(profile):
    lbl = []
    for b, sz in enumerate(profile):
        lbl.extend([b] * sz)
    return tuple(lbl)


def survives(lbl, g, n):
    """g is a tuple of length n over {0..n-1, UNDEF}."""
    for x in range(n):
        for y in range(x + 1, n):
            if lbl[x] != lbl[y]:
                continue
            dx, dy = g[x] != UNDEF, g[y] != UNDEF
            if dx != dy:
                return False
            if dx and lbl[g[x]] != lbl[g[y]]:
                return False
    return True


def class_maps(n, kind):
    """Enumerate the operation class. Each map is a tuple of length n."""
    if kind == "partial":
        yield from product(range(-1, n), repeat=n)
    elif kind == "total":
        yield from product(range(n), repeat=n)
    elif kind == "injective-partial":
        # partial and injective on its domain
        for g in product(range(-1, n), repeat=n):
            img = [v for v in g if v != UNDEF]
            if len(img) == len(set(img)):
                yield g
    elif kind == "permutation":
        for p in permutations(range(n)):
            yield p
    elif kind == "idempotent-total":
        for g in product(range(n), repeat=n):
            if all(g[g[x]] == g[x] for x in range(n)):
                yield g
    else:
        raise ValueError(kind)


def brute_sigma(profile, kind):
    n = sum(profile)
    lbl = labels_from_profile(profile)
    tot = cnt = 0
    for g in class_maps(n, kind):
        tot += 1
        if survives(lbl, g, n):
            cnt += 1
    return cnt, tot


def brute_sigma_fixed_domain(profile, d):
    """Partial maps with EXACTLY d defined points."""
    n = sum(profile)
    lbl = labels_from_profile(profile)
    tot = cnt = 0
    for g in product(range(-1, n), repeat=n):
        if sum(1 for v in g if v != UNDEF) != d:
            continue
        tot += 1
        if survives(lbl, g, n):
            cnt += 1
    return cnt, tot


# ----------------------------------------------------------------- reports

def rule(t):
    print()
    print("=" * 98)
    print(t)
    print("=" * 98)


rule("N1/N2/N3  NULL CONTROLS, declared before the run")
print(f"{'n':>2} {'class':>20} {'|class|':>12} {'sigma(discrete)':>16} {'N1':>11} "
      f"{'sigma_total((n,))':>18} {'N2':>11}")
for n in range(1, 6):
    for kind in ("partial", "total", "injective-partial", "permutation", "idempotent-total"):
        disc = (1,) * n
        c, tot = brute_sigma(disc, kind)
        n1 = "HOLDS" if c == tot else "VIOLATED"
        if kind == "total":
            cb, _ = brute_sigma((n,), "total")
            n2v = f"{cb} vs {n**n}"
            n2 = "HOLDS" if cb == n ** n else "VIOLATED"
        else:
            n2v, n2 = "-", "-"
        print(f"{n:>2} {kind:>20} {tot:>12} {c:>16} {n1:>11} {n2v:>18} {n2:>11}")

rule("N3  closed form vs brute force, every profile, both operation models")
print(f"{'n':>2} {'profile':>16} {'sigma_partial':>14} {'brute':>10} {'ok':>4} "
      f"{'sigma_total':>12} {'brute':>10} {'ok':>4}")
bad = 0
for n in range(1, 7):
    for p in int_partitions(n):
        sp = sigma_partial(p)
        bp, _ = brute_sigma(p, "partial")
        st = sigma_total(p)
        bt, _ = brute_sigma(p, "total")
        okp = sp == bp
        okt = st == bt
        bad += (0 if okp else 1) + (0 if okt else 1)
        if n <= 4:
            print(f"{n:>2} {str(p):>16} {sp:>14} {bp:>10} {'OK' if okp else 'BAD':>4} "
                  f"{st:>12} {bt:>10} {'OK' if okt else 'BAD':>4}")
print(f"  ... n up to 6, every profile, both models.  mismatches: {bad}")

rule("H2  TOTAL OPERATIONS ONLY. Does the extremal law survive dropping partiality?")
print(f"{'n':>3} {'m':>3} {'argmax total':>20} {'pred':>6} {'argmin total':>20} {'pred':>6}")
h2max = h2min = 0
for n in range(3, 19):
    for m in range(2, n):
        profs = [p for p in int_partitions(n) if len(p) == m]
        if len(profs) < 2:
            continue
        a = max((sigma_total(p), p) for p in profs)[1]
        b = min((sigma_total(p), p) for p in profs)[1]
        oka = a == unequal(n, m)
        okb = b == balanced(n, m)
        h2max += 0 if oka else 1
        h2min += 0 if okb else 1
        if n <= 8 or not (oka and okb):
            print(f"{n:>3} {m:>3} {str(a):>20} {'OK' if oka else 'FAIL':>6} "
                  f"{str(b):>20} {'OK' if okb else 'FAIL':>6}")
print(f"  ... n up to 18, every m, every profile.  argmax failures: {h2max}   "
      f"argmin failures: {h2min}")

rule("H1  NON-UNIFORM PRIORS. Restricted operation classes, exhaustive brute force.")
print("     Does the extremal shape survive when the modeller's operation pool is")
print("     not 'all partial maps'?")
for kind in ("injective-partial", "permutation", "idempotent-total"):
    print()
    print(f"  --- class: {kind}")
    print(f"  {'n':>3} {'m':>3} {'argmax observed':>18} {'pred unequal':>14} {'ok':>5} "
          f"{'argmin observed':>18} {'pred balanced':>14} {'ok':>5}")
    fa = fb = 0
    for n in range(3, 8):
        for m in range(2, n):
            profs = [p for p in int_partitions(n) if len(p) == m]
            if len(profs) < 2:
                continue
            vals = [(brute_sigma(p, kind)[0], p) for p in profs]
            a = max(vals)[1]
            b = min(vals)[1]
            oka = a == unequal(n, m)
            okb = b == balanced(n, m)
            fa += 0 if oka else 1
            fb += 0 if okb else 1
            print(f"  {n:>3} {m:>3} {str(a):>18} {str(unequal(n,m)):>14} "
                  f"{'OK' if oka else 'FAIL':>5} {str(b):>18} {str(balanced(n,m)):>14} "
                  f"{'OK' if okb else 'FAIL':>5}")
    print(f"  class {kind}: argmax failures {fa}, argmin failures {fb}")

rule("H1b FIXED DOMAIN SIZE. Partial maps with exactly d defined points, n = 6.")
print("     This is the sharpest version of the prior objection: it removes the")
print("     'mostly-undefined maps dominate the count' explanation entirely.")
n = 6
print(f"{'d':>3} {'|class|':>10} " + " ".join(f"{str(p):>12}" for p in
      [(5, 1), (4, 2), (3, 3), (4, 1, 1), (3, 2, 1), (2, 2, 2)]))
for d in range(0, n + 1):
    row = []
    tot = None
    for p in [(5, 1), (4, 2), (3, 3), (4, 1, 1), (3, 2, 1), (2, 2, 2)]:
        c, t = brute_sigma_fixed_domain(p, d)
        tot = t
        row.append(c)
    print(f"{d:>3} {tot:>10} " + " ".join(f"{v:>12}" for v in row))
print("  read across each row: within a fixed domain size, is (5,1) > (4,2) > (3,3)")
print("  and (4,1,1) > (3,2,1) > (2,2,2)?  m=2 group then m=3 group.")

rule("H3  ARITY 3. Does the extremal law survive at arity 3?")
print(f"{'n':>3} {'m':>3} {'argmax a=3':>18} {'ok':>5} {'argmin a=3':>18} {'ok':>5}")
f3a = f3b = 0
for n in range(3, 11):
    for m in range(2, n):
        profs = [p for p in int_partitions(n) if len(p) == m]
        if len(profs) < 2:
            continue
        a = max((sigma_partial(p, 3), p) for p in profs)[1]
        b = min((sigma_partial(p, 3), p) for p in profs)[1]
        oka = a == unequal(n, m)
        okb = b == balanced(n, m)
        f3a += 0 if oka else 1
        f3b += 0 if okb else 1
        if n <= 6 or not (oka and okb):
            print(f"{n:>3} {m:>3} {str(a):>18} {'OK' if oka else 'FAIL':>5} "
                  f"{str(b):>18} {'OK' if okb else 'FAIL':>5}")
print(f"  ... n up to 10.  argmax failures: {f3a}   argmin failures: {f3b}")

rule("H4  EXTENDED EXHAUSTIVE SEARCH, arity 1, unrestricted partial maps")
t0 = time.time()
fa = fb = tested = 0
worst = []
for n in range(2, 46):
    for m in range(2, n):
        profs = [p for p in int_partitions(n) if len(p) == m]
        if len(profs) < 2:
            continue
        a = max((sigma_partial(p), p) for p in profs)[1]
        b = min((sigma_partial(p), p) for p in profs)[1]
        tested += 1
        if a != unequal(n, m):
            fa += 1
            worst.append(("max", n, m, a))
        if b != balanced(n, m):
            fb += 1
            worst.append(("min", n, m, b))
print(f"  (n, m) cells tested exhaustively : {tested}")
print(f"  n range                          : 2 .. 45")
print(f"  argmax counterexamples           : {fa}")
print(f"  argmin counterexamples           : {fb}")
print(f"  elapsed                          : {time.time()-t0:.1f}s")
if worst:
    print("  FIRST FAILURES:", worst[:5])

rule("H5  NON-DEGENERACY. Fragility is not monotone in block count m.")
print("     For each n, the most fragile profile and the least fragile nontrivial one.")
print(f"{'n':>3} {'most fragile profile':>22} {'F':>10} {'one-block (n,) F':>18} "
      f"{'is (n,) the worst?':>19}")
for n in range(4, 13):
    amb = (n + 1) ** n
    vals = [(Fraction(amb - sigma_partial(p), amb), p) for p in int_partitions(n)
            if len(p) < n]
    hi = max(vals)
    one = Fraction(amb - sigma_partial((n,)), amb)
    print(f"{n:>3} {str(hi[1]):>22} {float(hi[0]):>10.6f} {float(one):>18.6f} "
          f"{'yes' if hi[1] == (n,) else 'NO':>19}")

rule("ASYMPTOTIC SANDWICH (written argument, checked numerically here)")
print("  Let M = max block size. Every factor satisfies  M^{n_i} <= 1 + S_{n_i} <= (1+m) M^{n_i},")
print("  because S_k = sum_j n_j^k lies in [M^k, m*M^k] and M^k >= 1. Multiplying over")
print("  the m blocks and using sum n_i = n:")
print()
print("        M^n  <=  sigma_1(C)  <=  (1+m)^m * M^n")
print()
print("  So log sigma_1 = n log M + O(m log m). For fixed m the leading term is")
print("  monotone in M, argmax M is the unequal profile and argmin M is balanced.")
print("  Numerical check of the sandwich, every profile:")
print(f"{'n':>3} {'profiles':>9} {'min sigma/M^n':>15} {'max sigma/M^n':>15} "
      f"{'bound (1+m)^m worst':>20} {'sandwich holds':>15}")
for n in range(2, 16):
    lo, hi, bnd, ok = None, None, 0, True
    cnt = 0
    for p in int_partitions(n):
        M = max(p)
        m = len(p)
        r = Fraction(sigma_partial(p), M ** n)
        cnt += 1
        lo = r if lo is None or r < lo else lo
        hi = r if hi is None or r > hi else hi
        b = (1 + m) ** m
        bnd = max(bnd, b)
        if not (1 <= r <= b):
            ok = False
    print(f"{n:>3} {cnt:>9} {float(lo):>15.6f} {float(hi):>15.4f} {bnd:>20} "
          f"{'YES' if ok else 'NO':>15}")
