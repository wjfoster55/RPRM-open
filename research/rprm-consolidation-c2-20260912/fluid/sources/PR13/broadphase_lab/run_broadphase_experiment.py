"""RPRM sufficiency-certificate transfer test in 2D rigid-body broadphase.

Single-command reproduction:
    /workspace/.venv/bin/python broadphase_lab/run_broadphase_experiment.py

Question under test (the honest crux):  does the RPRM certificate P
(conservative-advancement addition guard  AND  a force-balance persistence
certificate) add coverage OVER the sophisticated incumbent that mature engines
already ship (conservative advancement + island sleeping), at ZERO false positives?
Or does the incumbent already capture the win?

For every ISLAND at every STEP over >=1000 randomized scenes we record the method
verdicts and the TRUTH (did the contact set incident to the island change next
step?), then report confusion matrices, the FP rate (must be ~0), the certification
rate at 0 FP, and the P-vs-incumbent head-to-head.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sim import World, contact_set, CONTACT_BAND, GRAVITY, DT
import certificate as C
import scenes as S

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")
STORE = "/cursor/stores/self/artifacts"
os.makedirs(ART, exist_ok=True)
try:
    os.makedirs(STORE, exist_ok=True)
except OSError:
    STORE = None

STEPS_PER_SCENE = 25
A_BOUND = GRAVITY          # gravity-aware acceleration bound for the certificates
SLACK = 0.0               # P uses the derived bound with no tuning fudge


def eval_scene(scene_idx, family, world):
    """Roll a scene forward, recording one record per island per step."""
    records = []
    for step in range(STEPS_PER_SCENE):
        cset0 = contact_set(world)
        islands = C.compute_islands(world)

        # per-island inputs at state t
        island_info = []
        for isl in islands:
            inc0 = C.incident_pairs(cset0, isl)
            speed_max = max((float(np.hypot(*world.vel[i])) for i in isl), default=0.0)
            add_ok = C._addition_guard(world, isl, DT, A_BOUND, SLACK)
            pers_ok = C._persistence_forcebalance(world, isl, cset0, DT, A_BOUND, SLACK)
            island_info.append(dict(
                bodies=sorted(isl), inc0=inc0, speed_max=speed_max,
                add_ok=add_ok, pers_ok=pers_ok, has_contacts=len(inc0) > 0,
                n_contacts=len(inc0), n_bodies=len(isl),
            ))

        # advance TRUTH by one real step
        world.step()
        cset1 = contact_set(world)

        for info in island_info:
            isl = set(info["bodies"])
            inc1 = C.incident_pairs(cset1, isl)
            changed = (info["inc0"] != inc1)
            records.append(dict(
                scene=scene_idx, family=family, step=step,
                bodies=info["bodies"],
                changed=bool(changed),
                speed_max=info["speed_max"],
                add_ok=bool(info["add_ok"]),
                pers_ok=bool(info["pers_ok"]),
                has_contacts=bool(info["has_contacts"]),
                n_contacts=info["n_contacts"], n_bodies=info["n_bodies"],
            ))
    return records


# ---- method verdict functions over a record ----
def v_naive(r, tau):
    return r["speed_max"] < tau


def v_pure_ca(r):
    return r["add_ok"] and (not r["has_contacts"])


def v_ca_sleep(r, tau):
    if not r["add_ok"]:
        return False
    if not r["has_contacts"]:
        return True
    return r["speed_max"] < tau


def v_P(r):
    return r["add_ok"] and r["pers_ok"]


def confusion(records, verdict):
    tp = fp = fn = tn = 0
    for r in records:
        cert = verdict(r)
        nochange = not r["changed"]
        if cert and nochange:
            tp += 1
        elif cert and not nochange:
            fp += 1
        elif not cert and nochange:
            fn += 1
        else:
            tn += 1
    n = len(records)
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, n=n,
                cert_rate=(tp + fp) / n, fp_rate=fp / n,
                recall=tp / (tp + fn) if (tp + fn) else 0.0)


def best_tau_zero_fp(records, make_verdict, taus):
    """Largest tau with FP==0 (max coverage at zero false positives)."""
    best = (0.0, confusion(records, lambda r: False))
    for tau in taus:
        cm = confusion(records, lambda r: make_verdict(r, tau))
        if cm["fp"] == 0 and cm["cert_rate"] >= best[1]["cert_rate"]:
            best = (tau, cm)
    return best


def main():
    n_per_family = int(sys.argv[1]) if len(sys.argv) > 1 else 160
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    print(f"generating {n_per_family} scenes/family x {len(S.FAMILIES)} families ...")
    scene_list = S.generate(n_per_family, seed=seed)
    print(f"  {len(scene_list)} scenes; rolling {STEPS_PER_SCENE} steps each")

    records = []
    for idx, (family, world) in enumerate(scene_list):
        records.extend(eval_scene(idx, family, world))
        if (idx + 1) % 200 == 0:
            print(f"  ...{idx+1}/{len(scene_list)} scenes  ({len(records)} island-steps)")
    print(f"total island-step decisions: {len(records)}")

    n_nochange = sum(1 for r in records if not r["changed"])
    print(f"island-steps with NO contact-set change (reuse would be exact): "
          f"{n_nochange}/{len(records)} ({100*n_nochange/len(records):.1f}%)")

    # thresholds to sweep for velocity-based methods
    taus = np.linspace(0.0, 12.0, 241)

    tau_naive, cm_naive = best_tau_zero_fp(records, v_naive, taus)
    tau_cas, cm_cas = best_tau_zero_fp(records, lambda r, t: v_ca_sleep(r, t), taus)
    cm_pure = confusion(records, v_pure_ca)
    cm_P = confusion(records, v_P)

    # also record naive/ca_sleeping FP behaviour across all tau for the curve
    curve_naive = [(t, confusion(records, lambda r: v_naive(r, t))) for t in taus]
    curve_cas = [(t, confusion(records, lambda r: v_ca_sleep(r, t))) for t in taus]

    results = dict(
        n_records=len(records), n_nochange=n_nochange,
        tau_naive=tau_naive, tau_ca_sleeping=tau_cas,
        naive=cm_naive, pure_ca=cm_pure, ca_sleeping=cm_cas, P=cm_P,
    )

    print("\n================ CONFUSION MATRICES (per island-step) ================")
    hdr = f"{'method':<22}{'cert%':>8}{'FP':>6}{'FP%':>8}{'recall%':>9}{'TP':>7}{'FP ':>6}{'FN':>7}{'TN':>7}"
    print(hdr)
    def line(name, cm):
        print(f"{name:<22}{100*cm['cert_rate']:>8.2f}{cm['fp']:>6}{100*cm['fp_rate']:>8.3f}"
              f"{100*cm['recall']:>9.2f}{cm['tp']:>7}{cm['fp']:>6}{cm['fn']:>7}{cm['tn']:>7}")
    line(f"naive (tau={tau_naive:.2f})", cm_naive)
    line("pure CA", cm_pure)
    line(f"CA+sleeping (tau={tau_cas:.2f})", cm_cas)
    line("P (RPRM cert)", cm_P)

    # ---- per-family coverage breakdown (at 0 FP settings) ----
    fams = sorted(set(r["family"] for r in records))
    per_family = {}
    for fam in fams:
        rs = [r for r in records if r["family"] == fam]
        per_family[fam] = dict(
            n=len(rs),
            nochange=sum(1 for r in rs if not r["changed"]) / len(rs),
            naive=confusion(rs, lambda r: v_naive(r, tau_naive)),
            pure_ca=confusion(rs, v_pure_ca),
            ca_sleeping=confusion(rs, lambda r: v_ca_sleep(r, tau_cas)),
            P=confusion(rs, v_P),
        )
    results["per_family"] = per_family

    print("\n---- certification rate by family (cert% at 0-FP settings) ----")
    print(f"{'family':<16}{'nochg%':>8}{'naive':>8}{'pureCA':>8}{'CA+slp':>8}{'P':>8}")
    for fam in fams:
        pf = per_family[fam]
        print(f"{fam:<16}{100*pf['nochange']:>8.1f}{100*pf['naive']['cert_rate']:>8.1f}"
              f"{100*pf['pure_ca']['cert_rate']:>8.1f}{100*pf['ca_sleeping']['cert_rate']:>8.1f}"
              f"{100*pf['P']['cert_rate']:>8.1f}")

    # ---- head to head: island-steps P certifies that the incumbent does NOT ----
    p_only = [r for r in records if v_P(r) and not v_ca_sleep(r, tau_cas)]
    p_only_correct = [r for r in p_only if not r["changed"]]
    cas_only = [r for r in records if v_ca_sleep(r, tau_cas) and not v_P(r)]
    print("\n---- P vs sophisticated incumbent (CA+sleeping) head-to-head ----")
    print(f"island-steps P certifies but incumbent does NOT: {len(p_only)} "
          f"(all correct/no-change: {len(p_only_correct)}, i.e. FP among them: "
          f"{len(p_only)-len(p_only_correct)})")
    print(f"island-steps incumbent certifies but P does NOT: {len(cas_only)}")
    delta = cm_P["cert_rate"] - cm_cas["cert_rate"]
    ratio = (cm_P["cert_rate"] / cm_cas["cert_rate"]) if cm_cas["cert_rate"] > 0 else float("inf")
    print(f"certification rate: P={100*cm_P['cert_rate']:.2f}%  incumbent={100*cm_cas['cert_rate']:.2f}%  "
          f"delta=+{100*delta:.2f}pp  ratio={ratio:.2f}x")
    ratio_naive = (cm_P["cert_rate"] / cm_naive["cert_rate"]) if cm_naive["cert_rate"] > 0 else float("inf")
    print(f"(for context) P vs naive quiescence: {100*cm_P['cert_rate']:.2f}% vs "
          f"{100*cm_naive['cert_rate']:.2f}%  ratio={ratio_naive:.2f}x")

    # artifact-ROBUST part of the win: P-only correct certifications on islands that
    # are genuinely MOVING (speed above any sane velocity-sleep threshold). Velocity
    # sleeping can NEVER certify these at 0 FP, regardless of the band definition.
    MOVING = 0.5
    p_only_moving = [r for r in p_only_correct if r["speed_max"] > MOVING]
    p_only_resting = [r for r in p_only_correct if r["speed_max"] <= MOVING]
    print(f"  of the {len(p_only_correct)} P-only wins: {len(p_only_moving)} are "
          f"MOVING (speed>{MOVING}, unreachable by velocity sleeping) and "
          f"{len(p_only_resting)} are near-resting (sound-vs-band)")

    # sensitivity: incumbent coverage if a small missed-contact FP budget is allowed
    def cov_at_fp_budget(curve, budget):
        best = 0.0
        for _, cm in curve:
            if cm["fp_rate"] <= budget:
                best = max(best, cm["cert_rate"])
        return best
    cas_at_0p1 = cov_at_fp_budget(curve_cas, 0.001)
    cas_at_0p5 = cov_at_fp_budget(curve_cas, 0.005)
    print(f"  sensitivity: incumbent (CA+sleeping) coverage if FP<=0.1% : "
          f"{100*cas_at_0p1:.1f}%   if FP<=0.5% : {100*cas_at_0p5:.1f}%   (P: "
          f"{100*cm_P['cert_rate']:.1f}% at FP=0)")

    results["head_to_head"] = dict(
        p_only=len(p_only), p_only_fp=len(p_only) - len(p_only_correct),
        cas_only=len(cas_only), delta_pp=100 * delta, ratio=ratio,
        ratio_vs_naive=ratio_naive,
        p_only_moving=len(p_only_moving), p_only_resting=len(p_only_resting),
        incumbent_cov_at_fp_0p1pct=cas_at_0p1, incumbent_cov_at_fp_0p5pct=cas_at_0p5,
    )
    # dominant families in P-only wins
    from collections import Counter
    p_only_fams = Counter(r["family"] for r in p_only_correct)
    results["p_only_families"] = dict(p_only_fams)
    print(f"P-only correct certifications by family: {dict(p_only_fams)}")

    # ---- broadphase work saved (manifold recomputations skipped) ----
    def work_saved(verdict):
        total_contacts = sum(max(r["n_contacts"], 0) for r in records)
        total_bodies = sum(r["n_bodies"] for r in records)
        saved_contacts = sum(r["n_contacts"] for r in records if verdict(r))
        saved_bodies = sum(r["n_bodies"] for r in records if verdict(r))
        return saved_bodies / total_bodies, saved_contacts / max(total_contacts, 1)
    ws_naive = work_saved(lambda r: v_naive(r, tau_naive))
    ws_cas = work_saved(lambda r: v_ca_sleep(r, tau_cas))
    ws_P = work_saved(v_P)
    results["work_saved"] = dict(
        naive=dict(bodies=ws_naive[0], contacts=ws_naive[1]),
        ca_sleeping=dict(bodies=ws_cas[0], contacts=ws_cas[1]),
        P=dict(bodies=ws_P[0], contacts=ws_P[1]),
    )
    print("\n---- broadphase work saved (fraction of body-steps / contact-manifolds skipped) ----")
    print(f"naive:       bodies {100*ws_naive[0]:.1f}%   contacts {100*ws_naive[1]:.1f}%")
    print(f"CA+sleeping: bodies {100*ws_cas[0]:.1f}%   contacts {100*ws_cas[1]:.1f}%")
    print(f"P:           bodies {100*ws_P[0]:.1f}%   contacts {100*ws_P[1]:.1f}%")

    # save raw + summary json
    with open(os.path.join(ART, "broadphase_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=float)
    print(f"\nsaved summary -> {os.path.join(ART, 'broadphase_results.json')}")

    # figures + disagreement scene
    try:
        import figures
        figures.make_all(records, results, curve_naive, curve_cas, taus,
                         tau_naive, tau_cas, ART, STORE, seed, n_per_family)
    except Exception as e:  # pragma: no cover
        print(f"[figures] skipped/failed: {e}")

    return results


if __name__ == "__main__":
    main()
