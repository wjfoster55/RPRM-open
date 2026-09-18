# OB-dup: value-copy ports do not refine a panel

17 September 2026. Restricted theorem candidate on the Rank-2 sensor
menu. Nulls are frozen in [NULL-DUP.md](NULL-DUP.md) and were written
before this packet's duplication enumerator ran.

## Task record

1. **Carrier, types, equality, admitted context.** Machine L is the
   four-state layer of [CLAIM.md](CLAIM.md). Machine M is
   `{0,1,2}` with the three named ports in NULL-DUP.md. Ports are named
   occurrences of total maps. A duplicate is a distinct name with an
   identical value table, not a lookalike and not a later-time reading.
2. **Supplied ports, missing ports, requested readout.** Supplied: every
   nonempty L-panel from `{H,R,R2,X,Z}` and a fresh value-copy of each
   of its members (80 trials); M-panels `{A}`, `{A,A2}`, `{A,B}`;
   tick-horizon-3 traces of `{R}` and `{R,R2}`. Missing: whether any
   insufficient panel becomes sufficient after a true duplicate.
   Readout: repair count on L, three M dispositions, one trace
   comparison.
3. **Operation kind, direction, enabledness.** Observation only. All
   named ports and `tick` are total. No enabledness vacancy on this
   cut.
4. **Receiver.** L uses `Q=h`. M uses `Q(s)=[s=1]`. Sufficiency is
   constancy of `Q` on representation fibers.
5. **Inverse / complete fiber.** Same fiber rule as CLAIM.md. Q6 is
   `NONE` (zero repairs) or `ONE(counterexample)` with the listed
   `S`, `p`, and vanished pair. Q7 reports each M-panel as sufficient
   or not. Q8 is `ONE(yes)` or `NONE` for the copied trace panel.
6. **Coverage, hostile case, evidence grade.** Coverage: 80 L-trials,
   all 3 M-states, all 3 M-panels, both tick traces. Hostile machine M:
   `B` looks like `A` off the ghost and is **not** a duplicate. Grade:
   written factorization on the stated representation contract, plus
   finite exhaustive check. Not Lean. Not AD-R3.

## Claim

On this representation contract, adjoining a value-copy of an
already-supplied port yields the same source partition, so it cannot
make a previously non-constant `Q` constant. If the enumerator finds
zero L-repairs and `{A,A2}` stays insufficient while `{A,B}` becomes
sufficient, the claim is a **restricted theorem** on these two
machines and the written factorization that covers every finite total
port menu of this kind. If any L-trial repairs, the claim is **NONE**
and the numbers are the counterexample.
