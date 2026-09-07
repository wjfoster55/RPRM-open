"""Cold independent boundary-event geometry oracle and finite transition census."""
import argparse
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations
import json
import os
from uuid import uuid4
from pathlib import Path

HERE = Path(__file__).resolve().parent


def oracle(ray, cell):
    # Enumerate exact boundary events then retain those on the closed square.
    # This does not use the implementation's intersected-slab algorithm.
    a, b = ray; x, y = cell
    candidates = {F(0), F(1), F(2*x-1, 10), F(2*x+1, 10)}
    if b != a:
        candidates |= {F(2*y-1-2*a, 2*(b-a)), F(2*y+1-2*a, 2*(b-a))}
    good = [t for t in candidates if 0 <= t <= 1 and 2*x-1 <= 10*t <= 2*x+1 and 2*y-1 <= 2*(a+(b-a)*t) <= 2*y+1]
    return None if not good else (min(good), max(good))


def _run_checks(args):
    spec = importlib.util.spec_from_file_location("ray_model", HERE / "model.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    counts = {"geometry_pairs": 0, "scenes": 0, "toggles": 0, "singleton_moves": 0, "rejections": 0, "assertions": 0}
    def require(ok, reason):
        counts["assertions"] += 1
        if not ok: raise RuntimeError(reason)
    def rejects(fn):
        try: fn()
        except ValueError: counts["rejections"] += 1
        else: raise RuntimeError("hostile input admitted")
    rays = tuple((a,b) for a in range(6) for b in range(6))
    cells = tuple((x,y) for x in range(1,5) for y in range(6))
    contact = {(r,c): oracle(r,c) for r in rays for c in cells}
    for key, value in contact.items():
        require(m.intersection(*key) == value, "boundary-event geometry disagreement")
        counts["geometry_pairs"] += 1
    def full(opaque):
        rows = []
        for r in rays:
            hits = sorted(((c,contact[r,c]) for c in opaque if contact[r,c] is not None), key=lambda v:(v[1][0],v[1][1],v[0]))
            rows.append({"ray": list(r), "hits": [{"cell":list(c), "entry":[v[0].numerator,v[0].denominator], "exit":[v[1].numerator,v[1].denominator]} for c,v in hits]})
        return {"schema":"finite-grid-rays/v1", "opaque":[list(c) for c in sorted(opaque)], "rows":rows}
    scenes = [s for n in range(4) for s in combinations(cells,n)]
    expected = {s:full(s) for s in scenes}
    patch_probes = baseline_probes = ingress_probes = 0
    tie_witness = None
    for opaque in scenes:
        before = m.compile_scene(opaque)
        require(before == expected[opaque], "full scene disagreement")
        counts["scenes"] += 1
        for row in before["rows"]:
            hits = row["hits"]
            nearest = [] if not hits else [h["cell"] for h in hits if F(*h["entry"]) == min(F(*j["entry"]) for j in hits)]
            require(m.first_hit(row) == {"disposition":"NONE" if not nearest else "ONE" if len(nearest)==1 else "MANY", "cells":nearest}, "nearest tie was lost")
            if len(nearest)>1 and tie_witness is None: tie_witness = {"opaque":[list(c) for c in opaque],"ray":row["ray"],"cells":nearest}
        for c in cells:
            if len(opaque) == 3 and c not in opaque: continue
            target = tuple(sorted(set(opaque) ^ {c}))
            got = m.update(before,"TOGGLE",c)
            require(got["snapshot"] == expected[target], "incremental toggle differs from oracle")
            want_dirty = [list(r) for r in rays if contact[r,c] is not None]
            require(got["receipt"]["dirty_rays"] == want_dirty, "dirty set disagreement")
            require(before == expected[opaque], "update mutated prior state")
            counts["toggles"] += 1
            patch_probes += got["receipt"]["patch_cache_probes"]
            baseline_probes += got["receipt"]["full_baseline_cache_probes"]
            ingress_probes += got["receipt"]["ingress_cache_probes"]
    for a in cells:
        for b in cells:
            if a==b: continue
            before = expected[(a,)]
            forward = m.update(before,"MOVE",a,b)["snapshot"]
            require(forward == expected[(b,)], "singleton move disagreement")
            require(m.update(forward,"MOVE",b,a)["snapshot"] == before, "move inverse disagreement")
            counts["singleton_moves"] += 1
    # Every non-singleton geometry rejects MOVE at this declared operation seam.
    for opaque in scenes:
        if len(opaque) != 1:
            rejects(lambda s=opaque: m.update(expected[s],"MOVE",cells[0],cells[1]))
    require(tie_witness is not None, "tie fixture missing")
    good = m.compile_scene(((1,0),(2,0)))
    forged = deepcopy(good); forged["rows"][0]["hits"] = []
    rejects(lambda: m.validate_snapshot(forged))
    rejects(lambda: m.update(forged,"TOGGLE",(4,5)))  # false untouched row
    for bad in (True, 1.0, "1", None):
        rejects(lambda b=bad: m.compile_scene(((b,0),)))
        mutant = deepcopy(good); mutant["rows"][0]["ray"][0] = bad
        rejects(lambda s=mutant: m.validate_snapshot(s))
    for bad in ([(0,0)],[(1,0)]*2,[(1,0),(2,0),(3,0),(4,0)]): rejects(lambda b=bad: m.compile_scene(b))
    rejects(lambda:m.update(good,"TOGGLE",(4,5),claimed_dirty=[]))
    rejects(lambda:m.update(good,"TOGGLE",(4,5),claimed_dirty=[list(r) for r in rays]))
    rejects(lambda:m.load_snapshot('{"schema":"x","schema":"x"}'))
    rejects(lambda:m.load_snapshot('{"schema":NaN}'))
    rejects(lambda:m.load_snapshot(" "*131073))
    require(m.load_snapshot(json.dumps(good)) == good,"clean JSON round trip")
    left = m.compile_scene(((1,0),(2,0))); right = m.compile_scene(((1,0),(3,0)))
    require(m.first_hit(left["rows"][0]) == m.first_hit(right["rows"][0]),"future control initial receiver")
    l2=m.update(left,"TOGGLE",(1,0))["snapshot"]; r2=m.update(right,"TOGGLE",(1,0))["snapshot"]
    require(m.first_hit(l2["rows"][0]) != m.first_hit(r2["rows"][0]),"visible-only cache falsely future sufficient")
    result={"status":"PASS","evidence":"finite exhaustive census for the declared fixed grid", "counts":counts,
        "bounds":{"grid":[6,6],"rays":36,"admitted_cells":24,"max_occluders":3,"move_scope":"singleton only"},
        "logical_toggle_costs":{"patch_probes":patch_probes,"full_baseline_probes":baseline_probes,"ingress_probes":ingress_probes,"claim":"No wall-time or total-cost advantage established; ingress is extra."},
        "tie_witness":tie_witness,"source_hashes":{p.relative_to(HERE.parents[1]).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted([HERE/name for name in ("README.md","model.py","example.py","check.py")])}}
    payload=json.dumps(result,indent=2)+"\n"
    _publish(args.output, result)
    print(payload)


def _publish(path, result):
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional absolute JSON receipt path")
    args = parser.parse_args()
    if args.output is not None:
        if not args.output.is_absolute():
            parser.error("--output requires an absolute path")
        args.output = args.output.resolve()
        source_files = {(HERE / name).resolve() for name in ("README.md", "model.py", "example.py", "check.py")}
        if args.output in source_files:
            parser.error("--output cannot overwrite this pack's source files")
    _publish(args.output, {"status": "PENDING"})
    try:
        return _run_checks(args)
    except Exception as exc:
        _publish(args.output, {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"})
        raise


if __name__ == "__main__": main()
