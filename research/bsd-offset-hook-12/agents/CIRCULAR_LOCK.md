# Circular reference, overlap, and what a phase lock determines

Date: 2026-09-12. Evidence grades: elementary written theorems and fresh exact finite checks. This is a bounded interpretation of the proposed circular reference, with an explicit artificial-wrap tag. It does not claim a law for later digits of pi or a BSD identity.

**A circular reference can lock an unknown alignment.** A known overlap can remove rotational ambiguity; a marked occurrence can fix the remaining origin. The exact condition is that the complete compatible-phase fiber has one member. The resulting position is modulo the circle length. A traveled distance additionally needs winding, scale, and an equation connecting that distance to the phase.

## 1. Contract and source dependencies

The finite source words are fixed-width decimal words, with zero-based positions:

```text
W = 31415926535     N = 11
L = 0012300         N = 7
U = 0104820         N = 7
S = 010            N = 3
```

Each circle below is the explicit construction `circle(word, orientation=+1, seam=artificial_wrap)`. Its successor is `i -> i+1 mod N`. This adds a last-to-first adjacency to a supplied finite word; it does not assert that the next source-stream digit is its first digit. A word position, a digit value, a phase, an orientation, an integer winding count, and a real arithmetic distance are different types. Equal digits at different positions remain distinct occurrences.

Supplied ports: the word, its length, orientation unless explicitly made missing, observation words, and retained relative offsets. Missing ports: the compatible phase or joint phases. Requested receiver: occurrence placement, with winding included only in the separately declared lift. The operation is exact matching and compatibility filtering; it is enabled for admitted positions, decimal words, and offsets modulo the declared N. Malformed data are admission errors.

Read-only mathematical dependencies:

- [Carry and closure proof](C:/github/RPRM-open/research/closure-master-07/CLOSURE_PROOF.md), especially sections 1 and 2: a projected cycle can return while its retained accumulator has nonzero drift.
- [PI11 README](C:/github/RPRM-open/research/bsd-pi-reading-11/README.md): certified finite word, endpoint–midpoint chart, actual-distance enclosure, and the complete real fiber of the `34` reading.
- [PI11 history](C:/github/RPRM-open/research/bsd-pi-reading-11/agents/PI_HISTORY.md): exact D0 roles, tagged decoder alternatives, and historical mirror-ring closure.

No previous verifier was rerun or previous evidence grade increased. The new finite checks in section 7 use the displayed words directly. The parent task owns further distance refinement and the new overlap decoder.

## 2. Complete phase and synchronization theorem

For a known word `w` of length N and an observed word u, define

\[
 A_w(u)=\{s\in\mathbb Z/N\mathbb Z:\ w_{s+j}=u_j\text{ for every }0\le j<|u|\}.
\]

Indices of w are reduced modulo N. This definition permits observations longer than N, with repeated visits checked at every occurrence. For observations `u_j` at known offsets `a_j` from one missing root phase, the complete phase fiber is

\[
 K=\bigcap_j(A_w(u_j)-a_j).
\]

Every element of K satisfies every supplied observation; every satisfying phase belongs to each intersected set. Thus K is the complete fiber: NONE if empty, ONE if a singleton, otherwise MANY(K). A requested readout q is determined precisely when K is nonempty and q is constant on K. A repeated observation at the same offset adds no constraint; a new offset can split the fiber.

The following more general version handles a whole loop of overlapping references.

**Finite synchronization theorem.** Supply a nonempty finite graph, a common phase carrier `Z/NZ`, a directed offset `d_e` on each oriented edge `e:u -> v`, and a set `A_v` of permitted phases at every vertex. Edge reversal negates its offset. Seek joint phases satisfying

\[
 \theta_v-\theta_u=d_e\pmod N,\qquad \theta_v\in A_v.
\]

The edge equations have a solution exactly when the signed offset sum on every closed walk is zero modulo N. When this holds, choose one root and a spanning tree in each connected component C. Let `b_v` be the signed tree-path sum from its root to v and put

\[
 K_C=\bigcap_{v\in C}(A_v-b_v).
\]

The complete joint solution family is

\[
 \boxed{\theta_v=t_C+b_v\pmod N,\qquad(t_C)_C\in\prod_C K_C.}
\]

It is NONE if a closed-walk condition fails or some K_C is empty; ONE exactly when every K_C is a singleton; otherwise the displayed product, with correlated vertex phases retained, is the complete MANY family. The empty graph has its single empty assignment.

**Proof.** Summing edge equations along a closed walk telescopes, proving necessity. For sufficiency assign each `b_v` along the chosen tree. The closed walk made by a non-tree edge and its tree return path shows that this edge also has the required difference. Any other solution differs from b by a constant on each component, since its difference is equal across every edge. Vertex conditions then hold exactly for `t_C` in the displayed intersection. This proves both correctness and complete coverage without assuming the consistency being tested.

With no vertex marks or content restrictions, every A_v is the full circle. There are N choices per connected component. A connected arrangement is unique **up to simultaneous rotation**, but has N rooted phase assignments. One supplied occurrence mark in that component fixes the origin, provided all other constraints agree. Several components require their own anchors or connecting offsets.

