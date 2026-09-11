"""Cold check for the protein-folding process-mechanics kit."""

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


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()
    if args.output and not args.output.is_absolute():
        parser.error("--output must be absolute")

    result = demo.run(args.repo_root)
    require(result.get("status") != "OPEN_MISSING_DEPENDENCY", "lattice pack missing")
    geo = result["geometry_availability"]
    require(geo["same_contact_map"] and geo["same_energy"], "energy preservation")
    require(geo["enabledness_differs"], "continuation distinction")
    require(result["worked_example"]["path_count"] == 36, "HPPH path count")

    receipt = {
        "status": "PASS",
        "kit_id": "process-mechanics/protein-folding",
        "run_id": str(uuid4()),
        "checks": {
            "lattice_linked": True,
            "geometry_witness": True,
            "path_count_hpph": 36,
        },
        "evidence_grade": result["evidence_grade"],
        "environment": {"python": sys.version, "platform": platform.platform()},
        "source_files_sha256": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("example.py", "check.py", "README.md", "KIT.json")
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
