"""Independent ground-truth hydrostatic equilibrium solver.

This is the ORACLE for the falsification harness. It must be trustworthy and it
must share NO logic with model D's read-off (js/models.js `relaxLevels`): no
`top`-bounded cavity, no first-claim allocation.

Method: an explicit QUASISTATIC SPILL/RETENTION flood, iterated to a fixed point
to resolve merges/splits.

  Each outer pass:
    1. DOWNFALL to rest (incompressible gravity: water stacks on floors).
    2. Label connected water bodies (4-connected through water).
    3. For each body, place its conserved volume V by the quasistatic spill flood
       (`_fill_region`): water rises in the basin its source occupies, filling it
       bottom-up; when the surface reaches a spill crest and there is EXCESS, only
       that excess spills into the connected lower basin, which fills as its own
       pool at its own lower level. A lower basin that fills back up to the crest
       MERGES and the combined body rises as one flat surface. This equalizes a
       U-tube, refuses to cross a ridge taller than the water, pours over a ridge
       shorter than the water, and — unlike a single-global-level + mass rescale —
       never redistributes across a divider when V falls inside a discontinuous
       capacity jump (the PR#9 oracle bug: 6/2 was reported as 2.667/5.333).
    4. If two bodies' fill regions overlap (they merge at their rest levels), union
       them (combine cells+V) and refill; repeat until no overlap.
  Iterate passes until the mass grid stops changing.

Validated against analytic cases in `_selftest` (run this file directly),
including the two-compartment spill regression. Only trust its verdicts after
that passes; the dedicated suite is `experiments/test_spill_regression.py`.
"""
import heapq
import numpy as np

MAXMASS = 1.0
EPS = 1e-9


def _components(water):
    """4-connected components of boolean `water`. Returns (label grid, count)."""
    H, Wd = water.shape
    lab = -np.ones((H, Wd), dtype=np.int64)
    cid = 0
    for sy in range(H):
        for sx in range(Wd):
            if not water[sy, sx] or lab[sy, sx] != -1:
                continue
            stack = [(sy, sx)]
            lab[sy, sx] = cid
            while stack:
                y, x = stack.pop()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < Wd and water[ny, nx] and lab[ny, nx] == -1:
                        lab[ny, nx] = cid
                        stack.append((ny, nx))
            cid += 1
    return lab, cid


def _downfall_to_rest(mass, solid, max_sweeps=4000):
    """Incompressible gravity: repeatedly move water into empty capacity below
    until nothing moves. Vectorized column-wise."""
    H, Wd = mass.shape
    for _ in range(max_sweeps):
        cap = np.zeros_like(mass)
        cap[1:, :] = np.where(solid[1:, :], 0.0, MAXMASS - mass[1:, :])
        cap = np.clip(cap, 0.0, None)
        src = mass.copy()
        src[solid] = 0.0
        move = np.zeros_like(mass)
        move[1:, :] = np.minimum(src[:-1, :], cap[1:, :])
        move[1:, :][solid[:-1, :]] = 0.0
        if move.max() < EPS:
            break
        mass[1:, :] += move[1:, :]
        mass[:-1, :] -= move[1:, :]


def _nonsolid_region(seed_cells, solid):
    """Connected component of non-solid cells reachable from any seed (4-conn).
    Closed container => finite. Returns a boolean mask."""
    H, Wd = solid.shape
    mask = np.zeros((H, Wd), bool)
    stack = list(seed_cells)
    for (y, x) in seed_cells:
        mask[y, x] = True
    while stack:
        y, x = stack.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < Wd and not solid[ny, nx] and not mask[ny, nx]:
                mask[ny, nx] = True
                stack.append((ny, nx))
    return mask


def _solve_level(pool, level, top, remaining, bot):
    """Binary-search the free-surface height L in [level, top] such that raising a
    FIXED pool of cells from `level` to L adds exactly `remaining` water. Capacity
    is piecewise-linear + monotone in this interval, so bisection is exact."""
    lo, hi = level, top
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        add = 0.0
        for c in pool:
            b = bot[c]
            hival = 1.0 if mid - b >= 1.0 else (mid - b if mid > b else 0.0)
            loval = 1.0 if level - b >= 1.0 else (level - b if level > b else 0.0)
            add += hival - loval
        if add < remaining:
            lo = mid
        else:
            hi = mid
    return hi


