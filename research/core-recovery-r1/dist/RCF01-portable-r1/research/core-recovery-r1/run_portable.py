#!/usr/bin/env python3
"""Portable RCF01-R1 entrypoint. Uses only packaged relative dependencies."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path


def run(cmd, cwd: Path, timeout: int = 180) -> dict:
    started = time.perf_counter()
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return {
        "cmd": cmd,
        "cwd": str(cwd),
        "exit_code": proc.returncode,
        "seconds": round(time.perf_counter() - started, 4),
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--skip-starter", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    out = args.output_dir
    if out.exists():
        print(json.dumps({"status": "FAIL", "error": "output dir exists; choose a fresh path"}))
        return 2
    out.mkdir(parents=True)

    env = root / "experiments" / "core_recovery_bridge_01_r1"
    work = out / "work"
    work.mkdir()
    jobs = []
    jobs.append(run(
        [sys.executable, "-B", str(env / "check_envelope.py"),
         "--output", str(out / "envelope_r1.json"),
         "--work", str(work / "env"),
         "--control", "none"],
        cwd=env,
    ))
    for control in ("omit", "duplicate", "unexpected", "reorder"):
        jobs.append(run(
            [sys.executable, "-B", str(env / "check_envelope.py"),
             "--output", str(out / f"envelope_r1_{control}.json"),
             "--work", str(work / f"env_{control}"),
             "--control", control],
            cwd=env,
        ))
    ids = root / "research" / "core-recovery-01"
    jobs.append(run([sys.executable, "-B", str(ids / "check_ids.py")], cwd=ids))
    export = root / "research" / "core-recovery-r1" / "check_export.py"
    jobs.append(run(
        [sys.executable, "-B", str(export), "--root", str(root), "--layout", "export"],
        cwd=root,
    ))
    if not args.skip_starter:
        starter = root / "RPRM-CORE-FORMALIZATION-01"
        if (starter / "check_bridge.py").is_file():
            jobs.append(run(
                [sys.executable, "-B", str(starter / "check_bridge.py"),
                 "--output", str(out / "starter_replay.json")],
                cwd=starter,
            ))
        else:
            jobs.append({"cmd": ["starter"], "exit_code": None, "stdout": "",
                         "stderr": "starter checker not packaged", "seconds": 0})

    envelope_src = env / "prestige_envelope.py"
    protocol = env / "PROTOCOL.json"
    inherited = root / "experiments" / "core_recovery_bridge_01" / "PROTOCOL.json"
    summary = {
        "status": "PASS" if jobs[0]["exit_code"] == 0 else "FAIL",
        "python": sys.version,
        "platform": platform.platform(),
        "export_root": str(root),
        "envelope_source_sha256": sha(envelope_src),
        "protocol_sha256": sha(protocol),
        "inherited_protocol_sha256": sha(inherited),
        "rprm_core_sha256": sha(root / "rprm" / "core.py"),
        "jobs": jobs,
        "donor_replay": "NOT_REPLAYED; historical logs only",
    }
    (out / "portable_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "jobs": [{"cmd": j["cmd"][-1] if isinstance(j["cmd"], list) else j["cmd"],
                  "exit_code": j["exit_code"]} for j in jobs],
        "output": str(out),
    }))
    envelope_ok = jobs[0]["exit_code"] == 0
    omit_ok = jobs[1]["exit_code"] != 0
    dup_ok = jobs[2]["exit_code"] != 0
    unexpected_ok = jobs[3]["exit_code"] != 0
    reorder_ok = jobs[4]["exit_code"] == 0
    ids_ok = jobs[5]["exit_code"] == 0
    export_ok = jobs[6]["exit_code"] == 0
    ok = envelope_ok and omit_ok and dup_ok and unexpected_ok and reorder_ok and ids_ok and export_ok
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
