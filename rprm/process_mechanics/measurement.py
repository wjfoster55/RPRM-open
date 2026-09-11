"""Measurement-admission records separating arithmetic from scientific support.

``admit_measurement`` summarizes **caller-declared** prerequisites. It does not
inspect a calibration trace, estimator implementation, or laboratory notebook,
and a declared all-true record is not independent scientific verification.
Evidence and provenance remain separate from these flags.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class MeasurementAdmission:
    status: str  # ADMITTED | PARTIAL | REJECTED | ADMISSION_ERROR
    arithmetic_ok: bool
    calibration_ok: bool
    coverage_ok: bool
    estimator_equivalence_ok: bool
    notes: tuple[str, ...]
    payload: Mapping[str, Any]


def _require_bool(name: str, value: Any) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{name} must be an actual bool, not {type(value).__name__}")
    return value


def admit_measurement(
    *,
    arithmetic_ok: bool,
    calibration_ok: bool,
    coverage_ok: bool,
    estimator_equivalence_ok: bool,
    payload: Mapping[str, Any] | None = None,
    require_all_for_admit: bool = True,
) -> MeasurementAdmission:
    """Classify whether declared prerequisites support a requested quantity.

    Only actual booleans (or equivalently typed boolean statuses passed as
    ``bool``) are accepted. Strings such as ``\"false\"`` are admission errors.
    This helper does not independently prove scientific admissibility.
    """
    try:
        if type(require_all_for_admit) is not bool:
            raise ValueError("require_all_for_admit must be an actual bool")
        flags = (
            _require_bool("arithmetic_ok", arithmetic_ok),
            _require_bool("calibration_ok", calibration_ok),
            _require_bool("coverage_ok", coverage_ok),
            _require_bool("estimator_equivalence_ok", estimator_equivalence_ok),
        )
        notes: list[str] = [
            "summarizes declared prerequisites only; does not inspect calibration or prove admissibility"
        ]
        if not flags[0]:
            notes.append("arithmetic incomplete or nonfinite")
        if not flags[1]:
            notes.append("calibration bridge unsupported")
        if not flags[2]:
            notes.append("requested coverage window unsupported")
        if not flags[3]:
            notes.append("estimator equivalence to publication unsupported")
        body = dict(payload or {})
        if require_all_for_admit and all(flags):
            status = "ADMITTED"
        elif flags[0] and not all(flags):
            status = "PARTIAL"
        elif not flags[0]:
            status = "REJECTED"
        else:
            status = "ADMITTED"
        return MeasurementAdmission(
            status=status,
            arithmetic_ok=flags[0],
            calibration_ok=flags[1],
            coverage_ok=flags[2],
            estimator_equivalence_ok=flags[3],
            notes=tuple(notes),
            payload=body,
        )
    except ValueError as exc:
        return MeasurementAdmission(
            status="ADMISSION_ERROR",
            arithmetic_ok=False,
            calibration_ok=False,
            coverage_ok=False,
            estimator_equivalence_ok=False,
            notes=(str(exc),),
            payload={},
        )
    except Exception as exc:  # noqa: BLE001 — admission boundary
        return MeasurementAdmission(
            status="ADMISSION_ERROR",
            arithmetic_ok=False,
            calibration_ok=False,
            coverage_ok=False,
            estimator_equivalence_ok=False,
            notes=(str(exc),),
            payload={},
        )
