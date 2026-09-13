"""Local artifact/link audit; does not rerun mathematical experiments."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

root = Path('C:/github/RPRM-open')
pack = root / 'research/liar-teacher-formalization-2026-09-12'
out = pack / 'VERIFICATION.json'
files = sorted(p for p in pack.iterdir() if p.is_file() and p != out)
files += [root / p for p in (
    'recovered-concepts/README.md', 'recovered-concepts/NEXT-PAPER-BACKLOG.md',
    'README.md', 'AGENTS.md')]
links = []
for file in files:
    if file.suffix != '.md':
        continue
    for target in re.findall(r'\[[^\]]*\]\(([^)\n]+)\)', file.read_text(encoding='utf-8-sig')):
        target = unquote(target.strip('<>'))
        if target.startswith(('https:', 'http:', '#', 'mailto:')):
            continue
        path_part = re.sub(r':\d+$', '', target.split('#', 1)[0])
        if re.match(r'^/[A-Za-z]:/', path_part):
            path_part = path_part[1:]
        dest = Path(path_part)
        if not dest.is_absolute():
            dest = file.parent / dest
        ok = dest.exists() or dest.resolve() == out.resolve()
        links.append({'source': str(file.relative_to(root)), 'target': target, 'exists': ok})
bad = [item for item in links if not item['exists']]
assert not bad, bad

panel = json.loads((pack / 'PANEL-RESULTS.json').read_text(encoding='utf-8-sig'))
sat = json.loads((pack / 'SAT-RESULTS.json').read_text(encoding='utf-8-sig'))
code_hash = hashlib.sha256((pack / 'sat_pilot.py').read_bytes()).hexdigest()
assert code_hash == sat['implementation_sha256'], 'SAT code/receipt mismatch'
assert panel['status'] == sat['status'] == 'PASS'
assert panel['assertions'] == 13665
assert len(sat['finite_cases']) == 24 and not sat['failures']
assert all(c['panel']['status'] == c['whole_system_gaussian']['status'] == c['oracle_status']
           for c in sat['finite_cases'])
data = {
    'schema': 'rprm-local-research-verification/v1',
    'verified_at_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'PASS',
    'files': [{'path': str(p.relative_to(root)), 'bytes': p.stat().st_size,
               'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
    'local_links_checked': len(links), 'local_links': links,
    'panel': {'status': panel['status'], 'assertions': panel['assertions'],
              'execution': 'Final expanded fixture suite executed successfully; stdout saved as PANEL-RESULTS.json'},
    'sat': {'status': sat['status'], 'implementation_binding': 'MATCH',
            'finite_cases': len(sat['finite_cases']), 'guards': sat['guards'],
            'non_affine_controls': len(sat['non_affine_controls']),
            'algebra_only_cases': len(sat['scaling_cases']),
            'complete_local_oracle_assignments': sum(c['oracle_work']['complete_assignments'] for c in sat['finite_cases']),
            'local_boundary_memberships': sum(c['boundary_memberships_checked'] for c in sat['finite_cases'])},
    'review': [
        'Separate review of written P1-P9 and finite panel implementation found no incorrect assertions; scope gaps motivated the final expanded fixtures.',
        'Separate P10/P11 review accepted projection, join and exact non-affine extension; corrected zero-variable complexity notation and k>=1 recognition premise.',
        'SAT code review strengthened explicit positive recognition and actual joined relation validation; corrected counter and payload labels; final run passed.',
        'Root independently inspected SAT recognizer, private elimination and raw oracle; documented dense-ID cost scope.'
    ],
    'limits': [
        'Hashes bind the current local bytes, not their truth or general verifier soundness.',
        'Finite tests and written proofs are separate evidence grades; no Lean proof was run.',
        'The imported chat snapshot contains eight recent turns, with older history explicitly excluded.',
        'Larger SAT cases compare two algebraic implementations without independent exhaustive truth tables.',
        'This audit did not rerun the BSD, Yang-Mills, SAT02 or historical recovery campaigns.',
        'Files persisted locally with knowledge-base and agent-entry links; no Memory Fabric database ingestion or publication.'
    ]
}
out.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: data[k] for k in ('status', 'local_links_checked', 'panel', 'sat')}, indent=2))
