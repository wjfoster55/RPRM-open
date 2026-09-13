"""Verify source bindings and current authored-document links, not proof soundness."""
from hashlib import sha256
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
bindings = [
    ('evidence/hooks.json', 'source_sha256', 'work/check_hooks.py'),
    ('evidence/hooks.json', 'height_kernel_sha256', 'work/height_kernel.py'),
    ('evidence/anchor-readback.json', 'source_sha256', 'work/check_anchor_readback.py'),
    ('evidence/anchor-readback.json', 'input_sha256', 'evidence/hooks.json'),
    ('evidence/two-halves.json', 'source_sha256', 'work/check_two_halves.py'),
    ('evidence/two-halves.json', 'input_sha256', 'evidence/hooks.json'),
]
for evidence, field, source in bindings:
    record = json.loads((root/evidence).read_text(encoding='utf-8'))
    assert record[field] == sha256((root/source).read_bytes()).hexdigest(), (evidence, field)
capture = json.loads((root/'SOURCE_CAPTURE.json').read_text(encoding='utf-8'))
for row in capture['files']:
    assert sha256((root/row['snapshot']).read_bytes()).hexdigest() == row['sha256']
links = []
for name in ('README.md', 'TWO_HALVES.md', 'BSD_REBRIEF.md'):
    for target in re.findall(r'\]\(([^)]+)\)', (root/name).read_text(encoding='utf-8')):
        if target.startswith(('http:', 'https:', '#')):
            continue
        assert (root/target.split('#')[0]).is_file(), (name, target)
        links.append((name, target))
scripts = list((root/'work').glob('*.py'))
for source in scripts:
    compile(source.read_text(encoding='utf-8'), str(source), 'exec')
print(json.dumps({'status': 'SOURCE_BINDINGS_AND_AUTHORED_LINKS_VERIFIED',
                  'evidence_bindings': len(bindings), 'captured_dependencies': len(capture['files']),
                  'authored_document_links': len(links), 'source_syntax_checks': len(scripts),
                  'claim_ceiling': 'Byte binding, link existence and syntax only; not mathematical proof'}, indent=2))
