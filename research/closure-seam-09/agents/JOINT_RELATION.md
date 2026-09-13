# Closure seam 09: the relation between retained sides

Prepared 12 September 2026. This is a bounded formulation of the proposal that a seam can be a relation neither side possesses independently. It supplies a written factorization argument and an exhaustive finite matching example. It does not supply an E34 distance computation, a height theorem, or a claim about a universal extra object.

The precise positive reading is: **a receiver can ask a question of a joint source that neither separate observation determines.** Sometimes the two complete records together determine it; sometimes their summaries still omit a pairing, common frame, or other specified compatibility datum. Those cases have different missing ports.

## 1. Common-source formulation

Freeze a finite admitted source carrier `H`, exact equality of its occurrence-bearing records, observations `L:H→A` and `R:H→B`, and a requested readout `Q:H→V`. Let

```text
C(h) = (L(h), R(h))
H_(a,b) = {h in H : L(h)=a and R(h)=b}.
```

Both observations refer to the same `h`. The compatible joint image `C[H]` can be smaller than `L[H] × R[H]`; independent availability of `a` and `b` does not establish a common completion.

Three distinct claims are available:

1. **Neither side alone suffices:** `Q` does not factor through `L`, and does not factor through `R`. This requires one unequal-`Q` collision for each map; they need not be the same collision.
2. **Their retained pair suffices:** `Q=q∘C` for a decoder on `C[H]`. This holds exactly when every complete nonempty `H_(a,b)` has one `Q` value.
3. **Their retained pair still needs a distinction:** some `h,h'` satisfy `C(h)=C(h')` and `Q(h)≠Q(h')`. No decoder using only those retained data can answer correctly for both.

Claim 1 does not imply claim 3. For a bounded elementary example, `H={0,1}²`, `L(x,y)=x`, `R(x,y)=y`, and `Q(x,y)=|x-y|` satisfy claim 1 and claim 2. Each side alone leaves distance ambiguous; the actual ordered pair determines it with no independent hidden variable.

**Written proof of claim 2.** If a decoder exists, equal `C` values give equal decoded `Q` values. Conversely, if `Q` is constant on each reached fiber, define `q(a,b)` as that fiber's common `Q` value. This is well-defined and `q(C(h))=Q(h)`. An unreached pair has no admitted source; it is not evidence for a value of an unknown actual source. This is the existing receiver-factorization criterion specialized to two lanes, not a new domain theorem.

If the common source is specified by attachment, a more explicit carrier is

```text
J = {(a,b,s) : K(a,b,s)}.
```

Here `K` is the supplied compatibility law and `s` is a matching/orientation/witness record only when that contract needs one. Projecting to `(a,b)` forgets `s`. A fixed predicate with no distinct witnesses can use a singleton witness type. The notation does not make a third free quantity necessary in every relation.

## 2. A complete finite collision: same sides, different pairing

The left occurrence set is `{l0,l1}` and the right occurrence set is `{r0,r1}`. The symbols denote distinct occurrences. Their coordinates lie in the finite carrier `{0,1}`, in one supplied common frame with one fixed unit. Coordinate equality does not merge occurrence identities.

The fixed side records are

```text
L0 = ((l0,0), (l1,1))
R0 = ((r0,0), (r1,1)).
```

The admissible matching is a bijection `pi:{0,1}→{0,1}`. There are exactly two such maps. Define the common source `h=(L0,R0,pi)`, and the receiver

```text
D(h) = sum over i in {0,1} of (x_i - y_pi(i))².
```

`D` is the **total squared pair distance**, measured in squared coordinate units. It is not the distance between the two unpaired sets, and no assignment optimization is silently performed. The operation is total evaluation on the two admitted sources; no state-changing continuation is included.

| Source | Matching | Left record | Right record | Pair distances | `D` |
|---|---|---|---|---|---|
| `h_same` | `l0↔r0`, `l1↔r1` | `L0` | `R0` | `(0,0)` | `0` |
| `h_cross` | `l0↔r1`, `l1↔r0` | `L0` | `R0` | `(1,1)` | `2` |

The full separate side records agree, while the joint matching and requested answer differ. Thus the complete source fiber from those side records is `MANY({h_same,h_cross})`, and the complete readout image is `MANY({0,2})`. A computation that reports one actual distance from the side records alone has supplied a matching convention or extra evidence somewhere.

The minimum added datum for this exact receiver and fiber is **one binary distinction**. For example, supply

```text
t=0 iff pi is identity; t=1 iff pi is swap.
D=2t.
```

