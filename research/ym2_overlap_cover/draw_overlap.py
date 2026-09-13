"""Explanatory diagram and plots of proved bounds; not simulation data."""
from itertools import product
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                     "svg.fonttype": "none", "axes.spines.top": False,
                     "axes.spines.right": False})
fig = plt.figure(figsize=(16, 8), facecolor="#f5f3ee")
fig.text(.045, .948, "Overlap can strengthen a bound when the shared field stays joint",
         fontsize=22, weight="bold", color="#172c36")
fig.text(.045, .909, "Three groups of the SAME cubic field • colored links are varied jointly • gray links stay outside",
         fontsize=12.5, color="#4d626a")
colors = ["#c87920", "#2479b9", "#8a60bd"]
vertices = list(product(range(2), repeat=3))

def position(v):
    x, y, z = v
    return x + .52*y, z + .35*y

for col, omitted in enumerate([2, 1, 0]):
    ax = fig.add_axes([.055+.318*col, .495, .26, .355])
    ax.set_facecolor("#f5f3ee")
    for v in vertices:
        for k in range(3):
            if v[k] == 0:
                u = list(v); u[k] = 1
                x0, y0 = position(v); x1, y1 = position(u)
                ax.plot([x0, x1], [y0, y1], color="#bfc5c6" if k == omitted else colors[k],
                        lw=2 if k == omitted else 4.5,
                        ls=(0,(3,3)) if k == omitted else "-", solid_capstyle="round")
    for v in vertices:
        ax.plot(*position(v), "o", color="#172c36", ms=4)
    ax.set_xlim(-.12, 1.72); ax.set_ylim(-.3, 1.62)
    ax.set_aspect("equal"); ax.axis("off")
    name = ["x + y", "x + z", "y + z"][col]
    ax.text(.76, 1.58, name + " links", ha="center", fontsize=16, weight="bold")
    ax.text(.76, -.17, "weight ½ · omitted " + "xyz"[omitted] + " links form a forest",
            ha="center", fontsize=10.5, color="#4d626a")

fig.text(.06, .438, "Energy: each link occurs twice × ½ = 1 charge",
         fontsize=15, color="#172c36", weight="bold")
fig.text(.06, .400, "Physical variance: three full residuals × ½ = 1.5 checks",
         fontsize=15, color="#14766a", weight="bold")
fig.text(.06, .325, "Why the gray links matter", fontsize=13, weight="bold", color="#172c36")
fig.text(.06, .290, "They contain no closed loop. Under the gauge constraint,",
         fontsize=12, color="#4d626a")
fig.text(.06, .258, "a physical observable depending only on those links is constant.",
         fontsize=12, color="#4d626a")
fig.text(.06, .212, "Each colored group therefore removes the whole centered",
         fontsize=12, color="#4d626a")
fig.text(.06, .180, "conditional mean. The same energy pays for all three checks.",
         fontsize=12, color="#4d626a")
fig.text(.06, .114, "This is a cover of variables, not a deformation of physical space.",
         fontsize=11, color="#4d626a", style="italic")

ax = fig.add_axes([.655, .15, .30, .285], facecolor="#f5f3ee")
x = np.linspace(0, 1, 401)
y = 9/16*(1-np.sqrt(1-x))
old = 1.5*(1-4*y/3)*np.exp(-8*y/3)
ax.plot(x, 1.5*old, color="#14766a", lw=2.8, label="new physical bound")
ax.plot(x, old, color="#84939a", lw=2, ls="--", label="previous bound")
ax.scatter([1,1], [1.5*old[-1],old[-1]], c=["#14766a","#84939a"], s=26, zorder=5)
ax.set_ylim(0, 2.48); ax.set_xlim(0,1)
ax.set_ylabel("gap bound / electric energy unit", fontsize=10)
ax.set_xlabel("coupling r / proved endpoint (9/512)", fontsize=10)
ax.tick_params(labelsize=9)
ax.grid(alpha=.17)
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.set_title("3D: a 50% stronger certificate, same interval", fontsize=11, pad=9)
fig.text(.655, .075, "Curves are the proved lower bounds, not measured gaps.",
         fontsize=10, color="#4d626a")
fig.savefig(HERE/"overlap_cover.png", dpi=200, facecolor=fig.get_facecolor())
fig.savefig(HERE/"overlap_cover.svg", facecolor=fig.get_facecolor())
plt.close(fig)
