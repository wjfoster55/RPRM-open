"""Run the existing RPRM translator read-only, retaining reports and source hashes."""
from pathlib import Path
import subprocess
import sys
import json
import hashlib
from datetime import datetime,timezone

root=Path(__file__).resolve().parents[1]
source=Path('C:/github/RPRMLexicon/operational_numbers')
target=root/'evidence/translator'
if target.exists(): raise FileExistsError('Preserve prior translator evidence')
target.mkdir(parents=True)
report={'created_utc':datetime.now(timezone.utc).isoformat(),'source_root':str(source),
        'source_hashes':{n:hashlib.sha256((source/n).read_bytes()).hexdigest()
                         for n in ('translate_number.py','carrier_lexer.py','verify.py','readings.json')},'jobs':[]}
jobs=[('verify',[sys.executable,'-B',str(source/'verify.py')])]
for name,value in (('lower','2.0339867006'),('upper','2.0340237084'),('34','34'),('35','35'),('pi','31415926535')):
    command=[sys.executable,'-B',str(source/'translate_number.py'),value,'--scout','--compact']
    if name=='pi':command+=['--profile','pi-window']
    jobs.append((name,command))
for name,command in jobs:
    p=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
    file=target/(name+('.log' if name=='verify' else '.json'))
    file.write_text(p.stdout,encoding='utf-8')
    if p.stderr:(target/(name+'.stderr.log')).write_text(p.stderr,encoding='utf-8')
    report['jobs'].append({'name':name,'exit_code':p.returncode,'output':file.name,
                          'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    print(name+': '+str(p.returncode),flush=True)
    if p.returncode:
        report['status']='FAILED_OBLIGATION_PRESERVED';break
else:report['status']='FRESH_TRANSLATOR_RUN_COMPLETED'
(target/'RUN.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
if report['status']!='FRESH_TRANSLATOR_RUN_COMPLETED': raise SystemExit(1)
