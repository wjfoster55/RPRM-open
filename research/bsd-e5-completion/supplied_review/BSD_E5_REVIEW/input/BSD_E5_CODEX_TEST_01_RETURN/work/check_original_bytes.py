"""Compare every supplied ZIP member against the preserved extracted bytes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original_zip', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    supplied = (ROOT / 'supplied').resolve()
    rows = []
    with ZipFile(args.original_zip) as archive:
        for item in archive.infolist():
            if item.is_dir():
                continue
            target = (supplied / item.filename).resolve()
            if supplied not in target.parents:
                raise ValueError('ZIP member escapes supplied root')
            data = archive.read(item)
            if target.read_bytes() != data:
                raise ValueError(f'Original bytes changed: {item.filename}')
            rows.append({'member': item.filename, 'size': len(data),
                         'sha256': hashlib.sha256(data).hexdigest(), 'identical': True})
    actual = {p.relative_to(supplied).as_posix() for p in supplied.rglob('*') if p.is_file()}
    if actual != {row['member'] for row in rows}:
        raise ValueError('Unexpected/missing supplied member')
    result = {'status': 'ALL_ORIGINAL_MEMBERS_IDENTICAL',
              'utc': datetime.now(timezone.utc).isoformat(),
              'original_zip_name': args.original_zip.name,
              'original_zip_sha256': hashlib.sha256(args.original_zip.read_bytes()).hexdigest(),
              'files': rows, 'scope': 'Byte preservation, not mathematical truth.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'members': len(rows)}))


if __name__ == '__main__':
    main()
