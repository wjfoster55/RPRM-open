#!/usr/bin/env python3
"""Portable RCF01-R2 entrypoint. Uses only packaged relative dependencies."""
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


def parse_json_blob(text: str):
    text = (text or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        if start < 0:
            return None
        try:
            return json.loads(text[start:])
        except json.JSONDecodeError:
            return None


def load_json_file(path: Path):
    if path is None or not path.is_file():
        return None, "missing output"
    try:
        return json.loads(path.read_text(encoding="utf-8")), "ok"
    except json.JSONDecodeError:
        return None, "malformed output"


def check_pass_receipt(job: dict, path: Path) -> tuple[bool, str]:
    if job["exit_code"] != 0:
        return False, f"exit {job['exit_code']}"
    payload, state = load_json_file(path)
    if state != "ok":
        return False, state
    if payload.get("status") != "PASS":
        return False, f"status {payload.get('status')}"
    if payload.get("coverage_error"):
        return False, "unexpected coverage_error"
    if "results" in payload and not isinstance(payload.get("results"), list):
        return False, "malformed results"
    return True, "PASS receipt"


COVERAGE_REJECTION_MARKERS = (
    "Coverage mismatch",
    "Duplicate emitted case IDs",
    "Duplicate required protocol IDs",
    "Malformed result schema",
)


def check_coverage_rejection(job: dict, path: Path) -> tuple[bool, str]:
    if job["exit_code"] in (None, 0):
        return False, "coverage rejection requires a nonzero exit"
    payload, state = load_json_file(path)
    if state != "ok":
        return False, state
    if payload.get("status") != "FAIL":
        return False, "status is not FAIL"
    err = payload.get("coverage_error")
    if not isinstance(err, str) or not any(marker in err for marker in COVERAGE_REJECTION_MARKERS):
        return False, "missing coverage-rejection receipt"
    return True, "coverage rejection"


def check_stdout_pass(job: dict) -> tuple[bool, str]:
    if job["exit_code"] != 0:
        return False, f"exit {job['exit_code']}"
    payload = parse_json_blob(job.get("stdout") or "")
    if not isinstance(payload, dict) or payload.get("status") != "PASS":
        return False, "stdout is not a PASS record"
    return True, "PASS record"


def named_job(name: str, kind: str, result: dict, output: Path | None = None) -> dict:
    rec = dict(result)
    rec["job_name"] = name
    rec["kind"] = kind
    rec["output_path"] = str(output) if output is not None else None
    return rec


def evaluate_jobs(jobs: list[dict], starter_included: bool) -> dict:
    failures = []
    checks = []
    by_name = {job["job_name"]: job for job in jobs}

    def record(name: str, ok: bool, reason: str) -> None:
        checks.append({"job": name, "ok": ok, "reason": reason})
        if not ok:
            failures.append({"job": name, "reason": reason})

    envelope = by_name["envelope"]
    ok, reason = check_pass_receipt(envelope, Path(envelope["output_path"]))
    record("envelope", ok, reason)

    for name in ("omit", "duplicate", "unexpected"):
        job = by_name[name]
        ok, reason = check_coverage_rejection(job, Path(job["output_path"]))
        record(name, ok, reason)

    reorder = by_name["reorder"]
    ok, reason = check_pass_receipt(reorder, Path(reorder["output_path"]))
    record("reorder", ok, reason)

    ok, reason = check_stdout_pass(by_name["ids"])
    record("ids", ok, reason)

    ok, reason = check_stdout_pass(by_name["export"])
    record("export", ok, reason)

    if starter_included:
        starter = by_name["starter"]
        out = starter.get("output_path")
        if starter.get("exit_code") is None or not out:
            record("starter", False, "starter checker missing or produced no receipt")
        else:
            ok, reason = check_pass_receipt(starter, Path(out))
            record("starter", ok, reason)

    status = "PASS" if not failures else "FAIL"
    scope = "envelope_controls_ids_export_starter" if starter_included else "envelope_controls_ids_export_starter_skipped"
    return {
        "status": status,
        "reported_scope": scope,
        "starter_included": starter_included,
        "checks": checks,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--skip-starter", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    out = args.output_dir
    if not out.is_absolute():
        out = (root / out).resolve()
    if out.exists():
        print(json.dumps({"status": "FAIL", "error": "output dir exists; choose a fresh path"}))
        return 2
    out.mkdir(parents=True)

    env = root / "experiments" / "core_recovery_bridge_01_r2"
    work = out / "work"
    work.mkdir()
    jobs = []
    envelope_out = out / "envelope_r2.json"
    jobs.append(named_job("envelope", "envelope_pass", run(
        [sys.executable, "-B", str(env / "check_envelope.py"),
         "--output", str(envelope_out),
         "--work", str(work / "env"),
         "--control", "none"],
        cwd=env,
    ), envelope_out))
    for control in ("omit", "duplicate", "unexpected", "reorder"):
        control_out = out / f"envelope_r2_{control}.json"
        jobs.append(named_job(control, "envelope_control", run(
            [sys.executable, "-B", str(env / "check_envelope.py"),
             "--output", str(control_out),
             "--work", str(work / f"env_{control}"),
             "--control", control],
            cwd=env,
        ), control_out))
    ids = root / "research" / "core-recovery-01"
    jobs.append(named_job("ids", "ids", run(
        [sys.executable, "-B", str(ids / "check_ids.py")], cwd=ids,
    )))
    export = root / "research" / "core-recovery-r2" / "check_export.py"
    jobs.append(named_job("export", "export", run(
        [sys.executable, "-B", str(export), "--root", str(root), "--layout", "export"],
        cwd=root,
    )))
    starter_included = not args.skip_starter
    if starter_included:
        starter = root / "RPRM-CORE-FORMALIZATION-01"
        starter_out = out / "starter_replay.json"
        if (starter / "check_bridge.py").is_file():
            jobs.append(named_job("starter", "starter", run(
                [sys.executable, "-B", str(starter / "check_bridge.py"),
                 "--output", str(starter_out)],
                cwd=starter,
            ), starter_out))
        else:
            jobs.append(named_job("starter", "starter", {
                "cmd": ["starter"], "exit_code": None, "stdout": "",
                "stderr": "starter checker not packaged", "seconds": 0,
            }))

    verdict = evaluate_jobs(jobs, starter_included)
    envelope_src = env / "prestige_envelope.py"
    protocol = env / "PROTOCOL.json"
    inherited = root / "experiments" / "core_recovery_bridge_01_r1" / "PROTOCOL.json"
    original = root / "experiments" / "core_recovery_bridge_01" / "PROTOCOL.json"
    summary = {
        "status": verdict["status"],
        "reported_scope": verdict["reported_scope"],
        "starter_included": starter_included,
        "verdict": verdict,
        "python": sys.version,
        "platform": platform.platform(),
        "export_root": str(root),
        "envelope_source_sha256": sha(envelope_src),
        "protocol_sha256": sha(protocol),
        "inherited_r1_protocol_sha256": sha(inherited),
        "inherited_original_protocol_sha256": sha(original),
        "rprm_core_sha256": sha(root / "rprm" / "core.py"),
        "jobs": jobs,
        "donor_replay": "NOT_REPLAYED; historical logs only",
    }
    (out / "portable_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": verdict["status"],
        "reported_scope": verdict["reported_scope"],
        "jobs": [{"name": j["job_name"], "cmd": j["cmd"][-1] if isinstance(j["cmd"], list) else j["cmd"],
                  "exit_code": j["exit_code"]} for j in jobs],
        "failures": verdict["failures"],
        "output": str(out),
    }))
    return 0 if verdict["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
