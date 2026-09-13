"""Read-only source capture for this YM continuation; exact selected bytes."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import zipfile

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
OUT = RESEARCH / 'ym2_connected_vacuum'
PRIOR = RESEARCH / 'ym2-signed-20260912-delivery' / 'YM2-signed-differences-2026-09-12.zip'
EXPECTED = '914b1950ed762cd86f1b14ea6cd7816e99f8860a612ba3cea44773544bb3218f'
PREFIX = 'YM2-signed-differences/'


def digest(data):
    return sha256(data).hexdigest()


def main():
    if digest(PRIOR.read_bytes()) != EXPECTED:
        raise RuntimeError('Accepted prior ZIP hash changed')
    records = []
    with zipfile.ZipFile(PRIOR) as archive:
        selected = []
        for name in archive.namelist():
            if name.startswith(PREFIX+'accepted_sources/ym2_global_phase_joint/') and not name.endswith('/'):
                relative = name.removeprefix(PREFIX)
                selected.append((name, relative))
        for name in ('VACUUM_COMPARISON.md', 'NEXT_CONNECTED_OBLIGATION.md',
                     'DIFFERENCE_PROJECTION.md', 'STACKING_AND_SCALING.md',
                     'SIGNED_SEMANTICS.md', 'SOURCE_AUDIT.md',
                     'RESULTS_VACUUM_COMPARISON.json'):
            selected.append((PREFIX+name, 'accepted_sources/ym2_signed_differences/'+name))
        for name, relative in selected:
            data = archive.read(name)
            target = OUT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != data:
                raise RuntimeError('Refuse to overwrite a differing source copy: '+relative)
            target.write_bytes(data)
            records.append({'payload_path': relative, 'archive_member': name,
                            'sha256': digest(data), 'bytes': len(data),
                            'role': 'accepted_YM_source_not_rerun'})
    # Exact current-task files only; no recursive other-lane collection.
    wanted = {
        'liar-teacher-formalization-2026-09-12/THEORY-DRAFT.md': '9ab0e5b7dff70fd2ee5f8ef1c5b99ea82eb3015a82395cc7aa75202ac5581585',
        'liar-teacher-formalization-2026-09-12/SAT-PILOT.md': 'bed42c3901e0c24fba3b7556cc67d2fd1c2b41fc3c70fedb699deca51bc64f64',
        'liar-teacher-formalization-2026-09-12/RELATED-RESEARCH.md': 'fc8b002d65a06f4fc86889e26826393fa35e6a551651b8d49f03d487866544ae',
        'bsd-e5-test-01/ARITHMETIC_PROOF.md': '35f23551c397dc1a3a401c28243072b98eeb7a9733b4e5429b9f4ea592c5af49',
        'bsd-e5-test-01/INTERVAL_DERIVATION.md': '65e242dce048490f9ef0a0aabcb3e53c0f84bac548921760876755bcb6600206',
        'bsd-e5-completion/GENERATOR_PROOF.md': 'dd7a761f063eee413e10266f24e58d254df3416b8c57a40d8e8bed5e4b4b337a',
        'bsd-e5-completion/BSD_FACTORS.md': '9f570c5bf87c6b0b0b38f7fd4fd3d29f3495d2328917e64c11f613419456ed0b',
        'bsd-e5-completion/BSD_SHA_THEOREMS.md': '1cc196f2f5fce9992ba669c8185c2f769cfe47d7c2a28e4bd3889da6ad9516be',
        'bsd-e5-completion/work/coordinate_check.py': '642d21d6044ca54f45ba7ba53e2b2134fa9a13258f21a076411d824e2b7470ad',
    }
    mismatches = []
    for name, expected in wanted.items():
        source = RESEARCH / name
        data = source.read_bytes()
        actual = digest(data)
        rel = 'running_task_snapshots/'+name
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != data:
            raise RuntimeError('Refuse to overwrite an earlier snapshot: '+rel)
        target.write_bytes(data)
        records.append({'payload_path': rel, 'source': str(source),
                        'sha256': actual, 'bytes': len(data),
                        'captured_utc': datetime.now(timezone.utc).isoformat(),
                        'audit_sha256': expected, 'matches_audit_snapshot': actual == expected,
                        'role': 'running_task_snapshot_read_only_not_adjudicated'})
        if actual != expected:
            mismatches.append(name)
    result = {'schema': 'ym2-connected-source-provenance-v1',
              'prior_archive': str(PRIOR), 'prior_archive_sha256': EXPECTED,
              'capture_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Accepted YM bytes plus attributed running BSD/PNP source snapshots; no source commands executed',
              'files': records,
              'running_files_changed_since_audit': mismatches,
              'source_link_boundary': 'Unedited source copies retain their original historical link context; current top-level notes use bundled paths.'}
    (OUT/'SOURCE_PROVENANCE.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'files': len(records), 'changed_since_audit': mismatches}, indent=2))


if __name__ == '__main__':
    main()
