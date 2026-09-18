"""Complete / constructive class-T search for the horizon-pay ledges.

Same occupancy-count graph as token_aware.py. A legal T-path into
R_catwalk is MEETS (what a complete search would find). Exhaustion of
the monotonic right/down subgraph is recorded separately and is not
full-T exhaustion.
"""
from __future__ import annotations

from collections import deque

from f2_import import bound
from token_aware import token_dests, token_aware_search


class WitnessFail(Exception):
    pass


def _idx(x, y, W):
    return y * W + x


def _xy(i, W):
    return i % W, i // W


def apply_move(walls, occ, src, dest, W, H):
    if dest not in token_dests(walls, occ, src, W, H):
        return None
    nxt = set(occ)
    nxt.remove(src)
    nxt.add(dest)
    return nxt


def occupy_cell(walls, occ, x, y, W, H, path, R_cat, steps_left=400):
    """Walk some token on row y rightward until (x,y) is occupied."""
    target = _idx(x, y, W)
    if target in occ:
        return occ, bool(occ & R_cat)
    if steps_left <= 0:
        raise WitnessFail("occupy_cell budget")
    if bound.is_wall(walls, x, y, W, H):
        raise WitnessFail(f"target wall {(x, y)}")
    # Rightmost token on this row to the left of x.
    left = [
        i for i in occ
        if i // W == y and i % W < x
    ]
    if not left:
        raise WitnessFail(f"no token left of {(x, y)} on row")
    src = max(left)
    sx = src % W
    dest = _idx(sx + 1, y, W)
    nxt = apply_move(walls, occ, src, dest, W, H)
    if nxt is None:
        # Blocked: move the occupant of dest further right first.
        if dest in occ:
            occ, met = occupy_cell(
                walls, occ, sx + 2, y, W, H, path, R_cat, steps_left - 1,
            )
            if met:
                return occ, True
            return occupy_cell(
                walls, occ, x, y, W, H, path, R_cat, steps_left - 1,
            )
        raise WitnessFail(f"cannot step {(_xy(src, W))} -> {(sx + 1, y)}")
    path.append((_xy(src, W), (sx + 1, y)))
    occ = nxt
    if occ & R_cat:
        return occ, True
    return occupy_cell(walls, occ, x, y, W, H, path, R_cat, steps_left - 1)


def drop_floor(walls, occ, x, y, W, H, path, R_cat):
    """Move a wall-or-token-supported token at (x-1, y) to (x, y+1)."""
    src = _idx(x - 1, y, W)
    dest = _idx(x, y + 1, W)
    if src not in occ:
        raise WitnessFail(f"no token at {(x - 1, y)} for drop")
    nxt = apply_move(walls, occ, src, dest, W, H)
    if nxt is None:
        raise WitnessFail(f"illegal drop {(x - 1, y)} -> {(x, y + 1)}")
    path.append(((x - 1, y), (x, y + 1)))
    occ = nxt
    return occ, bool(occ & R_cat)


def splash_right(walls, occ, x, y, W, H, path, R_cat):
    """Move token at (x, y) to (x+1, y)."""
    src = _idx(x, y, W)
    dest = _idx(x + 1, y, W)
    if src not in occ:
        raise WitnessFail(f"no token at {(x, y)} for splash")
    nxt = apply_move(walls, occ, src, dest, W, H)
    if nxt is None:
        raise WitnessFail(f"illegal splash {(x, y)} -> {(x + 1, y)}")
    path.append(((x, y), (x + 1, y)))
    occ = nxt
    return occ, bool(occ & R_cat)


def injection_witness(walls, starts, R_cat, W, H, tip_x, row_y, gap_x):
    """Bucket-brigade from a wall-supported row into the gap column.

    tip_x is the last wall-supported x on row_y. Tokens start on that row.
    """
    occ = set(starts)
    path = []
    if occ & R_cat:
        return {
            "meets_R_catwalk": True,
            "exhausted": False,
            "method": "start",
            "witness_len": 0,
            "path": [],
        }
    try:
        occ, met = occupy_cell(walls, occ, tip_x, row_y, W, H, path, R_cat)
        if met:
            return _ok(path, "pack_tip")
        # For each air column tip_x+1 .. gap_x-1, plant a floor then a walker.
        for col in range(tip_x + 1, gap_x):
            occ, met = drop_floor(walls, occ, col, row_y, W, H, path, R_cat)
            if met:
                return _ok(path, "drop")
            occ, met = occupy_cell(
                walls, occ, col - 1, row_y, W, H, path, R_cat,
            )
            if met:
                return _ok(path, "repack")
            occ, met = splash_right(
                walls, occ, col - 1, row_y, W, H, path, R_cat,
            )
            if met:
                return _ok(path, "walk")
        # Last splash from (gap_x-1, row_y) into the gap, if not already.
        if _idx(gap_x, row_y, W) not in occ:
            occ, met = splash_right(
                walls, occ, gap_x - 1, row_y, W, H, path, R_cat,
            )
            if met:
                return _ok(path, "gap")
        if occ & R_cat:
            return _ok(path, "gap")
        return {
            "meets_R_catwalk": False,
            "exhausted": False,
            "method": "constructor_miss",
            "witness_len": len(path),
            "path": path[-8:],
            "final_max_x": max(i % W for i in occ),
        }
    except WitnessFail as e:
        return {
            "meets_R_catwalk": False,
            "exhausted": False,
            "method": "constructor_fail",
            "error": str(e),
            "witness_len": len(path),
            "path": path[-8:],
        }


