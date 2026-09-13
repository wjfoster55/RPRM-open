"""Run the bounded E5 continuation into a new directory, standard library only."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve()
    if out.exists():
        raise ValueError('Choose a new output directory.')
    for name in ('supplied_review','work','evidence'):
        protected=ROOT/name
        if out==protected or protected in out.parents:
            raise ValueError('Output cannot enter a preserved source/evidence directory.')
    out.mkdir(parents=True)
    stages=[('import','verify_import.py',['--output',str(out/'review_import.json')]),
            ('generator','generator_check.py',['--output',str(out/'generator.json')]),
            ('factors','bsd_factors.py',['--output',str(out/'bsd_factors.json')]),
            ('coordinates','coordinate_check.py',['--output',str(out/'coordinates.json')]),
            ('integration','final_check.py',['--input-dir',str(out),'--output',str(out/'final_check.json')])]
    report={'started_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
            'platform':platform.platform(),'commands':[],
            'scope':'Fresh bounded continuation computations; prior accepted analytic/descent proofs reused with source identity, not rerun. Cited theorems retain their written source audit.'}
    failed=False
    for label,filename,arguments in stages:
        script=ROOT/'work'/filename
        command=[sys.executable,'-B',str(script),*arguments]
        start=time.perf_counter()
        proc=subprocess.run(command,cwd=ROOT,capture_output=True,encoding='utf-8',errors='replace')
        (out/(label+'.stdout.txt')).write_text(proc.stdout,encoding='utf-8')
        (out/(label+'.stderr.txt')).write_text(proc.stderr,encoding='utf-8')
        report['commands'].append({'stage':label,'command':command,'exit_code':proc.returncode,
            'elapsed_seconds':time.perf_counter()-start,
            'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest()})
        print(label+': exit '+str(proc.returncode),flush=True)
        failed |= proc.returncode!=0
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    report['status']='EXECUTION_FAILURE' if failed else 'ALL_STAGES_COMPLETED'
    (out/'RUN.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return int(failed)


if __name__=='__main__':
    raise SystemExit(main())
