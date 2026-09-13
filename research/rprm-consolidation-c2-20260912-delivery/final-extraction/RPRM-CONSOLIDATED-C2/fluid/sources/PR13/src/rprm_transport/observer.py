"""Observer vs evaluator information separation.

Observer may see only declared acquired records.
Immobile inventory, hidden parameters, clean full trajectories, and future
target observations are evaluator-only unless an oracle diagnostic is named.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ObservationRecord:
    time: float
    sensor_id: str
    quantity: str
    value: float
    units: str
    acquired: bool = True


@dataclass
class ObserverView:
    """What a policy is allowed to see."""

    flow_known: bool = True
    outlet_series: list[ObservationRecord] = field(default_factory=list)
    extra_samples: list[ObservationRecord] = field(default_factory=list)
    retained_history_ids: list[str] = field(default_factory=list)

    def as_policy_input(self) -> dict[str, Any]:
        return {
            "flow_known": self.flow_known,
            "outlet": [
                {"t": r.time, "sensor": r.sensor_id, "q": r.quantity, "v": r.value, "u": r.units}
                for r in self.outlet_series
                if r.acquired
            ],
            "extra": [
                {"t": r.time, "sensor": r.sensor_id, "q": r.quantity, "v": r.value, "u": r.units}
                for r in self.extra_samples
                if r.acquired
            ],
            "retained_history_ids": list(self.retained_history_ids),
        }


@dataclass
class EvaluatorTruth:
    """Hidden state and future targets — never passed to policy selection."""

    immobile_inventory: list[float]
    mobile_inventory: list[float]
    hidden_params: dict[str, Any]
    future_outlet: list[ObservationRecord]
    target_exceeds: bool | None = None


def build_observer_from_outlet(
    times: list[float],
    outlet_c: list[float],
    *,
    t_cutoff: float,
    sensor_id: str = "outlet_mobile_c",
) -> ObserverView:
    """Prefix-only outlet readings up to t_cutoff (inclusive)."""
    series = [
        ObservationRecord(t, sensor_id, "concentration", c, "model_units", acquired=True)
        for t, c in zip(times, outlet_c)
        if t <= t_cutoff
    ]
    return ObserverView(outlet_series=series)


def build_evaluator_future(
    times: list[float],
    outlet_c: list[float],
    *,
    t_cutoff: float,
    mobile_mass: list[float],
    immobile_mass: list[float],
    hidden_params: dict[str, Any],
) -> EvaluatorTruth:
    future = [
        ObservationRecord(t, "outlet_mobile_c", "concentration", c, "model_units", acquired=False)
        for t, c in zip(times, outlet_c)
        if t > t_cutoff
    ]
    return EvaluatorTruth(
        immobile_inventory=list(immobile_mass),
        mobile_inventory=list(mobile_mass),
        hidden_params=dict(hidden_params),
        future_outlet=future,
    )


def assert_policy_blind_to_evaluator(policy_input: dict[str, Any], truth: EvaluatorTruth) -> None:
    """Sanity check: policy payload must not embed evaluator-only keys."""
    forbidden = {
        "immobile_inventory",
        "mobile_inventory",
        "hidden_params",
        "future_outlet",
        "target_exceeds",
        "cim",
        "oracle",
    }
    blob = str(policy_input).lower()
    for key in forbidden:
        assert key not in policy_input, f"policy_input contains forbidden key {key}"
        # soft textual check for accidental leakage of large arrays
        if key in ("immobile_inventory", "future_outlet"):
            assert key not in blob, f"policy_input text leaks {key}"
    _ = truth  # evaluator object stays out of policy_input by construction
