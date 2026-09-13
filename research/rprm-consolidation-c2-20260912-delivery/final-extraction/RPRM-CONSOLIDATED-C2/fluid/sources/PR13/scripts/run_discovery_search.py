#!/usr/bin/env python
"""Discovery search: same-summary / different-future under matched continuation.

RETROSPECTIVE / discovery-only. Selected examples are marked; not confirmatory.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rprm_transport.baselines import dual_domain_candidate_gate  # noqa: E402
from rprm_transport.passive_dual_domain import PassiveColumnSpec, run_episode  # noqa: E402
from rprm_transport.receiver import ReceiverQuestion, evaluate_threshold  # noqa: E402


def outlet_at(times, outlet, t_star: float) -> float:
    # nearest sample at or before t_star
    pairs = [(t, c) for t, c in zip(times, outlet) if t <= t_star]
    return pairs[-1][1] if pairs else float("nan")


def main() -> int:
    out_dir = ROOT / "results" / "discovery"
    out_dir.mkdir(parents=True, exist_ok=True)
    q = ReceiverQuestion(threshold_c=0.02, t0=250.0, t1=350.0)
    t_check = 100.0

    # Vary exchange rate and immobile porosity while keeping inlet pulse identical
    grid = []
    for zeta in [1e-4, 1e-3, 5e-3, 2e-2, 1.0]:
        for phi_im in [0.02, 0.10, 0.20]:
            spec = PassiveColumnSpec(
                name="discover",
                control="dual_slow",
                zetaim=zeta,
                porosity_immobile=phi_im,
                total_time=400.0,
                pulse_duration=40.0,
                obs_x=40.0,
                ncol=81,
                delr=1.0,
            )
            # unique folder via name override using replace on control string path:
            # encode params in name
            spec = replace(spec, name=f"z{zeta:g}_p{phi_im:g}")
            print(f"run {spec.name}", flush=True)
            ep = run_episode(spec, silent=True)
            grid.append(
                {
                    "id": spec.name,
                    "zetaim": zeta,
                    "porosity_immobile": phi_im,
                    "c_check": outlet_at(ep.times, ep.outlet_c, t_check),
                    "exceeds": evaluate_threshold(ep.times, ep.outlet_c, q),
                    "final_c": ep.outlet_c[-1],
                    "immobile_mass_at_end": ep.immobile_mass[-1],
                    "outlet_hash": ep.outlet_c[-1],  # placeholder scalar marker
                }
            )

    # Find pairs with similar checkpoint concentration but different exceedance
    pairs = []
    for i, a in enumerate(grid):
        for b in grid[i + 1 :]:
            if a["exceeds"] == b["exceeds"]:
                continue
            denom = max(abs(a["c_check"]), abs(b["c_check"]), 1e-12)
            rel = abs(a["c_check"] - b["c_check"]) / denom
            if rel <= 0.15:
                pairs.append(
                    {
                        "a": a["id"],
                        "b": b["id"],
                        "c_check_a": a["c_check"],
                        "c_check_b": b["c_check"],
                        "rel_diff_check": rel,
                        "exceeds_a": a["exceeds"],
                        "exceeds_b": b["exceeds"],
                        "selected_discovery_example": True,
                    }
                )

    pairs.sort(key=lambda p: p["rel_diff_check"])
    selected = pairs[:5]

    # Candidate gate demo on best pair if any
    gate = None
    if selected:
        best = selected[0]
        cand = {best["a"]: best["exceeds_a"], best["b"]: best["exceeds_b"]}
        gate = dual_domain_candidate_gate(cand).answer.to_dict()

    summary = {
        "stage": "discovery_RETROSPECTIVE",
        "receiver": asdict(q),
        "checkpoint_t": t_check,
        "n_grid": len(grid),
        "n_ambiguous_pairs": len(pairs),
        "selected_pairs": selected,
        "candidate_gate_on_best": gate,
        "note": (
            "Examples were searched and selected after seeing outcomes. "
            "Do not treat as confirmatory cohort."
        ),
        "grid": grid,
    }
    path = out_dir / "same_summary_different_future.json"
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in summary if k != "grid"}, indent=2))
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
