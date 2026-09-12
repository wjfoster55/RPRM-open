#!/usr/bin/env python3
"""Build the RCF01-R1 portable ZIP from this workspace. No secrets, no traversal."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent / "dist"
STAGING_NAME = "RCF01-portable-r1"
SKIP_NAMES = {".env", "credentials.json", ".git"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refuse_outside(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    resolved.relative_to(root.resolve())
    if resolved.is_symlink():
        raise RuntimeError(f"symlink refused: {path}")
    return resolved


FILES = [
    "CONTENTS.md",
    "research/core-recovery-01/README.md",
    "research/core-recovery-01/RETURN_TO_WILLIAM.md",
    "research/core-recovery-01/DONOR_RECONCILIATION.md",
    "research/core-recovery-01/FORMAL_BRIDGE_NOTE.md",
    "research/core-recovery-01/CONCEPT_REGISTER.md",
    "research/core-recovery-01/CONCEPT_REGISTER.json",
    "research/core-recovery-01/CONCEPT_REGISTER.source.md",
    "research/core-recovery-01/check_ids.py",
    "research/core-recovery-01/provenance/STARTER_PROTOCOL.json",
    "research/core-recovery-01/sources/RPRM-CONCEPT-RECOVERY.zip",
    "research/core-recovery-r1/STATUS_CORRECTIONS.md",
    "research/core-recovery-r1/README.md",
    "research/core-recovery-r1/check_export.py",
    "research/core-recovery-r1/run_portable.py",
    "research/core-recovery-r1/build_export.py",
    "experiments/core_recovery_bridge_01/README.md",
    "experiments/core_recovery_bridge_01/prestige_envelope.py",
    "experiments/core_recovery_bridge_01/check_envelope.py",
    "experiments/core_recovery_bridge_01/PROTOCOL.json",
    "experiments/core_recovery_bridge_01/PROOFS.md",
    "experiments/core_recovery_bridge_01/runs/cursor_rcf01_envelope.json",
    "experiments/core_recovery_bridge_01/runs/cursor_rcf01_envelope_02.json",
    "experiments/core_recovery_bridge_01/runs/env_control_omit.json",
    "experiments/core_recovery_bridge_01/runs/env_control_duplicate.json",
    "experiments/core_recovery_bridge_01/runs/env_control_unexpected.json",
    "experiments/core_recovery_bridge_01/runs/env_control_reorder.json",
    "experiments/core_recovery_bridge_01/runs/donor_fiving_verify.txt",
    "experiments/core_recovery_bridge_01/runs/donor_double_stamp_verify.txt",
    "experiments/core_recovery_bridge_01/runs/donor_graded_scar.txt",
    "experiments/core_recovery_bridge_01/runs/donor_ternary_bridge.txt",
    "experiments/core_recovery_bridge_01/runs/donor_prestige_examples.txt",
    "experiments/core_recovery_bridge_01_r1/README.md",
    "experiments/core_recovery_bridge_01_r1/prestige_envelope.py",
    "experiments/core_recovery_bridge_01_r1/check_envelope.py",
    "experiments/core_recovery_bridge_01_r1/PROTOCOL.json",
    "experiments/core_recovery_bridge_01_r1/PROTOCOL.inherited.json",
    "experiments/core_recovery_bridge_01_r1/PROOFS.md",
    "experiments/core_recovery_bridge_01_r1/runs/envelope_r1.json",
    "experiments/core_recovery_bridge_01_r1/runs/envelope_r1_02.json",
    "experiments/core_recovery_bridge_01_r1/runs/envelope_r1_omit.json",
    "experiments/core_recovery_bridge_01_r1/runs/envelope_r1_duplicate.json",
    "experiments/core_recovery_bridge_01_r1/runs/envelope_r1_unexpected.json",
    "experiments/core_recovery_bridge_01_r1/runs/envelope_r1_reorder.json",
    "rprm/__init__.py",
    "rprm/core.py",
    "RPRM-CORE-FORMALIZATION-01/CURSOR_START_HERE.md",
    "RPRM-CORE-FORMALIZATION-01/README.md",
    "RPRM-CORE-FORMALIZATION-01/check_bridge.py",
    "RPRM-CORE-FORMALIZATION-01/PROTOCOL.json",
    "RPRM-CORE-FORMALIZATION-01/MANIFEST.json",
    "RPRM-CORE-FORMALIZATION-01/runs/cursor_rcf01_starter.json",
    "RPRM-CORE-FORMALIZATION-01/runs/control_omit.json",
    "RPRM-CORE-FORMALIZATION-01/runs/control_duplicate.json",
    "RPRM-CORE-FORMALIZATION-01/runs/control_unexpected.json",
    "RPRM-CORE-FORMALIZATION-01/runs/control_reorder.json",
]

OPTIONAL = [
    "research/core-recovery-r1/RETURN_TO_WILLIAM_R1.md",
    "research/core-recovery-r1/INVENTORY.md",
    "research/core-recovery-r1/provenance/source_identities.json",
    "research/core-recovery-r1/CLEANROOM_REPLAY.json",
]

REVIEW_ROOT = Path(r"C:\Users\bkbee\Downloads\RCF01-REVIEW-01_extract\RCF01-REVIEW-01")
REVIEW_FILES = [
    "CURSOR_REVIEW_REPAIR.md",
    "REVIEW.md",
    "README.md",
    "MANIFEST.json",
    "review_extra_checks.py",
]


def copy_file(src: Path, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    data = dest.read_bytes()
    return {"path": str(dest), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    out_dir = args.out_dir
    if out_dir.exists():
        raise SystemExit("out-dir already exists; choose a fresh successor directory")
    staging = out_dir / STAGING_NAME
    staging.mkdir(parents=True)
    manifest_files = {}
    missing = []
    for rel in FILES:
        src = refuse_outside(REPO, REPO / rel)
        if src.name in SKIP_NAMES:
            raise RuntimeError(f"secret-like name refused: {rel}")
        if not src.is_file():
            missing.append(rel)
            continue
        dest = staging / rel
        refuse_outside(staging, dest.parent)
        info = copy_file(src, dest)
        manifest_files[rel.replace("\\", "/")] = {"bytes": info["bytes"], "sha256": sha256(dest)}
    for rel in OPTIONAL:
        src = REPO / rel
        if src.is_file():
            dest = staging / rel
            copy_file(src, dest)
            manifest_files[rel.replace("\\", "/")] = {"bytes": dest.stat().st_size, "sha256": sha256(dest)}
        else:
            missing.append(rel + " (optional, not yet present)")
    review_dest = staging / "review" / "RCF01-REVIEW-01"
    for name in REVIEW_FILES:
        src = REVIEW_ROOT / name
        if not src.is_file():
            missing.append(f"review/{name}")
            continue
        dest = review_dest / name
        copy_file(src, dest)
        key = f"review/RCF01-REVIEW-01/{name}"
        manifest_files[key] = {"bytes": dest.stat().st_size, "sha256": sha256(dest)}
    shutil.copy2(REPO / "research" / "core-recovery-r1" / "run_portable.py", staging / "run_portable.py")
    manifest_files["run_portable.py"] = {
        "bytes": (staging / "run_portable.py").stat().st_size,
        "sha256": sha256(staging / "run_portable.py"),
    }
    readme = staging / "README.md"
    readme.write_text(
        "# RCF01 portable export R1\n\n"
        "Clean-room replay (from this extracted directory, existing Python only):\n\n"
        "    python -B run_portable.py --output-dir runs/cleanroom_01\n\n"
        "This package includes the frozen original envelope (`experiments/core_recovery_bridge_01`)\n"
        "and the successor repair (`experiments/core_recovery_bridge_01_r1`).\n"
        "The bundled `review/` directory is the external review source, not independent\n"
        "confirmation of the new prototype.\n",
        encoding="utf-8",
    )
    manifest_files["README.md"] = {"bytes": readme.stat().st_size, "sha256": sha256(readme)}
    payload = {
        "package": "RCF01-portable-r1",
        "inherits": "RCF01-envelope-1",
        "not_retroactive_preregistration": True,
        "workspace_head_recorded": "4f5c8145a1d9389f28079ef63a385e406122fd34",
        "files": manifest_files,
        "missing_optional_or_unavailable": missing,
        "non_replayable_donors": [
            "experiments/core_recovery_bridge_01/runs/donor_*.txt are historical local logs; donor trees are not packaged"
        ],
    }
    (staging / "MANIFEST.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    zip_path = out_dir / "RCF01-portable-r1.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(staging.rglob("*")):
            if path.is_dir():
                continue
            refuse_outside(staging, path)
            if path.is_symlink() or stat.S_ISLNK(path.lstat().st_mode):
                raise RuntimeError(f"symlink refused in zip: {path}")
            zf.write(path, path.relative_to(staging).as_posix())
    print(json.dumps({
        "zip": str(zip_path),
        "sha256": sha256(zip_path),
        "files": len(manifest_files),
        "missing": missing,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
