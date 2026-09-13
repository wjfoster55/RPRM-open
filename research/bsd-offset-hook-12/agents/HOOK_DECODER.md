# Hook 12 — direct-code and zero-frame audit

Date: 2026-09-12. New report only; historical source files remain unchanged.

## Frozen bounded grammar before execution

This candidate slate was written before the fresh tests below. Candidate selection is post-target: the supplied targets are `123 -> 4`, and framed words `0012300` / `01230 -> 010`. Successful reproduction will establish only the named operation, not an independently discovered source rule. The larger unspecified digit grammar remains **OPEN**.

Source contracts are `research/bsd-pi-reading-11/dependencies/PI_ZIP_TEST_SPEC.md` (Direct decoder carrier; Endpoint teacher adapter; Reduction views and conditional abduction) and `research/bsd-pi-reading-11/agents/PI_HISTORY.md`. The rprm-math-lenses skill is applied; unchanged historical proofs are reused at their recorded scope. No old full campaign is rerun.

The semantic carrier is the seven integer pairs `(A,delta)` satisfying `A>=0`, `delta>=1`, `2A+3delta<=9`; `B=A+2delta` and direct code `c=(delta,2delta,A)`. Admission checks all three code ports and this carrier. This is narrower than the general historical D0/D1 direct-decoder carrier. Supplied inputs to the frame tests are **typed** `F(L,c,R)=0^L | c1 c2 c3 | 0^R`, with fixed three-digit core and explicit frame counts. Here the counts are `(2,2)` or `(1,1)`. Equality of digit values does not identify occurrences.

Fixed candidate operations:

1. **G-midpoint:** replace the typed core with `m=A+delta`, retaining all frame zeros, their source positions, and original core placement.
2. **G-half-gap:** replace the typed core with `delta`, retaining the same frame data. This is a different old-coordinate projection, with its full seven-state fiber retained.
3. **G-sum control:** replace the core by the ordinary digit sum `delta+2delta+A=A+3delta`; retain frames and compare its fibers with midpoint fibers.
4. **G-residual:** the old residual chart is the signed pair `(0,A-2delta)`. Only a separately tagged nonnegative decimal serialization can treat its target `(0,1)` as the word `01`. Preserve a signed integer token when negative. Ordinary concatenation retains all frame zeros.
5. **G-overlap:** normalize each nonempty boundary frame to one marked `0`, retaining its original count and positions, and compose those boundary words with the residual serialization by maximal suffix-prefix overlap. For words `u,v`, choose the largest `k<=min(|u|,|v|)` with `suffix_k(u)=prefix_k(v)` and return `u + v[k:]`; keep the overlap length and occurrence correspondence. This is a **new declared adapter**. Greedy deletion of all leading/trailing zeros is excluded: it would destroy the final core `0` of code `120`. Test all seven states; the signed residual remains a token, not an unsigned decimal digit word.
6. **G-uniform control:** the old uniform digit permutations `P,N,T,M` and position reversal may be composed. They preserve length and digit-equality pattern, so a literal width-five or width-seven input cannot directly become width-three `010`. A width-three distinct-digit word `123` cannot become repeated-endpoint `010` under such maps either. This result addresses only these uniform permutations, not all possible reductions.

Complete fibers to enumerate: direct-code-to-midpoint, direct-code-to-digit-sum, direct-code-to-half-gap, residual chart, and normalized overlap output on the seven-state carrier. Requested readouts preserve code roles, frame counts, occurrence placement, and any decimal scale supplied by the parent task. A bare decimal string supplies no scale or role tag by itself. The report will not infer the original number from a displayed normalized output alone.

Hostiles fixed before execution: midpoint collision at `240` versus `121`; digit-sum collision at `123` versus `240`; half-gap collision at `123` versus `120`; signed residual at `120`; core-ending-zero parsing at `0|120|0`; same target core with unequal or longer boundary frames; absent code-role tag; and a literal uniform-map attempt to change word length.

## Execution results

The initial enumeration passed: all seven states, all named scalar fibers, all seven signed residual states and normalized overlap displays, and 28 fixed-width frame parses across frame counts `(1,1),(2,2),(1,2),(3,1)`.

### Staged reference-assisted refinement, frozen before its tests

