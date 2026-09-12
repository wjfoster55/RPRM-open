#!/usr/bin/env python3
"""Operation-aware Prestige envelope for RCF01 review-repair successor.

Successor of frozen RCF01-envelope-1 (original bytes retained in
experiments/core_recovery_bridge_01/). This copy adds composition recipes and
output-class handling. It is not a retroactive protocol rewrite.

Three separately typed state families share one inspectable envelope API.
This is a bounded exact prototype, not a full Prestige One lifecycle and not
F5 arithmetic. Standard library plus the adjacent rprm.core fiber/quotient
helpers. Does not import the starter check_bridge.py.
"""
from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import FrozenSet, Mapping, Optional, Sequence, Tuple


def _find_repo() -> Path:
    here = Path(__file__).resolve().parent
    cursor = here
    for _ in range(8):
        if (cursor / "rprm" / "core.py").is_file():
            return cursor
        if cursor.parent == cursor:
            break
        cursor = cursor.parent
    raise RuntimeError("rprm.core was not packaged adjacent to this envelope")


_REPO = _find_repo()
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from rprm.core import (
    AdmissionError,
    Fiber,
    Port,
    Relation,
    Sort,
    Value,
    deterministic_quotient,
    require,
    solve,
)

N_SITES = 8
B2 = tuple(range(7))
OMITTED = 7
CUBE_CARRIER = "BOOL_CUBE_Q_n3"
CUBE_FRAME = "mask_lsb_h_then_x_then_y"
INHERITED_ENVELOPE_VERSION = "RCF01-envelope-1"
ENVELOPE_VERSION = "RCF01-envelope-1-r1"
DOUBLE_STAMP_CARRIER = "DOUBLE_STAMP_A5_B6_C7"
DOUBLE_STAMP_FRAME = "donor_labels_a0a1b0b1_c_c0c1_z"
FIVING_CARRIER = "C10_DISPLAY"
STRONG_FIVING_CARRIER = "Z_x_C2_x_C5"


def as_frac(value) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise AdmissionError("Cube entries must be exact int or Fraction")


def frac_tuple(values: Sequence) -> Tuple[Fraction, ...]:
    require(len(values) == N_SITES, "This cube carrier has exactly eight sites")
    return tuple(as_frac(v) for v in values)


def submasks(mask: int):
    t = mask
    while True:
        yield t
        if t == 0:
            return
        t = (t - 1) & mask


def mobius(table: Sequence) -> Tuple[Fraction, ...]:
    """Independent submask walk; not the starter list-comprehension path."""
    f = frac_tuple(table)
    out = []
    for s in range(N_SITES):
        acc = Fraction(0)
        for t in submasks(s):
            sign = -1 if ((s.bit_count() - t.bit_count()) & 1) else 1
            acc += sign * f[t]
        out.append(acc)
    return tuple(out)


def zeta(coeffs: Sequence) -> Tuple[Fraction, ...]:
    c = frac_tuple(coeffs)
    out = []
    for s in range(N_SITES):
        acc = Fraction(0)
        for t in submasks(s):
            acc += c[t]
        out.append(acc)
    return tuple(out)


def compact_from_table(table: Sequence) -> Tuple[Fraction, ...]:
    return mobius(table)[:7]


def degree_from_coeffs(coeffs: Sequence) -> int:
    padded = tuple(as_frac(v) for v in coeffs)
    if len(padded) < N_SITES:
        padded = padded + (Fraction(0),) * (N_SITES - len(padded))
    require(len(padded) == N_SITES, "degree_from_coeffs needs eight coefficients")
    degree = 0
    for site, coeff in enumerate(padded):
        if coeff != 0:
            degree = max(degree, site.bit_count())
    return degree


def eval_retained(coeffs7: Sequence, site: int) -> Fraction:
    require(site in B2, "Retained evaluation may not read the omitted site")
    c = tuple(as_frac(v) for v in coeffs7)
    require(len(c) == 7, "Seven retained coefficients required")
    acc = Fraction(0)
    for t in submasks(site):
        acc += c[t]
    return acc


def values_on_b2(coeffs7: Sequence) -> Tuple[Fraction, ...]:
    return tuple(eval_retained(coeffs7, s) for s in B2)


