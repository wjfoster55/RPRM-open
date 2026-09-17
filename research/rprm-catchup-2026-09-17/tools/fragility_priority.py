"""Priority separation: the enabledness condition is what the literature omits.

PRIOR ART LOCATED (2026-09-17 search, recorded as evidence, not as a completeness proof)

  T(X,P) = { f : X -> X total | for every block C_i there is a block C_j with
             C_i f subseteq C_j }.
  Introduced by H. Pei. Cardinality for finite X and ARBITRARY partition P
  computed in arXiv:2006.04242, "On certain Semigroups of Transformations that
  preserve a partition".

  The PARTIAL analogue for a UNIFORM partition (m blocks of size n) is studied in
  arXiv:1210.4775, "Partial transformation monoids preserving a uniform
  partition" (Fernandes and Quinteiro). Its published order is

        |PT preserving P| = ( m (n+1)^n - m + 1 )^m .

WHAT THE LITERATURE CONDITION IS, AND WHAT IT IS NOT

  The literature condition is SUCCESSOR AGREEMENT ONLY: wherever f is defined on
  a block, the images stay inside one block. It places NO condition on the
  DOMAIN. A map may be defined on part of a block and undefined on the rest.

  RPRM's O05 adds ENABLEDNESS AGREEMENT: x ~ y implies x in dom f iff y in dom f.
  A block is wholly enabled or wholly disabled. That is a strictly stronger
  condition, so it cuts out a submonoid.

  So the two counts are

    sigma_blind(C) = prod_i ( 1 + sum_j [ (n_j + 1)^{n_i} - 1 ] )      literature
    sigma_E(C)     = prod_i ( 1 + sum_j   n_j^{n_i}            )      RPRM O05

  and the ENABLEDNESS PRICE is the exact rational rho(C) = sigma_E / sigma_blind:
  the fraction of literature-admissible reductions that RPRM rejects is 1 - rho.

DECLARED BEFORE RUNNING
  P1  sigma_blind on a uniform profile (n repeated m times) must reproduce the
      published closed form (m(n+1)^n - m + 1)^m exactly. If it does not, this
      derivation is wrong and nothing below stands.
  P2  Both counts must match exhaustive brute force over every partial map.
  P3  sigma_E <= sigma_blind always, with equality iff every block is a singleton.
"""

import sys
from fractions import Fraction
from itertools import product

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


def sigma_E(p):
    return prod(1 + sum(nj ** ni for nj in p) for ni in p)


def sigma_blind(p):
    return prod(1 + sum((nj + 1) ** ni - 1 for nj in p) for ni in p)


def labels(p):
    out = []
    for b, sz in enumerate(p):
        out.extend([b] * sz)
    return tuple(out)


def brute(p, enforce_enabledness):
    n = sum(p)
    lbl = labels(p)
    cnt = 0
    for g in product(range(-1, n), repeat=n):
        ok = True
        for x in range(n):
            for y in range(x + 1, n):
                if lbl[x] != lbl[y]:
                    continue
                dx, dy = g[x] != UNDEF, g[y] != UNDEF
                if enforce_enabledness and dx != dy:
                    ok = False
                    break
                if dx and dy and lbl[g[x]] != lbl[g[y]]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            cnt += 1
    return cnt


def rule(t):
    print()
    print("=" * 100)
    print(t)
    print("=" * 100)


rule("P1  Does our sigma_blind reproduce the PUBLISHED uniform-partition order?")
print("     published:  ( m (n+1)^n - m + 1 )^m     for m blocks of size n")
print(f"{'m':>3} {'n':>3} {'|X|':>4} {'published':>26} {'our sigma_blind':>26} {'match':>7}")
allok = True
for m in range(1, 6):
    for n in range(1, 6):
        if m * n > 16:
            continue
        pub = (m * (n + 1) ** n - m + 1) ** m
        ours = sigma_blind((n,) * m)
        ok = pub == ours
        allok = allok and ok
        print(f"{m:>3} {n:>3} {m*n:>4} {pub:>26} {ours:>26} {'OK' if ok else 'MISMATCH':>7}")
print(f"  P1 verdict: {'HOLDS for every case tested' if allok else 'VIOLATED'}")

rule("P2  Both counts against exhaustive brute force over every partial map")
print(f"{'n':>3} {'profile':>18} {'sigma_E':>12} {'brute_E':>12} {'ok':>4} "
      f"{'sigma_blind':>14} {'brute_blind':>14} {'ok':>4}")
bad = 0
for n in range(1, 7):
    for p in int_partitions(n):
        se, sb = sigma_E(p), sigma_blind(p)
        be, bb = brute(p, True), brute(p, False)
        oke, okb = se == be, sb == bb
        bad += (0 if oke else 1) + (0 if okb else 1)
        if n <= 4:
            print(f"{n:>3} {str(p):>18} {se:>12} {be:>12} {'OK' if oke else 'BAD':>4} "
                  f"{sb:>14} {bb:>14} {'OK' if okb else 'BAD':>4}")
