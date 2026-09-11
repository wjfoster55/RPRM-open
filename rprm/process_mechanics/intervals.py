"""Exact half-open interval summary composition.

Preserves lower/upper bounds and attainment flags. Structural JOIN_OK does
not certify that child contents are true; callers must keep an independent
analytic or direct reference where truth is claimed.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence


@dataclass(frozen=True)
class IntervalBounds:
    lower: Fraction
    upper: Fraction
    lower_attained: bool
    upper_attained: bool

    def reaches(self, threshold: Fraction) -> bool:
        return self.upper > threshold or (self.upper == threshold and self.upper_attained)


@dataclass(frozen=True)
class ChildSummary:
    candidate_id: str
    t0: Fraction
    t1: Fraction
    bounds: IntervalBounds
    contract_id: str
    catalogue_version: str
    boundary_convention: str
    reach_flags: frozenset[str] = frozenset()


@dataclass(frozen=True)
class JoinOutcome:
    status: str
    parent: ChildSummary | None = None
    notes: tuple[str, ...] = ()


def combine_bounds(parts: Sequence[IntervalBounds]) -> IntervalBounds:
    if not parts:
        raise ValueError("combine_bounds requires at least one part")
    lo = min(part.lower for part in parts)
    hi = max(part.upper for part in parts)
    return IntervalBounds(
        lo,
        hi,
        any(part.lower == lo and part.lower_attained for part in parts),
        any(part.upper == hi and part.upper_attained for part in parts),
    )


def _cover_status(
    parent_t0: Fraction,
    parent_t1: Fraction,
    children: Sequence[ChildSummary],
) -> str | None:
    if not children:
        return "REJECT_EMPTY"
    ordered = sorted(children, key=lambda child: (child.t0, child.t1))
    if ordered[0].t0 != parent_t0 or ordered[-1].t1 != parent_t1:
        return "REJECT_PARENT_MISMATCH"
    cursor = parent_t0
    for child in ordered:
        if child.t0 > cursor:
            return "REJECT_GAP"
        if child.t0 < cursor:
            return "REJECT_OVERLAP"
        if child.t1 <= child.t0:
            return "REJECT_GAP"
        cursor = child.t1
    if cursor != parent_t1:
        return "REJECT_GAP"
    return None


def validate_and_join(
    parent_t0: Fraction,
    parent_t1: Fraction,
    children: Sequence[ChildSummary | None],
    *,
    expected_contract: str,
    expected_catalogue: str,
    expected_boundary: str = "(t0,t1]",
    expected_candidate: str | None = None,
) -> JoinOutcome:
    """Join trusted same-history child summaries, or reject / leave open."""
    if any(child is None for child in children):
        return JoinOutcome(
            status="OPEN_MISSING_CHILD",
            notes=("missing child is incomplete search, not NONE",),
        )
    present = list(children)
    cover = _cover_status(parent_t0, parent_t1, present)  # type: ignore[arg-type]
    if cover is not None:
        return JoinOutcome(status=cover)

    ids = {child.candidate_id for child in present}  # type: ignore[union-attr]
    if len(ids) != 1:
        return JoinOutcome(status="REJECT_IDENTITY_MISMATCH")
    candidate_id = next(iter(ids))
    if expected_candidate is not None and candidate_id != expected_candidate:
        return JoinOutcome(status="REJECT_IDENTITY_MISMATCH")
    if {child.contract_id for child in present} != {expected_contract}:  # type: ignore[union-attr]
        return JoinOutcome(status="REJECT_CONTRACT_MISMATCH")
    if {child.catalogue_version for child in present} != {expected_catalogue}:  # type: ignore[union-attr]
        return JoinOutcome(status="REJECT_CATALOGUE_MISMATCH")
    if {child.boundary_convention for child in present} != {expected_boundary}:  # type: ignore[union-attr]
        return JoinOutcome(status="REJECT_BOUNDARY_MISMATCH")

    combined = combine_bounds([child.bounds for child in present])  # type: ignore[union-attr]
    reach_flags = frozenset().union(*(child.reach_flags for child in present))  # type: ignore[union-attr]
    parent = ChildSummary(
        candidate_id=candidate_id,
        t0=parent_t0,
        t1=parent_t1,
        bounds=combined,
        contract_id=expected_contract,
        catalogue_version=expected_catalogue,
        boundary_convention=expected_boundary,
        reach_flags=reach_flags,
    )
    return JoinOutcome(
        status="JOIN_OK",
        parent=parent,
        notes=("JOIN_OK is structural only; it does not certify child truth",),
    )


def equal_partition_edges(t0: Fraction, t1: Fraction, n: int) -> list[Fraction]:
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive int")
    return [t0 + (t1 - t0) * Fraction(k, n) for k in range(n + 1)]
