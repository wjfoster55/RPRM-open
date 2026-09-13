"""Freeze new handoff research, extract it freshly, and replay only its new checker."""
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import struct
import subprocess
import sys
import zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/"ym2_vacuum_handoff"
ZIP=HERE/"YM2-vacuum-handoff-2026-09-12.zip"
EXTRACT=HERE/"final-extraction"
ROOT="YM2-vacuum-handoff"

def need(ok,message):
    if not ok:raise RuntimeError(message)
def digest(p):return sha256(p.read_bytes()).hexdigest()
def inventory(p):
    return [{"path":f.relative_to(p).as_posix(),"bytes":f.stat().st_size,"sha256":digest(f)}
            for f in sorted(p.rglob("*")) if f.is_file()]

def main():
    need(not ZIP.exists() and not EXTRACT.exists(),"Final output already exists")
    prov=json.loads((SOURCE/"SOURCE_PROVENANCE.json").read_text(encoding="utf-8"))
    prior=Path(prov["prior_archive"])
    need(digest(prior)==prov["prior_archive_sha256"],"Prior archive changed")
    for row in prov["files"]:
        need(digest(SOURCE/row["payload_path"])==row["sha256"],"Accepted snapshot changed")
    need(digest(SOURCE/"TRIAL_REFERENCE.md")==prov["reviewed_trial_reference_sha256"],
         "Independently reviewed source changed")
    review=(SOURCE/"INDEPENDENT_REVIEW.md").read_text(encoding="utf-8")
    need(prov["reviewed_trial_reference_sha256"] in review.lower(),"Review source hash absent")
    need((SOURCE/"VISUAL_CHECKS.md").is_file(),"Visual review absent")
    links=[]
    for note in SOURCE.glob("*.md"):
        prose=re.sub(r"```[\s\S]*?```","",note.read_text(encoding="utf-8"))
        prose=re.sub(r"`[^`\n]*`","",prose)
        for raw in re.findall(r"\]\(([^)]+)\)",prose):
            if raw.startswith(("http://","https://","#")):continue
            target=(note.parent/raw.split("#")[0]).resolve()
            need(target.is_relative_to(SOURCE.resolve()) and target.is_file(),
                 "Nonportable new-note link "+note.name+": "+raw)
            links.append({"note":note.name,"target":target.relative_to(SOURCE).as_posix()})
    dims=struct.unpack(">II",(SOURCE/"vacuum_handoff.png").read_bytes()[16:24])
    need(dims==(3000,1400),"Figure dimensions")
    need(all("__pycache__" not in p.parts for p in SOURCE.rglob("*")),"Bytecode in payload")
    rows=[r for r in inventory(SOURCE) if r["path"]!="MANIFEST.json"]
    (SOURCE/"MANIFEST.json").write_text(json.dumps({"schema":"ym2-vacuum-handoff-manifest-v1",
        "self_excluded":"MANIFEST.json","files":rows},indent=2)+"\n",encoding="utf-8")
    frozen=inventory(SOURCE)
    with zipfile.ZipFile(ZIP,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for row in frozen:z.write(SOURCE/row["path"],ROOT+"/"+row["path"])
    zip_sha=digest(ZIP)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ZIP) as z:
        need(z.testzip() is None,"ZIP CRC failure")
        need(len(z.namelist())==len(set(z.namelist()))==len(frozen),"ZIP member census")
        for name in z.namelist():
            need((EXTRACT/name).resolve().is_relative_to(EXTRACT.resolve()),"Unsafe member path")
        z.extractall(EXTRACT)
    target=EXTRACT/ROOT
    need(inventory(target)==frozen,"Fresh extraction mismatch")
    need(json.loads((target/"MANIFEST.json").read_text(encoding="utf-8"))["files"]==rows,"Manifest mismatch")
    command=[sys.executable,"-I","-B","-X","utf8",str(target/"check_handoff.py")]
    done=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding="utf-8",timeout=55)
    stdout=HERE/"check_handoff.stdout.txt";stderr=HERE/"check_handoff.stderr.txt"
    stdout.write_text(done.stdout,encoding="utf-8");stderr.write_text(done.stderr,encoding="utf-8")
    need(done.returncode==0 and not done.stderr and "PASS" in done.stdout,"Extracted checker failed: "+done.stderr)
    need(inventory(target)==frozen==inventory(SOURCE),"Replay changed source/extracted bytes")
    need(digest(ZIP)==zip_sha,"ZIP changed after replay")
    need(digest(prior)==prov["prior_archive_sha256"],"Prior archive changed after replay")
    result={"schema":"ym2-vacuum-handoff-final-export-v1","status":"PASS",
        "utc":datetime.now(timezone.utc).isoformat(),"archive":str(ZIP),"archive_sha256":zip_sha,
        "archive_bytes":ZIP.stat().st_size,"payload_files":len(frozen),
        "payload_bytes":sum(r["bytes"] for r in frozen),"manifest_covered_files":len(rows),
        "zip_crc":"PASS","fresh_extraction":str(target),"source_equals_extracted":True,
        "unchanged_after_replay":True,"command":command,"cwd":str(target),"exit_code":done.returncode,
        "stdout_file":stdout.name,"stdout_sha256":digest(stdout),"stderr_bytes":0,
        "python_version":sys.version,"accepted_snapshots":len(prov["files"]),
        "prior_archive_sha256":prov["prior_archive_sha256"],"prior_archive_unchanged":True,
        "reviewed_trial_reference_sha256":prov["reviewed_trial_reference_sha256"],
        "top_level_file_links_checked":len(links),"link_records":links,"figure_dimensions":dims,
        "old_checkers_executed":False,"receipt":json.loads((target/"RESULTS.json").read_text(encoding="utf-8")),
        "evidence_ceiling":"Written derivations and independent agent review, with bounded exact controls. Hash/replay integrity does not certify general mathematical truth or an actual coupling-window extension."}
    (HERE/"FINAL_EXPORT_EVIDENCE.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    (HERE/"YM2-vacuum-handoff-2026-09-12.sha256").write_text(zip_sha+"  "+ZIP.name+"\n",encoding="ascii")
    (HERE/"FINAL_EXPORT_EVIDENCE.md").write_text(f"""# Final export evidence — PASS

Archive: `{ZIP.name}`  
SHA-256: `{zip_sha}`  
Bytes: {ZIP.stat().st_size}; payload files: {len(frozen)}.

The ZIP passed CRC, duplicate-name and extraction-path checks. A fresh
extraction matched every frozen source byte and the manifest. The new
checker recomputed and compared its complete saved receipt under isolated
Python, UTF-8 and bytecode suppression. It exited zero with empty stderr.
All source, extracted and archive bytes remained unchanged after replay.
No previous checker was executed.

The new controls passed {result['receipt']['assertions']} exact assertions:
8,000 weight triples, calibrated ratio maps, a residual-sensitive two-state
operator, chart composition, the shifted scalar majorant, plaquette
residual formulas and finite collective-dependence controls. The general
SU(2) statements rely on the written derivations and supplied prior
proofs. The trial-reference source matches the independent review's
recorded SHA-256 `{prov['reviewed_trial_reference_sha256']}`.

All {len(links)} top-level local file links resolve inside the packet.
All {len(prov['files'])} accepted snapshots match their source hashes.
The preceding frozen overlap archive remains unchanged and is included.
Accepted snapshots retain historical links; full deep historical
navigation is not asserted. Related task messages retain their source
status, including a provisional BSD update that was not adopted as proof.

The 3000 by 1400 explanatory PNG was visually inspected; SVG and source
are included. It is a diagram of identities, not simulation data.

FINAL_EXPORT_EVIDENCE.json records interpreter, commands, output hashes,
paths, source bindings, full new receipt and link records. Actual stdout
and stderr are adjacent. These sidecars were generated after freezing
and replaying the ZIP. They establish byte and execution integrity,
not a continuum mass-gap theorem or an enlarged actual YM window.
""",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ["status","archive","archive_sha256","archive_bytes","payload_files","top_level_file_links_checked"]},indent=2))
    print(done.stdout.strip())

if __name__=="__main__":main()
