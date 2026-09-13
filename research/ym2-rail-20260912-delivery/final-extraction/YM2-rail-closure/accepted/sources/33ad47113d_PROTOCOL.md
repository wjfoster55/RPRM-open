# RPRM Ternary Nested Handoff 01 - exact protocol

Experiment ID: `RPRM_TERNARY_NESTED_HANDOFF_01`  
Status: exact finite F3 handoff, odometer, and rational gap calibration  
Date: 2026-08-11

## Two distinct ternary machines

The common carrier is `F3^3`, frozen in lexicographic `(x,y,z)` order. The
bench keeps two transition systems separate.

### Nested shear

```text
T(x,y,z) = (x+y, y+z, z+1) mod 3.
```

It is the ordered application `A,B,C`, equivalently `C o B o A`, where A adds
y into x, B adds z into y, and C increments z. The six written orders produce
four distinct maps; only `A,B,C` is the registered T. Its exact inverse is

```text
T^-1(x,y,z) = (x-y+z-1, y-z+1, z-1) mod 3.
```

Both paths verify the maps and inverse on all 27 states. The operational path
iterates primitive functions; the checker composes homogeneous affine
matrices over F3.

The closed form is

```text
z_t = z + t
y_t = y + t*z + C(t,2)
x_t = x + t*y + C(t,2)*z + C(t,3)       mod 3.
```

Finite exhaustive equality and the symbolic Pascal recurrence are separate
checks. The exact period facts are `T^3(x,y,z)=(x+1,y,z)`, `T^9=id`, and no
positive power below nine is identity. The carrier has three disjoint
nine-cycles. The frozen snake includes its start and return, hence ten listed
states but nine transitions and nine distinct orbit states.

### Base-three odometer

```text
value(x,y,z) = 9*x + 3*y + z
O(x,y,z) = digits_base3((value+1) mod 27).
```

This is one 27-cycle. Across its 27 source states, z changes 27 times, y nine
times, and x three times. Carry classes are 18 no-carry, six carry-into-y,
and three carry-into-x. Carry is adjacent: z may promote y and y may promote
x; no transition skips, drops, or doubles a promotion.

For the analogous O2 on `(x,y)` and O1 on x,

```text
project_xy(O^3(s)) = O2(project_xy(s))
project_x(O2^3(u)) = O1(project_x(u)).
```

Each projection has exact fiber size three. This is the scored 3-to-1
quotient compression. The shear and odometer orbit partitions are not merged.

## Receiver-relative closure and typed residual

The coarse receiver reads `(y,z)`; the full receiver reads `(x,y,z)`. At
steps three and six the coarse receiver has returned to its source value, but
the full state retains outer phase one or two. At step nine the full state
closes.

Every step uses exactly one of these typed contracts:

```text
OPEN
  {"kind":"NOT_AT_COARSE_BOUNDARY"}

COARSE_CLOSED_WITH_LIVE_OUTER_RESIDUAL
  {"kind":"LIVE_OUTER_PHASE","value":1 or 2}

FULLY_CLOSED
  {"kind":"CLEARED","value":0}
```

Null, field zero, and a live outer phase are not aliases.

## Literal nine-step handoff

A state artifact is canonical ASCII JSON with exact keys:

```text
artifact_type, machine, state, step
```

Its root is `sha256:` followed by uppercase SHA-256 of those exact canonical
bytes. Step `t+1` consumes bytes equal to the canonical output artifact bytes
from step `t`, and the receipt chain binds that content lineage. Semantic-only
reconstruction with different or noncanonical bytes is rejected. A
byte-identical canonical reproduction is observationally equivalent under this
content-hash contract unless a separate procedural receipt distinguishes it;
Python allocation or object identity is not claimed or tested.

Each receipt binds:

```text
coarse_status
input_root and input_state
outer_phase_residual
output_root and output_state
prior_receipt_root
receipt_type
step
```

The first prior root is the typed genesis
`{"kind":"GENESIS","value":"NESTED_SHEAR_HANDOFF_V1"}`. Later prior roots
are typed SHA-256 roots of the preceding canonical receipt. The fixture pins
all ten state roots and all nine receipt roots. Reverse application of T^-1
walks the same orbit backward and restores the source state.

