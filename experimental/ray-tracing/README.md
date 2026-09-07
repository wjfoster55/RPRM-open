# Finite ray cache experiment

**EXPERIMENTAL — executable exact geometry and cache-update demonstrator.**
Current state: complete finite tests of the model below, including forged cache
rejection. This pack computes ray contacts and nearest opaque cells. It has no
image formation, materials, radiometry, reflections, acceleration hierarchy, or
hardware benchmark.

## Run and inspect

Python 3.10 or newer; standard library only. From the repository root:

```sh
python -I -B experimental/ray-tracing/example.py
python -I -B experimental/ray-tracing/check.py
```

Both commands print JSON. Either accepts `--output ABSOLUTE_JSON_PATH`; replace
that placeholder with an absolute filename. The checker exits nonzero on any
failed condition. Its receipt records executed bounds and relative source
hashes. Example output includes a clean scene snapshot and update receipt.

## Model and receiver

There are 36 directed segments, named `(a,b)` for `a,b in {0,...,5}`:

`p(t) = (0,a) + t (5,b-a),  0 <= t <= 1`.

An opaque cell `(x,y)` is the **closed** square centered at that point, with
side length one. Admitted centers satisfy `x in {1,2,3,4}`, `y in {0,...,5}`:
24 cells. A scene is an unordered duplicate-free subset of at most three cells.
Segment/cell entry and exit parameters are exact rational numbers. Endpoint,
edge, and corner contacts count; a tie is not resolved by cell order.

The retained state contains the scene mask and every contact row, ordered by
`(entry,exit,cell)`. `first_hit(row)` returns the complete set of identities at
the smallest entry parameter, classified `NONE`, `ONE`, or `MANY`. This helper
requires a row from a validated state. `receiver(snapshot)` validates before
returning all 36 nearest-hit readouts. A `NONE` readout means no opaque contact,
not a failed geometry calculation.

The map from complete rows to first-hit identities forgets deeper hits. It is
lossy for future deletion queries. For the horizontal ray `(0,0)`, scenes
`{(1,0),(2,0)}` and `{(1,0),(3,0)}` both currently return `(1,0)`. Removing that
cell reveals different successors. A visible answer alone does not support
this continuation; retaining more hits or reopening geometry is necessary.
When hit depths are distinct, answering after `d` nearest-hit deletions needs
the next `d+1` hit identities or explicit end-of-list information. Exact ties
additionally require retaining each entire nearest-entry group.

## Operations and worked example

`compile_scene(opaque)` constructs all rows from geometry.
`update(snapshot, "TOGGLE", at)` removes an occupied cell or adds an empty one,
provided the result has at most three cells. It is self-inverse on admitted
states. `update(snapshot, "MOVE", at, target)` requires **exactly one** opaque
cell equal to `at` and a distinct admitted target. Swapping the endpoints is
its inverse. Moving a member of a multi-cell scene is outside this operation's
scope and is rejected, even when a geometric result could be computed.

The example starts with opaque cells `(1,0)` and `(2,0)`. Ray `(0,0)` first
enters `(1,0)` at `t=1/10`. Toggling that cell off reveals `(2,0)` at `t=3/10`.
The output contains all exact rows, not just this displayed answer.

The dirty set is the union of fixed ray/cell incidence lists for cells in the
old/new mask symmetric difference. Those rows are recomputed; unaffected rows
are retained. Optional `claimed_dirty` must equal the entire canonical dirty
list. There is no approximate or caller-authorized omission.

`load_snapshot(text)` admits at most 128 KiB of duplicate-key-free finite JSON.
The schema is `finite-grid-rays/v1` with only `schema`, `opaque`, and `rows`.
Imported rows must equal a **full geometric recomputation**. Booleans and
floating numbers cannot substitute for exact integer fields. Unknown metadata
is rejected. A hash or self-consistent cache is not geometric evidence.

## Hostile cases that remain part of the pack

- Equal first entry: cells `(1,0)` and `(1,1)` on ray `(0,5)` produce `MANY`.
- A forged empty cached row is rejected, including when a requested edit would
  otherwise leave that row untouched.
- Duplicate cells, out-of-grid cells, a fourth occluder, non-singleton MOVE,
  booleans, invalid numeric types, and extra/missing dirty rows are rejected.
- The first-hit-only deletion example separates current equality from future
  sufficiency.

## Baseline, costs, and coverage

The implementation compiles 864 ray/cell intersections once at module load,
then makes 864 contact-table probes to build reverse incidence.
It uses the ordinary closed-box slab intersection construction; see the
authors' [Physically Based Rendering, Basic Shape Interface](https://www.pbr-book.org/4ed/Shapes/Basic_Shape_Interface)
for the general ray/axis-aligned-box method. This pack specializes it to exact
2D rational segments. No code from that reference is included.

The baseline uses the **same precomputed contact table** and rebuilds all 36
rows. For a scene of size `m`, that means `36*m` table probes. The patch uses
`dirty_count*new_m` probes, but every public update first incurs `36*old_m`
probes and materializes 36 rows to validate ingress. It also returns 36 output
row references. The receipt exposes these separately, plus dirty row counts,
one-time intersection calls and serialized snapshot bytes. Allocation,
sorting, incidence construction and serialization time are not measured.

Thus a smaller patch count establishes **no total-cost or wall-time speedup**.
The conventional incidence-cache baseline receives the same dependency data.
An optimization study would need a specified trusted-state lifetime, measured
ingress, allocations, full requested output, and equal end-to-end results.

The cold checker independently computes contact intervals by collecting exact
boundary events and testing their coordinates, rather than intersecting slabs.
It covers all 864 ray/cell pairs, all 2,325 scenes, all 13,296 legal toggles, and
all 552 singleton moves and inverses. It compares every patch with the
independent full result and rejects MOVE on every non-singleton scene. These
are finite tests of this fixed context, not a proof about arbitrary scenes or
a complete renderer. Future work must declare new ray, geometry, material,
output, and performance contracts before transferring this result.
