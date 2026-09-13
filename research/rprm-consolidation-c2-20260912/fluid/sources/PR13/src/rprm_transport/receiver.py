"""Receiver contract and outcome vocabulary for the transport study."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class SolveStatus(str, Enum):
    NONE = "NONE"  # no compatible history
    ONE = "ONE"  # unique answer under declared candidates
    MANY = "MANY"  # unresolved ambiguity among candidates
    OPEN = "OPEN"  # insufficient evidence / not yet decidable
    FALSE_ONE = "FALSE_ONE"  # unique but wrong vs evaluator truth


@dataclass(frozen=True)
class ReceiverQuestion:
    """Primary held-out question (model-study endpoint, not a health standard)."""

    name: str = "outlet_exceedance"
    description: str = (
        "Does outlet mobile concentration exceed threshold C* over future "
        "interval [t0, t1] under a known continuation input?"
    )
    threshold_c: float = 0.05  # concentration units of the model
    t0: float = 200.0  # days from episode start
    t1: float = 300.0
    secondary: str = "cumulative_mass_released_over_[t0,t1]"


@dataclass(frozen=True)
class AnswerRecord:
    status: SolveStatus
    predicted_exceeds: bool | None
    predicted_mass: float | None
    supporting_candidate_ids: list[str]
    notes: str

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


def evaluate_threshold(times: list[float], outlet_c: list[float], q: ReceiverQuestion) -> bool:
    """Evaluator-side truth for the threshold question (not for the observer)."""
    for t, c in zip(times, outlet_c):
        if q.t0 <= t <= q.t1 and c > q.threshold_c:
            return True
    return False


def classify_from_candidates(
    candidate_predictions: dict[str, bool],
    truth: bool | None = None,
) -> AnswerRecord:
    """Map candidate yes/no predictions to NONE/ONE/MANY(/FALSE_ONE if truth given)."""
    if not candidate_predictions:
        return AnswerRecord(SolveStatus.NONE, None, None, [], "no compatible candidates")
    values = set(candidate_predictions.values())
    ids = list(candidate_predictions.keys())
    if len(values) > 1:
        return AnswerRecord(SolveStatus.MANY, None, None, ids, "candidates disagree")
    pred = next(iter(values))
    if truth is None:
        return AnswerRecord(SolveStatus.ONE, pred, None, ids, "unique under candidates")
    if pred == truth:
        return AnswerRecord(SolveStatus.ONE, pred, None, ids, "unique and correct")
    return AnswerRecord(
        SolveStatus.FALSE_ONE, pred, None, ids, "unique under candidates but incorrect"
    )
