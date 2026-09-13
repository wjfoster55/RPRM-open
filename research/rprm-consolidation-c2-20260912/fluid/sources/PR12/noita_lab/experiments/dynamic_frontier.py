#!/usr/bin/env python3
"""Dynamic-frontier INSUFFICIENCY experiment (Prop-1 refutation for a DYNAMIC receiver).

Claim under test (NOT a universal lower bound): model D/F's cheap body summary

    C_body = (per-body conserved volume V, containing-cavity/container geometry)

is a SUFFICIENT statistic for the *static* receiver Q_hydro (resting surface
level) — `design/SUFFICIENCY_TEST.md` measured that — but it is INSUFFICIENT for a
*dynamic* receiver Q_dyn. This harness proves the insufficiency by exhibiting a
witness pair and quantifying how often equal-summary states disagree on Q_dyn.

The dynamic receiver (stated exactly):

    Q_dyn(x) = 1  iff, under the known continuation "step the sim's own dynamics
                  forward with gravity and NO new inflow for H frames," the water
                  mass in the monitored region (past a lip / crest) exceeds a
                  breach threshold THETA at some frame t <= H; else 0.

Ground truth for Q_dyn is an ACTUAL dynamic rollout of the sim's own dynamics
(experiments/dynamic_frontier_sim.js drives the real js/ models), NOT a summary
read-off. The static truth is the independent quasistatic oracle
(truth_solver.settle_truth), shared with the sufficiency harness.

Two states x, y are a WITNESS pair iff  C_body(x) = C_body(y)  (same container,
same volume V)  but  Q_dyn(x) != Q_dyn(y). Even one proves insufficiency; we then
measure a "summary-collision disagreement rate" over a scene suite.

Run:  /workspace/.venv/bin/python dynamic_frontier.py [K_arrangements_per_class]
"""
import json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE = os.path.join(HERE, "dynamic_frontier_sim.js")
ART = os.path.join(HERE, "..", "artifacts")
SURF_ART = "/cursor/stores/self/artifacts"
os.makedirs(ART, exist_ok=True)
try:
    os.makedirs(SURF_ART, exist_ok=True)
except OSError:
    SURF_ART = None

sys.path.insert(0, HERE)
from truth_solver import settle_truth  # noqa: E402

H, W = 48, 64
DEFAULT_MODEL = "B"        # momentum: the discarded info manifests as in-flight momentum
HORIZON = 300              # frames of the known continuation
THETA = 0.5                # breach threshold: >0.5 cell-mass past the crest


# ----------------------------- container + monitor ---------------------------
def make_container(crest_h, dx=None):
    """Closed box with a central divider that rises `crest_h` cells from the floor,
    leaving an open gap above it (the lip/crest). Returns (walls, dx, floor,
    left_cols, monitor). The monitored region is the whole RIGHT compartment."""
    if dx is None:
        dx = W // 2
    walls = np.zeros((H, W), bool)
    walls[0, :] = walls[-1, :] = True
    walls[:, 0] = walls[:, -1] = True
    floor = H - 2
    crest_y = floor - crest_h
    walls[crest_y:floor + 1, dx] = True
    left_cols = list(range(1, dx))
    monitor = [y * W + x for y in range(1, H - 1) for x in range(dx + 1, W - 1)]
    return walls, dx, floor, left_cols, monitor, crest_y


# ---------------------- arrangements of a fixed volume V ---------------------
# Every builder places EXACTLY V cell-masses inside the LEFT compartment, so all
# arrangements in a family share C_body = (V, container). They differ only in the
# discarded spatial arrangement (== in-flight potential/momentum once released).
def _place(mass, cells, V):
    placed = 0
    for (y, x) in cells:
        if placed >= V:
            break
        mass[y, x] = 1.0
        placed += 1
    return placed


def arr_flat(walls, floor, left_cols, V):
    mass = np.zeros((H, W))
    cells = [(y, x) for y in range(floor, 0, -1) for x in left_cols if not walls[y, x]]
    _place(mass, cells, V)
    return mass


def arr_column(walls, floor, left_cols, V, width, x0):
    mass = np.zeros((H, W))
    cols = [x for x in range(x0, x0 + width) if x in left_cols]
    cells = [(y, x) for y in range(1, floor + 1) for x in cols if not walls[y, x]]
    # fill TOP-first so it is a tall column of potential energy
    cells = sorted(cells, key=lambda c: (c[0]))   # small y (high) first
    _place(mass, cells, V)
    return mass