If overlaps only suggest several possible edge offsets, each `d_e` is itself a missing port with a supplied finite allowed set. Apply the theorem to every admitted joint edge assignment and retain the compatible assignments together with their phases. Pairwise possible offsets cannot be chosen independently after forgetting the cycle condition. For example, on N=7 a three-edge loop with offsets `(1,1,1)` has individually satisfiable edge relations but no joint phase assignment: its sum is 3, not 0 modulo 7. The loop `(2,2,3)` is compatible and, with its first phase marked 0, has ONE joint phase tuple `(0,2,4)`.

## 3. Overlap can also reconstruct a word

If the word itself is unknown, known placements must be separated from known content. Supply an alphabet of size b, N circle positions, and finitely many patches with marked start positions and fixed orientation. Let T be the set of positions covered by at least one patch.

**Finite gluing theorem.** A complete word exists exactly when all patch assignments to each shared position agree, including a patch that wraps and revisits its own position. If they agree, the complete word fiber consists of those fixed symbols on T and arbitrary alphabet symbols on its complement. It has exactly `b^(N-|T|)` members.

**Proof.** Each word completion must use the prescribed symbol on every covered position. Pairwise agreement makes that prescription well defined. Every assignment on the uncovered positions extends it, and these are all possible completions.

Consequently complete compatible coverage forces ONE word. A closed geometric arrangement with an uncovered position leaves a content vacancy. Unknown placements require the phase theorem jointly with this gluing theorem. A picture of patches touching is useful once touching means a stated equality of their shared occurrences.

## 4. The actual finite words: successful locks and hostile cases

All phases below are complete forward circular match fibers. Braces show the full sets, not search samples.

| Observed pattern | W: `31415926535` | L: `0012300` | U: `0104820` | S: `010` |
|---|---|---|---|---|
| `0` | {} | {0,1,5,6} | {0,2,6} | {0,2} |
| `1` | {1,3} | {2} | {1} | {1} |
| `3` | {0,9} | {4} | {} | {} |
| `5` | {4,8,10} | {} | {} | {} |
| `01` | {} | {1} | {0} | {0} |
| `010` | {} | {} | {0} | {0} |
| `123` | {} | {2} | {} | {} |
| `01230` | {} | {1} | {} | {} |
| `35` | {9} | {} | {} | {} |

For W, observing `3` permits phases 0 and 9. Observing its forward neighbor as `1` leaves ONE(0); observing that neighbor as `5` leaves ONE(9). This is a concrete case of a hook determining alignment. For L, the entire `01230` patch has ONE(1). For U, `010` has ONE(0). Under literal matching, `010` does not occur on L even with wrap. This rejects that literal operation only; a decoder, deletion rule, or overlap assembly is a separate typed map and is not decided by this table.

**Occurrence control for the historical pi endpoints.** D0 assigns outer `A=3` to W[0] and outer `B=5` to W[10]. The unique *forward contiguous* `35` at phase 9 instead uses the inner occurrence W[9]=3 and outer W[10]=5. It does not automatically align the historical A occurrence. If orientation is also missing, the complete joint `(phase,orientation)` fiber for `35` is

```text
{(0,-1), (9,+1), (9,-1)}.
```

Only `(0,-1)` visits the outer A then outer B. Forward `53` occurs at phases 8 and 10; the latter crosses the artificial seam. An A/B occurrence tag, orientation, and seam tag preserve this distinction. Numeral equality alone does not.

Every supplied word has trivial full-word rotation stabilizer: the entire word matches only at phase 0. This property is a fact about these four words. The hostile periodic control `010010` matches its entire word at phases `{0,3}`, so even full coverage can leave two occurrence phases unless an origin mark is retained. Conversely the single zero on S has two placements despite the full S word having one.

## 5. What returning around the circle forgets

Fix an initial mark, circumference N in position units, orientation +1, and an admitted step budget `0<=k<=K`. The observed phase is `s=k mod N`, represented by `0<=s<N`. Its complete lifted-time fiber is

\[
 \{s+qN:\ q\in\mathbb Z,\ 0\le q\le\lfloor(K-s)/N\rfloor\},
\]

empty if `s>K`. Retaining q gives the inverse `k=s+qN`; phase alone forgets turns. If one position has physical length ell, path length is `ell*(s+qN)`. Neither ell nor q follows from a phase mark.

For the compatible N=7 triangle `(2,2,3)`, the chosen integer edge lifts sum to 7: one turn. They cannot simultaneously be differences of one real-valued potential on the three vertices, because those differences would telescope to zero. Replacing the last lift by -4 gives the same modular edge constraints and a zero sum. Thus the modular geometry does not choose the winding lift.

This is the same precise issue established by the carry proof: the digit tuple returns after b steps while its retained lift changes by `b*A`. Closing the displayed loop certifies a return in its receiver. A claim about zero accumulated change must additionally prove that the actual edge costs sum to zero.

## 6. Constructive circles and the independent scalar port

