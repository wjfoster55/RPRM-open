"""Decide one supplied fixed-gap integer fiber and write a fresh receipt (0BSD).

Defaults: n=5, s=2, d=1, whose complete fiber is empty. Use --n 2 --s 1
--d 1 to retain (3,4,5). No data acquisition or external packages are used.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rprm.fixed_gap import decide_fixed_gap


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--s", type=int, default=2)
    parser.add_argument("--d", type=int, default=1)
    parser.add_argument("--output", type=Path, help="New JSON path; default .artifacts/fixed-gap/<uuid>.json")
    args = parser.parse_args()
    output = (args.output or ROOT / ".artifacts" / "fixed-gap" / (str(uuid4()) + ".json")).resolve()
    if output.suffix.lower() != ".json":
        parser.error("--output must name a new .json file")
    output.parent.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    pending = {"schema": "rprm-fixed-gap-execution/v1", "status": "PENDING", "started_utc": started}
    try:
        # Exclusive creation prevents replacing an included asset or old receipt.
        with output.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(pending) + "\n")
    except FileExistsError:
        parser.error("--output already exists; choose a fresh receipt path")

    def publish(result):
        temporary = output.with_name(output.name + "." + uuid4().hex + ".tmp")
        temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, output)

    try:
        names = ("rprm/fixed_gap.py", "rprm/core.py", "examples/fixed_gap.py")
        before = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}
        fiber = decide_fixed_gap(args.n, args.s, args.d)
        after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names}
        if before != after:
            raise RuntimeError("Source changed during execution")
        result = {**pending, "status": "COMPLETE", "fiber_receipt": fiber,
                  "source_hashes": before, "source_unchanged": True, "python": sys.version,
                  "finished_utc": datetime.now(timezone.utc).isoformat()}
        publish(result)
    except Exception as error:
        publish({**pending, "status": "ERROR", "error": f"{type(error).__name__}: {error}",
                 "finished_utc": datetime.now(timezone.utc).isoformat()})
        print(f"ERROR: {error}; receipt: {output}", file=sys.stderr)
        return 1
    print(f"{fiber['status']}; bracket [{fiber['final_bracket']['lower']}, "
          f"{fiber['final_bracket']['upper']}]; receipt: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
