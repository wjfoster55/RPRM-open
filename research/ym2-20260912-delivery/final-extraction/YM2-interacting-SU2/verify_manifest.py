"""Verify exactly the portable YM2 byte inventory, not its scientific truth."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys


def main():
    root=Path(__file__).resolve().parent
    spec=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
    errors=[]
    expected=set()
    for row in spec['files']:
        name=row['path']
        path=PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or ':' in name or '\\' in name or name in expected:
            errors.append('unsafe_or_duplicate:'+name)
            continue
        expected.add(name)
        local=root/path
        if not local.is_file() or local.is_symlink():
            errors.append('missing_or_symlink:'+name)
            continue
        data=local.read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
            errors.append('mismatch:'+name)
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'}
    if actual != expected:
        errors.append('file_set_mismatch:'+repr(sorted(actual^expected)))
    print(json.dumps(dict(status='FAIL' if errors else 'PASS',files=len(expected),errors=errors),indent=2))
    return 1 if errors else 0


if __name__=='__main__':
    sys.exit(main())
