"""One-time exact-byte preservation of selected supplied dependencies."""
import hashlib, json, platform, shutil, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PACKET=ROOT.parent/'rprm-consolidation-c2-20260912-input/RPRM-CODEX-CONSOLIDATION-01'
names=['CODEX_START_HERE.md','CURRENT_STATE.md','SOURCE_INDEX.json','HANDOFF_MANIFEST.json','SOURCE_NOTES.md',
       'tasks/F1_FLUID_CLOSEOUT.md','tasks/AD1_SCOPED_CLAIM.md','tasks/YM1_PHYSICAL_BRIDGE.md',
       'accepted/C1_CLOSEOUT.md','accepted/SAT02_M1_CLOSEOUT.md','accepted/C1_CARRY_FORWARD.md',
       'accepted/C1_MATH_REVIEW.md',
       'accepted/archives/RCF01-portable-codex-c1.zip','accepted/archives/RCF01-codex-c1-final-evidence.zip',
       'accepted/archives/SAT02-portable-codex-m1.zip','accepted/archives/SAT02-codex-m1-final-evidence.zip',
       'sources/ad/PILOT_COLLECTION_V2_REVIEW.md','sources/ad/RECOVERED_CORE_INTEGRATION_HISTORICAL.md',
       'sources/bsd/LIND_REICHARDT_REVIEW005_CLOSEOUT.md','sources/fluid/PRIOR_OWNER_CARD.md',
       'sources/yang_mills/PRIOR_OWNER_CARD.md','sources/yang_mills/check_yang_mills_connections.py',
       'sources/yang_mills/YANG_MILLS_CONNECTION_CHECKS.json','source_access/FLUID_SOURCE_PLAN.json']
records=[]
for name in names:
    src=PACKET/name
    dest=ROOT/'supplied'/name
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():raise RuntimeError('refuse overwrite '+str(dest))
    shutil.copyfile(src,dest)
    data=dest.read_bytes()
    records.append({'original_path':name,'delivery_path':dest.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for name in ['AGENTS.md','README.md','AGENT_HANDBOOK.md']:
    src=ROOT.parents[1]/name;dest=ROOT/'provenance/workspace_instructions'/name
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    records.append({'original_path':str(src),'delivery_path':dest.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(ROOT/'provenance/PRESERVED_INPUTS.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
import numpy
env={'working_root':str(ROOT.parents[1]),'isolated_output':str(ROOT),'source_revision':'9b5e132ee36334311f125027c2a719563890a3c1',
     'python':sys.version,'python_executable':sys.executable,'platform':platform.platform(),'numpy':numpy.__version__,
     'node':subprocess.check_output(['node','--version'],text=True).strip(),
     'incoming_zip_sha256':hashlib.sha256((Path('C:/Users/bkbee/Downloads/RPRM-CODEX-CONSOLIDATION-01.zip')).read_bytes()).hexdigest(),
     'installations':False,'accepted_suites_replayed':False,
     'local_preflight':'No later equivalent return found in bounded research/Downloads file-name and named-task latest-turn checks. Only this consolidation and disjoint bounded reviewers are controlled here; unseen external activity is not ruled out.'}
(ROOT/'provenance/ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'copied':len(records),'numpy':numpy.__version__,'input_sha256':env['incoming_zip_sha256']}))
