# Frozen nulls — discriminating-view selection on named MANY fibers

Written **before** this packet's view enumerator was run. Do not edit
after `CENSUS-VIEW.json` exists except to record that a later task
superseded it.

Independent-math Rank 7 continuation: which extra readout splits a
MANY fiber to ONE. Adjacent written source: Manifesto II.2
factorization; IF-k Q3/Q7; IF-j extras. Not BSD. Not a physics law.
Not certified outer bounds.

## Carrier (frozen)

Same Bits2, Bits3, XOR, C as [NULL.md](NULL.md). Named complete fibers:

```text
XOR1 = ((0,1),(1,0))
C00  = ((0,0,0),(1,1,1))
```

A **view** is a named total readout on the ambient domain. On a fiber
`F` it restricts to `D|_F`.

- `D` **splits** `F` iff `D` is not constant on `F`.
- `D` **splits `F` to ONE** iff each value of `D` on `F` has exactly
  one preimage in `F` (equivalently `D|_F` is injective).
- If `D` is constant on `F`, the refined fiber is still `F` (MANY).

On a two-point fiber with values in `{0,1}`, split and split-to-ONE
coincide. That is a fact about these fibers, not a general theorem.

Named Bits2 menu, in this order: `FST`, `SND`, `AND`, `OR`, `EQ`,
`CONST0`.

```text
FST(a,b)=a
SND(a,b)=b
AND(a,b)=1 iff a=1 and b=1
OR(a,b)=1 iff a=1 or b=1
EQ(a,b)=1 iff a=b
CONST0(a,b)=0
```

Named Bits3 menu, in this order: `X`, `Y`, `Z`, `PARITY`, `AND3`,
`C0`.

```text
X(x,y,z)=x
Y(x,y,z)=y
Z(x,y,z)=z
PARITY(x,y,z)=x XOR y XOR z
AND3(x,y,z)=1 iff x=y=z=1
C0(x,y,z)=x XOR y
```

`C0` is the first component of the already-supplied readout `C`. It
is a hostile “more of the same.”

A refined fiber after supplying `D=d` is `{p in F: D(p)=d}`.
`NONE`/`ONE`/`MANY` only after listing every remaining member of `F`.

## QV1 — which Bits2 views split XOR=1 to ONE?

| Name | Predicted family |
|---|---|
| `N_xor1_fst_snd` | `(FST,SND)` |
| `N_xor1_all6` | all six |
| `N_xor1_and` | `(AND,)` |
| `N_xor1_none` | empty |

## QV2 — does AND split XOR=1?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_and_const` | no | AND=0 on both members |
| `N_and_splits` | yes | an extra gate always helps |

## QV3 — does OR split XOR=1?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_or_const` | no | OR=1 on both members |
| `N_or_splits` | yes | OR sees a 1 somewhere |

## QV4 — does FST split XOR=1 to ONE?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_fst_one` | yes | `FST(0,1)=0` and `FST(1,0)=1` |
| `N_fst_many` | no | two sources remain two sources |

## QV5 — XOR=1 refined by FST=0

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_fst0_one` | `ONE((0,1))` | only that pair has first bit 0 |
| `N_fst0_many` | still both | FST does not forget the second bit |
| `N_fst0_none` | `NONE` | XOR=1 forbids first bit 0 |

## QV6 — which Bits3 views split C=(0,0) to ONE?

| Name | Predicted family |
|---|---|
| `N_c00_xyzpa` | `(X,Y,Z,PARITY,AND3)` |
| `N_c00_x_only` | `(X,)` |
| `N_c00_all6` | all six including `C0` |
| `N_c00_none` | empty |

## QV7 — does already-supplied C0 split C=(0,0)?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c0_const` | no | both members have `C0=0` |
| `N_c0_splits` | yes | more of C is more information |

## QV8 — C=(0,0) refined by X=0

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_x0_one` | `ONE((0,0,0))` | `(1,1,1)` has X=1 |
| `N_x0_many` | still both | X is only one of three bits |
| `N_x0_none` | `NONE` | C=(0,0) forbids X=0 |

## Surviving-null test (frozen)

| Q | Surviving name | Rejected sibling(s) |
|---|---|---|
| QV1 | `N_xor1_fst_snd` | `N_xor1_all6`, `N_xor1_and`, `N_xor1_none` |
| QV2 | `N_and_const` | `N_and_splits` |
| QV3 | `N_or_const` | `N_or_splits` |
| QV4 | `N_fst_one` | `N_fst_many` |
| QV5 | `N_fst0_one` | `N_fst0_many`, `N_fst0_none` |
| QV6 | `N_c00_xyzpa` | `N_c00_x_only`, `N_c00_all6`, `N_c00_none` |
| QV7 | `N_c0_const` | `N_c0_splits` |
| QV8 | `N_x0_one` | `N_x0_many`, `N_x0_none` |

## Out of scope

Minimum-view search over all Boolean functions, information-theoretic
bounds, inverse graphics, SAT, Lean, a physics law, extra gates beyond
the named menus.

## What would make this run OPEN

If the enumerator imports `rprm`, if a constant view is labelled a
splitter, if a refined fiber is reported without listing every remaining
member of `F`, or if these predictions are edited after
`CENSUS-VIEW.json` exists, the result is OPEN.
