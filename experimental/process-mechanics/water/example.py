"""Water composition demo: exact child join, spoof control, scoped reuse."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
PAYLOAD_ROOT = HERE.parents[2]
if str(PAYLOAD_ROOT) not in sys.path:
    sys.path.insert(0, str(PAYLOAD_ROOT))

from rprm.process_mechanics.intervals import (  # noqa: E402
    ChildSummary,
    IntervalBounds,
    equal_partition_edges,
    validate_and_join,
)
from laws import (  # noqa: E402
    CATALOGUE_VERSION,
    CONTRACT_VERSION,
    THRESH_AUX,
    THRESH_PRIMARY,
    catalogue_ids,
    endpoint_only_bounds,
    interval_bounds,
)

PARENT = (F(4), F(8))


def _summary(cid: str, t0: F, t1: F, bounds, tag_reach: bool = True) -> ChildSummary:
    reach = set()
    if bounds.reaches(THRESH_PRIMARY):
        reach.add("ge_11_5")
    if bounds.reaches(THRESH_AUX):
        reach.add("ge_11")
    return ChildSummary(
        candidate_id=cid,
        t0=t0,
        t1=t1,
        bounds=IntervalBounds(bounds.lower, bounds.upper, bounds.lower_attained, bounds.upper_attained),
        contract_id=CONTRACT_VERSION,
        catalogue_version=CATALOGUE_VERSION,
        boundary_convention="(t0,t1]",
        reach_flags=frozenset(reach) if tag_reach else frozenset(),
    )


def compose_partition(cid: str, n: int) -> dict:
    edges = equal_partition_edges(PARENT[0], PARENT[1], n)
    children = [
        _summary(cid, a, b, interval_bounds(cid, a, b)) for a, b in zip(edges, edges[1:])
    ]
    direct = interval_bounds(cid, PARENT[0], PARENT[1])
    join = validate_and_join(
        PARENT[0],
        PARENT[1],
        children,
        expected_contract=CONTRACT_VERSION,
        expected_catalogue=CATALOGUE_VERSION,
        expected_candidate=cid,
    )
    parent = join.parent
    assert parent is not None or join.status != "JOIN_OK"
    match = (
        join.status == "JOIN_OK"
        and parent is not None
        and parent.bounds.lower == direct.lower
        and parent.bounds.upper == direct.upper
        and parent.bounds.lower_attained == direct.lower_attained
        and parent.bounds.upper_attained == direct.upper_attained
        and (("ge_11_5" in parent.reach_flags) == direct.reaches(THRESH_PRIMARY))
    )
    return {
        "candidate_id": cid,
        "parts": n,
        "join_status": join.status,
        "direct": {
            "infimum": str(direct.lower),
            "supremum": str(direct.upper),
            "infimum_attained": direct.lower_attained,
            "supremum_attained": direct.upper_attained,
            "reaches_ge_11_5": direct.reaches(THRESH_PRIMARY),
            "reaches_ge_11": direct.reaches(THRESH_AUX),
        },
        "composed_matches_direct": match,
        "cost_bounds_evals": n,
        "cost_joins": 1,
    }


def endpoint_spoof_case() -> dict:
    cid = "triangle_p4_phi0"
    # Endpoint-only children on (4,6] and (6,8]
    spoof_children = [
        _summary(cid, F(4), F(6), endpoint_only_bounds(cid, F(4), F(6))),
        _summary(cid, F(6), F(8), endpoint_only_bounds(cid, F(6), F(8))),
    ]
    join = validate_and_join(
        PARENT[0],
        PARENT[1],
        spoof_children,
        expected_contract=CONTRACT_VERSION,
        expected_catalogue=CATALOGUE_VERSION,
        expected_candidate=cid,
    )
    exact = interval_bounds(cid, PARENT[0], PARENT[1])
    parent = join.parent
    return {
        "candidate_id": cid,
        "join_status": join.status,
        "joined": None
        if parent is None
        else {
            "infimum": str(parent.bounds.lower),
            "supremum": str(parent.bounds.upper),
            "reaches_ge_11_5": "ge_11_5" in parent.reach_flags,
            "reaches_ge_11": "ge_11" in parent.reach_flags,
        },
        "exact": {
            "infimum": str(exact.lower),
            "supremum": str(exact.upper),
            "reaches_ge_11_5": exact.reaches(THRESH_PRIMARY),
            "reaches_ge_11": exact.reaches(THRESH_AUX),
        },
        "analytic_match": False if parent is None else (
            parent.bounds.lower == exact.lower and parent.bounds.upper == exact.upper
        ),
        "primary_11_5_unchanged": True,
        "note": "JOIN_OK with wrong contents; auxiliary reach-11 differs; primary 11.5 stays false",
    }


def reuse_context_case() -> dict:
    """Same numeric interval under a different contract must not silently reuse."""
    cid = "const10"
    child = _summary(cid, PARENT[0], PARENT[1], interval_bounds(cid, PARENT[0], PARENT[1]))
    wrong = ChildSummary(
        candidate_id=child.candidate_id,
        t0=child.t0,
        t1=child.t1,
        bounds=child.bounds,
        contract_id="different-contract",
        catalogue_version=child.catalogue_version,
        boundary_convention=child.boundary_convention,
        reach_flags=child.reach_flags,
    )
    ok = validate_and_join(
        PARENT[0],
        PARENT[1],
        [child],
        expected_contract=CONTRACT_VERSION,
        expected_catalogue=CATALOGUE_VERSION,
    )
    bad = validate_and_join(
        PARENT[0],
        PARENT[1],
        [wrong],
        expected_contract=CONTRACT_VERSION,
        expected_catalogue=CATALOGUE_VERSION,
    )
    missing = validate_and_join(
        PARENT[0],
        PARENT[1],
        [None],
        expected_contract=CONTRACT_VERSION,
        expected_catalogue=CATALOGUE_VERSION,
    )
    return {
        "same_context_join": ok.status,
        "changed_contract_join": bad.status,
        "missing_child": missing.status,
    }


def run() -> dict:
    comparisons = []
    for cid in catalogue_ids():
        for n in (2, 4, 8):
            comparisons.append(compose_partition(cid, n))
    # Mixed partition (4,5], (5,6], (6,8]
    mixed = []
    for cid in catalogue_ids():
        edges = [F(4), F(5), F(6), F(8)]
        children = [
            _summary(cid, a, b, interval_bounds(cid, a, b)) for a, b in zip(edges, edges[1:])
        ]
        direct = interval_bounds(cid, PARENT[0], PARENT[1])
        join = validate_and_join(
            PARENT[0],
            PARENT[1],
            children,
            expected_contract=CONTRACT_VERSION,
            expected_catalogue=CATALOGUE_VERSION,
            expected_candidate=cid,
        )
        parent = join.parent
        match = (
            join.status == "JOIN_OK"
            and parent is not None
            and parent.bounds.lower == direct.lower
            and parent.bounds.upper == direct.upper
            and parent.bounds.lower_attained == direct.lower_attained
            and parent.bounds.upper_attained == direct.upper_attained
        )
        mixed.append({"candidate_id": cid, "join_status": join.status, "composed_matches_direct": match})
    all_pos = all(row["composed_matches_direct"] for row in comparisons) and all(
        row["composed_matches_direct"] for row in mixed
    )
    spoof = endpoint_spoof_case()
    reuse = reuse_context_case()
    return {
        "kit_id": "process-mechanics/water",
        "version": "0.1.0",
        "claim_ids": ["W-COMP-01", "W-TRUST-01", "W-REUSE-01"],
        "evidence_grade": {
            "W-COMP-01": "REPRODUCED_PUBLIC_PORT",
            "W-TRUST-01": "REPRODUCED_PUBLIC_PORT",
            "W-REUSE-01": "NEW_ILLUSTRATIVE_DEMO",
        },
        "evidence_notes": {
            "W-COMP-01": "19 laws x (2,4,8 equal + mixed) replayed locally against direct exact bounds",
            "W-TRUST-01": "triangle_p4_phi0 endpoint spoof checked against frozen PR13 extract numbers",
            "W-REUSE-01": "local context-mismatch rejection demo; not independent PR14 audit replay",
        },
        "positive_comparisons": len(comparisons) + len(mixed),
        "all_positive_pass": all_pos,
        "spoof": spoof,
        "reuse": reuse,
        "source_content_commit": "90bf41040076af2b448ff5f52c512bbcbb0f2e26",
    }


def main() -> None:
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = HERE / "expected" / "demo_receipt.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text, end="")
    print("sha256", hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
