"""Verify this extracted payload and replay only its two new checks.

Python standard library only. This program writes nothing.
"""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def inventory():
    return [{'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,
             'sha256':sha256(p.read_bytes()).hexdigest()}
            for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']

def main():
    manifest_path=HERE/'MANIFEST.json'
    manifest_bytes=manifest_path.read_bytes()
    expected=json.loads(manifest_bytes)['files']
    if inventory()!=expected:
        raise RuntimeError('Payload inventory or byte hashes differ from manifest')
    for script in ['check_covering.py','check_conditional_cover.py']:
        done=subprocess.run([sys.executable,'-I','-B','-X','utf8',str(HERE/script)],
                            cwd=HERE,capture_output=True,text=True,encoding='utf-8',timeout=55)
        if done.returncode or done.stderr or 'PASS' not in done.stdout:
            raise RuntimeError(f'{script} failed: {done.stdout}\n{done.stderr}')
        print(done.stdout.strip())
    if inventory()!=expected or manifest_path.read_bytes()!=manifest_bytes:
        raise RuntimeError('Read-only replay changed payload bytes')
    print(f'PASS: {len(expected)} manifest-bound files unchanged; both new receipts match.')
    print('Byte verification and finite checks do not replace the written analytic proofs.')

if __name__=='__main__': main()
