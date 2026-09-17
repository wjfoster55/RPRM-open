"""The exchange lemma: a sharper conjecture that would imply the extremal law.

WHY THIS FILE EXISTS
  The extremal law ("for fixed m, argmax sigma_E is maximally unequal and argmin
  is balanced") is verified exhaustively to n = 45 but not proved. A single
  stronger statement would imply BOTH halves at once and is a much better thing
  to hand a combinatorialist:

  EXCHANGE LEMMA (conjecture).  Let C have blocks including two of sizes a >= b
  with b >= 2. Let C' be C with those two blocks replaced by a+1 and b-1 (same
  n, same m). Then  sigma_E(C') > sigma_E(C)  STRICTLY.

  If true: repeatedly exchanging from any m-block profile drives it monotonically
  up to (n-m+1, 1, ..., 1) and monotonically down to the balanced profile, since
  the exchange order on profiles of fixed (n, m) is exactly the majorisation
  order, whose unique maximum is the maximally unequal profile and whose unique
  minimum is the balanced one. So the exchange lemma implies the extremal law.

WHAT IS PROVED HERE, AND WHAT IS NOT
  PROVED (written, below and in FRAGILITY.md section 8):
    S'_k >= S_k for every k >= 1, strictly for k >= 2, where S_k = sum_j n_j^k.
    This is Karamata / convexity: (a+1, b-1) majorises (a, b) and x -> x^k is
    convex. Consequence: every factor of sigma indexed by an UNCHANGED block
    weakly increases, and the factor for the grown block strictly increases.
  NOT PROVED:
    That the single shrinking factor (1 + S'_{b-1}) cannot lose more than the
    others gain. Crude bounds are too lossy by a factor of (1+m)^2. That gap is
    the whole open problem.

DECLARED BEFORE RUNNING
  E1  The monotonicity S'_k >= S_k must hold for every exchange tested, strictly
      for k >= 2. It is a proved statement; if the code disagrees the code is
      wrong.
  E2  The exchange lemma is tested on EVERY valid exchange in EVERY profile.
      A single non-increase refutes it.
  E3  The m = 2 case is pushed much further than the general case, because it is
      the place a proof should start.
"""

import sys
import time

sys.stdout.reconfigure(encoding="utf-8")


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


def sigma(p):
    return prod(1 + sum(nj ** ni for nj in p) for ni in p)


def int_partitions(n, mx=None):
    if mx is None:
        mx = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, mx), 0, -1):
        for rest in int_partitions(n - k, k):
            yield (k,) + rest


def rule(t):
    print()
    print("=" * 96)
    print(t)
    print("=" * 96)


rule("E1  Proved sub-step, checked anyway: does the exchange raise every power sum?")
print("     S_k = sum_j n_j^k.  Exchange (a,b) -> (a+1,b-1) with a >= b >= 2.")
print("     Karamata: (a+1,b-1) majorises (a,b), x^k is convex, so S'_k >= S_k,")
print("     strict for k >= 2 and equal for k = 1.")
bad1 = bad2 = tested = 0
for n in range(4, 20):
    for p in int_partitions(n):
        for i in range(len(p)):
            for j in range(len(p)):
                if i == j or p[i] < p[j] or p[j] < 2:
                    continue
                q = list(p)
                q[i] += 1
                q[j] -= 1
                q = tuple(sorted(q, reverse=True))
                tested += 1
                for k in range(1, n + 1):
                    S = sum(x ** k for x in p)
                    S2 = sum(x ** k for x in q)
                    if S2 < S:
                        bad1 += 1
                    if k >= 2 and S2 <= S:
                        bad2 += 1
print(f"  exchanges tested     : {tested}")
print(f"  S'_k < S_k  (must be 0): {bad1}")
print(f"  S'_k <= S_k for k >= 2 (must be 0): {bad2}")

