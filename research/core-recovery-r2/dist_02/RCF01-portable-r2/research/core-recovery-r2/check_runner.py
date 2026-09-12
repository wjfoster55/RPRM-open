#!/usr/bin/env python3
"""Fault-injection check of the ACTUAL portable runner, not a math-suite replay.

Copies the package and replaces expensive mathematical subjobs with explicitly
labelled fixtures. Tests aggregation/error handling in run_portable.py.
These harness runs are not mathematical replays or additional theorem tests.
Use alongside, not instead of, the unmodified full replay.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ENVELOPE_FIXTURE = r'''
import argparse, json, sys
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument("--output")
p.add_argument("--work")
p.add_argument("--control", default="none")
a = p.parse_args()
fail = a.control in ("omit", "duplicate", "unexpected")
if a.control == "omit":
    coverage_error = "Coverage mismatch: missing={'PE28_GENERIC_MAP_INTERFACE'}, extra=set()"
elif a.control == "duplicate":
    coverage_error = "Coverage mismatch: missing={'PE28_GENERIC_MAP_INTERFACE'}, extra=set()"
elif a.control == "unexpected":
    coverage_error = "Coverage mismatch: missing={'PE28_GENERIC_MAP_INTERFACE'}, extra={'UNDECLARED'}"
else:
    coverage_error = None
status = "FAIL" if fail else "PASS"
payload = {
    "status": status,
    "control": a.control,
    "coverage_error": coverage_error,
    "scope": "AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION",
    "results": [{"case_id": "FIXTURE", "outcome": "PASS" if not fail else "FAIL"}],
}
Path(a.output).write_text(json.dumps(payload) + "\n", encoding="utf-8")
print(json.dumps({"status": status, "scope": "AGGREGATOR FIXTURE"}))
sys.exit(2 if fail else 0)
'''

CRASH_FIXTURE = r'''
import argparse, json, sys
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument("--output")
p.add_argument("--work")
p.add_argument("--control", default="none")
a = p.parse_args()
if a.control in ("omit", "duplicate", "unexpected"):
    raise RuntimeError("INJECTED UNRELATED CHILD CRASH; not a coverage rejection")
payload = {
    "status": "PASS",
    "control": a.control,
    "coverage_error": None,
    "scope": "AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION",
    "results": [{"case_id": "FIXTURE", "outcome": "PASS"}],
}
Path(a.output).write_text(json.dumps(payload) + "\n", encoding="utf-8")
print("fixture successful")
'''

STARTER_SUCCESS = r'''
import argparse, json
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument("--output")
a = p.parse_args()
payload = {
    "status": "PASS",
    "coverage_error": None,
    "scope": "AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION",
    "results": [{"case_id": "STARTER_FIXTURE", "outcome": "PASS"}],
}
Path(a.output).write_text(json.dumps(payload) + "\n", encoding="utf-8")
print(json.dumps({"status": "PASS", "scope": "AGGREGATOR FIXTURE"}))
'''

IDS_PASS = r'''
import json
print(json.dumps({"status": "PASS", "ids": ["RCF-P1"], "count": 13, "scope": "AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION"}))
'''

EXPORT_PASS = r'''
import argparse, json
p = argparse.ArgumentParser()
p.add_argument("--root")
p.add_argument("--layout")
a = p.parse_args()
print(json.dumps({"status": "PASS", "layout": a.layout, "scope": "AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION"}))
'''

EXPORT_FAIL = r'''
import json, sys
print(json.dumps({"status": "FAIL", "error": "AGGREGATOR FIXTURE export failure"}))
sys.exit(2)
'''


def run_case(out: Path, package: Path, case: str, env: dict) -> dict:
    root = out / case / "package"
    shutil.copytree(package, root)
    env_script = root / "experiments" / "core_recovery_bridge_01_r2" / "check_envelope.py"
    starter_script = root / "RPRM-CORE-FORMALIZATION-01" / "check_bridge.py"
    export_script = root / "research" / "core-recovery-r2" / "check_export.py"
    ids_script = root / "research" / "core-recovery-01" / "check_ids.py"
    if case == "negative_control_unrelated_crash":
        env_script.write_text(CRASH_FIXTURE, encoding="utf-8")
    else:
        env_script.write_text(ENVELOPE_FIXTURE, encoding="utf-8")
    if case == "starter_failure":
        starter_script.write_text("raise SystemExit(7)\n", encoding="utf-8")
    else:
        starter_script.write_text(STARTER_SUCCESS, encoding="utf-8")
    ids_script.write_text(IDS_PASS, encoding="utf-8")
    if case == "export_failure":
        export_script.write_text(EXPORT_FAIL, encoding="utf-8")
    else:
        export_script.write_text(EXPORT_PASS, encoding="utf-8")
    command = [sys.executable, "-B", str(root / "run_portable.py"),
               "--output-dir", str(root.parent / "run")]
    if case == "skip_starter":
        command.append("--skip-starter")
    result = subprocess.run(command, cwd=out, env=env, capture_output=True, text=True, timeout=30)
    (root.parent / "stdout.txt").write_text(result.stdout, encoding="utf-8")
    (root.parent / "stderr.txt").write_text(result.stderr, encoding="utf-8")
    summary_path = root.parent / "run" / "portable_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.is_file() else None
    printed = None
    try:
        printed = json.loads(result.stdout.strip().splitlines()[-1])
    except Exception:
        printed = {"parse_error": True, "stdout": result.stdout[-500:]}
    return {
        "case": case,
        "command": command,
        "exit_code": result.returncode,
        "reported_status": None if summary is None else summary.get("status"),
        "printed_status": None if not isinstance(printed, dict) else printed.get("status"),
        "reported_scope": None if summary is None else summary.get("reported_scope"),
        "job_exit_codes": None if summary is None else [
            {"name": item.get("job_name"), "exit_code": item.get("exit_code")}
            for item in summary.get("jobs", [])
        ],
        "verdict_failures": None if summary is None else summary.get("verdict", {}).get("failures"),
        "scope": "AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION",
    }


def expected_ok(row: dict) -> tuple[bool, str]:
    case = row["case"]
    status = row["reported_status"]
    printed = row["printed_status"]
    exit_code = row["exit_code"]
    if status != printed:
        return False, "JSON status and printed status disagree"
    if case in ("good_run", "skip_starter"):
        if not (status == "PASS" and exit_code == 0):
            return False, "good/skip run must PASS with exit 0"
        if case == "skip_starter" and row.get("reported_scope") != "envelope_controls_ids_export_starter_skipped":
            return False, "skip-starter must report the narrower scope"
        if case == "skip_starter":
            names = [item["name"] for item in row["job_exit_codes"] or []]
            if "starter" in names:
                return False, "skip-starter still executed starter"
        return True, "PASS"
    if status != "FAIL" or exit_code == 0:
        return False, "injected fault must FAIL with nonzero exit"
    failed_jobs = " ".join(
        f"{item.get('job', '')} {item.get('reason', '')}"
        for item in row.get("verdict_failures") or []
    )
    if case == "starter_failure":
        if "starter" not in failed_jobs:
            return False, "starter failure was not named in the verdict"
        return True, "starter counted"
    if case == "export_failure":
        if "export" not in failed_jobs:
            return False, "export failure was not named in the verdict"
        return True, "export counted"
    if case == "negative_control_unrelated_crash":
        if "coverage-rejection" in failed_jobs or "missing output" in failed_jobs or "malformed" in failed_jobs:
            return True, "crash distinguished from coverage rejection"
        if any(name in failed_jobs for name in ("omit", "duplicate", "unexpected")):
            return True, "negative control distinguished"
        return False, "crash was not distinguished from coverage rejection"
    return False, "unknown case"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    report = {
        "scope": (
            "Actual run_portable.py exercised in disposable copies with explicitly "
            "substituted fast mathematical subjobs; NOT a rerun of mathematical cases. "
            "Unmodified full replay is separate. Fixture checker/export/id scripts are "
            "labelled AGGREGATOR FIXTURE and are not hashed by check_export.py."
        ),
        "cases": [],
    }
    all_ok = True
    for case in (
        "good_run",
        "starter_failure",
        "export_failure",
        "negative_control_unrelated_crash",
        "skip_starter",
    ):
        row = run_case(out, args.package.resolve(), case, env)
        ok, reason = expected_ok(row)
        row["harness_ok"] = ok
        row["harness_reason"] = reason
        report["cases"].append(row)
        all_ok = all_ok and ok
    report["status"] = "PASS" if all_ok else "FAIL"
    (out / "runner_controls.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
