#!/usr/bin/env python3
"""Headless experiment harness for the mini-Noita liquid lab.

Drives the REAL browser physics (../js/*.js) through node (experiments/run_sim.js),
so the measured numbers describe the exact code the interactive demo runs.

Outputs, for a fixed set of scenarios x liquid models:
  * a printed comparison table (also written to artifacts/metrics_table.md)
  * animated GIFs of each scenario/model
  * matplotlib comparison plots (settling, mass conservation, active cells,
    U-tube equalization, and a compressibility trade-off sweep)

Run:  /workspace/.venv/bin/python run_experiments.py
"""
import json, os, subprocess, sys
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

MODELS = ["A", "B", "C", "D", "E"]
MODEL_LABEL = {"A": "A binary", "B": "B momentum", "C": "C mass-level",
               "D": "D level-aware", "E": "E D_fast (=D, exact)"}
SCENES = ["basin", "utube", "dam", "stress"]

# Grid / step budgets. Kept small so GIFs stay tiny and the whole run is quick.
W, H = 100, 64
STEPS = {"basin": 2000, "utube": 6000, "dam": 2000, "stress": 2000}
NFRAMES = 60  # target frames recorded per run


# ----------------------------- driver -----------------------------
def run(scenario, model, steps, overrides=None):
    frame_every = max(1, steps // NFRAMES)
    out = f"/tmp/nl_{scenario}_{model}_{steps}.json"
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


# ----------------------------- metrics -----------------------------
EMPTY, WALL, SAND, WATER = 0, 1, 2, 3


def mass_error(d):
    m = np.array([s["m"] for s in d["steps"]], dtype=np.float64)
    m0 = m[0] if m[0] != 0 else 1.0
    return float(np.max(np.abs(m - m0)) / m0), float(abs(m[-1] - m0) / m0)


def time_to_settle(d, thresh=10, window=40):
    """First step after which fewer than `thresh` cells change for a sustained
    window. None means the model never reaches quiescence (it keeps churning)."""
    mv = np.array([s["mv"] for s in d["steps"]])
    for i in range(len(mv) - window):
        if (mv[i:i + window] <= thresh).all():
            return i
    return None


def residual_activity(d):
    mv = np.array([s["mv"] for s in d["steps"]])
    tail = mv[int(0.8 * len(mv)):]
    return float(tail.mean())


def avg_active_pct(d):
    a = np.array([s["a"] for s in d["steps"]], dtype=np.float64)
    return float(a.mean() / (W * H) * 100.0)


def label_cost(d):
    """Model D's extra representation-change cost: average cells visited by the
    connected-body labeling+cavity pass per step, and average label passes/step
    (one per relaxed body). Zero for A/B/C (no labeling)."""
    lc = np.array([s.get("lc", 0) for s in d["steps"]], dtype=np.float64)
    lp = np.array([s.get("lp", 0) for s in d["steps"]], dtype=np.float64)
    return float(lc.mean()), float(lp.mean())


def surface_std(t, m):
    """Std of the free-surface top-row across wetted interior columns (flatness)."""
    tops = []
    for x in range(2, W - 2):
        col = m[:, x]
        wet = np.where(col > 0.1)[0]
        # skip columns that are just the container walls
        if len(wet) and t[wet[0], x] == WATER:
            tops.append(wet[0])
    if len(tops) < 4:
        return float("nan")
    return float(np.std(tops))


# U-tube shaft geometry — MUST match UT in ../js/scenarios.js.
UT_SW = max(5, int(W * 0.12))
UT_XL = int(W * 0.18)
UT_XR = int(W * 0.66)


def utube_heights(t, m):
    """Mean fill depth of each shaft (water volume / shaft width). Robust to
    splashes; equalized water gives left == right. A binary model leaves the far
    shaft near-empty -> large difference."""
    wmask = (t == WATER).astype(np.float32) * m
    left = wmask[:, UT_XL:UT_XL + UT_SW]
    right = wmask[:, UT_XR:UT_XR + UT_SW]
    lh = float(left.sum() / left.shape[1])
    rh = float(right.sum() / right.shape[1])
    return lh, rh


# ----------------------------- rendering -----------------------------
def render_rgb(t, m, scale=3):
    img = np.zeros((H, W, 3), dtype=np.uint8)
    img[t == EMPTY] = (12, 12, 18)
    img[t == WALL] = (90, 92, 100)
    img[t == SAND] = (194, 178, 108)
    wm = np.clip(m, 0.15, 1.4)
    r = (40 * (1.4 - wm) / 1.4 + 20).astype(np.uint8)
    g = (120 * np.clip(wm, 0, 1) + 40).astype(np.uint8)
    b = (180 + 55 * np.clip(wm, 0, 1)).astype(np.uint8)
    wmask = t == WATER
    img[wmask, 0] = r[wmask]; img[wmask, 1] = g[wmask]; img[wmask, 2] = b[wmask]
    if scale > 1:
        img = np.repeat(np.repeat(img, scale, axis=0), scale, axis=1)
    return img


def save_gif(d, path, scale=3, ms=45):
    from PIL import Image
    # Drop consecutive duplicate frames so models that freeze early don't make a
    # GIF that is 95% static; keep a short hold at the end.
    frames, prev = [], None
    for fr in d["frames"]:
        key = fr["t"]
        if key != prev:
            frames.append(fr)
            prev = key
    if frames and frames[-1] is not d["frames"][-1]:
        frames.append(d["frames"][-1])
    hold = 6  # repeat final frame so the settled state is visible before looping
    imgs = []
    for fr in frames:
        t, m = frame_arrays(fr)
        imgs.append(Image.fromarray(render_rgb(t, m, scale)).convert("P", palette=Image.ADAPTIVE, colors=32))
    imgs += [imgs[-1]] * hold
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=ms, loop=0, optimize=True)
    return os.path.getsize(path)


