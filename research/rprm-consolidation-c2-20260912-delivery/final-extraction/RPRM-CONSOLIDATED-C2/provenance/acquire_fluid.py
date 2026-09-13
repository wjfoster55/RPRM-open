"""Read-only exact-pin retrieval; no checkout or remote mutation."""
import concurrent.futures, hashlib, json, subprocess, zipfile, io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINS = {"PR12": "91d74b77bde86251468f0d3758f8e84125792677", "PR13": "7e3a6603c8f3c036f9f59f519b069cfc02b7825f"}

def acquire(item):
    label, sha = item
    url = f"https://codeload.github.com/wjfoster55/rprm-fluid-adjacency/zip/{sha}"
    endpoint = f'repos/wjfoster55/rprm-fluid-adjacency/zipball/{sha}'
    data = subprocess.run(['gh', 'api', endpoint], check=True, capture_output=True).stdout
    tree = json.loads(subprocess.run(['gh', 'api', f'repos/wjfoster55/rprm-fluid-adjacency/git/trees/{sha}?recursive=1'], check=True, capture_output=True).stdout)
    (ROOT / 'provenance' / f'{label}_GIT_TREE.json').write_text(json.dumps(tree, indent=2)+'\n', encoding='utf-8')
    blobs = {r['path']: r['sha'] for r in tree['tree'] if r['type']=='blob'}
    dest = ROOT / "fluid" / "sources" / label
    dest.mkdir(exist_ok=False)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for member in z.infolist():
            rel = Path(*member.filename.split('/')[1:])
            if member.is_dir() or not rel.parts: continue
            target = (dest / rel).resolve()
            if not target.is_relative_to(dest.resolve()): raise ValueError('unsafe ZIP')
            target.parent.mkdir(parents=True, exist_ok=True)
            raw = z.read(member)
            git_hash = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            if git_hash != blobs.get(rel.as_posix()): raise ValueError('git blob mismatch '+str(rel))
            target.write_bytes(raw)
    records = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(dest.rglob('*')) if p.is_file()]
    return {"pr": label, "git_commit": sha, "archive_url": url, "public_attempt": "HTTP 404 (repository private)", "acquired_via": 'gh api '+endpoint, "all_git_blob_ids_match":True, "archive_sha256": hashlib.sha256(data).hexdigest(), "files": records}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(acquire, PINS.items()))
    (ROOT / 'provenance' / 'FLUID_ACQUISITION.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')
    print(json.dumps([{'pr': r['pr'], 'files': len(r['files']), 'sha256':r['archive_sha256']} for r in records], indent=2))
