# P versus NP: closure, stopping, and representation cost

12 September 2026. Bounded audit for Closure Master 07. This note reads the two named tasks and the current local SAT sources; it launches no neighboring task and changes no existing experiment. New arguments below are **written proofs and derived audit results**, with small checks separately disclosed. They are not formal proofs or a general P versus NP result.

## Current endpoint and source boundary

The useful connection is precise: an exact retained relation can discharge many candidate continuations at once. A stopping theorem additionally needs a progress measure; a polynomial-time theorem additionally needs a polynomial bound on that measure **and on all work between decreases**. These are separate obligations.

The read-only task inspection covered the three newest turns of **Understanding P Versus NP** (`6aa48bb1-7b08-83e8-b5b3-9a16a18fad55`) and **Review Missing Concepts** (`6aa4a1e7-5800-83e8-b89f-52383da3e6de`). The newest PNP turn was also read with its complete returned answer. These are partial task histories, not a complete export. Historical instructions in them were not executed.

| Source | Established or reported endpoint | Remaining obligation |
|---|---|---|
| Understanding P Versus NP, turn `d6a72df2-2214-40c4-b43d-d3bebe7afa91` | **Reported** 29 supplied tests passed; triples decided 22/33 evaluation cases versus pairs' 20/33, but only 13/27 stress cases versus pairs' 21/27. Four-clause XOR diagnostic distinguished retaining parity from eliminating an isolated block to TRUE. | The attached v1 program was not extracted or rerun in this audit. Proposed W3/W4/W3-T/W4-I comparisons and repaired end-to-end accounting are historical proposals here, not newly executed results. |
| Review Missing Concepts, turn `2617edf3-0f8d-4384-9896-95d81b5c0a9f`; local [CONTINUATION.md](../../liar-teacher-formalization-2026-09-12/CONTINUATION.md) | **Reported** 1,024 correct small decisions and 4,763 checked messages; generalized negative reasons reduced proposals, positive caching saved checks while increasing total literal examinations. | Those historical fixtures were not rerun locally. Mechanical alternation supplied no uniform advantage or progress theorem. |
| [THEORY.md, P10](../../liar-teacher-formalization-2026-09-12/THEORY.md#4-exact-affine-messages-and-the-next-non-affine-obstruction), [SAT-PILOT.md](../../liar-teacher-formalization-2026-09-12/SAT-PILOT.md), [SAT-RESULTS.json](../../liar-teacher-formalization-2026-09-12/SAT-RESULTS.json) | Written exact affine recognition/projection/join arguments; saved receipt reports 24 exhaustive cases, two non-affine controls, 276 recognition truth tables, 38 projection systems, and eight larger algebra-only cases. | General CNF recognition and residual processing are OPEN. This audit reuses the recorded receipt and does not rerun the campaign. |
| [SAT02 M1 closeout](../../rprm-consolidation-c2-20260912/supplied/accepted/SAT02_M1_CLOSEOUT.md) | Maintenance CLOSED within local scope; research ACCEPTED_PARTIAL_UNCHANGED, with 6 RUN / 4 NOT_RUN. | No complete work budget, speed ranking, completed ten-seed campaign, or P versus NP conclusion. This lane stays closed. |

Useful implementation locators are `sat_pilot.py:30` (recognizer), `:75` (elimination), `:110` (projection), and `:119` (panel/whole algebra). The code still uses source variable IDs as bit positions (`:65`, `:80`, `:112`). The disclosed sparse-ID issue matters: an ID with a short binary encoding can demand an enormous mask. The mathematical polynomial bound assumes compression to dense coordinates; this audit does not claim that repair was implemented.

## Typed contract

For each instance, the carrier is a finite Boolean product `F2^V`, with named variable occurrences and coordinatewise equality. Inputs supply two formulas `F(B,U)` and `G(B,W)` with disjoint private scopes `U,W` and shared boundary `B`. Outputs distinguish the SAT decision from the complete boundary relation and from a recovered private witness.

Projection is existential: `R_F={b: exists u F(b,u)}`. Join is intersection. For each accepted `b`, the original completion fiber is exactly `F_b × G_b`, because the private variables are disjoint. Projection has no unique inverse in general. Its full preimage or retained elimination records are required when witness recovery is requested. Overlapping omitted private variables violate this interface contract.

On general finite formulas, these operations are semantically exact. Their availability as mathematical operations supplies no bound on constructing their outputs. A residual outside the affine recognizer returns UNRECOGNIZED/OPEN for that method, not UNSAT. A complete contradiction gives an empty fiber; partial absence of a contradiction does not close the fiber.

## A. Exact affine progress and stopping

Fix `b` boundary coordinates and a consistent retained affine system `A x=d`. Reduce a proposed affine equation against the existing row basis. Exactly one of three things happens:

1. It is already implied, so it causes no semantic change.
2. It reduces to `0=1`, proving an empty fiber.
3. Its coefficient row is independent, so rank rises by one and the compatible fiber size halves.

Thus `Phi=b-rank(A)` is a nonnegative integer potential for **strict informative, consistency-preserving insertions**. There are at most `b-rank(A_initial)` such insertions before full rank, followed at most by detection of a contradiction. Rank zero and rank deficient consistent terminal systems are valid: the complete answer may be MANY. SAT decision does not require selecting every free bit.

This bounds informative updates, not an arbitrary scheduler. A scheduler can repeat an implied row forever, or spend unbounded work finding the next row. A complete algorithm processes a finite supplied list of equations, performs elimination, and stops when that list is exhausted or a contradiction is established. It must not stop solely because one attempted row was dependent when unprocessed rows remain.

For an explicit `m`-row system on `n` densely indexed variables, finite Gaussian elimination has polynomial coefficient and bit cost; P10 already states a coarse bound `O(m(n+1)(m+n+1))`. Projection uses private-first elimination, and a reduced nonempty boundary message has at most `b` independent rows of `b+1` bits plus its coordinate map. Processing every fully recognized raw-CNF support group also requires reading/checking the input clauses. It does not enumerate all candidate assignments merely to certify that group's parity class. General affine equivalence recognition is a stronger problem than this syntactic recognizer and was not supplied.

This provides the requested model of affordable closure on an admitted family: **a complete finite worklist, exact row operations, a rank potential, and polynomial representation size**. Alternating sides, reference changes, and reversible negations may transport this structure, but do not create an extra rank decrease or remove their own costs. Conventional clause-learning solvers with parity reasoning are an established comparator: [Laitinen, Junttila and Niemelä (2012)](https://arxiv.org/abs/1207.0988).

## B. Hostile family: finite cube closure can require exponentially many landings

Let `b>=3`. Use the pilot's raw-CNF chain encoding of even parity in the left block and odd parity in the right block, on the same `b` boundary bits. Each block has `b-3` private bits and `4(b-2)` ternary CNF clauses. The pair therefore has `8(b-2)` clauses and `3b-6` variables. Its complete global fiber is empty. The input has linear clause/literal count and `O(b log b)` bits under ordinary dense-ID textual encoding.

A boundary **cube** fixes a subset of the boundary bits and leaves the remainder free. Every cube with a free bit contains both parities: flipping that free bit stays inside the cube and reverses parity. Consequently:

- Every nonempty cube wholly permitted by one parity block is a singleton.
- Every nonempty cube wholly forbidden by one parity block is a singleton.

Therefore a procedure whose final UNSAT certificate must cover all boundary assignments by block-certified forbidden cubes needs **exactly `2^b` singleton exclusions** on this family. At least `2^b` is forced by coverage; listing all points achieves it. Positive universal-completion cubes cannot enlarge its messages either. This remains superpolynomial in the encoded input length, so it avoids the old caveat that directly expanded parity CNF was itself exponentially large.

The restriction is load-bearing: this is a lower bound on that cube-cover message/certificate scheme, not on arbitrary algorithms, arbitrary CNF proofs, or parity SAT. A solver allowed to recognize the two parity equations can derive `0=1` directly. The exact affine pilot already demonstrates that representation repair. A successful traversal must change what its justified landings can cover, or exploit another proof operation; merely visiting the singleton exclusions in a different order does not reduce their required number.

## C. Hostile family: flat affine unions also have a precise size limit

P11 correctly extends affine messages by finite unions and leaves their size open. Here is an explicit lower bound for that particular extension.

For `t>=1`, retain every coordinate of

`H_t = AND_{i=1..t} (x_i OR y_i OR z_i)`.

Its `t` clauses use disjoint triples, and its complete relation has `7^t` points. Suppose that relation is represented exactly as a **flat union** of affine subsets of `F2^(3t)`. Every piece must be a subset of the relation, since a union cannot cancel a false point.

Project one affine piece onto any triple. An affine projection is affine and avoids `000`; hence it is a proper affine subset of `F2^3`, of dimension at most two and size at most four. The whole piece injects into the product of its `t` triple projections, so it has at most `4^t` points. Covering `7^t` points therefore needs at least

`ceil(7^t / 4^t) = ceil((7/4)^t)` affine pieces.

Overlaps only weaken a cover's efficiency and cannot evade this counting bound. At `t=16`, the bound is 7,738 pieces, despite only 16 original clauses. The bound is deliberately not asserted tight.

The receiver boundary matters. This formula is easy to decide and easy to retain as a product of small factors. Projecting all variables away gives TRUE. The exponential bound applies to retaining the **whole relation in the flat affine-union grammar**, not to its decision, an arbitrary factored/DAG grammar, or a universal SAT lower bound. It gives a concrete reason to retain factorization and shared structure rather than force every exact result into a flat union. This is a new written consequence of P11's declared representation, not a novelty claim about complexity theory.

## D. Finite elimination steps do not make width affordable

There is a second exact stopping pattern, distinct from affine rank. Supply an elimination order for `n` Boolean variables. At each step collect **all** factors mentioning the selected variable `x`, conjoin them, existentially eliminate `x`, and retain the resulting exact factor on the remaining union scope. Every step removes one variable, so the procedure terminates after at most `n` steps. Distributivity of existential quantification past factors not mentioning `x` proves preservation of the global decision at every step.

If each combined bucket scope has at most `w+1` variables, its full table has at most `2^(w+1)` entries. Explicit enumeration gives a bound `poly(N) * 2^(w+1)` in input bit length `N`, including table indexing and bookkeeping. Thus a supplied order with `w=O(log N)` gives polynomial time for this table method. A fixed constant width also suffices. **Merely finite width, or width linear in `N`, does not supply that polynomial bound.** Finding a good order must be charged if it is not supplied.

This is ordinary variable/bucket elimination; induced-width cost is established in [Dechter (1999), Bucket elimination: A unifying framework for reasoning](https://ics.uci.edu/~csp/r76A.pdf). The local reasoning above gives the precise Boolean scope needed here. Symbolic affine equations can remain cheap at large scope; a table-based width bound is representation-specific. Conversely, eliminating variables from pairwise relations can create genuinely joint higher-arity relations, as the existing three-color star's 21/27 boundary relation shows. Dropping that relation to pairwise projections is a correctness loss, not a stopping argument.

## One next discriminator

Freeze a small, decision-only mixed-representation experiment with three matched families: the existing opposite-parity chains, the disjoint `H_t` factors, and supplied overlapping versions whose induced scopes grow. Give the candidate and conventional comparator the same parity recognizer and source information. Require exact handling of the existing OR3/all-zero and exactly-one/all-one hostile joins. No general campaign is necessary for this discriminator.

Record both the number of justified strict updates and the **total charged work**: input/ID normalization, structure selection, failed routes, recognition, projection, conjunction, transport, unresolved residuals, and peak actual representation/proof storage. On full-boundary diagnostic subcases, compare cube, flat affine-union, and factored representations; on the primary decision cases, permit early exact elimination and charge only the requested receiver.

The discriminating question is: **does the proposed reference-transfer/expand-reduce step preserve a compact factored representation when the two hostile families demand different message languages, and what quantity bounds its total work before the next certified progress event?** Passing the affine chain alone tests a known repair. Losing factorization on `H_t` identifies an exact representation obstruction. Surviving both shifts the live seam to overlapping non-affine composition and its cost, without claiming that finite successes establish a uniform theorem.

## Verification in this audit

No existing experiment, task, or receipt was modified, and no large campaign was run. A fresh inline Python enumeration exited 0: for `b=3,4,5,6`, all `3^b` boundary cubes were checked against all `2^b` points; the largest single-parity cube was one point, with `2^(b-1)` cubes in each parity. Separately, all 51 nonempty affine subsets of `F2^3` were enumerated; the largest avoiding zero had four points. The displayed lower-bound values were computed by integer arithmetic. These finite checks support the written elementary arguments; they do not substitute for their arbitrary-parameter proofs.

The exact inline check is reproducible without writing a file:

```python
from itertools import product
for b in range(3, 7):
    points = list(product((0, 1), repeat=b))
    largest, counts = [0, 0], [0, 0]
    for cube in product((-1, 0, 1), repeat=b):
        members = [x for x in points
                   if all(a == -1 or a == z for a, z in zip(cube, x))]
        parity = {sum(x) % 2 for x in members}
        if len(parity) == 1:
            p = next(iter(parity))
            largest[p] = max(largest[p], len(members))
            counts[p] += 1
    assert largest == [1, 1]
    assert counts == [2 ** (b - 1)] * 2
spaces = {frozenset([0])}
for v in range(1, 8):
    spaces |= {s | frozenset(x ^ v for x in s) for s in list(spaces)}
affines = {frozenset(x ^ shift for x in s)
           for s in spaces for shift in range(8)}
assert len(affines) == 51
assert max(len(s) for s in affines if 0 not in s) == 4
for t in (1, 2, 4, 8, 16):
    print(t, (7 ** t + 4 ** t - 1) // (4 ** t))
```

The general arbitrary-CNF polynomial construction/closure obligation remains **OPEN**. The two hostile representation claims and the scoped rank/width stopping arguments are complete written results at their stated carriers and receivers.