def _ok(path, stage):
    return {
        "meets_R_catwalk": True,
        "exhausted": False,
        "method": "constructor:" + stage,
        "witness_len": len(path),
        "path": path,
    }


def monotonic_t_search(walls, starts, R_cat, W, H, max_states=2_000_000):
    """T-subgraph: only right or down moves. MEETS is sound for full T."""
    start = frozenset(starts)
    if start & R_cat:
        return {
            "meets_R_catwalk": True,
            "exhausted": True,
            "method": "monotonic_start",
            "states_expanded": 0,
            "states_seen": 1,
            "witness_depth": 0,
        }
    seen = {start}
    q = deque([(start, 0)])
    expanded = 0
    while q:
        if expanded >= max_states:
            return {
                "meets_R_catwalk": False,
                "exhausted": False,
                "method": "monotonic_budget",
                "states_expanded": expanded,
                "states_seen": len(seen),
            }
        cur, depth = q.popleft()
        expanded += 1
        occ = set(cur)
        for src in cur:
            sx, sy = src % W, src // W
            for dest in token_dests(walls, occ, src, W, H):
                dx, dy = dest % W, dest // W
                if dx < sx or (dx == sx and dy < sy):
                    continue
                if dx == sx and dy == sy:
                    continue
                nxt_set = occ - {src}
                nxt_set.add(dest)
                nxt = frozenset(nxt_set)
                if nxt in seen:
                    continue
                if nxt & R_cat:
                    return {
                        "meets_R_catwalk": True,
                        "exhausted": False,
                        "method": "monotonic_meet",
                        "states_expanded": expanded,
                        "states_seen": len(seen) + 1,
                        "witness_depth": depth + 1,
                    }
                seen.add(nxt)
                q.append((nxt, depth + 1))
    return {
        "meets_R_catwalk": False,
        "exhausted": True,
        "method": "monotonic_exhaust",
        "states_expanded": expanded,
        "states_seen": len(seen),
        "note": "monotonic subgraph only; not full-T exhaustion",
    }


def replay_path(walls, starts, path, R_cat, W, H):
    """Recompute each constructor step on the T graph. Admission check."""
    occ = set(starts)
    for k, (src_xy, dest_xy) in enumerate(path):
        src = _idx(src_xy[0], src_xy[1], W)
        dest = _idx(dest_xy[0], dest_xy[1], W)
        if src not in occ:
            return False, f"step {k}: src {src_xy} empty"
        nxt = apply_move(walls, occ, src, dest, W, H)
        if nxt is None:
            return False, f"step {k}: illegal {src_xy} -> {dest_xy}"
        occ = nxt
    return True, {
        "final_meets": bool(occ & R_cat),
        "final_cells": sorted((_xy(i, W) for i in occ)),
    }


def complete_t(walls, mass_n, monitor, W, H, tip_x, row_y, gap_x=32):
    starts = [
        i for i, m in enumerate(mass_n)
        if m > 0 and not walls[i]
    ]
    R_cat = bound.reverse_reachable(
        walls, monitor, W, H, bound.forward_moves_catwalk,
    )
    wit = injection_witness(
        walls, starts, R_cat, W, H, tip_x, row_y, gap_x,
    )
    if wit["meets_R_catwalk"] and wit.get("path") is not None:
        ok, detail = replay_path(
            walls, starts, wit["path"], R_cat, W, H,
        )
        wit["replay_ok"] = ok
        wit["replay_detail"] = detail
        if not ok or not (isinstance(detail, dict) and detail.get("final_meets")):
            wit["meets_R_catwalk"] = False
            wit["method"] = "constructor_replay_fail"
        else:
            return wit
    elif wit["meets_R_catwalk"]:
        return wit
    mono = monotonic_t_search(walls, starts, R_cat, W, H)
    if mono["meets_R_catwalk"]:
        return mono
    # Last resort: full T with a large budget (still may cap).
    full = token_aware_search(
        walls, starts, R_cat, W, H, max_states=500_000,
    )
    full["method"] = "full_T_" + (full.get("reason") or "done")
    return full
