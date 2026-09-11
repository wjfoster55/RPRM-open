"""Complete-identity candidate filtering with typed dispositions.

Dispositions here are filter outcomes, not ``rprm.core.Fiber`` tags:
RESOLVED / AMBIGUOUS / EMPTY_FAMILY / OPEN_INCOMPLETE / ADMISSION_ERROR.

EMPTY_FAMILY is not affirmative evidence that no physical event occurred.
OPEN_INCOMPLETE means required observations or children are still missing.

Admission rules (I1 public contract):
- Validate the full catalogue schema and every observation before any elimination.
- Reject duplicate candidate IDs.
- Require nonempty string outcome labels (no silent ``str()`` coercion).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Callable, Mapping, Sequence


@dataclass(frozen=True)
class CandidateFilterResult:
    status: str
    survivors: tuple[str, ...]
    outcomes: tuple[str, ...]
    notes: tuple[str, ...] = ()


def _finite(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a non-bool number")
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _validate_catalogue(
    catalogue: Sequence[Mapping[str, Any]],
    *,
    id_key: str,
    outcome_key: str,
) -> list[Mapping[str, Any]]:
    if not isinstance(catalogue, Sequence) or isinstance(catalogue, (str, bytes)):
        raise ValueError("catalogue must be a sequence of mappings")
    rows: list[Mapping[str, Any]] = []
    seen_ids: set[str] = set()
    for row in catalogue:
        if not isinstance(row, Mapping):
            raise ValueError("catalogue row must be a mapping")
        if id_key not in row or outcome_key not in row:
            raise ValueError(f"catalogue row needs {id_key} and {outcome_key}")
        cid = row[id_key]
        if not isinstance(cid, str) or not cid:
            raise ValueError("candidate_id must be a nonempty string")
        if cid in seen_ids:
            raise ValueError(f"duplicate candidate_id: {cid}")
        seen_ids.add(cid)
        outcome = row[outcome_key]
        if not isinstance(outcome, str) or not outcome:
            raise ValueError("outcome must be a nonempty string label")
        for field, value in row.items():
            if field in (id_key, outcome_key):
                continue
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                _finite(value, field)
        rows.append(row)
    return rows


def _validate_observations(
    observations: Sequence[Mapping[str, Any]],
    catalogue: Sequence[Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    if not isinstance(observations, Sequence) or isinstance(observations, (str, bytes)):
        raise ValueError("observations must be a sequence of mappings")
    known_fields: set[str] = set()
    for row in catalogue:
        known_fields.update(row.keys())
    validated: list[Mapping[str, Any]] = []
    for obs in observations:
        if not isinstance(obs, Mapping):
            raise ValueError("observation must be a mapping")
        for field, reading in obs.items():
            if field not in known_fields:
                raise ValueError(f"unknown observation field: {field}")
            _finite(reading, field)
        validated.append(obs)
    return validated


def filter_candidates(
    catalogue: Sequence[Mapping[str, Any]],
    observations: Sequence[Mapping[str, Any]] | None,
    *,
    id_key: str = "candidate_id",
    outcome_key: str = "outcome",
    tol: float = 0.01,
    require_same_context: Callable[[Mapping[str, Any]], bool] | None = None,
    incomplete: bool = False,
) -> CandidateFilterResult:
    """Intersect catalogue rows against all observations.

    Each observation maps field name -> numeric reading. A candidate survives
    only if every supplied field is within ``tol`` of its declared value and
    optional context predicate passes.
    """
    try:
        tol = _finite(tol, "tol")
        if tol < 0:
            raise ValueError("tol must be nonnegative")
        if incomplete or observations is None:
            return CandidateFilterResult(
                status="OPEN_INCOMPLETE",
                survivors=tuple(),
                outcomes=tuple(),
                notes=("required observation or child missing",),
            )
        rows = _validate_catalogue(catalogue, id_key=id_key, outcome_key=outcome_key)
        obs_list = _validate_observations(observations, rows)
        ids: list[str] = []
        survivors: list[Mapping[str, Any]] = []
        for row in rows:
            if require_same_context is not None and not require_same_context(row):
                continue
            ok = True
            for obs in obs_list:
                for field, reading in obs.items():
                    if field not in row:
                        # Field known in catalogue overall but absent on this row.
                        raise ValueError(f"unknown observation field: {field}")
                    declared = _finite(row[field], field)
                    measured = _finite(reading, field)
                    if abs(declared - measured) > tol:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                survivors.append(row)
                ids.append(str(row[id_key]))
        if not survivors:
            return CandidateFilterResult(
                status="EMPTY_FAMILY",
                survivors=tuple(),
                outcomes=tuple(),
                notes=("empty compatible family is not a NO_EVENT claim",),
            )
        outcomes = tuple(sorted({str(row[outcome_key]) for row in survivors}))
        if len(outcomes) == 1:
            status = "RESOLVED"
            notes: tuple[str, ...] = ("single outcome class among survivors",)
        else:
            status = "AMBIGUOUS"
            notes = ("multiple outcome classes remain",)
        return CandidateFilterResult(
            status=status,
            survivors=tuple(ids),
            outcomes=outcomes,
            notes=notes,
        )
    except ValueError as exc:
        return CandidateFilterResult(
            status="ADMISSION_ERROR",
            survivors=tuple(),
            outcomes=tuple(),
            notes=(str(exc),),
        )


def opposing_witness_step(
    survivors: Sequence[str],
    watched: tuple[str, str] | None,
    *,
    class_of: Callable[[str], str],
) -> dict[str, Any]:
    """Bookkeeping for an opposing-pair witness over a survivor set.

    Expired witnesses trigger replacement search; they do not themselves
    resolve the query.
    """
    alive = set(survivors)
    if watched is None:
        return {"pair_status": "NO_PAIR", "watched": None}
    a, b = watched
    if a not in alive or b not in alive:
        replacement = None
        by_class: dict[str, str] = {}
        for cid in survivors:
            by_class.setdefault(class_of(cid), cid)
        if len(by_class) >= 2:
            keys = sorted(by_class)
            replacement = (by_class[keys[0]], by_class[keys[1]])
            return {
                "pair_status": "PAIR_EXPIRED_REPLACED",
                "watched": replacement,
                "note": "expired witness is not a resolved query",
            }
        return {
            "pair_status": "PAIR_EXPIRED_NO_REPLACEMENT",
            "watched": None,
            "note": "expired witness is not a resolved query",
        }
    if class_of(a) == class_of(b):
        return {"pair_status": "PAIR_SAME_CLASS", "watched": watched}
    return {"pair_status": "PAIR_RETAINS_AMBIGUITY", "watched": watched}