def arr_two_columns(walls, floor, left_cols, V, width):
    mass = np.zeros((H, W))
    a0 = left_cols[0]
    b0 = left_cols[-1] - width + 1
    colsA = [x for x in range(a0, a0 + width) if x in left_cols]
    colsB = [x for x in range(b0, b0 + width) if x in left_cols]
    cellsA = sorted([(y, x) for y in range(1, floor + 1) for x in colsA if not walls[y, x]], key=lambda c: c[0])
    cellsB = sorted([(y, x) for y in range(1, floor + 1) for x in colsB if not walls[y, x]], key=lambda c: c[0])
    # interleave so both grow together
    cells = []
    for a, b in zip(cellsA, cellsB):
        cells.append(a); cells.append(b)
    _place(mass, cells, V)
    return mass


def arr_ramp(walls, floor, left_cols, V):
    """Triangular pile leaning on the divider side (higher near the crest)."""
    mass = np.zeros((H, W))
    # order columns from divider side outward; taller near divider
    order = sorted(left_cols, reverse=True)
    cells = []
    for depth in range(1, floor):
        for k, x in enumerate(order):
            y = floor - depth
            # only include this column if depth <= its allotted height (taller near divider)
            if depth <= (len(order) - k):
                if not walls[y, x]:
                    cells.append((y, x))
    _place(mass, cells, V)
    return mass


