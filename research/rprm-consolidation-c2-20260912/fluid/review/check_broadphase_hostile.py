"""Replay one fixed broadphase hostile case against the exact PR13 source bytes.

Run: python -I -B check_broadphase_hostile.py --output NEW_RESULT_PATH.json
Requires an existing NumPy installation. Does not import the benchmark runner,
change source files, or permit overwriting a result. This is not a suite replay.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import types


PIN = "7e3a6603c8f3c036f9f59f519b069cfc02b7825f"
EXPECTED = {
    "sim": "575102185dbf9e1291fb9835c1c107421f9720cd949c0ae87ce4e8f14efdf982",
    "certificate": "6aef43252a81f2cc62cd05bf4692e4254b1fc3d43f7b575ed5047caec4927d8a",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error(f"Refusing to overwrite: {output}")

    source_root = Path(__file__).resolve().parent.parent / "sources" / "PR13" / "broadphase_lab"
    if output == source_root or source_root in output.parents:
        parser.error("Output must not be inside the pinned source directory")
    if not output.parent.is_dir():
        parser.error(f"Output parent does not exist: {output.parent}")

    # Load exact, hash-checked bytes into memory copies. The certificate's ordinary
    # `from sim import ...` resolves to this pinned in-memory sim, never another sim.
    # No source-side __pycache__ or runner import is involved.
    modules = {}
    source_identity = {}
    for name, expected_hash in EXPECTED.items():
        path = source_root / f"{name}.py"
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if digest != expected_hash:
            raise RuntimeError(f"Pinned source SHA-256 mismatch: {path}")
        module = types.ModuleType(name)
        module.__file__ = str(path)
        sys.modules[name] = module
        exec(compile(content, str(path), "exec"), module.__dict__)
        modules[name] = module
        source_identity[name] = {
            "path_relative_to_fluid": path.relative_to(source_root.parent.parent.parent).as_posix(),
            "sha256": digest,
        }

    sim, cert = modules["sim"], modules["certificate"]
    inputs = {
        "W": 20.0, "H": 20.0, "gravity": sim.GRAVITY, "dt": sim.DT,
        "friction": 0.0, "restitution": 0.0, "walls": [],
        "positions": [[5.0, 5.0], [5.1, 5.0], [5.0, 6.028]],
        "velocities": [[0.0, 0.0]] * 3, "radii": [0.5] * 3,
        "density": 1.0, "initial_angular_velocities": [0.0] * 3,
        "island": [0, 1, 2], "ca_sleep_threshold": 1.6,
    }
    world = sim.World(W=20, H=20, friction=0.0, restitution=0.0, walls=())
    world.add_disks(inputs["positions"], inputs["velocities"], inputs["radii"])
    island = set(inputs["island"])

    def gaps():
        return {
            f"{a},{b}": float(sim.np.linalg.norm(world.pos[b] - world.pos[a]) -
                              (world.radius[a] + world.radius[b]))
            for a, b in ((0, 1), (0, 2), (1, 2))
        }

    before = sim.contact_set(world)
    before_gaps = gaps()
    verdicts = {
        "addition_guard": bool(cert._addition_guard(world, island, sim.DT, sim.GRAVITY, 0.0)),
        "persistence_guard": bool(cert._persistence_forcebalance(world, island, before,
                                                                  sim.DT, sim.GRAVITY, 0.0)),
        "P": bool(cert.method_P(world, island, before)),
        "ca_sleeping_tau_1_6": bool(cert.method_ca_sleeping(world, island, before, 1.6)),
    }
    world.step()
    after = sim.contact_set(world)
    expected_observation = (
        before == frozenset({(0, 1), (0, 2)}) and
        after == frozenset({(0, 1)}) and all(verdicts.values())
    )
    result = {
        "study": "one fixed hostile case; not a benchmark campaign",
        "source_commit": PIN,
        "sources": source_identity,
        "reproducer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "runtime": {
            "python": sys.version, "python_executable": sys.executable,
            "platform": platform.platform(), "numpy": sim.np.__version__,
        },
        "inputs": inputs,
        "before_pairs": sorted(before), "before_gaps": before_gaps,
        "verdicts": verdicts,
        "after_pairs": sorted(after), "after_gaps": gaps(),
        "after_positions": world.pos.tolist(), "after_velocities": world.vel.tolist(),
        "receiver_changed": before != after,
        "both_methods_falsely_certify": bool(verdicts["P"] and verdicts["ca_sleeping_tau_1_6"]
                                             and before != after),
        "expected_hostile_observation_reproduced": expected_observation,
        "scope": "Refutes universal soundness on accepted World inputs with deep overlap; does not alter the saved randomized suite's zero observed FP.",
    }
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": str(output), "expected_observation_reproduced": expected_observation}))
    return 0 if expected_observation else 1


if __name__ == "__main__":
    raise SystemExit(main())
