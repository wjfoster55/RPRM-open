"""Units/calibration/window mismatch toy with OLS translation invariance."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


def ols_slope(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n != len(ys) or n < 2:
        raise ValueError("need matched finite series length >= 2")
    if any(not math.isfinite(v) for v in xs + ys):
        raise ValueError("nonfinite values rejected")
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        raise ValueError("singular design")
    return num / den


def run() -> dict:
    hours = [0.0, 1.0, 2.0, 3.0]
    au = [0.0, 0.5, 1.0, 1.5]  # a.u./hour slope 0.5
    # Translation invariance: shift both axes, slope unchanged
    hours2 = [h + 7.0 for h in hours]
    au2 = [v + 3.0 for v in au]
    slope = ols_slope(hours, au)
    slope_shifted = ols_slope(hours2, au2)

    # Same numeric array, different units/window => different question
    pixel = [0.0, 10.0, 20.0, 30.0]  # px/hour = 10
    pixel_slope = ols_slope(hours, pixel)
    admission = {
        "arithmetic_ok": True,
        "calibration_ok": False,
        "coverage_ok": True,
        "estimator_equivalence_ok": False,
        "status": "PARTIAL",
        "note": "Pixel slope is not an a.u. publication estimator without a calibration bridge",
    }

    # Null: equal numbers with mismatched units must not silently equate
    equal_numbers_different_questions = {
        "array": [1.0, 2.0, 3.0],
        "as_volts": "V",
        "as_amperes": "A",
        "same_bytes": True,
        "same_question": False,
    }

    # Failure: nonfinite reject
    try:
        ols_slope([0.0, 1.0], [0.0, float("nan")])
        fail = "UNEXPECTED"
    except ValueError as exc:
        fail = str(exc)

    return {
        "kit_id": "process-mechanics/extras/units-calibration",
        "evidence_grade": "NEW_ILLUSTRATIVE_DEMO",
        "claim_ids": ["C-MEAS-01"],
        "claim_mapping_note": "Illustrates measurement-admission pattern related to C-MEAS-01; not a Liang replay",
        "ols_translation": {
            "slope": slope,
            "slope_shifted": slope_shifted,
            "invariant": abs(slope - slope_shifted) < 1e-12,
        },
        "ruler_change": {
            "au_slope": slope,
            "pixel_slope": pixel_slope,
            "equal": abs(slope - pixel_slope) < 1e-12,
        },
        "admission": admission,
        "units_mismatch": equal_numbers_different_questions,
        "nonfinite_rejection": fail,
    }


def main() -> None:
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = Path(__file__).resolve().parent / "expected" / "demo_receipt.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text, end="")
    print("sha256", hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()
