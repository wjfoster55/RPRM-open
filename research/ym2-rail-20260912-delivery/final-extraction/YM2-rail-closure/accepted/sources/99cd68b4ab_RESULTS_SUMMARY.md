# Ternary Nested Handoff 01 - frozen result

Status: `PASS` on both non-importing exact implementations.

## Nested shear arm

For

```text
T(x,y,z) = (x+y, y+z, z+1) mod 3
```

the 27-state carrier splits into three cycles of length nine. The exact
closed form passed 729 state/time checks, `T^3(x,y,z)=(x+1,y,z)`, and `T^9`
is the identity. The inverse and the reverse nine-step orbit were checked on
all states. The six primitive orders form four distinct maps with only
`A,B,C` realizing the registered transition.

Nine canonical byte-content handoffs form one SHA-256 receipt chain. Steps
3 and 6 close the coarse receiver while retaining typed live outer residuals
1 and 2; step 9 clears the residual and closes the full receiver. The
contract proves equality of canonical bytes plus receipt lineage. It does not
claim Python object identity, and a byte-identical canonical reproduction is
observationally equivalent unless separately procedurally receipted.

The exact commutators are

```text
[B,C](x,y,z)       = (x,y+1,z)
[A,[B,C]](x,y,z)   = (x+1,y,z)
```

under the frozen `F o G o F^-1 o G^-1` convention. A typed
`MISSING_CELL` marker follows the same nine-step cycle, remains distinct from
field zero, and has nine exact rollback receipts.

## Base-3 odometer arm

The separate odometer is one 27-cycle. Its coordinate-change census is
`x=3`, `y=9`, `z=27`; its carry census is 18 no-carry, 6 carry-into-y, and 3
carry-into-x steps. All carries are neighbor carries. The level-3 to level-2
identity passed 27 checks, the level-2 to level-1 identity passed 9 checks,
and both quotient fibers have exact size three.

The odometer and nested shear remain distinct lawful machines: their orbit
partitions are `[27]` and `[9,9,9]`, respectively.

## Connected gap and spiral calibration

The frozen top-left, clockwise, center-last 3x3 removal order has retained
rank sequences

```text
AFFINE:   3,3,3,3,3,3,3,2,1,0
BILINEAR: 4,4,4,4,4,4,3,2,1,0
```

over exact rationals. Affine reconstruction therefore survives six spiral
removals and bilinear reconstruction survives five. Exact kernel witnesses
certify the next loss. The connected-subset census enumerated all 512 masks
per model. The first affine connected failures occur at missing size six in
four shapes, each retaining three collinear cells; the first bilinear shape
failures occur at missing size four in four shapes. All eight D4 symmetries
passed 8,192 coordinate-plus-basis transport checks.

## Controls and boundary

Both paths rejected all 55 registered mutations with their exact expected
codes and preserved `tree_delta=0` during normal replay. Strict canonical
JSON rejects duplicate keys, floats, nonfinite constants, Boolean/integer
aliases, and noncanonical encodings. The flat inventory, manifests, privacy,
and no-cache/no-reparse constraints are part of normal replay.

Two machine-readable Scouts remain deferred and contribute zero scored
evidence:

- the mixed-base/depth quotient identity for future bases 2 and 3;
- the rolling `(PAST,PRESENT,FUTURE)` boundary policy, which requires a
  supplied `next` and never assumes an unregistered successor.

This bench earns only the registered finite F3, receipt, vacancy, odometer,
and rational rank/census facts. It earns no biology, physics, universal
dimensional law, identity between the two machines, open-problem progress,
or scored Scout claim.

Replay independently:

```text
python -I -B run_ternary_nested_handoff.py
python -I -B check_ternary_nested_handoff.py
```