def compact_from_b2(values7: Sequence) -> Tuple[Fraction, ...]:
    """Mobius using only B2 values; omitted coefficient is unused."""
    require(len(values7) == 7, "B2 has seven sites")
    padded = tuple(as_frac(v) for v in values7) + (Fraction(0),)
    return mobius(padded)[:7]


def compact_add(a: Sequence, b: Sequence) -> Tuple[Fraction, ...]:
    require(len(a) == len(b) == 7, "Seven retained coefficients required")
    return tuple(as_frac(x) + as_frac(y) for x, y in zip(a, b))


def compact_mul_from_sites(a: Sequence, b: Sequence) -> Tuple[Fraction, ...]:
    """Independent of monomial-union multiplication: multiply on B2, then Mobius."""
    va, vb = values_on_b2(a), values_on_b2(b)
    product = tuple(x * y for x, y in zip(va, vb))
    return compact_from_b2(product)


def input_maps() -> dict[str, Tuple[int, ...]]:
    maps = {"identity": tuple(range(N_SITES))}
    for i, label in enumerate(("h", "x", "y")):
        maps[f"clamp_{label}_0"] = tuple(s & ~(1 << i) for s in range(N_SITES))
        maps[f"clamp_{label}_1"] = tuple(s | (1 << i) for s in range(N_SITES))
        maps[f"flip_{label}"] = tuple(s ^ (1 << i) for s in range(N_SITES))
    return maps


def map_closes_b2(mapping: Sequence[int]) -> bool:
    return all(mapping[s] in B2 for s in B2)


def pullback_table(table: Sequence, mapping: Sequence[int]) -> Tuple[Fraction, ...]:
    f = frac_tuple(table)
    require(len(mapping) == N_SITES, "Map must cover eight sites")
    require(all(type(x) is int and 0 <= x < N_SITES for x in mapping), "Map leaves the cube")
    return tuple(f[mapping[s]] for s in range(N_SITES))


def fiving_display(d: int) -> int:
    require(type(d) is int and 0 <= d < 10, "Finite fiving display is C10")
    return (d + 5) % 10


def fiving_display_wrong(d: int, step: int) -> int:
    require(type(d) is int and 0 <= d < 10, "Finite display is C10")
    return (d + step) % 10


def encode_display(h: int, r: int) -> int:
    require(h in (0, 1) and r in range(5), "Display chart is d=5h+r")
    return 5 * h + r


def adapter_A(h: int, x: int, y: int, r: int) -> Tuple[int, int, int]:
    return (encode_display(h, r), x, y)


def strong_fiving(w: int, h: int, r: int) -> Tuple[int, int, int]:
    require(h in (0, 1) and r in range(5) and type(w) is int, "Strong lift n=10w+5h+r")
    return (w + h, 1 - h, r)


def strong_encode(w: int, h: int, r: int) -> int:
    return 10 * w + 5 * h + r


# --- Double-Stamp: source-declared graphs, not a count shortcut -----------------

DONOR_LABELS = {
    "a_arms": ("a0", "a1"),
    "b_arms": ("b0", "b1"),
    "shared_center": "c",
    "split_centers": ("c0", "c1"),
    "midpoint": "z",
}

STAGE_TYPES = {
    "A5": {"dwell_allowed": True, "type": "STATE"},
    "B6": {"dwell_allowed": False, "type": "EVENT"},
    "C7": {"dwell_allowed": True, "type": "STATE"},
}


def _edge(u: str, v: str) -> FrozenSet[str]:
    require(u != v, "Simple graphs forbid loops")
    return frozenset((u, v))


def graph_a5() -> Tuple[FrozenSet[str], FrozenSet[FrozenSet[str]]]:
    c = DONOR_LABELS["shared_center"]
    arms = DONOR_LABELS["a_arms"] + DONOR_LABELS["b_arms"]
    vertices = frozenset((c,) + arms)
    edges = frozenset(_edge(c, arm) for arm in arms)
    return vertices, edges


def graph_b6() -> Tuple[FrozenSet[str], FrozenSet[FrozenSet[str]]]:
    c0, c1 = DONOR_LABELS["split_centers"]
    a0, a1 = DONOR_LABELS["a_arms"]
    b0, b1 = DONOR_LABELS["b_arms"]
    vertices = frozenset((c0, c1, a0, a1, b0, b1))
    edges = frozenset((_edge(c0, a0), _edge(c0, a1), _edge(c1, b0), _edge(c1, b1), _edge(c0, c1)))
    return vertices, edges


