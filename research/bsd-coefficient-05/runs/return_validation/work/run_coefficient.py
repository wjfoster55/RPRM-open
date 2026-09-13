"""Fresh source snapshot, exact GP analytic calculations and rational readback."""
import argparse
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import time

def digest(p):return sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--gp',type=Path)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    target=args.output.resolve()
    if target.exists():raise FileExistsError('Use a fresh run directory')
    gp=args.gp or (root/'runtime/gp64-2-17-4.exe' if os.name=='nt' else Path(shutil.which('gp') or 'gp'))
    gp=gp.resolve()
    if not gp.is_file():raise FileNotFoundError('Supply a PARI/GP2.17.4 executable with --gp')
    target.mkdir(parents=True)
    for name in ('work','logs','evidence'):(target/name).mkdir()
    names=('coefficient.gp','padic_height.py','rational_ec.py','readback.py','run_coefficient.py')
    for name in names:shutil.copyfile(root/'work'/name,target/'work'/name)
    bootstrap=('import runpy,sys; from pathlib import Path; '
               'p=Path(sys.argv[1]).resolve(); sys.path.insert(0,str(p.parent)); '
               'sys.argv=sys.argv[1:]; runpy.run_path(str(p),run_name="__main__")')
    py=[sys.executable,'-I','-B','-c',bootstrap]
    jobs=[('analytic',[str(gp),'-q','-f','-s','256M','-D','parisizemax=1000000000',str(target/'work/coefficient.gp')]),
          ('arithmetic',py+[str(target/'work/padic_height.py'),'--output','evidence/padic_height.json']),
          ('readback',py+[str(target/'work/readback.py'),'--gp-log','logs/analytic.log',
                          '--height','evidence/padic_height.json','--output','evidence/coefficient_readback.json'])]
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
            'gp_executable':str(gp),'gp_sha256':digest(gp),
            'source_snapshot':{n:digest(target/'work'/n) for n in names},
            'saved_computational_PASS_used_as_input':False,
            'status':'RUNNING','jobs':[],'full_BSD':'OPEN','total_Sha':'OPEN'}
    begin=time.monotonic()
    for label,command in jobs:
        before=time.monotonic()
        p=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=300)
        payload=p.stdout+p.stderr;log=target/'logs'/f'{label}.log'
        log.write_text(payload,encoding='utf-8')
        ok=p.returncode==0 and (label!='analytic' or ('END_EXACT_COEFFICIENT_05' in payload and '***' not in payload))
        report['jobs'].append({'name':label,'exit_code':p.returncode,'completed':ok,
                               'elapsed_seconds':time.monotonic()-before,
                               'log':log.relative_to(target).as_posix(),'sha256':digest(log)})
        print(f'{label}: completed={ok}',flush=True)
        if not ok:report['status']='OPEN_FAILED_OBLIGATION_PRESERVED';break
    else:report['status']='ANALYTIC_COEFFICIENT_AND_INDEPENDENT_READBACK_VERIFIED'
    report['elapsed_seconds']=time.monotonic()-begin
    report['evidence_sha256']={p.name:digest(p) for p in (target/'evidence').glob('*.json')}
    (target/'RUN.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','elapsed_seconds','full_BSD','total_Sha')},indent=2))
    if report['status']!='ANALYTIC_COEFFICIENT_AND_INDEPENDENT_READBACK_VERIFIED':raise SystemExit(1)

if __name__=='__main__':main()
