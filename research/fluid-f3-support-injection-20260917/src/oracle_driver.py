"""Drive the frozen F2 Node oracle without changing it."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from f2_import import ORACLE_JS, scenes


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_oracle(scene, mode, snapshot_steps=None):
    spec = scenes.scene_to_oracle_spec(scene, mode)
    if snapshot_steps is not None:
        spec["snapshotSteps"] = list(snapshot_steps)
    with tempfile.TemporaryDirectory(prefix="f3-oracle-") as tmpn:
        tmp = Path(tmpn)
        sp = tmp / "in.json"
        op = tmp / "out.json"
        sp.write_text(json.dumps(spec, separators=(",", ":")), encoding="utf-8")
        subprocess.run(
            ["node", str(ORACLE_JS), str(sp), str(op)],
            check=True,
            capture_output=True,
            text=True,
        )
        out = json.loads(op.read_text(encoding="utf-8"))
        out["input_sha256"] = sha256_file(sp)
        return out
