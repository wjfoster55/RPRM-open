"""Reproduce the new operational adapter and height calculations from source."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    target=args.output.resolve()
    if target.exists():raise FileExistsError('Use a fresh run directory')
    source=Path(__file__).resolve().parents[1]
    target.mkdir(parents=True)
    sources={}
    for folder in ('work','input_source'):
        (target/folder).mkdir()
        for p in sorted((source/folder).glob('*.py')):
            destination=target/folder/p.name
            shutil.copyfile(p,destination)
            sources[destination.relative_to(target).as_posix()]=digest(destination)
    (target/'evidence').mkdir();(target/'logs').mkdir()
    bootstrap=('import runpy,sys; from pathlib import Path; '
               'p=Path(sys.argv[1]).resolve(); sys.path.insert(0,str(p.parent)); '
               'sys.argv=sys.argv[1:]; runpy.run_path(str(p),run_name="__main__")')
    jobs=[('height','padic_height.py',['--output','evidence/padic_height.json']),
          ('independent_height','padic_height_readback.py',
           ['--witness','evidence/padic_height.json','--output','evidence/padic_height_readback.json']),
          ('arithmetic_vector','bockstein_readout.py',
           ['--height-witness','evidence/padic_height.json','--output','evidence/bockstein_readout.json']),
          ('operational_shadow','operational_shadow.py',
           ['--output','evidence/operational_shadow.json'])]
    report={'created_utc':datetime.now(timezone.utc).isoformat(),
            'python':sys.version,'executable':sys.executable,'source_snapshot':sources,
            'saved_evidence_copied_as_input':False,'jobs':[],
            'status':'RUNNING','full_BSD':'OPEN','total_Sha':'OPEN'}
    start=time.monotonic()
    for label,name,arguments in jobs:
        command=[sys.executable,'-I','-B','-c',bootstrap,str(target/'work'/name),*arguments]
        before=time.monotonic()
        p=subprocess.run(command,cwd=target,text=True,encoding='utf-8',errors='replace',
                         stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log=target/'logs'/f'{label}.log'
        log.write_text(p.stdout,encoding='utf-8')
        report['jobs'].append({'name':label,'exit_code':p.returncode,
                               'elapsed_seconds':time.monotonic()-before,
                               'log':log.relative_to(target).as_posix(),'log_sha256':digest(log)})
        print(f'{label}: exit {p.returncode}',flush=True)
        if p.returncode:
            report['status']='OPEN_FAILED_OBLIGATION_PRESERVED'
            break
    else:
        report['status']='ALL_NEW_EXACT_CALCULATIONS_VERIFIED'
        h=json.loads((target/'evidence/padic_height.json').read_text())
        s=json.loads((target/'evidence/operational_shadow.json').read_text())
        v=json.loads((target/'evidence/bockstein_readout.json').read_text())
        report['MST_determinant_mod5']=h['MST_determinant_mod5']
        report['operational_partition_counts']=s['partition_refinement_class_counts']
        report['W_div5_coordinates_mod5']=v['W_div5_coordinates_mod5']
    report['elapsed_seconds']=time.monotonic()-start
    report['evidence_files']={p.relative_to(target).as_posix():digest(p)
                              for p in sorted((target/'evidence').glob('*.json'))}
    (target/'RUN.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','elapsed_seconds','full_BSD','total_Sha')},indent=2))
    if report['status']!='ALL_NEW_EXACT_CALCULATIONS_VERIFIED':raise SystemExit(1)


if __name__=='__main__':main()
