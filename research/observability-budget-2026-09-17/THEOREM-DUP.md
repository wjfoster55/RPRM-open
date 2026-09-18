# Restricted theorem — value-copy ports do not refine a panel

Written after the Q6–Q8 census. Nulls were frozen in
[NULL-DUP.md](NULL-DUP.md) at commit `f535cd0`.

## Domain

Finite nonempty state carrier `X`. Finite named ports, each a **total**
map `X → B`. A panel `S` is a finite set of port names. The
representation is `C_S(x) = (p(x) : p ∈ S)` in a fixed name order, or
the same tuple after each word of a declared action alphabet. Question
`Q: X → D` is a function of source state only.

Port `p'` **duplicates** `p ∈ S` when `p' ∉ S` and `p'(x) = p(x)` for
every `x ∈ X`. Lookalikes, later-time readings, and interventions are
outside this operation.

## Theorem

`C_{S ∪ {p'}}(x) = C_{S ∪ {p'}}(y)` if and only if `C_S(x) = C_S(y)`.
Therefore `Q` is constant on the fibers of `C_{S ∪ {p'}}` if and only if
it is constant on the fibers of `C_S`. In particular, a duplicate never
makes a previously non-constant `Q` constant.

## Proof

Write `C_{S ∪ {p'}}(x) = (C_S(x), p'(x))`. Because `p'` duplicates `p`
and `p ∈ S`, the coordinate `p'(x)` equals the already-recorded
coordinate `p(x)` and is therefore a function of `C_S(x)`. So
`(C_S(x), p'(x)) = (C_S(y), p'(y))` exactly when `C_S(x) = C_S(y)`.
The source partitions agree. Constancy of `Q` is a property of that
partition. The same argument applies wordwise to a trace representation:
each word repeats an already-recorded coordinate.

This is Manifesto II.2 / factorization applied to a representation that
factors through the old panel. It is not a new observability principle.

## Finite check

On machine L, 80 of 80 nonempty-panel value-copy trials left sufficiency
unchanged; repairs **NONE**. Tick-horizon 3 of `{R,R2}` stayed
insufficient. On hostile machine M, `{A}` and `{A,A2}` share the ghost
pair `{0,1}`; `{A,B}` is sufficient because `B(1) ≠ A(1)`, so `B` is
not a duplicate.

## What this does not cover

Partial ports with unequal domains, occurrence-count receivers, noisy
maps, infinite carriers, AD-R3 row spaces, Lean.
