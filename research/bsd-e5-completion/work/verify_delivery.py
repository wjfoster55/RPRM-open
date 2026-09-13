"""Check delivered bytes against the final inventory; not a mathematics verifier."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
inventory=json.loads((ROOT/'DELIVERY_INVENTORY.json').read_text(encoding='utf-8'))
seen=set()
for row in inventory['files']:
    path=(ROOT/row['path']).resolve()
    assert ROOT in path.parents and row['path'] not in seen
    seen.add(row['path'])
    data=path.read_bytes()
    assert len(data)==row['size'] and hashlib.sha256(data).hexdigest()==row['sha256']
print(json.dumps({'status':'BYTES_MATCH','files':len(seen),'scope':'Integrity only; execute work/run_all.py for fresh finite computations.'}))
