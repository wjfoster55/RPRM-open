# Light & Shadow

One editable shadow swatch controls three compatible scenes. Open
[index.html](index.html) directly in a modern browser. No install, build,
account, network request or external asset is required.

## Try this

1. **Drag the shared swatch** at the top. All three ground shadows and their
   cutouts move together. Change shape or size to reshape every scene.
   Matching colored dots trace the same ordered vertices through the views.
2. Change **one scene's height**. Its cutout changes size and position, while
   all three A shadows still match. Starting heights are 20, 50 and 80;
   cutout sizes are 80%, 50% and 20% of the target.
3. Switch **Read all three with → Light B**. The scenes stay unchanged; their
   observed shadows separate by height. A's outlines remain as dashed guides.
4. Move the shared lamp controls, or drag a warm lamp in any scene. All three
   cutouts refit to preserve the target. Set all heights equal and B's shadows
   coincide too: the match indicator compares exact polygon coordinates.

The swatch has a size handle, and each cutout can be dragged vertically.
Every drag has a native keyboard-accessible range control. The lamps move
together on the horizontal plane at height 100; vertical screen movement
does not change lamp height. Reset restores the swatch and starting heights.
The interface starts at 100% swatch size. Nothing persists after reload.
The former single-scene pin workflow has
been replaced by the always-visible three-scene comparison.

Each scene and its observed shadow form one aligned column. All three
observation panes use the **same fixed coordinates and scale for A and B**,
so switching lights neither zooms nor reframes them. The editing swatch uses
a larger scale. The lamps represent separate exposures, not composited light.

## What is linked

The forward question supplies a lamp and object, then calculates the shadow.
Here the desired shadow is editable input. The cutout is reconstructed from
that target, the lamp and its chosen height. These are **three different
compatible source scenes**. Within each column, the isometric scene and its
two possible projections are views of that column's retained source.

The shared settings are shape, size, target position and lamp position.
The three heights are independent. Changing an observation does not edit a
source. Changing a height refits that scene; changing shared settings refits
all three. Equal heights are allowed and must produce equal B observations.

The application uses the existing [affine relation and receiver
contract](../../docs/core.md) with ordinary central projection. The
[agent handbook](../../AGENT_HANDBOOK.md) explains complete fibers and
distinguishing observations; [MODEL.md](MODEL.md) gives this example's exact
source, equations, inverse calculation, closure and hostile cases.

For a fixed shadow, the complete model admits **181,447** sources: 161 × 161
lamp positions and seven heights. A second exact projection determines
height, leaving **25,921** possible lamp positions. The interface shows
three selected examples from that family, not an enumeration of all sources.
Its matching-shadow count describes those three examples only.

This is an application of familiar geometry, with no claim that inverse
design or shadow constraints are new to graphics. Existing tools provide
[light and shadow linking](https://docs.blender.org/manual/en/4.2/render/cycles/object_settings/light_linking.html).
The ordinary point-light idealization is described in
[Physically Based Rendering](https://www.pbr-book.org/4ed/Light_Sources/Point_Lights).

## Exact model and illustrative display

The unchanged model uses point lights at height 100, a flat opaque polygon
parallel to the ground, seven admitted heights and exact rational coordinates.
The second light has offset `(40,-30,0)` from the first. Projection follows
the declared ray/plane geometry.

The added `presentation.js` composes three admitted model scenes with shared
settings and an ordered depth triple in `{2,...,8}³`. `ShadowFamily.build`
retains the complete scenes; `observe` reads A or B without mutating them.
It compares complete ordered rational polygons and uses the model's exact
inverse to recover each depth under B. The compositions are deeply frozen.
They do not enlarge the underlying per-scene physical model.

SVG rounds coordinates for display. Floor tint, ray glow and lamp halos are
illustrative styling. They do not simulate light power, materials, soft
shadows, interreflection or measured brightness. Exact invariance refers to
retained polygon coordinates rather than anti-aliased pixels or photographs.

## Replay and scope

From the repository root, with Node.js 18 or newer:

```sh
node --test experimental/shadow-lens/model.test.cjs
node --test experimental/shadow-lens/presentation.test.cjs
node --check experimental/shadow-lens/app.js
```

The 11 model tests include the complete 181,447-scene fixed-shadow family and
the stated boundary/admission checks. Six presentation tests cover all 343
ordered depth triples, including duplicates; 96 shared-setting boundary
combinations; immutable sources across A/B; strict admission; and browser/
CommonJS compatibility. Neither suite executes the interface. The dated
[REVIEW.md](REVIEW.md) records browser observations separately.

This remains a local preview candidate, absent from the release pack index
and aggregate verifier. Original software uses the repository's
[0BSD license](../../LICENSE); original prose and diagrams use
[CC0](../../LICENSES/CC0-1.0.txt).
