"""Snapshot the exact written dependencies without executing earlier evidence."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
previous = root.parent/'bsd-pi-reading-11'
specs = [
    ('dependencies/PI_ZIP_TEST_SPEC.md', 'PI_ZIP_TEST_SPEC.md'),
    ('dependencies/EXPLICIT_IDENTITY_TARGET.md', 'EXPLICIT_IDENTITY_TARGET.md'),
    ('BSD_REBRIEF.md', 'PI11_BSD_REBRIEF.md'),
    ('agents/PI_GEOMETRY.md', 'PI11_PI_GEOMETRY.md'),
]
out = root/'dependencies'
out.mkdir(exist_ok=True)
records = []
for original, name in specs:
    source, target = previous/original, out/name
    if target.exists():
        raise FileExistsError(target)
    data = source.read_bytes()
    target.write_bytes(data)
    records.append({'original': str(source), 'snapshot': target.relative_to(root).as_posix(),
                    'sha256': sha256(data).hexdigest(), 'bytes': len(data)})
old_kernel = previous/'work/height_kernel.py'
kernel = root/'work/height_kernel.py'
assert old_kernel.read_bytes() == kernel.read_bytes()
records.append({'original': str(old_kernel), 'snapshot': 'work/height_kernel.py',
                'sha256': sha256(kernel.read_bytes()).hexdigest(),
                'bytes': kernel.stat().st_size})
target = root/'SOURCE_CAPTURE.json'
if target.exists():
    raise FileExistsError(target)
target.write_text(json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Attributed written dependencies and unchanged executable kernel. Earlier embedded relative links remain historical locators; this is not a replay of the entire prior BSD proof campaign.',
    'numerical_bounds_source': 'Fresh check_hooks.py execution, not the captured earlier rebrief',
    'files': records}, indent=2)+'\n', encoding='utf-8')
print(json.dumps(records, indent=2))
