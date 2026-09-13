import json, pathlib, re, subprocess, collections, hashlib

OUT=pathlib.Path(__file__).parent
ROOTS=[r'C:\Users\bkbee\.codex\sessions',r'C:\Users\bkbee\.codex\archived_sessions']
PAT=r'\bliars?\b|\btruth.?tellers?\b|\bteachers\b'
rx=re.compile(PAT,re.I)
proc=subprocess.run(['rg','-l','-i','-e',PAT,*ROOTS],capture_output=True,text=True,encoding='utf-8')
paths=sorted(set(proc.stdout.splitlines()))
(OUT/'original_candidate_paths.txt').write_text('\n'.join(paths),encoding='utf-8')
stats=collections.Counter(candidate_files=len(paths))
hits=[]
for pi,p in enumerate(paths):
    with open(p,encoding='utf-8') as f:
        first=f.readline()
        try: meta=json.loads(first).get('payload',{})
        except Exception: meta={}
        source=meta.get('source')
        thread_source=meta.get('thread_source')
        sub= isinstance(source,dict) or thread_source not in (None,'user')
        stats['subagent_files' if sub else 'native_files']+=1
        if sub: continue
        for lineno,line in enumerate(f,2):
            if not rx.search(line): continue
            try: obj=json.loads(line)
            except Exception: stats['parse_errors']+=1; continue
            pl=obj.get('payload',{})
            text=None
            if obj.get('type')=='response_item' and pl.get('type')=='message' and pl.get('role')=='user':
                text='\n'.join(c.get('text','') for c in pl.get('content',[]) if isinstance(c,dict))
            elif obj.get('type')=='event_msg' and pl.get('type')=='user_message':
                text=pl.get('message','')
            if not isinstance(text,str) or not rx.search(text): continue
            stats['native_user_occurrences']+=1
            ts=obj.get('timestamp','')
            if ts>='2026-09-12': stats['excluded_sep12_occurrences']+=1; continue
            if text.startswith(('# AGENTS.md instructions','<permissions instructions>','<environment_context>')):
                stats['excluded_instruction_occurrences']+=1;continue
            snippets=[]
            for m in rx.finditer(text):
                a=max(0,m.start()-160); b=min(len(text),m.end()+300)
                if snippets and a<snippets[-1][1]:
                    a0,b0=snippets.pop(); snippets.append((a0,max(b0,b)))
                else: snippets.append((a,b))
            hits.append(dict(path=p,line=lineno,timestamp=ts,type=obj.get('type'),source=source,thread_source=thread_source,text=text,snippets=[text[a:b] for a,b in snippets]))
    if pi%200==0: print('Processed',pi,flush=True)
dedup={}
for h in sorted(hits,key=lambda h:(h['timestamp'],h['path'],h['line'])):
    key=h['text']
    if key not in dedup: dedup[key]=h|{'duplicates':[]}
    else: dedup[key]['duplicates'].append({k:h[k] for k in ('path','line','timestamp','type')})
unique=list(dedup.values())
stats['retained_occurrences']=len(hits)
stats['unique_user_texts']=len(unique)
(OUT/'original_user_hits.json').write_text(json.dumps(unique,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'original_search_stats.json').write_text(json.dumps(dict(stats),indent=2),encoding='utf-8')
with (OUT/'original_user_snippets.txt').open('w',encoding='utf-8') as f:
    for i,h in enumerate(unique):
        f.write(f"[{i}] {h['timestamp']} {h['path']}:{h['line']} chars={len(h['text'])} dup={len(h['duplicates'])}\n")
        f.write('\n'.join(h['snippets'])+'\n\n')
print(json.dumps(dict(stats)),flush=True)
