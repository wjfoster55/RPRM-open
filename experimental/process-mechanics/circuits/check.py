"""Cold check for the circuits kit."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
from uuid import uuid4

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import example as demo  # noqa: E402
from circuit_model import RCParams, rc_exact_event  # noqa: E402


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and not args.output.is_absolute():
        parser.error("--output must be absolute")

    result = demo.run()
    require(result["known_plan_null"]["identical_replay"], "known-plan replay")
    require(result["withheld_plan"]["prefix_equal"], "prefix equality")
    require(result["withheld_plan"]["differ"], "withheld plans must differ")

    # Malformed rejection
    rc = RCParams(1000.0, 1e-6)
    try:
        rc_exact_event(float("nan"), 0.0, 10, 1e-5, 0.0, 1.0, 0.0, 0.5, rc)
        raise RuntimeError("nonfinite voltage should fail")
    except ValueError:
        pass

    rlc = result["rlc"]
    rlc_checks = {"optional_tier": rlc["status"]}
    if rlc["status"] == "ok":
        require(rlc["two_v_recon"]["status"] == "ok", "two-voltage recon")
        require(rlc["two_v_recon"]["abs_err"] < 1e-12, "recon error")
        require(rlc["singular_map"]["status"] == "SINGULAR_OBSERVATION_MAP", "singular reject")
        rlc_checks["two_v_recon"] = True
        rlc_checks["singular_handled"] = True
    else:
        rlc_checks["skipped"] = True

    receipt = {
        "status": "PASS",
        "kit_id": "process-mechanics/circuits",
        "run_id": str(uuid4()),
        "checks": {
            "known_plan_identical": True,
            "withheld_opposite": True,
            "nonfinite_rejected": True,
            "rlc": rlc_checks,
        },
        "claim_ids": result["claim_ids"],
        "evidence_grade": result["evidence_grade"],
        "environment": {"python": sys.version, "platform": platform.platform()},
        "source_files_sha256": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("circuit_model.py", "example.py", "check.py", "README.md", "KIT.json")
            if (HERE / name).exists()
        },
    }
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        raise SystemExit(1)
