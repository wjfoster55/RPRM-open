# Frozen nulls — F₂⁴ lift of HT-28

Written **before** any F₂⁴ enumerator on this branch ran. If the surviving
null is just “rank `< 4`”, the lift is not a new cut. Stop padding.

## Carrier

Source `V = F₂⁴`, sixteen vectors, integers `0..15` with XOR. Checks: the
fifteen nonzero linear functionals. Objects: the `C(15,4) = 1365`
unordered 4-sets of distinct checks. Readout injective iff every source
has a unique 4-bit answer word.

Hostile 4-set, frozen here: `{1,2,3,4}` (bitmasks `0001,0010,0011,0100`).
This extends the HT-28 line `{1,2,3}` by one new coordinate.

## Named nulls

| Name | Predicted | Guess |
|---|---|---|
| `N_any` | all 1365 inject | “any four of the fifteen” |
| `N_fano_only` | exactly 7 fail | the F₂³ lines lift unchanged |
| `N_rank` | a 4-set injects iff its labels span `F₂⁴` | the same P4 fact as for `k = 3` |

`N_rank` is the honest analog. Confirming it is not a new theorem.

## Stop condition

If the exact check agrees with `N_rank` on every 4-set, including the
hostile, **do not** open an HT-24 campaign. Record the matching
`|GL(4,2)|/4!` count as a derived integer, write the standalone
coding-theory note, and stop.
