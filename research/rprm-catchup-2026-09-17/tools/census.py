"""Enabledness census pilot.

Exhaustive enumeration of finite deterministic PARTIAL machines.
For each machine we compute two coarsest stable refinements:

  P_rprm   failure is a distinct successor tag        (RPRM O05 condition 2 enforced)
  P_stall  an undefined action is completed by a self-loop
           (the standard totalisation a modeller reaches for when enabledness
            is not instrumented)

P_stall is always coarser or equal.  gap = |P_rprm| - |P_stall| >= 0 is the
number of distinctions that condition 2 -- and only condition 2 -- retains.

When gap > 0 we also compute the EXPOSURE DEPTH: the shortlex-least word length
at which a pair merged by P_stall becomes separable once failure is observable.
That is the length of the cheapest experiment that would have caught the error.

Integers only.  Complete enumeration inside each declared family.
"""

import sys
import time
from collections import deque
from itertools import product

sys.stdout.reconfigure(encoding="utf-8")

FAIL = -1


def refine(n, k, obs, trans, stall):
    """Coarsest stable refinement. trans is a flat tuple of length n*k, -1 = undefined.

    Returns the block id per state as a tuple.
    """
    blocks = list(obs)
    # normalise initial labels
    seen = {}
    blocks = [seen.setdefault(b, len(seen)) for b in blocks]
    while True:
        sigs = []
        for s in range(n):
            row = [blocks[s]]
            for a in range(k):
                t = trans[a * n + s]
                if t == FAIL:
                    row.append(blocks[s] if stall else FAIL)
                else:
                    row.append(blocks[t])
            sigs.append(tuple(row))
        seen = {}
        new = [seen.setdefault(sg, len(seen)) for sg in sigs]
        if new == blocks:
            return tuple(blocks)
        blocks = new


def exposure_depth(n, k, obs, trans, x, y):
    """Shortlex-least separating word length with failure observable. None if no split."""
    SINK = n  # absorbing failure state

    def ob(s):
        return FAIL if s == SINK else obs[s]

    def step(s, a):
        if s == SINK:
            return SINK
        t = trans[a * n + s]
        return SINK if t == FAIL else t

    q = deque([(x, y, 0)])
    seen = {(x, y)}
    while q:
        u, v, d = q.popleft()
        if ob(u) != ob(v):
            return d
        for a in range(k):
            p = (step(u, a), step(v, a))
            if p not in seen:
                seen.add(p)
                q.append((p[0], p[1], d + 1))
    return None


def census(n, k, b, limit=None):
    """Exhaustive over all b^n observation labellings and (n+1)^(n*k) partial tables."""
    total = 0
    gapped = 0
    gapsum = 0
    gapmax = 0
    depth_hist = {}
    worst = None
    obs_space = list(product(range(b), repeat=n))
    tr_space = product(range(-1, n), repeat=n * k)
    for trans in tr_space:
        for obs in obs_space:
            total += 1
            pr = refine(n, k, obs, trans, stall=False)
            ps = refine(n, k, obs, trans, stall=True)
            cr = len(set(pr))
            cs = len(set(ps))
            if cr != cs:
                gapped += 1
                g = cr - cs
                gapsum += g
                if g > gapmax:
                    gapmax = g
                # deepest exposure among pairs merged by stall, split by rprm
                best = -1
                for x in range(n):
                    for y in range(x + 1, n):
                        if ps[x] == ps[y] and pr[x] != pr[y]:
                            d = exposure_depth(n, k, obs, trans, x, y)
                            if d is not None and d > best:
                                best = d
                if best >= 0:
                    depth_hist[best] = depth_hist.get(best, 0) + 1
                    if worst is None or best > worst[0]:
                        worst = (best, n, k, obs, trans)
        if limit and total >= limit:
            break
    return {
        "n": n, "k": k, "b": b, "machines": total, "gapped": gapped,
        "gap_sum": gapsum, "gap_max": gapmax, "depths": depth_hist, "worst": worst,
    }