def copy_to_surface(path):
    if not SURF_ART:
        return
    import shutil
    shutil.copy(path, os.path.join(SURF_ART, os.path.basename(path)))


# ----------------------------- main experiment -----------------------------
def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    results = {}          # (scenario, model) -> data
    rows = []             # metrics table rows
    saved = []            # artifact paths

    for scenario in SCENES:
        for model in MODELS:
            d = run(scenario, model, STEPS[scenario])
            results[(scenario, model)] = d
            gif = os.path.join(ART, f"{scenario}_{model}.gif")
            sz = save_gif(d, gif)
            copy_to_surface(gif)
            saved.append((gif, sz))

            t, m = frame_arrays(d["frames"][-1])
            mmax, mfin = mass_error(d)
            tts = time_to_settle(d)
            lc_avg, lp_avg = label_cost(d)
            row = {
                "scenario": scenario, "model": model,
                "mass_err_max_%": mmax * 100, "mass_err_final_%": mfin * 100,
                "settle_step": tts, "residual_moved": residual_activity(d),
                "surf_std": surface_std(t, m) if scenario != "utube" else float("nan"),
                "avg_active_%": avg_active_pct(d),
                "label_cells": lc_avg, "label_passes": lp_avg,
            }
            if scenario == "utube":
                lh, rh = utube_heights(t, m)
                row["utube_dh"] = abs(lh - rh)
            rows.append(row)
            print(f"  ran {scenario}/{model}: settle={tts}, "
                  f"resid={row['residual_moved']:.1f}, active={row['avg_active_%']:.1f}%")

    # ---------- comparison plots ----------
    # Settling (moved cells) per scenario
    for scenario in SCENES:
        plt.figure(figsize=(6, 3.4))
        for model in MODELS:
            mv = [s["mv"] for s in results[(scenario, model)]["steps"]]
            plt.plot(mv, label=MODEL_LABEL[model], lw=1.3)
        plt.title(f"Settling — {scenario}\n(cells changed per step; lower/flatter = calmer)")
        plt.xlabel("step"); plt.ylabel("cells changed"); plt.legend(fontsize=8)
        plt.tight_layout()
        p = os.path.join(ART, f"settle_{scenario}.png")
        plt.savefig(p, dpi=90); plt.close(); saved.append((p, os.path.getsize(p))); copy_to_surface(p)

    # Mass conservation (all scenarios/models on one plot)
    plt.figure(figsize=(6, 3.4))
    for scenario in SCENES:
        for model in MODELS:
            m = np.array([s["m"] for s in results[(scenario, model)]["steps"]])
            plt.plot((m - m[0]) / m[0] * 100, lw=1.0, label=f"{scenario}/{model}")
    plt.title("Mass conservation error (% of initial)")
    plt.xlabel("step"); plt.ylabel("mass error %"); plt.legend(fontsize=6, ncol=3)
    plt.tight_layout()
    p = os.path.join(ART, "mass_conservation.png")
    plt.savefig(p, dpi=90); plt.close(); saved.append((p, os.path.getsize(p))); copy_to_surface(p)

    # Active-cell cost over time (basin)
    plt.figure(figsize=(6, 3.4))
    for model in MODELS:
        a = np.array([s["a"] for s in results[("basin", model)]["steps"]]) / (W * H) * 100
        plt.plot(a, label=MODEL_LABEL[model], lw=1.3)
    plt.title("Active-cell cost — basin\n(% of grid simulated per step; idle cells sleep)")
    plt.xlabel("step"); plt.ylabel("% grid active"); plt.legend(fontsize=8)
    plt.tight_layout()
    p = os.path.join(ART, "active_cost.png")
    plt.savefig(p, dpi=90); plt.close(); saved.append((p, os.path.getsize(p))); copy_to_surface(p)

    # U-tube equalization over time — the headline A/B/C/D figure. Model D drops
    # to ~0 in tens of steps (level read off a per-body field); C plateaus; A/B freeze.
    for fname in ("utube_equalization_ABCD.png", "utube_equalization.png"):
        plt.figure(figsize=(6, 3.4))
        for model in MODELS:
            d = results[("utube", model)]
            xs, dh = [], []
            for fr in d["frames"]:
                t, m = frame_arrays(fr)
                lh, rh = utube_heights(t, m)
                xs.append(fr["s"]); dh.append(abs(lh - rh))
            lw = 2.0 if model == "D" else 1.4
            plt.plot(xs, dh, label=MODEL_LABEL[model], lw=lw, marker="o", ms=2)
        plt.title("U-tube equalization — models A/B/C/D\n(|left − right| surface height; 0 = perfectly level)")
        plt.xlabel("step"); plt.ylabel("height diff (cells)"); plt.legend(fontsize=8)
        plt.tight_layout()
        p = os.path.join(ART, fname)
        plt.savefig(p, dpi=90); plt.close(); saved.append((p, os.path.getsize(p))); copy_to_surface(p)

    # Zoomed early-window version so D's fast equalization is legible next to the
    # 6000-step full view.
    plt.figure(figsize=(6, 3.4))
    for model in MODELS:
        d = results[("utube", model)]
        xs, dh = [], []
        for fr in d["frames"]:
            if fr["s"] > 400:
                continue
            t, m = frame_arrays(fr)
            lh, rh = utube_heights(t, m)
            xs.append(fr["s"]); dh.append(abs(lh - rh))
        lw = 2.0 if model == "D" else 1.4
        plt.plot(xs, dh, label=MODEL_LABEL[model], lw=lw, marker="o", ms=3)
    plt.title("U-tube equalization (first 400 steps)\nmodel D reaches level; A/B freeze, C crawls")
    plt.xlabel("step"); plt.ylabel("height diff (cells)"); plt.legend(fontsize=8)
    plt.tight_layout()
    p = os.path.join(ART, "utube_equalization_ABCD_zoom.png")
    plt.savefig(p, dpi=90); plt.close(); saved.append((p, os.path.getsize(p))); copy_to_surface(p)

    # ---------- compressibility trade-off sweep (model C, U-tube) ----------
    print("  compressibility sweep (model C U-tube)...")
    comps = [0.02, 0.05, 0.1, 0.2, 0.4]  # 0.2 is the chosen default
    plt.figure(figsize=(6, 3.4))
    sweep_final = []
    for cval in comps:
        d = run("utube", "C", STEPS["utube"], overrides={"C": {"MaxCompress": cval}})
        xs, dh = [], []
        for fr in d["frames"]:
            t, m = frame_arrays(fr)
            lh, rh = utube_heights(t, m)
            xs.append(fr["s"]); dh.append(abs(lh - rh))
        plt.plot(xs, dh, label=f"MaxCompress={cval}", lw=1.3)
        sweep_final.append((cval, dh[-1], residual_activity(d)))
    plt.title("Model C: compressibility vs U-tube equalization speed")
    plt.xlabel("step"); plt.ylabel("height diff (cells)"); plt.legend(fontsize=8)
    plt.tight_layout()
    p = os.path.join(ART, "compress_sweep.png")
    plt.savefig(p, dpi=90); plt.close(); saved.append((p, os.path.getsize(p))); copy_to_surface(p)

    # ---------- model D relabel-amortization sweep (U-tube) ----------
    # Honest cost knob: recomputing the body-level field every step (k=1) is exact
    # but costs a full labeling pass; amortizing over k steps cuts label cost but
    # lets the field go stale on fast-moving/merging bodies.
    print("  relabel amortization sweep (model D U-tube)...")
    relabel_ks = [1, 2, 4, 8, 16]
    plt.figure(figsize=(6, 3.4))
    relabel_sweep = []
    for k in relabel_ks:
        d = run("utube", "D", STEPS["utube"], overrides={"D": {"RelabelEvery": k}})
        xs, dh = [], []
        for fr in d["frames"]:
            t, m = frame_arrays(fr)
            lh, rh = utube_heights(t, m)
            xs.append(fr["s"]); dh.append(abs(lh - rh))
        plt.plot(xs, dh, label=f"RelabelEvery={k}", lw=1.3)
        lc_avg, _ = label_cost(d)
        _, mfin = mass_error(d)
        relabel_sweep.append((k, dh[-1], lc_avg, mfin * 100))
    plt.title("Model D: relabel amortization vs U-tube equalization")
    plt.xlabel("step"); plt.ylabel("height diff (cells)"); plt.legend(fontsize=8)
    plt.xlim(0, 400)
    plt.tight_layout()
    p = os.path.join(ART, "relabel_sweep.png")
    plt.savefig(p, dpi=90); plt.close(); saved.append((p, os.path.getsize(p))); copy_to_surface(p)

    # ---------- metrics table ----------
    md = ["# Model comparison metrics", "",
          f"Grid {W}x{H}. Steps: basin {STEPS['basin']}, utube {STEPS['utube']}, dam {STEPS['dam']}.",
          "Driven headlessly through node against the same `js/` physics the demo uses.", ""]
    hdr = ("| scenario | model | mass err (max/final %) | settle step | residual "
           "moved/step | surface std (cells) | U-tube \u0394h | avg active % | "
           "label cells/step | label passes/step |")
    sep = "|" + "---|" * 10
    md += [hdr, sep]
    for r in rows:
        settle = "jitter (never)" if r["settle_step"] is None else str(r["settle_step"])
        surf = "-" if np.isnan(r["surf_std"]) else f"{r['surf_std']:.2f}"
        dh = f"{r['utube_dh']:.2f}" if "utube_dh" in r else "-"
        lcell = f"{r['label_cells']:.0f}" if r["label_cells"] else "-"
        lpass = f"{r['label_passes']:.2f}" if r["label_passes"] else "-"
        md.append(f"| {r['scenario']} | {MODEL_LABEL[r['model']]} | "
                  f"{r['mass_err_max_%']:.3f} / {r['mass_err_final_%']:.3f} | {settle} | "
                  f"{r['residual_moved']:.1f} | {surf} | {dh} | {r['avg_active_%']:.1f} | "
                  f"{lcell} | {lpass} |")
    md += ["", "## Compressibility sweep (model C, U-tube)", "",
           "| MaxCompress | final \u0394h (cells) | residual moved/step |",
           "|---|---|---|"]
    for cval, dh, res in sweep_final:
        md.append(f"| {cval} | {dh:.1f} | {res:.1f} |")
    md += ["", "## Model D relabel-amortization sweep (U-tube)", "",
           "| RelabelEvery k | final \u0394h (cells) | avg label cells/step | mass err final % |",
           "|---|---|---|---|"]
    for k, dh, lc, mfin in relabel_sweep:
        md.append(f"| {k} | {dh:.2f} | {lc:.0f} | {mfin:.3f} |")
    table = "\n".join(md) + "\n"
    with open(os.path.join(ART, "metrics_table.md"), "w") as f:
        f.write(table)

    print("\n" + table)
    print("Artifacts written:")
    total = 0
    for p, sz in saved:
        total += sz
        print(f"  {p}  ({sz/1024:.0f} KB)")
    print(f"  total artifact size: {total/1024:.0f} KB")
    if SURF_ART:
        print(f"  (GIFs+plots also copied to {SURF_ART})")


if __name__ == "__main__":
    main()
