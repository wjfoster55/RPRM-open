"""Audit local delivery links and byte bindings without rerunning experiments."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

repo = Path('C:/github/RPRM-open')
pack = repo / 'research/expansion-compression-2026-09-12'
output = pack/'VERIFICATION.json'
files = sorted(p for p in pack.iterdir() if p.is_file() and p != output)
files += [repo/'recovered-concepts/README.md', repo/'recovered-concepts/NEXT-PAPER-BACKLOG.md']
links = []
for file in files:
    if file.suffix != '.md':
        continue
    markdown = file.read_text(encoding='utf-8-sig')
    markdown = re.sub(r'```[\s\S]*?```', '', markdown)
    markdown = re.sub(r'`[^`\n]*`', '', markdown)
    for match in re.finditer(r'\[[^\]]*\]\(([^)\n]+)\)', markdown):
        target = unquote(match[1].strip('<>'))
        if target.startswith(('https:', 'http:', '#', 'mailto:')):
            continue
        raw = re.sub(r':\d+$', '', target.split('#', 1)[0])
        if re.match(r'^/[A-Za-z]:/', raw):
            raw = raw[1:]
        dest = Path(raw)
        if not dest.is_absolute():
            dest = file.parent / dest
        exists = dest.exists() or dest.resolve() == output.resolve()
        links.append({'file': str(file.relative_to(repo)), 'target': target, 'exists': exists})
assert all(item['exists'] for item in links), [item for item in links if not item['exists']]
result = json.loads((pack/'RESULTS.json').read_text(encoding='utf-8'))
for name, field in [('verify_connections.py', 'implementation_sha256'), ('TEST-SPEC.md', 'specification_sha256')]:
    assert hashlib.sha256((pack/name).read_bytes()).hexdigest() == result[field]
assert result['status'] == 'PASS' and result['assertions'] == 34936
assert [s['classes'] for s in result['operator_stages']] == [5, 10, 30, 60, 30, 5]
record = {
    'status': 'PASS', 'verified_at_utc': datetime.now(timezone.utc).isoformat(),
    'files': [{'path': str(file.relative_to(repo)), 'bytes': file.stat().st_size,
               'sha256': hashlib.sha256(file.read_bytes()).hexdigest()} for file in files],
    'local_links_checked': len(links), 'local_links': links,
    'test_status': result['status'], 'assertions': result['assertions'],
    'script_and_frozen_spec_bindings': 'MATCH',
    'execution': 'python -I -B research/expansion-compression-2026-09-12/verify_connections.py; exit 0',
    'memory_snapshot': {
        'source': 'configured read-only current_snapshot tool',
        'root': '944da1fef7bb71be819df694599f9908b878cd50e515bd02f973c50fa69adb2e',
        'blobs': 115, 'occurrences': 1932,
        'retrieval': 'Current local reports and exact corpus locators; no compile_context/cache write or database ingestion'
    },
    'review_scope': 'Source inspection and new finite executable checks; historical campaigns not rerun; no new independent external mathematical review claimed.',
    'delivery_audit_correction': 'Initial link parser falsely treated inline mathematical code E[2](Q) as a file link; repaired by excluding Markdown code spans/fences. No mathematical check failed.',
    'live_status_refresh': {'as_of_utc': '2026-09-12 18:54:18',
        'BSD_general_continuation': 'active', 'YM_connected_continuation': 'completed 18:53:44 UTC'},
    'limits': [
        'Hashes bind local bytes, not mathematical truth.',
        'Existing reports retain their written-proof and recorded-finite-test grades.',
        'New finite checks do not establish general compression, controller optimality or a Millennium-problem result.',
        'The knowledge-base/backlog files are live navigation; these hashes supersede their earlier navigation-file bindings only.',
        'No historical result manifest or paper was rewritten; no task messages, database writes, publication or neighboring-campaign edits.'
    ]
}
output.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'status': record['status'], 'files': len(files), 'links': len(links),
                  'test_assertions': record['assertions']}, indent=2))
