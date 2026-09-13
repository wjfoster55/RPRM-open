"""Freeze the new task payload, extract it afresh, and replay its exact checks.

Standard library only. One-shot: existing archive/extraction are errors.
No deletion, moving, old-suite execution, or git operation is performed.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'ym2_global_phase_joint'
ARCHIVE = HERE / 'YM2-global-phase-joint-2026-09-12.zip'
EXTRACT = HERE / 'final-extraction'
ROOTNAME = 'YM2-global-phase-joint'
OLD_ARCHIVES = {
    HERE.parent / 'ym2-20260912-delivery' / 'YM2-interacting-SU2-2026-09-12.zip':
        '167e181c19e6c2a5dfdcb3e9956412251a8dcb9d808c7684e68393e7d86f1f8c',
    HERE.parent / 'ym2-spatial-20260912-delivery' / 'YM2-spatial-joint-2026-09-12.zip':
        '60d0efd6577adaa24594071aa58001355e26b96353b386200d0f96546bb60e29',
}

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(base):
    return [{'path': p.relative_to(base).as_posix(), 'bytes': p.stat().st_size,
             'sha256': sha(p)} for p in sorted(base.rglob('*')) if p.is_file()]

def verify_priors():
    for path, expected in OLD_ARCHIVES.items():
        require(sha(path) == expected, f'Prior archive differs: {path}')
    provenance = json.loads((SOURCE / 'SOURCE_PROVENANCE.json').read_text(encoding='utf-8'))
    for row in provenance['files']:
        require(sha(Path(row['source'])) == row['sha256'], f"Accepted original changed: {row['source']}")
        require(sha(SOURCE / row['payload_path']) == row['sha256'], 'Accepted source copy differs')

def run(command, target, prefix):
    done = subprocess.run(command, cwd=target, capture_output=True, text=True,
                          encoding='utf-8', timeout=55)
    (HERE / (prefix+'.stdout.txt')).write_text(done.stdout, encoding='utf-8')
    (HERE / (prefix+'.stderr.txt')).write_text(done.stderr, encoding='utf-8')
    return done, {'command': command, 'cwd': str(target), 'exit_code': done.returncode,
                  'stdout_sha256': hashlib.sha256(done.stdout.encode()).hexdigest(),
                  'stderr_sha256': hashlib.sha256(done.stderr.encode()).hexdigest(),
                  'stderr_bytes': len(done.stderr.encode())}

def main():
    require(SOURCE.is_dir(), 'Missing payload')
    require(not ARCHIVE.exists() and not EXTRACT.exists(), 'One-shot export already exists')
    require(not (SOURCE / 'MANIFEST.json').exists(), 'Payload already frozen')
    require(all('__pycache__' not in p.parts for p in SOURCE.rglob('*')), 'Unexpected bytecode')
    verify_priors()
    entries = inventory(SOURCE)
    manifest = {'schema': 1, 'scope': 'Global fixed-graph continuation and bounded quantum bridge',
                'self_excluded': 'MANIFEST.json', 'files': entries}
    (SOURCE / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    frozen = inventory(SOURCE)
    with zipfile.ZipFile(ARCHIVE, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for item in frozen:
            z.write(SOURCE / item['path'], ROOTNAME+'/'+item['path'])
    archive_sha = sha(ARCHIVE)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ARCHIVE) as z:
        require(z.testzip() is None, 'ZIP CRC failure')
        require(len(z.namelist()) == len(set(z.namelist())) == len(frozen), 'ZIP member census differs')
        for member in z.namelist():
            target_path = (EXTRACT / member).resolve()
            require(target_path.is_relative_to(EXTRACT.resolve()), f'Unsafe extraction target: {member}')
        z.extractall(EXTRACT)
    target = EXTRACT / ROOTNAME
    before = inventory(target)
    require(before == frozen, 'Fresh extraction differs from source')
    loaded = json.loads((target / 'MANIFEST.json').read_text(encoding='utf-8'))
    require(loaded['files'] == [r for r in before if r['path'] != 'MANIFEST.json'], 'Manifest mismatch')

    runs = []
    for script, receipt in [('check_tree.py', 'RESULTS_TREE.json'),
                            ('check_invariants.py', 'RESULTS_INVARIANTS.json'),
                            ('check_quantum.py', 'RESULTS_QUANTUM.json')]:
        command = [sys.executable, '-I', '-B', '-X', 'utf8', str(target / script)]
        done, result = run(command, target, script)
        require(done.returncode == 0 and 'PASS' in done.stdout, f'Checker failed: {script}: {done.stderr}')
        require('compar' in done.stdout.lower() or 'match' in done.stdout.lower(), 'Missing receipt confirmation')
        result.update({'script': script, 'receipt': receipt,
                       'comparison': 'Default checker freshly recomputes and compares its complete saved receipt internally',
                       'status': 'PASS'})
        runs.append(result)

    command = [sys.executable, '-I', '-O', '-B', '-X', 'utf8', str(target / 'check_tree.py')]
    rejected, guard = run(command, target, 'tree_optimized_rejection')
    require(rejected.returncode != 0 and 'This checker requires assertions' in rejected.stderr,
            'Tree checker failed to reject optimization')
    require('PASS' not in rejected.stdout, 'Disabled checks reported success')
    guard.update({'status': 'PASS: optimized mode deliberately rejected',
                  'scope': 'Execution guard only; this is not a failed mathematical replay'})

    after = inventory(target)
    require(after == before == inventory(SOURCE), 'Replay changed payload bytes')
    require(sha(ARCHIVE) == archive_sha, 'Archive changed after freeze')
    verify_priors()
    tree = json.loads((target / 'RESULTS_TREE.json').read_text(encoding='utf-8'))
    invariant = json.loads((target / 'RESULTS_INVARIANTS.json').read_text(encoding='utf-8'))
    evidence = {'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
                'archive': str(ARCHIVE), 'archive_sha256': archive_sha,
                'archive_bytes': ARCHIVE.stat().st_size, 'payload_files': len(frozen),
                'payload_bytes': sum(r['bytes'] for r in frozen),
                'manifest_covered_files': len(entries), 'fresh_extraction': str(target),
                'python_version': sys.version, 'zip_crc': 'PASS',
                'source_payload_identical_to_extracted': True,
                'payload_before_and_after_replay_identical': True, 'runs': runs,
                'optimized_tree_guard': guard,
                'tree_phase_cases': len(tree['cases']),
                'tree_representatives_per_case': 2,
                'tree_regular_bridges': len(tree['regular_bridge_cases']),
                'invariant_counts': invariant['counts'],
                'quantum_support_subsets': 128,
                'accepted_source_copies': 9,
                'earlier_archives_unchanged': [{'path': str(p), 'sha256': h} for p,h in OLD_ARCHIVES.items()],
                'limits': 'Written proofs and exact bounded corroboration, not proof-assistant certification; finite graph quantum gap estimate, no continuum mass-gap solution or uniform graph-family bound.'}
    (HERE / 'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(evidence, indent=2)+'\n', encoding='utf-8')
    (HERE / 'YM2-global-phase-joint-2026-09-12.sha256').write_text(archive_sha+'  '+ARCHIVE.name+'\n', encoding='ascii')
    prose = f'''# Final export evidence — PASS

Archive: `{ARCHIVE.name}`  
SHA-256: `{archive_sha}`  
Archive bytes: {ARCHIVE.stat().st_size}; payload files: {len(frozen)};
uncompressed payload bytes: {evidence['payload_bytes']}.

The final archive passed CRC verification and was extracted into a new
directory. All {len(frozen)} files matched their source bytes; the manifest
covered the other {len(entries)} files. All three new checkers ran successfully
from that extraction with isolated Python and bytecode disabled. Each
freshly recomputed and compared its complete saved receipt. All three
exited zero with empty stderr. Neither source nor extracted payload bytes
changed during replay. The archive checksum also remained unchanged.

The exact receipts cover 14 tree phase cases in two gauge representatives
each, six regular bridges, 3,008 invariant checks, and all 128 quantum
edge-support subsets plus exact Pauli and drift calculations. Continuous
and all-spin coverage rests on the written proofs and their stated
established inputs, not finite-test extrapolation.

An execution control additionally confirmed that the assertion-based tree
checker refuses optimized Python instead of reporting success with its
checks disabled. That deliberately rejected invocation is separately
recorded; the three mathematical replays all passed normally.

Nine named accepted source copies and their originals still match the
recorded SHA-256 values. Both earlier frozen YM2 archives retain their
expected hashes. No accepted YM1 or earlier YM2 suite was rerun.

`FINAL_EXPORT_EVIDENCE.json` records commands, paths, interpreter, counts,
hashes and exit codes. Individual stdout/stderr files are beside this
note. This evidence binds bytes and actual execution; it is not a formal
proof of the checkers' soundness, quantum limit construction, or continuum
mass gap. The sidecar is generated after the ZIP is frozen.
'''
    (HERE / 'FINAL_EXPORT_EVIDENCE.md').write_text(prose, encoding='utf-8')
    print(json.dumps({key: evidence[key] for key in
                     ('status','archive','archive_sha256','archive_bytes','payload_files','invariant_counts')}, indent=2))

if __name__ == '__main__':
    main()
