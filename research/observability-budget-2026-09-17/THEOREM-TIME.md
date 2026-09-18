# Extra time cannot refine a descending panel

Let `X` be finite, `T:X→X` total, `C_S:X→O^k` a panel readout, and
`Q:X→D`. Say `S` **descends** under `T` when
`C_S(x)=C_S(y)` implies `C_S(Tx)=C_S(Ty)`.

Then `C_S(x)=C_S(y)` implies `C_S(T_w x)=C_S(T_w y)` for every finite
word `w`, by induction on length. The horizon-`b` trace is a function of
`C_S(x)`, so `ker C_S = ker(trace_b)`. Extra time cannot make `Q`
constant if `S` did not. The same holds for a finite action alphabet if
`S` descends under every letter.

A port `q` is **independent** of `S` when `q` is not a function of
`C_S`. Then `ker C_{S∪{q}}` may strictly refine `ker C_S`.

On L, all 31 nonempty panels descend under `tick`; horizon 3 never
refines. `{R,X}` works because `X` is independent of `{R}`. Hostile N:
`Y∘shift` reads `b`, not a function of `a`, so `{Y}` does not descend,
and horizon 2 of `Y` makes `Q=c` constant.

Not Lean. Not AD-R3. Not BSD. `reveal` is a different action family.
