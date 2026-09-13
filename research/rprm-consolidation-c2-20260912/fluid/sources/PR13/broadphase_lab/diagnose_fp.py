"""Classify WHERE P's false positives come from: the shared CA addition guard
(secondary-impact / restitution hole) vs the persistence clause (P-specific)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sim import contact_set, DT, GRAVITY
import certificate as C
import scenes as S

n_per_family = int(sys.argv[1]) if len(sys.argv) > 1 else 160
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7
A_BOUND, SLACK = GRAVITY, 0.0

v_rel_tols = [float(x) for x in (sys.argv[3].split(",") if len(sys.argv) > 3 else ["0.4", "0.2", "0.1", "0.05"])]
scene_list = S.generate(n_per_family, seed=seed)

# cache per island-step the raw geometry so we can re-evaluate persistence cheaply
add_fp = 0
pers_fp = {vt: 0 for vt in v_rel_tols}
pers_fp_examples = {vt: [] for vt in v_rel_tols}
add_fp_examples = []

for idx, (family, world) in enumerate(scene_list):
    for step in range(25):
        cset0 = contact_set(world)
        islands = C.compute_islands(world)
        info = []
        for isl in islands:
            inc0 = C.incident_pairs(cset0, isl)
            add_ok = C._addition_guard(world, isl, DT, A_BOUND, SLACK)
            pers = {vt: C._persistence_forcebalance(world, isl, cset0, DT, A_BOUND, SLACK, v_rel_tol=vt)
                    for vt in v_rel_tols}
            info.append((sorted(isl), inc0, add_ok, pers, len(inc0) > 0))
        world.step()
        cset1 = contact_set(world)
        for bodies, inc0, add_ok, pers, has_c in info:
            isl = set(bodies)
            inc1 = C.incident_pairs(cset1, isl)
            changed = inc0 != inc1
            if not changed:
                continue
            if add_ok and not has_c:
                add_fp += 1
                if len(add_fp_examples) < 6:
                    add_fp_examples.append((family, idx, step, bodies, sorted(inc1 - inc0), sorted(inc0 - inc1)))
            for vt in v_rel_tols:
                if add_ok and pers[vt] and has_c:
                    pers_fp[vt] += 1
                    if len(pers_fp_examples[vt]) < 5:
                        pers_fp_examples[vt].append((family, idx, step, bodies, sorted(inc1 - inc0), sorted(inc0 - inc1)))

print(f"P false positives: addition-guard (no-contact island) = {add_fp}")
for vt in v_rel_tols:
    print(f"P false positives: persistence-clause @ v_rel_tol={vt} = {pers_fp[vt]}")
print("\naddition-guard FP examples (family, scene, step, bodies, added, removed):")
for e in add_fp_examples: print("  ", e)
vt0 = v_rel_tols[-1]
print(f"\npersistence FP examples @ v_rel_tol={vt0}:")
for e in pers_fp_examples[vt0]: print("  ", e)