After that enumeration, the parent explicitly requested the reference-assisted half-gap branch. Extend G-half-gap by the already declared boundary normalization: display `0 | delta | 0`, retain original boundary counts `(L,R)` and source placements, and admit a separately supplied endpoint port `A_ref`. Its inverse solves `delta=display_middle`, `A=A_ref`, `c=(delta,2delta,A)` and checks the seven-state carrier. The reference is a side input, not information recovered from the short display. Test both unanchored and anchored fibers for every state and every listed frame count. At target `delta=1`, retain the full unanchored four-code fiber; supply independent `A_ref=3` to narrow it. If the reference already supplies `(A,m)=(3,4)`, the output `010` is a redundant consistency receipt because that reference alone determines the entire code. This is a new explicit framing/reference composition of the old half-gap coordinate, selected after the target, and does not replace the residual-overlap rival.

### Exact 123-to-4 decoder and complete fibers

The old endpoint generator makes `123` the typed triple `(delta,2delta,A)=(1,2,3)`. Consequently

```text
A=3, delta=1, B=A+2delta=5, m=A+delta=4.
```

This is why `123` reads as midpoint `4`. It is not the digit sum `1+2+3=6`. Neither the spelling `123` nor the unconstrained general D0/D1 direct-code carrier assigns those endpoint roles by itself: the **endpoint-generator tag** is essential.

| code | A | delta | B | midpoint m | digit sum | residual r=A-2delta |
|---|---:|---:|---:|---:|---:|---:|
| 120 | 0 | 1 | 2 | 1 | 3 | -2 |
| 121 | 1 | 1 | 3 | 2 | 4 | -1 |
| 122 | 2 | 1 | 4 | 3 | 5 | 0 |
| 123 | 3 | 1 | 5 | 4 | 6 | 1 |
| 240 | 0 | 2 | 4 | 2 | 6 | -4 |
| 241 | 1 | 2 | 5 | 3 | 7 | -3 |
| 360 | 0 | 3 | 6 | 3 | 9 | -6 |

The complete midpoint fibers are:

```text
1 -> ONE(120)
2 -> MANY({121,240})
3 -> MANY({122,241,360})
4 -> ONE(123).
```

For completeness, `m=4` gives `A=4-delta`; substitution into `2A+3delta<=9` yields `8+delta<=9`. Since `delta>=1`, necessarily `delta=1,A=3`. Midpoint 4 uniquely selects the pi endpoint code on this carrier. It does not uniquely select a code in an unspecified larger carrier.

The complete digit-sum fibers are `3:{120}`, `4:{121}`, `5:{122}`, `6:{123,240}`, `7:{241}`, `9:{360}`. In particular the sum 6 does not distinguish target `123` from `240`. The complete half-gap fibers are `1:{120,121,122,123}`, `2:{240,241}`, `3:{360}`.

### Literal frames versus normalized frames

| Input with declared frame counts | Preserve frames, midpoint | Preserve frames, half-gap | Preserve frames, sum | Preserve frames, residual `01` | Normalize frames, half-gap | Normalize frames, residual overlap |
|---|---|---|---|---|---|---|
| `0|123|0`, `(1,1)` | `040` | `010` | `060` | `0010` | `010` | `010` |
| `00|123|00`, `(2,2)` | `00400` | `00100` | `00600` | `000100` | `010` | `010` |
| `0|123|00`, `(1,2)` | `0400` | `0100` | `0600` | `00100` | `010` | `010` |
| `000|123|0`, `(3,1)` | `00040` | `00010` | `00060` | `000010` | `010` | `010` |

The output `010` therefore has at least two explicitly tested derivations in the frozen/refined grammar. The literal single-frame half-gap branch uses an old coordinate projection. Turning the longer frames into the same display additionally uses a newly declared frame normalization. The residual branch additionally uses newly declared occurrence overlap. None silently follows merely from the old equality `m=4`.

### Reference-assisted half-gap branch

On the seven-state carrier, normalized `0|delta|0` has exactly these code fibers:

```text
010 -> MANY({120,121,122,123})
020 -> MANY({240,241})
030 -> ONE(360).
```

With `A_ref=3`, the joint fiber over `(010,A_ref=3)` is `ONE(123)`. The explicit read-back is `delta=1`, `A=3`, `c=(1,2,3)`, followed by `B=5,m=4` and the historical finite pi decoder. With supplied `(L,R)`, rebuild exactly `0^L|123|0^R`. All seven codes and all four listed frame-count pairs passed this 28-case round trip.

