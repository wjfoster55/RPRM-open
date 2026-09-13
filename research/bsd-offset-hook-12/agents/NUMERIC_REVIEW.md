# Independent review of hook models and normalized offsets

Date: 2026-09-12 local. Disposition: **PASS at the declared finite-model and interval-transformation scope.** No correction to the reviewed files was needed. The exact height recurrence was not rerun, as requested; the new depth-10 enclosure remains evidence from the parent run. This review independently checked its rational coordinate transformations, outward displays, and comparisons with depth 9.

Reviewed read-only:

- [check_hooks.py](C:/github/RPRM-open/research/bsd-offset-hook-12/work/check_hooks.py)
- [hooks.json](C:/github/RPRM-open/research/bsd-offset-hook-12/evidence/hooks.json)
- The decimal and square-root helpers and ledger contract in [height_kernel.py](C:/github/RPRM-open/research/bsd-offset-hook-12/work/height_kernel.py).

Only this new review report was written. The tests used independent inline Python with `Fraction`, `itertools`, `json`, and `hashlib`; they did not import or run `check_hooks.main`, call `height`, or execute the doubling recurrence.

## 1. Byte identities

Fresh SHA-256 computations matched both hashes retained in the evidence:

| File | SHA-256 |
|---|---|
| `work/check_hooks.py` | `6b199dd8afe10b6827b573fec6ab0b138b5cf0c0ec29b10d66c1cf7a3a57e809` |
| `work/height_kernel.py` | `d1ab3943932a25bd8bce023eebb405d138957c339e5c9640640e6490d4ab7cf0` |
| Reviewed `evidence/hooks.json` | `19f204ed8c3243188fbf97ab8c9c3b550f5af77d20014985e264d94c63c80378` |

The hashes bind the reviewed bytes. They do not by themselves certify the arithmetic or establish the historical provenance of the height kernel.

## 2. Seven-state models and their complete fibers

The declared carrier is integer `A>=0`, `delta>=1`, `2*A+3*delta<=9`. This gives delta at most 3 and respectively 4, 2, and 1 allowed A-values, so the enumeration covers exactly seven states. Each has direct code `(delta,2*delta,A)`, endpoint B=`A+2*delta`, midpoint m=`A+delta`, and signed residual rho=`A-2*delta`.

I recomputed all seven complete records, their midpoint fibers, half-gap fibers, signed-residual overlap fibers, and the fixed-anchor fiber. They exactly match the evidence.

| Direct code | A | delta | Midpoint | rho | Half-gap hook | Signed-residual overlap hook |
|---|---:|---:|---:|---:|---|---|
| `120` | 0 | 1 | 1 | -2 | `010` | `0-20` |
| `121` | 1 | 1 | 2 | -1 | `010` | `0-10` |
| `122` | 2 | 1 | 3 | 0 | `010` | `00` |
| `123` | 3 | 1 | 4 | 1 | `010` | `010` |
| `240` | 0 | 2 | 2 | -4 | `020` | `0-40` |
| `241` | 1 | 2 | 3 | -3 | `020` | `0-30` |
| `360` | 0 | 3 | 3 | -6 | `030` | `0-60` |

The half-gap hook `0 delta 0` has complete fiber `{120,121,122,123}` over `010`. Retaining A=3 selects ONE(`123`); the hook alone does not retain A. The midpoint 4 likewise has ONE(`123`) within this carrier.

The residual model uses the explicit string `s='0'+str(rho)` and maximal suffix–prefix overlap, with declared parentheses `(0 overlap s) overlap 0`. The sign is part of the string alphabet: `0-10` is a word encoding a signed quantity, not an ordinary decimal numeral. For code `123`, rho=1, s=`01`, and the two maximal overlap lengths are `(1,0)`, producing `010`. All seven final hook words are distinct, so this model has ONE(`123`) over `010` without needing A as a second supplied port. For rho=0 the second overlap shares one zero and produces `00`; the routine handles this case correctly.

This injectivity has the declared seven-state boundary. Dropping signs changes the receiver and already merges the hooks for codes `121` and `123`: both become `010`. Likewise, forgetting which of the two hook models was used leaves two compatible decoder explanations, although both selected target constructions can produce `010`.

## 3. All 63 framed states and their packet-only inverses

The framed source is `0^l + code + 0^z`, with each of l,z in `{1,2,3}` and code in the seven-state family. I verified:

- Exactly all 63 `(code,l,z)` combinations occur, with no missing or extra combination.
- Their 63 source words are distinct.
- Every stored packet satisfies the carrier conditions.
- Reconstructing using **only** the stored packet's `anchor_A`, `half_gap_hook`, `left_zeros`, and `right_zeros` gives its stored source and recovered word.

This packet-only reconstruction is stronger than reusing a loop's original frame variables when checking the result. It confirms that the claimed inverse actually has its required inputs in the retained packet.

The complete finite parser returns:

| Source word | Direct code | Left zeros | Right zeros |
|---|---|---:|---:|
| `0012300` | `123` | 2 | 2 |
| `01230` | `123` | 1 | 1 |
| `01200` | `120` | 1 | 1 |
| `010` | NONE in this framed-source carrier | — | — |