print(f"  ... n up to 6, every profile.  mismatches: {bad}")

rule("P3  THE ENABLEDNESS PRICE.  rho = sigma_E / sigma_blind, exact rational.")
print("     1 - rho is the exact fraction of literature-admissible (successor-only)")
print("     reductions that RPRM's enabledness condition rejects.")
print(f"{'n':>3} {'profile':>20} {'sigma_E':>16} {'sigma_blind':>20} {'rho':>12} "
      f"{'rejected':>10}")
viol = 0
for n in (3, 4, 6, 8):
    for p in int_partitions(n):
        se, sb = sigma_E(p), sigma_blind(p)
        if se > sb:
            viol += 1
        rho = Fraction(se, sb)
        eq = all(x == 1 for x in p)
        print(f"{n:>3} {str(p):>20} {se:>16} {sb:>20} {float(rho):>12.8f} "
              f"{float(1-rho):>10.6f}" + ("   <- discrete, rho must be 1" if eq else ""))
    print()
print(f"  P3 verdict: sigma_E <= sigma_blind violations: {viol}")

rule("THE HEADLINE COMPARISON: does the enabledness condition change the ANSWER,")
print("     not merely the count?  Extremal profile under each monoid, fixed (n, m).")
print(f"{'n':>3} {'m':>3} {'argmax E':>18} {'argmax blind':>18} {'same':>6} "
      f"{'argmin E':>18} {'argmin blind':>18} {'same':>6}")
da = db = cells = 0
diffs = []
for n in range(3, 25):
    for m in range(2, n):
        profs = [p for p in int_partitions(n) if len(p) == m]
        if len(profs) < 2:
            continue
        cells += 1
        aE = max((sigma_E(p), p) for p in profs)[1]
        aB = max((sigma_blind(p), p) for p in profs)[1]
        bE = min((sigma_E(p), p) for p in profs)[1]
        bB = min((sigma_blind(p), p) for p in profs)[1]
        if aE != aB:
            da += 1
            diffs.append(("max", n, m, aE, aB))
        if bE != bB:
            db += 1
            diffs.append(("min", n, m, bE, bB))
        if n <= 8:
            print(f"{n:>3} {m:>3} {str(aE):>18} {str(aB):>18} "
                  f"{'yes' if aE==aB else 'NO':>6} {str(bE):>18} {str(bB):>18} "
                  f"{'yes' if bE==bB else 'NO':>6}")
print(f"  ... n up to 24, {cells} cells.  argmax differs in {da} cells; "
      f"argmin differs in {db} cells.")
if diffs:
    print("  first disagreements:", diffs[:6])

rule("EXTREMAL LAW UNDER THE LITERATURE MONOID (sigma_blind), for the record")
print(f"{'n':>3} {'m':>3} {'argmax blind':>20} {'= unequal?':>11} "
      f"{'argmin blind':>20} {'= balanced?':>12}")
fa = fb = 0
for n in range(3, 25):
    for m in range(2, n):
        profs = [p for p in int_partitions(n) if len(p) == m]
        if len(profs) < 2:
            continue
        a = max((sigma_blind(p), p) for p in profs)[1]
        b = min((sigma_blind(p), p) for p in profs)[1]
        oka, okb = a == unequal(n, m), b == balanced(n, m)
        fa += 0 if oka else 1
        fb += 0 if okb else 1
        if n <= 7 or not (oka and okb):
            print(f"{n:>3} {m:>3} {str(a):>20} {'OK' if oka else 'FAIL':>11} "
                  f"{str(b):>20} {'OK' if okb else 'FAIL':>12}")
print(f"  ... n up to 24.  argmax failures: {fa}   argmin failures: {fb}")

rule("SUBSET-SUM STRUCTURE: which domain sizes can a surviving operation have?")
print("     Under O05 a block is wholly enabled or wholly disabled, so the domain")
print("     size of any surviving partial operation is a SUBSET SUM of the profile.")
print("     Under the literature condition every domain size 0..n is reachable.")
print(f"{'profile':>22} {'admissible |dom| under O05':>46} {'count':>6} {'of n+1':>7}")
for p in [(5, 1), (4, 2), (3, 3), (4, 1, 1), (3, 2, 1), (2, 2, 2),
          (6,), (1, 1, 1, 1, 1, 1), (7, 1), (4, 4)]:
    n = sum(p)
    sums = {0}
    for k in p:
        sums |= {s + k for s in sums}
    s = sorted(sums)
    print(f"{str(p):>22} {str(s):>46} {len(s):>6} {n+1:>7}")
print()
print("  This is the mechanism behind the arity-independent extremal law: a profile")
print("  with one large blob concentrates its surviving operations at a few large")
print("  domain sizes where the count is enormous, while a balanced profile spreads")
print("  thinly. It is also the reason the fixed-domain-size slice in the hostile")
print("  battery has exact zeros.")
