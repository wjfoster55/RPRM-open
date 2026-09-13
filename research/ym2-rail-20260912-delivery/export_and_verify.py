"""Freeze the rail continuation; replay only its new checker from fresh extraction."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import struct
import subprocess
import sys
import zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ym2_rail_closure'
ZIP=HERE/'YM2-rail-closure-2026-09-12.zip'
EXTRACT=HERE/'final-extraction'
ROOT='YM2-rail-closure'

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(p):return sha256(p.read_bytes()).hexdigest()
def inventory(p):
    return [{'path':f.relative_to(p).as_posix(),'bytes':f.stat().st_size,'sha256':digest(f)}
            for f in sorted(p.rglob('*')) if f.is_file()]

def main():
    need(not ZIP.exists() and not EXTRACT.exists(),'Final output already exists')
    prov=json.loads((SOURCE/'SOURCE_PROVENANCE.json').read_text(encoding='utf-8'))
    prior=Path(prov['prior_archive'])
    need(digest(prior)==prov['prior_archive_sha256'],'Prior frozen archive changed')
    for row in prov['files']:
        need(digest(SOURCE/row['payload_path'])==row['sha256'],'Retained source bytes changed')
        if 'source_path' in row:
            need(digest(Path(row['source_path']))==row['sha256'],'Live source drift: '+row['source_path'])
    reviewed=prov['reviewed_theorem_sha256']
    need(digest(SOURCE/'CONDITIONAL_RAIL.md')==reviewed,'Reviewed theorem changed')
    need(reviewed in (SOURCE/'INDEPENDENT_REVIEW.md').read_text(encoding='utf-8').lower(),
         'Independent review binding absent')
    source_hashes={r['sha256'].lower() for r in prov['files']}
    cited_hashes=[]
    for name in ['VAULT_RECOVERY.md','RAIL_RECOVERY.md']:
        note=(SOURCE/name).read_text(encoding='utf-8')
        for h in re.findall(r'`([0-9A-Fa-f]{64})`',note):
            need(h.lower() in source_hashes,'Recovered source hash lacks a portable copy: '+h)
            cited_hashes.append(h.lower())
    links=[]
    for note in SOURCE.glob('*.md'):
        prose=re.sub(r'```[\s\S]*?```','',note.read_text(encoding='utf-8'))
        prose=re.sub(r'`[^`\n]*`','',prose)
        for raw in re.findall(r'\]\(([^)]+)\)',prose):
            if raw.startswith(('http://','https://','#')):continue
            rel=raw.strip()
            if rel.startswith('<') and rel.endswith('>'):rel=rel[1:-1]
            rel=rel.split('#',1)[0]
            rel=re.sub(r':\d+$','',rel)
            target=(note.parent/rel).resolve()
            need(target.is_relative_to(SOURCE.resolve()) and target.is_file(),
                 'Nonportable new-note link '+note.name+': '+raw)
            need(' ' not in rel or raw.startswith('<'),'Unwrapped space in Markdown link')
            links.append({'note':note.name,'target':target.relative_to(SOURCE).as_posix()})
    dims=struct.unpack('>II',(SOURCE/'rail_closure.png').read_bytes()[16:24])
    need(dims==(3200,1900),'Figure dimensions')
    need((SOURCE/'VISUAL_CHECKS.md').is_file(),'Visual inspection absent')
    need(all('__pycache__' not in p.parts for p in SOURCE.rglob('*')),'Bytecode present')
    rows=[r for r in inventory(SOURCE) if r['path']!='MANIFEST.json']
    (SOURCE/'MANIFEST.json').write_text(json.dumps({'schema':'ym2-rail-manifest-v1',
        'self_excluded':'MANIFEST.json','files':rows},indent=2)+'\n',encoding='utf-8')
    frozen=inventory(SOURCE)
    with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for row in frozen:z.write(SOURCE/row['path'],ROOT+'/'+row['path'])
    zip_sha=digest(ZIP)
    EXTRACT.mkdir()
    with zipfile.ZipFile(ZIP) as z:
        need(z.testzip() is None,'ZIP CRC failure')
        need(len(z.namelist())==len(set(z.namelist()))==len(frozen),'Member census')
        for name in z.namelist():
            need((EXTRACT/name).resolve().is_relative_to(EXTRACT.resolve()),'Unsafe ZIP path')
        z.extractall(EXTRACT)
    target=EXTRACT/ROOT
    need(inventory(target)==frozen,'Fresh extraction does not match')
    need(json.loads((target/'MANIFEST.json').read_text(encoding='utf-8'))['files']==rows,'Manifest mismatch')
    command=[sys.executable,'-I','-B','-X','utf8',str(target/'check_rail.py')]
    done=subprocess.run(command,cwd=target,capture_output=True,text=True,encoding='utf-8',timeout=55)
    stdout=HERE/'check_rail.stdout.txt';stderr=HERE/'check_rail.stderr.txt'
    stdout.write_text(done.stdout,encoding='utf-8');stderr.write_text(done.stderr,encoding='utf-8')
    need(done.returncode==0 and not done.stderr,'Extracted checker failed: '+done.stderr)
    receipt=json.loads((target/'RESULTS.json').read_text(encoding='utf-8'))
    need(json.loads(done.stdout)==receipt and receipt['status']=='PASS','Complete output receipt differs')
    need(inventory(target)==frozen==inventory(SOURCE),'Replay changed source or extraction')
    need(digest(ZIP)==zip_sha,'Archive changed after replay')
    need(digest(prior)==prov['prior_archive_sha256'],'Prior archive changed after replay')
    result={'schema':'ym2-rail-final-export-v1','status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
            'archive':str(ZIP),'archive_sha256':zip_sha,'archive_bytes':ZIP.stat().st_size,
            'payload_files':len(frozen),'payload_bytes':sum(r['bytes'] for r in frozen),
            'manifest_covered_files':len(rows),'zip_crc':'PASS','fresh_extraction':str(target),
            'source_equals_extracted':True,'unchanged_after_replay':True,'command':command,
            'cwd':str(target),'exit_code':done.returncode,'stdout_file':stdout.name,
            'stdout_sha256':digest(stdout),'stderr_bytes':0,'python_version':sys.version,
            'accepted_snapshots':len(prov['files']),'cited_source_hashes_checked':len(cited_hashes),
            'prior_archive_sha256':prov['prior_archive_sha256'],'prior_archive_unchanged':True,
            'reviewed_theorem_sha256':reviewed,'top_level_file_links_checked':len(links),
            'link_records':links,'figure_dimensions':dims,'old_checkers_executed':False,
            'receipt':receipt,'evidence_ceiling':'Written proofs and independent agent review plus exact bounded controls. Export integrity does not prove general mathematics, cryptographic security, or a continuum mass gap.'}
    (HERE/'FINAL_EXPORT_EVIDENCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (HERE/'YM2-rail-closure-2026-09-12.sha256').write_text(zip_sha+'  '+ZIP.name+'\n',encoding='ascii')
    (HERE/'FINAL_EXPORT_EVIDENCE.md').write_text(f'''# Final export evidence — PASS

Archive: `{ZIP.name}`  
SHA-256: `{zip_sha}`  
Bytes: {ZIP.stat().st_size}; payload files: {len(frozen)}.

The archive passed CRC, duplicate-name and extraction-path checks. A fresh
extraction matched every frozen source byte and the manifest. The new
standard-library checker recomputed and compared its complete saved receipt
under isolated Python with UTF-8 and bytecode suppression. It exited zero
with empty stderr. All source, extracted and archive bytes remained
unchanged after replay. No earlier checker was executed.

The new controls passed {receipt['assertions']:,} exact rational assertions:
272 positive joint-law families and their coordinate orders, compatible
rectangles, an incompatible kernel pair, exact four-state eigenfunctions,
normalized chart composition, signed approximation defects, weighted
influence comparison, and a minimal stale-revision control. These controls
do not prove the continuous SU(2) implications or their missing premises;
those claims have written derivations and stated evidence grades.

The reviewed conditional theorem matches SHA-256 `{reviewed}` recorded
by the separate mathematical reviewer. The review includes the applied
uniformity clarification and does not certify a new actual YM window.

All {len(links)} new top-level file links resolve within the packet, including
correctly wrapped filenames containing spaces. All {len(prov['files'])} retained
source copies match their recorded bytes; {len(cited_hashes)} source hashes in
the recovery notes are represented by matching portable copies. Historical
deep links inside accepted snapshots retain their original meaning and are
not claimed to be portable. The preceding frozen vacuum-handoff archive is
included unchanged. The bounded Memory Fabric packet, omission search,
expansion and scope note preserve the retrieval boundary.

The final 3200 by 1900 figure was visually inspected after correcting one
caption overlap. Its SVG and source are included. It shows a schematic
identity and exact auxiliary values, not a physical simulation.

FINAL_EXPORT_EVIDENCE.json records the interpreter, command, output hashes,
complete new receipt, archive identity, source bindings and link records.
The actual stdout and stderr are adjacent. These evidence sidecars were
written after freezing and replaying the ZIP; they establish execution
and byte integrity, not self-certified mathematical truth.
''',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','archive','archive_sha256','archive_bytes',
          'payload_files','top_level_file_links_checked','cited_source_hashes_checked']},indent=2))
    print('PASS:',receipt['assertions'],'exact rational assertions from fresh extraction')

if __name__=='__main__':main()
