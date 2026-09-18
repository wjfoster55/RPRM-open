# OB-k: finite-budget sensor selection on the four-state layer

17 September 2026. Smallest Rank-2 cut from the independent mathematical
reading. Nulls are frozen in [NULL.md](NULL.md) and were written before
this packet's enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Source carrier
   `X={(r,h): r,h in {0,1}}` with pair equality. Ports are named
   occurrences of maps `X→{0,1}`; `R` and `R2` are distinct ports with
   equal values. Actions `tick` and `reveal` are total `PARTIAL` maps as
   frozen in NULL.md. Equality of panels is equality of unordered name
   sets. Exact integer bits only; no floats, no booleans-as-ints.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   five-port menu, budgets `k=1` and `k=2`, named hostile
   `HOSTILE_MORE={R,R2,Z}`, the tick-only horizon-3 trace, and the
   tick+reveal horizon-1 trace. Missing: which size-`k` panels make `Q=h`
   constant on the representation fiber. Readout is the complete
   sufficient-panel family, classified `NONE`/`ONE`/`MANY`.
3. **Operation kind, direction, enabledness.** Observation is a total
   readout, not an update. `tick` and `reveal` are total, so enabledness
   does not split states on this carrier. Direction is sensor selection
   (choose a panel) then representation (read the panel, optionally after
   a word).
4. **Receiver.** `Q(r,h)=h`. A representation preserves `Q` exactly when
   `Q` is constant on each representation fiber (Manifesto II.2 /
   factorization). Full source identity is not requested. Physical
   existence of `h` is not requested; the two-state `r`-only control in
   `docs/relational-layer.md` remains a coverage boundary.
5. **Inverse / complete fiber.** For each panel `S` and each answer word
   `y`, the fiber is `{x in X: C_S(x)=y}`. Sufficiency fails as soon as
   one occupied word has two sources with different `Q`. Q1 and Q4 return
   `ONE(n)` after a complete census of singletons and pairs. Q2 and Q3
   return `ONE(yes)` or `NONE`. Q5 returns `ONE(yes)` or `NONE`.
6. **Coverage, hostile case, evidence grade.** Coverage: all 4 sources,
   all 5 singletons, all 10 pairs, the named 3-port hostile, every tick
   word of length `≤3`, every `{tick,reveal}` word of length `≤1`.
   Hostile case: `HOSTILE_MORE` — more sensors that still do not
   separate. Distinguishing control: `{R,X}` must not be treated as
   another copy of `{R}`. Grade: **finite exhaustive test** of this
   carrier. Not Lean. Not AD-R3. Not a new control-theoretic principle.

## Claim

On this carrier, budget-1 sufficiency is exactly the singleton `{H}`.
Extra copies of `R` plus a constant remain insufficient. Extra tick-time
with only `R` remains insufficient. A completing second port `{R,X}` or
the `reveal` intervention can make `Q` constant without adding port `H`.

## What this is not

Not a proof that AD-R3 is new. Not sensor placement for a plant outside
these four states. Not a claim that `h` must exist because `R` is seen.
Not an edit of the published Manifesto.
