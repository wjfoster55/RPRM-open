"""Equal-information baselines for the declared receiver question."""

from __future__ import annotations

from dataclasses import dataclass

from .observer import ObserverView
from .receiver import AnswerRecord, ReceiverQuestion, SolveStatus


@dataclass
class BaselineResult:
    name: str
    answer: AnswerRecord


def current_reading_baseline(view: ObserverView, q: ReceiverQuestion) -> BaselineResult:
    """Inexpensive: use last acquired outlet reading vs threshold (no storage model)."""
    if not view.outlet_series:
        ans = AnswerRecord(SolveStatus.OPEN, None, None, [], "no outlet readings")
        return BaselineResult("current_reading", ans)
    last = view.outlet_series[-1].value
    pred = last > q.threshold_c
    ans = AnswerRecord(
        SolveStatus.ONE,
        pred,
        None,
        ["current_reading"],
        f"last_c={last} vs C*={q.threshold_c} (myopic; ignores storage)",
    )
    return BaselineResult("current_reading", ans)


def history_mean_baseline(view: ObserverView, q: ReceiverQuestion) -> BaselineResult:
    """Cheap history summary: mean of acquired outlet readings vs threshold."""
    if not view.outlet_series:
        ans = AnswerRecord(SolveStatus.OPEN, None, None, [], "no outlet readings")
        return BaselineResult("history_mean", ans)
    vals = [r.value for r in view.outlet_series]
    mean = sum(vals) / len(vals)
    pred = mean > q.threshold_c
    ans = AnswerRecord(
        SolveStatus.ONE,
        pred,
        None,
        ["history_mean"],
        f"mean_c={mean} vs C*={q.threshold_c}",
    )
    return BaselineResult("history_mean", ans)


def dual_domain_candidate_gate(
    candidate_exceeds: dict[str, bool],
) -> BaselineResult:
    """RPRM-style candidate gate: ONE/MANY/NONE from admitted histories' predictions."""
    if not candidate_exceeds:
        ans = AnswerRecord(SolveStatus.NONE, None, None, [], "empty candidate set")
        return BaselineResult("candidate_gate", ans)
    vals = set(candidate_exceeds.values())
    ids = list(candidate_exceeds.keys())
    if len(vals) > 1:
        ans = AnswerRecord(SolveStatus.MANY, None, None, ids, "need distinguishing observation")
        return BaselineResult("candidate_gate", ans)
    pred = next(iter(vals))
    ans = AnswerRecord(SolveStatus.ONE, pred, None, ids, "candidates agree")
    return BaselineResult("candidate_gate", ans)
