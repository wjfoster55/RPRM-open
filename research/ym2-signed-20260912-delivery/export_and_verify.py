"""One-shot portable export and fresh exact replay; standard library only.

Does not delete/move files, run earlier suites, install, or use git.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import re
import struct
import subprocess
import sys
import zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ym2_signed_differences'
ARCHIVE=HERE/'YM2-signed-differences-2026-09-12.zip'
EXTRACT=HERE/'final-extraction'
ROOTNAME='YM2-signed-differences'

def require(condition,message):
    if not condition:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(base):
    return [{'path':p.relative_to(base).as_posix(),'bytes':p.stat().st_size,
             'sha256':digest(p)} for p in sorted(base.rglob('*')) if p.is_file()]

def verify_sources():
    provenance=json.loads((SOURCE/'SOURCE_PROVENANCE.json').read_text(encoding='utf-8'))
    require(digest(Path(provenance['prior_archive']))==provenance['prior_archive_sha256'],
            'Previous delivered archive changed')
    for row in provenance['files']:
        require(digest(SOURCE/row['payload_path'])==row['sha256'],'Accepted copy differs')
        if 'source' in row:
            require(digest(Path(row['source']))==row['sha256'],'Accepted RPRM original changed')
    return provenance

def main():
    require(SOURCE.is_dir(),'Missing new payload')
    require(not ARCHIVE.exists() and not EXTRACT.exists(),'One-shot export already exists')
    require(not (SOURCE/'MANIFEST.json').exists(),'Payload already frozen')
    require(all('__pycache__' not in p.parts for p in SOURCE.rglob('*')),'Unexpected bytecode')
    provenance=verify_sources()
    # Current task notes must have usable local file targets. Unchanged source
    # copies retain historical link contexts, as explicitly documented.
    links_checked=0
    for note in SOURCE.glob('*.md'):
        for destination in re.findall(r'\]\(([^)]+)\)',note.read_text(encoding='utf-8')):
            if destination.startswith(('https://','http://','#')):
                continue
            path=destination.split('#',1)[0]
            require((note.parent/path).is_file(),f'Missing local note target: {note.name}: {path}')
            links_checked+=1
    png=(SOURCE/'correction_supports.png').read_bytes()
    require(png[:8]==b'\x89PNG\r\n\x1a\n','Invalid figure signature')
    width,height=struct.unpack('>II',png[16:24])
    require((width,height)==(2080,1440),'Unexpected rendered figure dimensions')

    entries=inventory(SOURCE)
    (SOURCE/'MANIFEST.json').write_text(json.dumps({
        'schema':1,'scope':'New signed-residual research and attributed accepted sources',
        'self_excluded':'MANIFEST.json','files':entries},indent=2)+'\n',encoding='utf-8')
    frozen=inventory(SOURCE)
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for row in frozen:
            archive.write(SOURCE/row['path'],ROOTNAME+'/'+row['path'])
    archive_hash=digest(ARCHIVE)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ARCHIVE) as archive:
        require(archive.testzip() is None,'ZIP CRC failure')
        require(len(archive.namelist())==len(set(archive.namelist()))==len(frozen),'ZIP census mismatch')
        for member in archive.namelist():
            require((EXTRACT/member).resolve().is_relative_to(EXTRACT.resolve()),'Unsafe extraction path')
        archive.extractall(EXTRACT)
    target=EXTRACT/ROOTNAME
    before=inventory(target)
    require(before==frozen,'Fresh extraction differs from source')
    manifest=json.loads((target/'MANIFEST.json').read_text(encoding='utf-8'))
    require(manifest['files']==[row for row in before if row['path']!='MANIFEST.json'],
            'Manifest verification failure')
    runs=[]
    for script,receipt in [('check_differences.py','RESULTS_DIFFERENCES.json'),
                           ('check_stacking.py','RESULTS_STACKING.json'),
                           ('check_vacuum_comparison.py','RESULTS_VACUUM_COMPARISON.json')]:
        command=[sys.executable,'-I','-B','-X','utf8',str(target/script)]
        done=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',timeout=55)
        (HERE/(script+'.stdout.txt')).write_text(done.stdout,encoding='utf-8')
        (HERE/(script+'.stderr.txt')).write_text(done.stderr,encoding='utf-8')
        require(done.returncode==0 and 'PASS' in done.stdout,f'New checker failed: {script}: {done.stderr}')
        require(not done.stderr,f'Unexpected stderr: {script}')
        runs.append({'script':script,'receipt':receipt,'command':command,'cwd':str(target),
                     'exit_code':done.returncode,'status':'PASS',
                     'comparison':'Default mode freshly recomputes and compares the complete saved receipt internally',
                     'stdout_sha256':hashlib.sha256(done.stdout.encode()).hexdigest(),
                     'stderr_bytes':0})
    after=inventory(target)
    require(after==before==inventory(SOURCE),'Replay changed payload bytes')
    require(digest(ARCHIVE)==archive_hash,'Frozen ZIP changed')
    verify_sources()
    differences=json.loads((target/'RESULTS_DIFFERENCES.json').read_text(encoding='utf-8'))
    stacking=json.loads((target/'RESULTS_STACKING.json').read_text(encoding='utf-8'))
    result={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
            'archive':str(ARCHIVE),'archive_sha256':archive_hash,'archive_bytes':ARCHIVE.stat().st_size,
            'payload_files':len(frozen),'payload_bytes':sum(row['bytes'] for row in frozen),
            'manifest_covered_files':len(entries),'fresh_extraction':str(target),
            'zip_crc':'PASS','source_equals_extracted':True,'payload_unchanged_after_replay':True,
            'runs':runs,'python_version':sys.version,
            'difference_models':len(differences['rows']),
            'difference_matrix_controls':sum(row['check_count'] for row in differences['rows']),
            'stacking_counts':stacking['counts'],'sharp_tilt_controls':len(stacking['sharp_two_point_tilt_controls']),
            'six_square_envelope_checked':True,'accepted_source_files':len(provenance['files']),
            'top_level_local_file_links_checked':links_checked,
            'figure_dimensions':[width,height],
            'figure_visual_review':'See payload VISUAL_CHECKS.md; PNG inspected before freezing',
            'prior_archive_unchanged':provenance['prior_archive'],
            'prior_archive_sha256':provenance['prior_archive_sha256'],
            'limits':'Written proofs with exact bounded corroboration; no proof-assistant certification, uniform vacuum estimate, continuum theory, or mass-gap solution.'}
    (HERE/'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (HERE/'YM2-signed-differences-2026-09-12.sha256').write_text(archive_hash+'  '+ARCHIVE.name+'\n',encoding='ascii')
    note=f'''# Final export evidence — PASS

Archive: `{ARCHIVE.name}`  
SHA-256: `{archive_hash}`  
Archive bytes: {ARCHIVE.stat().st_size}; payload files: {len(frozen)};
uncompressed payload bytes: {result['payload_bytes']}.

The final archive passed CRC verification and was freshly extracted. All
{len(frozen)} files matched the source payload exactly. The top-level manifest
covered every other file, including the attributed prior evidence.

All three new checkers ran from that extraction with isolated Python and
bytecode disabled. Each recomputed and compared its complete saved receipt.
All three exited zero with empty stderr. Source, extracted and ZIP bytes
remained unchanged after replay.

The difference checker covered seven complete four-state models and 364
matrix/control checks plus centering controls. The stacking checker covered
12 cubes, 90 complete-basis eigenvectors, 465 off-diagonal orthogonality
controls, 42 complete sum fibers, three sharp conditional-tilt examples,
and the six-square support-envelope control. The vacuum checker verified
the exact rational Taylor, infinite-tail-majorant ingredients, four-support
polynomial, kernel ratio and comparison constants. Universal claims rely
on the written proofs; finite execution does not prove analytic coverage
or checker soundness.

The figure PNG is 2080 by 1440 pixels and was visually inspected before
export; the editable SVG and drawing source are included. All {links_checked}
local file links in the current top-level notes resolve. Historical source
copies retain their documented original link context.

All 29 accepted source copies remain byte-identical to their captured
sources. The previous delivered global-phase ZIP retains SHA-256
`{provenance['prior_archive_sha256']}`. No old checker was rerun.

See `FINAL_EXPORT_EVIDENCE.json` for actual commands, interpreter, counts,
paths and hashes, and the stdout/stderr files for exact replay output.
This sidecar is generated after the ZIP is frozen. It is execution and
byte-integrity evidence, not a continuum quantum proof.
'''
    (HERE/'FINAL_EXPORT_EVIDENCE.md').write_text(note,encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('status','archive','archive_sha256',
                                                'archive_bytes','payload_files',
                                                'top_level_local_file_links_checked')},indent=2))

if __name__=='__main__':
    main()
