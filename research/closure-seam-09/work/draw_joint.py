"""Draw paired-occurrence diagrams, with arrows explicitly distinct from lengths.

Reads the finite receipt and writes joint_pairing.png and joint_pairing.svg.
Existing figure paths are refused. This is a schematic, not a coordinate plot.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=root / "evidence" / "joint.json")
    parser.add_argument("--output-dir", type=Path, default=root / "figures")
    args = parser.parse_args()
    outputs = [args.output_dir / f"joint_pairing.{extension}" for extension in ("png", "svg")]
    for output in outputs:
        if output.exists():
            parser.error(f"refusing to overwrite existing figure: {output}")
    evidence_bytes = args.evidence.read_bytes()
    evidence = json.loads(evidence_bytes)
    if evidence.get("status") != "PASS" or evidence.get("fixed_records_distances") != [0, 2]:
        raise ValueError("expected a passed receipt with fixed-record distances [0, 2]")
    source_path = root / "work" / "check_joint.py"
    if hashlib.sha256(source_path.read_bytes()).hexdigest() != evidence["source_sha256"]:
        raise ValueError("receipt does not bind the current finite verifier")

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10.5,
        "svg.fonttype": "none",
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    })
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.9))
    fig.subplots_adjust(left=0.045, right=0.955, top=0.725, bottom=0.20, wspace=0.20)
    fig.text(0.5, 0.958, "Same side records. Different pairing.", ha="center", va="top",
             fontsize=18, weight="bold", color="#162337")
    fig.text(0.5, 0.882, r"Fixed values on each side: $(0,1)$     |     Readout: $D=\sum_i(x_i-y_{\pi(i)})^2$",
             ha="center", va="top", fontsize=11, color="#37455a")
    colors = ("#4655b8", "#087c83")
    y_positions = (0.67, 0.34)
    for ax, pi, title, formula in zip(
        axes,
        ((0, 1), (1, 0)),
        ("Identity matching", "Crossed matching"),
        (r"$D=(0-0)^2+(1-1)^2=\mathbf{0}$", r"$D=(0-1)^2+(1-0)^2=\mathbf{2}$"),
    ):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title(title, fontsize=13, weight="bold", pad=10, color="#162337")
        ax.text(0.25, 0.90, "Left", ha="center", color="#37455a")
        ax.text(0.75, 0.90, "Right", ha="center", color="#37455a")
        for i, partner in enumerate(pi):
            arrow = FancyArrowPatch(
                (0.25, y_positions[i]), (0.75, y_positions[partner]),
                arrowstyle="-|>", mutation_scale=16, linewidth=2.4,
                color=colors[i], shrinkA=18, shrinkB=20, zorder=1,
            )
            ax.add_patch(arrow)
        for side, xpos, label_x, alignment in (("l", 0.25, 0.13, "right"), ("r", 0.75, 0.87, "left")):
            for i, ypos in enumerate(y_positions):
                ax.scatter([xpos], [ypos], s=760, color="#eff2f7", edgecolors="#637389",
                           linewidths=1.2, zorder=3)
                ax.text(xpos, ypos, str(i), ha="center", va="center", fontsize=12,
                        weight="bold", color="#162337", zorder=4)
                ax.text(label_x, ypos, rf"${side}_{i}$", ha=alignment, va="center",
                        fontsize=12, color="#37455a")
        ax.text(0.5, 0.025, formula, ha="center", va="bottom", fontsize=12, color="#162337")
    fig.text(0.5, 0.103, "Arrows indicate occurrence pairing; their drawn lengths are not distances.",
             ha="center", va="center", fontsize=10.5, color="#37455a")
    fig.text(0.5, 0.060, "Each term uses the difference between the values printed at the paired nodes.",
             ha="center", va="center", fontsize=10.5, color="#37455a")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    description = (
        "Pairing schematic, not a coordinate plot. "
        f"Evidence SHA256: {hashlib.sha256(evidence_bytes).hexdigest()}. "
        f"Drawing source SHA256: {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}."
    )
    fig.savefig(outputs[0], dpi=180, metadata={"Description": description})
    fig.savefig(outputs[1], metadata={"Title": "Same side records, different pairing", "Description": description})
    plt.close(fig)
    for output in outputs:
        print(output.resolve())


if __name__ == "__main__":
    main()
