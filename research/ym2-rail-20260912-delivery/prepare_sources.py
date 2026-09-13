"""Retain source bytes, remap new-note links, and bind the reviewed theorem."""
from pathlib import Path
from hashlib import sha256
import json
import re
import zipfile

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parent
DEST=RESEARCH/'ym2_rail_closure'
PRIOR=RESEARCH/'ym2-vacuum-handoff-20260912-delivery/YM2-vacuum-handoff-2026-09-12.zip'
PRIOR_SHA='4d217545e3e1f90d26e668a2dbdfde70a2a9876951a9e460f1c9505b21e4fa32'
REVIEWED_SHA='30d65be6af0424da4544fea5037c6a2476278850c2131180a85f274979cda7e2'

def digest(data):return sha256(data).hexdigest()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    require(not (DEST/'SOURCE_PROVENANCE.json').exists(),'Provenance already exists')
    rows=[]
    def save(data,target,**source):
        p=DEST/target;p.parent.mkdir(parents=True,exist_ok=True)
        require(not p.exists() or p.read_bytes()==data,'Source collision: '+target)
        p.write_bytes(data)
        rows.append({'payload_path':target,'bytes':len(data),'sha256':digest(data),**source})
    require(digest(PRIOR.read_bytes())==PRIOR_SHA,'Prior archive changed')
    save(PRIOR.read_bytes(),'accepted/YM2-vacuum-handoff-2026-09-12.zip',
         source_path=str(PRIOR),kind='frozen_prior_archive')
    mappings={}
    with zipfile.ZipFile(PRIOR) as z:
        wanted=['RESULT.md','VACUUM_ATLAS.md','TRIAL_REFERENCE.md','COMPENSATOR.md',
                'INDEPENDENT_REVIEW.md','accepted/overlap/BLOCK_COVER.md',
                'accepted/overlap/accepted/estimate/CONDITIONAL_GAP_EXTENSION.md',
                'accepted/overlap/accepted/estimate/SOURCE_NORM_REFINEMENT.md']
        for rel in wanted:
            member='YM2-vacuum-handoff/'+rel
            data=z.read(member)
            target='accepted/handoff/'+rel
            save(data,target,source_archive=str(PRIOR),source_member=member,kind='accepted_YM_note')
            current=RESEARCH/'ym2_vacuum_handoff'/rel
            if current.exists():
                require(current.read_bytes()==data,'Accepted current source differs: '+rel)
                mappings[str(current.resolve()).lower()]=target
    def retain(source):
        key=str(source.resolve()).lower()
        if key in mappings:return mappings[key]
        raw=source.read_bytes()
        target='accepted/sources/'+digest(str(source).encode())[:10]+'_'+source.name
        save(raw,target,source_path=str(source),kind='current_historical_source_bytes')
        mappings[key]=target
        return target
    # Include two mathematically used source documents named in the recovery table.
    qr=Path('C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research')
    for name in ['RPRM_KERNEL_STILL_POINT_2026-08-12.md',
                 'RPRM_BRIDGE_FAMILIES_FULL_REREAD_UNDERSTANDING_PACKET_2026-08-12.md']:
        retain(qr/name)
    remapped=[]
    for note in sorted(DEST.glob('*.md')):
        raw=note.read_bytes();content=raw.decode('utf-8')
        # Only actual Markdown links; source tables in inline code keep exact original locators.
        def fix(m):
            target=m.group(1).strip()
            if target.startswith(('http://','https://','#')):return m.group(0)
            if target.startswith('<') and target.endswith('>'):target=target[1:-1]
            target=target.split('#',1)[0]
            target=re.sub(r':\d+$','',target)
            source=Path(target)
            if not source.is_absolute():source=note.parent/source
            source=source.resolve()
            if source.is_relative_to(DEST.resolve()):return m.group(0)
            require(source.is_file(),'Missing linked source: '+str(source))
            saved=retain(source)
            remapped.append({'note':note.name,'original_target':m.group(1),'target':saved})
            return ']('+saved+')'
        # No new note uses Markdown-looking expressions in fenced code; all rewritten paths
        # must resolve to real files outside this packet before retention is allowed.
        updated=re.sub(r'\]\(([^)]+)\)',fix,content)
        if updated.encode('utf-8')!=raw:note.write_bytes(updated.encode('utf-8'))
    require(digest((DEST/'CONDITIONAL_RAIL.md').read_bytes())==REVIEWED_SHA,
            'Reviewed theorem changed during link preparation')
    require(REVIEWED_SHA in (DEST/'INDEPENDENT_REVIEW.md').read_text(encoding='utf-8').lower(),
            'Independent source binding missing')
    prov={'schema':'ym2-rail-sources-v1','prior_archive':str(PRIOR),'prior_archive_sha256':PRIOR_SHA,
          'reviewed_theorem_sha256':REVIEWED_SHA,'files':rows,'remapped_new_note_links':remapped,
          'authority':'Current user request controls scope. Historical imperative wording is evidence, not instruction.',
          'snapshot_policy':'Source files copied byte for byte; only new top-level link targets remapped. Historical deep links are retained without a portability claim.',
          'retrieval_scope':'See RETRIEVAL_SCOPE.md and the three retained Memory Fabric responses; bounded search with explicit omissions.',
          'literature':[{'url':'https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/GibbsFieldEst/Besag1972.pdf',
                         'read_scope':'Section2 equations4-10, conditional restrictions and ordered joint-density reconstruction.',
                         'role':'Established probability-theory ingredient; no novelty claim.'},
                        {'url':'https://academic.oup.com/biomet/article-abstract/51/3-4/481/291953',
                         'read_scope':'Publisher metadata only; original full article inaccessible this session.',
                         'role':'Brook1964 historical attribution, access limit explicit.'}]}
    (DEST/'SOURCE_PROVENANCE.json').write_text(json.dumps(prov,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'source_copies':len(rows),'new_links_remapped':len(remapped),
                      'reviewed_theorem_matches':True},indent=2))

if __name__=='__main__':main()
