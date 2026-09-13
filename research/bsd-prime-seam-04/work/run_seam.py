"""Replay all new prime-seam calculations from isolated fresh source copies."""
import argparse
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess
import sys
import time

def digest(path):return sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();target=args.output.resolve()
    if target.exists():raise FileExistsError('Use a fresh run directory')
    source=Path(__file__).resolve().parents[1]
    target.mkdir(parents=True)
    for name in ('work','evidence','logs'):(target/name).mkdir()
    for file in sorted((source/'work').glob('*.py')):shutil.copyfile(file,target/'work'/file.name)
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
            'executable':sys.executable,'status':'RUNNING','jobs':[],
            'source_snapshot':{f.name:digest(f) for f in sorted((target/'work').glob('*.py'))},
            'saved_computational_evidence_used_as_input':False,
            'prior_interval_used_only_as_countermodel_receiver':True,
            'full_BSD':'OPEN','total_Sha':'OPEN'}
    start=time.monotonic()
    jobs=[('local_seams','prime_seam.py',['--output','evidence/prime_seam.json']),
          ('independent_readback','seam_readback.py',['--witness','evidence/prime_seam.json',
                                                    '--output','evidence/seam_readback.json']),
          ('scale_obstruction','scale_obstruction.py',['--output','evidence/scale_obstruction.json'])]
    for label,name,arguments in jobs:
        before=time.monotonic()
        proc=subprocess.run([sys.executable,'-I','-B',str(target/'work'/name),*arguments],
                            cwd=target,text=True,encoding='utf-8',errors='replace',
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log=target/'logs'/f'{label}.log';log.write_text(proc.stdout,encoding='utf-8')
        report['jobs'].append({'name':label,'exit_code':proc.returncode,
                               'elapsed_seconds':time.monotonic()-before,
                               'log':log.relative_to(target).as_posix(),'log_sha256':digest(log)})
        print(f'{label}: exit {proc.returncode}',flush=True)
        if proc.returncode:
            report['status']='OPEN_FAILED_OBLIGATION_PRESERVED';break
    else:report['status']='ALL_THREE_NEW_CALCULATIONS_VERIFIED'
    report['elapsed_seconds']=time.monotonic()-start
    report['evidence_sha256']={f.name:digest(f) for f in sorted((target/'evidence').glob('*.json'))}
    (target/'RUN.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','elapsed_seconds','full_BSD','total_Sha')},indent=2))
    if report['status']!='ALL_THREE_NEW_CALCULATIONS_VERIFIED':raise SystemExit(1)

if __name__=='__main__':main()
