"""F3 certificates for the pinned model-B breach receiver.

Frozen F2 Layer B (`sill_need` CERTIFIED_NO) remains refuted. Official
static routing is:

- Layer A on *unit-normalized* occupancy
- Unit-isolation NO: exactly one water cell, not on R_catwalk
- n >= 2: UNRESOLVED, then limited exact

Pair-soup audits live here as failed cheap V>=2 candidates, not as
official certificates. Evidence grades are in CLAIM.md.
"""
from __future__ import annotations

from collections import deque

from f2_import import bound

SPLASH = ((-1, 1), (1, 1), (-1, 0), (1, 0))


def normalize_unit_occupancy(mass, walls):
    """Match pinned normalizeForModel(B): every positive-mass non-wall cell
    becomes occupancy 1 before any certificate or rollout comparison."""
    out = []
    for i, m in enumerate(mass):
        if walls[i]:
            out.append(0.0)
        elif m > 0:
            out.append(1.0)
        else:
            out.append(0.0)
    return out


def unit_water_count(mass, walls):
    n = 0
    for i, m in enumerate(mass):
        if walls[i]:
            continue
        if m > 0:
            n += 1
    return n


def water_indices(mass, walls):
    out = []
    for i, m in enumerate(mass):
        if walls[i]:
            continue
        if m > 0:
            out.append(i)
    return out


def isolation_verdict(layers, n_water, theta):
    """CERTIFIED_NO only for a unique unit cell outside R_catwalk."""
    if n_water == 0:
        return {
            "verdict": "UNRESOLVED",
            "reason": "no_water_defer_to_A",
            "n_water": 0,
        }
    if n_water >= 2:
        return {
            "verdict": "UNRESOLVED",
            "reason": "n_ge_2_no_cheap_static_no",
            "n_water": n_water,
        }
    if layers["A"]["verdict"] == "CERTIFIED_YES":
        return {
            "verdict": "CERTIFIED_YES",
            "reason": "monitor_mass_gt_theta_now",
            "n_water": 1,
        }
    if layers["A"]["verdict"] == "CERTIFIED_NO":
        return {
            "verdict": "UNRESOLVED",
            "reason": "A_already_no",
            "n_water": 1,
        }
    w_cat = layers["stats"]["water_in_R_catwalk"]
    if w_cat > theta:
        return {
            "verdict": "UNRESOLVED",
            "reason": "unique_cell_on_R_catwalk",
            "n_water": 1,
        }
    return {
        "verdict": "CERTIFIED_NO",
        "reason": "unique_cell_not_on_R_catwalk",
        "n_water": 1,
    }


def catwalk_forward_from(walls, starts, W, H):
    seen = set()
    q = deque()
    for i in starts:
        x, y = i % W, i // W
        if bound.is_wall(walls, x, y, W, H):
            continue
        if i not in seen:
            seen.add(i)
            q.append(i)
    while q:
        i = q.popleft()
        x, y = i % W, i // W
        for nx, ny in bound.forward_moves_catwalk(walls, x, y, W, H):
            j = bound.idx(nx, ny, W)
            if j not in seen:
                seen.add(j)
                q.append(j)
    return seen


def splash_dests(walls, i, W, H):
    x, y = i % W, i // W
    out = []
    for dx, dy in SPLASH:
        nx, ny = x + dx, y + dy
        if bound.in_bounds(nx, ny, W, H) and not bound.is_wall(walls, nx, ny, W, H):
            out.append(bound.idx(nx, ny, W))
    return out


def support_enabled(walls, i, F, W, H, allow_water_floor):
    x, y = i % W, i // W
    if bound.wall_supported(walls, x, y, W, H):
        return True
    if not allow_water_floor:
        return False
    by = y + 1
    if not bound.in_bounds(x, by, W, H) or bound.is_wall(walls, x, by, W, H):
        return False
    return bound.idx(x, by, W) in F


def can_step_to(walls, src, dest, F, W, H, allow_water_floor):
    sx, sy = src % W, src // W
    dx, dy = dest % W, dest // W
    if bound.is_wall(walls, sx, sy, W, H) or bound.is_wall(walls, dx, dy, W, H):
        return False
    if sx == dx and dy > sy:
        k = dy - sy
        if k <= bound.MAX_FALL and bound.fall_clear(walls, sx, sy, k, W, H):
            return True
    if support_enabled(walls, src, F, W, H, allow_water_floor):
        if (dx - sx, dy - sy) in SPLASH:
            return True
    return False


