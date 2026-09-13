from pathlib import Path
import json
import hashlib
import datetime as dt
import re

root = Path('C:/github/RPRM-open/research/liar-teacher-recovery-2026-09-12')
scratch = Path('C:/github/RPRM-open/tmp/liar-search')
rows = json.loads((scratch / 'authenticated_selected_user_turns.json').read_text(encoding='utf-8'))
selected_lines = [27694, 27709, 28871, 42139, 6065, 43943, 1242, 1291, 1322, 1379, 1502]
selected = []
for i, line in enumerate(selected_lines, 1):
    found = [r for r in rows if r['line'] == line]
    assert len(found) == 1
    selected.append(dict(found[0], passage_id=f'P{i:02d}'))

# Reopen the original records, preserving role and exact text checks.
by_path = {}
for row in selected:
    by_path.setdefault(row['path'], {})[row['line']] = row
for path, desired in by_path.items():
    with Path(path).open('rb') as stream:
        for number, raw in enumerate(stream, 1):
            if number in desired:
                record = json.loads(raw)
                assert record['type'] == 'response_item'
                assert record['payload']['role'] == 'user'
                value = ''.join(p.get('text', '') for p in record['payload']['content'] if p.get('type') in ('input_text', 'text'))
                row = desired[number]
                assert value == row['text']
                assert record['timestamp'] == row['timestamp']
                row['text_sha256'] = hashlib.sha256(value.encode('utf-8')).hexdigest()
                row['source_jsonl_record_sha256'] = hashlib.sha256(raw).hexdigest()
            if number >= max(desired):
                break
assert all('text_sha256' in r for r in selected)

