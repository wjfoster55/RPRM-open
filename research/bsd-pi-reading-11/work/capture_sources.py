"""Preserve the exact finite decoder spec and earlier written dependencies."""
from pathlib import Path
import zipfile,json,hashlib
root=Path(__file__).resolve().parents[1]
repo=root.parents[1]
target=root/'dependencies';target.mkdir(exist_ok=True)
archive=Path('C:/github/RPRMFoundry/evidence/sealed/RPRMPiViewfinder_SEALED_96f920a.zip')
entry='experiments/PI_VIEWFINDER_TEACHER_ZIP_01/TEST_SPEC.md'
with zipfile.ZipFile(archive) as z:data=z.read(entry)
rows=[('PI_ZIP_TEST_SPEC.md',str(archive)+'::'+entry,data)]
for name,source in (
 ('DISTANCE_AND_SEAM.md',repo/'research/closure-seam-09/DISTANCE_AND_SEAM.md'),
 ('EXPLICIT_IDENTITY_TARGET.md',repo/'research/bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md'),
 ('FACTOR_COMPARISON.md',repo/'research/bsd-identity-01/input_source/FACTOR_COMPARISON.md'),
 ('PI_CLOSURE_LEGEND_AUDIT.md',Path('C:/github/RPRMLexicon/operational_numbers/PI_CLOSURE_LEGEND_AUDIT.md'))):
    rows.append((name,str(source),source.read_bytes()))
manifest=[]
for name,source,data in rows:
    p=target/name
    if p.exists():assert p.read_bytes()==data
    else:p.write_bytes(data)
    manifest.append({'file':name,'original_source':source,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
report={'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
        'scope':'Historical source snapshots; no saved numerical results used as fresh computation inputs',
        'relative_links':'Resolve internal links in original source directory if they point outside this snapshot.',
        'files':manifest}
dest=target/'SOURCES.json';payload=json.dumps(report,indent=2)+'\n'
if dest.exists():assert dest.read_text()==payload
else:dest.write_text(payload,encoding='utf-8')
print(json.dumps({'captured_files':len(rows),'source_bytes_preserved':True}))
