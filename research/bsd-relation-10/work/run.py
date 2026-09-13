"""Reproduce relation10 in a new output directory; Python3.10+, PARI/GP2.17.4."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--gp",type=Path,required=True)
    args=ap.parse_args(); target=args.output.resolve(); gp=args.gp.resolve()
    if target.exists(): raise FileExistsError("Use a new output directory")
    if not gp.is_file(): raise FileNotFoundError(gp)
    target.mkdir(parents=True)
    for name in ("work","logs","evidence"): (target/name).mkdir()
    source=Path(__file__).resolve().parent
    for name in ("analytic.gp","reciprocity.py","run.py"):
        shutil.copyfile(source/name,target/"work"/name)
    report={"created_utc":datetime.now(timezone.utc).isoformat(),"python":sys.version,
            "gp_executable":str(gp),"gp_sha256":digest(gp),
            "source_snapshot":{p.name:digest(p) for p in (target/"work").iterdir()},
            "saved_results_used_as_input":False,"jobs":[],"status":"RUNNING"}
    jobs=[("analytic",[str(gp),"-q","-f","-s","256M","-D","parisizemax=1000000000",str(target/"work/analytic.gp")]),
          ("reciprocity",[sys.executable,"-I","-B",str(target/"work/reciprocity.py"),
                          "--analytic-log",str(target/"logs/analytic.log"),"--output",str(target/"evidence/reciprocity.json")])]
    start=time.monotonic()
    for label,command in jobs:
        before=time.monotonic()
        try:
            p=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=300)
            payload=p.stdout+p.stderr; success=p.returncode==0 and "***" not in payload
            if label=="analytic": success=success and "END_RELATION_10_ANALYTIC" in payload
            code=p.returncode
        except subprocess.TimeoutExpired as e:
            payload="TIMEOUT\n"+str(e.stdout)+"\n"+str(e.stderr); success=False; code=None
        log=target/"logs"/f"{label}.log"; log.write_text(payload,encoding="utf-8")
        report["jobs"].append({"name":label,"exit_code":code,"success":success,"elapsed_seconds":time.monotonic()-before,"log_sha256":digest(log)})
        print(f"{label}: success={success}",flush=True)
        if not success:
            report["status"]="FAILED_OBLIGATION_PRESERVED"; break
    else: report["status"]="EXACT_FINITE_RELATION_VERIFIED"
    report["elapsed_seconds"]=time.monotonic()-start
    report["evidence_hashes"]={p.name:digest(p) for p in (target/"evidence").iterdir()}
    (target/"RUN.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    if report["status"]!="EXACT_FINITE_RELATION_VERIFIED": raise SystemExit(1)

if __name__=="__main__": main()
