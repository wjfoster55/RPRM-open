# Raw-CNF parity boundary pilot

Frozen specification written **2026-09-12, before the first experiment run**.
This is a new local pilot, separate from SAT02. The implementation and output
are `sat_pilot.py` and `SAT-RESULTS.json` in this directory.

## Contract and frozen selection

The carrier is finite Boolean assignments to positive integer variable IDs;
literal sign specifies negation. Equality of assignments is coordinatewise.
The input consists of two raw CNF clause lists and a supplied common boundary
coordinate list. Their private variable scopes must be disjoint. A variable
occurrence is shared only through its ID. The block partition is supplied to
both algebraic methods; discovering a useful partition is outside this pilot.
No solver receives the generator's parity labels or predicted answer.

Each local operation existentially projects private variables onto the full
boundary relation. Joining the two messages preserves SAT decision and every
boundary assignment that admits compatible local witnesses. It does not
retain the private witnesses. The preimage of an accepted boundary assignment
is the product of its two raw-CNF private completion fibers, because the
private scopes are disjoint. Reconstruction requires the source blocks or
elimination records; a projected row alone is not an inverse.

Freeze `seed=20260912`, boundary widths **3 through 8 inclusive**, right-block
parity **0 and 1** against left parity 0, and **identity** plus a seeded
**variable permutation/complement and clause/literal order shuffle**. This is
24 finite cases, selected in advance with no instance selection after results.
For b>=3, each block uses b-3 private auxiliaries and b-2 ternary XOR equations:
the auxiliary accumulates the first b-2 boundary bits, and the final equation
joins it with the last two. At b=3 there are no private auxiliaries. Every
ternary XOR is emitted as its four ordinary CNF clauses. Thus the pair has
8(b-2) raw clauses and 3b-6 variables. Auxiliary IDs differ across blocks.

Also freeze eight algebra-only cases at b=16,32,64,128, both parity settings,
identity coordinates. They have no exhaustive oracle or boundary validation.
Agreement there is a dependent implementation comparison, not an independent
proof of their decisions or of an asymptotic bound.

## Methods and recognition cost

The recognizer normalizes literal repetitions, discards tautologies, and
groups clauses by identical sorted variable support *within each supplied
block*. For support size k>=1 it accepts precisely when there are
2^(k-1) **distinct normalized clauses** and every clause's falsifying assignment
has the same parity s. The equation is XOR(support)=1 XOR s. Distinctness plus
cardinality covers that entire parity class. Empty clauses and unsupported
groups remain residual and produce **UNRECOGNIZED** for the affine method;
no affine hull or discarded residual is admitted. UNRECOGNIZED is neither
UNSAT nor a claim that the relation is non-affine. Empty CNF is TRUE.

- **Panel GF2:** recognize both blocks from raw CNF; eliminate each block's
  private columns first; retain and reduce all private-free equations; join
  the projected row systems and eliminate on the boundary.
- **Whole-system GF2:** use the identical recognizer on the identical supplied
  blocks, concatenate all rows, and eliminate all columns in ascending ID
  order. Both methods pay recognition independently. This comparator has the
  same algebraic capability and input information as the panel approach.
- **Whole-CNF DPLL:** plain recursive false-first DPLL, unit propagation, first
  unresolved literal branching, raw clauses rescanned; no learning or XOR
  detector. Its output is SAT decision.
- **Point boundary:** visit all 2^b boundary assignments, call that same DPLL
  engine on each local block with the boundary fixed, retain the two exact
  point relations and intersect them. This computes reusable messages as well
  as the decision; that extra work is disclosed when compared with DPLL.

Count recognition clauses/literals, normalization sort items/set probes,
support groups, distinct-clause parity visits, accepted rows and residuals.
Count Gaussian coefficient tests, pivot rows, row XORs, mask-build visits and
the bit spans touched by row XORs. Count DPLL calls, clause/literal visits,
unit assignments, decisions, and conflicts. These are separate work indicators,
not mutually interchangeable operations or a full machine-cost model. Python
integer row operations have width-dependent cost; row count alone is not bit
complexity. Dictionary hashing, allocation, interpreter and sort comparison
costs are not fully modeled. Do not add counters across unlike units or turn
them into a universal speed claim. No timing-based performance claim is made.
Input generation, oracle and test work are reported separately from solvers.

