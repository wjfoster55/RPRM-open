"""Node model tests for the offline playground (not a browser UI review)."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

HERE = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and not args.output.is_absolute():
        parser.error("--output must be absolute")

    script = r"""
const M = require('./model.js');
const cont = M.continuationDemo(10);
if (!(cont.sameDisplay && cont.nextA !== cont.nextB)) throw new Error('continuation');
if (cont.sufficientNextA === cont.sufficientNextB) throw new Error('sufficient control');
const catalogue = [
  {id:'c1', outcome:'NO_ENTRY', D:0.10, k_suppress:1.0, r_scale:1.0},
  {id:'c6', outcome:'DELAYED', D:0.42, k_suppress:1.2, r_scale:1.0},
  {id:'c5', outcome:'DELAYED', D:0.40, k_suppress:1.0, r_scale:0.25}
];
const joint = M.joinCandidates(catalogue, [{k_suppress:1.2},{r_scale:0.25}]);
if (joint.status !== 'EMPTY_FAMILY') throw new Error('joint');
const ok = M.reuseCheck({sourceId:'s', planId:'planA', interval:'(4,8]'}, {sourceId:'s', planId:'planA', interval:'(4,8]'});
const bad = M.reuseCheck({sourceId:'s', planId:'planA', interval:'(4,8]'}, {sourceId:'s', planId:'planB', interval:'(4,8]'});
if (ok.status !== 'REUSE_OK' || bad.status !== 'REJECT_CONTEXT_MISMATCH') throw new Error('reuse');
const receipt = M.exportReceipt({edited:true});
if (!receipt.includes('NEW_ILLUSTRATIVE_DEMO')) throw new Error('export grade');
console.log(JSON.stringify({ok:true, continuation:cont, joint, okReuse:ok, badReuse:bad}));
"""
    proc = subprocess.run(
        ["node", "-e", script],
        cwd=str(HERE),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout or "node failed")
    body = json.loads(proc.stdout.strip().splitlines()[-1])
    receipt = {
        "status": "PASS",
        "kit_id": "process-mechanics/playground",
        "run_id": str(uuid4()),
        "model_checks": body,
        "ui_review": "NOT_RUN",
        "ui_review_note": "Browser interaction checklist in README; not executed in this automated receipt",
        "environment": {"python": sys.version, "platform": platform.platform(), "node": True},
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