def graph_c7() -> Tuple[FrozenSet[str], FrozenSet[FrozenSet[str]]]:
    vertices, edges = graph_b6()
    z = DONOR_LABELS["midpoint"]
    c0, c1 = DONOR_LABELS["split_centers"]
    vertices = frozenset(set(vertices) | {z})
    edges = frozenset((set(edges) - {_edge(c0, c1)}) | {_edge(c0, z), _edge(z, c1)})
    return vertices, edges


def stamp_swap(name: str) -> str:
    mapping = {
        "a0": "b0", "b0": "a0", "a1": "b1", "b1": "a1",
        "c": "c", "c0": "c1", "c1": "c0", "z": "z",
    }
    require(name in mapping, "Unknown Double-Stamp vertex")
    return mapping[name]


def graph_summary(vertices: FrozenSet[str], edges: FrozenSet[FrozenSet[str]]) -> Tuple[int, int, int]:
    require(all(stamp_swap(stamp_swap(v)) == v for v in vertices), "Swap is not an involution")
    require(all(frozenset(stamp_swap(v) for v in e) in edges for e in edges), "Swap does not preserve edges")
    vorbits = {frozenset((v, stamp_swap(v))) for v in vertices}
    eorbits = {frozenset((e, frozenset(stamp_swap(v) for v in e))) for e in edges}
    inverted = sum(
        1 for e in edges
        if frozenset(stamp_swap(v) for v in e) == e and all(stamp_swap(v) != v for v in e)
    )
    return (len(vorbits), len(eorbits), inverted)


GRAPHS = {"A5": graph_a5, "B6": graph_b6, "C7": graph_c7}


# --- Envelope -----------------------------------------------------------------

@dataclass
class Meter:
    hot_ops: int = 0
    cold_reads: int = 0
    constructions: int = 0
    checks: int = 0
    storage_bytes: int = 0
    reopenings: int = 0
    invalidations: int = 0


METER = Meter()


@dataclass(frozen=True)
class Result:
    disposition: str
    status: str
    value: object = None
    witness: object = None

    def __post_init__(self):
        require(self.disposition in ("NONE", "ONE", "MANY", "OPEN"), "Unknown fiber disposition")
        require(self.status in ("EXACT", "REOPEN_REQUIRED", "UNRESOLVED", "UNSUPPORTED", "INVALID_DEPENDENCY"),
                "Unknown operational status")


@dataclass(frozen=True)
class Envelope:
    family: str
    visible_unit_label: str
    retained: tuple
    contract: FrozenSet[str]
    carrier_id: str
    frame_id: str
    version: str
    cold_route: Optional[str]
    cold_sha256: Optional[str]
    history: tuple = ()
    stage: Optional[str] = None
    recipe: Optional[tuple] = None
    degree_bound: Optional[int] = None

    def __post_init__(self):
        require(self.family in ("rational_cube", "boolean_cube", "double_stamp", "fiving_display", "fiving_strong"),
                "Unknown state family")
        require(type(self.visible_unit_label) is str and self.visible_unit_label, "Visible label required")
        require(type(self.contract) is frozenset, "Contract must be a frozenset of operation names")
        require(self.version == ENVELOPE_VERSION, "Envelope version mismatch")


def _canonical_artifact(payload: Mapping) -> bytes:
    return (json.dumps(payload, sort_keys=True, ensure_ascii=True, indent=2) + "\n").encode("utf-8")


def write_cold_artifact(path: Path, payload: Mapping) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _canonical_artifact(payload)
    if path.exists():
        raise AdmissionError("Cold artifact path already exists; use a fresh name")
    path.write_bytes(data)
    METER.storage_bytes += len(data)
    METER.constructions += 1
    return hashlib.sha256(data).hexdigest()


