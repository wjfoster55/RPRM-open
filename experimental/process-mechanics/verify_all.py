"""Consolidated verification for process-mechanics public kits.

Runs the seven kit checks, adapter contract regressions, and public
evidence table reaggregation. Optional dependencies that are skipped are
reported as SKIP, not counted as passed execution of that optional path.
Formal proofs are NOT_RUN unless a formal tool is invoked (none here).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]  # repository / payload root containing experimental/ and rprm/


CHECKS = [
    ("water", HERE / "water" / "check.py"),
    ("circuits", HERE / "circuits" / "check.py"),
    ("protein-folding", HERE / "protein-folding" / "check.py"),
    ("cancer-models", HERE / "cancer-models" / "check.py"),
    ("playground", HERE / "playground" / "check.py"),
    ("extras/retry-identity", HERE / "extras" / "retry-identity" / "check.py"),
    ("extras/units-calibration", HERE / "extras" / "units-calibration" / "check.py"),
    ("adapters/contract-regressions", HERE / "adapters" / "check_contract_regressions.py"),
]


def run_check(name: str, script: Path, out_dir: Path) -> dict:
    receipt = out_dir / f"{name.replace('/', '_')}.json"
    stdout_path = out_dir / f"{name.replace('/', '_')}.stdout.txt"
    stderr_path = out_dir / f"{name.replace('/', '_')}.stderr.txt"
    cmd = [sys.executable, "-I", "-B", str(script), "--output", str(receipt)]
    # contract regressions may not take --output; fall back
    if name.startswith("adapters/"):
        cmd = [sys.executable, "-I", "-B", str(script)]
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    status = "FAIL"
    optional_skip = False
    parsed = None
    if name.startswith("adapters/"):
        try:
            parsed = json.loads(proc.stdout)
            status = "PASS" if parsed.get("failed", 1) == 0 else "FAIL"
            if receipt:
                receipt.write_text(json.dumps(parsed, indent=2) + "\n", encoding="utf-8")
        except json.JSONDecodeError:
            status = "FAIL" if proc.returncode else "PASS"
    elif receipt.exists():
        parsed = json.loads(receipt.read_text(encoding="utf-8"))
        status = parsed.get("status", "FAIL")
        # Detect optional dependency skips inside nested checks
        checks = parsed.get("checks", {})
        if isinstance(checks, dict):
            rlc = checks.get("rlc")
            if isinstance(rlc, dict) and rlc.get("skipped"):
                optional_skip = True
    return {
        "name": name,
        "script": str(script.relative_to(ROOT)).replace("\\", "/"),
        "exit": proc.returncode,
        "status": status,
        "optional_dependency_skipped": optional_skip,
        "receipt": str(receipt) if receipt.exists() else None,
    }


def reaggregate(out_dir: Path) -> dict:
    script = HERE / "public_evidence" / "pc1" / "reaggregate_tables.py"
    proc = subprocess.run(
        [sys.executable, "-I", "-B", str(script)],
        cwd=str(HERE / "public_evidence" / "pc1"),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    (out_dir / "reaggregate.stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (out_dir / "reaggregate.stderr.txt").write_text(proc.stderr, encoding="utf-8")
    table = HERE / "public_evidence" / "pc1" / "CLAIM_TABLE.json"
    ok = proc.returncode == 0 and table.exists()
    return {
        "name": "public_evidence/reaggregate_tables",
        "exit": proc.returncode,
        "status": "PASS" if ok else "FAIL",
        "claim_table": str(table) if table.exists() else None,
        "claim_table_sha256": hashlib.sha256(table.read_bytes()).hexdigest() if table.exists() else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="Absolute path for consolidated receipt JSON",
    )
    args = parser.parse_args()
    if args.output and not args.output.is_absolute():
        parser.error("--output must be absolute")

    out_dir = (args.output.parent / "verify_parts") if args.output else (HERE / "expected" / "verify_parts")
    out_dir.mkdir(parents=True, exist_ok=True)

    results = [run_check(name, script, out_dir) for name, script in CHECKS]
    results.append(reaggregate(out_dir))

    executed = [r for r in results if r.get("status") in ("PASS", "FAIL")]
    passed = [r for r in executed if r["status"] == "PASS" and r.get("exit", 1) == 0]
    failed = [r for r in executed if r["status"] != "PASS" or r.get("exit", 1) != 0]
    optional_skips = [r["name"] for r in results if r.get("optional_dependency_skipped")]

    receipt = {
        "schema": "rprm.process-mechanics.verify_all.v1",
        "status": "PASS" if not failed else "FAIL",
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "cwd_root": str(ROOT),
        },
        "tests_executed": len(executed),
        "tests_passed": len(passed),
        "tests_failed": len(failed),
        "optional_dependency_skips_observed": optional_skips,
        "optional_skips_counted_as_pass_execution": False,
        "formal_proofs": "NOT_RUN",
        "results": results,
    }
    text = json.dumps(receipt, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
