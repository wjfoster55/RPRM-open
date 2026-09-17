"""Load the frozen F2 Python modules without mutating them."""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
F3_ROOT = HERE.parent
F2_ROOT = (
    F3_ROOT.parent
    / "fluid-f2-review-20260912"
    / "input"
    / "fluid_dynamic_frontier_02"
)
F2_SRC = F2_ROOT / "src"
F2_PINNED = F2_ROOT / "pinned"
ORACLE_JS = F2_SRC / "oracle.js"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bound = load("f2_bound", F2_SRC / "bound.py")
scenes = load("f2_scenes", F2_SRC / "scenes.py")