def read_cold_artifact(path: Path, expected_sha: str, expected: Mapping) -> dict:
    METER.cold_reads += 1
    METER.reopenings += 1
    if not path.exists():
        METER.invalidations += 1
        raise FileNotFoundError(str(path))
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected_sha:
        METER.invalidations += 1
        raise ValueError("cold_sha256 mismatch")
    payload = json.loads(data.decode("utf-8"))
    for key in ("carrier_id", "frame_id", "version", "family"):
        if payload.get(key) != expected[key]:
            METER.invalidations += 1
            raise ValueError(f"cold dependency mismatch: {key}")
    return payload


def promote_cube(table: Sequence, *, label: str, contract: FrozenSet[str],
                 cold_dir: Optional[Path], name: str,
                 history: tuple = (), family: str = "rational_cube") -> Envelope:
    METER.constructions += 1
    full = mobius(table)
    retained = full[:7]
    degree = degree_from_coeffs(full)
    route = None
    digest = None
    if cold_dir is not None:
        payload = {
            "carrier_id": CUBE_CARRIER,
            "frame_id": CUBE_FRAME,
            "version": ENVELOPE_VERSION,
            "family": family,
            "full_coeffs": [str(c) for c in full],
            "full_table": [str(v) for v in frac_tuple(table)],
            "history": list(history),
        }
        path = cold_dir / f"{name}.json"
        digest = write_cold_artifact(path, payload)
        route = str(path)
    return Envelope(
        family=family,
        visible_unit_label=label,
        retained=retained,
        contract=contract,
        carrier_id=CUBE_CARRIER,
        frame_id=CUBE_FRAME,
        version=ENVELOPE_VERSION,
        cold_route=route,
        cold_sha256=digest,
        history=history,
        recipe=None,
        degree_bound=degree,
    )


ARITH_CONTRACT = frozenset({
    "read_admitted", "add", "multiply", "clamp_h_0", "clamp_x_0", "clamp_y_0",
})
FLIP_CONTRACT = ARITH_CONTRACT | frozenset({"flip_h", "fiving_slice"})
FULL_CUBE_CONTRACT = FLIP_CONTRACT | frozenset({
    "clamp_h_1", "clamp_x_1", "clamp_y_1", "flip_x", "flip_y", "inspect_omitted", "reopen",
})
STAMP_CONTRACT = frozenset({"dwell", "split", "midpoint", "contract_restart"})
COORDINATE_BITS = {"h": 0, "x": 1, "y": 2}


def unit(axis: str, *, label: str = "one", contract: Optional[FrozenSet[str]] = None,
           cold_dir: Optional[Path] = None, name: Optional[str] = None,
           family: str = "rational_cube") -> Envelope:
    """Coordinate law 1_{axis=1} on the Boolean three-cube. Public prototype API."""
    require(axis in COORDINATE_BITS, "unit axis must be h, x, or y")
    bit = COORDINATE_BITS[axis]
    table = tuple((s >> bit) & 1 for s in range(N_SITES))
    if contract is None:
        contract = ARITH_CONTRACT
    return promote_cube(table, label=label, contract=contract, cold_dir=cold_dir,
                        name=name or f"unit_{axis}", family=family)


def _operand_spec(env: Envelope) -> Optional[tuple]:
    if env.recipe is not None:
        return env.recipe
    if env.cold_route is not None and env.cold_sha256 is not None:
        return ("cold", env.cold_route, env.cold_sha256, env.carrier_id,
                env.frame_id, env.version, env.family)
    return None


