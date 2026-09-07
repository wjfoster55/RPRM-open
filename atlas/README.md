# Mechanical Motion Atlas

An offline 2D workspace for twenty ideal mechanism laws and their typed
compositions. Open [index.html](index.html) in a browser with its sibling files
present. There is no installation, account or network dependency.

## Use the workspace

Check any combination of mechanisms in the library. Selecting a name changes
the inspected model without changing layer visibility. Each model retains its
own parameter and optional phase shift. Starting comparisons cover joints,
ratios, linkages, gates and accumulated travel.

The trace view plots a selected channel against time. The phase portrait plots
that channel against a numerical derivative per radian. The mechanism view
shows the inspected model: planar linkage diagrams use their ideal constraints;
other diagrams show phase and output pointers schematically. A pointer is not a
physical shaft when the output type is a position or another non-angular value.

Playback begins paused and stops at the observed endpoint. The admitted display
windows are 0.5, 1, 2, 4, 8 and 16 turns. The time slider works without motion.
The app also pauses when its document becomes hidden or reduced motion is
enabled. Pressing Play explicitly starts the animation.

Output, hidden and full typed component values are different receivers. For
example, an identity-phase coupling has a sine channel in the trace view and
the full phase in a typed composition. Per-layer normalization loses scale and
offset. Shared normalization uses one domain over the selected sample records;
raw view retains numerical coordinates, which may have different units between
models. The readout table and CSV always preserve raw channel values.

A shifted layer samples later source input but stops at the same admitted input
endpoint. Thus a +0.75-turn display shift in a two-turn window ends at display
time 1.25. An input outside this support has no plotted continuation.

## Typed builder and exports

The builder supports 38 registered component types, including all twenty
mechanisms, clock/carry sources, explicit coordinate handoffs and readout folds.
Choose a component and connect each input through its source selector. Exact
port matches and declared adapters are distinguished; a missing relation stays
OPEN. The carry example demonstrates two separately supplied input ports.

The app admits at most 24 graph nodes. Its pure graph API admits 128 nodes and
512 edges, with a specified increasing time interval inside `[0,32]` turns.
It validates finite numeric parameters in `[0,1]`. Numeric booleans, arbitrary
runtime code and undeclared metadata are not admitted. An unknown component
can remain in a graph as an explicit OPEN obligation.

Exports are local downloads:

- Workspace JSON restores layer settings, time, view and the clean graph. It
  reopens paused. The file limit is 256 KiB; no browser storage is read or saved.
- Graph JSON contains only the admitted component graph and its finite settings.
- CSV contains all retained raw samples, input/display times, numerical slopes
  and seam flags. There are 129–2,049 samples per visible layer.
- Python embeds that clean graph and evaluates its registered laws using only
  the standard library: `python motion-composition.py 0.25`.
- LaTeX describes the same graph, equations, parameters and port relations.
  Compile with LuaLaTeX or XeLaTeX. Compiled layout is not verified here.
- PNG captures the current plot. The editable JSON and CSV carry the underlying
  numerical state separately.

The standalone Python is a forward evaluator. Its ONE result is the computed
output for supplied inputs; it does not solve a general inverse fiber. Unknown
operations, missing inputs, incompatible ports and cycles retain explicit
non-success dispositions. The JSON retains the graph needed to reconsider the
question; it contains no executable imported code.

## Model and numerical boundaries

The source distinguishes ideal kinematics from chosen profiles and proxies.
It includes exact ideal phase/ratio laws, the positive square-root slider
branch, the branch-fixed Chebyshev linkage, a selected cam profile, and
schematic threshold/contact laws. Each inspected record states what is omitted.
The numerical implementation uses IEEE-754 arithmetic and standard library
trigonometric functions. It does not certify exact transcendental values.

Slopes use finite differences. Declared hidden-channel wraps/events split the
sample records, and the adjacent slopes are left unreported. Sampling can miss
behavior between samples; a continuous-looking curve does not prove smoothness,
an exact intersection, equivalence or collision avoidance. The fixed finite
window and samples are an operational boundary, not an unbounded theorem.

Drawings are schematic. Loads, wear, collision, engagement transients, backlash,
fabrication geometry and general physical inverse problems are outside these
models. The mathematical examples do not establish their own physical fidelity.

Separate polygon, curve and topology constructions are not
runtime dependencies of this atlas. Polygon or topology morphing proofs do not
turn the mechanism viewer into a general shape-deformation solver.

## Verification

From the repository root, run:

```text
node checks/atlas/verify.js --output ABSOLUTE_OUTPUT_PATH
node checks/atlas/view-checks.js
```

Replace `ABSOLUTE_OUTPUT_PATH` with an absolute JSON output filename. The first
command checks actual JavaScript model identities/constraints and
generated Python conformance over declared finite fixtures, including rejected
inputs and unknown/malformed compositions. It emits source hashes and its
counts. Node.js and Python 3 are required for these checks, but the browser app
itself has no runtime dependency beyond the browser.

The second executes the actual app with small DOM/Canvas stubs. It checks clean
workspace round trips, actual export payloads, finite shifted support and seam
handling. Stubs do not establish rendering, accessibility or real browser
compatibility. Visual/browser QA is **NOT_RUN** in this preparation; an actual
user-opened browser review remains necessary before calling the layout verified.

## Spatial view status

A three-coordinate state-volume experiment is deferred. Its coordinates are
normalized time, a scalar output channel and a sampled slope; these are not
solid-body spatial geometry. Before integrating that separate display, its
Chebyshev `path.xy` output must retain a coordinate pair, and composed chains
must propagate discontinuity/seam information. It also needs browser/runtime
checks and a declared state/import contract. No broken spatial application is
included in this version.