## Relation among operations

With `[F,G]=F o G o F^-1 o G^-1`, both paths derive rather than look up:

```text
[B,C](x,y,z)     = (x,y+1,z)
[A,[B,C]](x,y,z) = (x+1,y,z).
```

The second commutator equals the outer translation emitted by T cubed. This
is an exact finite operation identity, not a path-coherence or physics claim.

## Moving typed vacancy

The vacancy marker is a structured `MISSING_CELL` with a location and payload
ID. It is never field zero. T transports its location through the frozen
nine-cycle while the payload remains bound. Each inverse rollback receipt
binds source location, destination location, payload, and forward step. The
fixture pins all marker and rollback roots. Only one vacancy moves; no growing
erasure trail is modeled.

## Exact 3x3 connected-gap calibration

The spiral order is no longer implicit. It is top-left, clockwise around the
outside, then center:

```text
(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),
(-1,-1),(-1,0),(0,0).
```

For retained cells, exact rank over Q is computed for:

```text
AFFINE:   1,x,y
BILINEAR: 1,x,y,x*y.
```

The frozen spiral ranks are respectively

```text
3,3,3,3,3,3,3,2,1,0
4,4,4,4,4,4,3,2,1,0.
```

Thus affine reconstruction survives six missing prefix cells and bilinear
reconstruction survives five. The next removal has a nonzero kernel
polynomial: `y` for affine and `y+x*y` for bilinear. Each vanishes on every
retained cell and not on the newly removed cell, giving an exact collision
between zero and that polynomial.

Every one of the 512 missing subsets is grouped by size and tested for
edge-connectivity, with the empty set connected by frozen convention. The
connected/recoverable censuses in the fixture are derived exactly. The four
affine size-six failures retain three collinear cells; bilinear shape
dependence begins with four missing cells.

All eight D4 symmetries transport coordinates, the ordered gap, model basis,
kernel witness, payload IDs, and rollback locations together. The affine and
bilinear spans are invariant under these signed coordinate permutations, but
that does not license silently omitting the basis/witness receipt: a frozen
coordinates-only mutation fails the transported witness equation.

## Implementations, mutations, and integrity

The primary runner uses operational transitions, direct orbit walks, literal
artifact bytes, direct commutator execution, rational Gaussian elimination,
and flood-fill connected subsets.

The checker does not import it. It uses affine matrices and permutation
powers over F3, component decomposition, Bareiss/minor rank, explicit
projection fibers, and independent D4 transport equations.

Both parse canonical JSON independently; reject duplicate keys, floats,
nonfinite constants, Boolean/integer aliases, and schema drift; and reject all
registered transition, receipt, vacancy, gap, odometer, claim, and virtual
integrity mutations with exact codes. Normal replay verifies exact source and
distribution manifests, a flat regular-file inventory, privacy, no cache or
reparse entries, checked-in result equality, and `tree_delta=0`.

Replay:

```text
python -I -B run_ternary_nested_handoff.py
python -I -B check_ternary_nested_handoff.py
```

## Deferred Scout and claim clamp

The machine-readable mixed-base/depth identity

```text
q o O_(b,n)^b = O_(b,n-1) o q
```

is registered only as a deferred future comparison for bases two and three.
It contributes no scored evidence here.

A second unscored boundary Scout types a rolling
`(PAST, PRESENT, FUTURE)` window. Shifting it requires a supplied `next`.
At a horizon the only registered statuses are `WRAP_PERIODIC`,
`PROMOTE_CARRY_TO_COARSER_CLOCK`, `GENERATE_UNDER_REGISTERED_RULE`, and
`MISSING_FUTURE`; the bench never assumes an unregistered successor. This
Scout likewise contributes zero scored evidence.

A pass establishes only the registered finite F3 shear and odometer facts,
canonical receipt chain, one moving vacancy, and rational 3x3 rank/census
facts. It does not establish biology, physics, a universal dimensional law,
an identity between shear and odometer, a scored mixed-base result, or
progress on any open problem.
