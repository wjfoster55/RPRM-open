"""Machine check of a written proof of the exchange lemma (arity 1).

THE PROOF BEING CHECKED

Write a profile as a multiset p = (n_1, ..., n_m) of positive block sizes, and

    S_k(p) = sum_j n_j^k ,      f_p(k) = 1 + S_k(p) ,
    sigma_E(p) = prod_i f_p(n_i) .

Let p have two blocks a >= b >= 2, other blocks (spectators) c_1..c_{m-2}, and
let q be p with those two blocks replaced by a+1 and b-1. Write f = f_q, g = f_p.

  STEP 1 (base majorisation).  For every k >= 1,  S_k(q) >= S_k(p), strict for
  k >= 2.  Because (a+1, b-1) majorises (a, b) and x -> x^k is convex on x > 0,
  strictly so for k >= 2.  Hence f(k) >= g(k), strict for k >= 2.

  STEP 2 (exponent log-convexity).  f(k) = e^{k*0} + sum_j e^{k ln q_j} is a sum
  of log-convex functions of k, hence log-convex.  With h = log f convex and
  a >= b, the increment h(a+1) - h(a) is over an interval lying weakly right of
  [b-1, b], so h(a+1) + h(b-1) >= h(a) + h(b), i.e.

        f(a+1) f(b-1) >= f(a) f(b).

  STEP 3 (combine).
        sigma_E(q) = (prod_c f(c)) f(a+1) f(b-1)
                  >= (prod_c f(c)) f(a)   f(b)       [Step 2]
                  >= (prod_c g(c)) g(a)   g(b)       [Step 1, all factors > 0]
                   = sigma_E(p),
  and the last inequality is STRICT because a >= 2 forces f(a) > g(a).

  Therefore sigma_E(q) > sigma_E(p).  QED

WHAT THIS SCRIPT DOES
  It does not prove anything.  It checks each step as a separate numerical
  assertion on a large family of profiles, so that a wrong step shows up as a
  failure rather than as a plausible-looking paragraph.  Every quantity is an
  exact Python integer or Fraction.

DECLARED BEFORE RUNNING
  P1  Step 1 must hold with the stated strictness. A single failure kills it.
  P2  Step 2 must hold. This is the step that does the real work -- it is the
      factor that the earlier crude sandwich bound could not control.
  P3  The conclusion must hold, and must agree with direct computation of
      sigma_E on both profiles.
  P4  NULL CONTROL. Step 2 relies only on log-convexity, so it must hold for
      the *old* profile too: g(a+1) g(b-1) >= g(a) g(b). If that failed, the
      log-convexity claim would be false and Step 2 would be an accident.
  P5  HOSTILE. The large-spectator nearly-balanced family, where the direct
      ratio tends to 1 and where the crude bound was lossy by (1+m)^2, must
      still satisfy Step 2 with room to spare.
"""

import sys
import itertools
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")


_S_CACHE = {}


def S(p, k):
    key = (p, k)
    v = _S_CACHE.get(key)
    if v is None:
        v = sum(n ** k for n in p)
        _S_CACHE[key] = v
    return v


def f(p, k):
    return 1 + S(p, k)


def sigma(p):
    return prod(f(p, n) for n in p)


def prod(xs):
    v = 1
    for x in xs:
        v *= x
    return v


def exchanges(p):
    """Every (a, b) pair with a >= b >= 2, and the resulting profile."""
    p = tuple(sorted(p, reverse=True))
    seen = set()
    for i, j in itertools.permutations(range(len(p)), 2):
        a, b = p[i], p[j]
        if b < 2 or a < b:
            continue
        rest = tuple(sorted((p[t] for t in range(len(p)) if t not in (i, j)),
                            reverse=True))
        q = tuple(sorted(rest + (a + 1, b - 1), reverse=True))
        key = (a, b, rest)
        if key in seen:
            continue
        seen.add(key)
        yield a, b, rest, q


def partitions(n, m, top=None):
    """Partitions of n into exactly m positive parts, weakly decreasing."""
    if top is None:
        top = n
    if m == 1:
        if 1 <= n <= top:
            yield (n,)
        return
    for first in range(min(top, n - m + 1), 0, -1):
        for rest in partitions(n - first, m - 1, first):
            yield (first,) + rest


