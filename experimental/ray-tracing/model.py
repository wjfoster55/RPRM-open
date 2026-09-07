"""EXPERIMENTAL: exact finite first-hit cache, not a radiometric renderer."""
from fractions import Fraction
import json

SCHEMA = "finite-grid-rays/v1"
CELLS = tuple((x, y) for x in range(1, 5) for y in range(6))
RAYS = tuple((a, b) for a in range(6) for b in range(6))


def cell(value):
    if type(value) not in (tuple, list) or len(value) != 2 or any(type(x) is not int for x in value):
        raise ValueError("cell must contain two plain integers")
    value = tuple(value)
    if value not in CELLS:
        raise ValueError("cell outside the 24-cell carrier")
    return value


def mask(values):
    if type(values) not in (tuple, list) or len(values) > 3:
        raise ValueError("scene must be a list/tuple of at most three cells")
    result = tuple(cell(x) for x in values)
    if len(set(result)) != len(result):
        raise ValueError("duplicate opaque cell")
    return tuple(sorted(result))


def intersection(ray, square):
    """Closed unit square centered at square; p(t)=(0,a)+t*(5,b-a)."""
    if type(ray) not in (tuple, list) or len(ray) != 2 or any(type(x) is not int or not 0 <= x < 6 for x in ray):
        raise ValueError("ray must name two endpoint heights in 0..5")
    square = cell(square)
    lo, hi = Fraction(0), Fraction(1)
    for origin, delta, center in ((0, 5, square[0]), (ray[0], ray[1]-ray[0], square[1])):
        low, high = Fraction(2*center-1, 2), Fraction(2*center+1, 2)
        if delta == 0:
            if not low <= origin <= high:
                return None
        else:
            a, b = (low-origin)/delta, (high-origin)/delta
            lo, hi = max(lo, min(a, b)), min(hi, max(a, b))
            if lo > hi:
                return None
    return lo, hi


# Geometry is fixed by this context. This one-time construction costs 864
# ray/cell intersection calls; this includes both hit and miss candidates.
_CONTACT = {(r, c): intersection(r, c) for r in RAYS for c in CELLS}
_INCIDENCE = {c: tuple(r for r in RAYS if _CONTACT[r, c] is not None) for c in CELLS}


def _fraction(x):
    return [x.numerator, x.denominator]


def _row(ray, opaque):
    hits = []
    for c in opaque:
        contact = _CONTACT[ray, c]
        if contact is not None:
            hits.append((c, contact))
    hits.sort(key=lambda pair: (pair[1][0], pair[1][1], pair[0]))
    return {"ray": list(ray), "hits": [{"cell": list(c), "entry": _fraction(v[0]), "exit": _fraction(v[1])} for c, v in hits]}


def compile_scene(opaque):
    """Rebuild all rows from admitted geometry; never trust supplied cache rows."""
    opaque = mask(opaque)
    return {"schema": SCHEMA, "opaque": [list(c) for c in opaque], "rows": [_row(r, opaque) for r in RAYS]}


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def validate_snapshot(snapshot):
    """Strict JSON-type equality plus full geometric recomputation at ingress."""
    if type(snapshot) is not dict or set(snapshot) != {"schema", "opaque", "rows"}:
        raise ValueError("snapshot keys must be schema, opaque and rows")
    expected = compile_scene(snapshot["opaque"])
    # Canonical JSON separates true from 1 and 1.0 from 1; it is not a proof
    # of geometry. The independently recomputed expected rows supply that test.
    try:
        same = _json(snapshot) == _json(expected)
    except (ValueError, TypeError) as exc:
        raise ValueError("snapshot must be finite JSON data") from exc
    if not same:
        raise ValueError("snapshot disagrees with canonical scene geometry")
    return expected


def first_hit(row):
    """Complete nearest-entry identity fiber, including all exact ties."""
    hits = row["hits"]
    first = [] if not hits else [h["cell"] for h in hits if h["entry"] == hits[0]["entry"]]
    return {"disposition": "NONE" if not first else "ONE" if len(first) == 1 else "MANY", "cells": first}


def receiver(snapshot):
    state = validate_snapshot(snapshot)
    return [{"ray": row["ray"], **first_hit(row)} for row in state["rows"]]


def update(snapshot, operation, at, target=None, *, claimed_dirty=None):
    """TOGGLE <=3 cells; MOVE only from a singleton. Full ingress is charged."""
    if type(operation) is not str or operation not in ("TOGGLE", "MOVE"):
        raise ValueError("operation must be TOGGLE or MOVE")
    if type(snapshot) is not dict or "opaque" not in snapshot:
        raise ValueError("missing scene")
    old_mask = mask(snapshot["opaque"])
    at = cell(at)
    if operation == "MOVE":
        if len(old_mask) != 1 or old_mask[0] != at:
            raise ValueError("MOVE requires exactly one cell, equal to at")
        target = cell(target)
        if at == target:
            raise ValueError("MOVE requires a distinct target")
        new_mask = (target,)
    else:
        if target is not None:
            raise ValueError("TOGGLE has no target port")
        new_mask = mask([c for c in old_mask if c != at] if at in old_mask else [*old_mask, at])
    changed = tuple(sorted(set(old_mask) ^ set(new_mask)))
    dirty = tuple(sorted({r for c in changed for r in _INCIDENCE[c]}))
    if claimed_dirty is not None and _json(claimed_dirty) != _json([list(r) for r in dirty]):
        raise ValueError("dirty declaration must equal the canonical affected-ray list")
    old = validate_snapshot(snapshot)
    rows = [_row(r, new_mask) if r in dirty else old["rows"][i] for i, r in enumerate(RAYS)]
    new = {"schema": SCHEMA, "opaque": [list(c) for c in sorted(new_mask)], "rows": rows}
    return {"snapshot": new, "receipt": {
        "operation": operation, "changed_cells": [list(c) for c in changed], "dirty_rays": [list(r) for r in dirty],
        "cost_units": "logical table probes and materialized records, not time",
        "geometry_construction_intersections_once": 864,
        "incidence_construction_cache_probes_once": 864,
        "ingress_cache_probes": 36*len(old_mask), "ingress_rows_materialized": 36,
        "patch_cache_probes": len(dirty)*len(new_mask), "patch_rows_materialized": len(dirty),
        "full_baseline_cache_probes": 36*len(new_mask), "output_row_references": 36,
        "serialized_snapshot_utf8_bytes": len(_json(new).encode("utf-8")),
        "excluded_costs": ["Python allocation and equality", "sorting", "serialization time", "one-time incidence construction time"]}}


def load_snapshot(text):
    """Bounded strict JSON ingress. No paths, labels or arbitrary metadata."""
    if type(text) is not str or len(text.encode("utf-8")) > 131072:
        raise ValueError("snapshot text must be at most 128 KiB")
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result
    def nonfinite(_):
        raise ValueError("nonfinite JSON number")
    return validate_snapshot(json.loads(text, object_pairs_hook=unique, parse_constant=nonfinite))
