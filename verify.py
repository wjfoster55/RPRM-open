"""Run fresh repository checks; no downloaded packages or cached results.

Python 3.10+ and Node.js 18+ are required for the default suite. Supply --lean
with a Lean 4.22.0 executable to additionally recheck the formal declarations.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
NODE_CHECKS = (
    ("atlas", "checks/atlas/verify.js"),
    ("atlas_view", "checks/atlas/view-checks.js"),
    ("rule_lab_model", "experimental/rule-lab/model.test.cjs"),
    ("rule_lab_presentation", "experimental/rule-lab/presentation.test.cjs"),
)


def source_snapshot():
    excluded = {".git", ".artifacts", "__pycache__", ".venv", "node_modules"}
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(ROOT.rglob("*")) if p.is_file()
            and not excluded.intersection(p.relative_to(ROOT).parts)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", help="Lean 4.22.0 executable; omitted formal checks are recorded NOT_RUN")
    parser.add_argument("--python-only", action="store_true", help="Explicitly omit all four Node checks: Atlas model/view and Rule Lab model/presentation")
    args = parser.parse_args()
    output = ROOT / ".artifacts"
    output.mkdir(exist_ok=True)
    # The lock serializes writers of the aggregate pointer. If a process is
    # killed, its PENDING pointer and lock remain visibly incomplete.
    lock = output / "verification.lock"
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        parser.error("Another run owns .artifacts/verification.lock. If it has stopped, remove that lock and rerun.")
    os.close(descriptor)
    try:
        return run_requested(args, parser, output)
    finally:
        lock.unlink()


def run_requested(args, parser, output):
    run_id = str(uuid.uuid4())
    work = output / "runs" / run_id
    work.mkdir(parents=True)
    receipt = {"schema": "rprm-replay/v1", "run_id": run_id, "status": "PENDING",
               "started_utc": datetime.now(timezone.utc).isoformat(),
               "formal": "REQUESTED" if args.lean else "NOT_RUN", "atlas": "NOT_RUN" if args.python_only else "REQUESTED",
               "node": "NOT_RUN" if args.python_only else "REQUESTED",
               "node_suites": [name for name, _ in NODE_CHECKS],
               "checks": {}, "scope": "Fresh execution of the explicitly requested suites. See each receipt's coverage."}
    def publish():
        temporary = output / (run_id + ".tmp")
        payload = json.dumps(receipt, indent=2) + "\n"
        temporary.write_text(payload, encoding="utf-8")
        os.replace(temporary, output / "verification.json")
        (work / "verification.json").write_text(payload, encoding="utf-8")
    publish()
    before = source_snapshot()
    receipt["source_hashes"] = before
    jobs = [(name, [sys.executable, "-I", "-B", str(ROOT / "checks" / (name + ".py"))])
            for name in ("core", "unification", "futures", "proof_donut", "fermat", "prime_frontier")]
    jobs += [("experimental_" + name.replace("-", "_"),
              [sys.executable, "-I", "-B", str(ROOT / "experimental" / name / "check.py")])
             for name in ("primes", "ray-tracing", "music", "protein-folding", "context-communication")]
    jobs.append(("experimental_two_path", [sys.executable, "-I", "-B", str(ROOT / "experimental/two-path-lab/test_model.py")]))
    formal_jobs = [("formal", [sys.executable, "-I", "-B", str(ROOT / "checks/formal.py"), "--lean", args.lean])] if args.lean else []
    receipt["requested_checks"] = ([name for name, _ in jobs]
                                   + ([] if args.python_only else [name for name, _ in NODE_CHECKS])
                                   + [name for name, _ in formal_jobs])
    receipt["checks"] = {name: {"status": "PENDING"} for name in receipt["requested_checks"]}
    if not args.lean:
        receipt["checks"]["formal"] = {"status": "NOT_RUN", "reason": "Supply --lean to request formal checking"}
    if args.python_only:
        for name, _ in NODE_CHECKS:
            receipt["checks"][name] = {"status": "NOT_RUN", "reason": "Omitted by --python-only"}
    publish()
    if not args.python_only:
        node = shutil.which("node")
        if node is None:
            for name in receipt["requested_checks"]:
                receipt["checks"][name] = {"status": "NOT_RUN", "reason": "Node.js missing; no child suites started"}
            for name, _ in NODE_CHECKS:
                receipt["checks"][name] = {"status": "FAIL", "error": "Required Node.js runtime missing"}
            receipt.update(status="FAIL", node="FAIL", atlas="FAIL", formal="NOT_RUN", error="Node.js missing",
                           source_unchanged=before == source_snapshot(), finished_utc=datetime.now(timezone.utc).isoformat())
            publish()
            parser.error("Node.js is required for Atlas and Rule Lab verification; --python-only requests a limited run")
        jobs.extend((name, [node, str(ROOT / path)]) for name, path in NODE_CHECKS)
    jobs.extend(formal_jobs)
    for name, command in jobs:
        destination = work / (name + ".json")
        # A failed process must never leave an older PASS looking current.
        destination.write_text(json.dumps({"status": "PENDING"}) + "\n", encoding="utf-8")
        command += ["--output", str(destination)]
        try:
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", check=False, timeout=900)
            (work / (name + ".log")).write_text(run.stdout + run.stderr, encoding="utf-8")
            result = json.loads(destination.read_text(encoding="utf-8"))
            passed = run.returncode == 0 and result.get("status") == "PASS"
            if not passed:
                destination.write_text(json.dumps({"status": "FAIL", "run_id": run_id,
                    "returncode": run.returncode, "child_result": result}, indent=2) + "\n", encoding="utf-8")
            receipt["checks"][name] = {"status": "PASS" if passed else "FAIL", "returncode": run.returncode,
                                      "receipt": destination.relative_to(ROOT).as_posix(),
                                      "receipt_sha256": hashlib.sha256(destination.read_bytes()).hexdigest()}
            if not passed:
                print(run.stdout + run.stderr)
        except Exception as error:
            receipt["checks"][name] = {"status": "FAIL", "error": type(error).__name__ + ": " + str(error)}
            destination.write_text(json.dumps({"status": "FAIL", "run_id": run_id,
                "error": receipt["checks"][name]["error"]}, indent=2) + "\n", encoding="utf-8")
        print(name + ": " + receipt["checks"][name]["status"], flush=True)
        publish()
    receipt["status"] = "PASS" if all(receipt["checks"][name]["status"] == "PASS" for name, _ in jobs) else "FAIL"
    receipt["source_unchanged"] = before == source_snapshot()
    if not receipt["source_unchanged"]:
        receipt.update(status="FAIL", error="Repository source changed during replay")
    for optional in ("formal", "atlas"):
        if optional in receipt["checks"]:
            receipt[optional] = receipt["checks"][optional]["status"]
    if not args.python_only:
        receipt["node"] = "PASS" if all(receipt["checks"][name]["status"] == "PASS" for name, _ in NODE_CHECKS) else "FAIL"
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    publish()
    print("Requested suites: " + receipt["status"] + "; formal=" + receipt["formal"] + "; node=" + receipt["node"] + "; atlas=" + receipt["atlas"])
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
