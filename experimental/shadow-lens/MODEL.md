# Shadow Lens

A local point-light playground: change a planar object's height and its light
position while constructing the object to retain one exact ground shadow.
A second light observation separates the possible heights. This is ordinary
similar-triangle geometry, presented through an explicit retained-observation
and completion-fiber contract. It makes no new optics or physical-law claim.

Open [index.html](index.html) to use the preview. Replay the model checks with
Node.js 18 or newer, from the repository root:

```sh
node --test experimental/shadow-lens/model.test.cjs
```

The model is dependency-free and works as a classic browser script or a
CommonJS module. There is no install or build step. The checks are cold replay
from the local JavaScript files; the tests do not depend on a saved receipt.

## Carrier and observations

The source is exactly the seven integer fields below. Coordinates and height
use one consistent arbitrary length unit. `size` is a percentage; `centerX/Y`
locate the template's origin, which need not be its area centroid.

| Field | Admitted integers | Meaning |
|---|---:|---|
| `lightX`, `lightY` | -80 through 80 | Primary point-light ground coordinates |
| `depth` | 2 through 8 | Object height is `10 * depth` |
| `centerX`, `centerY` | -50 through 50 | Desired shadow's template-origin coordinates |
| `size` | 40 through 120 | Desired shadow scale, in percent of the template |
| `shape` | 0 through 2 | Kite, Chevron, or Wing; fixed 5-, 6-, or 7-vertex template |

The templates are explicit integer arrays in [model.js](model.js). Source
equality is coordinatewise integer equality. A polygon observation is its
exact ordered list of ground vertices, including the fixed vertex order.
There are `161² * 7 * 101² * 81 * 3 = 449,778,625,821` source tuples.
Derived rational geometry is an image of this finite carrier, not a new
unbounded source. The secondary light is fixed relative to the primary:
`delta = (40, -30)`. Both lights have height 100, and the ground is `z = 0`.

The physical idealization is a flat opaque polygon, a point light, and a
ground plane. There is no thickness, penumbra, material model, radiometry,
occlusion by other objects, or experimental measurement noise. The probe is
a **separate comparison observation** of the same object from another light;
two overlaid displayed polygons do not model their combined illumination.

## Construction and preservation

For template vertex `P`, desired ground vertex `S`, primary light `L`, object
vertex `O`, and integer depth `d`, construct

```text
S_xy = center_xy + (size / 100) * P_xy,       S_z = 0
L = (lightX, lightY, 100)
O_xy = (1 - d/10) * S_xy + (d/10) * L_xy,   O_z = 10d
```

The ordinary light ray through `O` is `R(t) = L + t(O - L)`. Its height is
`100 + t(10d - 100)`, so it meets the ground at `t = 10/(10-d) > 1`.
Substituting the construction gives `R_xy(t) = S_xy` exactly. The object
therefore lies between the light and each intended ground vertex. All its
vertices have one height; projection scales and translates the whole polygon,
so it carries edges and the filled polygon along with the vertices.

Changing `depth` or `lightX/Y` **reconstructs the object**, keeping `S` fixed.
It is an inverse-design operation, not a claim that an arbitrary rigid object
can be moved without changing its shadow. Changing `centerX/Y`, `size`, or
`shape` edits the desired shadow itself. Replacing any supplied integer field
with another admitted value is enabled; an invalid replacement is an admission
error and leaves the prior state untouched.

For the second light `B = L + (40, -30, 0)`, project the same object:

```text
S_B = S - [d/(10-d)] * delta
displacement = S_B - S = (-40d/(10-d), 30d/(10-d))
```

The nonzero known probe therefore reveals `d`. For example, if
`r = -displacement_x / 40`, then `d = 10r/(1+r)` when the observation belongs
to this model. Both coordinates must agree with the same admitted depth.
The code checks all seven candidate depths using exact rational equality.

## Complete fibers and what is forgotten

Fix admitted shadow settings `(centerX, centerY, size, shape)`, and supply the
resulting exact primary shadow. The complete compatible source family is

```text
{ (lightX, lightY, depth, centerX, centerY, size, shape) :
  lightX, lightY in {-80,...,80}, depth in {2,...,8} }
```

Every member projects to that shadow by the equation above, and these are
all missing fields of the source. This is `MANY(181447)`, not merely a list
of found witnesses. In fact, the exact ordered shadow also identifies its
shadow settings: vertex count selects the template; a nonzero edge recovers
the positive scale; its first vertex recovers the translation. The three
templates are simple, have no redundant collinear vertices, and have distinct
vertex counts. The displayed counts use the explicit fixed-settings aperture.

