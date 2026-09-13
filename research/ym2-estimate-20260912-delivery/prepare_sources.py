"""Copy frozen accepted sources and adjust only new-note portable links."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile

HERE=Path(__file__).resolve().parent
DEST=HERE.parent/'ym2_estimate_continuation'
PRIOR=HERE.parent/'ym2-covering-20260912-delivery'/'YM2-covering-argument-2026-09-12.zip'
PRIOR_SHA='02ceeb8207b862eb5034a9c24cff9e05566ed4636972e95146b6b673d0f6f5c5'

def main():
    if (DEST/'SOURCE_PROVENANCE.json').exists(): raise RuntimeError('Already captured')
    if sha256(PRIOR.read_bytes()).hexdigest()!=PRIOR_SHA: raise RuntimeError('Prior archive drift')
    (DEST/'accepted').mkdir(exist_ok=True)
    rows=[]
    with zipfile.ZipFile(PRIOR) as z:
        for name in ['DIRECT_COVER_ATTEMPT.md','CONDITIONAL_REFINEMENT.md','NEXT_OBLIGATION.md','COVERING_RESULT.md']:
            member='YM2-covering-argument/'+name; data=z.read(member)
            with (DEST/'accepted'/name).open('xb') as f:f.write(data)
            rows.append({'payload_path':'accepted/'+name,'archive_member':member,
                         'sha256':sha256(data).hexdigest(),'bytes':len(data)})
    for path in DEST.glob('*.md'):
        before=path.read_text(encoding='utf-8')
        after=before.replace('../ym2_covering_argument/','accepted/')
        if after!=before:path.write_text(after,encoding='utf-8')
    result={'prior_archive':str(PRIOR),'prior_archive_sha256':PRIOR_SHA,'files':rows,
            'role':'Accepted written proofs copied byte-for-byte; old checkers not executed.',
            'new_note_link_changes':'Only ../ym2_covering_argument/ replaced by accepted/ for portable top-level references.'}
    (DEST/'SOURCE_PROVENANCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Captured four accepted source files; prior archive unchanged.')

if __name__=='__main__': main()
