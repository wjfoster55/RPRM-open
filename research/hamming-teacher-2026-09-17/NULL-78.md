# Frozen nulls — HT-78 three eights

Written **before** `verify_ht78.py` ran and before `CENSUS-78.json`
existed. Do not edit after that receipt except to mark a supersession.

The 28/35 injectivity-vs-line lemma is immediate (see [LEMMA.md](LEMMA.md)).
This cut is the next smallest recovered-concepts claim: four/eight source
roles versus seven teacher answers / eight simplex words versus Hamming
seven/eight. THEORY P9–P9b. Not BSD, not fluid, not O05, not SAT.

## Three typed uses of “eight”

Freeze these as different types even if some cardinalities match:

| Name | Carrier | What “8” counts |
|---|---|---|
| `S` | image of `E : F₂³ → F₂⁷`, `E(x)_u = u·x` for `u = 1..7` | teacher-answer words |
| `C8` | even-parity extensions of Hamming-7 words | codeword *positions* are 8; message count is a different port |
| `X_c` | `U ∪ (c+U)` for `U = span{1,2} = {0,1,2,3}` | source roles after a candidate toggle `c` |

Column labels `1..7` for `E` and for Hamming-7 are the same bitmasks.
That shared labeling is an adapter, not a proof that the objects coincide.

Hostile check panel `{1,2,3}` remains a *check* line. It is not the source
quartet `U`, and it is not an 8-position Hamming block.

## Question Q1 — simplex word count

**Q1.** How many distinct words does `E` produce?

| Name | Predicted | Guess |
|---|---:|---|
| `N_s7` | 7 | one word per teacher, forgetting the source |
| `N_s8` | 8 | THEORY P9a: `E` injective, `|S| = 8` |
| `N_s16` | 16 | collapse onto Hamming-7 message count |

## Question Q2 — duality

**Q2.** Is `S` equal to the orthogonal of Hamming-7 `C = ker H`?

| Name | Predicted |
|---|---|
| `N_dual_yes` | `S = C⊥` (P9a orthogonality) |
| `N_dual_no` | same length 7 is enough; duality fails |
| `N_s_is_c` | `S = C` (8 words equal 16 codewords) |

## Question Q3 — Hamming-8 messages

Append one overall-parity bit to each word of `C`. **Q3.** How many
extended codewords?

| Name | Predicted | Guess |
|---|---:|---|
| `N_ext8` | 8 | count positions, not messages |
| `N_ext16` | 16 | P9: determined parity, same 16 messages |
| `N_ext32` | 32 | treat the extra bit as a free source toggle |

## Question Q4 — free toggle

`U = {0,1,2,3}`. **Q4a.** Does `c = 4 ∉ U` give `|U ∪ (4+U)| = 8`?
**Q4b.** Does `c = 3 ∈ U` (namely `1⊕2`) expand `U`?

| Name | Q4a | Q4b | Guess |
|---|---|---|---|
| `N_any_c` | 8 | 8 | any fourth role expands |
| `N_no_c` | not 8 | not 8 | four roles cannot become eight |
| `N_p9b` | 8 | not 8 | independence required; `{1,2,3}` as *sources* stays inside `U` |

`c = 3` is the source-role reading of the same glyphs as hostile check
panel `{1,2,3}`. The null is that those readings are interchangeable.

## Question Q5 — one eight or three

**Q5.** After Q1–Q4, are `S`, `C8`, and a successful `X_4` the same
typed object (same carrier, same equality, same receiver)?

| Name | Predicted |
|---|---|
| `N_one_eight` | yes; matching counts license identification |
| `N_three_eights` | no; three carriers (P9 / P9a / P9b) |

## Out of scope

Double-error location fibers (THEORY P9, already written), SAT, k>3,
nonlinear checks, the silent ninth position, BSD, fluid, O05.

## OPEN conditions

If `E` is not enumerated on all 8 sources, if Hamming-7 is not enumerated
on all 128 words, or if a nonlinear “teacher” is substituted, the result
is OPEN, not a count.
