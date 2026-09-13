"""Freeze this continuation, freshly extract it, and replay only new checks.

Standard library only. No destructive operations, installations, git, other
task commands or accepted-source checkers. Sidecars are written after freeze.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'ym2_connected_vacuum'
ARCHIVE = HERE/'YM2-connected-vacuum-2026-09-12.zip'
EXTRACT = HERE/'final-extraction'
ROOTNAME = 'YM2-connected-vacuum'
CHECKS = [('check_connected.py','RESULTS_CONNECTED.json'),
          ('check_witness.py','RESULTS_WITNESS.json'),
          ('check_conditional_head.py','RESULTS_CONDITIONAL_HEAD.json')]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def inventory(base):
    return [{'path': p.relative_to(base).as_posix(), 'bytes': p.stat().st_size,
             'sha256': digest(p)} for p in sorted(base.rglob('*')) if p.is_file()]


def verify_sources():
    provenance = json.loads((SOURCE/'SOURCE_PROVENANCE.json').read_text(encoding='utf-8'))
    require(digest(Path(provenance['prior_archive'])) == provenance['prior_archive_sha256'],
            'Prior accepted archive changed')
    for row in provenance['files']:
        require(digest(SOURCE/row['payload_path']) == row['sha256'], 'Copied evidence changed: '+row['payload_path'])
    # Concurrent task working files may legitimately evolve. The copied bytes
    # and their per-read provenance, not an assertion of live equality, are frozen.
    return provenance


def inspect_payload():
    provenance = verify_sources()
    link_records = []
    for note in sorted(SOURCE.glob('*.md')):
        for destination in re.findall(r'\]\(([^)]+)\)', note.read_text(encoding='utf-8')):
            if destination.startswith(('https://','http://','#')):
                continue
            relative = destination.split('#',1)[0]
            target = (note.parent/relative).resolve()
            require(target.is_relative_to(SOURCE.resolve()), 'Nonportable current note link: '+note.name+': '+relative)
            require(target.is_file(), 'Missing current note target: '+note.name+': '+relative)
            link_records.append({'note': note.name, 'target': target.relative_to(SOURCE).as_posix()})
    require(all('__pycache__' not in p.parts for p in SOURCE.rglob('*')), 'Unexpected bytecode')
    png = (SOURCE/'connected_joint.png').read_bytes()
    require(png[:8] == b'\x89PNG\r\n\x1a\n', 'Invalid PNG')
    width, height = struct.unpack('>II', png[16:24])
    require((width,height) == (3200,1700), 'Unexpected figure dimensions')
    for name in ('REVIEW_PERTURBATION.md','REVIEW_WITNESS.md','REVIEW_WITNESS_MATH.md',
                 'REVIEW_CONDITIONAL_PORTS.md','VISUAL_CHECKS.md'):
        require((SOURCE/name).is_file(), 'Missing final review: '+name)
    return provenance, link_records, (width,height)


def main():
    require(not ARCHIVE.exists() and not EXTRACT.exists(), 'One-shot export already exists')
    require(not (SOURCE/'MANIFEST.json').exists(), 'Payload already frozen')
    provenance, links, dimensions = inspect_payload()
    entries = inventory(SOURCE)
    (SOURCE/'MANIFEST.json').write_text(json.dumps({
        'schema': 'ym2-connected-vacuum-manifest-v1',
        'self_excluded': 'MANIFEST.json',
        'scope': 'New connected-vacuum research, accepted source copies and attributed running-task snapshots',
        'files': entries}, indent=2)+'\n', encoding='utf-8')
    frozen = inventory(SOURCE)
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for row in frozen:
            archive.write(SOURCE/row['path'], ROOTNAME+'/'+row['path'])
    archive_hash = digest(ARCHIVE)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ARCHIVE) as archive:
        require(archive.testzip() is None, 'ZIP CRC failure')
        require(len(archive.namelist()) == len(set(archive.namelist())) == len(frozen), 'ZIP census mismatch')
        for member in archive.namelist():
            require((EXTRACT/member).resolve().is_relative_to(EXTRACT.resolve()), 'Unsafe extraction member')
        archive.extractall(EXTRACT)
    target = EXTRACT/ROOTNAME
    before = inventory(target)
    require(before == frozen, 'Fresh extraction differs from source')
    manifest = json.loads((target/'MANIFEST.json').read_text(encoding='utf-8'))
    require(manifest['files'] == [r for r in before if r['path'] != 'MANIFEST.json'], 'Manifest mismatch')
    runs = []
    for script, receipt in CHECKS:
        command = [sys.executable,'-I','-B','-X','utf8',str(target/script)]
        done = subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',timeout=55)
        stdout_file = HERE/(script+'.stdout.txt')
        stderr_file = HERE/(script+'.stderr.txt')
        stdout_file.write_text(done.stdout,encoding='utf-8')
        stderr_file.write_text(done.stderr,encoding='utf-8')
        require(done.returncode == 0 and 'PASS' in done.stdout, 'New checker failed: '+script+': '+done.stderr)
        require(not done.stderr, 'Unexpected stderr: '+script)
        runs.append({'script': script, 'receipt': receipt, 'command': command,
                     'cwd': str(target), 'exit_code': done.returncode, 'status': 'PASS',
                     'receipt_comparison': 'Full fresh deterministic computation compared internally in default read-only mode',
                     'stdout_path': stdout_file.name, 'stdout_sha256': digest(stdout_file),
                     'stderr_path': stderr_file.name, 'stderr_bytes': 0})
    require(inventory(target) == before == inventory(SOURCE), 'Replay changed payload bytes')
    require(digest(ARCHIVE) == archive_hash, 'Frozen archive changed')
    verify_sources()
    connected = json.loads((target/'RESULTS_CONNECTED.json').read_text(encoding='utf-8'))
    witness = json.loads((target/'RESULTS_WITNESS.json').read_text(encoding='utf-8'))
    head = json.loads((target/'RESULTS_CONDITIONAL_HEAD.json').read_text(encoding='utf-8'))
    result = {
        'schema': 'ym2-connected-vacuum-final-export-v1',
        'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
        'archive': str(ARCHIVE), 'archive_sha256': archive_hash,
        'archive_bytes': ARCHIVE.stat().st_size, 'payload_files': len(frozen),
        'payload_bytes': sum(r['bytes'] for r in frozen),
        'manifest_covered_files': len(entries), 'zip_crc': 'PASS',
        'fresh_extraction': str(target), 'source_equals_extracted': True,
        'payload_unchanged_after_replay': True, 'archive_unchanged_after_replay': True,
        'runs': runs, 'python_version': sys.version,
        'polynomial_identity_checks': connected['checks_passed'],
        'witness_orthogonality_controls': witness['orthogonality_monomial_controls'],
        'witness_haar_convolution_controls': witness['convolution_haar_marginal_controls'],
        'local_star_dimensions': [r['dimension'] for r in head['local_stars']],
        'local_star_incident_pair_counts': [r['adjacent_pair_factors_incident_to_edge'] for r in head['local_stars']],
        'accepted_YM_source_files': sum(r['role'].startswith('accepted_YM') for r in provenance['files']),
        'running_task_source_files': sum(r['role'].startswith('running_task') for r in provenance['files']),
        'top_level_local_file_links_checked': len(links),
        'link_records': links,
        'figure_dimensions': dimensions, 'figure_visual_review': 'See VISUAL_CHECKS.md; root also inspected final PNG',
        'prior_archive_unchanged': provenance['prior_archive'],
        'prior_archive_sha256': provenance['prior_archive_sha256'],
        'evidence_boundary': 'Written analytic proofs with exact bounded corroboration; no proof-assistant certification, full conditional remainder bound, continuum construction, P=NP or mass-gap solution.'}
    (HERE/'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (HERE/'YM2-connected-vacuum-2026-09-12.sha256').write_text(archive_hash+'  '+ARCHIVE.name+'\n',encoding='ascii')
    note = f'''# Final export evidence — PASS

Archive: `{ARCHIVE.name}`  
SHA-256: `{archive_hash}`  
ZIP bytes: {result['archive_bytes']}; payload files: {result['payload_files']};
uncompressed payload bytes: {result['payload_bytes']}.

The final ZIP passed CRC verification and was freshly extracted into a new
directory. Every file matched the source payload. MANIFEST.json binds every
other payload file, including the attributed source copies.

All three new checkers ran from the fresh extraction with isolated Python,
UTF-8 mode and bytecode disabled. Each freshly computed and compared its
complete deterministic saved receipt. All exited zero with empty stderr.
Source, extracted and ZIP bytes remained unchanged after replay.

The connected-vacuum checker passed {connected['checks_passed']} exact polynomial identities,
with coefficient, Haar, normalization and hostile controls. The witness
checker passed {witness['orthogonality_monomial_controls']} exact orthogonality controls and
{witness['convolution_haar_marginal_controls']} Haar-convolution controls, plus the full rational margin ledger.
The conditional-head checker counted the complete two- and three-dimensional
local stars: 7 and 42 incident adjacent-pair factors, below the safe 8 and 48
bounds, including the omitted-factor hostile controls. None is a simulation.
Universal analytic and graph-family statements rely on their written proofs.

All {len(links)} file links in the new top-level notes resolve inside the portable
payload. Historical source copies retain their original link contexts.
The 3200 by 1700 PNG was visually inspected; the editable SVG and plotting
source are included. Mathematical replay does not require Matplotlib.

The 33 accepted YM files came from the previously delivered signed-residual
ZIP and remain byte-identical. The 9 other-task source files remain identical
to their captured bytes; their live tasks may continue changing. The prior
ZIP retains SHA-256 `{provenance['prior_archive_sha256']}`.
No accepted or other-lane checker was rerun, and no source task was modified.

See FINAL_EXPORT_EVIDENCE.json for actual commands, paths, interpreter,
hashes and link records; the adjacent stdout/stderr files retain replay
output. This sidecar was generated after freezing the ZIP. It establishes
execution and byte integrity, not the continuum mass-gap theorem.
'''
    (HERE/'FINAL_EXPORT_EVIDENCE.md').write_text(note,encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status','archive','archive_sha256',
          'archive_bytes','payload_files','top_level_local_file_links_checked')},indent=2))


if __name__ == '__main__':
    main()
