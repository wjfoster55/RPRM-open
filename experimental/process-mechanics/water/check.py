"""Cold check for the water process-mechanics kit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from fractions import Fraction as F
from pathlib import Path
from uuid import uuid4

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
PAYLOAD_ROOT = HERE.parents[2]
if str(PAYLOAD_ROOT) not in sys.path:
    sys.path.insert(0, str(PAYLOAD_ROOT))

import example as demo  # noqa: E402
from laws import interval_bounds  # noqa: E402


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and not args.output.is_absolute():
        parser.error("--output must be absolute")

    pending = {
        "status": "PENDING",
        "kit_id": "process-mechanics/water",
        "run_id": str(uuid4()),
    }
    result = demo.run()
    spoof = result["spoof"]
    require(result["all_positive_pass"], "positive composition comparisons failed")
    require(result["positive_comparisons"] == 76, "expected 19*4 comparisons")
    require(spoof["join_status"] == "JOIN_OK", "spoof should structurally join")
    require(spoof["joined"]["infimum"] == "10" and spoof["joined"]["supremum"] == "10", "spoof range")
    require(spoof["exact"]["infimum"] == "9" and spoof["exact"]["supremum"] == "11", "exact range")
    require(spoof["joined"]["reaches_ge_11_5"] is False, "primary threshold")
    require(spoof["exact"]["reaches_ge_11"] is True, "aux threshold exact")
    require(spoof["joined"]["reaches_ge_11"] is False, "aux threshold spoof")
    require(result["reuse"]["same_context_join"] == "JOIN_OK", "reuse ok")
    require(result["reuse"]["changed_contract_join"] == "REJECT_CONTRACT_MISMATCH", "reuse reject")
    require(result["reuse"]["missing_child"] == "OPEN_MISSING_CHILD", "missing child")

    # Hostile: gap rejection
    from rprm.process_mechanics.intervals import ChildSummary, IntervalBounds, validate_and_join
    from laws import CATALOGUE_VERSION, CONTRACT_VERSION

    gap_child = ChildSummary(
        "const10",
        F(4),
        F(6),
        IntervalBounds(F(10), F(10), True, True),
        CONTRACT_VERSION,
        CATALOGUE_VERSION,
        "(t0,t1]",
    )
    gap = validate_and_join(
        F(4),
        F(8),
        [gap_child],
        expected_contract=CONTRACT_VERSION,
        expected_catalogue=CATALOGUE_VERSION,
    )
    require(gap.status == "REJECT_PARENT_MISMATCH", "gap/parent cover")

    # Direct analytic sample
    b = interval_bounds("triangle_p4_phi0", F(4), F(8))
    require(b.lower == F(9) and b.upper == F(11), "direct triangle window")

    receipt = {
        "status": "PASS",
        "kit_id": "process-mechanics/water",
        "pending": pending,
        "checks": {
            "positive_comparisons": result["positive_comparisons"],
            "spoof_primary_11_5_false": True,
            "spoof_aux_11_differs": True,
            "reuse_context_reject": True,
            "open_missing_child": True,
        },
        "claim_ids": result["claim_ids"],
        "evidence_grade": result["evidence_grade"],
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "cwd_policy": "no network",
        },
        "source_files_sha256": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("laws.py", "example.py", "check.py", "README.md", "KIT.json")
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
        fail = {"status": "FAIL", "kit_id": "process-mechanics/water", "error": str(exc)}
        print(json.dumps(fail, indent=2))
        raise SystemExit(1)