Necessity: the two old-fiber members have different `D` values, so one tag value cannot serve both. Sufficiency: the displayed decoder works for both. Here the same bit also recovers the entire matching, because the fiber has only two members. No unvisited matching remains in the declared grammar. The source has `ONE(h_same)` after `t=0` and `ONE(h_cross)` after `t=1`; these are inverse fibers for the explicitly given representation.

This is an example where independently complete **part** records are still incomplete **joint** records. If each record already carries a shared partner identifier fixing `pi`, they no longer equal the seam-forgetting observations above; the required datum has already been retained.

## 3. What a distance receiver is missing

For any fixed finite number `n` of paired coordinates and a supplied finite coordinate alphabet, the same ordinary squared-distance law gives

```text
D(pi) = sum_i x_i² + sum_j y_j² - 2 K(pi)
K(pi) = sum_i x_i y_pi(i).
```

The equality follows by expanding each square and using bijectivity of `pi` for the second sum. The separate squared norms are independent of the pairing; the cross term `K` can depend on it. In the two-source example, the squared-norm sum is `2`, while `K(identity)=1` and `K(swap)=0`.

Consequently, if the receiver asks only for `D`, retaining the cross term along with the known norm sums is sufficient. Retaining the entire matching may be more information than that receiver needs. The cross term is derived from the admitted joint source and law; this equation does not make it recoverable from summaries that have erased it, or guarantee a cheap way to obtain it.

For two individually identified full point coordinates `p,q` already in a supplied common metric frame, distance is directly `d(p,q)`. It is a relational readout of two supplied inputs. If only separate norms survive, an inner product or equivalent relative-direction distinction can be missing. If coordinates are in independent local frames, a relative-frame map can instead be missing. If the metric itself is unspecified, that is a missing law. These are candidate *ports under different contracts*, not interchangeable explanations of every seam.

Even the matching example changes with the question. Asking for the minimum over all admitted matchings returns `ONE(0)` from the two fixed side records; asking for the actual matching's distance has readout image `{0,2}`. Optimization and historical/actual-source inference are separate receivers.

## 4. Minimum repair and continuation boundary

For a finite carrier and old representation `C`, define `h ~ h'` when `C(h)=C(h')` and `Q(h)=Q(h')`. The quotient into these classes is represented by `(C,Q)`: it is the least information refinement retaining the old summary and answering this question. For a nonempty carrier, if tags may be reused across old fibers, the minimum repair-alphabet size is

```text
max over reached c of |Q[C⁻¹(c)]|.
```

For an empty carrier the minimum alphabet size is `0`. This is the existing least-question-refinement and finite-repair theorem. In the chosen two-source example the value is `2`. It specifies the missing *distinction*, rather than prescribing a universal additional number, dimension, or object. Its construction still requires source access, a retained reopen route, or a distinguishing observation.

The receiver boundary is substantive. Change the left coordinates to `(0,0)` while retaining distinct `l0,l1`, and retain right coordinates `(0,1)`. Both matchings then give `D=1`: the source fiber is `MANY(2)` and the distance readout is `ONE(1)`. But the right occurrence paired to `l0` still differs. A distance-only repair cannot answer that stronger occurrence receiver. Updates to coordinates can also expose distinctions that today's distance forgets; exact future preservation requires the separate enabledness and successor obligations.

## 5. Executed finite verification

The following self-contained Python enumerates all 32 sources from two binary-coordinate lanes and the two matchings. It checks the distance/cross-term equation on every source, the two fixed-record collision, all 16 side-record fibers, the maximum two-class repair bound, and the equal-distance/different-occurrence hostile case. It uses explicit checks active under optimized Python. It does not test E34 arithmetic or infer an unbounded resource claim.

The exact enumeration is also preserved in [work/check_joint.py](C:/github/RPRM-open/research/closure-seam-09/work/check_joint.py). One standalone execution wrote [evidence/joint.json](C:/github/RPRM-open/research/closure-seam-09/evidence/joint.json), including all 32 source rows, the verifier's SHA-256 and a UTC timestamp. The optional `--output` argument refuses existing paths before running the enumeration, and exclusive file creation also guards the final write. A hash binds the verifier bytes; its mathematical obligations are stated above.

The [PNG pairing figure](C:/github/RPRM-open/research/closure-seam-09/figures/joint_pairing.png) and [SVG pairing figure](C:/github/RPRM-open/research/closure-seam-09/figures/joint_pairing.svg) are generated by [work/draw_joint.py](C:/github/RPRM-open/research/closure-seam-09/work/draw_joint.py), which reads the receipt and checks its verifier hash. The PNG was visually inspected. The diagram's arrows encode occurrence pairing; their drawn lengths do not encode the displayed squared-value differences.

