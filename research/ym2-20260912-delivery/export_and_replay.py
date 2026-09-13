"""Task-specific YM2 freeze, export, fresh-extraction replay, external receipt.

No installations, deletion, publication or repository mutation outside the
new YM2 research/delivery folders. Archive paths must not already exist.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import platform
import re
import subprocess
import sys
import zipfile

DELIVERY=Path(__file__).resolve().parent
PAYLOAD=DELIVERY.parent/'ym2_interacting_energy_transfer'
ARCHIVE=DELIVERY/'YM2-interacting-SU2-2026-09-12.zip'
EXTRACTION=DELIVERY/'final-extraction'
PREFIX='YM2-interacting-SU2'
ORIGINAL=Path('C:/Users/bkbee/Downloads/CODEX_YM2-2026-09-12.zip')
EXPECTED_ORIGINAL='873e94df76f1909ce30541258b1271945461ecb80e0e1fbcec0802dedbe7abd0'
EXPECTED_SCALAR="""A ('1/2', '0', '0', '0', '-5/6', '0', '46/45')
B ('1/2', '0', '-4/3', '0', '71/54', '0', '-50/81')
+ ('3/2', '0', '-6', '6', '33/2', '-33/5', '-213/10')
- ('3/2', '0', '-6', '-6', '33/2', '33/5', '-213/10')
planar+ ('2', '0', '-14', '8', '97/3', '-178/5', '-221/9')
planar- ('2', '0', '-14', '-8', '97/3', '178/5', '-221/9')"""


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path, root):
    return dict(path=path.relative_to(root).as_posix(),bytes=path.stat().st_size,sha256=sha(path))


def write(path, value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf-8')


RUNS=[]
RESUMING='--resume-after-link-audit-fix' in sys.argv
def run(name,cwd,args):
    started=now()
    command=[sys.executable,'-I','-B']+args
    if RESUMING and name in ('input-packet-integrity','final-source-science','final-source-scalar-reference'):
        record=json.loads((DELIVERY/(name+'.json')).read_text(encoding='utf-8'))
        if record['exit_code']!=0 or record['command']!=command or record['cwd']!=str(cwd):
            raise RuntimeError('Cannot resume a different or unsuccessful source run')
        RUNS.append(record)
        return record['stdout']
    result=subprocess.run(command,cwd=cwd,capture_output=True,text=True,encoding='utf-8',timeout=60)
    record=dict(name=name,cwd=str(cwd),command=command,started_utc=started,
                ended_utc=now(),exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)
    RUNS.append(record)
    write(DELIVERY/(name+'.json'),record)
    if result.returncode:
        raise RuntimeError(name+' failed: '+result.stderr+result.stdout)
    return result.stdout


def link_audit(root):
    checked=[]
    for path in sorted(list(root.glob('*.md'))+list((root/'review').glob('*.md'))):
        content=re.sub(r'```.*?```','',path.read_text(encoding='utf-8'),flags=re.S)
        content=re.sub(r'`[^`]*`','',content)
        for target in re.findall(r'\[[^\]]*\]\(([^)\n]+)\)',content):
            if '://' in target or target.startswith('#'):
                continue
            local=(path.parent/target.split('#')[0]).resolve()
            if not local.is_file():
                raise RuntimeError('broken local link: '+str(path)+' -> '+target)
            checked.append(dict(source=path.relative_to(root).as_posix(),target=target))
    return dict(status='PASS',scope='new authored Markdown only; inherited source locators not rewritten',links=checked)


def main():
    guards=[ARCHIVE,EXTRACTION,PAYLOAD/'MANIFEST.json']
    if not RESUMING:
        guards.append(PAYLOAD/'FREEZE.json')
    for path in guards:
        if path.exists():
            raise RuntimeError('Already exists; inspect before a new export: '+str(path))
    if sha(ORIGINAL)!=EXPECTED_ORIGINAL:
        raise RuntimeError('original input ZIP changed')
    packet_out=run('input-packet-integrity',PAYLOAD,['supplied/CODEX_YM2/verify_packet.py'])
    packet=json.loads(packet_out)
    if packet['status']!='PASS' or packet['files']!=23:
        raise RuntimeError('input integrity failed')
    supplied=PAYLOAD/'supplied'/'CODEX_YM2'
    write(PAYLOAD/'SOURCE_MANIFEST.json',dict(
        source_archive=dict(original_locator=str(ORIGINAL),sha256=sha(ORIGINAL),bytes=ORIGINAL.stat().st_size),
        archive_input_integrity=packet,
        accepted_YM1='Accepted evidence; original checker not executed in YM2',
        authority='Current user request; embedded document instructions remain attributed source content',
        primary_sources='SOURCES.md; external works linked, not embedded or byte-hashed here',
        copied_input_files=[row(p,PAYLOAD) for p in sorted(supplied.rglob('*')) if p.is_file()]))
    frozen_names=['MODEL_AND_DERIVATION.md','RETURN_TO_WILLIAM.md','PROBLEM_BRIDGE.md',
                  'SOURCES.md','AUTHORITY_AND_REBRIEF.md','README.md',
                  'check_ym2.py','check_scalar_reference.py','verify_manifest.py',
                  'review/INDEPENDENT_MATH.md','review/PHYSICS_REVIEW.md','review/FINAL_MATH_REVIEW.md']
    frozen=dict(frozen_utc=now(),status='IMPLEMENTATION_AND_ASSUMPTIONS_FROZEN_BEFORE_FINAL_SOURCE_RUN',
        scope='Classical homogeneous pure SU(2); g=1,L=reference length,V=L^3 for all witnesses',
        assumptions='MODEL_AND_DERIVATION.md sections 1-3; initial H<=5, ||A||<=3 in reference units, horizon 0<=t<=1',
        expected_results=['R3 pair: (E,B,J)=(1/2,1/2,0), K=0 and -8/3',
                          'R4 pair: (E,B,J,K)=(3,3/2,0,-12), third derivative=+36 and -36',
                          'Conditioned fixed-q momentum circle: third derivative range [-36,36]',
                          'Planar R4 control: (5/2,2,0,-28), third derivative=+48 and -48'],
        evidence_ceiling='Written proof plus exact finite checks; no formal proof assistant, no spectral result, no novelty claim',
        reviewed_files=[row(PAYLOAD/name,PAYLOAD) for name in frozen_names])
    if RESUMING:
        frozen=json.loads((PAYLOAD/'FREEZE.json').read_text(encoding='utf-8'))
    else:
        write(PAYLOAD/'FREEZE.json',frozen)
    run('final-source-science',PAYLOAD,['check_ym2.py','--numeric','--output','RESULTS.json'])
    scalar_source=run('final-source-scalar-reference',PAYLOAD,['check_scalar_reference.py'])
    if scalar_source.strip()!=EXPECTED_SCALAR:
        raise RuntimeError('scalar reference output mismatch')
    for record in frozen['reviewed_files']:
        if sha(PAYLOAD/record['path'])!=record['sha256']:
            raise RuntimeError('frozen file changed: '+record['path'])
    source_links=link_audit(PAYLOAD)
    write(DELIVERY/'source-link-audit.json',source_links)
    files=[row(p,PAYLOAD) for p in sorted(PAYLOAD.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
    # The inherited packet's own MANIFEST is part of the payload too.
    files.append(row(supplied/'MANIFEST.json',PAYLOAD))
    files.sort(key=lambda r:r['path'])
    write(PAYLOAD/'MANIFEST.json',dict(scope='Exact file inventory except this manifest; integrity is not scientific validity',files=files))
    run('final-source-manifest',PAYLOAD,['verify_manifest.py'])
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in sorted(PAYLOAD.rglob('*')):
            if path.is_file():
                z.write(path,PREFIX+'/'+path.relative_to(PAYLOAD).as_posix())
    archive_hash=sha(ARCHIVE)
    (DELIVERY/(ARCHIVE.name+'.sha256')).write_text(archive_hash+'  '+ARCHIVE.name+'\n',encoding='ascii')
    EXTRACTION.mkdir()
    with zipfile.ZipFile(ARCHIVE) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):
            raise RuntimeError('duplicate archive entry')
        for name in names:
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts or ':' in name or '\\' in name or p.parts[0]!=PREFIX:
                raise RuntimeError('unsafe archive member: '+name)
        if z.testzip() is not None:
            raise RuntimeError('archive CRC failure')
        z.extractall(EXTRACTION)
    fresh=EXTRACTION/PREFIX
    exported_manifest=json.loads(run('exported-manifest-before',fresh,['verify_manifest.py']))
    run('exported-science',fresh,['check_ym2.py','--numeric','--output',str(DELIVERY/'FINAL_REPLAY_RESULTS.json')])
    scalar_export=run('exported-scalar-reference',fresh,['check_scalar_reference.py'])
    if scalar_export.strip()!=EXPECTED_SCALAR:
        raise RuntimeError('exported scalar reference mismatch')
    exported_packet=json.loads(run('exported-input-packet',fresh,['supplied/CODEX_YM2/verify_packet.py']))
    run('exported-manifest-after',fresh,['verify_manifest.py'])
    if (fresh/'RESULTS.json').read_bytes()!=(DELIVERY/'FINAL_REPLAY_RESULTS.json').read_bytes():
        raise RuntimeError('fresh scientific results differ from packaged final-source results')
    if sha(ARCHIVE)!=archive_hash:
        raise RuntimeError('archive changed after hashing')
    if (fresh/'MANIFEST.json').read_bytes()!=(PAYLOAD/'MANIFEST.json').read_bytes():
        raise RuntimeError('exported manifest differs from source')
    final_links=link_audit(fresh)
    write(DELIVERY/'exported-link-audit.json',final_links)
    source_results=json.loads((fresh/'RESULTS.json').read_text(encoding='utf-8'))
    receipt=dict(status='PASS',completed_utc=now(),
        archive=dict(path=str(ARCHIVE),sha256=archive_hash,bytes=ARCHIVE.stat().st_size),
        exported_root=str(fresh),manifest_sha256=sha(fresh/'MANIFEST.json'),
        frozen_contract_sha256=sha(fresh/'FREEZE.json'),
        payload_files_excluding_manifest=exported_manifest['files'],
        runtime=dict(executable=sys.executable,version=sys.version,platform=platform.platform()),
        checks=dict(archive_crc='PASS',safe_unique_paths='PASS',source_manifest='PASS',
                    exported_manifest_before='PASS',exported_science='PASS',
                    exported_scalar_reference_exact_output='PASS',
                    source_export_scientific_bytes_equal=True,exported_manifest_after='PASS',
                    zip_hash_unchanged_after_replay=True,input_packet=exported_packet,
                    authored_local_links=final_links['status']),
        numeric_diagnostics=dict(
            max_step_difference=max(r['absolute_step_difference'] for r in source_results['numeric_illustration']['rows']),
            max_energy_drift=max(r[k]['max_absolute_energy_drift'] for r in source_results['numeric_illustration']['rows'] for k in ('coarse','fine')),
            absolute_tolerance=1e-10),
        runs=RUNS,
        evidence_boundary='Fresh exported-byte execution and integrity, not a formal proof or quantum spectral bound. YM1 checker not run.',
        export_history='Initial helper link audit mistook inline Taylor coefficient notation [t^n](...) for a Markdown link. Fixed helper to skip inline code; resumed successful frozen source runs. No frozen payload code, proof, or result was changed.',
        replay_results=row(DELIVERY/'FINAL_REPLAY_RESULTS.json',DELIVERY),
        export_script=row(Path(__file__),DELIVERY))
    write(DELIVERY/'FINAL_EXPORT_EVIDENCE.json',receipt)
    report=f'''# YM2 final export evidence

**PASS.** Final source was frozen, checked, archived, freshly extracted, and
replayed from the actual exported bytes. Final replay outputs remain outside
the already-hashed payload.

- Archive: [{ARCHIVE.name}]({ARCHIVE.name})
- SHA-256: `{archive_hash}`
- Archive bytes: {ARCHIVE.stat().st_size}
- Payload files: {exported_manifest['files']} plus its manifest
- Exact source checks, independent scalar reference and optional small numerical
  illustration: PASS from source and final extraction.
- Packet transfer inventory: PASS, 23 files; accepted YM1 checker NOT_RUN.
- Exported manifest before and after replay: PASS.
- Full fresh result bytes equal packaged final-source result bytes: PASS.
- Archive SHA-256 unchanged after replay: PASS.
- New authored Markdown local links: PASS.

[Machine-readable evidence with commands, outputs and exit codes](FINAL_EXPORT_EVIDENCE.json)
and [fresh full result rows](FINAL_REPLAY_RESULTS.json) are external to the ZIP.
Python: {platform.python_version()}; standard library only.

The mathematical result is exact failure of R3 and its one K refinement in the
declared interacting classical sector. A hash binds bytes; replay checks the
supplied executable calculations. Neither is a quantum mass-gap proof or a
general soundness proof of the checker.
'''
    (DELIVERY/'FINAL_EXPORT_EVIDENCE.md').write_text(report,encoding='utf-8')
    print(json.dumps(dict(status='PASS',archive=str(ARCHIVE),sha256=archive_hash,
                          payload_files=exported_manifest['files']+1,evidence=str(DELIVERY/'FINAL_EXPORT_EVIDENCE.json')),indent=2))


if __name__=='__main__':
    main()
