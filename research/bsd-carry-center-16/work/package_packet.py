"""Build or verify this bounded return packet using only the standard library."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT.name + '/'


def serialize(data):
    return (json.dumps(data, indent=2, sort_keys=True) + '\n').encode('utf-8')


def verify(archive):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None, 'ZIP CRC failure'
        names = z.namelist()
        assert len(names) == len(set(names)), 'Duplicate ZIP member'
        manifest = json.loads(z.read(PREFIX + 'MANIFEST.json'))
        expected = {PREFIX + row['path'] for row in manifest['files']}
        assert set(names) == expected | {PREFIX + 'MANIFEST.json'}, 'Manifest coverage mismatch'
        for row in manifest['files']:
            data = z.read(PREFIX + row['path'])
            assert len(data) == row['bytes'], row['path']
            assert sha256(data).hexdigest() == row['sha256'], row['path']
        return {'verified_members': len(names), 'manifested_files': len(manifest['files'])}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--build', type=Path)
    group.add_argument('--verify', type=Path)
    args = ap.parse_args()
    if args.verify:
        print(json.dumps(verify(args.verify), indent=2))
        return
    output = args.build.resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('Archive must be outside its source packet')
    receipt_path = output.with_suffix('.receipt.json')
    if output.exists() or receipt_path.exists():
        raise FileExistsError('Use a new archive and receipt path')
    paths = sorted(p for p in ROOT.rglob('*') if p.is_file()
                   and p.name != 'MANIFEST.json' and '__pycache__' not in p.parts)
    rows = []
    for p in paths:
        data = p.read_bytes()
        rows.append({'path': p.relative_to(ROOT).as_posix(),
                     'bytes': len(data), 'sha256': sha256(data).hexdigest()})
    manifest_bytes = serialize({'schema': 'bsd-carry-center-16-file-manifest-v1',
                               'claim': 'Byte integrity only; not mathematical verification',
                               'files': rows})
    manifest_path = ROOT / 'MANIFEST.json'
    if manifest_path.exists() and manifest_path.read_bytes() != manifest_bytes:
        raise ValueError('Existing manifest differs; choose a fresh source packet for changed contents')
    if not manifest_path.exists():
        manifest_path.write_bytes(manifest_bytes)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for p in paths + [manifest_path]:
            z.write(p, PREFIX + p.relative_to(ROOT).as_posix())
    verification = verify(output)
    with zipfile.ZipFile(output) as z:
        for p in paths + [manifest_path]:
            assert z.read(PREFIX + p.relative_to(ROOT).as_posix()) == p.read_bytes()
    result = {'status': 'ARCHIVE_BYTES_AND_MANIFEST_VERIFIED',
              'created_utc': datetime.now(timezone.utc).isoformat(),
              'archive': str(output), 'archive_bytes': output.stat().st_size,
              'archive_sha256': sha256(output.read_bytes()).hexdigest(),
              'source_tree_byte_comparison': True, **verification}
    receipt_path.write_bytes(serialize(result))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()




