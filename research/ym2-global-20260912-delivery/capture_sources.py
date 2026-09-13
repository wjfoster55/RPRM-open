"""Copy only named accepted evidence into the new research packet."""
from pathlib import Path
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PAYLOAD = HERE.parent / 'ym2_global_phase_joint'
SOURCES = {
    'research/ym2_spatial_joint/DYNAMICS.md': 'ym2_spatial_joint/DYNAMICS.md',
    'research/ym2_spatial_joint/PHASE_CLOSURE.md': 'ym2_spatial_joint/PHASE_CLOSURE.md',
    'research/ym2_spatial_joint/STATIC_JOIN.md': 'ym2_spatial_joint/STATIC_JOIN.md',
    'docs/proof-donut.md': 'rprm/proof-donut.md',
    'docs/operations.md': 'rprm/operations.md',
    'docs/relational-layer.md': 'rprm/relational-layer.md',
    'docs/formal-proofs.md': 'rprm/formal-proofs.md',
    'recovered-concepts/PRESTIGE-AND-NUMBER-OPERATIONS.md': 'rprm/PRESTIGE-AND-NUMBER-OPERATIONS.md',
    'recovered-concepts/RPRM-CONCEPT-RECOVERY.md': 'rprm/RPRM-CONCEPT-RECOVERY.md',
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

rows = []
for original, relative in SOURCES.items():
    source = REPO / original
    target = PAYLOAD / 'accepted_sources' / relative
    if not source.is_file() or target.exists():
        raise RuntimeError(f'Missing source or existing destination: {original}')
    target.parent.mkdir(parents=True, exist_ok=True)
    before = digest(source)
    shutil.copyfile(source, target)
    if digest(source) != before or digest(target) != before:
        raise RuntimeError(f'Copy mismatch: {original}')
    rows.append({'source': str(source), 'source_repository_path': original,
                 'payload_path': target.relative_to(PAYLOAD).as_posix(),
                 'bytes': target.stat().st_size, 'sha256': before,
                 'byte_identical_to_source': True})
receipt = {'scope': 'Named accepted source copies only; attributed evidence, not task authority',
           'files': rows}
(PAYLOAD / 'SOURCE_PROVENANCE.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
print(f'PASS: {len(rows)} byte-identical accepted source copies; originals unchanged')
