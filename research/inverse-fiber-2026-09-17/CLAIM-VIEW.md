# IF-v: extra readouts that split a MANY fiber to ONE

17 September 2026. Rank-7 discriminating-view cut. Nulls are frozen in
[NULL-VIEW.md](NULL-VIEW.md) and were written before this cut's
enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Bits2, Bits3, the
   named XOR=1 and C=(0,0) fibers, and the named view menus in
   NULL-VIEW. Tuple equality. Views are total maps to `{0,1}`.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   fiber and the view menu. Missing: which views split the fiber to
   ONE, and the refined fiber after one named extra bit. Readout is
   the complete splitting family, plus `NONE`/`ONE`/`MANY` of each
   named refinement.
3. **Operation kind, direction, enabledness.** Kind is observation.
   Direction is refinement of an already-computed fiber. Enabledness
   is total.
4. **Receiver.** Identity of the remaining source after the extra
   readout. A view that is constant on the fiber preserves the MANY
   ambiguity. Full source identity is requested only after a
   split-to-ONE view.
5. **Inverse / complete fiber.** The refined fiber is the complete
   subset of `F` with the supplied view value. `ONE` only if that
   subset is a singleton after a complete scan of `F`.
6. **Coverage, hostile case, evidence grade.** Coverage: every named
   view on every member of each named fiber. Hostile: AND/OR/EQ on
   XOR=1, and already-supplied `C0` on C=(0,0) — extra-looking
   readouts that do not split. Distinguishing control: FST and X do
   split to ONE. Grade: **finite exhaustive test**. Not Lean. Not a
   physics law.

## Claim

On XOR=1, exactly `FST` and `SND` from the named Bits2 menu split the
fiber to ONE; AND, OR, EQ, and CONST0 are constant. Supplying `FST=0`
leaves `ONE((0,1))`. On C=(0,0), exactly `X`, `Y`, `Z`, `PARITY`, and
`AND3` from the named Bits3 menu split to ONE; already-supplied `C0`
is constant. Supplying `X=0` leaves `ONE((0,0,0))`. An extra readout
that is constant on the fiber is not a discriminating view.

## What this is not

Not a minimum-view theorem over all Boolean functions. Not IF-j's
product-of-marginals claim. Not inverse graphics. Not a physics law.