All frozen fixtures use variable IDs in a dense interval of size equal to the
number of variables, including after permutation. The code indexes integer
masks by raw IDs. Its admitted syntax also allows very large sparse IDs, whose
mask spans can be enormous relative to the encoded ID lengths. A general
polynomial-cost implementation must first compress distinct IDs to dense
coordinates and retain that map; the present finite counters do not claim such
normalization or a bound for uncompressed arbitrary IDs.

## Independent checks and rejecting outcomes

The oracle enumerates **all assignments to each local raw CNF's variables plus
the boundary**, evaluates signed clauses directly, then intersects the exact
boundary projections. It shares neither the recognizer nor GF2 nor DPLL.
Each finite case compares the full projected relations at every boundary
assignment, their full join, the point messages, and all final SAT decisions.
The finite receipt also includes exhaustive single-support recognizer tests
for k=1,2,3; fixed and seeded small affine projection tests; normalization and
missing/duplicate clause guards; and a private-scope admission rejection.

Frozen non-affine controls are OR3 joined with all-zero units and exactly-one
on three variables joined with all-one units. Both are UNSAT. Their affine
hulls would admit those opposing assignments (OR3 has the whole cube hull;
exactly-one has the odd-parity hull). The algebraic method must explicitly
decline; raw-CNF DPLL and the exhaustive oracle must reject the join.
A full parity group with an extra duplicate must remain exact, whereas a
missing parity clause replaced with a duplicate must not be recognized.

Any oracle/projection/decision disagreement fails the run. A failed run writes
its error to the output receipt and must be retained in this note before a
correction. Success is finite implementation evidence. The algebra is ordinary
GF(2) elimination and existential projection; this pilot does not establish a
new SAT algorithm, a P=NP result, or a worst-case advantage over conventional
Gaussian elimination. The question is whether compact parity messages repair
the prior exponential point-message carrier, and whether any advantage
survives the equal-capability algebraic baseline.

Reproduce from repository root:

```powershell
python -I -B research/liar-teacher-formalization-2026-09-12/sat_pilot.py
```

## Execution results

Not run at specification freeze. Results will be appended after execution.

First execution passed the frozen fixtures. Independent code review then found
a validation gap: the generic case runner permitted UNRECOGNIZED for controls
but also for parity fixtures. None of the observed parity fixtures had that
status; an explicit parity-recognition assertion now enforces the intended
requirement. The actual eliminated join is now checked at every boundary
assignment as well. These strengthen the frozen obligations without changing
the selected inputs. Review also corrected clause-set operations from one to
two per normalized clause (membership plus insertion), and distinguished the
hypothetical dense-boundary coefficient size from stored global-ID mask spans.
The implementation stores global-ID masks, not a packed dense transmission.
Mapping entries are reported; Python/JSON object overhead is not a bit count.
No test failure occurred. The final receipt below belongs to the corrected
implementation and includes its SHA-256 binding.

Final reproduction command above exited **0** on 12 September 2026 with:

```text
PASS: 24 exhaustive cases, 2 non-affine controls, 276 recognizer truth tables, 38 projection systems, 8 algebra-only cases
```

The 24 parity cases enumerated **87,360 complete local raw-CNF assignments**
and checked **4,032 local boundary memberships**, plus every joined boundary
assignment. Both exact point messages and both projected affine messages
matched the independent oracle in every case. Twelve cases were SAT and
twelve UNSAT; all 24 were recognized. The two non-affine controls returned
UNRECOGNIZED from both algebraic paths and UNSAT from both raw-clause methods
and the independent oracle. The missing/duplicate guards, empty-clause guards,
normalization guard, and private-scope rejection passed.

Every local chain projected to **one parity row** describing 2^(b-1)
boundary assignments. The two point messages together therefore contain 2^b
points, while the two equation messages have a dense coefficient estimate of
2(b+1) bits plus the coordinate mapping. Actual stored global-ID mask spans
are reported separately. This repairs the exponential *point representation*
for this recognized affine family. It does not make arbitrary CNF relations
affine or supply inexpensive general recognition.

The identity-coordinate cases had the following counts. GF2 work is the same
for their SAT and UNSAT members; the final column refers only to UNSAT.