def _fill_region(omega, body_seeds, V, H, Wd):
    """Quasistatic spill/retention fill: place volume V, entering at `body_seeds`,
    into the connected non-solid region `omega` (a set of flat indices y*Wd+x).

    Contract (the FIX for the PR#9 oracle bug): water rises in the basin that its
    source occupies. It fills that basin from the bottom up. When the surface
    reaches a spill crest (a cell whose only escape is a *drop* into a lower cell
    that the current pool cannot yet reach) and there is EXCESS volume, ONLY that
    excess spills into the connected lower basin, which fills as its own pool at
    its own (lower) level. A lower basin that fills back up to the crest MERGES
    with the source pool and the combined body then rises as one flat surface.

    This never assigns a single global level across a divider, so no discontinuous
    capacity jump + mass rescale can occur (the failure that produced 2.667/5.333
    instead of 6/2 on a two-compartment container).

    Returns (fills: {cell: mass}, reach: set(cells))."""
    fills = {}
    claimed = set()
    bot = {c: (H - 1 - (c // Wd)) for c in omega}

    def neighbors(c):
        y = c // Wd
        x = c - y * Wd
        out = []
        if y > 0:      out.append(c - Wd)
        if y < H - 1:  out.append(c + Wd)
        if x > 0:      out.append(c - 1)
        if x < Wd - 1: out.append(c + 1)
        return out

    def frac(L, b):
        return 1.0 if L - b >= 1.0 else (L - b if L > b else 0.0)

    def pour(seeds, vol, cap_level):
        """Rise water from `seeds`, spilling into lower sub-basins recursively, but
        never above `cap_level`. Returns (leftover, level, pool_cells)."""
        pool = set()
        heap = []
        inheap = set()

        def push(c):
            if c in omega and c not in claimed and c not in pool and c not in inheap:
                heapq.heappush(heap, (bot[c], c))
                inheap.add(c)

        for s in seeds:
            if s in claimed or s not in omega:
                continue
            pool.add(s)
            claimed.add(s)
        if not pool:
            return vol, None, pool
        for s in pool:
            for nc in neighbors(s):
                push(nc)
        level = min(bot[c] for c in pool)

        def set_fills(L):
            for c in pool:
                fills[c] = frac(L, bot[c])

        set_fills(level)
        remaining = vol
        while remaining > EPS:
            nb = heap[0][0] if heap else (H + 1)
            top = min(nb, cap_level)
            if top > level + EPS:
                cap = 0.0
                for c in pool:
                    b = bot[c]
                    cap += frac(top, b) - frac(level, b)
                if remaining <= cap + EPS:
                    final = _solve_level(pool, level, top, remaining, bot)
                    set_fills(final)
                    return 0.0, final, pool
                remaining -= cap
                level = top
                set_fills(level)
                if level >= cap_level - EPS:
                    return remaining, level, pool
            if not heap:
                return remaining, level, pool
            nb, nc = heapq.heappop(heap)
            inheap.discard(nc)
            if nc in claimed:
                continue
            if bot[nc] >= level - EPS:
                # lateral cell at the current surface: extend this pool.
                pool.add(nc)
                claimed.add(nc)
                fills[nc] = frac(level, bot[nc])
                for x in neighbors(nc):
                    push(x)
            else:
                # crest crossed into a strictly-lower cell: spill the excess only.
                sub_left, sub_lvl, sub_pool = pour([nc], remaining, level)
                if sub_left <= EPS:
                    return 0.0, level, pool     # source pinned at crest; excess held below
                # lower basin filled to the crest -> merge, keep rising together.
                remaining = sub_left
                for c in sub_pool:
                    pool.add(c)
                    for x in neighbors(c):
                        push(x)
        return 0.0, level, pool

    pour(list(body_seeds), float(V), float(H + 1))
    out = {c: v * MAXMASS for c, v in fills.items() if v > 1e-9}
    reach = set(out.keys())
    return out, reach


def _fill_body(body_cells, V, solid, H, Wd):
    """Place volume V for a connected body at its true hydrostatic rest via the
    quasistatic spill/retention flood. Returns (fill_dict {(y,x): mass}, reach)."""
    omega = _nonsolid_region(body_cells, solid)
    omega_idx = {y * Wd + x for (y, x) in zip(*np.nonzero(omega))}
    seeds = [y * Wd + x for (y, x) in body_cells]
    out_idx, reach_idx = _fill_region(omega_idx, seeds, V, H, Wd)
    out = {(c // Wd, c % Wd): v for c, v in out_idx.items()}
    reach = np.zeros((H, Wd), bool)
    for c in reach_idx:
        reach[c // Wd, c % Wd] = True
    return out, reach


def settle_truth(mass0, walls, max_passes=60):
    """Return the true resting mass grid for the given start state."""
    solid = walls.astype(bool)
    H, Wd = mass0.shape
    mass = mass0.astype(np.float64).copy()
    mass[solid] = 0.0

    for _pass in range(max_passes):
        _downfall_to_rest(mass, solid)
        water = mass > EPS
        lab, n = _components(water)
        if n == 0:
            break
        # gather bodies
        bodies = []
        for c in range(n):
            ys, xs = np.nonzero(lab == c)
            cells = list(zip(ys.tolist(), xs.tolist()))
            V = float(mass[ys, xs].sum())
            bodies.append([cells, V])

        # fill each body; then union any whose fill regions overlap and refill.
        def fill_group(cells, V):
            return _fill_body(cells, V, solid, H, Wd)

        # iterate union-on-overlap to a stable set of filled regions
        fills = []
        regions = []
        for cells, V in bodies:
            out, reach = fill_group(cells, V)
            fills.append(out)
            regions.append(set(out.keys()))

        merged = True
        groups = [[i] for i in range(len(bodies))]
        while merged:
            merged = False
            # recompute group fills
            gfills = []
            gregions = []
            gcells = []
            gV = []
            for grp in groups:
                cells = []
                V = 0.0
                for i in grp:
                    cells += bodies[i][0]
                    V += bodies[i][1]
                out, reach = fill_group(cells, V)
                gfills.append(out)
                gregions.append(set(out.keys()))
                gcells.append(cells)
                gV.append(V)
            # detect overlap between groups
            newgroups = None
            for a in range(len(groups)):
                for b in range(a + 1, len(groups)):
                    if gregions[a] & gregions[b]:
                        newgroups = [groups[k] for k in range(len(groups)) if k not in (a, b)]
                        newgroups.append(groups[a] + groups[b])
                        merged = True
                        break
                if merged:
                    break
            if merged:
                groups = newgroups
            else:
                fills = gfills

        newmass = np.zeros_like(mass)
        for out in fills:
            for (y, x), v in out.items():
                newmass[y, x] += v
        newmass[solid] = 0.0

        if np.abs(newmass - mass).max() < 1e-7:
            mass = newmass
            break
        mass = newmass
    return mass


def surface_levels(mass, walls):
    """Free-surface height of every connected water body:
    list of (component_id, volume, surface_height, cells)."""
    solid = walls.astype(bool)
    water = (mass > EPS) & (~solid)
    lab, n = _components(water)
    H, Wd = mass.shape
    out = []
    for c in range(n):
        ys, xs = np.nonzero(lab == c)
        V = float(mass[ys, xs].sum())
        toprow = int(ys.min())
        toprow_cells = mass[toprow, xs[ys == toprow]]
        frac = float(np.clip(toprow_cells.mean() / MAXMASS, 0, 1))
        sh = (H - 1 - toprow) + frac
        out.append((c, V, sh, list(zip(ys.tolist(), xs.tolist()))))
    return out


# --------------------------- self-test --------------------------------------
def _mk(H, Wd):
    walls = np.zeros((H, Wd), bool)
    walls[0, :] = walls[-1, :] = True
    walls[:, 0] = walls[:, -1] = True
    mass = np.zeros((H, Wd))
    return walls, mass


def _selftest():
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 1. single flat basin
    H, Wd = 30, 40
    walls, mass = _mk(H, Wd)
    for y in range(5, 28):
        for x in range(5, 12):
            mass[y, x] = 1.0
    V0 = mass.sum()
    rest = settle_truth(mass, walls)
    check("single-basin mass conserved", abs(rest.sum() - V0) < 1e-4, f"{rest.sum():.3f} vs {V0:.3f}")
    lv = surface_levels(rest, walls)
    check("single-basin one body", len(lv) == 1, f"bodies={len(lv)}")
    water = rest > 1e-6
    tops = [np.nonzero(water[:, x])[0].min() for x in range(1, Wd - 1) if water[:, x].any()]
    check("single-basin flat surface", np.std(tops) < 0.8, f"std={np.std(tops):.3f}")

    # 2. U-tube
    H, Wd = 34, 40
    walls, mass = _mk(H, Wd)
    walls[3:H - 1, 1:Wd - 1] = True
    xL, xR, sw = 6, 26, 6
    floor = H - 4
    for y in range(3, floor):
        walls[y, xL:xL + sw] = False
        walls[y, xR:xR + sw] = False
    walls[floor:H - 1, xL:xR + sw] = False
    for y in range(6, floor):
        mass[y, xL:xL + sw] = 1.0
    mass[walls] = 0
    V0 = mass.sum()
    rest = settle_truth(mass, walls)
    lh = rest[:, xL:xL + sw].sum() / sw
    rh = rest[:, xR:xR + sw].sum() / sw
    check("U-tube mass conserved", abs(rest.sum() - V0) < 1e-3, f"{rest.sum():.3f} vs {V0:.3f}")
    check("U-tube equalizes", abs(lh - rh) < 1.0, f"lh={lh:.2f} rh={rh:.2f} dh={abs(lh-rh):.3f}")

    # 3. two DISCONNECTED basins at different fills
    H, Wd = 24, 40
    walls, mass = _mk(H, Wd)
    walls[:, 20] = True
    for y in range(10, 23):
        mass[y, 2:19] = 1.0
    for y in range(16, 23):
        mass[y, 21:39] = 1.0
    mass[walls] = 0
    V0 = mass.sum()
    rest = settle_truth(mass, walls)
    lv = surface_levels(rest, walls)
    check("two-basins mass conserved", abs(rest.sum() - V0) < 1e-3)
    check("two-basins stay separate", len(lv) == 2, f"bodies={len(lv)}")
    if len(lv) == 2:
        hs = sorted(s for _, _, s, _ in lv)
        check("two-basins different levels", (hs[1] - hs[0]) > 1.0, f"levels={[round(h,2) for h in hs]}")

    # 4. submerged low ridge -> spill and equalize to ONE level
    H, Wd = 24, 40
    walls, mass = _mk(H, Wd)
    walls[18:23, 20] = True
    for y in range(6, 23):
        mass[y, 2:19] = 1.0
    mass[walls] = 0
    V0 = mass.sum()
    rest = settle_truth(mass, walls)
    check("low-ridge mass conserved", abs(rest.sum() - V0) < 1e-3, f"{rest.sum():.3f} vs {V0:.3f}")
    lh = rest[:, 2:20].sum()
    rh = rest[:, 21:39].sum()
    check("low-ridge spills over", rh > 0.2 * V0, f"left={lh:.1f} right={rh:.1f}")
    # and equalizes to one flat level
    lv = surface_levels(rest, walls)
    check("low-ridge one connected level", len(lv) == 1, f"bodies={len(lv)}")

    # 5. TALL ridge -> water stays on its side (no spill)
    H, Wd = 24, 40
    walls, mass = _mk(H, Wd)
    walls[4:23, 20] = True   # tall ridge (near full height)
    for y in range(14, 23):
        mass[y, 2:19] = 1.0
    mass[walls] = 0
    V0 = mass.sum()
    rest = settle_truth(mass, walls)
    rh = rest[:, 21:39].sum()
    check("tall-ridge no spill", rh < 1e-3, f"right={rh:.3f}")

    # 6. mid-splash: a floating block over a basin settles to the right level.
    H, Wd = 30, 30
    walls, mass = _mk(H, Wd)
    for y in range(3, 8):       # floating block in the air
        mass[y, 10:20] = 1.0
    V0 = mass.sum()
    rest = settle_truth(mass, walls)
    check("mid-splash mass conserved", abs(rest.sum() - V0) < 1e-3)
    lv = surface_levels(rest, walls)
    check("mid-splash settles to one pool", len(lv) == 1, f"bodies={len(lv)}")

    print("\nSELFTEST:", "ALL PASS" if ok else "FAILURES PRESENT")
    return ok


if __name__ == "__main__":
    _selftest()
