"""Render the fixed-graph analytic witness as a static scientific figure.

The envelope is drawn from its exact affine formulas, using its two
endpoints. It contains no numerical eigenfunction, sampled vacuum values,
or simulation. SVG text remains editable (svg.fonttype='none').

Run: python -I -B draw_connected_joint.py
"""

from fractions import Fraction
from pathlib import Path
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parent
INK = "#14293C"
MUTED = "#516577"
BLUE = "#2476AD"
TEAL = "#087F8C"
GOLD = "#BB690A"
LIGHT_BLUE = "#E8F2FA"
LIGHT_GOLD = "#FCF0DE"
GRID = "#DCE4EB"
BACKGROUND = "#FCFDFE"


def arrow(ax, start, end, color, width=2.3, scale=13):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>",
                               mutation_scale=scale, lw=width,
                               color=color, shrinkA=0, shrinkB=0))


def render():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "none",
        "svg.hashsalt": "ym2-connected-joint-2026-09-12",
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": INK,
    })
    coefficient = Fraction(1, 936)
    radius_at_endpoint = Fraction(1, 1000)
    margin = coefficient - radius_at_endpoint
    assert margin == Fraction(4, 58500) and margin > 0
    assert Fraction(2, 351) * Fraction(6, 5) == Fraction(4, 585)

    fig = plt.figure(figsize=(16, 8.5), facecolor=BACKGROUND)
    fig.text(.045, .945, "The two-plaquette vacuum retains a joint orientation",
             fontsize=23, weight="bold")
    fig.text(.045, .903,
             r"Open two-square $SU(2)$ source  |  $r=\beta/(\alpha\hbar^2)$  |  "
             "Written theorem on a fixed graph",
             fontsize=12.4, color=MUTED)

    # Panel headings and separators use figure coordinates for stable layout.
    for x, label, title in [(.045, "A", "A shared link couples two loops"),
                            (.347, "B", "Same traces, different orientation"),
                            (.666, "C", "An actual-vacuum witness")]:
        fig.text(x, .830, label, color=TEAL, fontsize=17, weight="bold")
        fig.text(x + .023, .830, title, fontsize=12.1, weight="bold")
    for x in [.328, .642]:
        fig.add_artist(Line2D([x, x], [.270, .845], transform=fig.transFigure,
                             color=GRID, linewidth=1))

    # A: topology of the accepted seven-edge graph. No edge orientation is
    # inferred from this schematic; U,V use the source loop-word convention.
    graph = fig.add_axes([.053, .43, .255, .34])
    graph.set_aspect("equal")
    graph.set_xlim(-.18, 2.18)
    graph.set_ylim(-.23, 1.35)
    graph.axis("off")
    graph.add_patch(Rectangle((0, 0), 1, 1, facecolor=LIGHT_BLUE, edgecolor="none"))
    graph.add_patch(Rectangle((1, 0), 1, 1, facecolor=LIGHT_GOLD, edgecolor="none"))
    for start, end in [((0, 0), (1, 0)), ((1, 0), (2, 0)),
                       ((0, 1), (1, 1)), ((1, 1), (2, 1)),
                       ((0, 0), (0, 1)), ((2, 0), (2, 1))]:
        graph.plot([start[0], end[0]], [start[1], end[1]], color=INK,
                   lw=2.8, solid_capstyle="round")
    graph.plot([1, 1], [0, 1], color=TEAL, lw=6.0, solid_capstyle="round")
    for x in [0, 1, 2]:
        for y in [0, 1]:
            graph.plot(x, y, "o", color=INK, ms=5.5)
    graph.text(.5, .61, r"$U$", color=BLUE, fontsize=21, ha="center")
    graph.text(1.5, .61, r"$V$", color=GOLD, fontsize=21, ha="center")
    graph.text(.5, .35, r"$a=\mathrm{Sc}(U)$", fontsize=11.5, ha="center")
    graph.text(1.5, .35, r"$b=\mathrm{Sc}(V)$", fontsize=11.5, ha="center")
    graph.annotate("shared link", xy=(1, .96), xytext=(1, 1.22),
                   ha="center", color=TEAL, fontsize=11,
                   arrowprops={"arrowstyle": "-", "color": TEAL, "lw": 1.4})
    graph.text(1, -.21, r"Outer-loop trace: $w=\mathrm{Sc}(UV)$",
               ha="center", fontsize=11.7)
    fig.text(.055, .375, "7 link occurrences  •  6 vertices", fontsize=11.3, color=MUTED)
    fig.text(.055, .330, r"$T(ab)=13ab-w$", fontsize=18, color=TEAL)
    fig.text(.055, .287, "The kinetic operation retains the joint trace.",
             fontsize=10.9, color=MUTED)

    # B: representatives of two exact configuration fibers. These are
    # quaternion-vector directions, not physical positions or vacuum values.
    fig.text(.357, .770, r"Unit quaternions: $U=(0,\mathbf{u}),\;V=(0,\mathbf{v})$",
             fontsize=11.4)
    fig.text(.357, .732, r"Both examples have $a=b=0$ and $|\mathbf{u}|=|\mathbf{v}|=1$.",
             fontsize=10.8, color=MUTED)
    for left, cosine, w_label in [(.353, .6, r"$w=-3/5$"),
                                   (.501, -.6, r"$w=+3/5$")]:
        pair = fig.add_axes([left, .453, .131, .241])
        pair.set_aspect("equal")
        pair.set_xlim(-1.32, 1.42)
        pair.set_ylim(-.45, 1.44)
        pair.axis("off")
        pair.add_patch(Arc((0, 0), 2, 2, theta1=0, theta2=180,
                           color=GRID, lw=1.2, linestyle=(0, (3, 3))))
        arrow(pair, (0, 0), (1, 0), BLUE)
        arrow(pair, (0, 0), (cosine, .8), GOLD)
        theta = math.degrees(math.acos(cosine))
        pair.add_patch(Arc((0, 0), .68, .68, theta1=0, theta2=theta,
                           lw=1.2, color=MUTED))
        theta_mid = math.radians(theta / 2)
        pair.text(.50 * math.cos(theta_mid), .50 * math.sin(theta_mid),
                  r"$\theta$", fontsize=11, ha="center", va="center")
        pair.text(1.13, -.06, r"$\mathbf{u}$", color=BLUE, fontsize=13)
        pair.text(cosine, 1.03, r"$\mathbf{v}$", color=GOLD, fontsize=13, ha="center")
        pair.plot(0, 0, "o", ms=3.5, color=INK)
        pair.text(0, -.38, w_label, fontsize=15.5, ha="center")
    fig.text(.494, .440, r"$w=-\mathbf{u}\cdot\mathbf{v}=-\cos\theta$",
             fontsize=15.5, ha="center")
    fig.text(.357, .378, r"Order-$r^2$ log-density coefficients differ by $4/585$.",
             fontsize=10.7)
    fig.text(.357, .338, "Exact geometry and Taylor coefficients", fontsize=11.3,
             color=TEAL, weight="bold")
    fig.text(.357, .294, "The actual-vacuum conclusion uses the integral in C.",
             fontsize=10.5, color=MUTED)

    # C: the envelope is affine in x=3000r. Only its two exact endpoint
    # values are needed to render the full polygon and both boundary lines.
    ax = fig.add_axes([.710, .450, .245, .316])
    center = float(1000 * coefficient)
    lower = [center, float(1000 * margin)]
    upper = [center, float(1000 * (coefficient + radius_at_endpoint))]
    ax.set_facecolor(BACKGROUND)
    ax.fill_between([0, 1], lower, upper, color=TEAL, alpha=.13, zorder=2)
    ax.plot([0, 1], lower, color=TEAL, linewidth=1.8, zorder=3)
    ax.plot([0, 1], upper, color=TEAL, linewidth=1.8, zorder=3)
    ax.axhline(center, color=GOLD, linestyle=(0, (5, 3)), linewidth=1.5, zorder=3)
    ax.axhline(0, color=INK, linewidth=1.1, zorder=3)
    ax.plot(0, center, marker="o", markerfacecolor=BACKGROUND,
            markeredgecolor=TEAL, markersize=6, zorder=5, clip_on=False)
    ax.plot(1, lower[-1], marker="o", markerfacecolor=BACKGROUND,
            markeredgecolor=TEAL, markersize=5.3, zorder=5)
    ax.set_xlim(0, 1.015)
    ax.set_ylim(-.13, 2.2)
    ax.set_xticks([0, .25, .5, .75, 1], labels=["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([0, .5, 1, 1.5, 2])
    ax.tick_params(labelsize=10, length=3)
    ax.grid(axis="y", color=GRID, linewidth=.75, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.set_xlabel(r"$x=3000r$", fontsize=12, labelpad=7)
    ax.set_ylabel(r"$10^3 J(r)/r^2$", fontsize=12, labelpad=5)
    ax.text(.51, 1.83, "Proved enclosure", color=TEAL, fontsize=11,
            ha="center", transform=ax.transData)
    ax.text(.31, center + .07, r"$1/936$ coefficient", color=GOLD, fontsize=10.3,
            transform=ax.transData)
    ax.annotate("positive lower margin", xy=(1, lower[-1]), xytext=(.19, .26),
                fontsize=9.3, color=TEAL,
                arrowprops={"arrowstyle": "->", "color": TEAL, "lw": 1})
    fig.text(.710, .784, r"$\left|J(r)/r^2-1/936\right|<3r$", fontsize=13)
    fig.text(.710, .358, r"$0<r\leq1/3000$;  $x=0$ shows the limit only.",
             fontsize=10.5, color=MUTED)
    fig.text(.672, .315, r"$J(r)=\int (w-ab)\log\rho_r\,d\mu$", fontsize=15)
    fig.text(.672, .272, r"$J(r)>(4/58500)r^2>0$", fontsize=16,
             color=TEAL, weight="bold")

    # A single conclusion and a compact provenance/scope footer.
    fig.add_artist(Line2D([.045, .955], [.229, .229], transform=fig.transFigure,
                         color=GRID, linewidth=1))
    fig.text(.045, .174,
             r"The actual vacuum density $\rho_r$ cannot be a function of $(a,b)$ alone.",
             fontsize=17, weight="bold")
    fig.text(.045, .125,
             "Panel C is an analytic bound, not a simulation or a plotted vacuum solution. "
             "The theorem concerns the stated graph and coupling interval.",
             fontsize=11.1, color=MUTED)
    fig.text(.045, .077,
             "Source: VACUUM_SEPARATING_WITNESS.md, W1–W9; CONNECTED_VACUUM.md, CV7–CV11.  "
             "12 September 2026",
             fontsize=9.6, color=MUTED)

    title = "The two-plaquette vacuum retains a joint orientation"
    description = (
        "Three-panel scientific explanation of the accepted fixed-graph SU(2) "
        "vacuum witness. C depicts the rigorous affine envelope 1/936 +/- 3r "
        "for J(r)/r^2 on 0<r<=1/3000, not simulated vacuum values. "
        "B depicts exact configuration geometry and second-order coefficients."
    )
    fig.savefig(ROOT / "connected_joint.png", dpi=200, facecolor=BACKGROUND,
                metadata={"Title": title, "Description": description})
    fig.savefig(ROOT / "connected_joint.svg", facecolor=BACKGROUND,
                metadata={"Title": title, "Description": description,
                          "Date": "2026-09-12"})
    plt.close(fig)
    print("Rendered connected_joint.png (3200 x 1700) and editable connected_joint.svg")


if __name__ == "__main__":
    render()
