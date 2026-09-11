"""Cancer-models kit: one-reading null, empty joint family, measurement admission."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
PAYLOAD_ROOT = HERE.parents[2]
if str(PAYLOAD_ROOT) not in sys.path:
    sys.path.insert(0, str(PAYLOAD_ROOT))

from rprm.process_mechanics.candidates import filter_candidates, opposing_witness_step  # noqa: E402
from rprm.process_mechanics.measurement import admit_measurement  # noqa: E402
from catalogue import as_rows  # noqa: E402


def run() -> dict:
    rows = as_rows()
    # One-reading null: D from high_dose resolves ENTRY vs others under tol=0.01
    # Actually need D that separates - high_dose D=0.80 only matches c3 within 0.01? c4 is 0.82 so both ENTRY.
    one_reading = filter_candidates(rows, [{"D": 0.80}], tol=0.01)
    # Easy null still: first field D reduces to a single outcome class.
    fixed_order_first = filter_candidates(rows, [{"D": 0.10}], tol=0.01)

    # Empty joint family: combine exact fields from different candidates
    alone_a = filter_candidates(rows, [{"k_suppress": 1.2}], tol=0.01)
    alone_b = filter_candidates(rows, [{"r_scale": 0.25}], tol=0.01)
    joint = filter_candidates(rows, [{"k_suppress": 1.2}, {"r_scale": 0.25}], tol=0.01)

    # Plan/control context must stay present
    wrong_plan = filter_candidates(
        rows,
        [{"D": 0.80}],
        tol=0.01,
        require_same_context=lambda row: row["plan_id"] == "no_future_support",
    )

    # Incomplete observation stream
    incomplete = filter_candidates(rows, None, incomplete=True)

    # Witness expiry bookkeeping
    class_of = {row["candidate_id"]: row["outcome"] for row in rows}.__getitem__
    survivors = one_reading.survivors
    witness = opposing_witness_step(survivors, ("c1", "c3"), class_of=class_of)

    # Measurement admission: arithmetic without calibration/coverage/estimator equivalence
    partial = admit_measurement(
        arithmetic_ok=True,
        calibration_ok=False,
        coverage_ok=False,
        estimator_equivalence_ok=False,
        payload={
            "pixel_slope_per_hour": 21.62,
            "requested": "publication_au_per_hour",
            "figure_lane": "C1_CLOSED_PARTIAL",
        },
    )
    rejected_empty_event_claim = {
        "empty_family_status": joint.status,
        "not_a_no_event_claim": True,
        "note": "EMPTY_FAMILY ≠ affirmative evidence of no physical event",
    }

    return {
        "kit_id": "process-mechanics/cancer-models",
        "version": "0.1.0",
        "claim_ids": ["C-CAL-01", "C-MEAS-01"],
        "evidence_grade": {
            "C-CAL-01": "NEW_ILLUSTRATIVE_DEMO",
            "C-MEAS-01": "NEW_ILLUSTRATIVE_DEMO",
            "c1_figure_reconstruction": "ACCEPTED_PARTIAL_NOT_REPLAYED_HERE",
        },
        "evidence_notes": {
            "C-CAL-01": "Synthetic six-candidate easy D-reading null; not held-out biology",
            "C-MEAS-01": "Admission record pattern only; no Liang redigitization",
        },
        "one_reading_null": {
            "observation": {"D": 0.10},
            "status": fixed_order_first.status,
            "survivors": fixed_order_first.survivors,
            "outcomes": fixed_order_first.outcomes,
            "cost_readings": 1,
        },
        "class_resolution_example": {
            "observation": {"D": 0.80},
            "status": one_reading.status,
            "survivors": one_reading.survivors,
            "outcomes": one_reading.outcomes,
        },
        "empty_joint_family": {
            "alone_a": {"status": alone_a.status, "survivors": alone_a.survivors},
            "alone_b": {"status": alone_b.status, "survivors": alone_b.survivors},
            "joint": {"status": joint.status, "survivors": joint.survivors},
        },
        "wrong_plan_context": {
            "status": wrong_plan.status,
            "survivors": wrong_plan.survivors,
        },
        "incomplete": {"status": incomplete.status, "notes": incomplete.notes},
        "witness": witness,
        "measurement_admission": {
            "status": partial.status,
            "arithmetic_ok": partial.arithmetic_ok,
            "calibration_ok": partial.calibration_ok,
            "coverage_ok": partial.coverage_ok,
            "estimator_equivalence_ok": partial.estimator_equivalence_ok,
            "notes": partial.notes,
            "payload": dict(partial.payload),
        },
        "empty_family_interpretation": rejected_empty_event_claim,
        "links": {
            "research_brca1": "research-packs/brca1-function/",
            "c1_external": "wjfoster55/rprm-cancer-research@a0538e8",
        },
        "non_claims": [
            "No clinical risk tool",
            "No treatment prescription",
            "No patient-data entry",
            "No malignant-transformation evidence",
            "C1 figure lane stays closed/partial",
        ],
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