def check(profiles, label):
    stats = dict(cases=0, s1=0, s1strict=0, s2=0, s3=0, null=0, agree=0)
    fails = []
    for p in profiles:
        for a, b, rest, q in exchanges(p):
            stats["cases"] += 1

            # P1 -- base majorisation, every exponent that actually gets used
            ok1 = ok1s = True
            for k in set(list(p) + list(q) + [a, b, a + 1, b - 1]):
                if S(q, k) < S(p, k):
                    ok1 = False
                if k >= 2 and not S(q, k) > S(p, k):
                    ok1s = False
            stats["s1"] += ok1
            stats["s1strict"] += ok1s

            # P2 -- exponent log-convexity on the NEW profile
            ok2 = f(q, a + 1) * f(q, b - 1) >= f(q, a) * f(q, b)
            stats["s2"] += ok2

            # P4 -- same claim on the OLD profile (null control on log-convexity)
            ok4 = f(p, a + 1) * f(p, b - 1) >= f(p, a) * f(p, b)
            stats["null"] += ok4

            # P3 -- the chained conclusion, and agreement with direct sigma
            lhs = prod(f(q, c) for c in rest) * f(q, a + 1) * f(q, b - 1)
            mid = prod(f(q, c) for c in rest) * f(q, a) * f(q, b)
            rhs = prod(f(p, c) for c in rest) * f(p, a) * f(p, b)
            ok3 = lhs >= mid >= rhs and lhs > rhs
            stats["s3"] += ok3
            ok5 = (lhs == sigma(q)) and (rhs == sigma(p)) and sigma(q) > sigma(p)
            stats["agree"] += ok5

            if not (ok1 and ok1s and ok2 and ok3 and ok4 and ok5):
                fails.append((p, a, b, q, ok1, ok1s, ok2, ok3, ok4, ok5))

    n = stats["cases"]
    print(f"  {label}")
    print(f"    exchanges checked                         {n:>12,}")
    for key, name in (("s1", "P1  S_k(q) >= S_k(p)"),
                      ("s1strict", "P1  strict for k >= 2"),
                      ("s2", "P2  f(a+1)f(b-1) >= f(a)f(b)"),
                      ("null", "P4  same on old profile (null)"),
                      ("s3", "P3  chain, strict overall"),
                      ("agree", "P3  chain == direct sigma_E")):
        v = stats[key]
        mark = "ok" if v == n else "FAIL"
        print(f"    {name:<41} {v:>12,}  {mark}")
    if fails:
        print(f"    FAILURES: {len(fails)}")
        for row in fails[:5]:
            print("     ", row)
    return len(fails)


NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 22

print("=" * 84)
print(f"P1-P4  Every step of the written proof, on all partitions, n = 4..{NMAX}")
print("=" * 84)
bad = 0
allp = [p for n in range(4, NMAX + 1) for m in range(1, n + 1)
        for p in partitions(n, m)]
bad += check(allp, f"all {len(allp):,} partitions of n = 4..{NMAX}")

print()
print("=" * 84)
print("P5  HOSTILE: large spectator, nearly balanced split -- the tight family")
print("=" * 84)
print("  The direct ratio here tends to 1, so Step 2 is where the proof has to")
print("  survive. Reporting Step 2's slack as a ratio; it must stay >= 1.")
print()
print("  ('direct' is only computed where K^K is a tractable integer; Step 2 is")
print("   cheap at every K because the spectator enters it only through S_k.)")
print()
print(f"{'K (spectator)':>15} {'j':>6} {'step-2 ratio':>22} {'direct sigma ratio':>22}")
worst2 = None
for K in (10, 120, 10 ** 4, 10 ** 9, 10 ** 30):
    for j in (3, 8, 40):
        p, q = (K, j, j), (K, j + 1, j - 1)
        a = b = j
        s2 = Fraction(f(q, a + 1) * f(q, b - 1), f(q, a) * f(q, b))
        if worst2 is None or s2 < worst2:
            worst2 = s2
        if K <= 120:
            direct = Fraction(sigma(q), sigma(p))
            dtxt = f"{float(direct):>22.15f}"
            if direct <= 1:
                bad += 1
                dtxt += "  FAIL"
        else:
            dtxt = f"{'(K^K too large)':>22}"
        print(f"{K:>15} {j:>6} {float(s2):>22.15f} {dtxt}")
        if s2 < 1:
            bad += 1
            print("      FAIL on step 2")
print()
print(f"  worst Step-2 ratio in the hostile family: {float(worst2):.15f}  (>= 1 required)")
print("  Step 2 does not degrade as the spectator grows -- it does not even")
print("  depend on the spectator except through S_k, and the dependence pushes")
print("  the ratio toward 1 from above rather than through it. That is exactly")
print("  why this route beats the sandwich bound, which tried to control the")
print("  spectator product directly and lost a factor of (1+m)^2 doing it.")

print()
print("=" * 84)
print("P6  Does the same argument survive higher arity?  (not claimed proved)")
print("=" * 84)


def sigma_r(p, r):
    return prod(f(p, prod(t)) for t in itertools.product(p, repeat=r))


for r in (2, 3):
    cases = ok = 0
    for n in range(2, 17 if r == 2 else 12):
        for m in range(1, n + 1):
            for p in partitions(n, m):
                for a, b, rest, q in exchanges(p):
                    cases += 1
                    ok += sigma_r(q, r) > sigma_r(p, r)
    mark = "ok" if ok == cases else "FAIL"
    if ok != cases:
        bad += 1
    print(f"  arity {r}: {ok:,} / {cases:,} exchanges strictly increase  {mark}")
print()
print("  Arity 1 is proved above. Arity 2 and 3 are checked only. The same route")
print("  should work -- the exponent multiset {prod of q_i} majorises {prod of")
print("  p_i} termwise by the same convexity -- but that majorisation is not")
print("  written out here, so higher arity stays OPEN.")

print()
print("=" * 84)
print("TOTAL FAILURES:", bad)
print("=" * 84)
