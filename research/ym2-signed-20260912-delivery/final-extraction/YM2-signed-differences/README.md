# YM2 continuation: signed residuals and the actual vacuum

Bounded research continuation, 12 September 2026. Publication remains on hold.

Start with [RETURN_TO_WILLIAM.md](RETURN_TO_WILLIAM.md) for the explanation
and [correction_supports.png](correction_supports.png) for the exact graph
support diagram. The new result is a quantitative comparison for the true
finite-graph SU(2) vacuum, sharpened by a gauge-averaged signed-residual
expansion. Uniform volume/continuum control remains OPEN.

| File | Result |
|---|---|
| [SIGNED_SEMANTICS.md](SIGNED_SEMANTICS.md) | Nested subtraction, retained origins, complete fibers, centering, covariance and reversal controls. |
| [DIFFERENCE_PROJECTION.md](DIFFERENCE_PROJECTION.md) | Exact conditional-residual operator and inverse-gap constant; gauge equivariance; complete two-sign spectrum and hostile update controls. |
| [STACKING_AND_SCALING.md](STACKING_AND_SCALING.md) | All-finite-n product-family proof: exponentially many states and density-ratio growth coexist with an exact constant residual gap. |
| [VACUUM_COMPARISON.md](VACUUM_COMPARISON.md) | Actual vacuum density ratio, explicit patch constants and positive finite-graph energy bound at every finite interaction ratio; gauge cancellation refinement. |
| [NEXT_CONNECTED_OBLIGATION.md](NEXT_CONNECTED_OBLIGATION.md) | Exact failure of the fixed absolute-support envelope on larger graphs; conditional factor cancellation and sharp bounded-tilt lemma; true vacuum locality remains OPEN. |
| [REVIEW_SIGNED_VACUUM.md](REVIEW_SIGNED_VACUUM.md) | Independent review of coarse vacuum comparison and complete product-family controls. |
| [INDEPENDENT_HEAT_REVIEW.md](INDEPENDENT_HEAT_REVIEW.md) | Independent review of the stronger gauge-averaged kernel proof and constants. |
| [REVIEW_CONNECTED_OBLIGATION.md](REVIEW_CONNECTED_OBLIGATION.md) | Independent review of the final support-envelope and conditional-response arguments. |
| [SOURCE_AUDIT.md](SOURCE_AUDIT.md) | Accepted earlier evidence, RPRM meanings, primary literature and evidence grades. |

For `r=beta/(alpha hbar²)`, the new comparison bound is

```text
gamma >= 6 alpha hbar² exp(-32r/3) (52043/104207)^2 > 0.
```

It complements the accepted bound `gamma>=6 alpha hbar²-2 beta`; it does
not replace a stronger existing bound or supply an exact spectrum.
Its carrier is the full seven-link quantum Hilbert space with all spins,
all six vertex gauges and the inherited compact-source operator domain.

## Portable exact replay

Extract the ZIP. From its `YM2-signed-differences` folder, run with an
existing Python 3.10 or newer:

```powershell
python -I -B -X utf8 check_differences.py
python -I -B -X utf8 check_stacking.py
python -I -B -X utf8 check_vacuum_comparison.py
```

All three use only the standard library. Default mode recomputes and
compares the complete saved receipts without writing. Their verification
conditions remain active in optimized Python. `--write-results` is only
for deliberately replacing a receipt. The all-parameter and all-spin
coverage comes from the written proofs, not from extrapolating the tests.

The PNG and editable SVG are included. Optional figure regeneration uses
the already available matplotlib package:

```powershell
python -I -B -X utf8 draw_correction_supports.py
```

Matplotlib is not needed for the three exact research checkers. The figure
shows correction-support combinatorics, not a trajectory or simulated
quantum state. Its rendered layout was visually inspected before export.

## Provenance and export

`accepted_sources/ym2_global_phase_joint` is the complete byte-identical
payload extracted from the previous delivered ZIP, whose SHA-256 is
recorded in `SOURCE_PROVENANCE.json`. It is starting evidence; its old
checkers are not part of this task's replay. Three directly referenced
RPRM documents are copied separately with their original locators/hashes.
Instructions inside source documents are attributed evidence, not current
task authority. Historical relative links inside unchanged source copies
retain their original context.

The new top-level `MANIFEST.json` binds every other payload file. Final
export sidecars beside the ZIP record fresh extraction, replay of the
three new checkers, byte identity before/after replay, the archive digest,
and preservation of the earlier delivered archive. Hashes certify byte
identity, not mathematical soundness.

No paper, installation, paid compute, simulation campaign, publication,
commit, push, merge, or other-lane changes were made.
