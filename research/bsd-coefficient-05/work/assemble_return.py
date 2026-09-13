"""Package the completed experiment; check bytes, not mathematical truth.

Usage: python -I -B work/assemble_return.py --output /new/path/return.zip
Run work/run_coefficient.py separately for fresh mathematical computation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    if output.exists() or root in output.parents:
        raise SystemExit("Use a new ZIP path outside the experiment directory")
    run_dir = root / "runs/final_validation"
    run = json.loads((run_dir / "RUN.json").read_text())
    if not all(job["completed"] for job in run["jobs"]):
        raise SystemExit("Final run contains an unfinished job")
    if sha(root / "runtime/gp64-2-17-4.exe") != run["gp_sha256"]:
        raise SystemExit("Runtime changed since final run")
    for name, digest in run["source_snapshot"].items():
        for path in (root / "work" / name, run_dir / "work" / name):
            if sha(path) != digest:
                raise SystemExit(f"Source changed: {path}")
    for job in run["jobs"]:
        if sha(run_dir / job["log"]) != job["sha256"]:
            raise SystemExit(f"Log changed: {job['name']}")
    for name, digest in run["evidence_sha256"].items():
        if sha(run_dir / "evidence" / name) != digest:
            raise SystemExit(f"Evidence changed: {name}")
    manifest_path = root / "MANIFEST.json"
    files = sorted(p for p in root.rglob("*") if p.is_file() and p != manifest_path)
    manifest = {
        "scope": "Byte integrity only; hashes do not prove mathematical claims",
        "final_run": "runs/final_validation/RUN.json",
        "files": {p.relative_to(root).as_posix(): sha(p) for p in files},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    files.append(manifest_path)
    with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, root.name + "/" + path.relative_to(root).as_posix())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise SystemExit("ZIP CRC failure")
        if len(archive.infolist()) != len(files):
            raise SystemExit("ZIP member count mismatch")
        for path in files:
            member = root.name + "/" + path.relative_to(root).as_posix()
            if archive.read(member) != path.read_bytes():
                raise SystemExit(f"ZIP byte mismatch: {member}")
    print(json.dumps({"zip": str(output), "sha256": sha(output),
                      "bytes": output.stat().st_size, "files": len(files),
                      "archive_byte_comparison": "VERIFIED"}, indent=2))


if __name__ == "__main__":
    main()
