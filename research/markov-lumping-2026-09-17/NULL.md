# Frozen nulls — receiver-specific Markov-state coarse graining

Written **before** this packet's enumerator was run. Do not edit after
`CENSUS.json` exists except to record that a later task superseded it.

Independent-math Rank 3 from
`rprm-corpus-2026-09-17/03-independent-math-reading.md`: Markov-state
coarse graining for a fixed scientific receiver. This cut is the smallest
typed conjunction, not the Rank-3 novelty target (coarsest hitting /
path / intervention receiver). Adjacent written sources: Manifesto
Proposition IV.1.2 and the four-state matrices; AGENT_HANDBOOK §11
three-state rows. Not BSD. Not fluid. Not Hamming. Not O05. Not
observability-budget padding.

## Carrier (frozen)

Finite nonempty state set `S`. Homogeneous kernel `P` with exact
nonnegative `Fraction` entries, one row per state, each row summing to
`1`. Equality of states is name equality. Equality of masses is
`Fraction` equality. No floats.

A **partition** `C` is a surjective map `r:S→B`, written as a set of
nonempty blocks. Block-mass from `x` is

```text
K_x(b) = sum(P[x,y] for y with r(y)=b)
```

A **receiver** is a total map `Q:S→D`. Named **zero-rate ports** are
declared per chain; default ports are `enter_b` with rate `K_x(b)` for
each block `b`. Port `α` is **enabled** at `x` iff its rate is `>0`.

`C` is an **operational quotient for `Q`** iff all three hold:

1. `r(x)=r(y)` implies `Q(x)=Q(y)`
2. `r(x)=r(y)` implies `K_x=K_y` (strong lumpability)
3. `r(x)=r(y)` implies matching enabledness for every named port

The lumped kernel, when (2) holds, is `Qbar[r(x),b]=K_x(b)`. That
reduced matrix is not a physical law.

## Named chains (frozen)

**FairTwo.** `S={H,T}`.

```text
P[H,*] = (1/2, 1/2)
P[T,*] = (1/2, 1/2)
```

`C_merge={{H,T}}`. `Q_const=0`. `Q_id` is identity.

**AbsorbingTwo.** `S={L,D}`.

```text
P[L,*] = (1/2, 1/2)
P[D,*] = (0,   1)
```

`C_merge={{L,D}}`. `Q_const=0`. Named extra port `enter_L` with rate
`P[x,L]`.

**ManifestoFour-P.** `S={a,b,c,d}`, Manifesto IV.1 successful matrix,
row/column order `a,b,c,d`:

```text
P[a,*] = (1/2, 1/4, 1/4, 0)
P[b,*] = (1/4, 1/2, 0,   1/4)
P[c,*] = (1/4, 0,   1/2, 1/4)
P[d,*] = (0,   1/4, 1/4, 1/2)
```

`C_AB={{a,b},{c,d}}`. `C_fine={{a},{b},{c,d}}`.
`C_diag={{a,c},{b,d}}`. `Q_color` is `0` on `{a,b}` and `1` on `{c,d}`.
`Q_split` is `0` on `{a,c}` and `1` on `{b,d}`. Default `enter_b` ports.

**ManifestoFour-Ptilde.** Same `S` and named partitions; Manifesto IV.1
failed matrix:

```text
Pt[a,*] = (1/2, 1/4, 1/4, 0)
Pt[b,*] = (1/4, 3/4, 0,   0)
Pt[c,*] = (1/4, 0,   1/2, 1/4)
Pt[d,*] = (0,   0,   1/4, 3/4)
```

**HandbookThreeSkew.** `S={a,b,c}`. Handbook §11 absorbing third state,
with the `b`-row skewed so both `a` and `b` can enter `B={c}`:

```text
Ps[a,*] = (1/2, 1/4, 1/4)
Ps[b,*] = (1/8, 1/8, 3/4)
Ps[c,*] = (0,   0,   1)
```

`C_AB={{a,b},{c}}`. `Q_color` is `0` on `{a,b}` and `1` on `{c}`. Named
port `enter_B` with rate `K_x(B)`.

## Q1 — FairTwo merge, constant receiver

Is `C_merge` an operational quotient for `Q_const`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_fair_yes` | yes | equal rows, constant Q |
| `N_fair_no` | no | two states are never one |

## Q2 — FairTwo merge, identity receiver (vice versa)

Is `C_merge` an operational quotient for `Q_id`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_fair_lump` | yes | strong lumpability is enough |
| `N_fair_qfail` | no | Q splits the only block |

## Q3 — AbsorbingTwo merge, constant receiver (hostile)

