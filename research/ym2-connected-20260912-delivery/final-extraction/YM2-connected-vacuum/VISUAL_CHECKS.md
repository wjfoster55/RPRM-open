# Scientific figure: joint orientation and actual-vacuum witness

Completed and visually inspected on 12 September 2026, by 18:47:24 UTC.

## Artifacts and reproduction

- `draw_connected_joint.py`: self-contained plotting source, using the
  already-installed Matplotlib 3.10.8 and Python standard library.
- `connected_joint.png`: 3200 × 1700 pixels, 200 dpi, 16 × 8.5 inches.
- `connected_joint.svg`: editable vector output; 1152 × 612 pt,
  `viewBox="0 0 1152 612"`. The XML contains 53 text elements. The source
  sets `svg.fonttype="none"`, preserving editable text rather than turning
  all lettering into paths. Font: DejaVu Sans.

From `C:/github/RPRM-open/`, reproduce with:

```powershell
python -I -B research/ym2_connected_vacuum/draw_connected_joint.py
```

The script writes only its adjacent PNG and SVG. No package installation,
eigenfunction solve, simulation, old-checker rerun, or source-proof mutation
was performed for this figure.

## Exact claim labels

**Panel A — shared-edge source.** Two adjacent square plaquettes have seven
link occurrences and six vertices. The common edge is highlighted. The
labels retain `a=Sc(U)`, `b=Sc(V)`, `w=Sc(UV)` and `T(ab)=13ab-w` in the
declared source loop-word convention. The topology schematic supplies no
new choice of directed source link variables or boundary conditions.

**Panel B — configuration geometry and Taylor coefficients.** The depicted
quaternion vector representatives have `u=(1,0)`, `v=(3/5,4/5)` and
`v=(-3/5,4/5)` in their displayed plane. Both have `a=b=0`; their dot
products give `w=-3/5` and `w=+3/5`. The exact identity is
`w=-u.v=-cos(theta)`. Their order-`r^2` log-density coefficients differ by
`(2/351)(6/5)=4/585`. The panel explicitly labels this as geometry and
Taylor coefficients. It does not assert an actual pointwise vacuum-density
difference from an L2 remainder.

**Panel C — actual-vacuum integral witness.** The shaded enclosure displays

```text
J(r) = integral (w-ab) log(rho_r) dmu,
|J(r)/r^2 - 1/936| < 3r,     0 < r <= 1/3000.
```

The horizontal coordinate is `x=3000r`; the vertical coordinate is
`1000 J(r)/r^2`. Therefore the boundary lines are exactly
`1000/936 - x` and `1000/936 + x`. The script draws this affine envelope
using only its two endpoints. No vacuum values are sampled. The dashed
horizontal line is explicitly labeled as the second-order coefficient.
The open point at `x=0` represents the limiting coefficient; the caption
explicitly excludes zero from the divided witness. The open point on the
lower boundary at `x=1` marks a strict lower bound, while the coupling
endpoint itself remains admitted.

The lower boundary stays positive through the endpoint:
`1/936-1/1000=1/14625=4/58500>0`. The figure states the actual-vacuum
conclusion `J(r)>(4/58500)r^2>0`, which excludes a density measurable in
`(a,b)` alone on this interval. The footer labels the picture an analytic
bound and confines the result to the stated graph and coupling interval.
It does not claim a larger-graph or continuum result.

## Visual inspection

The PNG was opened with `view_image`. The first render exposed an overlap
between the horizontal-axis label and the interval caption. The plot was
raised and rendered again; the final PNG was opened and inspected again.
All panel titles, equations, graph labels, vector arrows, axis ticks,
interval labels, and the positive endpoint margin are visible without
overlap or clipping. The displayed inspection preview was resized by the
viewer from 3200 × 1700 to 2048 × 1088; the delivered PNG retains its full
dimensions. The SVG was generated from the same figure and its XML was
checked for size and editable text; it was not separately rasterized.

## Inspected byte identities

SHA-256 values were read at 18:47:24 UTC on 12 September 2026. The proof
files were read for the exact conventions; these hashes identify that source
snapshot and do not themselves prove the mathematics.

| File | SHA-256 |
|---|---|
| `draw_connected_joint.py` | `122f84b60278d6de78679231a58dd54a82be4a309d65c7242da637c9b6512bf6` |
| `connected_joint.png` | `ab3742aba7a1f75a59c00c3e0097c75638678c3276fd3762235d7d1a262e4c5b` |
| `connected_joint.svg` | `a1926116ce1b657e2ee610a52d0022ee5b4a3dd62b5256fc067097bb00db6502` |
| `VACUUM_SEPARATING_WITNESS.md` | `b9137decf54e233136c868f601af7d986eadc5dbe3907b74d4dca9dafcc66884` |
| `CONNECTED_VACUUM.md` | `9923cf495cb7b90d041569afd28805f7f9ac3b9c14100d0e6ff2173c4333c7ab` |
