#!/usr/bin/env python
"""Run passive dual-domain controls and write compact witnesses."""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rprm_transport.baselines import (  # noqa: E402
    current_reading_baseline,
    dual_domain_candidate_gate,
    history_mean_baseline,
)
from rprm_transport.observer import (  # noqa: E402
    assert_policy_blind_to_evaluator,
    build_evaluator_future,
    build_observer_from_outlet,
)
from rprm_transport.passive_dual_domain import PassiveColumnSpec, run_episode  # noqa: E402
from rprm_transport.receiver import ReceiverQuestion, evaluate_threshold  # noqa: E402


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    out_dir = ROOT / "results" / "passive_dual_domain"
    out_dir.mkdir(parents=True, exist_ok=True)
    q = ReceiverQuestion()
    controls = ["dual_slow", "no_immobile", "rapid_equilibration"]
    episodes = {}
    for control in controls:
        spec = PassiveColumnSpec(name="col101", control=control)  # type: ignore[arg-type]
        print(f"Running control={control} ...", flush=True)
        ep = run_episode(spec, silent=True)
        episodes[control] = {
            "control": ep.control,
            "n_obs": len(ep.times),
            "final_outlet_c": ep.outlet_c[-1] if ep.outlet_c else None,
            "peak_outlet_c": max(ep.outlet_c) if ep.outlet_c else None,
            "mass_residual_rel": ep.mass_residual_rel,
            "truth_exceeds": evaluate_threshold(ep.times, ep.outlet_c, q),
            "times_hash": _sha256_text(json.dumps(ep.times)),
            "outlet_hash": _sha256_text(json.dumps(ep.outlet_c)),
            "mobile_mass_final": ep.mobile_mass[-1] if ep.mobile_mass else None,
            "immobile_mass_final": ep.immobile_mass[-1] if ep.immobile_mass else None,
        }
        # Persist compact witness (not full arrays in git-facing summary)
        witness = {
            "spec": asdict(spec),
            "times": ep.times,
            "outlet_c": ep.outlet_c,
            "mobile_mass": ep.mobile_mass,
            "immobile_mass": ep.immobile_mass,
            "mass_residual_rel": ep.mass_residual_rel,
        }
        wpath = out_dir / f"witness_{control}.json"
        wpath.write_text(json.dumps(witness, indent=2), encoding="utf-8")

    # Same-summary / different-future illustration using dual_slow vs rapid at a checkpoint
    slow = json.loads((out_dir / "witness_dual_slow.json").read_text(encoding="utf-8"))
    t_cut = 120.0
    obs = build_observer_from_outlet(slow["times"], slow["outlet_c"], t_cutoff=t_cut)
    truth = build_evaluator_future(
        slow["times"],
        slow["outlet_c"],
        t_cutoff=t_cut,
        mobile_mass=slow["mobile_mass"],
        immobile_mass=slow["immobile_mass"],
        hidden_params={"control": "dual_slow", "zetaim": PassiveColumnSpec().zetaim},
    )
    truth.target_exceeds = evaluate_threshold(slow["times"], slow["outlet_c"], q)
    policy_in = obs.as_policy_input()
    assert_policy_blind_to_evaluator(policy_in, truth)

    b_cur = current_reading_baseline(obs, q)
    b_hist = history_mean_baseline(obs, q)
    # Toy candidates: slow-exchange vs no-immobile futures for exceedance
    cand = {
        "dual_slow": episodes["dual_slow"]["truth_exceeds"],
        "no_immobile": episodes["no_immobile"]["truth_exceeds"],
    }
    b_gate = dual_domain_candidate_gate(cand)

    summary = {
        "receiver": asdict(q),
        "episodes": episodes,
        "checkpoint_t": t_cut,
        "baselines": {
            "current_reading": b_cur.answer.to_dict(),
            "history_mean": b_hist.answer.to_dict(),
            "candidate_gate": b_gate.answer.to_dict(),
        },
        "evaluator_truth_exceeds": truth.target_exceeds,
        "hypothesis_vs_evidence": {
            "hypothesis": "Present outlet reading can hide stored tracer that changes later release.",
            "evidence_grade": "simulated_model_episode",
            "not_claimed": [
                "field observation",
                "RPRM discovered slow exchange (exchange was in the simulator)",
                "health/safety threshold",
            ],
        },
    }
    spath = out_dir / "summary.json"
    spath.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Wrote {spath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
