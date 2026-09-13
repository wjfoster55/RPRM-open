"""Capture accepted evidence from the prior delivered ZIP and named RPRM files.

Originals and prior archives are read only. No old checker is executed.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

HERE=Path(__file__).resolve().parent
REPO=HERE.parent.parent
PAYLOAD=HERE.parent/'ym2_signed_differences'
PRIOR=HERE.parent/'ym2-global-20260912-delivery'/'YM2-global-phase-joint-2026-09-12.zip'
EXPECTED='c42d6cd9f09a8377af2eaff7b36f07ca69c553fe585cb0a0078c2f87f100062d'
PREFIX='YM2-global-phase-joint/'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def require(ok,message):
    if not ok:
        raise RuntimeError(message)

require(sha(PRIOR.read_bytes())==EXPECTED,'Prior delivered ZIP changed')
rows=[]
with zipfile.ZipFile(PRIOR) as archive:
    require(archive.testzip() is None,'Prior ZIP CRC failure')
    for name in archive.namelist():
        require(name.startswith(PREFIX) and not name.endswith('/'),'Unexpected prior member')
        relative=PurePosixPath(name[len(PREFIX):])
        require(not relative.is_absolute() and '..' not in relative.parts,'Unsafe prior member')
        target=PAYLOAD/'accepted_sources'/'ym2_global_phase_joint'/str(relative)
        require(target.resolve().is_relative_to(PAYLOAD.resolve()),'Escaped payload')
        require(not target.exists(),'Accepted destination already exists')
        data=archive.read(name)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
        require(target.read_bytes()==data,'Prior payload copy mismatch')
        rows.append({'kind':'prior_zip_payload','archive_member':name,
                     'payload_path':target.relative_to(PAYLOAD).as_posix(),
                     'bytes':len(data),'sha256':sha(data)})
for original,name in [('docs/core.md','core.md'),('docs/operations.md','operations.md'),
                       ('recovered-concepts/PRESTIGE-AND-NUMBER-OPERATIONS.md','PRESTIGE-AND-NUMBER-OPERATIONS.md')]:
    source=REPO/original
    data=source.read_bytes()
    target=PAYLOAD/'accepted_sources'/'rprm'/name
    require(not target.exists(),'RPRM copy already exists')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    require(source.read_bytes()==data and target.read_bytes()==data,'RPRM copy mismatch')
    rows.append({'kind':'local_rprm_source','source':str(source),
                 'payload_path':target.relative_to(PAYLOAD).as_posix(),
                 'bytes':len(data),'sha256':sha(data)})
for note in PAYLOAD.glob('*.md'):
    text=note.read_text(encoding='utf-8')
    changed=text.replace('../ym2_global_phase_joint/','accepted_sources/ym2_global_phase_joint/')
    changed=changed.replace('../../docs/core.md','accepted_sources/rprm/core.md')
    changed=changed.replace('../../docs/operations.md','accepted_sources/rprm/operations.md')
    changed=changed.replace('../../recovered-concepts/PRESTIGE-AND-NUMBER-OPERATIONS.md',
                            'accepted_sources/rprm/PRESTIGE-AND-NUMBER-OPERATIONS.md')
    if changed!=text:
        note.write_text(changed,encoding='utf-8')
receipt={'scope':'Attributed accepted evidence, not task authority; old payload copied from delivered ZIP rather than mutable working files',
         'prior_archive':str(PRIOR),'prior_archive_sha256':EXPECTED,'files':rows}
(PAYLOAD/'SOURCE_PROVENANCE.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
require(sha(PRIOR.read_bytes())==EXPECTED,'Prior ZIP mutated')
print(f'PASS: {len(rows)} byte-identical accepted files, prior archive unchanged')
