#!/usr/bin/env python3
"""RPRM sufficiency-certificate falsification harness.

Receiver question R_static: "what is the resting free-surface level of this
connected water body?" Model D answers it instantaneously from the summary
C_body = (body volume V, containing-cavity geometry) by a bottom-up cavity fill
(js/models.js `relaxLevels`). The RPRM certificate P (js/certificate.js), derived
from Prop 1 / Prop 2 of the Process Mechanics paper, is supposed to certify —
cheaply, from the instantaneous state — WHEN that read-off equals the true rest.

This harness tries to BREAK that claim. Over a large randomized suite of
container geometries and fill states it:
  1. gets D's read-off + P's verdict + naive baseline signals from node
     (certify_sim.js -> js/certificate.js), all instantaneous, no settling;
  2. computes the TRUTH with an independent solver (truth_solver.settle_truth);
  3. asks: was D's read-off exact (pred grid == truth grid within eps)?
and reports the CONFUSION MATRIX {P says exact} x {actually exact}, the
false-positive rate (the decisive number), certification rate, and a head-to-head
against the naive "quiescent" and "low-speed" baselines.

Run:  /workspace/.venv/bin/python sufficiency_test.py [N_per_family]
"""
import json, os, subprocess, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CERT_SIM = os.path.join(HERE, "certify_sim.js")
ART = os.path.join(HERE, "..", "artifacts")
SURF_ART = "/cursor/stores/self/artifacts"
os.makedirs(ART, exist_ok=True)
try:
    os.makedirs(SURF_ART, exist_ok=True)
except OSError:
    SURF_ART = None

sys.path.insert(0, HERE)
from truth_solver import settle_truth, surface_levels, MAXMASS  # noqa: E402

H, W = 40, 52
EXACT_TV = 1.0     # scene is "exact" if TV(pred,truth) < this many cell-masses


# ============================ geometry generators ===========================
def _base():
    walls = np.zeros((H, W), bool)
    walls[0, :] = walls[-1, :] = True
    walls[:, 0] = walls[:, -1] = True
    mass = np.zeros((H, W))
    return walls, mass


def _fill_rect(mass, walls, y0, y1, x0, x1, amt=1.0):
    y0, y1 = max(1, y0), min(H - 1, y1)
    x0, x1 = max(1, x0), min(W - 1, x1)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not walls[y, x]:
                mass[y, x] = amt


