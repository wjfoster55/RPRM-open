"""Verify current packet byte bindings and authored local links."""
from hashlib import sha256
import json,re
from pathlib import Path

root=Path(__file__).resolve().parents[1]
bindings=[('evidence/keyring.json','source_sha256','work/check_keyring.py'),
          ('evidence/keyring.json','input_sha256','inputs/hooks12.json'),
          ('evidence/joint-seam.json','source_sha256','work/check_joint_seam.py'),
          ('evidence/joint-seam.json','dependency_sha256','work/check_keyring.py'),
          ('evidence/visual-check.json','preview_sha256','evidence/keyring-preview.html')]
for evidence,field,target in bindings:
    data=json.loads((root/evidence).read_text(encoding='utf-8'))
    assert data[field]==sha256((root/target).read_bytes()).hexdigest(),(evidence,target)
for source in (root/'work').glob('*.py'):
    compile(source.read_text(encoding='utf-8'),str(source),'exec')
links=0
for name in ('README.md','BSD_REBRIEF.md'):
    for target in re.findall(r'\]\(([^)]+)\)',(root/name).read_text(encoding='utf-8')):
        if target.startswith(('https:','http:','#')):continue
        assert (root/target.split('#')[0]).is_file(),target
        links+=1
print(json.dumps({'status':'SOURCE_BINDINGS_SYNTAX_AND_LINKS_VERIFIED','bindings':len(bindings),
                  'authored_local_links':links,'claim_ceiling':'Byte, syntax and link checks, not mathematical proof'},indent=2))
