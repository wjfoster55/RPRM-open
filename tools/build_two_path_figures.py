"""Render the two analytic plates from MANIFESTO.md, section III.9.

Matplotlib and NumPy are optional plotting dependencies. No data are acquired.
Every run owns a fresh .artifacts/two-path-figures/<build-id> directory.
"""

from pathlib import Path
import hashlib
import json
import argparse
from datetime import datetime, timezone
import platform
import re
import uuid

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PHASES = np.array([0, np.pi/2, np.pi, 3*np.pi/2])
ROWS = (
    (1, r"$\gamma=1$", "Identical markers", [1, .5, 0, .5]),
    (0, r"$\gamma=0$", "Orthogonal markers", [.5, .5, .5, .5]),
    (-1, r"$\gamma=-1$", "Opposite relative phase", [0, .5, 1, .5]),
    (1j, r"$\gamma=i$", "Quarter-turn relative phase", [.5, 0, .5, 1]),
    (.6, r"$\gamma=3/5$", "Partial distinguishability", [.8, .5, .2, .5]),
    (.6+.8j, r"$\gamma=(3+4i)/5$", "Extrema between sample settings", [.8, .1, .2, .9]),
)
NAVY, AMBER, INK = "#17485A", "#B96724", "#202B32"


def setup():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8,
        "axes.titlesize": 9, "axes.labelsize": 8,
        "xtick.labelsize": 7, "ytick.labelsize": 7,
        "text.color": INK, "axes.labelcolor": INK,
        "axes.edgecolor": "#A8B0B4", "xtick.color": INK, "ytick.color": INK,
        "axes.spines.top": False, "axes.spines.right": False,
        "savefig.facecolor": "white", "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })


def decorate(ax):
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-.04, 1.04)
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
                  ["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    ax.set_yticks([0, .5, 1], ["0", "1/2", "1"])
    ax.grid(axis="y", color="#DDE2E5", lw=.6, zorder=0)
    ax.set_xlabel(r"Relative phase $\theta$")
    ax.set_ylabel(r"$P_{\theta}(+)$")


def save(fig, stem, output_dir):
    for suffix in ("svg", "pdf", "png"):
        fig.savefig(output_dir / (stem + "." + suffix), dpi=220, bbox_inches="tight", pad_inches=.1)
    plt.close(fig)


def draw_figures(output_dir):
    setup()
    phase = np.linspace(0, 2*np.pi, 601)
    fig, axes = plt.subplots(2, 3, figsize=(7.1, 4.65), layout="constrained")
    for ax, (gamma, label, description, expected) in zip(axes.flat, ROWS):
        curve = .5 + np.real(np.exp(1j*phase) * gamma)/2
        sample = .5 + np.real(np.exp(1j*PHASES) * gamma)/2
        if not np.allclose(sample, expected, rtol=0, atol=1e-14):
            raise ValueError("Plot convention differs from the written exact control table.")
        ax.plot(phase, curve, color=NAVY, lw=1.6)
        ax.scatter(PHASES, expected, color=AMBER, s=18, zorder=3, edgecolors="white", linewidths=.4)
        decorate(ax)
        ax.set_title(label + "\n" + description, loc="left", pad=7)
    save(fig, "two_path_complete_controls", output_dir)

    fig, ax = plt.subplots(figsize=(6.0, 2.45), layout="constrained")
    ax.plot(phase, (1+np.cos(phase))/2, color=NAVY, lw=1.6,
            label=r"Selected $r=+1$, weight $1/2$")
    ax.plot(phase, (1-np.cos(phase))/2, color=AMBER, lw=1.6, ls="--",
            label=r"Selected $r=-1$, weight $1/2$")
    ax.axhline(.5, color=INK, lw=1.6, ls=":", label="Weighted marginal")
    decorate(ax)
    ax.set_title("Opposite selected fringes; flat unconditional output", loc="left", pad=9)
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.33), ncol=3,
              frameon=False, fontsize=7, handlelength=2.2)
    save(fig, "two_path_eraser_weights", output_dir)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_HEADING = b"### III.9. Two-path interference and retained coherence"
STEMS = ("two_path_complete_controls", "two_path_eraser_weights")
SUFFIXES = ("svg", "pdf", "png")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def source_section(source):
    """Return the exact III.9 bytes, including its heading and trailing blank lines."""
    lines = source.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.rstrip(b"\r\n") == SOURCE_HEADING]
    if len(starts) != 1:
        raise ValueError("MANIFESTO.md must contain exactly one expected III.9 heading.")
    start = starts[0]
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith((b"# ", b"## ", b"### "))), len(lines))
    return b"".join(lines[start:end])


def write_receipt(path, record):
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8],
        help="New directory name: 1-64 ASCII letters, digits, underscores or hyphens; start with a letter or digit.",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", args.build_id):
        parser.error("Invalid --build-id; use 1-64 ASCII letters, digits, underscores or hyphens.")
    artifact_root = ROOT / ".artifacts" / "two-path-figures"
    output_dir = artifact_root / args.build_id
    # Resolve existing ancestors as well, so a redirected .artifacts cannot escape.
    if not artifact_root.resolve().is_relative_to(ROOT) or not output_dir.resolve().is_relative_to(artifact_root.resolve()):
        parser.error("Output directory resolves outside the repository artifact area.")
    source_path = ROOT / "MANIFESTO.md"
    generator_path = Path(__file__).resolve()
    source = source_path.read_bytes()
    generator = generator_path.read_bytes()
    section = source_section(source)
    try:
        output_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error("Build directory already exists; choose a new --build-id.")
    receipt_path = output_dir / "TWO_PATH_FIGURES.json"
    record = {
        "status": "BUILDING_PENDING_VISUAL_REVIEW",
        "role": "Analytic illustration of supplied conventional quantum probabilities; no measured or simulated counts.",
        "mathematical_source": "MANIFESTO.md#iii9-two-path-interference-and-retained-coherence",
        "source_sha256": sha256(source),
        "source_section": SOURCE_HEADING.decode("ascii"),
        "source_section_sha256": sha256(section),
        "source_section_byte_rule": "Exact heading through the byte before the next heading of level three or higher, including trailing blank lines.",
        "generator": "tools/build_two_path_figures.py",
        "generator_sha256": sha256(generator),
        "build_id": args.build_id,
        "output_directory": output_dir.relative_to(ROOT).as_posix(),
        "rendering_only_check": "Four plotted phase markers in every row must match the independently written rational control table to absolute floating plotting tolerance 1e-14. This is not an exact-arithmetic proof.",
        "matplotlib": matplotlib.__version__,
        "numpy": np.__version__,
        "python": platform.python_version(),
        "final_page_layout_verified": False,
        "visual_review_performed": False,
    }
    write_receipt(receipt_path, record)
    try:
        draw_figures(output_dir)
        if source_path.read_bytes() != source or generator_path.read_bytes() != generator:
            raise RuntimeError("Bound manuscript or generator bytes changed during rendering.")
        outputs = [output_dir / (stem + "." + suffix) for stem in STEMS for suffix in SUFFIXES]
        record.update({
            "status": "GENERATED_PENDING_VISUAL_REVIEW",
            "all_six_source_rows_included": True,
            "rendering_only_check_passed": True,
            "output_sha256": {path.name: sha256(path.read_bytes()) for path in outputs},
        })
        write_receipt(receipt_path, record)
    except Exception as exc:
        record.update({"status": "FAILED", "error": str(exc)})
        write_receipt(receipt_path, record)
        raise
    print("Two analytic plates, each in SVG/PDF/PNG; pending visual review.")
    print(output_dir)


if __name__ == "__main__":
    main()

