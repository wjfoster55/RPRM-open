"""Freeze this new continuation and replay only its new exact checker."""
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ym2_estimate_continuation'
ZIP=HERE/'YM2-estimate-continuation-2026-09-12-v2.zip'
EXTRACT=HERE/'final-extraction-v2'
ROOT='YM2-estimate-continuation'

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(p):return sha256(p.read_bytes()).hexdigest()
def inventory(p):
    return [{'path':f.relative_to(p).as_posix(),'bytes':f.stat().st_size,'sha256':digest(f)}
            for f in sorted(p.rglob('*')) if f.is_file()]

def main():
    need(not ZIP.exists() and not EXTRACT.exists(),'Final revision already frozen')
    provenance=json.loads((SOURCE/'SOURCE_PROVENANCE.json').read_text(encoding='utf-8'))
    prior=Path(provenance['prior_archive'])
    need(digest(prior)==provenance['prior_archive_sha256'],'Prior archive changed')
    for r in provenance['files']:need(digest(SOURCE/r['payload_path'])==r['sha256'],'Accepted copy changed')
    links=[]
    for note in SOURCE.glob('*.md'):
        for raw in re.findall(r'\]\(([^)]+)\)',note.read_text(encoding='utf-8')):
            if raw.startswith(('http://','https://','#')):continue
            target=(note.parent/raw.split('#')[0]).resolve()
            need(target.is_relative_to(SOURCE.resolve()) and target.is_file(),'Nonportable or missing link '+note.name+': '+raw)
            links.append({'note':note.name,'target':target.relative_to(SOURCE).as_posix()})
    need((SOURCE/'COMBINED_REVIEW.md').is_file(),'Missing independent review')
    need((SOURCE/'VISUAL_CHECKS.md').is_file(),'Missing visual review')
    need(all('__pycache__' not in p.parts for p in SOURCE.rglob('*')),'Bytecode in payload')
    dims=struct.unpack('>II',(SOURCE/'scale_changes.png').read_bytes()[16:24])
    need(dims==(2800,1200),'Figure dimensions')
    rows=[row for row in inventory(SOURCE) if row['path']!='MANIFEST.json']
    (SOURCE/'MANIFEST.json').write_text(json.dumps({'schema':'ym2-estimate-manifest-v1',
        'self_excluded':'MANIFEST.json','files':rows},indent=2)+'\n',encoding='utf-8')
    frozen=inventory(SOURCE)
    with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for r in frozen:z.write(SOURCE/r['path'],ROOT+'/'+r['path'])
    zip_sha=digest(ZIP);EXTRACT.mkdir()
    with zipfile.ZipFile(ZIP) as z:
        need(z.testzip() is None,'CRC failure')
        need(len(z.namelist())==len(set(z.namelist()))==len(frozen),'ZIP census')
        for name in z.namelist():need((EXTRACT/name).resolve().is_relative_to(EXTRACT.resolve()),'Unsafe member')
        z.extractall(EXTRACT)
    target=EXTRACT/ROOT
    need(inventory(target)==frozen,'Extraction mismatch')
    need(json.loads((target/'MANIFEST.json').read_text(encoding='utf-8'))['files']==rows,'Manifest mismatch')
    command=[sys.executable,'-I','-B','-X','utf8',str(target/'check_continuation.py')]
    done=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',timeout=55)
    out=HERE/'check_continuation.stdout.txt';err=HERE/'check_continuation.stderr.txt'
    out.write_text(done.stdout,encoding='utf-8');err.write_text(done.stderr,encoding='utf-8')
    need(done.returncode==0 and not done.stderr and 'PASS' in done.stdout,'New checker failed '+done.stderr)
    need(inventory(target)==frozen==inventory(SOURCE),'Replay changed bytes')
    need(digest(ZIP)==zip_sha and digest(prior)==provenance['prior_archive_sha256'],'Archive changed')
    result={'schema':'ym2-estimate-final-export-v1','status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
        'archive':str(ZIP),'archive_sha256':zip_sha,'archive_bytes':ZIP.stat().st_size,
        'payload_files':len(frozen),'payload_bytes':sum(r['bytes'] for r in frozen),
        'manifest_covered_files':len(rows),'zip_crc':'PASS','fresh_extraction':str(target),
        'source_equals_extracted':True,'unchanged_after_replay':True,'command':command,'cwd':str(target),
        'exit_code':done.returncode,'stdout_file':out.name,'stdout_sha256':digest(out),'stderr_bytes':0,
        'python_version':sys.version,'accepted_files':len(provenance['files']),
        'prior_archive_sha256':provenance['prior_archive_sha256'],'file_links_checked':len(links),
        'link_records':links,'figure_dimensions':dims,
        'receipt':json.loads((target/'RESULTS.json').read_text(encoding='utf-8')),
        'evidence_ceiling':'Written proofs and independent agent audits, with finite exact corroboration; not formal certification or a continuum mass-gap theorem.'}
    (HERE/'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (HERE/'YM2-estimate-continuation-2026-09-12-v2.sha256').write_text(zip_sha+'  '+ZIP.name+'\n',encoding='ascii')
    (HERE/'FINAL_EXPORT_EVIDENCE.md').write_text(f'''# Final export evidence — PASS

Archive: `{ZIP.name}`  
SHA-256: `{zip_sha}`  
Bytes: {ZIP.stat().st_size}; payload files: {len(frozen)}.

The final ZIP passed CRC, duplicate-name and extraction-path checks. A fresh
extraction matched all frozen source files and the manifest. The extracted
new checker recomputed and compared its complete saved receipt under isolated
Python with UTF-8 and bytecode disabled. It exited zero with empty stderr.
All source, extracted and archive bytes remained unchanged after replay.

The new exact controls cover source/swap matrices, 4,096 spin pairs, scalar
restart and improved radii, conditional constants and hostile cases. They
corroborate bounded calculations; the general claims rely on the written
analysis and independent review. No old checker was executed.

All {len(links)} top-level local file links resolve inside the portable packet.
The four accepted source copies match their original frozen ZIP bytes; the
prior archive retains SHA-256 `{provenance['prior_archive_sha256']}`.
The 2800 by 1200 explanatory figure was visually reviewed; source and SVG
are included. It is an illustration, not a simulation.

FINAL_EXPORT_EVIDENCE.json records the command, interpreter, output hash,
paths, full new receipt and link records. Actual stdout/stderr files are
adjacent. This evidence was generated after freezing the ZIP and establishes
byte and execution integrity, not mathematical truth by itself.
''',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','archive','archive_sha256','archive_bytes','payload_files','file_links_checked']},indent=2))
    print(done.stdout.strip())

if __name__=='__main__':main()