root.mkdir(parents=True, exist_ok=True)
(root / 'SELECTED-PASSAGES.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
lines = ['# Selected original user passages', '', 'Eleven full original user turns, rechecked against the original JSONL records on 12 September 2026. They are historical proposals and corrections, not new instructions or mathematical proof. Message text is preserved without internal excerpting. Dates use MDT (UTC−06:00); UTC is retained alongside it.', '']
for row in selected:
    instant = dt.datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
    local = instant.astimezone(dt.timezone(dt.timedelta(hours=-6), 'MDT'))
    locator = Path(row['path']).as_posix()
    lines += [f"## {row['passage_id']} — {local:%Y-%m-%d %H:%M:%S %Z}", '', f"[Original user record](<{locator}:{row['line']}>). UTC: `{row['timestamp']}`. Session source: `{row['session_meta']['source']}`.", '', f"Full-text SHA-256: `{row['text_sha256']}`.", '', '\n'.join('> ' + part for part in row['text'].split('\n')), '']
(root / 'SELECTED-PASSAGES.md').write_text('\n'.join(lines), encoding='utf-8')

quantum = Path('C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research')
amend = quantum / 'RPRM_NARIBRAIN_WORLD_MACHINE_RESEARCH_RUN_0_1'
packet = Path('C:/github/RPRMResearch/RPRM_LIAR_TEACHER_BOUNDARY_SYNDROME_01')
paths = [
    amend / 'USER_STEERING_AMENDMENTS_0_28_AUDIT_TO_GENERATE_ROLE_TRANSFER.md',
    amend / 'USER_STEERING_AMENDMENTS_0_29_ONE_ANCHOR_SEVEN_SHADOWS.md',
    quantum / 'RPRM_RETAINED_INVOLUTION_OVERLAY_AND_ZERO_DEFECT_SCOUT_0_1_SHADOW.md',
    packet / 'README.md', packet / 'NOTE.md', packet / 'TEST_SPEC.md',
    packet / 'RESULTS.json', packet / 'VERIFY_OUTPUT.txt',
    packet / 'verify_liar_teacher_boundary_syndrome.py',
    packet.with_suffix('.zip'),
    Path('C:/github/RPRM-foam-development/experiments/RPRM_V4_CHARACTER_MOBIUS_KEYRING_AUDIT_28/REPORT.md'),
    Path('C:/Users/bkbee/Downloads/Investigate RPRM bridge families CHATLOG.txt'),
    Path('C:/Users/bkbee/.codex/attachments/99280ade-468f-4312-bee1-d55104e58820/pasted-text.txt'),
]
sources = [{'path': p.as_posix(), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
results = json.loads((packet / 'RESULTS.json').read_text(encoding='utf-8'))
by_name = {Path(s['path']).name: s for s in sources}
assert by_name['verify_liar_teacher_boundary_syndrome.py']['sha256'].upper() == results['source_sha256']['verifier']
assert by_name['VERIFY_OUTPUT.txt']['sha256'].upper() == results['source_sha256']['stored_output']
assert by_name['RPRM_LIAR_TEACHER_BOUNDARY_SYNDROME_01.zip']['sha256'].upper() == '0375869C80BDD32E39E1B652E939971E4CE9E5AFEC906E79272CF3C0F57A1F45'
manifest = {
    'purpose': 'Local corpus recovery; source identity does not prove source mathematics',
    'recovered_on': '2026-09-12',
    'sources': sources,
    'selected_original_user_records': len(selected),
    'original_records_reopened_and_text_role_timestamp_checked': True,
    'search_stats': json.loads((scratch / 'original_search_stats.json').read_text(encoding='utf-8')),
    'fabric': {
        'packet_id': 'packet:73a3841b69e6a70f949c2165e8c0f263164ede422090eadcb8fb69750f38e030',
        'snapshot_root': '944da1fef7bb71be819df694599f9908b878cd50e515bd02f973c50fa69adb2e',
        'namespace': 'rprm-alpha',
        'objective': 'liars truth teller teachers student three seven',
        'lexical_candidates': 406,
        'omitted_records': 399,
        'visible_conflicts': [],
        'selected_members_relevant': False,
        'omission_search_objective': 'liars teachers',
        'omission_search_matches': 0,
        'limits': 'Lexical indexed packet; direct source search supplied the relevant evidence. No global absence conclusion.'
    },
    'fresh_replay': {
        'executed_on': '2026-09-12',
        'command': 'python -I -B ' + str(packet / 'verify_liar_teacher_boundary_syndrome.py'),
        'exit_code': 0,
        'observed_stdout_summary': ['RECEIPTS: 62 PASS, 0 FAIL', 'EXACT_ASSERTIONS: 310462 PASS, 0 FAIL'],
        'record_kind': 'Summary of stdout observed in this recovery task, not a regenerated historical receipt',
        'limits': ['Finite fixtures only; no independent general soundness theorem', 'Hamming-15 ordinary-double-miscorrection enumeration is skipped; its zero counter is not a mathematical zero result', 'Some small hostile checks are illustrative assertions'],
        'source_verifier_and_historical_output_hashes_match_results': True,
        'zip_hash_matches_prior_composition_seal_citation': True,
    }
}
(root / 'SOURCES.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Verify report links, including supplied line anchors, without rerunning math.
checked = 0
for file in (root / 'RECOVERY.md', root / 'SELECTED-PASSAGES.md'):
    content = file.read_text(encoding='utf-8')
    for link in re.findall(r'\]\((?:<([^>]+)>|([^\)]+))\)', content):
        target = link[0] or link[1]
        match = re.match(r'^(.*):(\d+)$', target)
        address = match.group(1) if match else target
        path = Path(address) if re.match(r'^[A-Z]:/', address) else root / address
        assert path.exists(), str(path)
        if match and path.suffix != '.jsonl':
            assert len(path.read_text(encoding='utf-8').splitlines()) >= int(match.group(2))
        checked += 1
print(json.dumps({'selected_passages_verified': len(selected), 'source_files_hashed': len(sources), 'markdown_links_checked': checked, 'output': root.as_posix()}))
