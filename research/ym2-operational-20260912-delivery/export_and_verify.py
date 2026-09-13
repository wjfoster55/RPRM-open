"""Freeze once, extract safely, replay only new stdlib checker, bind evidence."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,re,struct,subprocess,sys,zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ym2_operational_seam'
ZIP=HERE/'YM2-operational-seam-2026-09-12.zip'
EXTRACT=HERE/'final-extraction'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(p):return sha256(p.read_bytes()).hexdigest()
def inventory(root):
    return [{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
            for p in sorted(root.rglob('*')) if p.is_file()]
need(not ZIP.exists() and not EXTRACT.exists(),'Final export already exists')
prov=json.loads((SOURCE/'SOURCE_PROVENANCE.json').read_text(encoding='utf-8-sig'))
for row in prov['files']:
    need(digest(SOURCE/row['payload_path'])==row['sha256'],'Snapshot differs')
    need(digest(Path(row['source_path']))==row['sha256'],'Donor source changed; snapshot needs review')
review=(SOURCE/'OPERATIONAL_REVIEW.md').read_text(encoding='utf-8')
for name,expected in prov['reviewed_files'].items():
    need(digest(SOURCE/name)==expected and expected in review,'Final review binding missing or changed: '+name)
links=[]
for p in SOURCE.glob('*.md'):
    prose=re.sub(r'```[\s\S]*?```','',p.read_text(encoding='utf-8'))
    for raw in re.findall(r'\]\(([^)]+)\)',prose):
        if raw.startswith(('https://','http://','#')):continue
        rel=raw.strip('<>').split('#',1)[0];target=(p.parent/rel).resolve()
        need(target.is_relative_to(SOURCE.resolve()) and target.is_file(),'Nonportable link: '+raw)
        links.append({'source':p.name,'target':target.relative_to(SOURCE).as_posix()})
dimensions=struct.unpack('>II',(SOURCE/'operational_seam.png').read_bytes()[16:24])
need(dimensions==(3200,1800) and (SOURCE/'VISUAL_CHECKS.md').is_file(),'Visual evidence missing')
need(not any('__pycache__' in p.parts for p in SOURCE.rglob('*')),'Bytecode in payload')
rows=[r for r in inventory(SOURCE) if r['path']!='MANIFEST.json']
(SOURCE/'MANIFEST.json').write_text(json.dumps({'schema':'ym2-operational-manifest-v1','self_excluded':'MANIFEST.json','files':rows},indent=2)+'\n',encoding='utf-8')
frozen=inventory(SOURCE)
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for row in frozen:z.write(SOURCE/row['path'],'YM2-operational-seam/'+row['path'])
sha=digest(ZIP)
EXTRACT.mkdir()
with zipfile.ZipFile(ZIP) as z:
    need(z.testzip() is None,'ZIP CRC failed')
    need(len(z.namelist())==len(set(z.namelist()))==len(frozen),'ZIP member census failed')
    for n in z.namelist():need((EXTRACT/n).resolve().is_relative_to(EXTRACT.resolve()),'Unsafe path')
    z.extractall(EXTRACT)
target=EXTRACT/'YM2-operational-seam'
need(inventory(target)==frozen,'Extraction byte mismatch')
command=[sys.executable,'-I','-B','-X','utf8',str(target/'check_operational.py')]
run=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',timeout=55)
(HERE/'check_operational.stdout.txt').write_text(run.stdout,encoding='utf-8')
(HERE/'check_operational.stderr.txt').write_text(run.stderr,encoding='utf-8')
need(run.returncode==0 and not run.stderr,'Fresh extracted checker failed: '+run.stderr)
receipt=json.loads((target/'RESULTS.json').read_text(encoding='utf-8-sig'))
need(json.loads(run.stdout)==receipt and receipt['status']=='PASS','Complete receipt differs')
need(inventory(SOURCE)==frozen==inventory(target) and digest(ZIP)==sha,'Replay changed frozen bytes')
for row in prov['files']:
    need(digest(Path(row['source_path']))==row['sha256'],'Accepted original changed during final export')
ev={'schema':'ym2-operational-final-export-v1','status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
    'archive':str(ZIP),'archive_sha256':sha,'archive_bytes':ZIP.stat().st_size,
    'payload_files':len(frozen),'manifest_covered_files':len(rows),'snapshots':len(prov['files']),
    'zip_crc':'PASS','duplicate_and_path_checks':'PASS','source_equals_fresh_extraction':True,
    'unchanged_after_replay':True,'fresh_extraction':str(target),'command':command,'cwd':str(target),
    'python_version':sys.version,'exit_code':run.returncode,'stderr_bytes':0,
    'stdout_sha256':digest(HERE/'check_operational.stdout.txt'),'reviewed_files':prov['reviewed_files'],
    'top_level_links':links,'figure_dimensions':dimensions,'prior_archive_sha256':prov['prior_archive_sha256'],
    'original_sources_unchanged':True,'old_checkers_executed':False,'receipt':receipt,
    'ceiling':'Written scoped proofs and independent agent review with exact finite controls; byte integrity is not formal proof or a continuum mass-gap theorem.'}
(HERE/'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(ev,indent=2)+'\n',encoding='utf-8')
(HERE/'YM2-operational-seam-2026-09-12.sha256').write_text(sha+'  '+ZIP.name+'\n',encoding='ascii')
(HERE/'FINAL_EXPORT_EVIDENCE.md').write_text(f'''# Final export evidence — PASS

Archive: `{ZIP.name}`  
SHA-256: `{sha}`  
Size: {ZIP.stat().st_size} bytes; {len(frozen)} payload files.

The ZIP passed CRC, duplicate-member and extraction-path checks. Every
freshly extracted file matched the frozen source and manifest. The new
standard-library checker passed {receipt['assertions']} exact assertions
under isolated Python with bytecode disabled. Its entire JSON output
matched RESULTS.json, with zero exit status and empty stderr. Source,
extraction and ZIP bytes remained unchanged after replay. No old checker
was run, and no package installation was needed for portable replay.

Four reviewed notes match the independent review's final SHA-256 bindings.
All {len(links)} top-level local links resolve inside the packet; all
{len(prov['files'])} accepted snapshots match their recorded originals.
The previous frozen YM construction ZIP is included unchanged. Historical
links inside unchanged snapshots are not asserted portable. The final
3200 by 1800 plot was visually inspected and its annotation was moved to
avoid the response curves; PNG, SVG and drawing source are included.

FINAL_EXPORT_EVIDENCE.json records the exact interpreter, command, receipt,
link checks, source hashes, review bindings and archive identity. Actual
stdout/stderr are adjacent. These sidecars were created after freezing and
replaying the ZIP. This is execution and byte evidence for the delivered
packet, not a formal proof, external peer review, novelty certificate or
quantum Yang-Mills continuum mass-gap result. Publication remains on hold.
''',encoding='utf-8')
print(json.dumps({k:ev[k] for k in ['status','archive','archive_sha256','archive_bytes','payload_files','snapshots']},indent=2))
print('PASS',receipt['assertions'],'new exact assertions;',len(links),'portable top-level links')