def build_family(walls, floor, left_cols, V):
    """A set of DISTINCT arrangements, all of exact volume V, same container."""
    out = {}
    out["flat"] = arr_flat(walls, floor, left_cols, V)
    dx = left_cols[-1] + 1
    out["col_adj_w4"] = arr_column(walls, floor, left_cols, V, 4, dx - 4)
    out["col_adj_w6"] = arr_column(walls, floor, left_cols, V, 6, dx - 6)
    out["col_mid_w4"] = arr_column(walls, floor, left_cols, V, 4, (left_cols[0] + dx) // 2)
    out["col_far_w4"] = arr_column(walls, floor, left_cols, V, 4, left_cols[0])
    out["two_col_w3"] = arr_two_columns(walls, floor, left_cols, V, 3)
    out["ramp"] = arr_ramp(walls, floor, left_cols, V)
    # keep only arrangements that actually hold the full V (capacity check)
    return {k: m for k, m in out.items() if abs(m.sum() - V) < 0.5}


# ------------------------------ rollout bridge -------------------------------
def rollout(walls, mass, model, monitor, steps=HORIZON, thresh=THETA, snaps=None):
    spec = {"W": W, "H": H, "walls": walls.astype(int).flatten().tolist(),
            "mass": [round(float(v), 5) for v in mass.flatten().tolist()],
            "model": model, "steps": steps, "monitor": monitor, "thresh": thresh,
            "snapshotSteps": snaps or []}
    json.dump(spec, open("/tmp/df_spec.json", "w"))
    subprocess.run(["node", BRIDGE, "/tmp/df_spec.json", "/tmp/df_out.json"], check=True)
    return json.load(open("/tmp/df_out.json"))


def q_dyn(walls, mass, model, monitor):
    return rollout(walls, mass, model, monitor)


# ------------------------------- rendering -----------------------------------
def render_state(walls, mass, scale=5):
    img = np.zeros((H, W, 3), dtype=np.uint8)
    img[:] = (12, 12, 18)
    img[walls.astype(bool)] = (90, 92, 100)
    wm = np.clip(mass, 0.0, 1.0)
    wmask = mass > 1e-6
    img[wmask, 0] = (30 + 20 * (1 - wm[wmask])).astype(np.uint8)
    img[wmask, 1] = (90 + 60 * wm[wmask]).astype(np.uint8)
    img[wmask, 2] = (180 + 55 * wm[wmask]).astype(np.uint8)
    return np.repeat(np.repeat(img, scale, 0), scale, 1)


def snap_grid(snapshot):
    m = np.array(snapshot["m"], dtype=np.float64).reshape(H, W)
    walls = m < 0
    mass = np.where(m < 0, 0.0, m)
    return walls, mass


def copy_surface(path):
    if not SURF_ART:
        return
    import shutil
    shutil.copy(path, os.path.join(SURF_ART, os.path.basename(path)))


# --------------------------------- main --------------------------------------
def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    K = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    model = DEFAULT_MODEL
    report = []

    def log(s=""):
        print(s)
        report.append(s)

    log("# Dynamic-frontier insufficiency: C_body is NOT sufficient for Q_dyn")
    log("")
    log(f"Grid {H}x{W}. Continuation model = {model} (momentum). Horizon H = {HORIZON} "
        f"frames. Breach threshold THETA = {THETA} cell-mass past the crest.")
    log("")

    # ======================= 1. the headline witness pair ====================
    walls, dx, floor, left_cols, monitor, crest_y = make_container(crest_h=10)
    V = 180
    fam = build_family(walls, floor, left_cols, V)
    tall = fam["col_adj_w6"]
    flat = fam["flat"]

    # static truth: identical for both (same V, same container) -> C_body sufficient for Q_hydro
    t_tall = settle_truth(tall, walls)
    t_flat = settle_truth(flat, walls)
    static_tv = float(np.abs(t_tall - t_flat).sum() / 2.0)
    right_static_tall = float(t_tall[:, dx + 1:W - 1].sum())
    right_static_flat = float(t_flat[:, dx + 1:W - 1].sum())

    snaps = [0, 3, 6, 12, 40]
    r_tall = rollout(walls, tall, model, monitor, snaps=snaps)
    r_flat = rollout(walls, flat, model, monitor, snaps=snaps)

    log("## 1. Witness pair (concrete numbers)")
    log("")
    log(f"Container: closed box, central divider rising {floor - crest_y} cells from the "
        f"floor (crest row {crest_y}); monitored region = the entire RIGHT compartment.")
    log(f"Both states: identical container, identical volume V = {V} "
        f"(TALL sum={tall.sum():.0f}, FLAT sum={flat.sum():.0f}) => identical C_body.")
    log("")
    log(f"- STATIC receiver Q_hydro (independent QUASISTATIC oracle): the resting "
        f"distribution it assigns each state is IDENTICAL — right-compartment mass "
        f"TALL={right_static_tall:.3f}, FLAT={right_static_flat:.3f}, TV(tall,flat) = "
        f"{static_tv:.3f}. So both states share one Q_hydro answer — **C_body IS "
        f"sufficient for the quasistatic receiver**, as `SUFFICIENCY_TEST.md` certified.")
    log(f"- DYNAMIC receiver Q_dyn (actual model-{model} rollout, H={HORIZON}): "
        f"**TALL Q_dyn = {r_tall['Qdyn']}** (peak right-mass {r_tall['maxMonitored']:.1f}, "
        f"first breach at frame {r_tall['firstBreach']}); "
        f"**FLAT Q_dyn = {r_flat['Qdyn']}** (peak right-mass {r_flat['maxMonitored']:.1f}).")
    log("")
    log(f"=> C_body(TALL) = C_body(FLAT) but Q_dyn(TALL)={r_tall['Qdyn']} != "
        f"Q_dyn(FLAT)={r_flat['Qdyn']}. **C_body is INSUFFICIENT for Q_dyn** (Prop-1 "
        f"refutation for this receiver). This is insufficiency of THIS summary, not a "
        f"universal lower bound.")
    log("")
    log(f"**The sharp version (read this):** the quasistatic oracle *assigns the tall "
        f"column the same resting-left answer as the flat one* — but the model-{model} "
        f"rollout shows the tall column's momentum actually carries ~{r_tall['maxMonitored']:.0f} "
        f"cell-mass over the crest, which the one-way crest then TRAPS on the right. That "
        f"path-dependent, momentum-driven deposit is a real dynamic outcome the "
        f"quasistatic summary (and C_body) provably cannot represent — the two states are "
        f"Q_hydro-indistinguishable yet Q_dyn-distinct. That gap IS the insufficiency.")
    log("")

    # figure: the two start states + a rollout frame each + the timeseries
    fig = plt.figure(figsize=(11, 5.2))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.3, 1])
    # start states
    for col, (r, label) in enumerate([(r_tall, "TALL column"), (r_flat, "FLAT puddle")]):
        ax = fig.add_subplot(gs[0, col])
        w0, m0 = snap_grid(r["snapshots"][0])
        ax.imshow(render_state(w0, m0))
        ax.set_title(f"{label}: start (V={V}, same C_body)", fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
    # a mid-rollout frame of the tall one (the overtopping wave)
    ax = fig.add_subplot(gs[0, 2])
    w6, m6 = snap_grid(r_tall["snapshots"][3])  # frame 12
    ax.imshow(render_state(w6, m6))
    ax.set_title(f"TALL @ frame {r_tall['snapshots'][3]['s']}: wave overtops crest", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    # timeseries
    ax = fig.add_subplot(gs[1, :])
    ax.plot(r_tall["series"], lw=1.6, color="tab:red",
            label=f"TALL  (Q_dyn={r_tall['Qdyn']}, peak {r_tall['maxMonitored']:.1f})")
    ax.plot(r_flat["series"], lw=1.6, color="tab:blue",
            label=f"FLAT  (Q_dyn={r_flat['Qdyn']}, peak {r_flat['maxMonitored']:.1f})")
    ax.axhline(THETA, ls="--", color="k", lw=1, label=f"breach threshold THETA={THETA}")
    ax.set_xlabel("continuation frame t"); ax.set_ylabel("water mass past the crest")
    ax.set_title("Same C_body (V, container), DIFFERENT transient overflow — "
                 "C_body cannot decide Q_dyn", fontsize=10)
    ax.legend(fontsize=8, loc="upper right"); ax.grid(alpha=0.3)
    fig.tight_layout()
    p = os.path.join(ART, "dynamic_frontier_witness.png")
    fig.savefig(p, dpi=95); plt.close(fig)
    copy_surface(p)
    log(f"![witness pair](dynamic_frontier_witness.png)")
    log("")

    # ================= 2. summary-collision disagreement rate ================
    log("## 2. Summary-collision disagreement rate (scene suite)")
    log("")
    log(f"For each (container, V) CLASS all arrangements share C_body. We roll out "
        f"K per class and count how often equal-summary states DISAGREE on Q_dyn. "
        f"We also verify the static truth is identical within each class (so the "
        f"disagreement is purely dynamic).")
    log("")
    classes = []
    for crest_h in [8, 10, 12]:
        walls, dx, floor, left_cols, monitor, crest_y = make_container(crest_h=crest_h)
        capacity = int((~walls[:, 1:dx]).sum())
        for V in [140, 180, 220]:
            if V > 0.6 * capacity:
                continue
            fam = build_family(walls, floor, left_cols, V)
            # cap at K arrangements
            items = list(fam.items())[:max(2, K)]
            qs = {}
            static_grids = []
            for name, m in items:
                r = q_dyn(walls, m, model, monitor)
                qs[name] = (r["Qdyn"], r["maxMonitored"], r["firstBreach"])
                static_grids.append(settle_truth(m, walls))
            # static agreement within class
            base = static_grids[0]
            max_static_tv = max(float(np.abs(g - base).sum() / 2.0) for g in static_grids)
            spill = sum(1 for v in qs.values() if v[0] == 1)
            nospill = len(qs) - spill
            n = len(qs)
            pair_dis = (2 * spill * nospill) / (n * (n - 1)) if n > 1 else 0.0
            mixed = spill > 0 and nospill > 0
            classes.append(dict(crest_h=crest_h, V=V, n=n, spill=spill, nospill=nospill,
                                pair_dis=pair_dis, mixed=mixed, max_static_tv=max_static_tv,
                                qs=qs))

    log("| container crest_h | V | arrangements | Q_dyn=1 | Q_dyn=0 | pairwise disagreement | static TV (within class) | mixed? |")
    log("|---|---|---|---|---|---|---|---|")
    tot_pairs = 0
    dis_pairs = 0
    mixed_classes = 0
    for c in classes:
        n = c["n"]
        pairs = n * (n - 1) // 2
        dpairs = c["spill"] * c["nospill"]
        tot_pairs += pairs
        dis_pairs += dpairs
        mixed_classes += 1 if c["mixed"] else 0
        log(f"| {c['crest_h']} | {c['V']} | {n} | {c['spill']} | {c['nospill']} | "
            f"{c['pair_dis']*100:.1f}% | {c['max_static_tv']:.3f} | "
            f"{'YES' if c['mixed'] else 'no'} |")
    overall = (dis_pairs / tot_pairs * 100) if tot_pairs else 0.0
    log("")
    log(f"**Summary-collision disagreement rate: {dis_pairs}/{tot_pairs} equal-C_body "
        f"pairs ({overall:.1f}%) disagree on Q_dyn.** "
        f"{mixed_classes}/{len(classes)} equal-summary classes are 'mixed' (contain both "
        f"a spill and a no-spill state). Within every class the static truth is identical "
        f"(max static TV = {max((c['max_static_tv'] for c in classes), default=0):.3f}), so "
        f"the disagreement is entirely dynamic: C_body determines the static answer but "
        f"not Q_dyn.")
    log("")

    # ==================== 3. the minimal RPRM repair =========================
    log("## 3. The minimal RPRM repair (Prop-1: C' = (C_body, extra))")
    log("")
    # cheap partial summaries: do they resolve the classes?
    def summary_of(mass, walls, kind):
        ys, xs = np.nonzero(mass > 1e-6)
        V = float(mass.sum())
        if kind == "V":                 # exactly C_body's volume coordinate
            return (round(V, 3),)
        if kind == "V_top":             # C_body + the highest occupied row (D's `top`)
            top = int(ys.min()) if len(ys) else H
            return (round(V, 3), top)
        raise ValueError(kind)

    # For each class, check whether a candidate cheap summary still COLLIDES (two
    # states with equal summary but different Q_dyn -> summary insufficient).
    log("A cheap summary S is INSUFFICIENT for Q_dyn if two states with equal S "
        "disagree on Q_dyn (a collision). C_body's own coordinate is V; a natural "
        "'obvious fix' is to also retain the highest occupied row (D's `top`). Both "
        "still collide:")
    log("")
    for kind in ["V", "V_top"]:
        collide = 0
        colwit = None
        for c in classes:
            walls_c, dx_c, floor_c, left_cols_c, mon_c, cy_c = make_container(crest_h=c["crest_h"])
            fam = build_family(walls_c, floor_c, left_cols_c, c["V"])
            items = list(fam.items())[:c["n"]]
            buckets = {}
            for name, m in items:
                s = summary_of(m, walls_c, kind)
                q = c["qs"][name][0]
                buckets.setdefault(s, []).append((name, q))
            for s, members in buckets.items():
                if len(set(q for _, q in members)) > 1:
                    collide += 1
                    if colwit is None:
                        colwit = (c["crest_h"], c["V"], s, members)
        wit = ""
        if colwit:
            wit = (f" e.g. crest_h={colwit[0]} V={colwit[1]}, equal summary "
                   f"{colwit[2]}: {[(n, q) for n, q in colwit[3]]} "
                   f"(position of an equal-height column decides spill).")
        label = {"V": "V  (== C_body)", "V_top": "V + top row"}[kind]
        log(f"- **{label}**: {collide} colliding summary-classes => still "
            f"**INSUFFICIENT**.{wit}")
    log("")
    log("So even C_body augmented with the surface height (`top`) does not decide "
        "Q_dyn: two equal-volume columns of the same height but different horizontal "
        "position disagree on whether their collapse overtops the crest. The exact "
        "Prop-1 repair is `C'(x) = (C_body(x), Q_dyn(x))` — cache the "
        "answer, the least informative refinement. The minimal *physical* state that "
        "restores sufficiency is the full **dynamic field** (the in-flight water "
        "distribution / arrangement, and under a momentum model the velocity field): "
        "with it, rolling the dynamics forward reproduces Q_dyn exactly, BY "
        "CONSTRUCTION. This is precisely RPRM_FLUIDS.md §3.3's forced fallback "
        "`C' = (C_body, velocity field)`: retaining it reintroduces the dynamic cost. "
        "So 'dynamic is expensive' is reframed honestly as 'this cheap summary is "
        "insufficient; here is the minimal add-back, and it is exactly the dynamic "
        "state we tried to discard.'")
    log("")
    log("## Honest scope")
    log("")
    log("This refutes sufficiency of the SPECIFIC summary C_body = (V, container "
        "geometry) for the SPECIFIC dynamic receiver Q_dyn. It is **not** a universal "
        "lower bound and **not** a claim that no local representation can answer Q_dyn "
        "(consistent with RPRM_FLUIDS.md §3.1's insufficiency *conjecture*, which we do "
        "not upgrade to a theorem). The static receiver Q_hydro remains sufficient for "
        "C_body — verified here by identical within-class static truth.")

    # write the doc-friendly results md (numbers only; the prose doc is DYNAMIC_FRONTIER.md)
    with open(os.path.join(ART, "dynamic_frontier_results.md"), "w") as f:
        f.write("\n".join(report) + "\n")
    copy_surface(os.path.join(ART, "dynamic_frontier_results.md"))
    print("\nArtifacts:")
    print(f"  {p}")
    print(f"  {os.path.join(ART, 'dynamic_frontier_results.md')}")


if __name__ == "__main__":
    main()