```python
from itertools import product, permutations
import json

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

lanes = tuple(product((0, 1), repeat=2))
matchings = tuple(permutations(range(2)))
rows = []
fibers = {}
for x, y, pi in product(lanes, lanes, matchings):
    direct = sum((x[i] - y[pi[i]]) ** 2 for i in range(2))
    cross = sum(x[i] * y[pi[i]] for i in range(2))
    expanded = sum(v * v for v in x + y) - 2 * cross
    require(direct == expanded, "cross-term identity failed")
    rows.append((x, y, pi, direct))
    fibers.setdefault((x, y), []).append((pi, direct))

fixed = fibers[((0, 1), (0, 1))]
require(fixed == [((0, 1), 0), ((1, 0), 2)], "pairing collision changed")
require(all(d == 2 * int(pi == (1, 0)) for pi, d in fixed), "repair decoder failed")
classes = [len({d for _, d in members}) for members in fibers.values()]
require(len(rows) == 32 and len(fibers) == 16, "finite coverage changed")
require(max(classes) == 2 and classes.count(2) == 4, "repair classes changed")
hostile = fibers[((0, 0), (0, 1))]
require({d for _, d in hostile} == {1}, "distance should be constant")
require({pi[0] for pi, _ in hostile} == {0, 1}, "occurrence distinction lost")
print(json.dumps({
    "status": "PASS",
    "sources": len(rows),
    "side_record_fibers": len(fibers),
    "distance_ambiguous_fibers": classes.count(2),
    "maximum_repair_alphabet": max(classes),
    "fixed_records_distances": [d for _, d in fixed],
    "equal_distance_distinct_matchings": len(hostile)
}, sort_keys=True))
```

Execution receipt: `PASS`; 32 sources, 16 side-record fibers, 4 distance-ambiguous fibers, maximum repair alphabet 2, fixed-record distances `[0,2]`, and 2 distinct matchings in the equal-distance control. Both ordinary isolated Python and optimized isolated Python produced this receipt. These finite checks accompany the written arguments; they do not independently certify their own general soundness.

## 6. Exact source connections and evidence grade

- The common-source fiber and readout-constancy test come directly from [proof-donut inference](C:/github/RPRM-open/docs/proof-donut.md:49). The common witness warning is explicit at [line 44](C:/github/RPRM-open/docs/proof-donut.md:44).
- The current definition identifies a seam as retained matched occurrences, maps, orientation and checked agreement: [core seam contract](C:/github/RPRM-open/docs/core.md:461). The witness-bearing attachment carrier is [ATTACH](C:/github/RPRM-open/docs/operations.md:73).
- The pair/full-source distinction and the least repair bound are explicit in [handbook sections 3–4](C:/github/RPRM-open/AGENT_HANDBOOK.md:109), [O08](C:/github/RPRM-open/docs/operations.md:230), and [O08R](C:/github/RPRM-open/docs/operations.md:236).
- The earlier bounded [bridge-08 corpus map](C:/github/RPRM-open/research/closure-bridge-08/agents/CORPUS_MAP.md:1) proposes retaining one joint middle fiber and choosing a missing distinction for a fixed receiver. This note instantiates that proposal; it does not upgrade bridge-08's other open targets.
- Recovered [missing Walsh direction and Tetris connector](C:/github/RPRM-open/recovered-concepts/CUBES-AND-PI-CURVES.md:169) are source-attributed examples where extra data must distinguish the actual missing joint feature. Their historical test counts were read, not rerun here.
- The recovered `Whole = A ⊕_R B` and pairwise/higher seam bridge is an [attributed assistant synthesis](C:/github/RPRM-open/recovered-concepts/CUBES-AND-PI-CURVES.md:389). The positive formulation above gives that reading a concrete finite carrier without treating the synthesis as an additional experiment.
- The recovered [6|4 readouts](C:/github/RPRM-open/recovered-concepts/ZERO-AND-RAILS.md:46) separately name center, distance/difference and source-locator questions. This supports keeping the present distance receiver separate from an automatically selected “middle.”

Evidence grades: source contracts and attributed recovery as labeled; elementary written proof for factorization, distance expansion and the chosen minimum repair; exhaustive finite test for the displayed 32-source kernel. No historical artifact was edited, no Memory Fabric ingestion/compile was performed, and no E34 or height computation was undertaken.
