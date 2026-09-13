"""One-shot task export and replay. Python standard library; no installation.

Produces a new ZIP and fresh extraction; fails if either already exists.
Does not delete/move files or mutate any prior research output.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
import zipfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'ym2_spatial_joint'
OLD = HERE.parent / 'ym2-20260912-delivery' / 'YM2-interacting-SU2-2026-09-12.zip'
EXPECTED_OLD = '167e181c19e6c2a5dfdcb3e9956412251a8dcb9d808c7684e68393e7d86f1f8c'
ARCHIVE = HERE / 'YM2-spatial-joint-2026-09-12.zip'
EXTRACT = HERE / 'final-extraction'
ROOTNAME = 'YM2-spatial-joint'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path, base):
    return {'path': path.relative_to(base).as_posix(), 'bytes': path.stat().st_size,
            'sha256': sha(path)}


def inventory(base):
    return [record(p, base) for p in sorted(base.rglob('*')) if p.is_file()]


def main():
    assert SOURCE.is_dir()
    assert sha(OLD) == EXPECTED_OLD, 'Earlier frozen YM2 ZIP changed'
    assert not ARCHIVE.exists() and not EXTRACT.exists(), 'One-shot export already exists'
    assert all('__pycache__' not in p.parts for p in SOURCE.rglob('*'))
    entries = [r for r in inventory(SOURCE) if r['path'] != 'MANIFEST.json']
    manifest = {'schema': 1, 'scope': 'New spatial joint research payload only',
                'self_excluded': 'MANIFEST.json', 'files': entries}
    (SOURCE / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    frozen = inventory(SOURCE)
    with zipfile.ZipFile(ARCHIVE, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for item in frozen:
            z.write(SOURCE / item['path'], ROOTNAME + '/' + item['path'])
    archive_sha = sha(ARCHIVE)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(set(z.namelist())) == len(frozen)
        for member in z.namelist():
            target = (EXTRACT / member).resolve()
            assert target.is_relative_to(EXTRACT.resolve()), member
        z.extractall(EXTRACT)
    target = EXTRACT / ROOTNAME
    before = inventory(target)
    assert before == frozen, 'Extracted payload differs from source'
    loaded = json.loads((target / 'MANIFEST.json').read_text(encoding='utf-8'))
    assert loaded['files'] == [r for r in before if r['path'] != 'MANIFEST.json']

    runs = []
    for script, receipt in [('check_dynamics.py', 'RESULTS_DYNAMICS.json'),
                            ('check_static_join.py', 'RESULTS_STATIC.json'),
                            ('check_phase.py', 'RESULTS_PHASE.json')]:
        command = [sys.executable, '-I', '-B', '-X', 'utf8', str(target / script)]
        completed = subprocess.run(command, cwd=target, capture_output=True, text=True,
                                   encoding='utf-8', timeout=90)
        (HERE / (script + '.stdout.txt')).write_text(completed.stdout, encoding='utf-8')
        (HERE / (script + '.stderr.txt')).write_text(completed.stderr, encoding='utf-8')
        assert completed.returncode == 0, (script, completed.stderr)
        assert 'PASS' in completed.stdout, script
        if script == 'check_dynamics.py':
            assert json.loads(completed.stdout) == json.loads((target / receipt).read_text(encoding='utf-8'))
            comparison = 'Fresh stdout JSON equals saved receipt'
        else:
            comparison = 'Default checker recomputes and compares complete saved JSON internally'
        runs.append({'script': script, 'command': command, 'cwd': str(target),
                     'exit_code': completed.returncode, 'receipt': receipt,
                     'comparison': comparison, 'stdout_sha256': hashlib.sha256(completed.stdout.encode()).hexdigest(),
                     'stderr_bytes': len(completed.stderr.encode())})
    after = inventory(target)
    assert after == before == inventory(SOURCE), 'A default replay changed payload bytes'
    assert sha(ARCHIVE) == archive_sha and sha(OLD) == EXPECTED_OLD
    static = json.loads((target / 'RESULTS_STATIC.json').read_text(encoding='utf-8'))
    phase = json.loads((target / 'RESULTS_PHASE.json').read_text(encoding='utf-8'))
    result = {'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
              'archive': str(ARCHIVE), 'archive_sha256': archive_sha,
              'archive_bytes': ARCHIVE.stat().st_size, 'payload_files': len(frozen),
              'manifest_covered_files': len(entries), 'fresh_extraction': str(target),
              'zip_crc': 'PASS', 'payload_before_and_after_replay_identical': True,
              'source_payload_identical_to_extracted': True, 'runs': runs,
              'static_checks': static['counts'],
              'phase_regular_cases': len(phase['regular_cases']),
              'phase_gauge_cases': len(phase['gauge_covariance_cases']),
              'phase_boundary_cases': len(phase['boundary_cases']),
              'phase_polynomial_identity': phase['polynomial_determinant'],
              'earlier_YM2_zip': str(OLD), 'earlier_YM2_zip_sha256_unchanged': EXPECTED_OLD,
              'limits': 'Written mathematics plus finite executable checks; not formal verification, global singular closure or a continuum quantum result.'}
    (HERE / 'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    (HERE / 'YM2-spatial-joint-2026-09-12.sha256').write_text(archive_sha+'  '+ARCHIVE.name+'\n', encoding='ascii')
    prose = f'''# Final export evidence — PASS

Archive: `{ARCHIVE.name}`  
SHA-256: `{archive_sha}`  
Bytes: {ARCHIVE.stat().st_size}; payload files: {len(frozen)}.

The final ZIP passed CRC verification and was freshly extracted. Every
payload file matched the source inventory, including the manifest. All three
checkers ran from that extraction with isolated Python and bytecode disabled.
The dynamics result matched its saved full JSON; the static and phase
checkers freshly recomputed and compared their full saved JSON internally.
All runs exited zero. Extracted and source bytes remained identical after
replay, and the ZIP checksum stayed unchanged.

The phase checks include {len(phase['regular_cases'])} regular full-link cases,
{len(phase['gauge_covariance_cases'])} gauge controls, three boundary cases,
the singular electric-circulation witness and an exact determinant polynomial
identity. The static receipt records independent matrix products, ordered
triple associativity, joint updates and coarse-fiber recovery controls.
The dynamics receipt contains the exact noncommuting shared-edge witnesses.

The earlier frozen YM2 ZIP remains SHA-256 `{EXPECTED_OLD}`. No accepted YM1
or earlier-lane suite was rerun. This evidence binds delivered bytes and
records actual execution; the written proofs carry the continuous claims.

See `FINAL_EXPORT_EVIDENCE.json` for commands, paths, counts and hashes, and
the three stdout/stderr files beside this note for exact run output.
'''
    (HERE / 'FINAL_EXPORT_EVIDENCE.md').write_text(prose, encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['status', 'archive', 'archive_sha256', 'archive_bytes', 'payload_files']}, indent=2))


if __name__ == '__main__':
    main()
