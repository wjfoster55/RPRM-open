"""Build the four finite explanatory figures; matplotlib is an optional build dependency.

The distributed SVG/PNG assets need no plotting runtime. Every admitted case
in the displayed small carrier is shown; these illustrations are not test receipts.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
INK, BLUE, RED, LIGHT = "#142d3a", "#176b83", "#ac4c38", "#d5dde1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "text.color": INK, "axes.labelcolor": INK,
                     "svg.fonttype": "none", "svg.hashsalt": "rprm-figures-v1"})


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight", metadata={"Creator": "RPRM", "Date": None})
    svg = OUT / (name + ".svg")
    svg.write_bytes(svg.read_bytes().replace(b"\r\n", b"\n"))
    fig.savefig(OUT / (name + ".png"), bbox_inches="tight", dpi=200, metadata={"Software": "RPRM"})
    plt.close(fig)


def box(ax, x, y, text, width=1.6, height=.6, color=BLUE):
    ax.add_patch(FancyBboxPatch((x-width/2, y-height/2), width, height,
                               boxstyle="round,pad=0.04", facecolor="white", edgecolor=color, linewidth=1.3))
    ax.text(x, y, text, ha="center", va="center", fontsize=9)


def arrow(ax, a, b, label=None, color=BLUE):
    ax.annotate("", xy=b, xytext=a, arrowprops={"arrowstyle": "->", "color": color, "lw": 1.4})
    if label:
        ax.text((a[0]+b[0])/2, (a[1]+b[1])/2+.13, label, ha="center", va="bottom", fontsize=8)


def aperture():
    fig, axes = plt.subplots(1, 2, figsize=(6.1, 2.6), layout="constrained")
    for index, ax in enumerate(axes):
        for a in range(5):
            for b in range(5):
                lawful = a+b == 4
                ax.scatter(a, b, c=BLUE if lawful else RED if index else LIGHT,
                           marker="o" if lawful else "x", s=42 if lawful else 25, linewidths=1)
        ax.set(xlim=(-.5,4.5), ylim=(-.5,4.5), xticks=range(5), yticks=range(5), xlabel="a", ylabel="b")
        ax.set_aspect("equal"); ax.spines[["top","right"]].set_visible(False)
        ax.set_title("Complete fiber: a + b = 4" if index == 0 else "Product of marginals", fontsize=10)
        ax.text(.5,-.27,"5 lawful joint pairs" if index==0 else "5 lawful + 20 spurious pairs",
                transform=ax.transAxes, ha="center", fontsize=9, color=BLUE if index==0 else RED)
    save(fig, "01-joint-aperture")


def future():
    fig, ax = plt.subplots(figsize=(6.1, 2.35)); ax.set(xlim=(0,7), ylim=(0,3)); ax.axis("off")
    box(ax,1.1,2.1,"p\nnow: 0"); box(ax,1.1,.75,"q\nnow: 0")
    box(ax,4.2,2.1,"r\nafter a: 1"); box(ax,4.2,.75,"q\nafter a: 0")
    arrow(ax,(1.95,2.1),(3.35,2.1),"action a"); arrow(ax,(1.95,.75),(3.35,.75),"action a")
    ax.text(6,1.45,"Same present\n\nDifferent future",ha="center",va="center",fontsize=10)
    ax.text(3.4,.1,"Merging p and q preserves the present but cannot preserve this update.",ha="center",fontsize=9)
    save(fig,"02-future-distinction")


def parity():
    fig, axes=plt.subplots(1,2,figsize=(6.1,2.1)); fig.subplots_adjust(wspace=.15)
    for ax in axes: ax.set(xlim=(0,5),ylim=(0,2.6)); ax.axis("off")
    for i,value in enumerate(("1","0","1","?")):
        box(axes[0],.6+i*1.15,1.45,value,width=.72,height=.65,color=RED if value=="?" else BLUE)
    axes[0].set_title("A labeled erasure",fontsize=10)
    axes[0].text(2.4,.55,"Even parity forces the missing bit to 0.",ha="center",fontsize=8.5)
    for i,value in enumerate(("1","0","1","1")):
        box(axes[1],.6+i*1.15,1.45,value,width=.72,height=.65,color=RED)
    axes[1].set_title("An unknown changed position",fontsize=10)
    axes[1].text(2.4,.55,"Odd parity detects an error.\nIt does not identify which bit changed.",ha="center",va="center",fontsize=8.5)
    save(fig,"03-erasure-and-error")


def descriptions():
    fig, ax=plt.subplots(figsize=(6.1,2.4)); ax.set(xlim=(0,8),ylim=(0,3.1)); ax.axis("off")
    box(ax,1.35,1.7,"Integer\n1000",width=1.6,height=.85)
    box(ax,4.45,2.3,"Decimal word\n4 positions: 1, 0, 0, 0",width=3,height=.7)
    box(ax,4.45,1.05,"Operational path\n1 -> 10 -> 100 -> 1000",width=3,height=.7)
    arrow(ax,(2.2,1.95),(2.9,2.3),"format"); arrow(ax,(2.2,1.45),(2.9,1.05),"steps")
    ax.text(7.05,1.7,"Geometric\ndimension?\n\nNeeds a\nseparate map",ha="center",va="center",color=RED,fontsize=9)
    ax.text(4,.15,"Value, word length, operation count and geometric dimension are typed separately.",ha="center",fontsize=8.5)
    save(fig,"04-number-descriptions")


if __name__ == "__main__":
    aperture(); future(); parity(); descriptions()