This realizes a finite **reference-assisted decoding/checking loop**. Pi can supply the reference through its already certified endpoints. Any separately supplied valid `A_ref=3` serves the same typed role. The loop is not an independent pi source. In fact, the stronger boundary is that **A=3 alone already forces delta=1** under `2A+3delta<=9`, so even that single reference port determines `123` on this carrier. A full `(A,m)=(3,4)` reference also makes `010` redundant. It is a consistency readout of the referenced state, not fresh information about it.

If only normalized display `010` is retained and the frame counts are forgotten, the two user-supplied frame records form `MANY({(1,1,123),(2,2,123)})` after fixing code `123`. In the reference-free half-gap branch they instead form the complete eight-record product of the two listed frame pairs with `{120,121,122,123}`. This product is licensed here because the declared frame choices are independent of the semantic code; no general rule permits replacing correlated missing ports with a product. Other frame counts or missing numeric source scale require an explicitly enlarged contract.

### Residual-overlap branch

The recovered residual chart is `(0,r)=(0,A-2delta)`, with target `01`. Its target composition is

```text
0 ⊙ 01 = 01          overlap length 1
01 ⊙ 0 = 010         overlap length 0.
```

The first operation merges the **display positions** of the normalized left-frame zero and the residual's first zero. Their provenance remains two marked source roles in the occurrence correspondence. This is a declared gluing operation; equality of zero values alone does not authorize it. Normalization of `00` to a marked `0` similarly stores both original zero positions and count 2.

The complete signed-token receiver is:

| code | signed residual pair | normalized overlap display | overlap lengths |
|---|---|---|---|
| 120 | `(0,-2)` | `0-20` | `(1,0)` |
| 121 | `(0,-1)` | `0-10` | `(1,0)` |
| 122 | `(0,0)` | `00` | `(1,1)` |
| 123 | `(0,1)` | `010` | `(1,0)` |
| 240 | `(0,-4)` | `0-40` | `(1,0)` |
| 241 | `(0,-3)` | `0-30` | `(1,0)` |
| 360 | `(0,-6)` | `0-60` | `(1,0)` |

These seven displays are distinct. The signed chart and this tagged display are injective on the complete seven-state carrier, so each reached display has `ONE(code)` there. The inverse reads the retained signed residual token `r`, enumerates `delta in {1,2,3}`, sets `A=r+2delta`, and checks the original inequalities. With frame counts and original position/scale metadata, it reconstructs the supplied framed source. This inverse is derived from the original formula and checked on all seven states; it is not a target lookup substituted for a rule.

For a **digit-only word receiver**, five negative residuals are out of carrier, leaving the two-state subcarrier `{122,123}` and outputs `{00,010}`. The display `0-20` is a structured signed-token serialization, not an unsigned integer, a decimal word, or an instruction to subtract 20. Retaining that distinction prevents false digit-string closures.

### Hostiles, uniform maps, and missing ports

The fixed hostile cases survived as intended:

- `240` and `121` share midpoint 2; midpoint compression does not globally invert all seven states.
- `240` and `123` share digit sum 6; digit sum cannot replace the midpoint law.
- `120` and `123` share half-gap 1; unanchored half-gap compression cannot distinguish them.
- `0|120|0=01200` retains core `120` under fixed-width parsing. Greedy zero stripping gives `12`, which is malformed for the declared three-port code.
- Negative residuals preserve their minus sign and integer-token type. The code `122` produces overlap display `00`, exposing the otherwise easy-to-miss full overlap of the final zero.
- Longer and unequal zero frames share normalized `010`, so frame counts are necessary for exact lexical reconstruction.
- `010` is not itself an admitted endpoint-generated direct code: its first two coordinates `(0,1)` violate both `delta>=1` and `c2=2c1`.
- Uniform `P,N,T,M` permutations and reversal preserve word length. They cannot send literal `01230` or `0012300` to literal `010`. They also preserve the digit equality pattern and cannot send three distinct digits `123` to repeated-endpoint `010`. This written invariant covers every finite composition of the named operations; it does not reject reductions, reference-assisted projections, or new grammar.

The tested literal transforms confirm the operation definitions:

