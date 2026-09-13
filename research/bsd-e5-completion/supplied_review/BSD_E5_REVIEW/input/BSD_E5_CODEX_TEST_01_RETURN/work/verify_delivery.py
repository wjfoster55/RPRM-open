"""Verify this experiment's delivery inventory; hashes bind bytes, not proofs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, default=ROOT / 'DELIVERY_INVENTORY.json')
    args = parser.parse_args()
    manifest = json.loads(args.inventory.read_text(encoding='utf-8'))
    seen = set()
    for row in manifest['files']:
        rel = row['path']
        path = (ROOT / rel).resolve()
        if ROOT not in path.parents or rel in seen:
            raise ValueError(f'Unsafe or duplicate member: {rel}')
        seen.add(rel)
        if path.stat().st_size != row['size'] or sha(path) != row['sha256']:
            raise ValueError(f'Byte mismatch: {rel}')
    print(json.dumps({'status': 'BYTES_MATCH', 'members_checked': len(seen),
                      'scope': 'Integrity only; execute work/run_all.py for fresh finite checks.'}))


if __name__ == '__main__':
    main()
