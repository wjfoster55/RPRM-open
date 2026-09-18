"""Token-aware occupancy-count certificate (class T).

Not official static routing. Not Layer B. Occupancy-ignoring soups stay
failed. This search tracks exactly n occupied cells.

NO only on exhaustion inside the frozen budget (NULLS.md). Meeting
R_catwalk, hitting the cap, or n > MAX_N is UNRESOLVED. Never YES.
"""
from __future__ import annotations

from collections import deque
import heapq

from f2_import import bound

SPLASH = ((-1, 1), (1, 1), (-1, 0), (1, 0))

MAX_N = 32
MAX_STATES = 50000


def _frontier_key(walls, occ, W, H):
    """Prefer pushing supported occupancy right. Witness hunt only."""
    max_x = -1
    max_sup = -1
    for i in occ:
        x, y = i % W, i // W
        if x > max_x:
            max_x = x
        by = y + 1
        supported = bound.wall_supported(walls, x, y, W, H)
        if not supported and bound.in_bounds(x, by, W, H):
            if (x + by * W) in occ:
                supported = True
        if supported and x > max_sup:
            max_sup = x
    return (-max_sup, -max_x)


def token_dests(walls, occ, src, W, H):
    """Occupancy-respecting dests for one token. Fall if empty below;
    else splash. Matches stepB's fall-vs-splash split, not its scan order.
    """
    sx, sy = src % W, src // W
    if bound.is_wall(walls, sx, sy, W, H):
        return
    by = sy + 1
    can_fall = (
        bound.in_bounds(sx, by, W, H)
        and not bound.is_wall(walls, sx, by, W, H)
        and (sx + by * W) not in occ
    )
    if can_fall:
        for k in range(1, bound.MAX_FALL + 1):
            ny = sy + k
            if not bound.in_bounds(sx, ny, W, H) or bound.is_wall(
                walls, sx, ny, W, H,
            ):
                return
            dest = sx + ny * W
            if dest in occ:
                return
            yield dest
        return
    for dx, dy in SPLASH:
        nx, ny = sx + dx, sy + dy
        if not bound.in_bounds(nx, ny, W, H) or bound.is_wall(
            walls, nx, ny, W, H,
        ):
            continue
        dest = nx + ny * W
        if dest in occ:
            continue
        yield dest


def token_aware_search(walls, starts, R_cat, W, H, max_states=MAX_STATES):
    """Search n-token occupancy configs from the actual start.

    n<=4 uses complete BFS (exhaustion can be a NO). n>4 uses best-first
    toward a supported right frontier; the cap is not a NO.
    """
    n = len(starts)
    out = {
        "n_water": n,
        "max_n": MAX_N,
        "max_states": max_states,
        "meets_R_catwalk": False,
        "exhausted": False,
        "budget_hit": False,
        "skipped": False,
        "skip_reason": None,
        "states_expanded": 0,
        "states_seen": 0,
        "witness_depth": None,
        "verdict": "UNRESOLVED",
        "reason": None,
    }
    if n < 2:
        out["skipped"] = True
        out["skip_reason"] = "n_lt_2_use_isolation"
        out["reason"] = "n_lt_2_use_isolation"
        return out
    if n > MAX_N:
        out["skipped"] = True
        out["skip_reason"] = "n_gt_MAX_N"
        out["reason"] = "n_gt_MAX_N"
        return out
    start = frozenset(starts)
    if start & R_cat:
        out["meets_R_catwalk"] = True
        out["witness_depth"] = 0
        out["states_seen"] = 1
        out["reason"] = "start_on_R_catwalk"
        return out

    seen = {start}
    expanded = 0
    if n <= 4:
        q = deque([(start, 0)])
        while q:
            if expanded >= max_states:
                out["budget_hit"] = True
                out["states_expanded"] = expanded
                out["states_seen"] = len(seen)
                out["reason"] = "budget_hit"
                return out
            cur, depth = q.popleft()
            expanded += 1
            occ = set(cur)
            for src in cur:
                for dest in token_dests(walls, occ, src, W, H):
                    nxt_set = occ - {src}
                    nxt_set.add(dest)
                    nxt = frozenset(nxt_set)
                    if nxt in seen:
                        continue
                    if nxt & R_cat:
                        out["meets_R_catwalk"] = True
                        out["witness_depth"] = depth + 1
                        out["states_expanded"] = expanded
                        out["states_seen"] = len(seen) + 1
                        out["reason"] = "meets_R_catwalk"
                        return out
                    seen.add(nxt)
                    q.append((nxt, depth + 1))
        out["exhausted"] = True
        out["states_expanded"] = expanded
        out["states_seen"] = len(seen)
        out["verdict"] = "CERTIFIED_NO"
        out["reason"] = "token_occ_exhausted_no_R_catwalk"
        return out

    heap = []
    tie = 0
    fk = _frontier_key(walls, start, W, H)
    heapq.heappush(heap, (fk[0], fk[1], 0, tie, start))
    while heap:
        if expanded >= max_states:
            out["budget_hit"] = True
            out["states_expanded"] = expanded
            out["states_seen"] = len(seen)
            out["search"] = "best_first"
            out["reason"] = "budget_hit"
            return out
        _a, _b, depth, _, cur = heapq.heappop(heap)
        expanded += 1
        occ = set(cur)
        for src in cur:
            for dest in token_dests(walls, occ, src, W, H):
                nxt_set = occ - {src}
                nxt_set.add(dest)
                nxt = frozenset(nxt_set)
                if nxt in seen:
                    continue
                if nxt & R_cat:
                    out["meets_R_catwalk"] = True
                    out["witness_depth"] = depth + 1
                    out["states_expanded"] = expanded
                    out["states_seen"] = len(seen) + 1
                    out["search"] = "best_first"
                    out["reason"] = "meets_R_catwalk"
                    return out
                seen.add(nxt)
                tie += 1
                fk = _frontier_key(walls, nxt, W, H)
                heapq.heappush(
                    heap, (fk[0], fk[1], depth + 1, tie, nxt),
                )
    out["exhausted"] = True
    out["states_expanded"] = expanded
    out["states_seen"] = len(seen)
    out["search"] = "best_first"
    out["verdict"] = "CERTIFIED_NO"
    out["reason"] = "token_occ_exhausted_no_R_catwalk"
    return out


def token_aware_audit(walls, mass_n, monitor, W, H, max_states=MAX_STATES):
    starts = [
        i for i, m in enumerate(mass_n)
        if m > 0 and not walls[i]
    ]
    R_cat = bound.reverse_reachable(
        walls, monitor, W, H, bound.forward_moves_catwalk,
    )
    return token_aware_search(walls, starts, R_cat, W, H, max_states=max_states)
