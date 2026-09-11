"""Circuits kit demo: known-plan null, withheld-plan twins, RLC reconstruction."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from circuit_model import (  # noqa: E402
    RCParams,
    RLCParams,
    numpy_available,
    rc_exact_event,
    rc_trajectory,
    rlc_reconstruct_i,
    rlc_trajectory_optional,
)


def run() -> dict:
    rc = RCParams(1000.0, 1e-6)
    # Sufficient present-state null: known plan + present voltage determines event.
    e1 = rc_exact_event(0.8, 0.003, 100, 2e-5, 0.004, 1.0, 0.0, 0.5, rc)
    e2 = rc_exact_event(0.8, 0.003, 100, 2e-5, 0.004, 1.0, 0.0, 0.5, rc)
    known_plan = {
        "identical_replay": e1 == e2,
        "event": e1,
        "note": "Noiseless RC with known plan needs no extra history beyond present state",
    }

    hold = 0.004
    tA, vA = rc_trajectory(0.765, [(hold, 1.0), (0.006, 0.0)], 2e-5, rc)
    tB, vB = rc_trajectory(0.765, [(hold, 1.0), (0.006, 1.0)], 2e-5, rc)
    idx = int(round(0.003 / 2e-5))
    prefix_equal = all(abs(a - b) < 1e-12 for a, b in zip(vA[: idx + 1], vB[: idx + 1]))
    labA = rc_exact_event(vA[idx], tA[idx], 100, 2e-5, hold, 1.0, 0.0, 0.5, rc)
    labB = rc_exact_event(vB[idx], tB[idx], 100, 2e-5, hold, 1.0, 1.0, 0.5, rc)
    withheld = {
        "prefix_equal": prefix_equal,
        "v_now": vA[idx],
        "labA": labA,
        "labB": labB,
        "differ": labA != labB,
        "note": "Identical observed past; unprovided future release yields opposite labels",
    }

    rlc_section: dict
    if not numpy_available():
        rlc_section = {"status": "SKIP_OPTIONAL_DEPENDENCY", "reason": "numpy/scipy unavailable"}
    else:
        rlc = RLCParams(200.0, 1e-3, 1e-6)
        traj = rlc_trajectory_optional((0.8, 0.001), [(0.0002, 0.0)], 5e-7, rlc)
        lag = 5
        idx_r = 100
        recon = rlc_reconstruct_i(
            traj["v"][idx_r - lag],
            traj["v"][idx_r],
            0.0,
            lag * 5e-7,
            rlc,
        )
        abs_err = abs(recon["i_now"] - traj["i"][idx_r]) if recon["status"] == "ok" else None
        singular = rlc_reconstruct_i(0.8, 0.8, 0.0, 0.0, rlc)
        # Force singular path explicitly when lag_dt=0 => F=I => F01=0
        rlc_section = {
            "status": "ok",
            "zeta": rlc.zeta,
            "two_v_recon": {
                "status": recon["status"],
                "abs_err": abs_err,
                "F01": recon.get("F01"),
            },
            "singular_map": {
                "status": singular["status"],
                "F01": singular.get("F01"),
            },
            "observation_count": 2,
            "units": {"R": "ohm", "L": "H", "C": "F", "v": "V", "i": "A", "t": "s"},
        }

    return {
        "kit_id": "process-mechanics/circuits",
        "version": "0.1.0",
        "claim_ids": ["PC-CONT-01", "PC-INPUT-01", "PC-STATE-01", "PC-NULL-01", "PC-EST-01"],
        "evidence_grade": {
            "PC-CONT-01": "REPRODUCED_PUBLIC_PORT",
            "PC-INPUT-01": "REPRODUCED_PUBLIC_PORT",
            "PC-STATE-01": "REPRODUCED_PUBLIC_PORT" if numpy_available() else "SKIP_OPTIONAL_DEPENDENCY",
            "PC-NULL-01": "NEW_ILLUSTRATIVE_DEMO",
            "PC-EST-01": "REAGGREGATED_PUBLIC_EXTRACT",
        },
        "evidence_notes": {
            "PC-NULL-01": "Present-state sufficiency under known plan shown; not the 15475-row hard-decision null",
            "PC-EST-01": (
                "Historical noisy LS MSE reaggregated from public_evidence/pc1/MATCHED_INFO_HEADLINE.json; "
                "not model regeneration. Full panel support is the allowlisted extract, not this toy demo."
            ),
        },
        "known_plan_null": known_plan,
        "withheld_plan": withheld,
        "rlc": rlc_section,
        "source_content_commit": "d2e63b56d79d3c620e8aec8121adf18bcb7395bd",
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
