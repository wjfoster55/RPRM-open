"""Freeze new construction research and replay only its checker from fresh extraction."""
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import struct
import subprocess
import sys
import zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ym2_conditional_construction'
ZIP=HERE/'YM2-conditional-construction-2026-09-12.zip'
EXTRACT=HERE/'final-extraction'
ROOT='YM2-conditional-construction'

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(path):return sha256(path.read_bytes()).hexdigest()
def inventory(root):
    return [{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
            for p in sorted(root.rglob('*')) if p.is_file()]

def main():
    need(not ZIP.exists() and not EXTRACT.exists(),'Final output already exists')
    prov=json.loads((SOURCE/'SOURCE_PROVENANCE.json').read_text(encoding='utf-8'))
    prior=Path(prov['prior_archive'])
    need(digest(prior)==prov['prior_archive_sha256'],'Prior archive changed')
    for row in prov['files']:
        need(digest(SOURCE/row['payload_path'])==row['sha256'],'Retained source changed')
        need(digest(Path(row['source_path']))==row['sha256'],'Current source differs from retained bytes')
    review=(SOURCE/'CONSTRUCTION_REVIEW.md').read_text(encoding='utf-8').lower()
    for name,expected in prov['reviewed_files'].items():
        need(digest(SOURCE/name)==expected,'Reviewed theorem changed: '+name)
        need(expected in review,'Final independent hash binding missing: '+name)
    links=[]
    for p in SOURCE.glob('*.md'):
        prose=re.sub(r'```[\s\S]*?```','',p.read_text(encoding='utf-8'))
        prose=re.sub(r'`[^`\n]*`','',prose)
        for raw in re.findall(r'\]\(([^)]+)\)',prose):
            if raw.startswith(('https://','http://','#')):continue
            rel=raw[1:-1] if raw.startswith('<') and raw.endswith('>') else raw
            rel=re.sub(r':\d+$','',rel.split('#',1)[0])
            target=(p.parent/rel).resolve()
            need(target.is_relative_to(SOURCE.resolve()) and target.is_file(),
                 'Nonportable link '+p.name+': '+raw)
            need(' ' not in rel or raw.startswith('<'),'Unwrapped space in link')
            links.append({'note':p.name,'target':target.relative_to(SOURCE).as_posix()})
    dimensions=struct.unpack('>II',(SOURCE/'joint_construction.png').read_bytes()[16:24])
    need(dimensions==(3200,1800),'Figure dimension mismatch')
    need((SOURCE/'VISUAL_CHECKS.md').is_file(),'Visual inspection missing')
    need(all('__pycache__' not in p.parts for p in SOURCE.rglob('*')),'Bytecode in payload')
    rows=[row for row in inventory(SOURCE) if row['path']!='MANIFEST.json']
    (SOURCE/'MANIFEST.json').write_text(json.dumps({'schema':'ym2-construction-manifest-v1',
        'self_excluded':'MANIFEST.json','files':rows},indent=2)+'\n',encoding='utf-8')
    frozen=inventory(SOURCE)
    with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for row in frozen:z.write(SOURCE/row['path'],ROOT+'/'+row['path'])
    zip_sha=digest(ZIP)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ZIP) as z:
        need(z.testzip() is None,'ZIP CRC failure')
        need(len(z.namelist())==len(set(z.namelist()))==len(frozen),'ZIP member census')
        for name in z.namelist():
            need((EXTRACT/name).resolve().is_relative_to(EXTRACT.resolve()),'Unsafe extraction path')
        z.extractall(EXTRACT)
    target=EXTRACT/ROOT
    need(inventory(target)==frozen,'Fresh extraction byte mismatch')
    need(json.loads((target/'MANIFEST.json').read_text(encoding='utf-8'))['files']==rows,'Manifest mismatch')
    command=[sys.executable,'-I','-B','-X','utf8',str(target/'check_construction.py')]
    done=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',timeout=55)
    stdout=HERE/'check_construction.stdout.txt';stderr=HERE/'check_construction.stderr.txt'
    stdout.write_text(done.stdout,encoding='utf-8');stderr.write_text(done.stderr,encoding='utf-8')
    need(done.returncode==0 and not done.stderr,'Extracted checker failed: '+done.stderr)
    receipt=json.loads((target/'RESULTS.json').read_text(encoding='utf-8'))
    need(json.loads(done.stdout)==receipt and receipt['status']=='PASS','Full checker receipt mismatch')
    need(inventory(SOURCE)==frozen==inventory(target),'Replay changed source or extracted bytes')
    need(digest(ZIP)==zip_sha,'ZIP changed after replay')
    need(digest(prior)==prov['prior_archive_sha256'],'Prior archive changed after replay')
    result={'schema':'ym2-construction-final-export-v1','status':'PASS',
            'utc':datetime.now(timezone.utc).isoformat(),'archive':str(ZIP),'archive_sha256':zip_sha,
            'archive_bytes':ZIP.stat().st_size,'payload_files':len(frozen),
            'payload_bytes':sum(row['bytes'] for row in frozen),'manifest_covered_files':len(rows),
            'zip_crc':'PASS','fresh_extraction':str(target),'source_equals_extracted':True,
            'unchanged_after_replay':True,'command':command,'cwd':str(target),'exit_code':done.returncode,
            'stdout_file':stdout.name,'stdout_sha256':digest(stdout),'stderr_bytes':0,
            'python_version':sys.version,'accepted_snapshots':len(prov['files']),
            'prior_archive_sha256':prov['prior_archive_sha256'],'prior_archive_unchanged':True,
            'reviewed_files':prov['reviewed_files'],'top_level_file_links_checked':len(links),
            'link_records':links,'figure_dimensions':dimensions,'old_checkers_executed':False,
            'receipt':receipt,'evidence_ceiling':'Written all-spin finite-lattice proofs and independent agent audit, with exact finite controls. Export integrity is not a formal proof or a continuum gap theorem.'}
    (HERE/'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (HERE/'YM2-conditional-construction-2026-09-12.sha256').write_text(zip_sha+'  '+ZIP.name+'\n',encoding='ascii')
    (HERE/'FINAL_EXPORT_EVIDENCE.md').write_text(f'''# Final export evidence — PASS

Archive: `{ZIP.name}`  
SHA-256: `{zip_sha}`  
Bytes: {ZIP.stat().st_size}; payload files: {len(frozen)}.

The archive passed CRC, duplicate-member and extraction-path checks. A
fresh extraction matched every frozen source byte and the manifest.
The new checker recomputed and compared its entire saved receipt under
isolated Python, UTF-8 and bytecode suppression. It exited zero with
empty stderr. The source, extracted files, prior archive and new ZIP
remained unchanged after replay. No old checker was executed.

The new exact controls passed {receipt['assertions']:,} assertions: quotient
polynomial identities, direct quaternion derivatives on 24 seven-link
SU(2) configurations, the second-order residual, 2,304 finite spin pairs,
and the combined contraction and conditional-gap constants. General
all-spin and graph-uniform implications rest on written proofs with
explicit accepted dependencies, not finite extrapolation.

Four mathematical sources match the independent review's final SHA-256
bindings: GAUGE_NORM_GAIN.md, LOCAL_VACUUM_ROUTE.md, COMBINED_RESULT.md,
and TWO_SQUARE_GEOMETRY.md. Portability edits occurred before those final
bindings and changed only local link targets. No source note was silently
replaced by an unreviewed revision.

All {len(links)} new top-level file links resolve within the packet. All
{len(prov['files'])} accepted copies match their recorded source bytes.
The preceding rail archive is included unchanged. Deep historical links
inside accepted snapshots retain their original meaning and are not
claimed portable. The 3200 by 1800 explanatory figure was visually
inspected after correcting a caption near its axis ticks and shortening
an overlong line. SVG and drawing source are included.

FINAL_EXPORT_EVIDENCE.json records the interpreter, exact command, output
hash, complete receipt, source bindings, link checks and archive identity.
Actual stdout and stderr are adjacent. These sidecars were generated
after the ZIP was frozen and replayed. They establish byte/execution
integrity; they do not turn an agent review into a formal proof or imply
a continuum quantum Yang–Mills mass-gap theorem. Publication remains on hold.
''',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','archive','archive_sha256','archive_bytes',
           'payload_files','top_level_file_links_checked']},indent=2))
    print('PASS:',receipt['assertions'],'exact checks from fresh extraction')

if __name__=='__main__':main()
