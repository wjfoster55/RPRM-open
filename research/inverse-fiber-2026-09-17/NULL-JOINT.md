# Frozen nulls — XOR/C fibers are not products of marginals

Written **before** this packet's joint enumerator was run. Do not edit
after `CENSUS-JOINT.json` exists except to record that a later task
superseded it.

Independent-math Rank 7 continuation: correlated missing ports stay
joint. Adjacent written source: handbook §3; core.md §5; IF-k Q3, Q6,
Q7, Q8, Q12. Not a rewrite of IF-k. Not BSD. Not a physics law.

The IF-k complete fibers are reused as named sets. This cut asks a
different question: whether those fibers equal the product of their
one-port marginals, and which extra pairs the product illegally adds.

## Carrier (frozen)

Same Bits2, Bits3, AND, XOR, C as [NULL.md](NULL.md). Tuple equality.

For a set `F` of ordered pairs, the one-bit marginals are

```text
A = {a : (a,b) in F}
B = {b : (a,b) in F}
```

and the product is `A×B` in lexicographic order. For triples, three
bit-marginals and their product. Extra illegal members are
`(A×B) \ F`, listed lexicographically.

A fiber **factors** iff `F = A×B` (or the three-way product). `NONE`
of equality means the fiber is not that product. Reconstructing by
choosing each missing port independently from its marginal is the
named hostile.

IF-k named fibers, treated as already-complete sets (not re-opened
searches):

```text
XOR1 = ((0,1),(1,0))
XOR0 = ((0,0),(1,1))
AND1 = ((1,1),)
C00  = ((0,0,0),(1,1,1))
C11  = ((0,1,1),(1,0,0))
```

## QJ1 — XOR=1 equals its product of marginals?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_xor1_joint` | no | handbook: correlation is not a product |
| `N_xor1_factor` | yes | each bit separately takes both values |

## QJ2 — extra illegal pairs in the XOR=1 product

| Name | Predicted extras |
|---|---|
| `N_xor1_extra_eq` | `((0,0),(1,1))` — the XOR=0 fiber |
| `N_xor1_extra_and` | `((1,1),)` only |
| `N_xor1_extra_none` | empty |

## QJ3 — C=(0,0) equals its product of three bit-marginals?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c00_joint` | no | IF-k already listed eight-vs-two |
| `N_c00_factor` | yes | each coordinate's marginal is `{0,1}` |

## QJ4 — extra illegal triples in the C=(0,0) product

| Name | Predicted extras |
|---|---|
| `N_c00_extra6` | the six triples not in `C00` |
| `N_c00_extra_none` | empty |
| `N_c00_extra_rep` | `((0,0,1),)` one representative extra |

## QJ5 — C=(1,1) equals its product of three bit-marginals?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_c11_joint` | no | same three `{0,1}` marginals |
| `N_c11_factor` | yes | reconstruct each bit independently |

## QJ6 — does the XOR=1 product admit `(1,1)`?

Hostile reconstruction: “first bit any of `{0,1}`, second bit any of
`{0,1}`.”

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_xor1_admits_11` | yes | `(1,1)` is in `{0,1}×{0,1}` and XOR maps it to 0 |
| `N_xor1_blocks_11` | no | a design for XOR=1 would not allow AND=1 |

## QJ7 — AND=1 equals its product of marginals? (control)

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_and1_equals` | yes | singleton `{1}×{1} = ((1,1),)` |
| `N_and1_never` | no | “no fiber equals its product” |

## QJ8 — do XOR=0 and XOR=1 share the same marginal product?

| Name | Predicted | Source of the guess |
|---|---|---|
| `N_xor_same_prod` | yes | both marginal pairs are `{0,1}×{0,1}` |
| `N_xor_diff_prod` | no | complementary fibers should have complementary products |

## Surviving-null test (frozen)

| Q | Surviving name | Rejected sibling(s) |
|---|---|---|
| QJ1 | `N_xor1_joint` | `N_xor1_factor` |
| QJ2 | `N_xor1_extra_eq` | `N_xor1_extra_and`, `N_xor1_extra_none` |
| QJ3 | `N_c00_joint` | `N_c00_factor` |
| QJ4 | `N_c00_extra6` | `N_c00_extra_none`, `N_c00_extra_rep` |
| QJ5 | `N_c11_joint` | `N_c11_factor` |
| QJ6 | `N_xor1_admits_11` | `N_xor1_blocks_11` |
| QJ7 | `N_and1_equals` | `N_and1_never` |
| QJ8 | `N_xor_same_prod` | `N_xor_diff_prod` |

## Out of scope

Discriminating-view selection, extra gates, inverse graphics, Lean, a
physics law, rewriting IF-k Q6 as this cut.

## What would make this run OPEN

If the enumerator imports `rprm`, if it treats pairs as unordered, if
it edits these predictions after `CENSUS-JOINT.json` exists, or if an
extra-illegal list is reported without listing every product member
outside the fiber, the result is OPEN.