Is `C_merge` an operational quotient for `Q_const`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_abs_qenough` | yes | Q is constant, so fold |
| `N_abs_mass` | no | `K_L(D)=1/2` and `K_D(D)=1` |

## Q4 — AbsorbingTwo `enter_L` enabledness

Do `L` and `D` match on port `enter_L`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_abs_en_yes` | yes | both rows are stochastic |
| `N_abs_en_no` | no | `P[L,L]=1/2>0` and `P[D,L]=0` |

## Q5 — ManifestoFour-P, `C_AB`, `Q_color`

Is `C_AB` an operational quotient for `Q_color` on `P`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_p_yes` | yes | Manifesto IV.1 written success |
| `N_p_no` | no | four states need four blocks |

## Q6 — ManifestoFour-P, `C_AB`, `Q_split` (vice versa)

Is `C_AB` an operational quotient for `Q_split` on `P`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_p_lump` | yes | `C_AB` is strongly lumpable |
| `N_p_qfail` | no | `Q_split(a)=0` and `Q_split(b)=1` |

## Q7 — ManifestoFour-P, `C_fine`, `Q_color` (hostile)

Is `C_fine` an operational quotient for `Q_color` on `P`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_fine_qenough` | yes | Q-constant: `{c,d}` is one color |
| `N_fine_mass` | no | `K_c({a})=1/4` and `K_d({a})=0` |

## Q8 — ManifestoFour-P, `C_diag`, `Q_color` (vice versa)

Is `C_diag` an operational quotient for `Q_color` on `P`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_diag_lump` | yes | equal block-masses on the diagonal |
| `N_diag_qfail` | no | `Q_color(a)=0` and `Q_color(c)=1` |

## Q9 — ManifestoFour-Ptilde, `C_AB`, `Q_color` (hostile)

Is `C_AB` an operational quotient for `Q_color` on `Pt`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_pt_same` | yes | same Q-constant blocks as P |
| `N_pt_mass` | no | Manifesto: start-`a` next-B is `1/4`, start-`b` is `0` |

## Q10 — ManifestoFour-Ptilde `enter_B` enabledness

Do `a` and `b` match on `enter_B` under `C_AB`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_pt_en_yes` | yes | both can leave A somehow |
| `N_pt_en_no` | no | `K_a(B)=1/4>0` and `K_b(B)=0` |

## Q11 — HandbookThreeSkew `enter_B` enabledness

Do `a` and `b` match on `enter_B`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_sk_en_yes` | yes | `1/4>0` and `3/4>0` |
| `N_sk_en_no` | no | different rates cannot both count as enabled |

## Q12 — HandbookThreeSkew operational?

Is `C_AB` an operational quotient for `Q_color` on `Ps`?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_sk_support` | yes | equal supports of next-block, Q constant |
| `N_sk_mass` | no | `K_a(B)=1/4` and `K_b(B)=3/4` |

## Surviving-null test (frozen)

The enumerator must return the named prediction below, or the claim is
restricted / the surviving name is recorded as dead. Attractive errors
are the rejected siblings.

| Q | Surviving name | Rejected sibling |
|---|---|---|
| Q1 | `N_fair_yes` | `N_fair_no` |
| Q2 | `N_fair_qfail` | `N_fair_lump` |
| Q3 | `N_abs_mass` | `N_abs_qenough` |
| Q4 | `N_abs_en_no` | `N_abs_en_yes` |
| Q5 | `N_p_yes` | `N_p_no` |
| Q6 | `N_p_qfail` | `N_p_lump` |
| Q7 | `N_fine_mass` | `N_fine_qenough` |
| Q8 | `N_diag_qfail` | `N_diag_lump` |
| Q9 | `N_pt_mass` | `N_pt_same` |
| Q10 | `N_pt_en_no` | `N_pt_en_yes` |
| Q11 | `N_sk_en_yes` | `N_sk_en_no` |
| Q12 | `N_sk_mass` | `N_sk_support` |

## Out of scope

Approximate lumpability, total-variation bounds, infinite carriers,
continuous-time generators as a separate type, molecular MSM comparison,
hitting / path / intervention receivers beyond `Q` and `enter_b`, Lean,
a new physics law, a general advantage theorem against ordinary
lumpability software.

## What would make this run OPEN

If any row is not an exact `Fraction` summing to `1`, if the enumerator
imports `rprm` or another research tree, if `P` and `Pt` are swapped, if
Q7 uses `{c,d}` as singletons, or if a prediction is edited after
`CENSUS.json` exists, the result is OPEN, not a yes/no.
