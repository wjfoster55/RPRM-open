"""Make and verify the one E5 delivery ZIP; no mathematical claims from hashes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = 'BSD_E5_CODEX_TEST_01_RETURN'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    target = args.output.resolve()
    if target.exists() or ROOT == target or ROOT in target.parents:
        raise ValueError('Choose a new ZIP outside the experiment directory.')
    required = ['RETURN_TO_WILLIAM.md', 'BSD_REBRIEF.md', 'CLAIM_LEDGER.json',
        'INDEPENDENT_CHECKS.json', 'CONTROLS.json', 'DERIVATIVE_INTERVAL.json',
        'ARITHMETIC_PROOF.md', 'ANALYTIC_THEOREMS.md', 'INTERVAL_DERIVATION.md',
        'work/run_all.py', 'runs/portable_validation/RUN.json']
    for rel in required:
        if not (ROOT / rel).is_file():
            raise ValueError(f'Missing required delivery file: {rel}')
    members = []
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path == ROOT / 'DELIVERY_INVENTORY.json':
            continue
        if '__pycache__' in path.parts or '.pytest_cache' in path.parts or path.suffix == '.pyc':
            continue
        raw = path.read_bytes()
        members.append({'path': path.relative_to(ROOT).as_posix(),
                        'size': len(raw), 'sha256': digest(raw)})
    inventory = {'generated_utc': datetime.now(timezone.utc).isoformat(),
                 'files': members, 'file_count_excluding_inventory': len(members),
                 'exclusions': ['This inventory itself', 'Python caches, if any'],
                 'scope': 'Final byte inventory; mathematical support resides in the source, execution evidence and written proofs.'}
    (ROOT / 'DELIVERY_INVENTORY.json').write_text(json.dumps(inventory, indent=2) + '\n', encoding='utf-8')
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, 'x', compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for row in members:
            archive.write(ROOT / row['path'], ARCHIVE_ROOT+'/'+row['path'])
        archive.write(ROOT / 'DELIVERY_INVENTORY.json', ARCHIVE_ROOT+'/DELIVERY_INVENTORY.json')
    with ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError('Archive CRC failure')
        expected = {ARCHIVE_ROOT+'/'+row['path'] for row in members} | {ARCHIVE_ROOT+'/DELIVERY_INVENTORY.json'}
        if set(archive.namelist()) != expected or len(archive.namelist()) != len(expected):
            raise ValueError('Archive has missing, extra or duplicate members')
        for row in members:
            raw = archive.read(ARCHIVE_ROOT+'/'+row['path'])
            if len(raw) != row['size'] or digest(raw) != row['sha256']:
                raise ValueError('Archive member differs from the final inventory')
        if archive.read(ARCHIVE_ROOT+'/DELIVERY_INVENTORY.json') != (ROOT/'DELIVERY_INVENTORY.json').read_bytes():
            raise ValueError('Archive inventory mismatch')
    sha = digest(target.read_bytes())
    checksum = target.with_suffix(target.suffix+'.sha256')
    checksum.write_text(sha+'  '+target.name+'\n', encoding='ascii')
    print(json.dumps({'status': 'PACKAGED_AND_BYTE_VERIFIED', 'archive': str(target),
                      'archive_members': len(members)+1, 'size': target.stat().st_size,
                      'sha256': sha, 'checksum_file': str(checksum)}, indent=2))


if __name__ == '__main__':
    main()