A geometrically closed system of equations can determine its unknowns. The synchronization proof constructs a spanning-tree assignment and checks the closing edges; it does not assume their success. Even mutually referencing equations can have a unique solution: `a=b+1` and `b=3-a` force `(a,b)=(2,1)`. Merely stipulating a self-return has a weaker content: `a=a` accepts every admitted a. The mathematical distinction is the strength and provenance of the supplied equations, not whether the diagram is circular.

**Derived-reference obstruction.** Let C be a supplied representation of a source x and let F be any deterministic construction on C's reached values: a decoder, circle, phase convention, or computed overlap signature. Then `(C(x),F(C(x)))` has exactly the same source fibers as C. Equality of C forces equality of F(C), and retaining C gives the converse. Such construction can expose a relation or make a question easy to read, but it does not separate source candidates already merged by C. A genuinely additional observation H(x) refines the fiber by intersecting with `H^-1(h)`; it may earn a lock.

In PI11, within `X=[2,2.1)`, the specified digit extractor and endpoint–midpoint decoder have the complete pi-word source fiber `[2.034,2.035)`. All deterministic circles built solely from the resulting W retain that real ambiguity. Keeping the tighter PI11 enclosure reduces the fiber, but still permits, for example, both exact rationals

```text
x = 2.034005,   y = 2.034009,
2.034001230068 < x < y < 2.034010481998.
```

Both select the same chart `34` and the same W. These are alternative completions of the *observation record*, not a claim that the already-defined E34 height distance has two actual values, nor that another elliptic curve realizes each counterpoint. The lower and upper endpoint strings describe the shared enclosure; they are not automatically the later digits of every member inside it.

There is also a direct obstruction for an independent target scalar. Let S be a nonempty complete phase fiber and explicitly admit the source carrier `S x {0,1}`. All circle observations depend only on s, and let the requested residual readout be `R(s,r)=r`. Even if a marked reference reduces S to ONE(s*), the joint source fiber remains `{(s*,0),(s*,1)}`. These two models satisfy every stated circular constraint and disagree on the residual. Therefore those constraints alone do not imply residual zero. This is a complete finite countermodel to the inference, not a refutation of a stronger arithmetic law that might connect the ports.

To pin an actual BSD quantity, add and justify that connecting law. PI11 already supplies a useful example with a real pi reference: the independently established relation `Omega_c * M34 = pi`, with `M34=AGM(sqrt(68),sqrt(34))>0`, determines `Omega_c=pi/M34`. The equality and its normalization perform the lock. The remaining BSD equation recorded there is

\[
 M_{34}\lambda_2
 =136\sigma\left[pq-\frac{(p+q-d^2)^2}{4}\right].
\]

It is a relation between the actual analytic coefficient, heights, distance, and Sha-order candidate. A phase rule that is derived only from a finite word does not supply this equality or identify sigma with the actual Sha order. The useful open continuation is a map from actual arithmetic/analytic data into the circular constraint system, with a proof that every compatible completion has the same required residual. Until that bridge is supplied, that target is OPEN; the finite phase and decoder fibers can already be closed.

## 7. Fresh checks and replay

Exact Python enumeration checked every phase in the table, all four full-word rotation stabilizers, all 22 `(phase,orientation)` placements of `35` in W, and the periodic hostile control. It also checked all 224 triangle edge assignments over N=2,3,4,5 against all phase triples: 54 edge assignments were compatible; each had N unanchored solutions and exactly one with its first vertex marked 0. The other 170 had none. Rational arithmetic checked both counterpoints against the prior enclosure and the `34` extractor. The written theorems above cover their declared finite parameters independently of these tests.

The core enumeration is reproducible without project imports or external packages:

```python
from itertools import product
from fractions import Fraction

words = ['31415926535', '0012300', '0104820', '010']
patterns = ['0', '1', '3', '5', '01', '010', '123', '01230', '35']
def phases(w, u):
    return [s for s in range(len(w))
            if all(w[(s+j) % len(w)] == c for j, c in enumerate(u))]
for w in words:
    print(w, {u: phases(w, u) for u in patterns}, phases(w, w))
w = words[0]
assert [(s,e) for s in range(11) for e in (1,-1)
        if all(w[(s+e*j) % 11] == c for j,c in enumerate('35'))] == [
            (0,-1), (9,1), (9,-1)]
assert phases('010010', '010010') == [0,3]
checks = closed = 0
for n in range(2,6):
    for a,b,c in product(range(n), repeat=3):
        states = [p for p in product(range(n), repeat=3)
                  if (p[1]-p[0]) % n == a
                  and (p[2]-p[1]) % n == b
                  and (p[0]-p[2]) % n == c]
        expected = n if (a+b+c) % n == 0 else 0
        assert len(states) == expected
        assert sum(p[0] == 0 for p in states) == int(expected > 0)
        checks += 1
        closed += bool(states)
assert (checks, closed) == (224,54)
lo, hi = map(Fraction, ['2.034001230068', '2.034010481998'])
for x in map(Fraction, ['2.034005', '2.034009']):
    assert lo < x < hi
    assert ((100*x).__floor__() % 10, (1000*x).__floor__() % 10) == (3,4)
```

Only this new report was written by this subtask. No circle was promoted to a statement about the unexamined pi stream, and no original source lane was edited.
