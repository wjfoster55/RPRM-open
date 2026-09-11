"""Request-context validation shared by composition and candidate kits."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Mapping


@dataclass(frozen=True)
class ContextRecord:
    """Finite request context for a scoped readout.

    Fields are strings or exact finite numbers. Missing required fields yield
    an admission error, not an empty fiber.
    """

    model_id: str
    source_id: str
    plan_id: str
    plan_contents: tuple
    time_value: object
    event_side: str
    units: Mapping[str, str]
    requested_result: str


@dataclass(frozen=True)
class ContextValidation:
    status: str  # OK | ADMISSION_ERROR
    reason: str | None = None
    normalized: ContextRecord | None = None


_ALLOWED_SIDES = frozenset({"left", "right", "interval", "present", "n/a"})


def _finite_number(value: Any, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a non-bool int or float")
    if isinstance(value, float) and not isfinite(value):
        raise ValueError(f"{name} must be finite")


def validate_context(
    raw: Mapping[str, Any],
    *,
    required: tuple[str, ...] = (
        "model_id",
        "source_id",
        "plan_id",
        "plan_contents",
        "time_value",
        "event_side",
        "units",
        "requested_result",
    ),
    allowed_results: frozenset[str] | None = None,
) -> ContextValidation:
    """Validate a context mapping.

    Returns ADMISSION_ERROR for malformed input. Does not invent defaults for
    missing plan contents or units.
    """
    try:
        if not isinstance(raw, Mapping):
            raise ValueError("context must be a mapping")
        missing = [key for key in required if key not in raw]
        if missing:
            raise ValueError("missing fields: " + ", ".join(missing))
        for key in ("model_id", "source_id", "plan_id", "requested_result", "event_side"):
            value = raw[key]
            if not isinstance(value, str) or not value:
                raise ValueError(f"{key} must be a nonempty string")
        if raw["event_side"] not in _ALLOWED_SIDES:
            raise ValueError("event_side not in allowed set")
        plan_contents = raw["plan_contents"]
        if not isinstance(plan_contents, (tuple, list)):
            raise ValueError("plan_contents must be a tuple or list")
        plan_tuple = tuple(plan_contents)
        units = raw["units"]
        if not isinstance(units, Mapping) or not units:
            raise ValueError("units must be a nonempty mapping of strings")
        for ukey, uval in units.items():
            if not isinstance(ukey, str) or not isinstance(uval, str) or not uval:
                raise ValueError("units keys/values must be nonempty strings")
        time_value = raw["time_value"]
        if isinstance(time_value, (tuple, list)):
            if len(time_value) != 2:
                raise ValueError("interval time_value needs length 2")
            _finite_number(time_value[0], "time_value[0]")
            _finite_number(time_value[1], "time_value[1]")
            time_norm: object = (time_value[0], time_value[1])
        else:
            _finite_number(time_value, "time_value")
            time_norm = time_value
        if allowed_results is not None and raw["requested_result"] not in allowed_results:
            raise ValueError("requested_result outside allowed set")
        record = ContextRecord(
            model_id=raw["model_id"],
            source_id=raw["source_id"],
            plan_id=raw["plan_id"],
            plan_contents=plan_tuple,
            time_value=time_norm,
            event_side=raw["event_side"],
            units=dict(units),
            requested_result=raw["requested_result"],
        )
        return ContextValidation(status="OK", normalized=record)
    except ValueError as exc:
        return ContextValidation(status="ADMISSION_ERROR", reason=str(exc))
