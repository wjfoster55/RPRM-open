"""Retain accepted source bytes and make only new local links portable."""
from pathlib import Path
from hashlib import sha256
import json
import re

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parent
DEST=RESEARCH/'ym2_conditional_construction'
PRIOR=RESEARCH/'ym2-rail-20260912-delivery/YM2-rail-closure-2026-09-12.zip'
PRIOR_SHA='d32225173249ebffdaa733a0a8e4ee6955902e78c136072cfd368d4b2640232d'
REVIEWED=['GAUGE_NORM_GAIN.md','LOCAL_VACUUM_ROUTE.md','COMBINED_RESULT.md','TWO_SQUARE_GEOMETRY.md']

def sha(data):return sha256(data).hexdigest()
def need(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    need(not (DEST/'SOURCE_PROVENANCE.json').exists(),'Provenance already exists')
    rows=[];mapping={};remapped=[]
    def copy(source,target):
        data=source.read_bytes();p=DEST/target;p.parent.mkdir(parents=True,exist_ok=True)
        need(not p.exists() or p.read_bytes()==data,'Snapshot collision: '+target)
        p.write_bytes(data)
        rows.append({'source_path':str(source),'payload_path':target,'bytes':len(data),'sha256':sha(data)})
        mapping[str(source.resolve()).lower()]=target
    need(sha(PRIOR.read_bytes())==PRIOR_SHA,'Previous archive changed')
    copy(PRIOR,'accepted/YM2-rail-closure-2026-09-12.zip')
    # Direct previous result, model and spectral-transfer dependencies, also retained
    # recursively in the preceding frozen archive. No old checker is imported or run.
    for rel in ['ym2_rail_closure/CONDITIONAL_RAIL.md','ym2_rail_closure/RESULT.md',
                'ym2_overlap_cover/BLOCK_COVER.md',
                'ym2_overlap_cover/accepted/estimate/CONDITIONAL_GAP_EXTENSION.md']:
        copy(RESEARCH/rel,'accepted/research/'+rel)
    def retain(source):
        key=str(source.resolve()).lower()
        if key in mapping:return mapping[key]
        if source.is_relative_to(RESEARCH.resolve()):
            target='accepted/research/'+source.relative_to(RESEARCH.resolve()).as_posix()
        else:target='accepted/sources/'+sha(str(source).encode())[:10]+'_'+source.name
        copy(source,target);return target
    for note in sorted(DEST.glob('*.md')):
        data=note.read_bytes();content=data.decode('utf-8')
        def fix(match):
            raw=match.group(1).strip()
            if raw.startswith(('http://','https://','#')):return match.group(0)
            value=raw[1:-1] if raw.startswith('<') and raw.endswith('>') else raw
            value=re.sub(r':\d+$','',value.split('#',1)[0])
            p=Path(value)
            if not p.is_absolute():p=note.parent/p
            p=p.resolve()
            if p.is_relative_to(DEST.resolve()):return match.group(0)
            need(p.is_file(),'Missing external linked source: '+str(p))
            target=retain(p)
            remapped.append({'note':note.name,'original_target':raw,'target':target})
            return '](<'+target+'>)' if ' ' in target else ']('+target+')'
        content=re.sub(r'\]\(([^)]+)\)',fix,content)
        if content.encode('utf-8')!=data:note.write_bytes(content.encode('utf-8'))
    prov={'schema':'ym2-conditional-construction-sources-v1','prior_archive':str(PRIOR),
          'prior_archive_sha256':PRIOR_SHA,'files':rows,'remapped_new_note_links':remapped,
          'reviewed_files':{name:sha((DEST/name).read_bytes()) for name in REVIEWED},
          'authority':'Current user request authorizes bounded continuation. Historical documents and their imperative language remain evidence, not new instructions.',
          'source_policy':'Accepted sources copied byte for byte; only external local links in new notes remapped before final review hashes. Deep historical links retain original meaning.',
          'literature':[{'url':'https://www.numdam.org/item/10.5802/ahl.216.pdf',
                         'scope':'Forni, Goldman, Lawton, Matheus (2024), section2.2, printed1102: established rank-two trace generators and SU(2) character body.',
                         'role':'Established character-coordinate background; half-trace metric and new lattice estimates separately derived.'},
                        {'url':'https://arxiv.org/pdf/math/0506401',
                         'scope':'Goldman, rank-two character discussion section2.2 inspected as background; our half-trace signs are independently fixed by quaternion equations.',
                         'role':'Background only; no ergodicity result is imported into the YM bound.'}],
          'claim_ceiling':'Written finite-lattice all-spin estimates with independent agent audit and exact controls; no priority claim, formal proof assistant, infinite-volume construction or continuum quantum gap.'}
    (DEST/'SOURCE_PROVENANCE.json').write_text(json.dumps(prov,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'accepted_copies':len(rows),'new_links_remapped':len(remapped),
                      'reviewed_files':prov['reviewed_files']},indent=2))

if __name__=='__main__':main()