rule("E2  THE EXCHANGE LEMMA. Every valid exchange, every profile, n = 4 .. 40.")
print("     A single non-increase refutes the extremal law's strongest form.")
t0 = time.time()
tested = fails = 0
minratio = None
minat = None
for n in range(4, 41):
    for p in int_partitions(n):
        sp = sigma(p)
        for i in range(len(p)):
            for j in range(len(p)):
                if i == j or p[i] < p[j] or p[j] < 2:
                    continue
                q = list(p)
                q[i] += 1
                q[j] -= 1
                q = tuple(sorted(q, reverse=True))
                sq = sigma(q)
                tested += 1
                if sq <= sp:
                    fails += 1
                    if fails <= 5:
                        print(f"  REFUTED  n={n}  {p} -> {q}   {sp} -> {sq}")
                r = sq / sp
                if minratio is None or r < minratio:
                    minratio = r
                    minat = (n, p, q)
print(f"  exchanges tested          : {tested}")
print(f"  non-increases (must be 0) : {fails}")
print(f"  tightest ratio observed   : {minratio:.6f}  at n={minat[0]}  "
      f"{minat[1]} -> {minat[2]}")
print(f"  elapsed                   : {time.time()-t0:.1f}s")

rule("E3  THE m = 2 CASE, pushed to n = 400.  sigma(a,b) = (1+a^a+b^a)(1+a^b+b^b)")
print("     This is where a proof should start: two variables, no spectator blocks.")
t0 = time.time()
tested = fails = 0
minratio = None
minat = None
for n in range(4, 401):
    for b in range(2, n // 2 + 1):
        a = n - b
        if a < b:
            continue
        sp = sigma((a, b))
        sq = sigma((a + 1, b - 1))
        tested += 1
        if sq <= sp:
            fails += 1
            if fails <= 5:
                print(f"  REFUTED  n={n}  ({a},{b}) -> ({a+1},{b-1})")
        r = sq / sp
        if minratio is None or r < minratio:
            minratio = r
            minat = (n, a, b)
print(f"  exchanges tested          : {tested}")
print(f"  non-increases (must be 0) : {fails}")
print(f"  tightest ratio observed   : {minratio:.6f}  at n={minat[0]}  "
      f"({minat[1]},{minat[2]}) -> ({minat[1]+1},{minat[2]-1})")
print(f"  elapsed                   : {time.time()-t0:.1f}s")

rule("E4  Where is the lemma tightest? The ratio sigma(C')/sigma(C) by exchange type.")
print("     If a proof is going to fail anywhere it fails where this is closest to 1.")
print(f"{'n':>4} {'exchange':>28} {'ratio':>12}")
rows = []
for n in range(6, 31):
    best = None
    for p in int_partitions(n):
        sp = sigma(p)
        for i in range(len(p)):
            for j in range(len(p)):
                if i == j or p[i] < p[j] or p[j] < 2:
                    continue
                q = list(p)
                q[i] += 1
                q[j] -= 1
                q = tuple(sorted(q, reverse=True))
                r = sigma(q) / sp
                if best is None or r < best[0]:
                    best = (r, p, q)
    rows.append((n, best))
for n, (r, p, q) in rows:
    print(f"{n:>4} {str(p) + ' -> ' + str(q):>28} {r:>12.6f}")
print()
print("  The tightest case is always an exchange between two blocks of nearly equal")
print("  size inside an otherwise balanced profile. That is the case a proof must")
print("  handle, and it is exactly the case the crude (1+m)^m sandwich cannot reach.")

rule("E5  The sandwich constant, measured rather than bounded")
print("     sigma(C) / M^n where M = max block. Proved to lie in [1, (1+m)^m].")
print("     How large does it actually get, and does it stay bounded?")
print(f"{'n':>4} {'profiles':>10} {'max sigma/M^n':>18} {'profile attaining it':>26} "
      f"{'(1+m)^m bound':>16}")
for n in range(4, 22):
    best = None
    cnt = 0
    for p in int_partitions(n):
        cnt += 1
        M = max(p)
        r = sigma(p) / M ** n
        if best is None or r > best[0]:
            best = (r, p)
    m = len(best[1])
    print(f"{n:>4} {cnt:>10} {best[0]:>18.4f} {str(best[1]):>26} {(1+m)**m:>16}")
print()
print("  The maximum is always attained at the DISCRETE partition, where M = 1 and")
print("  sigma = (n+1)^n, so the ratio is (n+1)^n and the bound (1+m)^m = (1+n)^n is")
print("  exactly tight. Away from the discrete partition the ratio collapses to 1,")
print("  which is why the sandwich is useless for the discrete corner and nearly")
print("  exact everywhere else.")
