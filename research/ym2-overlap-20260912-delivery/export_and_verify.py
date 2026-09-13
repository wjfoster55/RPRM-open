"""Freeze final new packet, fresh-extract, and execute only its new checker."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import struct
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "ym2_overlap_cover"
ZIP = HERE / "YM2-overlap-cover-2026-09-12.zip"
EXTRACT = HERE / "final-extraction"
ROOT = "YM2-overlap-cover"

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def inventory(p):
    return [{"path": f.relative_to(p).as_posix(), "bytes": f.stat().st_size,
             "sha256": digest(f)} for f in sorted(p.rglob("*")) if f.is_file()]

def main():
    need(not ZIP.exists() and not EXTRACT.exists(), "Final output already exists")
    provenance = json.loads((SOURCE/"SOURCE_PROVENANCE.json").read_text(encoding="utf-8"))
    for archive in provenance["archives"]:
        need(digest(Path(archive["path"])) == archive["sha256"], "Accepted archive changed")
    for row in provenance["files"]:
        need(digest(SOURCE/row["payload_path"]) == row["sha256"], "Accepted copy changed")
    need((SOURCE/"INDEPENDENT_REVIEW.md").is_file(), "Independent review absent")
    need((SOURCE/"VISUAL_CHECKS.md").is_file(), "Visual review absent")
    links = []
    for note in SOURCE.glob("*.md"):
        prose = re.sub(r"```[\s\S]*?```", "", note.read_text(encoding="utf-8"))
        prose = re.sub(r"`[^`\n]*`", "", prose)
        for raw in re.findall(r"\]\(([^)]+)\)", prose):
            if raw.startswith(("https://", "http://", "#")):
                continue
            target = (note.parent/raw.split("#")[0]).resolve()
            need(target.is_relative_to(SOURCE.resolve()) and target.is_file(),
                 "Nonportable top-level link " + note.name + ": " + raw)
            links.append({"note": note.name, "target": target.relative_to(SOURCE).as_posix()})
    dims = struct.unpack(">II", (SOURCE/"overlap_cover.png").read_bytes()[16:24])
    need(dims == (3200, 1600), "Figure dimensions")
    need(all("__pycache__" not in f.parts for f in SOURCE.rglob("*")), "Bytecode in payload")
    rows = [r for r in inventory(SOURCE) if r["path"] != "MANIFEST.json"]
    (SOURCE/"MANIFEST.json").write_text(json.dumps({"schema": "ym2-overlap-manifest-v1",
          "self_excluded": "MANIFEST.json", "files": rows}, indent=2)+"\n", encoding="utf-8")
    frozen = inventory(SOURCE)
    with zipfile.ZipFile(ZIP, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for row in frozen:
            z.write(SOURCE/row["path"], ROOT+"/"+row["path"])
    zip_sha = digest(ZIP)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ZIP) as z:
        need(z.testzip() is None, "CRC failure")
        need(len(z.namelist()) == len(set(z.namelist())) == len(frozen), "Member census")
        for name in z.namelist():
            need((EXTRACT/name).resolve().is_relative_to(EXTRACT.resolve()), "Unsafe member path")
        z.extractall(EXTRACT)
    target = EXTRACT/ROOT
    need(inventory(target) == frozen, "Fresh extraction byte mismatch")
    need(json.loads((target/"MANIFEST.json").read_text(encoding="utf-8"))["files"] == rows,
         "Manifest mismatch")
    command = [sys.executable, "-I", "-B", "-X", "utf8", str(target/"check_overlap.py")]
    done = subprocess.run(command, cwd=target, capture_output=True, text=True, encoding="utf-8", timeout=55)
    stdout = HERE/"check_overlap.stdout.txt"
    stderr = HERE/"check_overlap.stderr.txt"
    stdout.write_text(done.stdout, encoding="utf-8")
    stderr.write_text(done.stderr, encoding="utf-8")
    need(done.returncode == 0 and not done.stderr and "PASS" in done.stdout,
         "Extracted new checker failed: "+done.stderr)
    need(inventory(target) == frozen == inventory(SOURCE), "Replay changed frozen bytes")
    need(digest(ZIP) == zip_sha, "ZIP changed")
    for archive in provenance["archives"]:
        need(digest(Path(archive["path"])) == archive["sha256"], "Prior archive changed after replay")
    result = {"schema": "ym2-overlap-final-export-v1", "status": "PASS",
        "utc": datetime.now(timezone.utc).isoformat(), "archive": str(ZIP),
        "archive_sha256": zip_sha, "archive_bytes": ZIP.stat().st_size,
        "payload_files": len(frozen), "payload_bytes": sum(r["bytes"] for r in frozen),
        "manifest_covered_files": len(rows), "zip_crc": "PASS",
        "fresh_extraction": str(target), "source_equals_extracted": True,
        "unchanged_after_replay": True, "command": command, "cwd": str(target),
        "exit_code": done.returncode, "stdout_file": stdout.name,
        "stdout_sha256": digest(stdout), "stderr_bytes": 0, "python_version": sys.version,
        "accepted_snapshots": len(provenance["files"]), "prior_archives_unchanged": provenance["archives"],
        "top_level_file_links_checked": len(links), "link_records": links,
        "historical_link_scope": "Accepted byte-exact snapshots retain historical relative links; complete deep historical navigation is not asserted. Prior final ZIP included.",
        "figure_dimensions": dims, "receipt": json.loads((target/"RESULTS.json").read_text(encoding="utf-8")),
        "old_checkers_executed": False,
        "evidence_ceiling": "Written proofs with independent agent audits and bounded exact corroboration; export evidence binds bytes/execution, not mathematical truth or continuum existence."}
    (HERE/"FINAL_EXPORT_EVIDENCE.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (HERE/"YM2-overlap-cover-2026-09-12.sha256").write_text(zip_sha+"  "+ZIP.name+"\n", encoding="ascii")
    (HERE/"FINAL_EXPORT_EVIDENCE.md").write_text(f"""# Final export evidence — PASS

