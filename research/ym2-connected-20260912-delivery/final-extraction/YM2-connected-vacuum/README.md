# YM2: connected vacuum continuation

Research packet dated 12 September 2026. Publication remains on hold.
Start with [the explanation for William](RETURN_TO_WILLIAM.md).

**Checked result:** the actual interacting two-cell SU(2) vacuum is not a
function of the two separate plaquette traces alone for 0<r<=1/3000,
where r=beta/(alpha hbar^2). A signed integral witness detects the missing
joint orientation with an explicit bound on its entire remainder.

| Readout | Result and evidence |
|---|---|
| First two vacuum coefficients and energy remainder | [Written analytic proof and exact polynomial checks](CONNECTED_VACUUM.md) |
| Actual vacuum dependence on the missing outer-loop trace | [Uniform separating witness](VACUUM_SEPARATING_WITNESS.md) |
| Adjacent versus edge-disjoint support | Exact second-order cancellation in CONNECTED_VACUUM.md; no all-order truncation claim |
| Local conditional response on a graph family | [Finite-head bound and explicit missing remainder port](NEXT_CONDITIONAL_PORTS.md) |
| Help from the running P=NP and BSD tasks | [PNP audit](CROSS_PNP.md), [BSD audit](CROSS_BSD.md), [later source update](CROSS_SOURCE_UPDATE.md) |
| Continuum mass gap | OPEN; no new continuum field or improved gap theorem is claimed |

The full seven-link compact source, six vertex gauges, inherited quantum
domain and all-spin free spectrum are retained. No spin cutoff, numerical
eigensolver or large simulation is used. Earlier YM1/YM2 suites are accepted
starting evidence and are not rerun. Finite coordinates of a quotient do
not imply a finite-dimensional function algebra or a complete solved spectrum.

## Replay

Extract the ZIP into any local directory. From its YM2-connected-vacuum
folder, use Python 3.10 or later. The exact checkers use only the standard
library and require no installation, network access or original checkout.

```powershell
python -I -B -X utf8 check_connected.py
python -I -B -X utf8 check_witness.py
python -I -B -X utf8 check_conditional_head.py
```

Default mode freshly computes and compares the full saved receipt without
writing. The --write-results option is only for intentionally regenerating
an adjacent receipt during development. The third checker independently
counts the complete local incidence stars in two and three dimensions.

The [PNG figure](connected_joint.png), editable [SVG](connected_joint.svg)
and [drawing source](draw_connected_joint.py) are included. Viewing does not
require Matplotlib; regenerating the optional figure does. It was generated
with the existing local runtime, not an installation. See
[visual verification](VISUAL_CHECKS.md).

## Evidence and provenance

[SOURCE_AUDIT.md](SOURCE_AUDIT.md) separates established literature,
accepted prior derivations, current written proofs, exact finite checks and
open obligations. [SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json) binds
the 33 accepted YM source copies and nine read-only other-task snapshots.
Their historical links retain their source contexts; this packet's new
proofs/checkers use bundled dependencies. Running-task results are attributed
snapshots, not independent new verifications of those research lanes.

The prior signed-residual ZIP remains unchanged at SHA-256
`914b1950ed762cd86f1b14ea6cd7816e99f8860a612ba3cea44773544bb3218f`.
The top-level MANIFEST.json binds every other delivered payload file.
The final-export sidecars live beside the final ZIP and record its own hash,
fresh extraction, manifest verification and actual read-only replay.
Hashes establish byte identity; they do not prove the mathematical content.