| source | P | N | T | M |
|---|---|---|---|---|
| `123` | `983` | `987` | `127` | `876` |
| `0012300` | `5598355` | `0098700` | `5512755` | `9987699` |
| `01230` | `59835` | `09870` | `51275` | `98769` |
| `010` | `595` | `090` | `515` | `989` |

These were freshly returned by the installed operational-number translator with `scout=True`. Its lexical receipts retain widths and leading zeros, and explicitly leave digit-word versus integer-literal interpretation unselected. Scout prose supplied no decoder authority. The adjacent historical findings recorded only an older 42-check translator receipt, so the current small translator verifier was freshly run: `python -B C:/github/RPRMLexicon/operational_numbers/verify.py` returned **PASS: 114/114 operational-number checks**. This did not replay the old pi campaign.

The remaining source adapter must specify the exact source window and decimal column; whether zeros are number digits, boundary marks, or both; the three code roles; which source reference supplies A; the retained count/scale data; and why half-gap or residual overlap is the selected receiver. Source fractional-place metadata is not generated by these word maps. For example, reading the same digits as fractional places or an integer gives different quantities, and replacing a framed word by its normalized display does not preserve positional numeric value. The parent task owns the actual enclosure and suffix-position audit.

### Evidence and replay

Evidence grades: the old formulas and seven-state pi codebook are **recovered prior finite results**; the midpoint formula and permutation invariants are **written derivations**; the tables, 28 frame parses, seven signed-overlap results, and 28 reference-assisted round trips are **fresh finite tests**. Frame normalization, reference-assisted framing, and residual overlap are **new explicit candidate adapters, selected after seeing the target**. Their selection by the numeric source and any larger unnamed grammar remain **OPEN**. No new pi digit, infinite pi law, or new analytic relation is established.

Exact read-only source bindings (SHA-256; hashes bind bytes, not truth):

- `C:/github/RPRM-open/research/bsd-pi-reading-11/dependencies/PI_ZIP_TEST_SPEC.md`: `dd93a02c259461d2d7292d51876ede667da3ef50b4ba74cadb674e3f12540456`; endpoint generator at line 74, reduction views at line 101, residual view at line 115.
- `C:/github/RPRM-open/research/bsd-pi-reading-11/agents/PI_HISTORY.md`: `a54b1c5c4883757f3c3f55ed14368978982ee98f89120a7ed41203d2e31275c3`; seven-state chart at line 112.
- `C:/github/RPRMLexicon/operational_numbers/translate_number.py`: `6e7fab0a37430b7d6fc197940129756b1a14277dbfc990e1a07a446eb18c5e67`.

The following standalone Python reconstructs the bounded tables and core assertions without any historical campaign. The embedded block itself was extracted and executed after writing this report and returned **PASS**:

```python
from collections import defaultdict
S = [(A,d) for d in range(1,4) for A in range(10) if 2*A+3*d <= 9]
frame_pairs = [(1,1),(2,2),(1,2),(3,1)]
def overlap(u,v):
    k = max(k for k in range(min(len(u),len(v))+1)
            if (u[-k:] if k else '') == v[:k])
    return u + v[k:], k
def residual_display(A,d):
    a,k1 = overlap('0','0'+str(A-2*d))
    b,k2 = overlap(a,'0')
    return b,(k1,k2)
fibers = {name:defaultdict(list) for name in ('midpoint','sum','half_gap','overlap')}
for A,d in S:
    c = f'{d}{2*d}{A}'
    values = {'midpoint':A+d,'sum':A+3*d,'half_gap':f'0{d}0',
              'overlap':residual_display(A,d)[0]}
    for name,value in values.items(): fibers[name][value].append(c)
    for L,R in frame_pairs:
        w = '0'*L + c + '0'*R
        assert w[L:L+3] == c
        # Side port A and visible delta reconstruct the source.
        recovered = '0'*L + f'{d}{2*d}{A}' + '0'*R
        assert recovered == w
assert len(S) == 7
assert dict(fibers['midpoint']) == {1:['120'],2:['121','240'],
                                   3:['122','241','360'],4:['123']}
assert fibers['sum'][6] == ['123','240']
assert fibers['half_gap']['010'] == ['120','121','122','123']
assert len(fibers['overlap']) == 7
assert fibers['overlap']['010'] == ['123']
assert fibers['overlap']['00'] == ['122']
assert [(A,d) for A,d in S if A == 3] == [(3,1)]
for name,fiber in fibers.items(): print(name,dict(fiber))
```
