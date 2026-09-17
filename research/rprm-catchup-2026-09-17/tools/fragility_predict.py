"""Does the log-convexity failure PREDICT the classical monoid's bad cells?

§8f showed two things sit in the same regime: the classical factor function
f_blind(k) = sum_j (n_j+1)^k - (m-1) fails log-convexity, and sigma_blind fails
the extremal law. Same regime is not the same as same cause. This script asks
whether the first actually predicts the second.

The proof of §8d has exactly two ingredients. If sigma_blind fails an exchange,
at least one of them must have failed for it. So:

DECLARED BEFORE RUNNING
  R1  Every sigma_blind exchange failure must coincide with a failure of
      Step 2 (log-convexity of f_blind at the relevant exponents) or of Step 1
      (the base inequality f_blind,q >= f_blind,p pointwise). If some exchange
      fails with BOTH steps intact, the proof of §8d is wrong, because the same
      two steps would then chain to a contradiction. This is therefore a check
      on §8d as much as on the mechanism.
  R2  PREDICTIVE DIRECTION. Restricting to exchanges where Step 2 holds for
      f_blind, sigma_blind should never fail. That is the useful statement: the
      log-convexity of the factor function at the two exponents being exchanged
      is what decides it.
  R3  NULL / specificity. Step-2 failure must NOT be ubiquitous. If Step 2 fails
      almost everywhere for f_blind then it predicts nothing. Report the base
      rate, and report how often Step-2 failure is accompanied by an actual
      sigma_blind exchange failure -- if that is near zero the condition is
      necessary but useless.
  R4  CONTROL. The same audit run against sigma_E must show zero of everything.
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


def f_E(p, k):
    return 1 + sum(n ** k for n in p)


def f_B(p, k):
    return 1 + sum((n + 1) ** k - 1 for n in p)


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


NMAX = 26


def audit(f, label):
    tot = 0
    step1_fail = 0
    step2_fail = 0
    sig_fail = 0
    both_intact_and_failed = []
    step2ok_and_failed = []
    step2fail_and_failed = 0

    for n in range(4, NMAX + 1):
        for m in range(1, n + 1):
            for p in partitions(n, m):
                for a, b, rest, q in exchanges(p):
                    tot += 1
                    s1 = all(f(q, k) >= f(p, k)
                             for k in set(list(p) + list(q)))
                    s2 = f(q, a + 1) * f(q, b - 1) >= f(q, a) * f(q, b)
                    sg = prod(f(q, k) for k in q) > prod(f(p, k) for k in p)
                    step1_fail += not s1
                    step2_fail += not s2
                    sig_fail += not sg
                    if not sg:
                        if s1 and s2:
                            both_intact_and_failed.append((p, a, b, q))
                        if s2:
                            step2ok_and_failed.append((p, a, b, q))
                        else:
                            step2fail_and_failed += 1

    print(f"  {label}")
    print(f"    exchanges audited                                {tot:>10,}")
    print(f"    Step 1 (base inequality) failures                {step1_fail:>10,}")
    print(f"    Step 2 (log-convexity at the exchanged exponents) {step2_fail:>9,}"
          f"   base rate {step2_fail/tot:>6.1%}")
    print(f"    actual exchange failures (sigma decreased)       {sig_fail:>10,}")
    print()
    print(f"    R1  failures with BOTH steps intact              "
          f"{len(both_intact_and_failed):>10,}  "
          f"{'ok' if not both_intact_and_failed else 'FAIL -- §8d would be wrong'}")
    print(f"    R2  failures where Step 2 HELD                   "
          f"{len(step2ok_and_failed):>10,}  "
          f"{'ok -- Step 2 holding is sufficient' if not step2ok_and_failed else 'FAIL'}")
    if step2_fail:
        print(f"    R3  of the {step2_fail:,} Step-2 failures, "
              f"{step2fail_and_failed:,} ({step2fail_and_failed/step2_fail:.1%}) "
              f"actually broke sigma")
    for row in both_intact_and_failed[:4]:
        print("       counterexample to R1:", row)
    for row in step2ok_and_failed[:4]:
        print("       counterexample to R2:", row)
    return len(both_intact_and_failed) + len(step2ok_and_failed)


print("=" * 88)
print(f"R1-R4  Is log-convexity the deciding condition?  (all partitions, n <= {NMAX})")
print("=" * 88)
bad = 0
bad += audit(f_B, "sigma_blind  --  successor agreement only")
print()
bad += audit(f_E, "sigma_E      --  enabledness enforced  (R4 control)")

print()
print("=" * 88)
print("TOTAL FAILURES:", bad)
print("=" * 88)
print()
print("  Reading, if R1 and R2 both hold. Log-convexity of the factor function at")
print("  the two exchanged exponents is not merely correlated with the extremal")
print("  law -- whenever it holds, the exchange holds. The classical monoid loses")
print("  the law exactly where the -1 per block costs it log-convexity, and the")
print("  enabledness-enforced monoid never loses it because a sum of exponentials")
print("  is log-convex everywhere.")
print()
print("  R3 is the honest qualifier: Step-2 failure is necessary, not sufficient.")
print("  A Step-2 failure at one exchanged pair can still be outweighed by the")
print("  spectator factors, so the base rate of Step-2 failure is much higher than")
print("  the rate of actual extremal failure. The condition predicts where the law")
print("  CAN break, not where it must.")
print()
print("  Evidence grade: finite test, complete enumeration in the stated range.")