def _reopen_from_spec(spec: tuple) -> Result:
    kind = spec[0]
    if kind == "cold":
        _, route, digest, carrier_id, frame_id, version, family = spec
        try:
            payload = read_cold_artifact(
                Path(route), digest,
                {"carrier_id": carrier_id, "frame_id": frame_id,
                 "version": version, "family": family},
            )
        except FileNotFoundError:
            return Result("OPEN", "UNRESOLVED", witness="cold path missing")
        except ValueError as exc:
            return Result("NONE", "INVALID_DEPENDENCY", witness=str(exc))
        table = tuple(Fraction(v) for v in payload["full_table"])
        return Result("ONE", "EXACT", value=table, witness={"used_recipe": True, "leaf": "cold"})
    if kind in ("add", "multiply"):
        left = _reopen_from_spec(spec[1])
        if left.status != "EXACT":
            return left
        right = _reopen_from_spec(spec[2])
        if right.status != "EXACT":
            return right
        if kind == "add":
            table = tuple(x + y for x, y in zip(left.value, right.value))
        else:
            table = tuple(x * y for x, y in zip(left.value, right.value))
        return Result("ONE", "EXACT", value=table, witness={"used_recipe": True, "op": kind})
    if kind == "pullback":
        map_name, inner = spec[1], spec[2]
        maps = input_maps()
        if map_name not in maps:
            return Result("NONE", "UNSUPPORTED", witness=f"unknown map {map_name}")
        inner_table = _reopen_from_spec(inner)
        if inner_table.status != "EXACT":
            return inner_table
        table = pullback_table(inner_table.value, maps[map_name])
        return Result("ONE", "EXACT", value=table, witness={"used_recipe": True, "op": "pullback"})
    if kind == "pullback_sites":
        mapping, inner = spec[1], spec[2]
        inner_table = _reopen_from_spec(inner)
        if inner_table.status != "EXACT":
            return inner_table
        table = pullback_table(inner_table.value, mapping)
        return Result("ONE", "EXACT", value=table, witness={"used_recipe": True, "op": "pullback_sites"})
    return Result("NONE", "UNSUPPORTED", witness="unknown recipe kind")


def _compose_recipe(op: str, a: Envelope, b: Envelope) -> Optional[tuple]:
    left, right = _operand_spec(a), _operand_spec(b)
    if left is None or right is None:
        return None
    METER.constructions += 1
    return (op, left, right)


def _family_after_arith(a: Envelope, b: Envelope, retained: Sequence) -> str:
    values = values_on_b2(retained)
    if any(v not in (Fraction(0), Fraction(1)) for v in values):
        return "rational_cube"
    if a.family == "boolean_cube" and b.family == "boolean_cube":
        return "boolean_cube"
    return "rational_cube"


def _degree_after_mul(a: Envelope, b: Envelope) -> Optional[int]:
    if a.degree_bound is None or b.degree_bound is None:
        return None
    return min(3, a.degree_bound + b.degree_bound)


def _degree_after_add(a: Envelope, b: Envelope) -> Optional[int]:
    if a.degree_bound is None or b.degree_bound is None:
        return None
    return max(a.degree_bound, b.degree_bound)


def compatible(a: Envelope, b: Envelope) -> Optional[str]:
    if a.family != b.family:
        return "family"
    if a.carrier_id != b.carrier_id or a.frame_id != b.frame_id:
        return "frame"
    if a.version != b.version:
        return "version"
    return None


def read_admitted(env: Envelope) -> Result:
    METER.hot_ops += 1
    METER.checks += 1
    if env.family not in ("rational_cube", "boolean_cube"):
        return Result("NONE", "UNSUPPORTED", witness="not a cube family")
    if "read_admitted" not in env.contract:
        return Result("NONE", "UNSUPPORTED", witness="read_admitted not admitted")
    values = values_on_b2(env.retained)
    return Result("ONE", "EXACT", value=values)


def add_units(a: Envelope, b: Envelope) -> Result:
    METER.hot_ops += 1
    mismatch = compatible(a, b)
    if mismatch:
        return Result("NONE", "UNSUPPORTED", witness=mismatch)
    if "add" not in a.contract or "add" not in b.contract:
        return Result("NONE", "UNSUPPORTED", witness="add not admitted")
    retained = compact_add(a.retained, b.retained)
    recipe = _compose_recipe("add", a, b)
    family = _family_after_arith(a, b, retained)
    out = Envelope(
        family=family, visible_unit_label=a.visible_unit_label,
        retained=retained, contract=a.contract & b.contract,
        carrier_id=a.carrier_id, frame_id=a.frame_id, version=a.version,
        cold_route=None, cold_sha256=None, history=(),
        recipe=recipe, degree_bound=_degree_after_add(a, b),
    )
    return Result("ONE", "EXACT", value=out, witness={
        "counts": "unique_C2_output_summary",
        "object_fiber_not_enumerated": True,
    })


