#!/usr/bin/env python3
"""D_fast cost comparison — the HONEST version (post trust-audit).

Drives the SAME js/ physics as the interactive demo through node (run_sim.js) so
the numbers describe the real code. Three models are compared:

  * D   — the level-aware baseline (re-floods every awake body every frame).
  * E   — E_exact: the cache/skip machinery constrained to reproduce D's global
          relabel EXACTLY (verified frame-for-frame identical to D by
          experiments/test_frame_equality.js). Because frame-identity forces a
          full row-major re-flood each relabel frame, E_exact does essentially
          the SAME flood work as D — it is a faithful mirror, NOT a speedup.
  * F   — D_fast: the certificate-gated variant that actually skips work
          (certificate-moving-skip + orphan adoption + per-body gate). This is
          where the speedup lives, and it is NOT frame-identical to D (small
          hydrostatic-equivalent deviations on fragmenting scenes).

For each scenario it measures:
  * correctness   — U-tube final |left-right| Δh and mass error %;
  * flood cost    — connected-component + cavity cells visited per step
                    (avg AND peak) — the expensive "change of representation";
  * cache work    — cavity cells touched by cache-only relaxation per step
                    (F's replacement work, so the comparison is honest);
  * skip rate     — fraction of body-processings that skipped the flood, split
                    into certificate-moving-skips vs settled-skips;
  * wall clock    — ms/step measured in node (avg AND peak).

Outputs: a printed + markdown table (artifacts/perf_table.md) and cost-over-time
plots for the dam-break (the worst case) and the U-tube, into BOTH artifacts/ and
/cursor/stores/self/artifacts/.

Run:  /workspace/.venv/bin/python perf_experiment.py
"""
import json, os, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_SIM = os.path.join(HERE, "run_sim.js")
ART = os.path.join(HERE, "..", "artifacts")
SURF_ART = "/cursor/stores/self/artifacts"
os.makedirs(ART, exist_ok=True)
try:
    os.makedirs(SURF_ART, exist_ok=True)
except OSError:
    SURF_ART = None

W, H = 100, 64
STEPS = {"basin": 2000, "utube": 6000, "dam": 2000, "stress": 2000}
SCENARIOS = ["basin", "utube", "dam", "stress"]
MODELS = ["D", "E", "F"]
MODEL_LABEL = {"D": "D (baseline)", "E": "E_exact (= D)", "F": "F = D_fast"}
# The model whose speedup we ablate against the certificate.
FAST = "F"

EMPTY, WALL, SAND, WATER = 0, 1, 2, 3
UT_SW = max(5, int(W * 0.12)); UT_XL = int(W * 0.18); UT_XR = int(W * 0.66)


