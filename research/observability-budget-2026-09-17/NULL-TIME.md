# Frozen nulls — extra time vs extra independent port

Written **before** this packet's time/independence enumerator was run.
Do not edit after `CENSUS.json` records Q9–Q13 except to note a later
supersession. Q1–Q8 stay as already frozen. Not BSD.

## Descent (frozen)

Panel `S` **descends** under total action `T` when `C_S ∘ T` is a
function of `C_S`: `C_S(x)=C_S(y)` implies `C_S(T x)=C_S(T y)`.
Port `q` is **independent** of `S` when `q` is not a function of `C_S`.

**Claim.** If `S` descends under every admitted action, then every
finite-horizon trace of `S` has the same joint kernel as `C_S`. Extra
time cannot make `Q` constant if `S` did not. An independent port may.

## Machine L — four-state layer, action `tick` only

Same `X`, `Q=h`, ports `{H,R,R2,X,Z}` as NULL.md. `reveal` is **not**
admitted in Q9–Q11.

### Q9 — how many of the 31 nonempty L-panels descend under `tick`?

| Name | Predicted | Source of the guess |
|---|---:|---|
| `N_all31` | 31 | each named map after `tick` is a function of its present value |
| `N_sing5` | 5 | only singletons descend |
| `N_none` | 0 | flip mixes the bits |

### Q10 — among descending insufficient panels, does horizon-3 refine `ker C_S`?

| Name | Predicted |
|---|---|
| `N_time_closed_never` | no: every such trace kernel equals the static kernel |
| `N_time_closed_sometimes` | at least one descending insufficient panel is repaired by time |

### Q11 — is `X` a function of `{R}`? Does `{R,X}` make `Q` constant?

| Name | `X` of `{R}` | `{R,X}` sufficient |
|---|---|---|
| `N_port_indep` | no | yes |
| `N_port_dep` | yes | yes |
| `N_port_fail` | no | no |

## Machine N — named hostile shift

States `{(a,b,c): a,b,c in {0,1}}`. `Q(a,b,c)=c`.
Port `Y(a,b,c)=a`. Total `shift(a,b,c)=(b,c,0)`.
No other ports. This is the load-bearing “extra time can help”
hypothesis, not a relabeling of L.

### Q12 — `{Y}` static vs `{Y}` after `shift`-words of length ≤2

| Name | static `{Y}` | horizon-2 `{Y}` |
|---|---|---|
| `N_shift_time` | insufficient | sufficient |
| `N_shift_none` | insufficient | insufficient |
| `N_shift_already` | sufficient | sufficient |

### Q13 — does `{Y}` descend under `shift`?

| Name | Predicted |
|---|---|
| `N_shift_open` | no (`Y∘shift` reads `b`, not a function of `a`) |
| `N_shift_closed` | yes |

## Out of scope

`reveal` on L, AD-R3, Kalman rank, BSD, fluid, Hamming, partial actions.

## What would make this run OPEN

If any of the 31 L-panels is skipped, if `reveal` is admitted in Q9–Q11,
if machine N is replaced by L, or if Q1–Q8 dispositions change, OPEN.
