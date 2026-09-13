"""Figure generation for the broadphase transfer test (headless matplotlib)."""
from __future__ import annotations

import os
import shutil

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import scenes as S
import certificate as C
from sim import contact_set, CONTACT_BAND


def _mirror(paths, store):
    if not store:
        return
    for p in paths:
        try:
            shutil.copy(p, os.path.join(store, os.path.basename(p)))
        except OSError:
            pass


def fig_confusion(results, art):
    methods = ["naive", "pure_ca", "ca_sleeping", "P"]
    labels = ["naive\nquiescence", "pure CA", "CA+sleeping\n(incumbent)", "P\n(RPRM cert)"]
    cert = [100 * results[m]["cert_rate"] for m in methods]
    fp = [100 * results[m]["fp_rate"] for m in methods]
    colors = ["#b0b0b0", "#7aa6d6", "#f0a35e", "#5cb85c"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    bars = ax1.bar(labels, cert, color=colors)
    ax1.set_ylabel("certification rate (%)")
    ax1.set_title("Certification rate at 0-FP settings\n(fraction of island-steps safely skipped)")
    for b, v in zip(bars, cert):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9)
    ax1.set_ylim(0, max(cert) * 1.2 + 5)

    bars2 = ax2.bar(labels, fp, color=colors)
    ax2.set_ylabel("false-positive rate (%)")
    ax2.set_title("False-positive rate\n(certified 'no change' but contact set changed)")
    for b, v in zip(bars2, fp):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.002, f"{v:.3f}", ha="center", fontsize=9)
    ax2.set_ylim(0, max(fp + [0.05]) * 1.4)
    fig.suptitle("Broadphase reuse certificate: confusion summary", fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    p = os.path.join(art, "broadphase_confusion.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def fig_cert_vs_fp(results, curve_naive, curve_cas, taus, tau_naive, tau_cas, art):
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    cn = np.array([[100 * cm["fp_rate"], 100 * cm["cert_rate"]] for _, cm in curve_naive])
    cc = np.array([[100 * cm["fp_rate"], 100 * cm["cert_rate"]] for _, cm in curve_cas])
    ax.plot(cn[:, 0], cn[:, 1], "-", color="#909090", label="naive quiescence (sweep tau)")
    ax.plot(cc[:, 0], cc[:, 1], "-", color="#e08a3c", label="CA+sleeping incumbent (sweep tau)")
    ax.scatter([100 * results["pure_ca"]["fp_rate"]], [100 * results["pure_ca"]["cert_rate"]],
               color="#3b7dd8", s=80, zorder=5, label="pure CA")
    ax.scatter([100 * results["P"]["fp_rate"]], [100 * results["P"]["cert_rate"]],
               color="#2ca02c", s=110, marker="*", zorder=6, label="P (RPRM certificate)")
    ax.axvline(0, color="k", lw=0.8, ls=":")
    ax.set_xlabel("false-positive rate (%)  [decisive: must be ~0]")
    ax.set_ylabel("certification rate (%)")
    ax.set_title("Certification rate vs false-positive rate\n(the operating point at FP=0 is what counts)")
    ax.set_xlim(-0.2, max(3.0, cn[:, 0].max() * 1.05))
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    p = os.path.join(art, "broadphase_cert_vs_fp.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def fig_by_family(results, art):
    pf = results["per_family"]
    fams = sorted(pf.keys())
    x = np.arange(len(fams))
    w = 0.2
    naive = [100 * pf[f]["naive"]["cert_rate"] for f in fams]
    pure = [100 * pf[f]["pure_ca"]["cert_rate"] for f in fams]
    cas = [100 * pf[f]["ca_sleeping"]["cert_rate"] for f in fams]
    P = [100 * pf[f]["P"]["cert_rate"] for f in fams]
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.bar(x - 1.5 * w, naive, w, label="naive", color="#b0b0b0")
    ax.bar(x - 0.5 * w, pure, w, label="pure CA", color="#7aa6d6")
    ax.bar(x + 0.5 * w, cas, w, label="CA+sleeping (incumbent)", color="#f0a35e")
    ax.bar(x + 1.5 * w, P, w, label="P (RPRM cert)", color="#5cb85c")
    ax.set_xticks(x)
    ax.set_xticklabels(fams, rotation=20, ha="right")
    ax.set_ylabel("certification rate (%)")
    ax.set_title("Certification rate by scene family (at 0-FP settings)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    p = os.path.join(art, "broadphase_by_family.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def _find_disagreement(records, tau_cas):
    """Best P-only-correct case: P certifies (no-change truth) while incumbent wakes,
    prefer the one with the largest island speed (most 'moving-but-invariant')."""
    def v_P(r):
        return r["add_ok"] and r["pers_ok"]

    def v_cas(r):
        if not r["add_ok"]:
            return False
        if not r["has_contacts"]:
            return True
        return r["speed_max"] < tau_cas

    cands = [r for r in records if v_P(r) and not v_cas(r) and not r["changed"]]
    if not cands:
        return None
    # prefer a genuinely MOVING, MULTI-body island (invariant contact SET while it
    # moves) -- the clearest illustration; fall back to single-body sliders.
    multi = [r for r in cands if r["n_bodies"] >= 2 and r["speed_max"] > 0.8]
    pool = multi if multi else cands
    pool.sort(key=lambda r: (r["n_bodies"], r["speed_max"]), reverse=True)
    return pool[0]


def fig_disagreement(records, results, tau_cas, seed, n_per_family, art):
    rec = _find_disagreement(records, tau_cas)
    if rec is None:
        return None
    # reproduce the exact scene deterministically
    scene_list = S.generate(n_per_family, seed=seed)
    family, world = scene_list[rec["scene"]]
    for _ in range(rec["step"]):
        world.step()

    isl = set(rec["bodies"])
    cset = contact_set(world)
    fig, ax = plt.subplots(figsize=(7.2, 7.2))
    # walls
    ax.plot([0, world.W, world.W, 0, 0], [0, 0, world.H, world.H, 0], "k-", lw=1.5)
    for i in range(world.n):
        x, y = world.pos[i]
        r = world.radius[i]
        in_isl = i in isl
        col = "#5cb85c" if in_isl else "#cccccc"
        ax.add_patch(Circle((x, y), r, color=col, ec="k", alpha=0.85, zorder=3))
        vx, vy = world.vel[i]
        sp = np.hypot(vx, vy)
        if sp > 0.05:
            ax.arrow(x, y, vx * 0.15, vy * 0.15, head_width=0.12, head_length=0.12,
                     fc="red", ec="red", zorder=4, length_includes_head=True)
    # draw the island's contacts (disk-disk AND wall) -- this is the "contact set"
    wall_pos = {-1: lambda x, y, r: (x, y - r), -2: lambda x, y, r: (x, y + r),
                -3: lambda x, y, r: (x - r, y), -4: lambda x, y, r: (x + r, y)}
    for p in cset:
        a, b = p
        if a in isl or (b >= 0 and b in isl):
            if b >= 0:
                ax.plot([world.pos[a, 0], world.pos[b, 0]],
                        [world.pos[a, 1], world.pos[b, 1]], "b-", lw=2.5, zorder=5)
            else:
                cx, cy = wall_pos[b](world.pos[a, 0], world.pos[a, 1], world.radius[a])
                ax.plot([world.pos[a, 0], cx], [world.pos[a, 1], cy], "b-", lw=2.5, zorder=5)
                ax.scatter([cx], [cy], color="b", s=30, zorder=6)

    speed = rec["speed_max"]
    # bounds view
    xs = world.pos[list(isl), 0]
    ys = world.pos[list(isl), 1]
    pad = 3.0
    ax.set_xlim(max(0, xs.min() - pad), min(world.W, xs.max() + pad))
    ax.set_ylim(max(0, ys.min() - pad), min(world.H, ys.max() + pad))
    ax.set_aspect("equal")
    ax.set_title(
        f"Most convincing disagreement (family={family}, {len(isl)} bodies)\n"
        f"P CERTIFIES this island: it MOVES @ speed={speed:.2f} but its contact SET is invariant;\n"
        f"CA+sleeping WAKES it (absolute speed > tau={tau_cas:.2f}); truth = NO change  =>  P correct, incumbent wasteful",
        fontsize=9.5)
    ax.text(0.02, 0.02, "green = certified island   blue = its contacts   red = velocity",
            transform=ax.transAxes, fontsize=8, va="bottom")
    fig.tight_layout()
    p = os.path.join(art, "broadphase_disagreement.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


def make_all(records, results, curve_naive, curve_cas, taus, tau_naive, tau_cas,
             art, store, seed, n_per_family):
    paths = []
    paths.append(fig_confusion(results, art))
    paths.append(fig_cert_vs_fp(results, curve_naive, curve_cas, taus, tau_naive, tau_cas, art))
    paths.append(fig_by_family(results, art))
    d = fig_disagreement(records, results, tau_cas, seed, n_per_family, art)
    if d:
        paths.append(d)
    _mirror([p for p in paths if p], store)
    print("figures written:")
    for p in paths:
        if p:
            print("  ", p)
    return paths