Archive: `{ZIP.name}`  
SHA-256: `{zip_sha}`  
Bytes: {ZIP.stat().st_size}; payload files: {len(frozen)}.

The final ZIP passed CRC, duplicate-name and extraction-path checks. A
fresh extraction matched every frozen source byte and the manifest.
The extracted new checker recomputed and compared the complete saved
receipt under isolated Python with UTF-8 and bytecode disabled. It exited
zero with empty stderr. All source, extracted and archive bytes remained
unchanged after replay. No old checker was executed.

The new controls passed {result['receipt']['assertions']} exact assertions,
including all 384 cube spanning trees, optimal finite cover weights,
six direction-grid instances, duplicate and nonphysical controls,
rational isometry/IMS calculations and free inverse multipliers.
The general mathematical conclusions rely on the written proofs and
two independent agent audits; the finite controls do not prove them alone.

All {len(links)} top-level local file links resolve within the portable
packet. All {len(provenance['files'])} accepted snapshots match their
recorded source bytes. Both prior archives remain unchanged. Accepted
notes keep historical links and context; full deep historical navigation
is outside this export check. The preceding final archive is included.

The 3200 by 1600 explanatory PNG was visually inspected. The SVG and
plotting source are included. It plots proved bounds, not simulation data.

FINAL_EXPORT_EVIDENCE.json records commands, interpreter, output hashes,
paths, source-archive hashes, the full new receipt and link records.
Actual stdout and stderr files are adjacent. This sidecar was generated
after freezing and replaying the ZIP; it establishes byte and execution
integrity, not independent mathematical certification.
""", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["status", "archive", "archive_sha256", "archive_bytes", "payload_files", "top_level_file_links_checked"]}, indent=2))
    print(done.stdout.strip())

if __name__ == "__main__":
    main()
