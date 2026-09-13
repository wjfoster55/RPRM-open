"""Seal the finished isolated tree once, then create one ZIP (no overwrites)."""
import argparse, hashlib, json, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--zip',type=Path,required=True);args=ap.parse_args()
    archive=args.zip.resolve();manifest=ROOT/'DELIVERY_MANIFEST.json'
    if archive.exists() or manifest.exists():raise SystemExit('Use a fresh export; refusing overwrite')
    if archive==ROOT or ROOT in archive.parents:raise SystemExit('ZIP must be outside payload')
    records=[]
    forbidden={'.ttf','.otf','.woff','.woff2','.eot','.pyc'}
    for path in sorted(ROOT.rglob('*')):
        if path.is_symlink():raise RuntimeError('symlink in delivery')
        if not path.is_file():continue
        rel=path.relative_to(ROOT)
        if any(p in {'.git','.venv','node_modules','__pycache__'} for p in rel.parts) or path.suffix.lower() in forbidden:raise RuntimeError('excluded payload '+str(rel))
        data=path.read_bytes()
        records.append({'path':rel.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    manifest.write_text(json.dumps({'schema':'RPRM-CONSOLIDATED-C2-1','self_hash':'excluded; bound by exported ZIP SHA-256','files':records},indent=2)+'\n',encoding='utf-8')
    archive.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in sorted(ROOT.rglob('*')):
            if path.is_file():z.write(path,'RPRM-CONSOLIDATED-C2/'+path.relative_to(ROOT).as_posix())
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.sha256').write_text(digest+'  '+archive.name+'\n',encoding='ascii')
    print(json.dumps({'zip':str(archive),'sha256':digest,'payload_files':len(records)+1,'bytes':archive.stat().st_size},indent=2))

if __name__=='__main__':main()
