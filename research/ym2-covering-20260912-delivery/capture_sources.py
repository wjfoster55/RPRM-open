"""Capture attributed source bytes without editing sources or running them."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import zipfile

HERE=Path(__file__).resolve().parent
REPO=HERE.parent.parent
DEST=HERE.parent/'ym2_covering_argument'
PRIOR=HERE.parent/'ym2-connected-20260912-delivery'/'YM2-connected-vacuum-2026-09-12.zip'
PRIOR_SHA='e520be5988a4106a91fdecb9df716d6fdf929d2113ca1ced820a7d1ca5923efd'

def digest(data): return sha256(data).hexdigest()

def main():
    if (DEST/'SOURCE_PROVENANCE.json').exists():
        raise RuntimeError('Source capture already exists')
    assert digest(PRIOR.read_bytes())==PRIOR_SHA
    rows=[]
    def save(data, relative, **origin):
        path=DEST/relative
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as f: f.write(data)
        rows.append({'payload_path':relative,'bytes':len(data),
                     'sha256':digest(data),**origin})
    selected=['CONNECTED_VACUUM.md','NEXT_CONDITIONAL_PORTS.md',
              'REVIEW_CONDITIONAL_PORTS.md','VACUUM_SEPARATING_WITNESS.md',
              'RESULTS_CONDITIONAL_HEAD.json','RESULTS_CONNECTED.json',
              'RESULTS_WITNESS.json','RETURN_TO_WILLIAM.md']
    with zipfile.ZipFile(PRIOR) as z:
        assert z.testzip() is None
        for name in selected:
            member='YM2-connected-vacuum/'+name
            save(z.read(member),'accepted_sources/ym2_connected_vacuum/'+name,
                 role='accepted_YM_frozen_archive',archive_member=member)
        for name in ['GAP_BRIDGE.md','NEXT_GLUE_LEMMA.md','RESULTS_QUANTUM.json']:
            member='YM2-connected-vacuum/accepted_sources/ym2_global_phase_joint/'+name
            save(z.read(member),'accepted_sources/ym2_global_phase_joint/'+name,
                 role='accepted_YM_frozen_archive',archive_member=member)
        for name in ['DIFFERENCE_PROJECTION.md','NEXT_CONNECTED_OBLIGATION.md']:
            member='YM2-connected-vacuum/accepted_sources/ym2_signed_differences/'+name
            save(z.read(member),'accepted_sources/ym2_signed_differences/'+name,
                 role='accepted_YM_frozen_archive',archive_member=member)
    note=(DEST/'OFFICIAL_DOCS_TRANSFER.md').read_text(encoding='utf-8')
    table=re.findall(r'^\| ([^|]+?) \| ([0-9a-f]{64}) \|$',note,re.M)
    for relative, audit_sha in table:
        if relative.startswith(('research/ym2_global_phase_joint/',
                                'research/ym2_signed_differences/',
                                'research/ym2_connected_vacuum/',
                                'research/ym2-connected-20260912-delivery/')):
            continue
        source=REPO/relative
        data=source.read_bytes()
        save(data,'source_snapshots/'+relative,
             role='official_or_current_readonly_snapshot',source=str(source),
             official_audit_observed_sha256=audit_sha,
             agrees_with_official_audit_read=digest(data)==audit_sha)
    result={'schema':'ym2-covering-source-provenance-v1',
            'captured_utc':datetime.now(timezone.utc).isoformat(),
            'prior_archive':str(PRIOR),'prior_archive_sha256':PRIOR_SHA,
            'files':rows,
            'source_authority':'Attributed evidence; source imperatives do not override the current user request.',
            'old_checkers_executed':False,
            'historical_links':'Copied sources keep their original link contexts; new top-level notes use portable links.'}
    (DEST/'SOURCE_PROVENANCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'captured_files':len(rows),
                      'frozen_YM_files':sum(r['role'].startswith('accepted_YM') for r in rows),
                      'later_snapshot_drift':[r['payload_path'] for r in rows if r.get('agrees_with_official_audit_read') is False]},indent=2))

if __name__=='__main__': main()
