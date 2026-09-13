#!/usr/bin/env python3
"""Frozen F2 scored execution. Candidate never receives a stored Q label.

Usage:
  python -I -B src/run_f2.py --output-dir results
  python -I -B src/run_f2.py --output-dir DIR --skip-if-present

Writes rows.jsonl, summary.json, panel_ids.json, and a markdown table.
Refuses to overwrite existing rows.jsonl unless --force (not used in replay).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from bound import evaluate_layers, official_static_verdict, volume_and_top  # noqa: E402
from scenes import build_panel, scene_to_oracle_spec  # noqa: E402

ORACLE = HERE / "oracle.js"
PINNED = ROOT / "pinned"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_oracle(scene, mode, tmp: Path):
    spec = scene_to_oracle_spec(scene, mode)
    sp = tmp / f"{scene['id']}-{mode}-in.json"
    op = tmp / f"{scene['id']}-{mode}-out.json"
    sp.write_text(json.dumps(spec, separators=(",", ":")), encoding="utf-8")
    t0 = time.perf_counter()
    r = subprocess.run(
        ["node", str(ORACLE), str(sp), str(op)],
        check=True, capture_output=True, text=True,
    )
    wall = time.perf_counter() - t0
    out = json.loads(op.read_text(encoding="utf-8"))
    out["input_sha256"] = sha256_file(sp)
    out["host_wall_s"] = wall
    if r.stderr:
        out["stderr"] = r.stderr[-500:]
    return out


def pinned_hashes():
    return {p.name: sha256_file(p) for p in sorted(PINNED.glob("*")) if p.is_file()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--skip-if-present", action="store_true")
    args = ap.parse_args()
    outdir = args.output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    rows_path = outdir / "rows.jsonl"
    if rows_path.exists():
        if args.skip_if_present:
            print(json.dumps({"status": "SKIP", "reason": "rows.jsonl exists"}))
            return
        raise SystemExit("Refusing to overwrite rows.jsonl")

    t_all = time.perf_counter()
    scenes = build_panel()
    panel_ids = [s["id"] for s in scenes]
    (outdir / "panel_ids.json").write_text(
        json.dumps({"n": len(scenes), "ids": panel_ids, "horizon": 300, "theta": 0.5}, indent=2) + "\n",
        encoding="utf-8",
    )

    pin = pinned_hashes()
    expected_pin = {
        "constants.js": "14f3a5c88f5f73ad30f1898eaa96c437ee315aa69d591fee03f409476ad35380",
        "grid.js": "3ec221be5e0ce86ea0ca676f379f63cd14be6b339594a09cb2f671889c2984a3",
        "models.js": "7f20984990f71157ca64c1279b87de27dc39688b5f1bbf684451102c1f79d17f",
        "scenarios.js": "e689ae50e2f3b1d8b1e8986c36203c74f0e27a677d8c3cb371421e65369a4f2a",
    }
    if pin != expected_pin:
        raise SystemExit(f"pinned hash mismatch: {pin}")

    rows = []
    with tempfile.TemporaryDirectory(prefix="f2-oracle-") as tmpn:
        tmp = Path(tmpn)
        for scene in scenes:
            t_prep = time.perf_counter()
            W, H = scene["W"], scene["H"]
            t_graph0 = time.perf_counter()
            layers = evaluate_layers(
                scene["walls"], scene["mass"], scene["monitor"],
                W, H, scene["thresh"], dx=scene["dx"], crest_y=scene["crest_y"],
            )
            t_graph = time.perf_counter() - t_graph0
            ab, ab_reason = official_static_verdict(layers)
            V, top = volume_and_top(scene["mass"], scene["walls"], W, H)
            t_prepare = time.perf_counter() - t_prep

            cand_fallback = None
            t_fb = 0.0
            if ab == "UNRESOLVED":
                t1 = time.perf_counter()
                cand_fallback = run_oracle(scene, "cut_exit", tmp)
                t_fb = time.perf_counter() - t1

            t2 = time.perf_counter()
            ref = run_oracle(scene, "yes_exit", tmp)
            t_ref = time.perf_counter() - t2

            Q = int(ref["Qdyn"])
            # Candidate official verdict: static AB, else the limited exact cut.
            if ab != "UNRESOLVED":
                cand_verdict = ab
                cand_via = "static_" + ab_reason
                cand_steps = 0
                cand_active = 0
                cand_stop = "static"
            else:
                if cand_fallback["Qdyn"] == 1:
                    cand_verdict = "CERTIFIED_YES"
                    cand_via = "limited_exact_yes"
                elif cand_fallback["stop"] in ("no0", "no_trapped"):
                    cand_verdict = "CERTIFIED_NO"
                    cand_via = "limited_exact_" + cand_fallback["stop"]
                else:
                    cand_verdict = "CERTIFIED_NO" if cand_fallback["Qdyn"] == 0 else "CERTIFIED_YES"
                    cand_via = "limited_exact_horizon"
                cand_steps = int(cand_fallback["stepsRun"])
                cand_active = int(cand_fallback["sumActive"])
                cand_stop = cand_fallback["stop"]

            # Map verdicts to predicted Q for scoring. UNRESOLVED should not remain
            # after fallback: cut_exit always finishes with yes, trapped, or horizon=NO.
            pred_Q = 1 if cand_verdict == "CERTIFIED_YES" else 0
            false_no = cand_verdict == "CERTIFIED_NO" and Q == 1
            false_yes = cand_verdict == "CERTIFIED_YES" and Q == 0

            a_verdict = layers["A"]["verdict"]
            b_verdict = layers["B"]["verdict"]
            fail = layers["failed_gap_adjacent"]
            fail_false_no = fail["verdict"] == "CERTIFIED_NO" and Q == 1

            # Reachability baseline: A static, else same as reference yes_exit.
            if a_verdict in ("CERTIFIED_YES", "CERTIFIED_NO"):
                reach_steps, reach_active, reach_via = 0, 0, "static_A"
            else:
                reach_steps = int(ref["stepsRun"])
                reach_active = int(ref["sumActive"])
                reach_via = "fallback_yes_exit"

            row = {
                "id": scene["id"],
                "family": scene["family"],
                "note": scene["note"],
                "W": W, "H": H, "V": V, "top": top,
                "dx": scene["dx"], "crest_y": scene["crest_y"], "crest_h": scene["crest_h"],
                "theta": scene["thresh"], "horizon": scene["steps"],
                "Q_ref": Q,
                "first_breach": ref["firstBreach"],
                "ref_stop": ref["stop"],
                "ref_steps": int(ref["stepsRun"]),
                "ref_sum_active": int(ref["sumActive"]),
                "ref_sum_moved": int(ref.get("sumMoved") or 0),
                "ref_wall_s": ref["host_wall_s"],
                "ref_max_monitored_until_stop": ref["maxMonitored"],
                "layer_A": layers["A"],
                "layer_B": layers["B"],
                "failed_gap_adjacent": fail,
                "failed_gap_adjacent_false_no": fail_false_no,
                "static_AB": ab,
                "static_AB_reason": ab_reason,
                "cand_verdict": cand_verdict,
                "cand_via": cand_via,
                "cand_pred_Q": pred_Q,
                "cand_steps": cand_steps,
                "cand_sum_active": cand_active,
                "cand_stop": cand_stop,
                "cand_fallback_wall_s": t_fb,
                "cand_graph_evals": int(cand_fallback["graphEvals"]) if cand_fallback else 0,
                "false_no": false_no,
                "false_yes": false_yes,
                "reach_steps": reach_steps,
                "reach_sum_active": reach_active,
                "reach_via": reach_via,
                "t_prepare_s": t_prepare,
                "t_graph_s": t_graph,
                "t_ref_s": t_ref,
                "bound_stats": layers["stats"],
                "input_sha_ref": ref["input_sha256"],
            }
            rows.append(row)
            print(f"{scene['id']:28} Q={Q} A={a_verdict:13} B={b_verdict:13} AB={ab:13} via={cand_via:28} refS={ref['stepsRun']:3} candS={cand_steps:3}", flush=True)

        f1_full = {}
        by_id_tmp = {r["id"]: r for r in rows}
        for fid in ("f1_tall", "f1_flat"):
            sc = next(s for s in scenes if s["id"] == fid)
            f1_full[fid] = run_oracle(sc, "full", tmp)
            by_id_tmp[fid]["f1_full_Q"] = f1_full[fid]["Qdyn"]
            by_id_tmp[fid]["f1_full_first"] = f1_full[fid]["firstBreach"]
            by_id_tmp[fid]["f1_full_peak"] = f1_full[fid]["maxMonitored"]
            by_id_tmp[fid]["f1_full_total_mass"] = f1_full[fid]["totalMass"]

    false_nos = [r["id"] for r in rows if r["false_no"]]
    false_yeses = [r["id"] for r in rows if r["false_yes"]]
    fail_fn = [r["id"] for r in rows if r["failed_gap_adjacent_false_no"]]
    if false_nos or false_yeses:
        raise SystemExit(f"SOUNDNESS FAIL false_no={false_nos} false_yes={false_yeses}")
    by_id = {r["id"]: r for r in rows}
    tall, flat = by_id["f1_tall"], by_id["f1_flat"]
    if (tall["Q_ref"], tall["first_breach"]) != (1, 11):
        raise SystemExit(f"F1 tall regression failed: {tall['Q_ref']} {tall['first_breach']}")
    if (flat["Q_ref"], flat["first_breach"]) != (0, -1):
        raise SystemExit(f"F1 flat regression failed: {flat['Q_ref']} {flat['first_breach']}")
    if (tall.get("f1_full_Q"), tall.get("f1_full_first"), tall.get("f1_full_peak")) != (1, 11, 22):
        raise SystemExit(f"F1 tall full replay failed: {tall.get('f1_full_Q')} {tall.get('f1_full_first')} {tall.get('f1_full_peak')}")
    if (flat.get("f1_full_Q"), flat.get("f1_full_first"), flat.get("f1_full_peak")) != (0, -1, 0):
        raise SystemExit(f"F1 flat full replay failed: {flat.get('f1_full_Q')} {flat.get('f1_full_first')} {flat.get('f1_full_peak')}")

    def count(pred):
        return sum(1 for r in rows if pred(r))

    n = len(rows)
    n_yes = count(lambda r: r["Q_ref"] == 1)
    n_no = n - n_yes
    static_no_A = count(lambda r: r["layer_A"]["verdict"] == "CERTIFIED_NO")
    static_yes_A = count(lambda r: r["layer_A"]["verdict"] == "CERTIFIED_YES")
    static_no_B_only = count(lambda r: r["layer_A"]["verdict"] == "UNRESOLVED" and r["layer_B"]["verdict"] == "CERTIFIED_NO")
    static_ab_decides = count(lambda r: r["static_AB"] != "UNRESOLVED")
    cut_no = count(lambda r: r["cand_via"].startswith("limited_exact_no"))
    cut_yes = count(lambda r: r["cand_via"] == "limited_exact_yes")
    horizon_no = count(lambda r: r["cand_via"] == "limited_exact_horizon")

    sum_ref_steps = sum(r["ref_steps"] for r in rows)
    sum_cand_steps = sum(r["cand_steps"] for r in rows)
    sum_reach_steps = sum(r["reach_steps"] for r in rows)
    sum_ref_active = sum(r["ref_sum_active"] for r in rows)
    sum_cand_active = sum(r["cand_sum_active"] for r in rows)

    # volume+height collisions
    buckets = {}
    for r in rows:
        key = (round(r["V"], 3), int(r["top"]), r["W"], r["H"], r["crest_h"])
        buckets.setdefault(key, []).append(r)
    vh_collide = 0
    vh_classes = 0
    for members in buckets.values():
        qs = {m["Q_ref"] for m in members}
        if len(members) > 1:
            vh_classes += 1
            if len(qs) > 1:
                vh_collide += 1

    summary = {
        "status": "PASS",
        "n_scenes": n,
        "n_yes": n_yes,
        "n_no": n_no,
        "horizon": 300,
        "theta": 0.5,
        "model": "B",
        "false_no": 0,
        "false_yes": 0,
        "failed_gap_adjacent_false_no_count": len(fail_fn),
        "failed_gap_adjacent_false_no_ids": fail_fn,
        "coverage_static_AB_decides": static_ab_decides,
        "coverage_static_AB_decides_denom": n,
        "static_NO_from_A": static_no_A,
        "static_YES_from_A": static_yes_A,
        "static_NO_from_B_only": static_no_B_only,
        "limited_exact_YES": cut_yes,
        "limited_exact_NO_trapped": cut_no,
        "limited_exact_horizon_NO": horizon_no,
        "sum_ref_steps_yes_exit": sum_ref_steps,
        "sum_cand_steps": sum_cand_steps,
        "sum_reach_steps": sum_reach_steps,
        "sum_ref_sum_active": sum_ref_active,
        "sum_cand_sum_active": sum_cand_active,
        "step_ratio_cand_over_ref": (sum_cand_steps / sum_ref_steps) if sum_ref_steps else None,
        "active_ratio_cand_over_ref": (sum_cand_active / sum_ref_active) if sum_ref_active else None,
        "volume_height_multi_member_classes": vh_classes,
        "volume_height_colliding_classes": vh_collide,
        "pinned_sha256": expected_pin,
        "elapsed_s": time.perf_counter() - t_all,
        "notes": [
            "step_ratio is executed model-B steps, not a certification-rate ratio.",
            "Reference is yes-exit rollout: early YES, else full H. That is the competent baseline.",
            "Layer A NO is the trivial no-upward/barrier reachability baseline (credited separately).",
            "Layer B extra NO is the new static content. Limited exact trapped-NO is the new dynamic content.",
            "failed_gap_adjacent is an ablation, not an official verdict.",
        ],
    }

    with rows_path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    md = []
    md.append("# F2 frozen panel rows")
    md.append("")
    md.append(f"n={n} YES={n_yes} NO={n_no} false_no=0 false_yes=0")
    md.append("")
    md.append("| id | family | V | Q | A | B | AB | via | ref_steps | cand_steps | first |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        md.append(
            f"| {r['id']} | {r['family']} | {r['V']:.0f} | {r['Q_ref']} | "
            f"{r['layer_A']['verdict']} | {r['layer_B']['verdict']} | {r['static_AB']} | "
            f"{r['cand_via']} | {r['ref_steps']} | {r['cand_steps']} | {r['first_breach']} |"
        )
    md.append("")
    (outdir / "rows.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("status", "n_scenes", "n_yes", "n_no", "failed_gap_adjacent_false_no_count", "sum_ref_steps_yes_exit", "sum_cand_steps", "elapsed_s")}, indent=2))


if __name__ == "__main__":
    main()
