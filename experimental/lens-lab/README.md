# Lens Lab

**Interactive example.** A small, offline JavaScript playground for moving
one retained relationship through several visual lenses.

Start by dragging a point with **Move together** on. The colors rotate,
the curves shift, and the geometry moves as one configuration. Turn the lock
off and move the same point again: now just that point changes. That contrast
is the idea of lens locking—keep the relationships fixed while moving where
they live, or deliberately edit the relationships themselves.

The four panels show different uses of one source. Changing a lens changes
how the source appears, while the retained source makes it possible to return
to another view without guessing what was lost.

Open [index.html](index.html) directly in a modern browser after downloading
the repository. GitHub's file viewer displays HTML source; it does not run
the playground. There is no build, account,
package installation, telemetry, remote font, external script, or network
dependency. The same files can be served by an ordinary static server.

## Play

1. Drag a lettered point on the wheel. The palette, curves, constellation,
   and composition all use the same source points.
2. Select a swatch or an A–E button, then use **Move point** as a keyboard
   alternative. Native range inputs support arrow keys, Home, and End.
3. Turn off **Move together** to edit just one point. The other four absolute
   phases stay put, including when the edited point is A.
4. Change saturation/lightness, wave height/cycles, or geometry spread/rotation.
   These are renderer parameters: they do not rewrite the source relationship.
   Colors also identify the same occurrences across all views, and the final
   composition deliberately consumes all three lenses.
5. Set **Height**, **Spread**, or **Saturation** to zero. The corresponding
   output loses phase distinctions; restoring its control uses the retained
   source to recover the picture. Reset restores the complete starting scene.

There is no automatic animation or saved browser state. A reload resets the
scene. The application quantizes pointer edits to whole degrees.

## Declared model

This is a newly authored visualization of anchor-and-residue coordinates,
with deliberately specified display adapters. It is an instance of the
repository's [representation contract](../../docs/core.md) and
[lens definition](../../docs/glossary.md), not a physical color/curve identity.

| Field | Contract |
|---|---|
| Strong carrier | Five **ordered occurrences** in `(Z/360Z)^5`; each phase is an integer 0–359. Equal phases keep distinct occurrence labels A–E. |
| Coordinate carrier | `anchor` in Z/360Z and five ordered offsets, with `offsets[0]=0`. |
| Equality | Exact integer equality of the ordered phase tuple; visual resemblance is not equality. |
| Edit aperture | A selected occurrence index 0–4 and a target phase 0–359; a Boolean chooses common translation or single-point replacement. |
| Receiver | Reconstruct the complete ordered source tuple and evaluate the declared renderers after admitted edits. |
| Forgetting | Source phases omit revolution count. A cyclic phase does not recover an integer winding. Display pixels also omit source data. |
| Evidence | Written elementary identities below; finite executable tests for the stated fixtures; numerical display checks use floating-point tolerances. |

For `x=(x_0,...,x_4)`, write all following differences modulo 360:

```text
anchor = x_0
offset[i] = x_i - x_0
x_i = anchor + offset[i]
```

Substitution in both directions gives the original tuple or coordinate record.
This is a CAR between the two declared carriers. No arity changes, winding
values, colors, or curves enter that inverse.

With the relationship locked, moving point `j` to target `t` sets
`anchor' = t - offset[j]`. Consequently every point receives the same
translation `delta = t - x_j`, and every ordered pairwise difference survives:

```text
x_i' = x_i + delta
x_k' - x_i' = x_k - x_i
```

A fixed-delta translation has inverse translation by `-delta`. An absolute
target setter does **not** remember the previous anchor: reversing that edit
requires the old selected phase or delta. The UI offers a starting-scene Reset,
not an undo history. Selecting another point to manipulate also does not
change which occurrence supplies the stored anchor; it remains A.

When unlocked, replace only `x_j` and re-encode the tuple. Editing A therefore
changes the stored anchor and offsets but preserves the other four phases.

For an admitted offset vector without its anchor, the **complete** source
fiber is `{(a+offset[i])_i : a=0,...,359}`: `MANY(360)`. The members are
distinct because their A coordinates differ. With the anchor, reconstruction
is `ONE(tuple)`. Malformed states are admission errors, not empty fibers.
Any extra coordinate, renderer, operation, or required observation needs its
own contract; it does not inherit this carrier's verification.

## Separate visual maps

Let `p` be a phase, `s,l` percentages, `h,r` values in `[0,1]`, `k` an integer
1–4, `q` a rotation in Z/360Z, and `t` a sample position in `[0,1]`.

| Lens | Specified readout | Loss and limit |
|---|---|---|
| Color | HSL hue `p`, saturation `s`, lightness `l`, converted and rounded to 8-bit sRGB hex. UI lightness range: 20–80%. | HSL is a display convention, not a perceptually uniform metric. At zero saturation all 360 phases give the same gray. Quantized RGB can collide. |
| Curves | `h sin(2π(kt+p/360))`, sampled at 241 positions for drawing. | At `h=0` every phase yields the same zero wave; one sine sample alone also need not recover phase. The graph is a new phase-wave renderer, not a moving-frame curve reconstruction result. |
| Geometry | `(r cos(2π(p+q)/360), r sin(2π(p+q)/360))`, followed by known x/y screen scales. | At `r=0` all phases land at the origin. Pixels are not exact real coordinates. Rotation here changes this renderer, not the source. |
| Composition | Palette-derived fills/background, geometry-derived ellipse centers, and wave-derived ellipse radii. | A many-to-one decorative display; it makes no source-inverse claim. |

The source remains stored when any output collapses. The demo never attempts
to recover the whole relationship from a hex value or a pixel. All maps are
deliberately shared design choices. This makes synchronization concrete; it
does not establish an independently discovered equivalence between color
perception, geometry, music, or other domains.

## Replay

From the repository root, with Node.js 18 or newer:

```sh
node --test experimental/lens-lab/model.test.js
node --check experimental/lens-lab/app.js
python -I -B verify.py
```

The 16 model tests cover:

- Every anchor, selected index, and target for one nonuniform five-point
  fixture: **648,000 locked transitions**, all pairwise invariants, and
  reversal with the old selected phase retained.
- **3,600** duplicate/wrap signature checks and **5,400** unlocked edits.
- All 360 phases for source-coordinate and projection checks; canonical
  colors, wave/orbit identities, degenerate outputs, malformed inputs,
  immutability, and browser/CommonJS export compatibility.

The finite suite does not enumerate `360^5` source tuples. The identities above
give the general coordinate/translation argument; sample counts are finite
execution evidence. The tests run solely from adjacent source bytes without
cached reports or private repositories. The aggregate `verify.py` also runs
this suite through `verify.cjs`, which writes a fresh scoped result for the
repository's verification receipt.

Manual browser review on 2026-09-07 exercised all three presets, point
selection, locked/unlocked editing including A, pointer drag, keyboard ranges,
independent lens changes, collapse and restore, Reset, and desktop/390-pixel
layouts. These checks passed in the tested browser. They are not an automated
browser suite or a cross-browser accessibility certification. Visual review
does not replace the pure model checks.

## Files

`model.js` is the standalone browser/CommonJS coordinate and renderer module;
`model.test.js` is its cold test suite. `index.html`, `style.css`, and `app.js`
are the presentation. `verify.cjs` connects the adjacent test suite to the
repository's aggregate checker. Everything is self-contained within this
directory. The [experimental index](../README.md) links the other examples.

Original software follows the repository's [0BSD license](../../LICENSE);
original prose and diagrams follow [CC0](../../LICENSES/CC0-1.0.txt).
