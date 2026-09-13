# Independent block and carry review

Date: 2026-09-12. Reviewed [check_keyring.py](../work/check_keyring.py), [check_joint_seam.py](../work/check_joint_seam.py), [keyring.json](../evidence/keyring.json), and [joint-seam.json](../evidence/joint-seam.json). This review writes only this file. It does not rerun or independently prove the attributed height enclosures.

**Result: the declared block inverse, tagged carry formulas, source-record counts, and exact decimal boundary controls pass.** Preserve one counting distinction: the joint carrier has **2,100 source interval records**, representing **1,605 distinct normalized numerical intervals**. Its 1,100/1,000 split is a count of source records. No code correction is required for those stated counts.

## Fixed-width block inverse

For positive integer widths `w,m`, put `B=10^w` and `M=10^m`. On normalized records with nonnegative integer `I`, `0≤P<B`, and `0≤T<M`,

\[
V(I,P,T)=I+\frac{P}{B}+\frac{T}{BM},\qquad
BMV=BM I+MP+T.
\]

Euclidean division first by `BM` and then by `M` uniquely recovers `I,P,T`. This is exactly the two `divmod` operations in `recover`. Padding the two nonnegative remainders to widths `w,m` restores leading zeros. The inverse requires the fixed widths and an exact nonnegative rational value on the `1/(BM)` grid; the function's denominator assertion checks grid membership. The test calls supply the declared integer widths and carriers. These helpers are not claimed to be a general input-validation API.

For a joint normalized block `(I,P,(a,b))` with `0≤a≤b<M`, applying this inverse to both endpoints reconstructs the joint record; their recovered `(I,P)` agree by the source contract. The interval determines the record within this fixed-width source image. This statement does not extend to intervals whose endpoints have different normalized prefixes.

The four attributed endpoint words in `keyring.json` decode exactly as recorded:

| Depth | Joint eight-place tail block following `2.0340` |
|---|---|
| 9 | `01230068`, `10481998` |
| 10 | `04870820`, `07183803` |

The decimal strings and saved rational readbacks agree exactly. This checks the supplied numerical records and their positional decomposition, not the upstream height theorem or computation.

## Complete shape-label family: 5,050 intervals

The finite family is `I=2,P=340,w=4,m=2,0≤a≤b<100`. There are

\[
\sum_{a=0}^{99}(100-a)=\frac{100\cdot101}{2}=5050
\]

ordered endpoint pairs, including 100 degenerate intervals. Since each tail value maps injectively to a numerical endpoint, these are also 5,050 distinct numerical intervals. Both inverse readbacks passed for every pair. Describing this as one shape fiber is conditional on the declared representation assigning the same geometry to all those labels; the numeral count does not establish the topology.

## Tagged normalization: 200 source records

For the carry operation, write

\[
T=M c_T+T',\quad 0\le T'<M;
\qquad P+c_T=B c_I+P',\quad 0\le P'<B;
\qquad I'=I+c_I.
\]

Substitution proves `V(I,P,T)=V(I',P',T')`. Keeping `(cT,cI)` gives the exact inverse

\[
I=I'-c_I,\qquad P=P'+B c_I-c_T,\qquad T=T'+M c_T.
\]

The code implements these equations. The tested source carrier has `I=2,P=0..9,T=0..19,w=m=1`, hence `10·20=200` records. All saved normalized values and tags agreed with an independent scaled-integer calculation, and every tagged inverse recovered its original record.

These are **200 tagged source records but 110 distinct normalized numerical values**. For example, raw records `(2,0,10)` and `(2,1,0)` both normalize to `(2,1,0)`; their tail-carry tags differ. Thus untagged normalization is value-preserving but is not injective on the raw source carrier. The retained tags are sufficient; no minimality claim for those tags is needed.

## Joint carry seam: 2,100 source records

For each `P=0..9`, admit `0≤a≤b<20`. There are `20·21/2=210` tail pairs, giving `10·210=2100` source records. A tail below 10 has no tail carry; a tail from 10 through 19 has one. The two normalized prefixes differ exactly when

\[
a<10\le b.
\]

This remains true at `P=9`, where the upper prefix carries into the integer block. For each `P`, 10 choices of `a` and 10 of `b` straddle the seam, giving **1,000 split-prefix records**. The two nonstraddling triangular blocks have 55 pairs each, giving `10·(55+55)=` **1,100 same-prefix records**.

Distinct numerical intervals must be counted separately. Adjacent `P` frames overlap on ten endpoint values. Each adjacent pair therefore duplicates `10·11/2=55` same-prefix intervals. There are nine adjacent frame pairs and no triple overlap. Consequently:

| Receiver | Same prefix | Split prefix | Total |
|---|---:|---:|---:|
| Source interval records `(P,a,b)` | 1,100 | 1,000 | 2,100 |
| Distinct normalized numerical intervals | 605 | 1,000 | 1,605 |

For an explicit duplicate, `(P,a,b)=(0,10,11)` and `(1,0,1)` both denote `[2.10,2.11]`. This is the repository's distinction between equal values and equal occurrences. The code's `same` and `split` variables correctly count occurrences.

## Exact boundary at the actual widths

For `I=2,P=340,w=4,m=8`, the final tail before carry and the next raw tail give:

| Raw tail | Normalized blocks | Exact decimal word |
|---:|---|---|
| 99,999,999 | `(2,0340,99999999)` | `2.034099999999` |
| 100,000,000 | `(2,0341,00000000)` | `2.034100000000` |

Their difference is exactly `10^-12`. The second source tail needs nine digits and is outside the normalized eight-digit tail carrier; the declared carry buffer admits it. A single shared normalized middle word `0340` cannot represent this straddling pair. Endpoint-specific normalized prefixes or a retained common frame with extended raw offsets can represent it exactly.

The additional `(2,9999,100000000)` control normalizes to `(3,0000,00000000)` with tags `(1,1)`, as recorded. All these are **boundary controls at the same widths**, not new estimates for the actual height distance. The supplied depth-9 and depth-10 enclosures do not straddle this seam.

## Verification performed

Ran a read-only Python `-I -B` review using independent scaled integers as the normalization oracle, exact `Fraction` arithmetic for readbacks, and the supplied `check_keyring` functions for comparison. It completed with `PASS_INDEPENDENT_INTEGER_ORACLE` and independently obtained every count in the table above. The read-only review also checked all 200 saved carry rows, all 5,050 shape-label interval pairs, all 2,100 joint source records, the four attributed endpoint readbacks, and the two exact seam words.

Source bindings were checked against current bytes: `keyring.json` names the current `check_keyring.py` and `inputs/hooks12.json`; `joint-seam.json` names the current `check_joint_seam.py` and the same current `check_keyring.py`. The reviewed source hashes are:

- `check_keyring.py`: `e24e2c603e9389b30d8ff5906db133b4961eaf50d792c5be56a8093806198fe8`.
- `check_joint_seam.py`: `3f502a7d23c0bdc28a27aeeb02a432b7885a258dfdb71b9b321b0dc5fac4c343`.

These hashes identify reviewed bytes. The algebra and independent finite comparisons supply the arithmetic evidence. Height certification, any rule selecting the geometry from the labels, and the actual BSD operational comparison retain their prior claim ceilings.
