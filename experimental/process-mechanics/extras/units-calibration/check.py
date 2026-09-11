"""Cold check for units-calibration extra."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path
from uuid import uuid4

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import example as demo


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
    require(result["ols_translation"]["invariant"], "translation invariance")
    require(not result["ruler_change"]["equal"], "ruler change")
    require(result["admission"]["status"] == "PARTIAL", "partial")
    require("nonfinite" in result["nonfinite_rejection"], "nonfinite")
    receipt = {
        "status": "PASS",
        "kit_id": "process-mechanics/extras/units-calibration",
        "run_id": str(uuid4()),
        "evidence_grade": "NEW_ILLUSTRATIVE_DEMO",
        "environment": {"python": sys.version, "platform": platform.platform()},
        "result": result,
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
