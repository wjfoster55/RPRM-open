# Light & Shadow review — 2026-09-07

Local preview candidate, separate from the approved Music Lens release.
The model, application and documentation are adjacent and need no private
source, network service or installed package to replay. This directory has
not been committed, pushed or registered in aggregate release verification.

## Model execution

`node --test experimental/shadow-lens/model.test.cjs`: **11 passed**, zero
failed, cancelled or skipped. The suite independently intersects rays with
the ground for the complete 181,447-state default-shadow light/depth family,
finding seven second-projection fibers of 25,921. It also checks 49,086
shape/size/individual-center cases, 672 boundary combinations, inverse depth
recovery, malformed input, immutable successors, browser/CommonJS exports,
and the hostile repeated-same-light control.

This covers the declared finite families. It does not enumerate the full
449,778,625,821-state source product. The written equations and complete
fiber argument are separately documented in MODEL.md.

`node --check experimental/shadow-lens/app.js`: PASS. Independent integration
review found no blocking issue in the model/UI wiring, pointer transforms,
family counts, inverse readout or the bounded geometry in the SVG frames.

## Initial single-scene browser observations

The local in-app browser was exercised through the actual controls:

- Pin a height-50 scene, then change height to 80: cutout polygon changes,
  while the primary polygon's complete SVG points string remains identical.
- Enable the second light: height 80 is recovered from exact displacement
  `(-160,120)` and the compatible-scene count becomes 25,921. At height 20
  the displacement is `(-10,15/2)`, with the same primary shadow.
- Set the lamp to opposite grid bounds: both shadows remain identical at
  the same height, matching the remaining absolute-position ambiguity.
- Move the target and select Wing: the primary polygon changes to seven
  vertices and the pin status correctly reports a changed target.
- An off-center horizontal lamp drag changes both world-plane coordinates
  under the fixed isometric map and preserves the primary polygon.
- A vertical cutout drag changes height 60 to 80 and preserves the primary
  polygon. The shadow handle changes the two target coordinates.
- Native range keys change height; the control also exposes the rendered
  height through `aria-valuetext`. Select and toggle controls operate normally.
- Desktop and 390×844 layouts were visually inspected. Height and pin controls
  were moved beside the scene, and the second-light toggle beside its view.
  The narrow page had no horizontal overflow (document width 375 including
  the browser's scrollbar allocation inside a 390-wide viewport), and its
  second-light control recovered height 70 with shift `(-280/3,70)`.
- Browser warning/error log was empty during these checks.

Temporary viewport settings were restored. These are manual observations in
one browser, not an automated UI suite, screen-reader audit, photometric
validation or cross-browser certification. Styling is illustrative; exact
claims apply to retained rational geometry.

## Companion release

Music Lens was published separately on main in commit
`aaa3dcf7c854bf2fbbbf398a18a4282da2162afa`, including explanation and aggregate
model/audio registrations. Its isolated release export passed all 20
requested Python/Node jobs with unchanged source and formal Lean NOT_RUN;
remote main was checked against that commit. No Shadow Lens bytes were
included in that export or push.

## Linked-swatch UI revision — 2026-09-07

William's review found that the original single-scene interface looked like
an ordinary lighting control and did not expose the linked relation clearly.
The revised interface replaces pinning with one shared shadow swatch feeding
three simultaneous source scenes. Shape, size, target position and lamp
position are shared; the three heights are independent. Corresponding vertex
colors, a visible branch, per-scene resize readouts and aligned observation
panes make the shared input and the resulting changes visible together.

The original per-scene model and its 11-test suite are unchanged. The new
`presentation.js` composition passes six tests, covering all 343 depth
triples (including duplicates), 96 boundary combinations, exact A/B grouping,
immutable retained source scenes, malformed inputs and browser/CommonJS
parity. A/B switch behavior does not borrow the old differing-zoom display:
every observation now uses the same fixed coordinates and scale.

Browser checks of the revised interface passed:

- A shared size edit changed all three cutouts, and the three complete A
  polygon strings remained equal. Direct swatch dragging changed all three
  scenes together; a test drag set the shared position to `(30,15)`.
- Switching A to B left all three complete scene SVG contents identical.
  Only the observations changed, producing three different polygons and
  recovering heights 20, 50 and 80.
- Setting every height to 50 correctly changed B to one matching shadow.
  The explanatory text recognized this case instead of claiming separation.
- On Chevron, the size handle changed 40% to 80% with all three six-vertex
  scenes updating. Review corrected the handle's scale divisor to use the
  active template's rightmost vertex, rather than assuming every shape had
  the same extent.
- Dragging a lamp in the middle scene refitted all three cutouts while
  preserving all three A polygons. Dragging that scene's cutout changed
  heights `(20,50,80)` to `(20,60,80)` and preserved the three shadows.
- Desktop and 390×844 layouts were inspected. The narrow layout has no
  horizontal overflow, and keyboard resizing followed by the B switch worked.
  The compact phone source controls leave more of the first scene visible.
- Browser warning/error log was empty; application syntax check passed.

The viewport override was reset. Reset starts the UI at 100% swatch size,
heights 20/50/80 and light A. These remain manual observations in one browser,
not a full accessibility audit or automatic UI suite. The revised local
preview is still uncommitted and unpublished.