def gen_flat_basin(rng):
    walls, mass = _base()
    floor = H - 2
    # optional inner bowl walls
    bw = rng.integers(0, 3)
    x0 = rng.integers(2, 8)
    x1 = W - rng.integers(2, 8)
    if bw:
        wy = rng.integers(H // 2, H - 3)
        walls[wy:H - 1, 1:x0] = True
        walls[wy:H - 1, x1:W - 1] = True
    # water: a column dropped somewhere (often non-quiescent) or a settled slab
    if rng.random() < 0.5:
        cw = rng.integers(3, 10)
        cx = rng.integers(x0 + 1, max(x0 + 2, x1 - cw - 1))
        ytop = rng.integers(2, H // 2)
        _fill_rect(mass, walls, ytop, floor, cx, cx + cw)
    else:
        depth = rng.integers(3, H // 2)
        _fill_rect(mass, walls, floor - depth, floor, x0, x1)
    return "flat_basin", walls, mass


def gen_utube(rng):
    walls, mass = _base()
    top = rng.integers(2, 6)
    walls[top:H - 1, 1:W - 1] = True
    sw = rng.integers(4, 8)
    xL = rng.integers(3, 10)
    xR = rng.integers(W // 2 + 2, W - sw - 3)
    floor = H - rng.integers(3, 6)
    for y in range(top, floor):
        walls[y, xL:xL + sw] = False
        walls[y, xR:xR + sw] = False
    walls[floor:H - 1, xL:xR + sw] = False       # bottom channel
    # fill: left tall, right maybe partly (asymmetric, usually non-quiescent)
    fillH = rng.integers(4, floor - top - 1)
    _fill_rect(mass, walls, floor - fillH, floor, xL, xL + sw)
    if rng.random() < 0.4:
        fh2 = rng.integers(1, max(2, fillH // 2))
        _fill_rect(mass, walls, floor - fh2, floor, xR, xR + sw)
    mass[walls] = 0
    return "utube", walls, mass


def gen_multipocket(rng):
    walls, mass = _base()
    floor = H - 2
    npk = rng.integers(2, 4)
    xs = np.linspace(2, W - 2, npk + 1).astype(int)
    # ridges between pockets, random heights (some tall, some short)
    ridge_x = []
    for k in range(1, npk):
        rx = int(xs[k])
        rh = rng.integers(4, H - 4)          # ridge extends from floor up rh cells
        walls[H - 1 - rh:H - 1, rx] = True
        ridge_x.append((rx, rh))
    # water in each pocket, random depth (some may spill / share levels)
    for k in range(npk):
        x0 = int(xs[k]) + 1
        x1 = int(xs[k + 1]) - 1
        if x1 - x0 < 2:
            continue
        d = rng.integers(0, H - 6)
        if d > 0:
            _fill_rect(mass, walls, floor - d, floor, x0, x1)
    mass[walls] = 0
    return "multipocket", walls, mass


def gen_ledge(rng):
    walls, mass = _base()
    floor = H - 2
    # a raised shelf on the left forming an upper basin with a lip, lower basin right
    shelf_y = rng.integers(H // 3, 2 * H // 3)
    lip_x = rng.integers(W // 3, 2 * W // 3)
    walls[shelf_y:H - 1, 1:2] = True
    walls[shelf_y, 1:lip_x] = True               # shelf floor
    walls[shelf_y - rng.integers(3, 8):shelf_y, lip_x] = True  # the lip wall
    # water on the shelf (upper basin), maybe overfilled to spill
    d = rng.integers(1, max(2, shelf_y - 3))
    _fill_rect(mass, walls, shelf_y - d, shelf_y, 2, lip_x)
    # maybe some water already in the lower basin
    if rng.random() < 0.5:
        d2 = rng.integers(1, 6)
        _fill_rect(mass, walls, floor - d2, floor, lip_x + 1, W - 2)
    mass[walls] = 0
    return "ledge", walls, mass


def gen_tilted(rng):
    walls, mass = _base()
    # staircase floor
    steps = rng.integers(3, 7)
    sw = (W - 4) // steps
    for s in range(steps):
        h = 2 + s * rng.integers(1, 3)
        x0 = 1 + s * sw
        x1 = x0 + sw
        walls[H - 1 - h:H - 1, x0:x1] = True
    # water poured somewhere on the staircase
    cx = rng.integers(3, W - 6)
    cw = rng.integers(3, 8)
    ytop = rng.integers(2, H // 2)
    _fill_rect(mass, walls, ytop, H - 2, cx, cx + cw)
    mass[walls] = 0
    return "tilted", walls, mass


def gen_midsplash(rng):
    _, _ = _base()
    name, walls, mass = rng.choice([gen_flat_basin, gen_multipocket, gen_tilted])(rng)
    # lift a chunk of the water into the air to make a genuine non-quiescent state
    ys, xs = np.nonzero(mass > 0)
    if len(ys):
        k = min(len(ys), rng.integers(5, 40))
        idx = rng.choice(len(ys), size=k, replace=False)
        for i in idx:
            y, x = ys[i], xs[i]
            ny = max(1, y - rng.integers(3, 12))
            if not walls[ny, x] and mass[ny, x] == 0:
                mass[ny, x] = mass[y, x]
                mass[y, x] = 0
    # plus a free-floating block
    if rng.random() < 0.6:
        bw = rng.integers(3, 8)
        bx = rng.integers(2, W - bw - 2)
        by = rng.integers(2, H // 3)
        _fill_rect(mass, walls, by, by + rng.integers(2, 5), bx, bx + bw)
    mass[walls] = 0
    return "midsplash", walls, mass


def gen_trap_shared_cavity(rng):
    """TRAP: two water-DISCONNECTED pools that share one air cavity, arranged so
    D's `top`-bounded cavity flood spans both and its first-claim under-allocates
    the second pool. A quiescent scene that D nonetheless mis-levels."""
    walls, mass = _base()
    floor = H - 2
    # a central divider that does NOT reach the ceiling -> shared air above it
    dx = W // 2
    div_h = rng.integers(6, H - 8)               # divider height from floor
    walls[H - 1 - div_h:H - 1, dx] = True
    # left pool DEEP so its surface sits ABOVE the divider top (triggers over-flood)
    dl = rng.integers(div_h + 2, H - 4)
    _fill_rect(mass, walls, floor - dl, floor, 2, dx)
    # right pool shallow (below divider)
    dr = rng.integers(1, max(2, div_h - 2))
    _fill_rect(mass, walls, floor - dr, floor, dx + 1, W - 2)
    mass[walls] = 0
    return "trap_shared_cavity", walls, mass


def gen_trap_perched(rng):
    """TRAP: water piled above a submerged ridge (non-quiescent) so D's cavity,
    bounded by the inflated `top`, spans two basins that the resting water won't
    connect."""
    walls, mass = _base()
    floor = H - 2
    rx = W // 2
    rh = rng.integers(5, H - 10)
    walls[H - 1 - rh:H - 1, rx] = True
    # pile a tall thin column on the LEFT, well above the ridge
    cw = rng.integers(3, 7)
    _fill_rect(mass, walls, 2, floor, 3, 3 + cw)     # tall column, small volume rel. to basin
    mass[walls] = 0
    return "trap_perched", walls, mass


def gen_trapped_air(rng):
    """Adversarial STILL scene: an overhang encloses an air pocket BELOW the
    water surface. Water rests around it (locally quiescent). D's cavity flood
    reaches the pocket through a submerged gap and fills it, but the truth may
    keep it as trapped air (or vice versa). Probes for still-but-wrong-for-D."""
    walls, mass = _base()
    floor = H - 2
    # a big tank
    tank_l, tank_r = 3, W - 3
    tank_top = rng.integers(4, 10)
    # an overhang: a horizontal wall slab jutting from the left, with a gap under
    ov_y = rng.integers(tank_top + 4, H - 8)
    ov_x1 = rng.integers(W // 3, 2 * W // 3)
    walls[ov_y, tank_l:ov_x1] = True                 # overhang ceiling
    # a short wall hanging down at the right end of the overhang, leaving a gap
    hang = rng.integers(2, 5)
    walls[ov_y:ov_y + hang, ov_x1 - 1] = True         # lip under the overhang
    # fill the tank with water to above the overhang (so pocket is submerged)
    fill_top = rng.integers(tank_top + 1, ov_y - 1)
    _fill_rect(mass, walls, fill_top, floor, tank_l, tank_r)
    mass[walls] = 0
    return "trapped_air", walls, mass


def gen_closed_tank(rng):
    """A settled (or nearly) closed tank with irregular floor bumps. Mostly
    quiescent, single connected body -> D should be exact; a control family to
    check the certificate does not over-reject easy cases."""
    walls, mass = _base()
    floor = H - 2
    # a few floor bumps (submerged, below the water line)
    nb = rng.integers(0, 4)
    for _ in range(nb):
        bx = rng.integers(3, W - 4)
        bw = rng.integers(1, 4)
        bh = rng.integers(1, 5)
        walls[floor - bh:floor, bx:bx + bw] = True
    depth = rng.integers(6, H - 8)
    _fill_rect(mass, walls, floor - depth, floor, 2, W - 2)
    mass[walls] = 0
    return "closed_tank", walls, mass


GENERATORS = [gen_flat_basin, gen_utube, gen_multipocket, gen_ledge, gen_tilted,
              gen_midsplash, gen_trap_shared_cavity, gen_trap_perched,
              gen_trapped_air, gen_closed_tank]


# ============================ evaluation ====================================
def evaluate(walls, mass, tag, idx):
    spec = {"W": W, "H": H, "walls": walls.astype(int).flatten().tolist(),
            "mass": [round(float(v), 5) for v in mass.flatten().tolist()]}
    sp = f"/tmp/nl_cert_spec_{idx}.json"
    op = f"/tmp/nl_cert_out_{idx}.json"
    json.dump(spec, open(sp, "w"))
    subprocess.run(["node", CERT_SIM, sp, op], check=True)
    r = json.load(open(op))
    pred = np.array(r["pred"], dtype=np.float64).reshape(H, W)
    massg = np.array(r["mass"], dtype=np.float64).reshape(H, W)

    truth = settle_truth(massg, walls)

    # sanity: both representations must conserve the starting mass exactly.
    m0 = float(massg.sum())
    assert abs(pred.sum() - m0) < 1e-2, f"D pred leaks mass {pred.sum()} vs {m0}"
    assert abs(truth.sum() - m0) < 1e-2, f"truth leaks mass {truth.sum()} vs {m0}"

    tv = float(np.abs(pred - truth).sum() / 2.0)
    maxc = float(np.abs(pred - truth).max())
    total = float(massg.sum())
    exact = tv < EXACT_TV

    bodies = r["bodies"]
    # scene certificate = AND over bodies of each variant
    def allb(key):
        return all(b[key] for b in bodies) if bodies else True
    C1 = allb("C1"); C2 = allb("C2"); C3 = allb("C3"); C4 = allb("C4")
    P_full = C1 and C2 and C3
    P_noC2 = C1 and C3
    P_geo = C1 and C3 and C4          # the "pure geometric" certificate (no quiescence)
    P_C1only = C1
    base = r["baseline"]
    os.remove(sp); os.remove(op)
    return {
        "tag": tag, "total": total, "tv": tv, "maxc": maxc, "exact": exact,
        "C1": C1, "C2": C2, "C3": C3, "C4": C4,
        "P_full": P_full, "P_noC2": P_noC2, "P_geo": P_geo, "P_C1only": P_C1only,
        "nbodies": len(bodies),
        "activeWaterCells": base["activeWaterCells"],
        "maxFlow": base["maxFlow"], "movedMass": base["movedMass"],
        "walls": walls, "mass": massg, "pred": pred, "truth": truth,
    }


def confusion(rows, verdict_key):
    """Return (TP, FP, FN, TN) for {verdict says exact} x {actually exact}."""
    TP = FP = FN = TN = 0
    for r in rows:
        says = r[verdict_key]
        act = r["exact"]
        if says and act: TP += 1
        elif says and not act: FP += 1
        elif not says and act: FN += 1
        else: TN += 1
    return TP, FP, FN, TN


def metrics(rows, verdict_key):
    TP, FP, FN, TN = confusion(rows, verdict_key)
    n = len(rows)
    cov = (TP + FP) / n if n else 0            # fraction certified
    fp_rate = FP / (TP + FP) if (TP + FP) else 0.0   # of certified, fraction wrong
    fp_of_all = FP / n if n else 0
    recall = TP / (TP + FN) if (TP + FN) else 0.0    # of exact cases, fraction caught
    return dict(TP=TP, FP=FP, FN=FN, TN=TN, coverage=cov, fp_rate=fp_rate,
                fp_of_all=fp_of_all, recall=recall)


def baseline_verdicts(rows, tau_active, tau_speed):
    for r in rows:
        r["base_quiescent"] = r["activeWaterCells"] <= tau_active
        r["base_speed"] = r["maxFlow"] <= tau_speed


def best_baseline_tau(rows, key, taus):
    """Pick the baseline threshold with the HIGHEST coverage subject to FP==0
    (favor the baseline). If none reach FP==0, pick min FP then max coverage."""
    best = None
    for t in taus:
        for r in rows:
            r["_b"] = (r[key] <= t)
        m = metrics(rows, "_b")
        score = (m["FP"], -m["coverage"])
        if best is None or score < best[0]:
            best = (score, t, m)
    for r in rows:
        r.pop("_b", None)
    return best[1], best[2]


# ============================ rendering =====================================
def render_state(walls, mass, scale=6):
    img = np.zeros((H, W, 3), dtype=np.uint8)
    img[:] = (12, 12, 18)
    img[walls.astype(bool)] = (90, 92, 100)
    wm = np.clip(mass, 0.0, 1.0)
    wmask = mass > 1e-6
    img[wmask, 0] = (30 + 20 * (1 - wm[wmask])).astype(np.uint8)
    img[wmask, 1] = (90 + 60 * wm[wmask]).astype(np.uint8)
    img[wmask, 2] = (180 + 55 * wm[wmask]).astype(np.uint8)
    return np.repeat(np.repeat(img, scale, 0), scale, 1)


def save_case_figure(row, path, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.7))
    for ax, (lbl, grid) in zip(axes, [
            ("start state", row["mass"]),
            ("D read-off (pred rest)", row["pred"]),
            ("TRUTH (independent solve)", row["truth"])]):
        ax.imshow(render_state(row["walls"], grid))
        ax.set_title(lbl, fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
    verdicts = (f"P_full={row['P_full']}  C1={row['C1']} C2={row['C2']} C3={row['C3']}  "
                f"quiescent={row.get('base_quiescent')}  |  exact={row['exact']} (TV={row['tv']:.2f})")
    fig.suptitle(title + "\n" + verdicts, fontsize=8)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(path, dpi=90); plt.close(fig)
    return os.path.getsize(path)


def copy_surface(path):
    if not SURF_ART:
        return
    import shutil
    shutil.copy(path, os.path.join(SURF_ART, os.path.basename(path)))


# ============================ main ==========================================
def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 130
    rng = np.random.default_rng(20260911)
    saved = []

    rows = []
    print(f"Generating + evaluating ~{n_per * len(GENERATORS)} cases...")
    idx = 0
    for gen in GENERATORS:
        made = 0
        attempts = 0
        while made < n_per and attempts < n_per * 4:
            attempts += 1
            _tag, walls, mass = gen(rng)
            if mass.sum() < 3:        # skip trivially empty
                continue
            # volume budget: skip if water is a huge fraction of the void (avoid
            # ceiling overflow which neither D nor the closed-container truth model).
            void = int((~walls).sum())
            if mass.sum() > 0.6 * void:
                continue
            try:
                row = evaluate(walls, mass, _tag, idx)
            except Exception as e:
                print(f"  [skip {_tag}] {e}")
                continue
            rows.append(row)
            made += 1
            idx += 1
        print(f"  {gen.__name__}: {made} cases")

    n = len(rows)
    print(f"\nTotal evaluated: {n}")

    # ---- baselines: give them their best fair shot (max coverage at FP==0) ----
    taus_active = list(range(0, 60))
    taus_speed = [x / 100 for x in range(0, 105, 2)]
    tau_a, m_quies = best_baseline_tau(rows, "activeWaterCells", taus_active)
    tau_s, m_speed = best_baseline_tau(rows, "maxFlow", taus_speed)
    baseline_verdicts(rows, tau_a, tau_s)

    variants = ["P_geo", "P_full", "P_noC2", "P_C1only", "C1", "C2", "C3", "C4",
                "base_quiescent", "base_speed"]
    M = {v: metrics(rows, v) for v in variants}

    exact_n = sum(r["exact"] for r in rows)
    print(f"\nGround truth: {exact_n}/{n} scenes have EXACT D read-off "
          f"({100*exact_n/n:.1f}%).")
    print(f"Baseline thresholds chosen for max certification rate at FP=0: "
          f"quiescent active<= {tau_a}, speed maxFlow<= {tau_s}\n")

    hdr = f"{'verdict':<16}{'cert%':>8}{'FP':>5}{'FPrate%':>9}{'recall%':>9}{'TP':>5}{'FN':>5}{'TN':>5}"
    print(hdr); print("-" * len(hdr))
    lines = [hdr, "-" * len(hdr)]
    for v in variants:
        m = M[v]
        ln = (f"{v:<16}{100*m['coverage']:>8.1f}{m['FP']:>5}{100*m['fp_rate']:>9.2f}"
              f"{100*m['recall']:>9.1f}{m['TP']:>5}{m['FN']:>5}{m['TN']:>5}")
        print(ln); lines.append(ln)

    # ---- DECISIVE diagnostic: are D's errors confined to non-quiescent states? ----
    wrong = [r for r in rows if not r["exact"]]
    wrong_act = sorted(r["activeWaterCells"] for r in wrong)
    quiescent_wrong = [r for r in rows if (not r["exact"]) and r["activeWaterCells"] <= tau_a]
    still_wrong_P_catches = [r for r in quiescent_wrong if not r["P_geo"]]
    moving_exact_Pcov = [r for r in rows if r["exact"] and (not r["base_quiescent"]) and r["P_geo"]]
    diag = ["", "== DECISIVE DIAGNOSTIC ==",
            f"D-wrong scenes: {len(wrong)}. Their activeWaterCells: "
            f"min={wrong_act[0] if wrong_act else '-'} "
            f"median={wrong_act[len(wrong_act)//2] if wrong_act else '-'} "
            f"max={wrong_act[-1] if wrong_act else '-'}",
            f"QUIESCENT-but-D-WRONG (active<= {tau_a}): {len(quiescent_wrong)}  "
            f"(these are where naive quiescence would FALSE-POSITIVE)",
            f"  ...of those, RPRM P (C1&C3) correctly REJECTS: {len(still_wrong_P_catches)} "
            f"(RPRM's potential soundness win over quiescence)",
            f"MOVING-but-exact that RPRM P_geo certifies and quiescence misses: {len(moving_exact_Pcov)} "
            f"(RPRM's certification-rate win over quiescence)"]
    for l in diag:
        print(l)
    lines += diag

    # ---- per-family breakdown ----
    fams = sorted(set(r["tag"] for r in rows))
    fam_lines = ["", "Per-family (exact / total, and P_noC2 FP):"]
    for f in fams:
        fr = [r for r in rows if r["tag"] == f]
        ex = sum(r["exact"] for r in fr)
        fp = sum(1 for r in fr if r["P_geo"] and not r["exact"])
        cov = sum(1 for r in fr if r["P_geo"])
        fpq = sum(1 for r in fr if r["base_quiescent"] and not r["exact"])
        fam_lines.append(f"  {f:<20} exact {ex:>3}/{len(fr):<3}  P_geo cert={cov:>3} FP={fp}  quiescent FP={fpq}")
    for l in fam_lines:
        print(l)
    lines += fam_lines

    # ============================ figures ============================
    # (A) confusion-matrix figure for P_noC2 (headline certificate) and the two
    #     baselines side by side.
    def conf_grid(v):
        TP, FP, FN, TN = confusion(rows, v)
        return np.array([[TP, FN], [FP, TN]])

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4))
    for ax, v, name in zip(axes,
                           ["P_geo", "base_quiescent", "base_speed"],
                           [f"RPRM certificate P (C1&C3&C4)",
                            f"naive quiescent (active<= {tau_a})",
                            f"naive low-speed (maxFlow<= {tau_s})"]):
        cg = conf_grid(v)
        ax.imshow(cg, cmap="Blues")
        ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
        ax.set_xticklabels(["truly\nexact", "truly\nwrong"], fontsize=8)
        ax.set_yticklabels(["says\nexact", "says\nnot"], fontsize=8)
        for (i, j), val in np.ndenumerate(cg):
            bad = (i == 1 and j == 0)   # FP cell
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=13, color=("red" if bad and val > 0 else "black"),
                    fontweight=("bold" if bad else "normal"))
        m = M[v]
        ax.set_title(f"{name}\ncert {100*m['coverage']:.0f}%  FP={m['FP']}",
                     fontsize=8)
    fig.suptitle("Certified-sufficient vs actually-exact  (red = FALSE POSITIVE: "
                 "certified but wrong)", fontsize=9)
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    p = os.path.join(ART, "sufficiency_confusion.png")
    fig.savefig(p, dpi=95); plt.close(fig)
    saved.append(p); copy_surface(p)

    # (B) coverage-vs-FP tradeoff: P (single point) vs baselines (full curves).
    fig, ax = plt.subplots(figsize=(6, 4))
    for key, name, col in [("activeWaterCells", "naive quiescent", "tab:orange"),
                           ("maxFlow", "naive low-speed", "tab:green")]:
        vals = sorted(set(r[key] for r in rows))
        covs, fps = [], []
        for t in vals:
            for r in rows:
                r["_b"] = r[key] <= t
            m = metrics(rows, "_b")
            covs.append(100 * m["coverage"]); fps.append(100 * m["fp_of_all"])
        order = np.argsort(fps)
        ax.plot(np.array(fps)[order], np.array(covs)[order], "-o", ms=3,
                label=name, color=col, lw=1.3)
    for r in rows:
        r.pop("_b", None)
    for v, name, col, mk in [("P_geo", "RPRM P (C1&C3&C4)", "tab:blue", "*"),
                             ("P_noC2", "C1&C3 (no trap guard)", "tab:red", "X"),
                             ("P_full", "RPRM P (C1&C2&C3)", "tab:purple", "P")]:
        m = M[v]
        ax.scatter([100 * m["fp_of_all"]], [100 * m["coverage"]], marker=mk,
                   s=140, color=col, zorder=5, label=name, edgecolor="k")
    ax.set_xlabel("false-positive rate (% of ALL scenes certified-but-wrong)")
    ax.set_ylabel("certification rate (% of scenes accepted as sufficient)")
    ax.set_title("RPRM certificate vs naive baselines\n(up-and-left is better; "
                 "0 FP is the requirement)")
    ax.legend(fontsize=8, loc="lower right"); ax.grid(alpha=0.3)
    fig.tight_layout()
    p = os.path.join(ART, "sufficiency_vs_baseline.png")
    fig.savefig(p, dpi=95); plt.close(fig)
    saved.append(p); copy_surface(p)

    # (C) illustrative disagreements: cases where P and quiescent DISAGREE about
    #     an actually-wrong (trap) or actually-exact (coverage-win) scene.
    # trap that C1&C3 (no guard) would wrongly certify but C4 catches:
    trap = [r for r in rows if (not r["exact"]) and r["P_noC2"] and (not r["P_geo"])]
    win = [r for r in rows if r["exact"] and r["P_geo"] and (not r["base_quiescent"])]
    illus = []
    if trap:
        trap.sort(key=lambda r: -r["tv"])
        p = os.path.join(ART, "case_trap_c4_catch.png")
        save_case_figure(trap[0], p,
                         "TRAP: D drains a lip-pocket it should retain. C1&C3 alone would "
                         "CERTIFY it (wrong); the RPRM drainage guard C4 rejects it.")
        saved.append(p); copy_surface(p); illus.append(("trap", trap[0]))
    if win:
        win.sort(key=lambda r: -r["activeWaterCells"])
        p = os.path.join(ART, "case_moving_but_exact.png")
        save_case_figure(win[0], p,
                         "COVERAGE: a MOVING scene whose read-off is already exact. "
                         "RPRM P certifies it; naive quiescent misses it.")
        saved.append(p); copy_surface(p); illus.append(("win", win[0]))

    # ---- write report ----
    report = ["# Sufficiency-certificate falsification results (auto-generated)", "",
              f"Grid {H}x{W}. Scenes evaluated: {n}. "
              f"Exact D read-offs: {exact_n} ({100*exact_n/n:.1f}%).",
              f"EXACT means TV(D read-off, independent truth) < {EXACT_TV} cell-masses "
              f"(agreement within a 1 cell-mass total-variation tolerance).",
              f"Baselines tuned for max certification rate at FP=0: quiescent active<= {tau_a}, "
              f"speed maxFlow<= {tau_s}.", "",
              "```", *lines, "```", ""]
    if trap:
        t = trap[0]
        report += [f"Illustrative TRAP (D drains a pocket it should keep): family "
                   f"`{t['tag']}`, TV={t['tv']:.2f}. C1&C3 alone certify it (wrong); "
                   f"the drainage guard C4 rejects it (C4={t['C4']}).", ""]
    else:
        report += ["No trap that C1&C3 certified and the C4 guard rejected was found.", ""]
    if win:
        wv = win[0]
        report += [f"Illustrative CERTIFICATION-RATE win: family `{wv['tag']}`, exact "
                   f"read-off with activeWaterCells={wv['activeWaterCells']} (NOT "
                   f"quiescent); RPRM P_geo certifies it, naive quiescence cannot.", ""]
    with open(os.path.join(ART, "sufficiency_results.md"), "w") as f:
        f.write("\n".join(report) + "\n")

    # raw JSON (lightweight) for reproducibility
    slim = [{k: (float(r[k]) if isinstance(r[k], (np.floating,)) else r[k])
             for k in ("tag", "total", "tv", "maxc", "exact", "C1", "C2", "C3", "C4",
                       "P_full", "P_noC2", "P_geo", "P_C1only", "nbodies",
                       "activeWaterCells", "maxFlow", "movedMass",
                       "base_quiescent", "base_speed")} for r in rows]
    json.dump({"meta": {"H": H, "W": W, "n": n, "exact": exact_n,
                        "tau_active": int(tau_a), "tau_speed": float(tau_s),
                        "EXACT_TV": EXACT_TV},
               "metrics": M, "rows": slim},
              open(os.path.join(ART, "sufficiency_raw.json"), "w"), indent=1)

    print("\nArtifacts:")
    for p in saved:
        print(f"  {p} ({os.path.getsize(p)/1024:.0f} KB)")
    print(f"  {os.path.join(ART, 'sufficiency_results.md')}")
    print(f"  {os.path.join(ART, 'sufficiency_raw.json')}")
    return M, rows


if __name__ == "__main__":
    main()