def multiply_units(a: Envelope, b: Envelope) -> Result:
    METER.hot_ops += 1
    mismatch = compatible(a, b)
    if mismatch:
        return Result("NONE", "UNSUPPORTED", witness=mismatch)
    if "multiply" not in a.contract or "multiply" not in b.contract:
        return Result("NONE", "UNSUPPORTED", witness="multiply not admitted")
    retained = compact_mul_from_sites(a.retained, b.retained)
    recipe = _compose_recipe("multiply", a, b)
    family = _family_after_arith(a, b, retained)
    out = Envelope(
        family=family, visible_unit_label=a.visible_unit_label,
        retained=retained, contract=a.contract & b.contract,
        carrier_id=a.carrier_id, frame_id=a.frame_id, version=a.version,
        cold_route=None, cold_sha256=None, history=(),
        recipe=recipe, degree_bound=_degree_after_mul(a, b),
    )
    return Result("ONE", "EXACT", value=out, witness={
        "counts": "unique_C2_output_summary",
        "affine_inherited": False if out.degree_bound is None or out.degree_bound > 1 else True,
    })


def _reopen_cube_table(env: Envelope) -> Result:
    spec = _operand_spec(env)
    if spec is not None:
        return _reopen_from_spec(spec)
    return Result("MANY", "REOPEN_REQUIRED",
                  witness={"omitted_site": OMITTED, "reason": "no cold artifact"})


def apply_input_map(env: Envelope, map_name: str) -> Result:
    METER.hot_ops += 1
    maps = input_maps()
    stored_name = map_name
    if map_name == "fiving_slice":
        map_name = "flip_h"
    if map_name not in maps:
        return Result("NONE", "UNSUPPORTED", witness=f"unknown map {map_name}")
    if map_name not in env.contract and not (map_name == "flip_h" and "fiving_slice" in env.contract):
        return Result("NONE", "UNSUPPORTED", witness="map not in contract")
    mapping = maps[map_name]
    spec = _operand_spec(env)
    mapped_recipe = None
    if spec is not None:
        METER.constructions += 1
        mapped_recipe = ("pullback", map_name, spec)
    if map_closes_b2(mapping):
        pulled = tuple(eval_retained(env.retained, mapping[s]) for s in B2)
        retained = compact_from_b2(pulled)
        out = Envelope(
            family=env.family, visible_unit_label=env.visible_unit_label,
            retained=retained, contract=env.contract,
            carrier_id=env.carrier_id, frame_id=env.frame_id, version=env.version,
            cold_route=None, cold_sha256=None,
            history=env.history, recipe=mapped_recipe, degree_bound=env.degree_bound,
        )
        return Result("ONE", "EXACT", value=out, witness={"closed_on_B2": True, "map": stored_name})
    reopened = _reopen_cube_table(env)
    if reopened.status != "EXACT":
        return reopened
    table = pullback_table(reopened.value, mapping)
    retained = compact_from_table(table)
    out = Envelope(
        family=env.family, visible_unit_label=env.visible_unit_label,
        retained=retained, contract=env.contract,
        carrier_id=env.carrier_id, frame_id=env.frame_id, version=env.version,
        cold_route=None, cold_sha256=None,
        history=env.history, recipe=mapped_recipe, degree_bound=degree_from_coeffs(mobius(table)),
    )
    return Result("ONE", "EXACT", value=out, witness={"closed_on_B2": False, "used_cold": True,
                                                      "reopened_composed_result": True})


def inspect_omitted(env: Envelope) -> Result:
    METER.hot_ops += 1
    if "inspect_omitted" not in env.contract:
        return Result("NONE", "UNSUPPORTED", witness="inspect_omitted not admitted")
    reopened = _reopen_cube_table(env)
    if reopened.status != "EXACT":
        return reopened
    table = reopened.value
    return Result("ONE", "EXACT", value=table[OMITTED], witness={"site": OMITTED})


def coherent_transport(env: Envelope, mapping: Sequence[int]) -> Result:
    """Transport both the law (pullback) and the retained receiver."""
    METER.hot_ops += 1
    require(len(mapping) == N_SITES, "Need an eight-site map")
    new_sites = tuple(s for s in range(N_SITES) if mapping[s] in B2)
    reopened = _reopen_cube_table(env)
    if reopened.status != "EXACT":
        # Compact transport of the receiver does not require the omitted site
        # when both representation and question move together: retained values
        # at s with mapping[s] in B2 are already known.
        transported = []
        known = True
        for s in new_sites:
            src = mapping[s]
            if src not in B2:
                known = False
                break
            transported.append((s, eval_retained(env.retained, src)))
        if not known:
            return reopened
        return Result("ONE", "EXACT", value=tuple(transported),
                      witness={"receiver": new_sites, "coherent": True, "used_cold": False})
    table = pullback_table(reopened.value, mapping)
    transported = tuple((s, table[s]) for s in new_sites)
    return Result("ONE", "EXACT", value=transported,
                  witness={"receiver": new_sites, "coherent": True, "used_cold": True})


