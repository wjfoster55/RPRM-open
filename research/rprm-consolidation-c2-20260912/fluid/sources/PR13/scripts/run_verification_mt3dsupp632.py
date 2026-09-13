#!/usr/bin/env python
"""Reproduce official MT3DMS Supplemental Guide Problem 6.3.2 (all three scenarios)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rprm_transport.verification_mt3dsupp632 import PARAMETERS, run_scenario  # noqa: E402


def main() -> int:
    out_dir = ROOT / "results" / "verification_mt3dsupp632"
    out_dir.mkdir(parents=True, exist_ok=True)
    reports = []
    for idx in range(len(PARAMETERS)):
        print(f"Running scenario {idx} ...", flush=True)
        rep = run_scenario(idx, silent=True)
        print(json.dumps(rep, indent=2))
        reports.append(rep)
    path = out_dir / "summary.json"
    path.write_text(json.dumps(reports, indent=2), encoding="utf-8")
    print(f"Wrote {path}")
    # Soft acceptance: MF6 vs MT3DMS should be close on official problem
    worst = max(r["max_abs_rel_diff_vs_mt3dms"] for r in reports)
    print(f"Worst max abs relative diff (MF6 vs MT3DMS interp): {worst:.6g}")
    return 0 if worst < 0.25 else 2


if __name__ == "__main__":
    raise SystemExit(main())