| b | Raw clauses | Point messages | Panel row XORs | Whole GF2 row XORs | Panel / whole coefficient tests | Whole DPLL literal visits, UNSAT |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 8 | 8 | 1 | 1 | 6 / 4 | 124 |
| 4 | 16 | 16 | 3 | 5 | 11 / 18 | 652 |
| 5 | 24 | 32 | 5 | 9 | 20 / 40 | 2,228 |
| 6 | 32 | 64 | 7 | 13 | 33 / 70 | 6,348 |
| 7 | 40 | 128 | 9 | 17 | 50 / 108 | 16,452 |
| 8 | 48 | 256 | 11 | 21 | 71 / 154 | 40,316 |

Recognition was separately paid by each algebraic method. For example, at
b=8 each inspected 48 clauses / 144 raw literals, performed 288 literal-set
operations and 96 clause-set operations, and inspected 144 literals for
distinct-clause parity, obtaining 12 rows in 12 support groups. Panel work
then used 11 row XORs spanning 162 coefficient/RHS bit positions in total;
whole GF2 used 21 spanning 363. The point method made 512 local DPLL queries
and 69,632 literal visits. These quantities are not summed or equated.

Permutation/complement cases preserved all exact relations under their
transported coordinate descriptions. They also exposed implementation-order
dependence: at transformed b=8 UNSAT both algebraic methods used **20 row
XORs**, while panel/whole coefficient tests were 77/165. At b=3 the panel
used more coefficient tests (6 versus 4). The panel is not uniformly cheaper
even in these recorded operation units.

At b=128 the raw pair had 1,008 clauses. Panel/whole GF2 used 251/501 row
XORs, 31,631/63,754 coefficient tests, and 64,002/159,003 XOR bit spans.
Both returned matching decisions for each of the eight large cases. These
are **algebra-only finite runs**, with no independent exhaustive oracle and
no claim that the observed growth proves a complexity bound.

## Why the projection is exact, and what remains open

The recognition argument is a direct clause truth-table argument: a normalized
k-literal clause excludes exactly one assignment on its support. Exactly
2^(k-1) distinct excluded assignments of one parity are the entire forbidden
parity class. Replacing that complete group with the opposite-parity equation
preserves and reflects satisfaction. Group conjunction therefore remains
equivalent only when every group is recognized; residual clauses prevent
promotion of the full block to an affine system.

Row swaps and XORing one row into another are reversible operations on a GF2
equation system. Eliminate all private columns first. Each private pivot row
then uniquely sets its pivot variable after choosing the remaining private
free variables and the boundary; the remaining rows have no private
coefficients. Thus a boundary assignment extends iff it satisfies precisely
those retained rows. Boundary reduction is again reversible. This proves the
existential projection rule as ordinary finite linear algebra; the independent
truth-table suite tests this implementation, including derived contradictions
and the hostile pair x XOR u=0, y XOR u=1, whose projection must retain
x XOR y=1. Simply dropping both private-bearing input rows would lose it.

For blocks F(B,U) and G(B,V) with U and V disjoint, a boundary assignment lies
in both projections iff its two private witnesses can be combined into one
assignment satisfying F AND G. This is why shared private variables are an
admission error here. The proof establishes an existential fiber rule; it does
not reconstruct or retain private witness identities in the message.

**What the panel adds over the equal-capability Gaussian baseline:** an
explicit local boundary interface and, for this implementation's frozen
orders, sometimes fewer elimination operations. It adds no new decision
capability or general complexity improvement over GF2 elimination. The panel
algorithm itself is block-structured Gaussian elimination. A conventional
solver can use private-first ordering and the same disjoint-support locality,
and can retain the same projected rows for reuse. No reuse speedup was measured
here. The matched Gaussian baseline already avoids point enumeration.

The remaining P versus NP obligation is an exact, uniformly affordable method
for arbitrary CNF, including finding usable structure, handling all residual
non-affine constraints, constructing sufficient messages, joining them, and
counting their full representation and computation costs. That obligation is
**OPEN**. These tests close the specified affine pilot only; the independent
oracle proves the finite fixture results, not the unrestricted solver theorem
or the general soundness of its own implementation.
