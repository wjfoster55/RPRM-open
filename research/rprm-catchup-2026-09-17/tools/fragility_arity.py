"""Machine check of the general-arity exchange proof.

WHAT §8d LEFT OPEN
  At arity r the factors of sigma_r are indexed by PRODUCTS of block sizes:
      sigma_r(p) = prod over ordered r-tuples T of  f_p( prod_{i in T} p_i ).
  Step 2 of the arity-1 proof needed the two evaluation points (a, b) and
  (a+1, b-1) to have equal sum. At higher arity there are m^r evaluation points
  and the needed statement is that, for every convex phi,

      sum_T phi(e'_T)  >=  sum_T phi(e_T)                             (*)

  where e_T and e'_T are the exponent products before and after the exchange.

THE ARGUMENT FOR (*), written before this script was run

  Read a uniformly random ordered r-tuple as r independent draws. Each coordinate
  independently picks a block. Condition on WHICH coordinates land in the two
  changed blocks (call that set U, |U| = s) and on the spectator choices for the
  rest, whose product is a constant P > 0. Every tuple is covered exactly once.

  Within one such cell the exponent is P times a product of s independent draws,
  each uniform on {a, b} before and on {a+1, b-1} after.

  1. {a+1, b-1} majorises {a, b} at equal mean, so the single-draw variable
     satisfies  X <=_cx X'  in the convex order.
  2. Convex order is closed under multiplication by an independent nonnegative
     factor: for y >= 0 the map x -> phi(xy) is convex, so conditioning on the
     other factor and integrating gives X Y <=_cx X' Y <=_cx X' Y'. Induction on
     s gives  prod X_i  <=_cx  prod X'_i.
  3. Scaling by the constant P >= 0 preserves convex order for the same reason.
  4. The inequality sum phi(.) >= sum phi(.) is additive over the cells, so
     summing over all U and all spectator assignments gives (*).

  Then, exactly as at arity 1:
      sigma_r(q) = prod_T f_q(e'_T) >= prod_T f_q(e_T) >= prod_T f_p(e_T)
                 = sigma_r(p),
  the first step by (*) with phi = log f_q (convex, since f_q is log-convex), the
  second by the base majorisation S_k(q) >= S_k(p), and strictly because a >= 2
  makes the factor at the all-a tuple, exponent a^r >= 2, strictly larger.

DECLARED BEFORE RUNNING
  A1  (*) must hold for a battery of convex test functions phi -- not just the
      one the proof uses. A convex phi that violates it refutes the argument.
  A2  NULL CONTROL. A strictly CONCAVE phi should REVERSE the inequality. If a
      concave phi also satisfies (*), the test is not sensitive to convexity and
      proves nothing.
  A3  The conclusion sigma_r(q) > sigma_r(p) must hold at every arity tested.
  A4  The cell decomposition must be exact: the multiset of exponents assembled
      cell by cell must equal the multiset assembled by brute-force enumeration
      of all m^r tuples. If it does not, step 4 is unsound.
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


def f(p, k):
    return 1 + sum(n ** k for n in p)


def exps(p, r):
    return sorted(prod(t) for t in itertools.product(p, repeat=r))


def sigma_r(p, r):
    return prod(f(p, e) for e in exps(p, r))


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
        yield a, b, rest, tuple(sorted(rest + (a + 1, b - 1), reverse=True))


# Convex test functions (A1) and concave controls (A2), all exact on integers.
CONVEX = [
    ("x^2", lambda x: Fraction(x) ** 2),
    ("x^3", lambda x: Fraction(x) ** 3),
    ("max(x-7,0)", lambda x: Fraction(max(x - 7, 0))),
    ("max(x-100,0)", lambda x: Fraction(max(x - 100, 0))),
    ("|x-20|", lambda x: Fraction(abs(x - 20))),
    ("2^x", lambda x: Fraction(2) ** x),
]
# Concave controls. A concave phi must give <= (the reverse of A1). Only a
# STRICTLY concave phi is required to give < ; min(x,12) is concave but linear
# below the kink, so on exchanges whose exponents all sit under it the two sides
# are equal. That is the correct behaviour, not a failure -- an earlier version
# of this script demanded strictness from it and flagged 143 phantom failures.
CONCAVE = [
    ("-x^2", lambda x: -Fraction(x) ** 2, True),
    ("min(x,12)", lambda x: Fraction(min(x, 12)), False),
]

NMAX = {2: 14, 3: 11, 4: 9}

print("=" * 88)
print("A1-A4  The general-arity exchange argument")
print("=" * 88)

bad = 0
for r in (2, 3, 4):
    cases = 0
    convex_ok = {name: 0 for name, _ in CONVEX}
    concave_rev = {name: 0 for name, _, _ in CONCAVE}
    concave_str = {name: 0 for name, _, _ in CONCAVE}
    concave_tot = {name: 0 for name, _, _ in CONCAVE}
    sigma_ok = 0
    decomp_ok = 0
    for n in range(2, NMAX[r] + 1):
        for m in range(1, n + 1):
            for p in partitions(n, m):
                for a, b, rest, q in exchanges(p):
                    cases += 1
                    eo, en = exps(p, r), exps(q, r)

                    # A4 -- cell decomposition reproduces the exponent multiset
                    cell = []
                    for U in itertools.product((0, 1), repeat=r):
                        s = sum(U)
                        for spect in itertools.product(rest, repeat=r - s):
                            P = prod(spect)
                            for pick in itertools.product((a + 1, b - 1),
                                                          repeat=s):
                                cell.append(P * prod(pick))
                    decomp_ok += sorted(cell) == en

                    for name, phi in CONVEX:
                        if sum(map(phi, en)) >= sum(map(phi, eo)):
                            convex_ok[name] += 1
                    for name, phi, _ in CONCAVE:
                        concave_tot[name] += 1
                        lo, hi = sum(map(phi, en)), sum(map(phi, eo))
                        concave_rev[name] += lo <= hi
                        concave_str[name] += lo < hi

                    sigma_ok += sigma_r(q, r) > sigma_r(p, r)

    print()
    print(f"  arity {r}   (all partitions of n = 2..{NMAX[r]})   "
          f"{cases:,} exchanges")
    print(f"    A4  cell decomposition == brute-force exponent multiset "
          f"{decomp_ok:>8,}/{cases:,}  "
          f"{'ok' if decomp_ok == cases else 'FAIL'}")
    if decomp_ok != cases:
        bad += 1
    print("    A1  sum phi(new) >= sum phi(old) for convex phi:")
    for name, _ in CONVEX:
        v = convex_ok[name]
        mark = "ok" if v == cases else "FAIL"
        if v != cases:
            bad += 1
        print(f"          phi = {name:<14} {v:>8,}/{cases:,}  {mark}")
    print("    A2  NULL: concave phi must reverse it (strictly, if strictly concave):")
    for name, _, strict in CONCAVE:
        v, s, t = concave_rev[name], concave_str[name], concave_tot[name]
        need = s if strict else v
        mark = "reversed, as required" if need == t else f"NOT reversed in {t-need}"
        if need != t:
            bad += 1
        extra = "" if strict else f"  (equality in {t-s}, phi is linear there)"
        print(f"          phi = {name:<14} {need:>8,}/{t:,}  {mark}{extra}")
    mark = "ok" if sigma_ok == cases else "FAIL"
    if sigma_ok != cases:
        bad += 1
    print(f"    A3  sigma_{r}(q) > sigma_{r}(p)                        "
          f"{sigma_ok:>8,}/{cases:,}  {mark}")

print()
print("=" * 88)
print("TOTAL FAILURES:", bad)
print("=" * 88)
if bad:
    print()
    print("  Failures present. Do not read the paragraph below as established.")
print()
print("  Reading. A1 holds for every convex test function tried, including ones")
print("  the proof never mentions, and A2 confirms the test can tell convex from")
print("  concave -- the concave controls reverse every time. Together with the")
print("  written argument above, the exchange lemma and therefore the extremal")
print("  law hold at every arity, not only arity 1.")
print()
print("  Evidence grade: written proof, with every step of the decomposition")
print("  checked in exact arithmetic on the stated finite range. The proof is")
print("  the warrant; the range is the check on the proof, not the claim.")
