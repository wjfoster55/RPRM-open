"""Cold check for the cancer-models kit."""

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
PAYLOAD_ROOT = HERE.parents[2]
if str(PAYLOAD_ROOT) not in sys.path:
    sys.path.insert(0, str(PAYLOAD_ROOT))

import example as demo  # noqa: E402
from rprm.process_mechanics.candidates import filter_candidates  # noqa: E402
from catalogue import as_rows  # noqa: E402


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
    one = result["one_reading_null"]
    require(one["status"] == "RESOLVED", "one-reading should resolve")
    require(list(one["outcomes"]) == ["NO_ENTRY"], "easy null class")
    require(one["cost_readings"] == 1, "cost one")
    joint = result["empty_joint_family"]["joint"]
    require(joint["status"] == "EMPTY_FAMILY", "joint empty")
    require(result["empty_joint_family"]["alone_a"]["status"] != "EMPTY_FAMILY", "alone a")
    require(result["empty_joint_family"]["alone_b"]["status"] != "EMPTY_FAMILY", "alone b")
    require(result["incomplete"]["status"] == "OPEN_INCOMPLETE", "incomplete")
    require(result["measurement_admission"]["status"] == "PARTIAL", "partial admission")
    require(result["wrong_plan_context"]["status"] == "EMPTY_FAMILY", "plan context")

    # Malformed nonfinite observation
    bad = filter_candidates(as_rows(), [{"D": float("inf")}])
    require(bad.status == "ADMISSION_ERROR", "nonfinite reject")

    receipt = {
        "status": "PASS",
        "kit_id": "process-mechanics/cancer-models",
        "run_id": str(uuid4()),
        "checks": {
            "one_reading_null": True,
            "empty_joint_family": True,
            "open_incomplete": True,
            "measurement_partial": True,
            "nonfinite_rejected": True,
            "plan_context_retained": True,
        },
        "claim_ids": result["claim_ids"],
        "evidence_grade": result["evidence_grade"],
        "environment": {"python": sys.version, "platform": platform.platform()},
        "source_files_sha256": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("catalogue.py", "example.py", "check.py", "README.md", "KIT.json")
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