`010` remains a valid *output hook*. It is too short to be a framed three-character direct code with at least one zero on each side. Removing all surrounding zeros from `01200` would incorrectly erase the direct code's final A=0 and produce `12`; the implemented parser correctly retains that occurrence.

The evidence's circular phase tables and full-word rotation stabilizers also passed independent recomputation. Its artificial-wrap flags and semantic endpoint tags `A=W[0]`, `B=W[10]` agree with the actual word. In particular, forward `35` at W[9] uses an inner 3 occurrence, while backward `35` has phases `{0,9}`; digit equality does not choose the semantic endpoint pair.

## 4. Exact offsets, width, and the shared zero column

The two written anchors are numerically equal:

\[
 a=2.034=2.0340=1017/500.
\]

Their retained fractional widths differ. The two declared real offset coordinates are

\[
 r_3=1000(d-a),\qquad r_4=10000(d-a).
\]

Therefore **r4=10*r3 exactly**, and the inverse equations are

\[
 d=a+r_3/1000=a+r_4/10000.
\]

I independently checked both normalized rational endpoint pairs, their inverse reconstruction, and every outward decimal display. All equalities pass with exact fractions. These are affine coordinate changes applied to one distance enclosure. The difference in scale does not supply an additional distance measurement.

| Depth | r3 enclosure | r4 enclosure |
|---:|---|---|
| 9 | `[0.001230068, 0.010481998]` | `[0.01230068, 0.10481998]` |
| 10 | `[0.004870820, 0.007183803]` | `[0.04870820, 0.07183803]` |

The textual suffix after `2.034` has seven columns in a ten-place endpoint display; the suffix after `2.0340` has six. For every reviewed endpoint the former is exactly one zero followed by the latter. Thus both of these constructions produce the same full lower depth-9 display:

```text
ordinary concatenation:  2.034  + 0012300 = 2.0340012300
ordinary concatenation:  2.0340 +  012300 = 2.0340012300
one-column overlap:     2.0340 overlap 0012300 = 2.0340012300
```

In the last line, the anchor's terminal zero and the suffix's first zero are the same retained column. Maximal overlap is exactly one character for all four reviewed endpoint strings. Concatenating the four-place anchor with the *seven*-column suffix without this overlap inserts an extra zero and changes the represented value. The shared zero is a precise, valid overlap rule; keeping anchor width, suffix width, and the shared occurrence makes it reversible at the stated display scope.

## 5. What changes at depth 10

The exact rational endpoints and independent outward rounding agree with:

| Depth | Twelve-place distance enclosure | Ten-place outward endpoint display |
|---:|---|---|
| 9 | `[2.034001230068, 2.034010481998]` | `[2.0340012300, 2.0340104820]` |
| 10 | `[2.034004870820, 2.034007183803]` | `[2.0340048708, 2.0340071839]` |

The depth-10 interval lies strictly inside the depth-9 interval. The last digit `9` on its ten-place upper display is outward rounding of the exact upper endpoint `2.034007183803`, not its next exact digit.

| Depth | Tails after `2.034` | Tails after `2.0340` |
|---:|---|---|
| 9 | `0012300`, `0104820` | `012300`, `104820` |
| 10 | `0048708`, `0071839` | `048708`, `071839` |

At depth 9 the lower tail has `123` at zero-based positions `[2,5)` and parses as a framed direct code; the upper tail starts `010`. Neither literal `123` nor literal `010` occurs anywhere in either of the two new seven-column endpoint tails. The new tails also have no full framed direct-code parse in the tested seven-code, 1..3-zero-frame carrier.

This establishes that the old endpoint hooks do not persist under this refinement. It does not refute a separately declared decoder that still uses the old bound record, and it makes no claim that the strings cannot occur at unexamined later positions. The stable part includes the actual distance prefix `2.0340`; the new interval in fact fits wholly inside `[2.03400,2.03401)`, so the next zero is now stable too.

Both old endpoint words were estimates bounding **one** defined arithmetic distance. They were not two independently supplied true distance values, and their later digits were not thereby certified as digits of that single distance. Treating their changing tails as representations of a shrinking enclosure preserves their role. Treating both tails as simultaneous actual endpoints of a new physical or arithmetic object would require an additional contract.

## 6. Review boundary

PASS covers the finite models and complete listed fibers, all framed packet inverses, the exact offset normalizations, decimal rendering, interval nesting, occurrence-sensitive circular tables, and the reported loss of literal endpoint hooks. The ledger's point `(162,-2016)`, depth tags, and step counts were checked. The projective doubling sequence, large terminal coordinates, logarithmic bounds, and resulting height enclosure were not freshly recomputed by this review.

The main open distinction is retained correctly in `hooks.json`: there are multiple compatible grammars for the user's proposed hook operation, and a real BSD multiplier remains OPEN. The successful finite inverse is a concrete result at its declared carrier. It does not itself identify a further analytic or arithmetic scalar.