def main():
    print("=" * 96)
    print("PILOT A  Reproduce the shipped census family from checks/futures.py")
    print("         families (n,actions): (0,a) (1,ab) (2,ab) (3,a)   binary observations")
    print("=" * 96)
    shipped = [(0, 1), (1, 2), (2, 2), (3, 1)]
    tot = 0
    for n, k in shipped:
        cnt = (2 ** n) * ((n + 1) ** (n * k))
        tot += cnt
        print(f"  n={n} k={k}  observations 2^{n}={2**n:>3}  tables ({n}+1)^{n*k}={(n+1)**(n*k):>6}"
              f"   machines {cnt:>6}")
    print(f"  TOTAL {tot}   shipped docs/verification.md says 845   "
          f"{'MATCH' if tot == 845 else 'MISMATCH'}")

    print()
    print("=" * 96)
    print("PILOT B  Enabledness census. How many machines have distinctions that ONLY")
    print("         condition 2 (enabledness agreement) retains?")
    print("=" * 96)
    print(f"{'n':>2} {'k':>2} {'b':>2} {'machines':>10} {'gapped':>9} {'% gapped':>9} "
          f"{'sum gap':>8} {'max gap':>8} {'max exposure depth':>19}")
    rows = []
    fams = [(1, 1, 2), (1, 2, 2), (2, 1, 2), (2, 2, 2), (3, 1, 2), (3, 2, 2),
            (4, 1, 2), (2, 2, 3), (3, 1, 3), (3, 2, 3), (4, 1, 3), (5, 1, 2)]
    for (n, k, b) in fams:
        t0 = time.time()
        r = census(n, k, b)
        dt = time.time() - t0
        md = max(r["depths"]) if r["depths"] else 0
        pct = 100.0 * r["gapped"] / r["machines"] if r["machines"] else 0.0
        print(f"{n:>2} {k:>2} {b:>2} {r['machines']:>10} {r['gapped']:>9} {pct:>8.2f}% "
              f"{r['gap_sum']:>8} {r['gap_max']:>8} {md:>19}   ({dt:.1f}s)")
        rows.append(r)

    print()
    print("=" * 96)
    print("PILOT C  Exposure-depth histogram: cheapest experiment that catches the error")
    print("         (shortlex-least word length separating a stall-merged pair once")
    print("          failure is observable)")
    print("=" * 96)
    alldepths = {}
    for r in rows:
        for d, c in r["depths"].items():
            alldepths[d] = alldepths.get(d, 0) + c
    print(f"{'depth':>6} {'machines':>10}")
    for d in sorted(alldepths):
        print(f"{d:>6} {alldepths[d]:>10}")

    print()
    print("=" * 96)
    print("PILOT D  Minimal witness: smallest family with a nonzero gap, and one machine")
    print("=" * 96)
    for r in rows:
        if r["gapped"]:
            print(f"  first nonzero gap at n={r['n']} k={r['k']} b={r['b']}")
            break
    # exhibit one explicit smallest machine
    found = None
    for n, k, b in [(1, 1, 2), (1, 2, 2), (2, 1, 2), (2, 2, 2), (3, 1, 2)]:
        for trans in product(range(-1, n), repeat=n * k):
            for obs in product(range(b), repeat=n):
                pr = refine(n, k, obs, trans, stall=False)
                ps = refine(n, k, obs, trans, stall=True)
                if len(set(pr)) != len(set(ps)):
                    found = (n, k, b, obs, trans, pr, ps)
                    break
            if found:
                break
        if found:
            break
    if found:
        n, k, b, obs, trans, pr, ps = found
        print(f"  states {list(range(n))}  actions {list(range(k))}")
        print(f"  observation  {dict(enumerate(obs))}")
        for a in range(k):
            tb = {s: trans[a * n + s] for s in range(n) if trans[a * n + s] != FAIL}
            print(f"  delta_{a}      {tb}   (undefined at "
                  f"{[s for s in range(n) if trans[a*n+s] == FAIL]})")
        print(f"  P_rprm  blocks {pr}  -> {len(set(pr))} classes")
        print(f"  P_stall blocks {ps}  -> {len(set(ps))} classes")
        for x in range(n):
            for y in range(x + 1, n):
                if ps[x] == ps[y] and pr[x] != pr[y]:
                    print(f"  pair ({x},{y}) merged by stall, split by RPRM; "
                          f"exposure depth {exposure_depth(n, k, obs, trans, x, y)}")

    print()
    print("=" * 96)
    print("PILOT E  NULL CONTROL, declared before the run: on TOTAL machines (no")
    print("         undefined transitions) condition 2 is vacuous, so the gap must be")
    print("         exactly 0 in every family. If this prints anything but 0 the")
    print("         instrument is broken.")
    print("=" * 96)
    for n, k, b in [(2, 2, 2), (3, 2, 2), (4, 1, 2), (3, 2, 3)]:
        bad = 0
        cnt = 0
        for trans in product(range(n), repeat=n * k):
            for obs in product(range(b), repeat=n):
                cnt += 1
                if len(set(refine(n, k, obs, trans, False))) != \
                   len(set(refine(n, k, obs, trans, True))):
                    bad += 1
        print(f"  n={n} k={k} b={b}  total machines {cnt:>8}  nonzero gaps {bad}  "
              f"{'NULL HOLDS' if bad == 0 else 'NULL VIOLATED'}")


if __name__ == "__main__":
    main()