def apply_fixed_receiver_map(env: Envelope, mapping: Sequence[int]) -> Result:
    """Keep the original B2 receiver after an input-view change."""
    METER.hot_ops += 1
    if map_closes_b2(mapping):
        pulled = tuple(eval_retained(env.retained, mapping[s]) for s in B2)
        retained = compact_from_b2(pulled)
        spec = _operand_spec(env)
        mapped_recipe = ("pullback_sites", tuple(int(x) for x in mapping), spec) if spec is not None else None
        if mapped_recipe is not None:
            METER.constructions += 1
        out = Envelope(
            family=env.family, visible_unit_label=env.visible_unit_label,
            retained=retained, contract=env.contract,
            carrier_id=env.carrier_id, frame_id=env.frame_id, version=env.version,
            cold_route=None, cold_sha256=None, history=env.history,
            recipe=mapped_recipe, degree_bound=env.degree_bound,
        )
        return Result("ONE", "EXACT", value=out, witness={"closed_on_B2": True})
    reopened = _reopen_cube_table(env)
    if reopened.status != "EXACT":
        return reopened
    table = pullback_table(reopened.value, mapping)
    spec = _operand_spec(env)
    mapped_recipe = None
    if spec is not None:
        METER.constructions += 1
        mapped_recipe = ("pullback_sites", tuple(int(x) for x in mapping), spec)
    out = Envelope(
        family=env.family, visible_unit_label=env.visible_unit_label,
        retained=compact_from_table(table), contract=env.contract,
        carrier_id=env.carrier_id, frame_id=env.frame_id, version=env.version,
        cold_route=None, cold_sha256=None, history=env.history,
        recipe=mapped_recipe, degree_bound=degree_from_coeffs(mobius(table)),
    )
    return Result("ONE", "EXACT", value=out, witness={"closed_on_B2": False, "used_cold": True})


def promote_stamp(stage: str, *, label: str) -> Envelope:
    METER.constructions += 1
    require(stage in GRAPHS, "Unknown Double-Stamp stage")
    vertices, edges = GRAPHS[stage]()
    summary = graph_summary(vertices, edges)
    return Envelope(
        family="double_stamp",
        visible_unit_label=label,
        retained=summary,
        contract=STAMP_CONTRACT,
        carrier_id=DOUBLE_STAMP_CARRIER,
        frame_id=DOUBLE_STAMP_FRAME,
        version=ENVELOPE_VERSION,
        cold_route=None,
        cold_sha256=None,
        history=(stage,),
        stage=stage,
    )


def dwell_enabled(env: Envelope) -> Result:
    METER.hot_ops += 1
    METER.checks += 1
    if env.family != "double_stamp" or env.stage is None:
        return Result("NONE", "UNSUPPORTED", witness="not a Double-Stamp state")
    if "dwell" not in env.contract:
        return Result("NONE", "UNSUPPORTED", witness="dwell not admitted")
    allowed = STAGE_TYPES[env.stage]["dwell_allowed"]
    kind = STAGE_TYPES[env.stage]["type"]
    if allowed:
        return Result("ONE", "EXACT", value=True, witness={"stage": env.stage, "type": kind})
    return Result("NONE", "UNSUPPORTED", value=False,
                  witness={"stage": env.stage, "type": kind, "reason": "EVENT_DWELL_FORBIDDEN"})


def split_center(env: Envelope) -> Result:
    METER.hot_ops += 1
    if env.family != "double_stamp" or env.stage != "A5":
        return Result("NONE", "UNSUPPORTED", witness="split is A5 -> B6")
    return Result("ONE", "EXACT", value=promote_stamp("B6", label=env.visible_unit_label),
                  witness={"event": "split_fixed_center"})


