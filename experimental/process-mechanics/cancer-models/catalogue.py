"""Finite synthetic candidate catalogue for the cancer-models kit.

NEW_ILLUSTRATIVE_DEMO / REPRODUCED_PUBLIC_PORT of the six-candidate easy-null
pattern. Not patient data, not a clinical tool, and not malignant-transformation
evidence. C1 figure reconstruction remains PARTIAL and is not re-run here.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SynthCandidate:
    candidate_id: str
    prep_source: str
    outcome: str
    D: float
    S: float
    P: float
    E: float
    k_suppress: float
    r_scale: float
    plan_id: str
    active_control: str


# Six-candidate easy catalogue: a single D reading at tol=0.01 resolves the class.
# Values chosen so D uniquely identifies outcome classes under the stated tol.
CATALOGUE: tuple[SynthCandidate, ...] = (
    SynthCandidate("c1", "low_dose", "NO_ENTRY", 0.10, 0.40, 0.20, 0.50, 1.0, 1.0, "support_1_at_3.5", "none"),
    SynthCandidate("c2", "mid_dose", "NO_ENTRY", 0.12, 0.41, 0.21, 0.51, 1.0, 1.0, "support_1_at_3.5", "none"),
    SynthCandidate("c3", "high_dose", "ENTRY", 0.80, 0.40, 0.20, 0.50, 1.0, 1.0, "support_1_at_3.5", "none"),
    SynthCandidate("c4", "fast_repair", "ENTRY", 0.82, 0.55, 0.22, 0.52, 1.0, 1.0, "support_1_at_3.5", "none"),
    SynthCandidate("c5", "slow_repair", "DELAYED", 0.40, 0.70, 0.30, 0.40, 1.0, 0.25, "support_1_at_3.5", "none"),
    SynthCandidate("c6", "suppress", "DELAYED", 0.42, 0.72, 0.32, 0.42, 1.2, 1.0, "support_1_at_3.5", "k_suppress"),
)


def as_rows() -> list[dict]:
    return [
        {
            "candidate_id": c.candidate_id,
            "prep_source": c.prep_source,
            "outcome": c.outcome,
            "D": c.D,
            "S": c.S,
            "P": c.P,
            "E": c.E,
            "k_suppress": c.k_suppress,
            "r_scale": c.r_scale,
            "plan_id": c.plan_id,
            "active_control": c.active_control,
        }
        for c in CATALOGUE
    ]
