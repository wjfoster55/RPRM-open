"""Crest-cut certificates for model-B breach questions.

Layer A: occupancy-ignoring geometric reachability R_opt under the actual
model-B move set (down 1..maxV, down-diagonal, horizontal; never up; walls
block). If water-mass occupying R_opt is already <= theta, CERTIFIED_NO.
If monitor mass > theta, CERTIFIED_YES.

Layer B: wall-supported catwalk R_catwalk (fall plus splash only from cells
with a WALL immediately below) plus a conservative sill-fill need. If no
water occupies R_catwalk and total V is strictly less than the water cells
required to stack from an existing wall up to a one-move fringe of R_catwalk,
CERTIFIED_NO. This does not treat other water as a floor, so it does not
attempt to decide packed-column creep.

Neither layer is a decoder for every above-crest arrangement. Packed water
can create and destroy support in one scan; that interaction is left to the
limited exact query (real stepB until A/B decide or the horizon ends).

The ablation `gap_adjacent_static` is recorded as a FAILED candidate: it is
not used for official verdicts.
"""
from __future__ import annotations

from collections import deque

# Pinned constants.js B.maxV
MAX_FALL = 6

# Official candidate summaries in this round.
CANDIDATES = ("crest_cut_A", "crest_cut_AB", "failed_gap_adjacent")
BASELINES = ("volume_height", "reachability_A", "early_exit_yes")


def idx(x, y, W):
    return y * W + x


def in_bounds(x, y, W, H):
    return 0 <= x < W and 0 <= y < H


def is_wall(walls, x, y, W, H):
    return (not in_bounds(x, y, W, H)) or bool(walls[idx(x, y, W)])


def wall_supported(walls, x, y, W, H):
    """Splash is possible without other water iff the cell below is WALL."""
    return is_wall(walls, x, y + 1, W, H) and not is_wall(walls, x, y, W, H)


def fall_clear(walls, x, y, k, W, H):
    """True if (x,y) can fall k cells: dest in bounds, not wall, and every
    intermediate cell is non-wall. Occupancy of water is ignored."""
    if k < 1:
        return False
    ny = y + k
    if not in_bounds(x, ny, W, H) or is_wall(walls, x, ny, W, H):
        return False
    for s in range(1, k):
        if is_wall(walls, x, y + s, W, H):
            return False
    return True


def forward_moves_opt(walls, x, y, W, H):
    """Occupancy-ignoring model-B moves from (x,y)."""
    if is_wall(walls, x, y, W, H):
        return
    for k in range(1, MAX_FALL + 1):
        if fall_clear(walls, x, y, k, W, H):
            yield (x, y + k)
        else:
            break
    for dx, dy in ((-1, 1), (1, 1), (-1, 0), (1, 0)):
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny, W, H) and not is_wall(walls, nx, ny, W, H):
            yield (nx, ny)


