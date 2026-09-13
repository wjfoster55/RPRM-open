"""One constructed hostile control for Cursor F2 Layer B. Input stays frozen.

Run from anywhere: python -I -B check_layer_b_support_injection.py
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "input" / "fluid_dynamic_frontier_02"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bound = load("f2_bound", SOURCE / "src" / "bound.py")
scenes = load("f2_scenes", SOURCE / "src" / "scenes.py")

# Original 64x48 geometry and receiver; only two ledge wall cells added.
# Both initial water masses are exactly one and all velocities normalize to zero.
geo = scenes.make_container(64, 48, 10, extra_walls=[(29, 36), (30, 36)])
mass = scenes.empty_mass(64, 48)
for x, y in [(30, 34), (31, 34)]:
    mass[y * 64 + x] = 1.0
scene = scenes.spec_of(
    geo, mass, "audit_two_cell_support_injection", "hostile_support",
    "Two cells fall once, then same-row diagonal injection supplies temporary support.",
)
layers = bound.evaluate_layers(
    scene["walls"], scene["mass"], scene["monitor"], scene["W"], scene["H"],
    scene["thresh"], dx=scene["dx"], crest_y=scene["crest_y"],
)
verdict, reason = bound.official_static_verdict(layers)
spec = scenes.scene_to_oracle_spec(scene, "full")
spec["snapshotSteps"] = [0, 1, 2, 3]
spec_path = HERE / "layer_b_support_injection_spec.json"
oracle_path = HERE / "layer_b_support_injection_oracle.json"
spec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
subprocess.run(["node", str(SOURCE / "src" / "oracle.js"), str(spec_path), str(oracle_path)], check=True)
oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
trace = []
for snapshot in oracle["snapshots"]:
    trace.append({
        "t": snapshot["s"],
        "water": [{"x": i % scene["W"], "y": i // scene["W"], "mass": m}
                  for i, m in enumerate(snapshot["m"]) if m > 0],
    })
result = {
    "source_root": str(SOURCE),
    "scene_id": scene["id"],
    "contract": {"W": 64, "H": 48, "steps": 300, "theta": 0.5,
                 "divider_x": 32, "crest_y": 36, "initial_water": [[30, 34], [31, 34]],
                 "extra_walls": [[29, 36], [30, 36]], "sand": False, "new_inflow": False,
                 "normalization": "Pinned normalizeForModel(B); frame starts at zero."},
    "static_verdict": verdict,
    "static_reason": reason,
    "layers": layers,
    "oracle": {key: oracle[key] for key in ["Qdyn", "firstBreach", "maxMonitored", "totalMass", "stepsRun"]},
    "trace": trace,
    "false_no": verdict == "CERTIFIED_NO" and oracle["Qdyn"] == 1,
    "interpretation": "The stack lemma is false for the stated ledge geometry contract: a diagonally arriving cell can support the next cell without a filled column to the wall.",
}
result_path = HERE / "layer_b_support_injection_result.json"
result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
assert result["false_no"], "Constructed Layer B false-NO control did not reproduce."
