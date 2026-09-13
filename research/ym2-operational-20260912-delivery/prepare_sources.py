"""Snapshot read dependencies and make new top-level links portable."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,re,shutil

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'research/ym2_operational_seam'
def digest(p):return sha256(p.read_bytes()).hexdigest()
rows={}
def copy(p):
    p=p.resolve()
    try: rel=p.relative_to(ROOT)
    except ValueError:rel=Path('external')/p.parent.name/p.name
    target=SOURCE/'accepted'/rel
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(p,target)
    rows[str(p)]={'source_path':str(p),'payload_path':target.relative_to(SOURCE).as_posix(),
                  'bytes':p.stat().st_size,'sha256':digest(p)}
    return target.relative_to(SOURCE).as_posix()

extra=['research/ym2_conditional_construction/COMBINED_RESULT.md',
       'research/ym2_conditional_construction/CONSTRUCTION_REVIEW.md',
       'research/bsd-carry-key-06/COLUMN_HANDOFF.md',
       'research/bsd-carry-key-06/work/column_handoff.py',
       'research/bsd-carry-key-06/evidence/column_handoff_extended.json',
       'research/bsd-carry-key-06/work/operational_probe.py',
       'research/bsd-carry-key-06/runs/fresh_validation/evidence/operations.json',
       'research/bsd-carry-key-06/runs/fresh_validation/RUN.json',
       'research/bsd-carry-key-06/runs/fresh_validation/logs/analytic.log',
       'research/bsd-carry-key-06/runs/fresh_validation/logs/finite_audit.log',
       'research/bsd-operational-03/evidence/operational_sources.json',
       'research/bsd-operational-03/runs/return_validation/RUN.json',
       'AGENT_HANDBOOK.md','docs/operations.md']
for name in extra:copy(ROOT/name)
for name in ('translate_number.py','carrier_lexer.py','readings.json','README.md','SOURCE_MANIFEST.json'):
    copy(Path('C:/github/RPRMLexicon/operational_numbers')/name)
remaps=[]
for p in SOURCE.glob('*.md'):
    content=p.read_text(encoding='utf-8')
    def replace(m):
        raw=m.group(1)
        if raw.startswith(('https://','http://','#')):return m.group(0)
        cleaned=raw.strip('<>');part,sep,anchor=cleaned.partition('#')
        target=(p.parent/part).resolve()
        if target.is_relative_to(SOURCE):return m.group(0)
        if not target.is_file():raise RuntimeError('Missing source link '+str(p)+': '+raw)
        rel=copy(target)+(sep+anchor if sep else '')
        remaps.append({'note':p.name,'from':raw,'to':rel})
        if ' ' in rel:rel='<'+rel+'>'
        return ']('+rel+')'
    after=re.sub(r'\]\(([^)]+)\)',replace,content)
    if after!=content:p.write_text(after,encoding='utf-8')
prior=ROOT/'research/ym2-construction-20260912-delivery/YM2-conditional-construction-2026-09-12.zip'
assert digest(prior)=='1f2c4017faf270367de7209ec59eb5e2c19e32fdcaa99b27405d2b624aae785d'
copy(prior)
prov={'schema':'ym2-operational-provenance-v1','snapshot_utc':datetime.now(timezone.utc).isoformat(),
      'files':sorted(rows.values(),key=lambda r:r['payload_path']),'link_remaps':remaps,
      'prior_archive':str(prior),'prior_archive_sha256':digest(prior),
      'donor_task':{'title':'Run BSD E5 test 01','thread_id':'01a096b0-a546-76b0-b680-53e3a37f0e4a',
                    'status_at_initial_read':'active','status_at_final_snapshot':'completed turn; idle',
                    'completion_turn':'01a0981d-0df1-7093-afca-85facea1c8b5','read_only':True},
      'reviewed_files':{name:digest(SOURCE/name) for name in ['CHANNEL_SOURCE.md','SPECTRAL_CHANNEL.md','COMBINED_RESULT.md','BSD_DONOR.md']},
      'ceiling':'Exact byte snapshots; no old mathematical checker executed; snapshots are evidence not task authority.'}
(SOURCE/'SOURCE_PROVENANCE.json').write_text(json.dumps(prov,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'snapshots':len(rows),'portable_remaps':len(remaps),'reviewed_files':prov['reviewed_files']},indent=2))
