"""Validate this frozen handoff's files; does not execute research code."""
from __future__ import annotations
import argparse, hashlib, json, sys, zipfile
from pathlib import Path, PurePosixPath

REQUIRED = {
    'README.md', 'CODEX_START_HERE.md', 'CURRENT_STATE.md', 'WORK_QUEUE.json',
    'tasks/F1_FLUID_CLOSEOUT.md', 'tasks/AD1_SCOPED_CLAIM.md',
    'tasks/YM1_PHYSICAL_BRIDGE.md', 'accepted/C1_CLOSEOUT.md',
    'accepted/SAT02_M1_CLOSEOUT.md', 'source_access/FLUID_SOURCE_PLAN.json',
    'accepted/archives/RCF01-portable-codex-c1.zip',
    'accepted/archives/SAT02-portable-codex-m1.zip',
}
FORBIDDEN = {'.ttf', '.otf', '.woff', '.woff2', '.eot'}
def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
def check(root: Path) -> dict:
    errors=[]; checked=0; archives=0
    manifest=json.loads((root/'HANDOFF_MANIFEST.json').read_text(encoding='utf-8'))
    rows=manifest.get('files')
    if not isinstance(rows,list) or not rows:
        raise ValueError('Manifest has no file records')
    expected=set()
    for row in rows:
        name=row.get('path') if isinstance(row,dict) else None
        if not isinstance(name,str) or not name:
            errors.append('invalid manifest row');continue
        rel=PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts or '\\' in name or ':' in name or name in expected:
            errors.append('unsafe or duplicate path: '+name);continue
        expected.add(name)
        p=root.joinpath(*rel.parts)
        if not p.is_file() or p.is_symlink():
            errors.append('missing or symbolic file: '+name);continue
        if p.suffix.lower() in FORBIDDEN:errors.append('forbidden font file: '+name)
        data=p.read_bytes()
        if type(row.get('bytes')) is not int or len(data)!=row['bytes'] or digest(data)!=row.get('sha256'):
            errors.append('file identity mismatch: '+name)
        else:checked+=1
        if p.suffix.lower()=='.zip':
            with zipfile.ZipFile(p) as z:
                bad=z.testzip()
                if bad:errors.append('nested ZIP CRC mismatch: '+name+'!/'+bad)
            archives+=1
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != expected|{'HANDOFF_MANIFEST.json'}:
        errors.append('file set mismatch: '+repr(sorted(actual^(expected|{'HANDOFF_MANIFEST.json'}))))
    if not REQUIRED.issubset(expected):errors.append('missing required handoff files: '+repr(sorted(REQUIRED-expected)))
    queue=json.loads((root/'WORK_QUEUE.json').read_text(encoding='utf-8'))
    if queue.get('execution_order')!=['F1','AD1','YM1']:errors.append('unexpected active task order')
    if [t.get('id') for t in queue.get('tasks',[])]!=['F1','AD1','YM1']:errors.append('unexpected active task IDs')
    return {'status':'FAIL' if errors else 'PASS','scope':'transfer integrity only; no research checks executed',
            'files_checked':checked,'nested_archives_crc_checked':archives,'errors':errors}
def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();root=args.root.resolve()
    if args.output and (args.output.resolve()==root or root in args.output.resolve().parents):
        raise SystemExit('Write validation output outside the frozen handoff directory.')
    try:result=check(root)
    except Exception as exc:result={'status':'FAIL','scope':'transfer integrity only','errors':[type(exc).__name__+': '+str(exc)]}
    text=json.dumps(result,indent=2);print(text)
    if args.output:
        if args.output.exists():raise SystemExit('Refusing to overwrite an existing validation receipt.')
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text+'\n',encoding='utf-8')
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__':
    sys.exit(main())
