"""Check recorded byte bindings, Python syntax, visual embedding and local links."""
from hashlib import sha256
from html.parser import HTMLParser
import json,re
from pathlib import Path

root=Path(__file__).resolve().parents[1]
bindings=[
 ('evidence/display-bounds.json','source_sha256','work/check_display_bounds.py'),
 ('evidence/ratio-loop.json','source_sha256','work/check_ratio_loop_initial.py'),
 ('evidence/ratio-loop-v2.json','source_sha256','work/check_ratio_loop.py'),
 ('evidence/visual-check.json','preview_sha256','evidence/sliding-preview.html')]
for evidence,field,target in bindings:
    data=json.loads((root/evidence).read_text(encoding='utf-8'))
    assert data[field]==sha256((root/target).read_bytes()).hexdigest(),(evidence,target)
for source in root.rglob('*.py'):
    compile(source.read_text(encoding='utf-8-sig'),str(source),'exec')

class FrameParser(HTMLParser):
    def __init__(self):
        super().__init__();self.documents=[]
    def handle_starttag(self,tag,attrs):
        if tag=='iframe':
            attributes=dict(attrs)
            if 'srcdoc' in attributes:self.documents.append(attributes['srcdoc'])

parser=FrameParser()
parser.feed((root/'evidence/sliding-preview.html').read_text(encoding='utf-8'))
fragment=(root/'visual/sliding-keyring.html').read_text(encoding='utf-8').strip()
assert len(parser.documents)==1 and fragment in parser.documents[0]
links=0
for name in ('README.md','BSD_REBRIEF.md'):
    for target in re.findall(r'\]\(([^)]+)\)',(root/name).read_text(encoding='utf-8')):
        if target.startswith(('https:','http:','#')):continue
        assert (root/target.split('#')[0]).is_file(),target
        links+=1
print(json.dumps({'status':'SOURCE_BINDINGS_SYNTAX_VISUAL_EMBEDDING_AND_LINKS_VERIFIED',
 'bindings':len(bindings),'authored_local_links':links,'visual_fragment_matches_preview':True,
 'claim_ceiling':'Byte, syntax, embedding and link checks; not a mathematical proof'},indent=2))