def run(scenario, model, steps, overrides=None):
    tag = model + ("_ov" if overrides else "")
    out = f"/tmp/perf_{scenario}_{tag}_{steps}.json"
    frame_every = max(1, steps // 60)
    args = ["node", RUN_SIM, scenario, model, str(steps), str(W), str(H),
            str(frame_every), out]
    if overrides:
        args.append(json.dumps(overrides))
    subprocess.run(args, check=True, stderr=subprocess.DEVNULL)
    with open(out) as f:
        return json.load(f)


def frame_arrays(fr):
    t = np.frombuffer(fr["t"].encode(), dtype=np.uint8) - ord("0")
    t = t.reshape(H, W)
    m = np.array(fr["m"], dtype=np.float32).reshape(H, W)
    return t, m


def utube_dh(fr):
    t, m = frame_arrays(fr)
    wm = (t == WATER).astype(np.float32) * m
    lh = wm[:, UT_XL:UT_XL + UT_SW].sum() / UT_SW
    rh = wm[:, UT_XR:UT_XR + UT_SW].sum() / UT_SW
    return abs(float(lh) - float(rh))


def metrics(d, scenario):
    st = d["steps"]
    mass = np.array([s["m"] for s in st], dtype=np.float64)
    m0 = mass[0] if mass[0] else 1.0
    mass_err = float(abs(mass[-1] - m0) / m0 * 100)
    lc = np.array([s.get("lc", 0) for s in st], dtype=np.float64)      # flood cells
    rc = np.array([s.get("rc", 0) for s in st], dtype=np.float64)      # cache-relax cells
    dt = np.array([s.get("dt", 0) for s in st], dtype=np.float64) / 1000.0  # ms
    brf = np.array([s.get("brf", 0) for s in st], dtype=np.float64)
    bcs = np.array([s.get("bcs", 0) for s in st], dtype=np.float64)
    bss = np.array([s.get("bss", 0) for s in st], dtype=np.float64)
    bt = np.array([s.get("bt", 0) for s in st], dtype=np.float64)
    tot_bodies = bt.sum()
    return {
        "mass_err": mass_err,
        "peak_flood": float(lc.max()), "avg_flood": float(lc.mean()),
        "avg_relax": float(rc.mean()),
        "avg_ms": float(dt.mean()), "peak_ms": float(dt.max()),
        "reflood": float(brf.sum()), "cert_skip": float(bcs.sum()),
        "settled_skip": float(bss.sum()), "bodies": float(tot_bodies),
        "cert_skip_pct": float(bcs.sum() / tot_bodies * 100) if tot_bodies else 0.0,
        "settled_skip_pct": float(bss.sum() / tot_bodies * 100) if tot_bodies else 0.0,
        "skip_pct": float((bcs.sum() + bss.sum()) / tot_bodies * 100) if tot_bodies else 0.0,
        "utube_dh": utube_dh(d["frames"][-1]) if scenario == "utube" else None,
        "lc_series": lc, "rc_series": rc, "dt_series": dt,
    }


def copy_to_surface(path):
    if not SURF_ART:
        return
    import shutil
    shutil.copy(path, os.path.join(SURF_ART, os.path.basename(path)))


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    res = {}
    for sc in SCENARIOS:
        for m in MODELS:
            res[(sc, m)] = metrics(run(sc, m, STEPS[sc]), sc)
            r = res[(sc, m)]
            print(f"  {sc:7s}/{m}: peakFlood={r['peak_flood']:.0f} avgFlood={r['avg_flood']:.1f} "
                  f"avgRelax={r['avg_relax']:.1f} avgMs={r['avg_ms']:.4f} skip%={r['skip_pct']:.1f}")

    # ---------- cost-over-time plots (dam = worst case, and U-tube) ----------
    # Zoom to the ACTIVE window (the transient) where D re-floods every frame but
    # F floods once then rides the certificate — the flat tail is uninformative.
    WINDOW = {"dam": 90, "utube": 260}
    for sc in ("dam", "utube"):
        win = WINDOW[sc]
        fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
        for m in MODELS:
            r = res[(sc, m)]
            x = np.arange(len(r["lc_series"]))[:win]
            ax[0].plot(x, r["lc_series"][:win], lw=1.4, label=f"{MODEL_LABEL[m]} flood")
            if m == FAST:
                ax[0].plot(x, r["rc_series"][:win], lw=1.0, ls=":", label="F cache-relax")
            ax[1].plot(x, r["dt_series"][:win], lw=1.1, label=MODEL_LABEL[m])
        ax[0].set_title(f"{sc}: flood cells / step (first {win})")
        ax[0].set_xlabel("step"); ax[0].set_ylabel("cells visited"); ax[0].legend(fontsize=7)
        ax[1].set_title(f"{sc}: ms / step (node, first {win})")
        ax[1].set_xlabel("step"); ax[1].set_ylabel("ms"); ax[1].legend(fontsize=7)
        fig.tight_layout()
        p = os.path.join(ART, f"perf_cost_{sc}.png")
        fig.savefig(p, dpi=85); plt.close(fig)
        copy_to_surface(p)
        print(f"  wrote {p} ({os.path.getsize(p)/1024:.0f} KB)")

    # bar chart: avg + peak flood cells per scenario, D vs E vs F
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
    xs = np.arange(len(SCENARIOS)); wbar = 0.27
    for j, m in enumerate(MODELS):
        avg = [res[(sc, m)]["avg_flood"] for sc in SCENARIOS]
        peak = [res[(sc, m)]["peak_flood"] for sc in SCENARIOS]
        ax[0].bar(xs + (j - 1) * wbar, avg, wbar, label=MODEL_LABEL[m])
        ax[1].bar(xs + (j - 1) * wbar, peak, wbar, label=MODEL_LABEL[m])
    for a, ttl in ((ax[0], "avg flood cells/step"), (ax[1], "peak flood cells/step")):
        a.set_xticks(xs); a.set_xticklabels(SCENARIOS); a.set_title(ttl); a.legend(fontsize=8)
    fig.tight_layout()
    p = os.path.join(ART, "perf_flood_bars.png")
    fig.savefig(p, dpi=85); plt.close(fig)
    copy_to_surface(p)
    print(f"  wrote {p} ({os.path.getsize(p)/1024:.0f} KB)")

    # ---------- markdown table ----------
    md = ["# D_fast cost comparison (D vs E_exact vs F) — honest, post-audit", "",
          f"Grid {W}x{H}. Steps: " + ", ".join(f"{k} {v}" for k, v in STEPS.items()) + ".",
          "Driven headlessly through node against the same `js/` physics the demo uses.",
          "",
          "- **E (E_exact)** is verified frame-for-frame identical to **D** "
          "(`experiments/test_frame_equality.js`): its flood cost tracks D because "
          "frame-identity forces the full row-major relabel every frame. It is a "
          "faithful mirror, not a speedup.",
          "- **F (D_fast)** is the certificate-gated variant that actually skips "
          "work; it is NOT frame-identical to D (hydrostatic-equivalent deviations "
          "on fragmenting scenes).", "",
          "`flood cells` = connected-component + cavity cells visited by the level "
          "solve; `cache-relax` = cavity cells F touches while relaxing off a cached "
          "target (no flood); `skip%` = body-processings that skipped the flood "
          "(cert-moving + settled). ms/step is wall-clock in node.", "",
          "| scenario | model | mass err % | U-tube Δh | peak flood | avg flood | avg cache-relax | cert-skip % | settled-skip % | skip % | avg ms | peak ms |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for sc in SCENARIOS:
        for m in MODELS:
            r = res[(sc, m)]
            dh = f"{r['utube_dh']:.3f}" if r["utube_dh"] is not None else "-"
            md.append(f"| {sc} | {m} | {r['mass_err']:.3f} | {dh} | {r['peak_flood']:.0f} | "
                      f"{r['avg_flood']:.1f} | {r['avg_relax']:.1f} | {r['cert_skip_pct']:.1f} | "
                      f"{r['settled_skip_pct']:.1f} | {r['skip_pct']:.1f} | {r['avg_ms']:.4f} | {r['peak_ms']:.3f} |")

    md += ["", "## Speedup — F (D_fast) vs D, and E_exact vs D", "",
           "E_exact should read ~1× (it does D's work); F is where the reduction is.", "",
           "| scenario | E avg flood ÷ D | F avg flood ↓ vs D | F peak flood ↓ | F avg ms ↓ |",
           "|---|---|---|---|---|"]
    for sc in SCENARIOS:
        D, E, F = res[(sc, "D")], res[(sc, "E")], res[(sc, "F")]
        e_ratio = E["avg_flood"] / D["avg_flood"] if D["avg_flood"] else float("inf")
        af = D["avg_flood"] / F["avg_flood"] if F["avg_flood"] else float("inf")
        pf = D["peak_flood"] / F["peak_flood"] if F["peak_flood"] else float("inf")
        ms = D["avg_ms"] / F["avg_ms"] if F["avg_ms"] else float("inf")
        md.append(f"| {sc} | {e_ratio:.2f}× | {af:.1f}× | {pf:.2f}× | {ms:.2f}× |")

    # ---------- ablation: does the CERTIFICATE actually pay off? ----------
    # F_noCert = D_fast with the certificate-moving-skip OFF (pure dirty-region
    # tracking + quiescence: re-flood every moving body, skip only settled ones).
    # The gap between F and F_noCert is exactly what the RPRM certificate buys.
    print("  ablation: F_noCert (certificate gate OFF)...")
    ncf = {}
    for sc in SCENARIOS:
        ncf[sc] = metrics(run(sc, FAST, STEPS[sc], overrides={"D": {"CertGate": False}}), sc)
    md += ["", "## Ablation — the certificate's own contribution (measured on F)", "",
           "`F_noCert` = D_fast with the certificate-moving-skip disabled (pure",
           "dirty-region tracking + quiescence: every MOVING body is re-flooded, only",
           "SETTLED undisturbed bodies are skipped). The extra reduction from `F_noCert`",
           "to `F` is precisely what the RPRM `P_geo` certificate buys on top of plain",
           "incremental tracking. (D and E_exact do the same full flood, so both are",
           "shown as the un-skipped baseline.)", "",
           "| scenario | D avg flood | F_noCert avg flood | F avg flood | dirty-track ↓ (D→noCert) | **certificate ↓ (noCert→F)** |",
           "|---|---|---|---|---|---|"]
    for sc in SCENARIOS:
        D = res[(sc, "D")]["avg_flood"]; NC = ncf[sc]["avg_flood"]; F = res[(sc, "F")]["avg_flood"]
        dt = D / NC if NC else float("inf")
        ct = NC / F if F else float("inf")
        md.append(f"| {sc} | {D:.1f} | {NC:.1f} | {F:.1f} | {dt:.1f}× | **{ct:.1f}×** |")

    md += ["", "![dam cost](perf_cost_dam.png)", "![utube cost](perf_cost_utube.png)",
           "![flood bars](perf_flood_bars.png)"]
    table = "\n".join(md) + "\n"
    with open(os.path.join(ART, "perf_table.md"), "w") as f:
        f.write(table)
    copy_to_surface(os.path.join(ART, "perf_table.md"))
    print("\n" + table)


if __name__ == "__main__":
    main()
