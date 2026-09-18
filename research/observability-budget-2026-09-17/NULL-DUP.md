# Frozen nulls — port duplication (OB-dup)

Written **before** this packet's duplication enumerator was run. Do not
edit after `CENSUS.json` records Q6–Q8 except to note a later
supersession. Q1–Q5 stay as frozen in [NULL.md](NULL.md).

Not BSD, fluid, Hamming, AD-R3, or n=4 obstruction padding.

## Duplicate (frozen)

A port `p'` **duplicates** an already-supplied port `p` in panel `S`
exactly when:

- `p ∈ S` and `p' ∉ S`;
- both are total on the declared state carrier;
- `p'(x) = p(x)` for every state `x`.

Occurrence names may differ. A port that differs at even one state is
not a duplicate. Extra tick-time is not a duplicate. `reveal` is not a
duplicate.

Representation: the ordered tuple of port values, or the same tuple
after each admitted word. `Q` is a function of source state only.

**Q6 claim.** If `S` does not make `Q` constant on its fibers, then
`S ∪ {p'}` does not either.

## Machine L — four-state layer (already in NULL.md)

States `X = {(r,h)}`, `Q = h`, ports `{H,R,R2,X,Z}` with the same maps
as NULL.md. Fresh value-copies admitted for the test only:
`H2=H`, `R3=R`, `X2=X`, `Z2=Z`. `R2` is already a value-copy of `R`.

Trials: every nonempty `S ⊆ {H,R,R2,X,Z}` and every `p ∈ S`, add one
fresh value-copy of `p`. That is `5 · 2^4 = 80` trials. Empty `S` has
no already-supplied port and is excluded.

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_dup_never` | 0 of 80 insufficient `S` become sufficient | `C_{S∪{p'}}` is a function of `C_S` |
| `N_dup_repairs` | at least one repair | a new occurrence is a new coordinate |

If `N_dup_repairs` lands, the receipt must list `S`, `p`, and the
splitting pair that vanished.

## Machine M — named hostile lookalike

States `{0,1,2}` with integer equality.
`Q(s) = 1` if `s = 1`, else `0`.
Total ports, no actions:

| Port | `0` | `1` | `2` |
|---|---:|---:|---:|
| `A` | 0 | 0 | 1 |
| `A2` | 0 | 0 | 1 |
| `B` | 0 | 1 | 1 |

`A2` duplicates `A`. `B` agrees with `A` at `0` and `2` and differs at
the live ghost `1`. That is the load-bearing “already-supplied”
hypothesis, not a second copy of L.

| Name | `{A}` | `{A,A2}` | `{A,B}` |
|---|---|---|---|
| `N_look_copy` | insufficient | insufficient | sufficient |
| `N_look_any_second` | insufficient | sufficient | sufficient |
| `N_look_none` | insufficient | insufficient | insufficient |

## Q8 — duplicate under tick traces on L

Panel `{R}` versus `{R,R2}`, alphabet `{tick}`, horizon 3. Does adding
the value-copy make `Q` constant?

| Name | Predicted |
|---|---|
| `N_trace_copy_helps` | `{R,R2}` sufficient, `{R}` not |
| `N_trace_copy_never` | both insufficient |

## Out of scope

Partial ports with unequal domains called “copies,” occurrence-count
receivers, noisy maps, infinite carriers, Hamming panels, BSD, fluid.

## What would make this run OPEN

If any of the 80 L-trials is skipped, if `R` and `R2` are merged by
map-equality before the fiber is formed, if `B` is treated as a
duplicate of `A`, or if Q1–Q5 change their frozen dispositions, the
result is OPEN.
