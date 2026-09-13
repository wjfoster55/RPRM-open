"""Verify exact-evidence source hashes, local report links and Python syntax."""
from pathlib import Path
from hashlib import sha256
import json,re
root=Path(__file__).resolve().parents[1]
pairs=[('carry-center.json','check_carry_center.py'),
 ('phase-bridge.json','check_phase_bridge.py'),('p-hinge.json','check_p_hinge.py'),
 ('number-scouts.json','scout_numbers.py')]
for evidence,source in pairs:
    data=json.loads((root/'evidence'/evidence).read_text(encoding='utf-8'))
    assert data['source_sha256']==sha256((root/'work'/source).read_bytes()).hexdigest()
for p in (root/'work').glob('*.py'):
    compile(p.read_text(encoding='utf-8-sig'),str(p),'exec')
links=0;external_dependencies=[]
for p in (root/'README.md',root/'BSD_REBRIEF.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if target.startswith(('https:','http:','#')):continue
        file=(p.parent/target.split('#')[0]).resolve()
        if file.is_relative_to(root):assert file.is_file(),target
        else:external_dependencies.append(target)
        links+=1
print(json.dumps({'status':'BYTE_BINDINGS_SYNTAX_AND_LOCAL_LINKS_CHECKED',
 'source_bindings':len(pairs),'local_links':links,'attributed_external_local_notes':external_dependencies,
 'claim_ceiling':'Byte, syntax and path verification, not proof of source claims'},indent=2))
