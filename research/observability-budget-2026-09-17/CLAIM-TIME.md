# OB-time: extra time vs an independent port

17 September 2026. Next cut after the 20-line duplicate-function proof.
Nulls are frozen in [NULL-TIME.md](NULL-TIME.md) and were written before
this packet's time enumerator ran.

## Task record

1. **Carrier.** L is the four-state layer; N is the eight-state shift
   `shift(a,b,c)=(b,c,0)`. Ports are functions, not names. Equality of
   ports is equality of functions `X→O`.
2. **Supplied / missing.** Supplied: all 31 nonempty L-panels, `tick`
   only, horizon 3; port `X` versus `{R}`; N-port `Y` and `shift` words
   of length `≤2`. Missing: which descending panels have extra time
   refine the static kernel, and whether an independent port or extra
   time is the repair.
3. **Operation.** Total `PARTIAL` maps `tick` and `shift`. `reveal` is
   excluded from Q9–Q11.
4. **Receiver.** L: `Q=h`. N: `Q=c`.
5. **Fiber.** Descent is `ker C_S ⊆ ker(C_S ∘ T)`. Trace sufficiency
   uses the same constancy rule as CLAIM.md.
6. **Hostile / grade.** Hostile N: `{Y}` does not descend, and extra
   time may repair. Grade: written kernel argument if Q9–Q10 match
   `N_all31` / `N_time_closed_never`; otherwise a listed counterexample.
   Finite exhaustive check on L and N. Not Lean. Not AD-R3. Not BSD.

## Claim

If `C_S ∘ T` is a function of `C_S`, extra time cannot refine `ker C_S`.
On L every nonempty panel descends under `tick`, so extra tick-time
never repairs; `{R,X}` can, because `X` is independent of `{R}`. On N,
`{Y}` does not descend under `shift`, so the descent hypothesis fails
and horizon 2 may make `Q` constant.
