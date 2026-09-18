# HT-28: three-check panels on `F₂³`

17 September 2026. Smallest first-party Hamming / liar-teacher finite cut
from `recovered-concepts/NEXT-PAPER-BACKLOG.md`. Independent of the 12
September SAT pilot. Nulls are frozen in [NULL.md](NULL.md) and were
written before this packet's enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Source carrier `V = F₂³`
   as integers `0..7` with bitwise XOR. Check type: nonzero vectors
   `u ∈ {1,…,7}` used as linear functionals, not as source roles and not
   as Hamming error positions. Equality is integer equality of these codes.
   Admitted context: exact arithmetic, deterministic views, complete
   enumeration of `C(7,3)` triples. Other fields, nonlinear checks, and
   incomplete search are out of carrier.
2. **Supplied ports, missing ports, requested readout.** Supplied: the
   seven checks and the 35 triples. Missing: which triples make the joint
   readout injective. Readout for Q1 is the integer count of injective
   triples. Readout for a named triple is its complete source fiber
   partition (NONE/ONE/MANY per answer word, after covering all 8 sources).
3. **Operation kind, direction, enabledness.** `PARTIAL` maps `ℓ_u : V → F₂`,
   total on this carrier. Direction is observation, not an update. No
   enabledness vacancy on these maps. Replacement of a third check is a
   change of panel, not an execution of a source toggle.
4. **Receiver.** Source identity `Q = id_V`. A panel preserves this
   receiver iff the joint readout is injective (THEORY P1 special case).
   Later operational student handoff (P3) is not requested here.
5. **Inverse / complete fiber.** For each triple `τ` and each 3-bit answer
   `y`, the fiber is `{x ∈ V : C_τ(x) = y}`. Report ONE only when that
   set is a singleton; MANY when several sources share `y`; empty answer
   words are recorded but do not count as source states. Q1 is ONE(n)
   after the 35-element census is complete. Q2 and Q4 are ONE(yes) or
   NONE after comparing two explicitly listed 7-sets.
6. **Coverage, hostile case, evidence grade.** Coverage: all 35 triples,
   all 8 sources, all 8 answer words.    Hostile case: `HOSTILE_LINE = {1,2,3}`
   (`{001,010,011}`). The identified source pair is a census readout, not
   a frozen prediction; THEORY P6's printed `{100,010,110}` is a different
   line of the same family. Distinguishing control: `SWAP_XOR = {1,2,5}`
   must not be silently treated as the same panel. Grade: **finite
   exhaustive test** of this carrier. Written proof already exists as
   THEORY P4–P6 / P9; this packet does not replace it and does not add a
   Lean declaration.

## Claim

On this carrier, the injective three-check panels are exactly the linearly
independent triples. The backlog sentence under test is: “exactly 28/35
triples preserve all eight states.” The historical phrase “scale back down
… with any of those seven” is the named null `N_any`, not the claim.

## What this is not

Not a proof that every historical “seven teachers” sentence means linear
`F₂` checks. Not Hamming-8. Not a free fourth source bit. Not a SAT
complexity bound. Not an edit of the published Manifesto.