def forward_moves_catwalk(walls, x, y, W, H):
    """Fall always; lateral/diag only if this cell is wall-supported."""
    if is_wall(walls, x, y, W, H):
        return
    for k in range(1, MAX_FALL + 1):
        if fall_clear(walls, x, y, k, W, H):
            yield (x, y + k)
        else:
            break
    if wall_supported(walls, x, y, W, H):
        for dx, dy in ((-1, 1), (1, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny, W, H) and not is_wall(walls, nx, ny, W, H):
                yield (nx, ny)


def reverse_reachable(walls, monitor, W, H, move_fn):
    """Cells that can reach some monitor cell on the given forward-move graph."""
    mon = set()
    for m in monitor:
        x, y = m % W, m // W
        if in_bounds(x, y, W, H) and not is_wall(walls, x, y, W, H):
            mon.add((x, y))
    if not mon:
        return set()
    # Build reverse adjacency lazily via reverse scan of all non-wall cells.
    # Grid is small (admitted <= ~96x64).
    pred = [[] for _ in range(W * H)]
    for y in range(H):
        for x in range(W):
            if is_wall(walls, x, y, W, H):
                continue
            i = idx(x, y, W)
            for nx, ny in move_fn(walls, x, y, W, H):
                pred[idx(nx, ny, W)].append(i)
    seen = set()
    q = deque()
    for x, y in mon:
        i = idx(x, y, W)
        seen.add(i)
        q.append(i)
    while q:
        i = q.popleft()
        for j in pred[i]:
            if j not in seen:
                seen.add(j)
                q.append(j)
    return seen


def water_cells(mass, walls, W, H):
    out = []
    n = W * H
    for i in range(n):
        if mass[i] > 0 and not walls[i]:
            out.append(i)
    return out


def water_mass_in(mass, cells):
    return float(sum(mass[i] for i in cells))


def monitor_mass(mass, walls, monitor):
    s = 0.0
    for i in monitor:
        if not walls[i]:
            s += float(mass[i])
    return s


def volume_and_top(mass, walls, W, H):
    V = 0.0
    top = H
    for y in range(H):
        for x in range(W):
            i = idx(x, y, W)
            if mass[i] > 0 and not walls[i]:
                V += float(mass[i])
                if y < top:
                    top = y
    if V <= 0:
        top = H
    return V, top


def left_below_capacity(walls, dx, crest_y, W, H):
    """Non-wall cells with x < dx and y >= crest_y (left basin below crest).
    Used only as a documented comparison, not as an official certificate."""
    n = 0
    for y in range(crest_y, H):
        for x in range(0, dx):
            if not is_wall(walls, x, y, W, H):
                n += 1
    return n


def sill_need(walls, R_catwalk, W, H):
    """Minimum water cells to occupy a one-move fringe cell of R_catwalk
    by stacking on some existing wall in the same column.

    Conservative: ignores spreading, scan order, and the fact that 1-wide
    stacks usually slump. A number larger than V is required to claim NO.
    Returns None if no fringe exists (then only R_catwalk matters).
    """
    R = R_catwalk
    fringe = []
    for y in range(H):
        for x in range(W):
            if is_wall(walls, x, y, W, H):
                continue
            i = idx(x, y, W)
            if i in R:
                continue
            for nx, ny in forward_moves_opt(walls, x, y, W, H):
                if idx(nx, ny, W) in R:
                    fringe.append((x, y))
                    break
    if not fringe:
        return None
    best = None
    for x, y in fringe:
        # Occupy (x,y) sitting on a wall somewhere below in this column.
        need = None
        for yb in range(y + 1, H):
            if is_wall(walls, x, yb, W, H):
                # must fill y, y+1, ..., yb-1
                cells = 0
                ok = True
                for yy in range(y, yb):
                    if is_wall(walls, x, yy, W, H):
                        ok = False
                        break
                    cells += 1
                if ok:
                    need = cells
                break
        if need is None:
            continue
        if best is None or need < best:
            best = need
    return best


def evaluate_layers(walls, mass, monitor, W, H, theta, dx=None, crest_y=None):
    """Return layer verdicts and the graphs. No simulator rollout."""
    stats = {
        "graph_nodes_visited": 0,
        "R_opt_size": 0,
        "R_catwalk_size": 0,
        "water_in_R_opt": 0.0,
        "water_in_R_catwalk": 0.0,
        "monitor_mass": 0.0,
        "V": 0.0,
        "top": H,
        "sill_need": None,
        "left_below_capacity": None,
    }
    V, top = volume_and_top(mass, walls, W, H)
    stats["V"] = V
    stats["top"] = top
    mm = monitor_mass(mass, walls, monitor)
    stats["monitor_mass"] = mm
    if dx is not None and crest_y is not None:
        stats["left_below_capacity"] = left_below_capacity(walls, dx, crest_y, W, H)

    if mm > theta:
        stats["graph_nodes_visited"] = 0
        return {
            "A": {"verdict": "CERTIFIED_YES", "reason": "monitor_mass_gt_theta_now"},
            "B": {"verdict": "CERTIFIED_YES", "reason": "monitor_mass_gt_theta_now"},
            "failed_gap_adjacent": {"verdict": "CERTIFIED_YES", "reason": "monitor_mass_gt_theta_now"},
            "stats": stats,
        }

    R_opt = reverse_reachable(walls, monitor, W, H, forward_moves_opt)
    R_cat = reverse_reachable(walls, monitor, W, H, forward_moves_catwalk)
    stats["R_opt_size"] = len(R_opt)
    stats["R_catwalk_size"] = len(R_cat)
    stats["graph_nodes_visited"] = (W * H) * 2  # two full scans to build pred
    wcells = water_cells(mass, walls, W, H)
    w_opt = water_mass_in(mass, [i for i in wcells if i in R_opt])
    w_cat = water_mass_in(mass, [i for i in wcells if i in R_cat])
    stats["water_in_R_opt"] = w_opt
    stats["water_in_R_catwalk"] = w_cat
    need = sill_need(walls, R_cat, W, H)
    stats["sill_need"] = need

    if w_opt <= theta:
        a = {"verdict": "CERTIFIED_NO", "reason": "no_water_in_R_opt"}
    else:
        a = {"verdict": "UNRESOLVED", "reason": "water_in_R_opt"}

    if w_cat > theta:
        b = {"verdict": "UNRESOLVED", "reason": "water_in_R_catwalk"}
    elif need is None:
        # No fringe: cannot build a new one-move bridge to R_catwalk.
        # With no water on the catwalk either, R_opt may still be nonempty
        # because occupancy-ignoring horizontal walks exist. If V cannot
        # occupy even one fringe cell, NO; else UNRESOLVED.
        b = {"verdict": "CERTIFIED_NO", "reason": "no_catwalk_and_no_fringe"}
    elif V < need:
        b = {"verdict": "CERTIFIED_NO", "reason": "no_catwalk_and_V_lt_sill_need"}
    else:
        b = {"verdict": "UNRESOLVED", "reason": "V_may_build_sill_or_creep"}

    # Failed candidate: "not currently gap-adjacent and basin cannot fill".
    failed = failed_gap_adjacent_verdict(walls, mass, monitor, W, H, theta, dx, crest_y, mm, V)
    return {"A": a, "B": b, "failed_gap_adjacent": failed, "stats": stats}


def failed_gap_adjacent_verdict(walls, mass, monitor, W, H, theta, dx, crest_y, mm, V):
    """UNSOUND candidate kept as an ablation. Not an official verdict."""
    if mm > theta:
        return {"verdict": "CERTIFIED_YES", "reason": "monitor_mass_gt_theta_now"}
    if dx is None or crest_y is None:
        return {"verdict": "UNRESOLVED", "reason": "no_declared_divider"}
    gap_adj = 0.0
    for y in range(0, crest_y):
        for x in (dx - 1, dx, dx + 1):
            if in_bounds(x, y, W, H) and not is_wall(walls, x, y, W, H):
                gap_adj += float(mass[idx(x, y, W)])
    cap = left_below_capacity(walls, dx, crest_y, W, H)
    if gap_adj <= theta and V <= cap:
        return {"verdict": "CERTIFIED_NO", "reason": "not_gap_adjacent_and_V_le_basin"}
    return {"verdict": "UNRESOLVED", "reason": "gap_adjacent_or_fill_possible"}


def official_static_verdict(layers):
    """crest_cut_AB: YES from A; NO from A or B; else UNRESOLVED."""
    if layers["A"]["verdict"] == "CERTIFIED_YES":
        return "CERTIFIED_YES", "A:" + layers["A"]["reason"]
    if layers["A"]["verdict"] == "CERTIFIED_NO":
        return "CERTIFIED_NO", "A:" + layers["A"]["reason"]
    if layers["B"]["verdict"] == "CERTIFIED_NO":
        return "CERTIFIED_NO", "B:" + layers["B"]["reason"]
    return "UNRESOLVED", "AB:" + layers["A"]["reason"] + "|" + layers["B"]["reason"]


def current_cut_empty(walls, mass, monitor, W, H, theta):
    """Per-frame Layer A test used by the limited exact query."""
    mm = monitor_mass(mass, walls, monitor)
    if mm > theta:
        return "CERTIFIED_YES", mm
    R_opt = reverse_reachable(walls, monitor, W, H, forward_moves_opt)
    wcells = water_cells(mass, walls, W, H)
    w_opt = water_mass_in(mass, [i for i in wcells if i in R_opt])
    if w_opt <= theta:
        return "CERTIFIED_NO", mm
    return "UNRESOLVED", mm
