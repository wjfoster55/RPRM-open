"""Check recorded source/log bytes and package the bounded experiment."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import zipfile


def digest(p):return sha256(p.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1];out=args.output.resolve()
    if out.exists() or root in out.parents: raise ValueError('Use a new ZIP path outside experiment')
    run=root/'runs/fresh_validation'
    receipt=json.loads((run/'RUN.json').read_text())
    assert all(j['completed'] for j in receipt['jobs'])
    for name,h in receipt['source_hashes'].items():
        assert digest(run/'work'/name)==h
        current=root/('dependencies' if name.startswith('operational_numbers/') else 'work')/name
        assert digest(current)==h
    for job in receipt['jobs']:
        assert digest(run/'logs'/f"{job['name']}.log")==job['log_sha256']
    for filename,source in [('column_handoff.json','evidence/column_handoff_initial_source.py'),
                            ('column_handoff_extended.json','work/column_handoff.py')]:
        assert json.loads((root/'evidence'/filename).read_text())['source_sha256']==digest(root/source)
    manifest=root/'MANIFEST.json'
    paths=sorted(p for p in root.rglob('*') if p.is_file() and p!=manifest)
    manifest.write_text(json.dumps({'scope':'Byte integrity only; not mathematical proof',
                         'files':{p.relative_to(root).as_posix():digest(p) for p in paths}},indent=2)+'\n',encoding='utf-8')
    paths.append(manifest)
    with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED) as z:
        for p in paths:z.write(p,root.name+'/'+p.relative_to(root).as_posix())
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None and len(z.infolist())==len(paths)
        for p in paths:assert z.read(root.name+'/'+p.relative_to(root).as_posix())==p.read_bytes()
    print(json.dumps({'zip':str(out),'sha256':digest(out),'bytes':out.stat().st_size,
                      'files':len(paths),'archive_byte_comparison':'VERIFIED'},indent=2))


if __name__=='__main__':main()
