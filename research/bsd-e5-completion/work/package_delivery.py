"""Package this single E5 continuation after all files are final."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
target=args.output.resolve()
assert not target.exists() and ROOT not in target.parents
rows=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p==ROOT/'DELIVERY_INVENTORY.json':
        continue
    if '__pycache__' in p.parts or p.suffix=='.pyc':
        continue
    raw=p.read_bytes()
    rows.append({'path':p.relative_to(ROOT).as_posix(),'size':len(raw),
                 'sha256':hashlib.sha256(raw).hexdigest()})
inventory={'generated_utc':datetime.now(timezone.utc).isoformat(),'files':rows,
    'exclusions':['This inventory itself','Python caches, if any'],
    'scope':'Byte identities only; theorem dependencies and exact evidence are separately stated.'}
(ROOT/'DELIVERY_INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
prefix='BSD_E5_COMPLETION_RETURN/'
with ZipFile(target,'x',compression=ZIP_DEFLATED,compresslevel=9) as z:
    for row in rows:
        z.write(ROOT/row['path'],prefix+row['path'])
    z.write(ROOT/'DELIVERY_INVENTORY.json',prefix+'DELIVERY_INVENTORY.json')
with ZipFile(target) as z:
    assert z.testzip() is None
    expected={prefix+r['path'] for r in rows}|{prefix+'DELIVERY_INVENTORY.json'}
    assert set(z.namelist())==expected and len(z.namelist())==len(expected)
    for row in rows:
        raw=z.read(prefix+row['path'])
        assert len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    assert z.read(prefix+'DELIVERY_INVENTORY.json')==(ROOT/'DELIVERY_INVENTORY.json').read_bytes()
sha=hashlib.sha256(target.read_bytes()).hexdigest()
target.with_suffix(target.suffix+'.sha256').write_text(sha+'  '+target.name+'\n',encoding='ascii')
print(json.dumps({'status':'PACKAGED_AND_BYTE_VERIFIED','path':str(target),
                  'members':len(rows)+1,'size':target.stat().st_size,'sha256':sha},indent=2))
