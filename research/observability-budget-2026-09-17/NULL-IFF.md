# Frozen nulls — when extra time refines Q

Written **before** Q14–Q16 ran. Not BSD. Stop after this iff: do not
open another budget-k family.

## Claim (frozen)

On a finite carrier, total actions, and panel functions `C_S`, extra
time **weakly refines Q** at horizon `b` iff there exist states `x,y`
and a word `w` of length at most `b` with

`C_S(x)=C_S(y)`, `Q(x)≠Q(y)`, and `C_S(T_w x)≠C_S(T_w y)`.

It **repairs Q** when `ker C_S ⊈ ker Q` and `ker(trace_b) ⊆ ker Q`.

Descent (`C_S ∘ T` a function of `C_S`) forbids both, for every `b`.
Descent failure is **not** enough: the later observation must hit a
present **Q-ghost**, not only some other pair. That is the whole claim.
It is not a new shift-homomorphism theorem.

## Q14 — machine L, `tick` only, horizon 3

How many of the 31 nonempty panels weakly refine `Q=h`?

| Name | Predicted |
|---|---:|
| `N_l_none` | 0 |
| `N_l_some` | ≥1 |

## Q15 — machine M, identity action, panel `{A}`, any horizon

Does extra time weakly refine `Q=[s=1]`?

| Name | Predicted |
|---|---|
| `N_m_id_none` | no (`A ∘ id = A`) |
| `N_m_id_yes` | yes |

## Q16 — hostile `{Y}` on the shift, `Q=c`

| Name | horizon 1 weakly refines Q | horizon 2 repairs Q |
|---|---|---|
| `N_y_delay` | no | yes |
| `N_y_immediate` | yes | yes |
| `N_y_never` | no | no |

`N_y_delay` is the guess that `Y∘shift` splits equal-`a` pairs with
different `b` (descent fails) while the live Q-ghost `(000),(001)`
still agrees on the first successor `Y`.

## Out of scope

Another port-menu census, AD-R3, BSD, `reveal` as a third L-action in
Q14. After Q14–Q16, write the standalone note and stop.
