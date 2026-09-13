"""Verify preserved review bytes and fresh finite premises of the torsion corollary."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT/'supplied_review/BSD_E5_REVIEW'


def verify_manifest(base, name, size_key):
    manifest = json.loads((base/name).read_text(encoding='utf-8'))
    seen = set()
    for row in manifest['files']:
        path = (base/row['path']).resolve()
        if base.resolve() not in path.parents or row['path'] in seen:
            raise ValueError('Invalid manifest path')
        seen.add(row['path'])
        raw = path.read_bytes()
        assert len(raw) == row[size_key]
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
    actual = {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()}
    assert actual == seen|{name}
    return len(seen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'evidence/review_import.json')
    parser.add_argument('--review-zip', type=Path)
    args = parser.parse_args()
    review_count = verify_manifest(REVIEW,'REVIEW_INVENTORY.json','bytes')
    input_count = verify_manifest(REVIEW/'input/BSD_E5_CODEX_TEST_01_RETURN',
                                  'DELIVERY_INVENTORY.json','size')
    zip_record = {'status':'NOT_RUN','reason':'Optional original archive not supplied to this command.'}
    if args.review_zip:
        count = 0
        with ZipFile(args.review_zip) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                path = (ROOT/'supplied_review'/info.filename).resolve()
                assert (ROOT/'supplied_review').resolve() in path.parents
                assert path.read_bytes() == archive.read(info)
                count += 1
        zip_record = {'status':'ALL_MEMBERS_IDENTICAL','members':count,
                      'sha256':hashlib.sha256(args.review_zip.read_bytes()).hexdigest()}
    delta = -16*4*(-25)**3
    counts = {p: 1+sum((y*y-x*x*x+25*x)%p == 0
                       for x in range(p) for y in range(p)) for p in (3,7)}
    assert delta%3 != 0 and counts[3] == 4 and counts[7] == 8
    result = {'status':'CONFIRMED', 'utc':datetime.now(timezone.utc).isoformat(),
        'review_inventory_members':review_count,'prior_return_inventory_members':input_count,
        'original_archive':zip_record,'integrity_scope':'Bytes only; not mathematical proof.',
        'fresh_torsion_premises': {'discriminant':delta,'good_prime_counts':counts,
            'rational_two_torsion':['O',['0','0'],['5','0'],['-5','0']],
            'conclusion':'E(Q)_tors has order4 and equals E[2](Q), by the cited injection theorem.',
            'theorem_kind':'THEOREM_CITED',
            'theorem':'Milne, Elliptic Curves (2006), II Corollary5.7, printedp66/PDFp74',
            'url':'https://www.jmilne.org/math/Books/ectext6.pdf#page=74',
            'hypotheses':['Elliptic curve over Q','3 is odd','Good reduction at3'],
            'scope':'Torsion injects under this reduction; the infinite rational group does not.'},
        'prior_reuse':'The unchanged prior descent and analytic proof are reused at the same model and normalization. The supplied review has been read; its PASS strings are not new proofs.',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'review_members':review_count,
                      'original_archive':zip_record['status'],'fresh_torsion_order':4}))


if __name__ == '__main__':
    main()