def insert_midpoint(env: Envelope) -> Result:
    METER.hot_ops += 1
    if env.family != "double_stamp" or env.stage != "B6":
        return Result("NONE", "UNSUPPORTED", witness="midpoint is B6 -> C7")
    return Result("ONE", "EXACT", value=promote_stamp("C7", label=env.visible_unit_label),
                  witness={"event": "insert_fixed_midpoint"})


def contract_restart(env: Envelope) -> Result:
    METER.hot_ops += 1
    if env.family != "double_stamp" or env.stage != "C7":
        return Result("NONE", "UNSUPPORTED", witness="contract restart is C7 -> A5")
    return Result("ONE", "EXACT", value=promote_stamp("A5", label=env.visible_unit_label),
                  witness={"event": "contract_central_path"})


def count_shortcut_dwell(summary: Tuple[int, int, int]) -> bool:
    """Hostile generic implementation: vertex-orbit count == 3 and no extra test."""
    return summary[0] == 3


def boolean_fiber_for_compact(retained: Sequence) -> Fiber:
    """Complete C2 fiber on the Boolean family: always MANY(2) differing at site 7."""
    site = Sort("site_value", (0, 1))
    ports = tuple(Port(f"v{i}", site) for i in range(N_SITES))
    target = tuple(as_frac(v) for v in retained)
    rows = []
    for omitted in (0, 1):
        table = []
        for s in range(N_SITES):
            if s == OMITTED:
                table.append(omitted)
            else:
                table.append(int(eval_retained(target, s)))
        # Only keep tables whose compact matches target exactly (Boolean 0/1).
        if compact_from_table(table) == target:
            rows.append(tuple(table))
    relation = Relation(ports, frozenset(rows))
    return solve(relation, {})


def quotient_for_map(map_name: str) -> dict:
    """Reuse rprm.core.deterministic_quotient on all 256 Boolean laws."""
    maps = input_maps()
    mapping = maps[map_name]
    states = tuple(range(256))
    tables = []
    for index in states:
        tables.append(tuple((index >> s) & 1 for s in range(N_SITES)))
    summary = {i: compact_from_table(tables[i]) for i in states}
    # Atoms cannot be Fraction tuples in some cores? rprm.core.atom allows tuples of ints.
    # Compact coeffs for Boolean tables are integers; convert to int tuples.
    summary_atoms = {i: tuple(int(v) for v in summary[i]) for i in states}
    observation = {i: tables[i][6] for i in states}
    transition = {}
    for i in states:
        pulled = pullback_table(tables[i], mapping)
        bits = 0
        for s, val in enumerate(pulled):
            bits |= (int(val) << s)
        transition[i] = bits
    return deterministic_quotient(states, summary_atoms, observation, transition)


# --- Baselines (honest comparison; not required to "win") ----------------------

class FullTableStore:
    def __init__(self):
        self.tables: dict[str, Tuple[Fraction, ...]] = {}
        self.lookups = 0

    def put(self, name: str, table: Sequence) -> None:
        self.tables[name] = frac_tuple(table)

    def add(self, a: str, b: str) -> Tuple[Fraction, ...]:
        self.lookups += 2
        return tuple(x + y for x, y in zip(self.tables[a], self.tables[b]))

    def mul(self, a: str, b: str) -> Tuple[Fraction, ...]:
        self.lookups += 2
        return tuple(x * y for x, y in zip(self.tables[a], self.tables[b]))

    def apply(self, name: str, mapping: Sequence[int]) -> Tuple[Fraction, ...]:
        self.lookups += 1
        return pullback_table(self.tables[name], mapping)


class MemoProduct:
    def __init__(self):
        self.cache: dict[tuple, Tuple[Fraction, ...]] = {}
        self.hits = 0
        self.misses = 0

    def mul(self, a: Sequence, b: Sequence) -> Tuple[Fraction, ...]:
        key = (tuple(a), tuple(b))
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        value = compact_mul_from_sites(a, b)
        self.cache[key] = value
        return value


def meter_snapshot() -> dict:
    return {
        "hot_ops": METER.hot_ops,
        "cold_reads": METER.cold_reads,
        "constructions": METER.constructions,
        "checks": METER.checks,
        "storage_bytes": METER.storage_bytes,
        "reopenings": METER.reopenings,
        "invalidations": METER.invalidations,
    }


def reset_meter() -> None:
    global METER
    METER = Meter()