Supplying the probe observation selects one depth but leaves both primary
light coordinates free. The complete full-source fiber is then
`MANY(25921)`. The **depth readout** is `ONE(d)`; the **full scene** remains
`MANY`. If no depth matches both displacement coordinates, the complete
depth fiber is `NONE`. Malformed data is an admission error, never `NONE`.

The primary-shadow map is a lossy FOLD for the full scene and an exact
representation of its stated shadow receiver. The pair of shadows retains
height as well. Neither observation recovers absolute light position. The
full source retained by the application is the reopen route for all geometry;
it is not recovered from raster pixels. Numeric SVG coordinates are only a
display of the exact rational outputs. The visible scene and controls supply
additional information beyond the shadow-only receiver.

For the permitted absolute field replacements, an unchanged set of shadow
settings keeps the primary observation unchanged after any finite sequence
of light/depth edits. A shadow-setting replacement has a well-defined shadow
successor too. The primary shadow alone does not answer the probe question:
two compatible sources of different depths produce different probe shadows.
No guarantee is made for rigid-object moves, arbitrary new sensors, rotations,
light heights, or new source fields; those require a new declared contract.

## JavaScript API

The browser global is `ShadowLens`; CommonJS uses `require('./model.js')`.

| Function or constant | Contract |
|---|---|
| `defaults()` | Fresh frozen source: `{lightX:-40,lightY:30,depth:5,centerX:0,centerY:0,size:80,shape:0}` |
| `createState(partial = {})` | Validate a partial source and fill omitted fields from defaults |
| `update(state, patch)` | Require a complete admitted source and partial patch; return a new frozen source |
| `scene(state)` | Require a complete source; return a frozen source copy, geometry, and fiber counts |
| `rational(n, d = 1)` | Safe-integer input, nonzero denominator; reduced frozen `{n,d}` with positive denominator |
| `depthFromDisplacement({x,y})` | Exact rational coordinate records; return frozen `{kind,values,count}` with `ONE,[d],1` or `NONE,[],0` |
| `BOUNDS`, `SHAPES` | Frozen `{min,max}` field bounds and `{id,name,vertices}` templates |
| `LIGHT_HEIGHT`, `PROBE_DELTA` | Fixed 100 and frozen `{x:40,y:-30}` |

`scene` returns `shadow`, `cutout`, and `secondary` arrays of numeric
`{x,y,z}` points; `light` and `probe` are individual numeric points.
`displacement` has numeric `{x,y}`. `exact` mirrors those fields, replacing
each coordinate with a reduced rational `{n,d}`. `state` is the complete
source; `fibers` is `{primary:181447, withProbe:25921}`.

No input coercion is performed. Unknown fields, symbols, inherited records,
accessors, missing full-source fields, nonintegers, and out-of-range values
are rejected. Plain records with a null prototype are admitted; integer `-0`
is canonicalized to `0`. Rational
readout inputs may use equivalent unreduced or negative-denominator fractions;
matching uses integer cross-products with `BigInt` to avoid overflow.
Geometry's finite bounds keep all pre-normalization arithmetic within exact
JavaScript safe integers. Results are deeply frozen. A pure update validates
before returning; callers install its new reference only after success.
This module does not supply a concurrent-state or stale-parent coordinator.

## Evidence and hostile controls

The projection and fiber-coverage arguments above are written algebraic
derivations using conventional affine geometry and finite counting. They
cover every admitted source; they are not formal proof-assistant declarations.

The 11 executable tests provide separate implementation evidence:

- Exhaust all 181,447 light/depth tuples at the default shadow settings.
  Independently ray-project every constructed vertex from each light, verify
  one primary shadow, and count seven probe fibers of exactly 25,921.
- Check all 243 shape/size pairs, each of the 101 values of each center axis
  while the other is zero: 49,086 scenes, each independently projected.
- Check all 672 combinations of endpoint size/centers/lights, all shapes,
  and all depths; verify drawing coordinates against exact outputs.
- Check polygon simplicity/nondegeneracy, shadow-setting recovery, all seven
  exact inverse depths, inconsistent observations, admission boundaries,
  immutable updates, and both script/module loading modes.
- Preserve two distinguishing controls: equal primary shadows with different
  probe shadows, and equal shadow pairs with different absolute lights.
  Reusing the same light (zero probe offset) separates no depth. Zero offset
  is not exposed as a configurable probe; zero observed displacement is
  `NONE` under the actual fixed nonzero-probe contract.

The tests are not an enumeration of all 449 billion source tuples. Full
carrier coverage comes from the stated equations; the tests exercise the
declared finite censuses and boundaries. Browser presentation checks are
separate from this pure-model suite. Measured optics, arbitrary polygons,
perspective photographs, and noisy inverse estimation remain outside scope.
