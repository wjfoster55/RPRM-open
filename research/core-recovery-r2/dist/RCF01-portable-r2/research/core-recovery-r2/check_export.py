#!/usr/bin/env python3
"""Package-completeness and record check for an RCF01-R2 portable export.

This is not a mathematical refutation tool. ID coverage remains in
research/core-recovery-01/check_ids.py. A disposable mutation that strips
meanings or deletes packaged sources must fail here without rewriting
historical mathematical results.

Does not hash-pin the envelope checker bytes, so a runner-fixture
substitution of check_envelope.py still reaches the aggregation boundary
rather than failing this integrity check first.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REQUIRED_IDS = [
    "RCF-P1", "RCF-P2", "RCF-P3", "RCF-F1", "RCF-F2", "RCF-F3",
    "RCF-C1", "RCF-C2", "RCF-C3", "RCF-N1", "RCF-R1", "RCF-PI1", "RCF-AD1",
]
REQUIRED_FIELDS = (
    "original_meaning",
    "source_anchors",
    "formal_candidate",
    "evidence_status",
    "unformalized_remainder",
)
DEFERRED_MARKERS = ("DEFERRED", "NOT_RUN")


def fail(message: str) -> None:
    raise ValueError(message)


def nonempty(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return len(value) > 0
    return True


def resolve_in_tree(root: Path, link: str) -> Path:
    if not isinstance(link, str) or not link.strip():
        fail("empty artifact link")
    raw = Path(link)
    if raw.is_absolute():
        fail(f"absolute artifact link refused: {link}")
    if ".." in Path(link).parts:
        fail(f"path traversal refused: {link}")
    target = (root / link).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        fail(f"artifact escapes export root: {link}")
    if target.is_symlink():
        fail(f"symlink artifact refused: {link}")
    return target


def inspect_register(root: Path, register: Path) -> dict:
    payload = json.loads(register.read_text(encoding="utf-8"))
    entries = payload.get("entries")
    if not isinstance(entries, list):
        fail("register entries missing")
    ids = [entry.get("id") for entry in entries]
    if ids != REQUIRED_IDS:
        fail(f"ID set drifted: {ids}")
    if len(ids) != len(set(ids)):
        fail("duplicate IDs")
    missing_fields = []
    missing_artifacts = []
    deferred = []
    executed_ok = []
    for entry in entries:
        if not isinstance(entry, dict):
            fail("entry is not an object")
        cid = entry["id"]
        for field in REQUIRED_FIELDS:
            if not nonempty(entry.get(field)):
                missing_fields.append({"id": cid, "field": field})
        status = str(entry.get("evidence_status") or "")
        remainder = entry.get("unformalized_remainder")
        if remainder is None:
            missing_fields.append({"id": cid, "field": "unformalized_remainder"})
        is_deferred = any(marker in status for marker in DEFERRED_MARKERS)
        if is_deferred:
            deferred.append(cid)
            continue
        links = entry.get("artifact_links") or []
        if not isinstance(links, list) or not links:
            missing_artifacts.append({"id": cid, "reason": "no artifact_links"})
            continue
        for link in links:
            target = resolve_in_tree(root, link)
            if not target.is_file():
                missing_artifacts.append({"id": cid, "link": link, "exists": False})
            else:
                executed_ok.append({"id": cid, "link": link})
    if missing_fields:
        fail(f"empty required fields: {missing_fields}")
    if missing_artifacts:
        fail(f"executed-claim artifacts missing: {missing_artifacts}")
    return {
        "ids": ids,
        "deferred": deferred,
        "executed_artifact_ok": executed_ok,
        "files_present_boolean_not_accepted": True,
    }


def inspect_packaged_tree(root: Path) -> dict:
    required = [
        "run_portable.py",
        "MANIFEST.json",
        "research/core-recovery-01/CONCEPT_REGISTER.json",
        "research/core-recovery-01/CONCEPT_REGISTER.source.md",
        "research/core-recovery-01/check_ids.py",
        "research/core-recovery-01/sources/RPRM-CONCEPT-RECOVERY.zip",
        "experiments/core_recovery_bridge_01/prestige_envelope.py",
        "experiments/core_recovery_bridge_01/check_envelope.py",
        "experiments/core_recovery_bridge_01/PROTOCOL.json",
        "experiments/core_recovery_bridge_01/PROOFS.md",
        "experiments/core_recovery_bridge_01/runs/cursor_rcf01_envelope.json",
        "experiments/core_recovery_bridge_01/runs/cursor_rcf01_envelope_02.json",
        "experiments/core_recovery_bridge_01_r1/prestige_envelope.py",
        "experiments/core_recovery_bridge_01_r1/check_envelope.py",
        "experiments/core_recovery_bridge_01_r1/PROTOCOL.json",
        "experiments/core_recovery_bridge_01_r1/runs/envelope_r1.json",
        "experiments/core_recovery_bridge_01_r1/runs/envelope_r1_02.json",
        "experiments/core_recovery_bridge_01_r2/prestige_envelope.py",
        "experiments/core_recovery_bridge_01_r2/check_envelope.py",
        "experiments/core_recovery_bridge_01_r2/PROTOCOL.json",
        "experiments/core_recovery_bridge_01_r2/PROTOCOL.inherited.json",
        "experiments/core_recovery_bridge_01_r2/runs/envelope_r2.json",
        "experiments/core_recovery_bridge_01_r2/runs/envelope_r2_02.json",
        "research/core-recovery-r1/check_export.py",
        "research/core-recovery-r2/check_export.py",
        "rprm/core.py",
        "rprm/__init__.py",
    ]
    missing = [path for path in required if not (root / path).is_file()]
    if missing:
        fail(f"packaged files missing: {missing}")
    for path in required:
        resolve_in_tree(root, path)
    return {"required_files": required, "missing": []}


def mutate(work: Path, control: str) -> None:
    register = work / "research" / "core-recovery-01" / "CONCEPT_REGISTER.json"
    if control == "id-only":
        payload = json.loads(register.read_text(encoding="utf-8"))
        skeletal = {"entries": [{"id": entry["id"]} for entry in payload["entries"]]}
        register.write_text(json.dumps(skeletal), encoding="utf-8")
        return
    if control == "missing-source":
        target = work / "experiments" / "core_recovery_bridge_01_r2" / "prestige_envelope.py"
        target.unlink()
        return
    if control == "missing-receipt":
        target = work / "experiments" / "core_recovery_bridge_01" / "runs" / "cursor_rcf01_envelope_02.json"
        target.unlink()
        return
    fail(f"unknown control {control}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--layout", choices=("export", "records"), default="export")
    parser.add_argument("--control", choices=("none", "id-only", "missing-source", "missing-receipt"),
                        default="none")
    parser.add_argument("--work", type=Path, default=None,
                        help="Disposable copy directory for mutation controls")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(json.dumps({"status": "FAIL", "error": "root is not a directory"}))
        return 2
    try:
        if args.control != "none":
            if args.layout != "export":
                fail("mutation controls require --layout export")
            if args.work is None:
                fail("--work is required for mutation controls")
            if args.work.exists():
                fail("work directory already exists; choose a fresh path")
            shutil.copytree(root, args.work, dirs_exist_ok=False)
            mutate(args.work, args.control)
            root = args.work.resolve()
        tree = None
        if args.layout == "export":
            tree = inspect_packaged_tree(root)
        register = inspect_register(root, root / "research" / "core-recovery-01" / "CONCEPT_REGISTER.json")
        report = {"status": "PASS", "control": args.control, "layout": args.layout,
                  "tree": tree, "register": register}
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "control": args.control, "error": f"{type(exc).__name__}: {exc}"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
