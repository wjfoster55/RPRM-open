"""Fresh GP refinement, existing RPRM translator and complete finite map audit."""
import argparse
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--gp',type=Path)
    args=ap.parse_args();root=Path(__file__).resolve().parents[1]
    gp=(args.gp or root.parent/'bsd-coefficient-05/runtime/gp64-2-17-4.exe').resolve()
    if not gp.is_file(): raise FileNotFoundError('Supply PARI/GP 2.17.4 with --gp')
    target=args.output.resolve()
    if target.exists(): raise FileExistsError('Use a new output directory')
    target.mkdir(parents=True)
    for name in ('work','logs','evidence'): (target/name).mkdir()
    for name in ('refine.gp','operational_probe.py','run_probe.py'):
        shutil.copyfile(root/'work'/name,target/'work'/name)
    translator=root/'dependencies/operational_numbers'
    shutil.copytree(translator,target/'work/operational_numbers')
    py=[sys.executable,'-B']
    jobs=[('translator_verifier',py+[str(target/'work/operational_numbers/verify.py')]),
          ('analytic',[str(gp),'-q','-f','-s','256M',str(target/'work/refine.gp')]),
          ('finite_audit',py+[str(target/'work/operational_probe.py'),'--gp-log','logs/analytic.log','--output','evidence/operations.json'])]
    jobs += [(f'translator_{word}',py+[str(target/'work/operational_numbers/translate_number.py'),word,'--scout','--compact'])
             for word in ('426','625','624','46','35','325','1051','2301')]
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'gp_path':str(gp),
            'gp_sha256':digest(gp),'python':sys.version,'jobs':[],
            'source_hashes':{p.relative_to(target/'work').as_posix():digest(p) for p in (target/'work').rglob('*') if p.is_file()},
            'previous_PASS_used_as_computation_input':False,'status':'RUNNING'}
    begin=time.monotonic()
    for name,command in jobs:
        start=time.monotonic()
        result=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        payload=result.stdout+result.stderr
        log=target/'logs'/f'{name}.log';log.write_text(payload,encoding='utf-8')
        ok=result.returncode==0
        if name=='analytic': ok=ok and '***' not in payload and 'END_CARRY_KEY_06' in payload
        report['jobs'].append({'name':name,'exit_code':result.returncode,'completed':ok,
                               'elapsed_seconds':time.monotonic()-start,'log_sha256':digest(log)})
        print(f'{name}: {ok}',flush=True)
        if not ok:
            report['status']='FAILED_OBLIGATION_PRESERVED'
            break
    else:
        report['status']='COMPLETED_WITH_REFUTED_AND_SUPPORTED_CANDIDATES_RETAINED'
    report['elapsed_seconds']=time.monotonic()-begin
    (target/'RUN.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(report['status'])
    if report['status']=='FAILED_OBLIGATION_PRESERVED': raise SystemExit(1)


if __name__=='__main__':
    main()