def cell_graph_closure(walls, starts, R_cat, W, H, allow_water_floor):
    """Occupancy-ignoring soup. Simultaneity / token count is ignored.

    allow_water_floor True: a soup cell may stand on another soup cell.
    That recovers packed-column laterals and also unbounded stacking.
    False: only wall-supported injection. Useful on isolated shelves,
    unsound on packed-column YES scenes.
    """
    F = catwalk_forward_from(walls, starts, W, H)
    if F & R_cat:
        return F, True
    changed = True
    while changed:
        changed = False
        members = list(F)
        newcomers = set()
        for q in members:
            qx, qy = q % W, q // W
            by = qy + 1
            if not bound.in_bounds(qx, by, W, H) or bound.is_wall(walls, qx, by, W, H):
                continue
            below = bound.idx(qx, by, W)
            supported = allow_water_floor and below in F
            if not supported:
                for p in members:
                    if p == q:
                        continue
                    if allow_water_floor:
                        if can_step_to(
                            walls, p, below, F, W, H, True,
                        ):
                            supported = True
                            break
                    else:
                        px, py = p % W, p // W
                        if not bound.wall_supported(walls, px, py, W, H):
                            continue
                        if (below % W - px, below // W - py) in SPLASH:
                            if not bound.is_wall(
                                walls, below % W, below // W, W, H,
                            ):
                                supported = True
                                break
            if not supported:
                continue
            for dest in splash_dests(walls, q, W, H):
                if dest not in F:
                    newcomers.add(dest)
        if not newcomers:
            break
        extra = catwalk_forward_from(walls, newcomers, W, H)
        added = extra - F
        if added:
            F |= added
            changed = True
            if F & R_cat:
                return F, True
    return F, bool(F & R_cat)


def soup_audit(walls, mass_n, monitor, W, H, allow_water_floor):
    starts = water_indices(mass_n, walls)
    R_cat = bound.reverse_reachable(walls, monitor, W, H, bound.forward_moves_catwalk)
    F, meets = cell_graph_closure(
        walls, starts, R_cat, W, H, allow_water_floor=allow_water_floor,
    )
    return {
        "n_water": len(starts),
        "F_size": len(F),
        "meets_R_catwalk": meets,
        "allow_water_floor": allow_water_floor,
    }


def evaluate_f3(
    walls, mass, monitor, W, H, theta, dx=None, crest_y=None, audit_soups=False,
):
    mass_n = normalize_unit_occupancy(mass, walls)
    n_water = unit_water_count(mass_n, walls)
    layers = bound.evaluate_layers(
        walls, mass_n, monitor, W, H, theta, dx=dx, crest_y=crest_y,
    )
    iso = isolation_verdict(layers, n_water, theta)
    full_soup = None
    wall_soup = None
    if (
        audit_soups
        and n_water >= 2
        and layers["A"]["verdict"] == "UNRESOLVED"
    ):
        full_soup = soup_audit(walls, mass_n, monitor, W, H, True)
        wall_soup = soup_audit(walls, mass_n, monitor, W, H, False)
    official, reason = official_static_verdict_f3(layers, iso)
    return {
        "normalized_mass": mass_n,
        "n_water": n_water,
        "A": layers["A"],
        "B_refuted": layers["B"],
        "isolation": iso,
        "full_soup": full_soup,
        "wall_soup": wall_soup,
        "failed_gap_adjacent": layers["failed_gap_adjacent"],
        "stats": layers["stats"],
        "static": official,
        "static_reason": reason,
        "layers_raw": layers,
    }


def official_static_verdict_f3(layers, iso):
    """A first; isolation NO; never B sill_need; never a V>=2 cell-graph NO."""
    if layers["A"]["verdict"] == "CERTIFIED_YES":
        return "CERTIFIED_YES", "A:" + layers["A"]["reason"]
    if layers["A"]["verdict"] == "CERTIFIED_NO":
        return "CERTIFIED_NO", "A:" + layers["A"]["reason"]
    if iso["verdict"] == "CERTIFIED_NO":
        return "CERTIFIED_NO", "ISO:" + iso["reason"]
    return "UNRESOLVED", "ISO:" + iso["reason"]
