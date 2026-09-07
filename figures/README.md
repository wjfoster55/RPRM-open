# Explanatory figures

Six figures illustrate stated laws and their boundaries. The first four are
finite diagrams; the last two plot supplied analytic probabilities from
[III.9 of the manuscript](../MANIFESTO.md#iii9-two-path-interference-and-retained-coherence).
They are illustrations, not empirical results or proof receipts.

| Figure | Readable source | Print input |
|---|---|---|
| 1. Joint aperture | [SVG](01-joint-aperture.svg) | [PNG](01-joint-aperture.png) |
| 2. Future distinction | [SVG](02-future-distinction.svg) | [PNG](02-future-distinction.png) |
| 3. Erasure and error | [SVG](03-erasure-and-error.svg) | [PNG](03-erasure-and-error.png) |
| 4. Number descriptions | [SVG](04-number-descriptions.svg) | [PNG](04-number-descriptions.png) |
| 5. Complete two-path controls (Figure III.9.2) | [SVG](two_path_complete_controls.svg) | [PDF](two_path_complete_controls.pdf) |
| 6. Conditional eraser weights (Figure III.9.1) | [SVG](two_path_eraser_weights.svg) | [PDF](two_path_eraser_weights.pdf) |

1. **Joint aperture:** the carrier is all 25 pairs in `{0,…,4}²`, with the
   fixed target `c=4`. Exactly five satisfy `a+b=4`. Each marginal allows
   all five coordinate values, so their product admits 20 extra joint pairs.
   Both panels show the whole carrier on the same axes. The hostile case is
   inferring the original joint constraint from its separate marginals.
2. **Future distinction:** the drawn transitions are `p→r` and `q→q`
   under action `a`. The complete example also has `r→r`; that self-loop
   is not drawn. Current observations at `p,q` are both 0, while those
   after `a` are 1 and 0. The one action separates the states and rejects
   a merge based only on their present observations.
3. **Erasure and error:** four bits obey even parity. In `1,0,1,?`, the
   labeled erasure is uniquely 0. The word `1,0,1,1` has odd parity and
   therefore violates that constraint, but parity alone cannot identify an
   arbitrary changed position. Even numbers of bit flips can escape this
   parity check; error detection is not general error correction.
4. **Number descriptions:** integer value, a base-ten word, an operation
   path and geometric dimension have separate types. The illustrated paths
   do not supply an adapter from word length or operation count to geometric
   dimension.
5. **Complete two-path controls:** balanced input with equal amplitudes
   `a=b=1/√2` uses
   `Pθ(+) = 1/2 + Re(exp(iθ)γ)/2` with the chapter's fixed path basis and
   phase convention. All six marker-overlap rows are shown on identical
   axes. Dots mark phases `0, π/2, π, 3π/2`, in that order:

   | γ | Four control probabilities |
   |---|---|
   | 1 | 1, 1/2, 0, 1/2 |
   | 0 | 1/2, 1/2, 1/2, 1/2 |
   | −1 | 0, 1/2, 1, 1/2 |
   | i | 1/2, 0, 1/2, 1 |
   | 3/5 | 4/5, 1/2, 1/5, 1/2 |
   | (3+4i)/5 | 4/5, 1/10, 1/5, 9/10 |

   The hostile comparisons are explicit: equal populations do not determine
   interference, and equal overlap magnitudes do not determine phase.
   The last row has true extrema between the four marked settings; sampled
   extrema do not establish its full visibility.
6. **Conditional eraser weights:** for the balanced orthogonally marked
   state `(|00⟩+|11⟩)/√2` measured in the chapter's eraser basis, each marker outcome
   `r=±1` has probability `qᵣ=1/2`. The selected curves are
   `P(+|r,θ)=(1+r cos θ)/2`, while the joint probabilities are
   `P(+,r|θ)=(1+r cos θ)/4`. Their weighted marginal
   `Σᵣ qᵣ P(+|r,θ)` is the constant `1/2`. The hostile inference is
   treating a selected fringe as unconditional recovery after discarding
   the marker outcome. This illustration does not implement a communicated
   outcome followed by a conditional phase correction, nor a coherent
   reversal of the joint marking interaction.

## Regenerate and inspect

Matplotlib and NumPy are optional external plotting dependencies in a
Python 3.10 or later development environment. No data download is used.
They are not bundled or required to read the repository or run its core
checks. The plotting versions and Python version are recorded for the
two-path run; another environment needs its own output inspection.

From the repository root, the original four-diagram command is:

```text
python -I -B tools/build_figures.py
```

That existing command writes the four SVG/PNG pairs in `figures/`.
The separate two-path command is:

```text
python -I -B tools/build_two_path_figures.py
```

Each invocation creates a fresh
`.artifacts/two-path-figures/<build-id>/` containing both plates in SVG,
PDF and PNG, plus `TWO_PATH_FIGURES.json`. Use `--build-id NAME` to choose
a new name; an existing directory is rejected. The generator leaves the
included assets unchanged. The generated PNGs are convenient direct
inspection outputs; the two-path PNGs are not part of the supplied asset
set.

The receipt binds the generator bytes, all of `MANIFESTO.md`, the exact
III.9 section bytes and all six generated output files. It checks the four
plotted phase markers in every row against the written control table using
absolute floating tolerance `1e-14`. This is a rendering convention
check, not an exact-arithmetic proof or a new theorem test. Successful
generation records `GENERATED_PENDING_VISUAL_REVIEW`; it does not claim
that someone has inspected the images or their final book pages.

SVGs use local font selection. The first four source PNGs are the book's
raster print inputs; the two-path PDFs are its vector print inputs.
Generated metadata and plotting-library versions can change file hashes
without establishing a change in mathematical content or pixel appearance.
Compare the actual output, then review any intended asset replacement.

The [public book build](../tools/typesetting/README.md) selects the print
inputs and checks the bindings in
[ASSETS.json](../tools/typesetting/ASSETS.json). If an included asset is
deliberately replaced, review it and update its binding before rebuilding
with `python -I -B tools/build_paper.py`. Running a figure generator does
not update those bindings or certify the resulting book layout.

The six original figures are CC0; both generators are 0BSD. Embedded font
programs retain their own licenses; see the
[third-party notices](../THIRD_PARTY_NOTICES.md).
