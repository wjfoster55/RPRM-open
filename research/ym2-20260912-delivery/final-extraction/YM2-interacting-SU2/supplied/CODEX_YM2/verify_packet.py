"""Validate this handoff's byte inventory; not a scientific checker."""
from pathlib import Path, PurePosixPath
import hashlib,json,sys
root=Path(__file__).resolve().parent
spec=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
errors=[]; expected=set()
for row in spec['files']:
    rel=row['path']; q=PurePosixPath(rel)
    if q.is_absolute() or '..' in q.parts or rel in expected:
        errors.append('unsafe_or_duplicate:'+rel);continue
    expected.add(rel);p=root/rel
    if not p.is_file() or p.is_symlink(): errors.append('missing_or_symlink:'+rel);continue
    b=p.read_bytes()
    if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:errors.append('mismatch:'+rel)
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'}
if actual!=expected:errors.append('file_set_mismatch:'+repr(sorted(actual^expected)))
print(json.dumps({'status':'FAIL' if errors else 'PASS','files':len(expected),'errors':errors},indent=2))
sys.exit(1 if errors else 0)
