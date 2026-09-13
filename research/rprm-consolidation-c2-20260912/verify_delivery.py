"""Verify exported payload identities and replay only the four new bounded checks.

Write receipts outside the extracted payload. No network, installation, closed
suite replay, or source mutation. Python standard library + existing NumPy/Node.
"""
import argparse, hashlib, json, platform, subprocess, sys
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parent
CHECKS=[('F1','fluid/check_f1.py'),('F1_hostile','fluid/review/check_broadphase_hostile.py'),
        ('AD1','ad/check_ad1.py'),('YM1','yang_mills/check_ym1.py')]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);args=ap.parse_args()
    out=args.output_dir.resolve()
    if out==ROOT or ROOT in out.parents or out.exists():raise SystemExit('Use a fresh directory outside the payload')
    out.mkdir(parents=True)
    manifest=json.loads((ROOT/'DELIVERY_MANIFEST.json').read_text(encoding='utf-8'))
    errors=[];expected=set()
    for row in manifest['files']:
        rel=PurePosixPath(row['path'])
        if rel.is_absolute() or '..' in rel.parts or '\\' in row['path'] or ':' in row['path'] or row['path'] in expected:
            errors.append('unsafe/duplicate manifest path');continue
        expected.add(row['path']);p=ROOT.joinpath(*rel.parts)
        if not p.is_file() or p.is_symlink():errors.append('missing/linked '+str(rel));continue
        data=p.read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:errors.append('identity mismatch '+str(rel))
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    if actual != expected|{'DELIVERY_MANIFEST.json'}:errors.append('payload file set differs')
    # Copied input files must also match the preserved source ledger.
    for row in json.loads((ROOT/'provenance/PRESERVED_INPUTS.json').read_text(encoding='utf-8')):
        if hashlib.sha256((ROOT/row['delivery_path']).read_bytes()).hexdigest()!=row['sha256']:errors.append('preserved source mismatch '+row['delivery_path'])
    for acquisition in json.loads((ROOT/'provenance/FLUID_ACQUISITION.json').read_text(encoding='utf-8')):
        tree=json.loads((ROOT/f"provenance/{acquisition['pr']}_GIT_TREE.json").read_text(encoding='utf-8'))
        blobs={r['path']:r['sha'] for r in tree['tree'] if r['type']=='blob'}
        for row in acquisition['files']:
            p=ROOT/row['path'];data=p.read_bytes()
            rel=p.relative_to(ROOT/'fluid/sources'/acquisition['pr']).as_posix()
            if hashlib.sha256(data).hexdigest()!=row['sha256'] or hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=blobs[rel]:errors.append('fluid source mismatch '+row['path'])
    checks=[]
    if not errors:
        for name,entry in CHECKS:
            receipt=out/f'{name}.json'
            cmd=[sys.executable,'-I','-B',str(ROOT/entry),'--output',str(receipt)]
            proc=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
            (out/f'{name}.stdout.txt').write_text(proc.stdout,encoding='utf-8')
            (out/f'{name}.stderr.txt').write_text(proc.stderr,encoding='utf-8')
            result=json.loads(receipt.read_text(encoding='utf-8')) if receipt.exists() else {}
            ok=proc.returncode==0 and bool(result)
            if name=='F1':ok=ok and result.get('status')=='PASS'
            elif name=='F1_hostile':ok=ok and result.get('expected_hostile_observation_reproduced') is True
            else:ok=ok and result.get('status')=='PASS'
            checks.append({'name':name,'entrypoint':entry,'entrypoint_sha256':hashlib.sha256((ROOT/entry).read_bytes()).hexdigest(),
                           'command':cmd,'exit_code':proc.returncode,'receipt':receipt.name,'pass':ok})
            if not ok:errors.append(name+' replay failed')
    # Recheck content identity after all child processes; a passing receipt is not
    # permission to mutate the extracted source.
    for row in manifest['files']:
        if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:errors.append('post-run mutation '+row['path'])
    result={'status':'FAIL' if errors else 'PASS','payload_root':str(ROOT),'manifest_sha256':hashlib.sha256((ROOT/'DELIVERY_MANIFEST.json').read_bytes()).hexdigest(),
            'files_verified':len(expected),'python':sys.version,'platform':platform.platform(),'checks':checks,'errors':errors,
            'evidence_scope':'Transfer/source identity and new bounded numerical/development checks; not formal proof or independent external scientific review. Closed suites NOT_RUN.'}
    (out/'FINAL_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'files_verified':len(expected),'checks':[{k:r[k] for k in ('name','pass')} for r in checks],'errors':errors},indent=2))
    return int(bool(errors))

if __name__=='__main__':raise SystemExit(main())
