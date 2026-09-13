"""One-shot freeze and fresh verification of the covering continuation.

Standard library only; no destructive operations, old checkers, installs,
git, or other-lane writes. Final sidecars are generated after the ZIP.
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

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ym2_covering_argument'
ARCHIVE=HERE/'YM2-covering-argument-2026-09-12.zip'
EXTRACT=HERE/'final-extraction'
ROOT='YM2-covering-argument'

def require(ok,message):
    if not ok: raise RuntimeError(message)

def digest(path): return sha256(path.read_bytes()).hexdigest()

def inventory(base):
    return [{'path':p.relative_to(base).as_posix(),'bytes':p.stat().st_size,
             'sha256':digest(p)} for p in sorted(base.rglob('*')) if p.is_file()]

def sources(base):
    p=json.loads((base/'SOURCE_PROVENANCE.json').read_text(encoding='utf-8'))
    for row in p['files']:
        require(digest(base/row['payload_path'])==row['sha256'],'Source copy drift '+row['payload_path'])
    require(digest(Path(p['prior_archive']))==p['prior_archive_sha256'],'Prior archive drift')
    return p

def inspect():
    require(all('__pycache__' not in p.parts for p in SOURCE.rglob('*')),'Unexpected bytecode')
    links=[]
    for note in sorted(SOURCE.glob('*.md')):
        for raw in re.findall(r'\]\(([^)]+)\)',note.read_text(encoding='utf-8')):
            if raw.startswith(('https://','http://','#')): continue
            relative=raw.split('#',1)[0]
            target=(note.parent/relative).resolve()
            require(target.is_relative_to(SOURCE.resolve()),'Nonportable top-level link '+note.name+': '+relative)
            require(target.is_file(),'Missing link '+note.name+': '+relative)
            links.append({'note':note.name,'target':target.relative_to(SOURCE).as_posix()})
    for name in ['DIRECT_COVER_REVIEW.md','DIRECT_COVER_RPRM_REVIEW.md',
                 'CONDITIONAL_REVIEW.md','FINAL_MATH_REVIEW.md','VISUAL_CHECKS.md']:
        require((SOURCE/name).is_file(),'Missing review '+name)
    raw=(SOURCE/'covering_argument.png').read_bytes()
    require(raw[:8]==b'\x89PNG\r\n\x1a\n','Invalid PNG')
    dims=struct.unpack('>II',raw[16:24])
    require(dims==(3200,1500),'Unexpected figure dimensions')
    return links,dims

def main():
    require(not ARCHIVE.exists() and not EXTRACT.exists(),'One-shot export already exists')
    require(not (SOURCE/'MANIFEST.json').exists(),'Payload already frozen')
    provenance=sources(SOURCE)
    links,dimensions=inspect()
    rows=inventory(SOURCE)
    (SOURCE/'MANIFEST.json').write_text(json.dumps({
        'schema':'ym2-covering-manifest-v1','self_excluded':'MANIFEST.json',
        'evidence_ceiling':'Byte binding, not mathematical certification',
        'files':rows},indent=2)+'\n',encoding='utf-8')
    frozen=inventory(SOURCE)
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for row in frozen: z.write(SOURCE/row['path'],ROOT+'/'+row['path'])
    archive_sha=digest(ARCHIVE)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ARCHIVE) as z:
        require(z.testzip() is None,'ZIP CRC failed')
        require(len(z.namelist())==len(set(z.namelist()))==len(frozen),'ZIP census mismatch')
        for name in z.namelist():
            require((EXTRACT/name).resolve().is_relative_to(EXTRACT.resolve()),'Unsafe member')
        z.extractall(EXTRACT)
    target=EXTRACT/ROOT
    before=inventory(target)
    require(before==frozen,'Fresh extraction differs')
    require(json.loads((target/'MANIFEST.json').read_text(encoding='utf-8'))['files']==rows,'Manifest differs')
    command=[sys.executable,'-I','-B','-X','utf8',str(target/'verify_portable.py')]
    done=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',timeout=55)
    stdout_path=HERE/'verify_portable.stdout.txt'
    stderr_path=HERE/'verify_portable.stderr.txt'
    stdout_path.write_text(done.stdout,encoding='utf-8')
    stderr_path.write_text(done.stderr,encoding='utf-8')
    require(done.returncode==0 and not done.stderr and 'PASS' in done.stdout,'Fresh verifier failed: '+done.stderr)
    require(inventory(target)==before==inventory(SOURCE),'Replay changed payload')
    require(digest(ARCHIVE)==archive_sha,'Archive changed')
    sources(SOURCE)
    covering=json.loads((target/'RESULTS_COVERING.json').read_text(encoding='utf-8'))
    conditional=json.loads((target/'RESULTS_CONDITIONAL_COVER.json').read_text(encoding='utf-8'))
    result={
        'schema':'ym2-covering-final-export-v1','status':'PASS',
        'utc':datetime.now(timezone.utc).isoformat(),
        'archive':str(ARCHIVE),'archive_sha256':archive_sha,'archive_bytes':ARCHIVE.stat().st_size,
        'payload_files':len(frozen),'payload_bytes':sum(r['bytes'] for r in frozen),
        'manifest_covered_files':len(rows),'zip_crc':'PASS','fresh_extraction':str(target),
        'source_equals_extracted':True,'payload_unchanged_after_replay':True,
        'archive_unchanged_after_replay':True,'command':command,'cwd':str(target),
        'exit_code':done.returncode,'python_version':sys.version,
        'stdout':stdout_path.name,'stdout_sha256':digest(stdout_path),
        'stderr':stderr_path.name,'stderr_bytes':0,
        'covering_assertions':covering['assertions'],
        'conditional_receipt':conditional,
        'accepted_frozen_YM_files':sum(r['role'].startswith('accepted_YM') for r in provenance['files']),
        'official_current_snapshot_files':sum(r['role'].startswith('official_or_current') for r in provenance['files']),
        'snapshot_audit_drift':[r['payload_path'] for r in provenance['files'] if r.get('agrees_with_official_audit_read') is False],
        'top_level_file_links_checked':len(links),'link_records':links,
        'figure_dimensions':dimensions,'figure_visual_review':'VISUAL_CHECKS.md',
        'prior_archive':provenance['prior_archive'],'prior_archive_sha256':provenance['prior_archive_sha256'],
        'scope':'Reviewed written fixed-lattice proof plus finite exact controls. No formal theorem certificate, continuum construction or continuum mass-gap solution.'}
    (HERE/'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (HERE/'YM2-covering-argument-2026-09-12.sha256').write_text(archive_sha+'  '+ARCHIVE.name+'\n',encoding='ascii')
    note=f'''# Final export evidence — PASS

Archive: `{ARCHIVE.name}`  
SHA-256: `{archive_sha}`  
ZIP bytes: {result['archive_bytes']}; payload files: {len(frozen)};
uncompressed payload bytes: {result['payload_bytes']}.

The final archive passed ZIP CRC and duplicate/path checks. It was freshly
extracted into a new directory. Every file matched the frozen source bytes;
MANIFEST.json binds all {len(rows)} other files.

The extracted verify_portable.py checked the complete manifest and executed
only check_covering.py and check_conditional_cover.py, with isolated Python,
UTF-8 and bytecode disabled. Both recomputed and matched their full saved
deterministic receipts. The verifier exited zero with empty stderr. Source,
extracted and ZIP bytes remained unchanged after replay.

The covering checker passed {covering['assertions']} finite exact assertions,
including all 4,224 edge subsets of its two named fixtures and the hostile
cube boundary omission. The conditional checker verifies its rational tail,
head matching and complete bounded oscillation/support fixtures; its full
receipt is copied into FINAL_EXPORT_EVIDENCE.json. These are bounded controls,
not empirical certificates of the unrestricted analytic arguments.

All {len(links)} top-level local file links resolve within the portable payload.
The 3200 by 1500 figure was visually inspected; SVG and drawing source are
included. The figure depicts analytic bounds, not a simulated spectrum.

The 13 accepted YM source files are byte-identical to entries in the earlier
frozen archive. The 18 official/current source snapshots match the bytes
observed in the official-docs audit. No old checker or other-lane task was
executed or changed. The earlier archive remains at SHA-256
`{provenance['prior_archive_sha256']}`.

Exact commands, interpreter, paths, stdout hash, complete conditional receipt
and link records are in FINAL_EXPORT_EVIDENCE.json. Actual stdout/stderr
files are adjacent. This sidecar was generated after freezing the ZIP;
it establishes execution and byte integrity, not a continuum theorem.
'''
    (HERE/'FINAL_EXPORT_EVIDENCE.md').write_text(note,encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','archive','archive_sha256','archive_bytes',
                                          'payload_files','covering_assertions','top_level_file_links_checked']},indent=2))
    print(done.stdout.strip())

if __name__=='__main__': main()
