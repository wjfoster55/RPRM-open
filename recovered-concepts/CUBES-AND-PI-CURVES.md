# Recovery: formula cubes, dimensional algebra, abduction space, centers, and the flexible pi curve

Recovery date: 2026-09-11 (machine-local date). This is a source-grounded retrieval report, not a new mathematical result or a publication edit. Existing source files were read only; historical experiments were not rerun. Reported PASS counts below are the retained receipts' claims, separately identified from the written definitions and proofs.

## Source roots and attribution

`QR` below abbreviates the exact historical root:

`C:\Users\bkbee\OneDrive\DOCUME~1-DESKTOP-06BJRV0-219031\ChatGPT\Quantum Research`

`Foam` abbreviates `C:\github\RPRM-foam-development`, the current implementation root. This recovery read its `AGENTS.md`, README, and `atlas/CURRENT_STATE.md`; the latter is dated 2026-09-08. The historical QR root is not interchangeable with Foam. LawCube and RelationForge are independent exact-software donors under `C:\github`; neither contains an `AGENTS.md` at its root.

Most QR research notes identify their date and evidence status but do not name a human author. Accordingly this report calls them **assistant research records**, not William's verbatim speech. Phrases explicitly attributed to William in those records are secondary quotations unless the source addendum supplies the original export turn. Exact original task IDs are preserved where a source supplies them.

## What the recovery actually found

There is substantial completed mathematics behind the remembered cube. It is not only a picture, an unfinished plan, or the public paper's four-corner example. In particular:

1. **General-dimensional formula translation exists in a precise finite-product form.** The Aug19 Graded Scar Cube 02 note proves a general-n Boolean cube transform, its exact inverse, grade-blindness theorem, general-n ternary line-check kernels, and a common tensor-grid Newton interpolation theorem. This is the strongest located donor for “formula in any dimensionality.”
2. **An executable self-checking finite formula compiler exists.** LawCube translates complete scalar three-input F2/F3 tables to exact polynomial normal forms and back; it emits standalone table/polynomial evaluators with exhaustive per-address self-checks. RelationForge separately rotates finite relation apertures and returns complete fibers.
3. **A dimensional constructor exists.** Full-Zip Hypercube Ladder constructs Q0 through Q4 by direct prior-artifact byte handoff, including all inherited faces, incidence, boundary, and the new top cell.
4. **Several distinct abduction constructions were completed.** The `7 -> 8` missing-Walsh-direction lift is exact; the ternary affine code has complete board and correction receipts; the moving vacancy has an exact cube-face adapter. These are different operations with their own carriers.
5. **A center is not the universal abduction vacancy.** The source explicitly distinguishes geometric center, numeric zero, puncture, missing port, candidate fiber, and free cell. A later Seam Zero locator Board can correctly infer `ONE(6)` at a withheld raw-source port while the translator's geometric middle remains raw `5`, centered `0`, normalized `1/2`.
6. **The “true pi” curve has coherent retained formulations and original user wording.** The Aug11 Hilbert/Aimer note and independent Curve-Frame audit develop the flexible Bishop-frame law. A subsequently located export explicitly recovers the **Circle Compiler Candidate**: metric-addressed circles, pi-factored dimensional transport, bounded phase, and winding/readback. Original user speech says it is an equation for curves, not a number. See the source addendum below; this is independent of decimal pi-window and nines-complement work.
7. **Some broader compositions remained designs in the inspected bytes.** The centered translator hub and centered cube-sphere experiment folders contain only prefreeze designs. The rotated-face abduction atlas record explicitly says its combined bench was not executed. That does not undo completed component theorems, and it is not evidence that no later source elsewhere exists.

## 1. The strongest general-dimensional formula donor

Source: [Graded Scar Cube 02, NOTE.md](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_GRADED_SCAR_CUBE_02/NOTE.md:1>), dated **2026-08-19**; [retained results](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_GRADED_SCAR_CUBE_02/RESULTS_SUMMARY.md:1>).

### Binary cube: exact formula and inverse

Carrier: all functions `f:{0,1}^n -> R`, equivalently real-valued functions on subsets of `[n]`. Origin, coordinates, and multilinear basis are frozen. Equal values at different corners remain separate table occurrences.

Definition A.0, line 26:

```text
r_S = sum_{T subseteq S} (-1)^(|S|-|T|) f(T).
grade(r_S) = |S|.
```

Theorem A.1, line 38, gives the exact inverse:

```text
f(S) = sum_{T subseteq S} r_T.
```

The transform is a linear bijection with determinant 1. With `mu` the signed subset-inclusion matrix and `zeta[S,T]=[T subseteq S]`, `r=mu f`, `f=zeta r`, and `zeta mu=I`. The written proof expands the matrix product to `(1-1)^(|S\U|)`.

Proposition A.3, line 67, states three equal descriptions: scars are anchored mixed discrete derivatives, coefficients of the unique multilinear polynomial, and the inverse coordinates of the subset-incidence evaluation basis. Thus:

```text
f(x) = sum_{S subseteq [n]} r_S product_{i in S} x_i.
```

There are `C(n,k)` coefficients at grade k and `2^n` total. For n=3 the grade count is `1+3+3+1=8`. This is an actual all-finite-n theorem, not merely an n=3 table extrapolation. Its empirical verification coverage is narrower and separately stated: direct submask sums and fast tensor transforms, exact rational round trips for n=1..12, and floating tests with maximum error `4.60e-14` under tolerance `1e-9`.

### What a lower-dimensional/grade receiver misses

Definition B.0 and Theorem B.1, lines 103 and 107, define the receiver `R_k(f)=(r_T:|T|<=k)` and prove:

```text
ker R_k = span{x^S : |S|>k}
dim ker R_k = sum_{j=k+1}^n C(n,j)
rank R_k = sum_{j=0}^k C(n,j).
```

This is a complete ambiguity description: given one compatible table `f0`, the entire compatible family is `f0 + ker R_k`. It supplies the missing directions rather than guessing a completion. The source gives minimal scar-support and value-support witnesses for every k<n. For a three-cube, seeing grades 0,1,2 still leaves one three-way direction.

The hostile coordinate case is crucial: Graded Scar Cube 01 recodes a constant table by an arbitrary invertible basis into coordinates with positive grades 1,2,3, then exactly reconstructs the constant. Grade is relative to the declared anchor/basis, not an intrinsic property of a bare table under all representations. A grade-3 value scar also does not imply noncommuting operations: commuting bit setters can feed a three-way product. Conversely noncommuting matrix products can have the same determinant receiver.

Exact donor: [Graded Scar Cube 01 retained results](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_GRADED_SCAR_CUBE_01/RESULTS_SUMMARY.md:1>), PASS, two non-importing exact-rational implementations and 51 registered rejected mutations.

### The genuinely broad finite-product translation theorem

Theorem C.3 at NOTE.md line 258 is broader than a binary cube:

> Let `A_1, ..., A_n` be finite node sets of reals, each with a fixed enumeration. Define `N_(i,j)(x)=product_{l<j}(x-a_(i,l))` and tensor products `N_alpha=product_i N_(i,alpha_i)`. Evaluation on `product A_i` is triangular with nonzero diagonal, so every function on the grid has a unique expansion `f=sum c_alpha N_alpha`; coefficients are mixed divided differences at the chosen anchor.

The binary scar transform is the `{0,1}` instance; the ternary grid is the `{-1,0,1}` instance. It is classical multivariate Newton interpolation, with its established ancestry explicitly retained in Part D. This offers a precise recoverable reading of a “formula translator of any dimensionality”: any **finite number of axes**, each with an explicitly finite distinct-node carrier, admits an exact table-to-polynomial coordinate system and inverse. It does not assert that arbitrary continuous formulas, unknown laws, algorithms, and all their future behavior are recovered from a finite table.

The note records **328 assertions, zero failures** (241 A/B plus Walsh, 87 C). It explicitly claims established mathematics/recontextualization, not novelty. Its five receiver kernels have a common degree-class form, but C.4 preserves an attempted umbrella's failure: symmetry alone is insufficient, and no one nontrivial common blindness theorem was supplied. That correction belongs with the successful common interpolation theorem.

## 2. The ternary self-checking cube and its general-n theorem

Sources: [Zero-Cube exact results](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_MATHSEED_0_1/zero_cube/RESULTS_SUMMARY.md:1>); Graded Scar Cube 02 NOTE.md, Part C beginning line 175, Theorems C.1/C.2 at lines 200/229.

Carrier: `{-1,0,1}^n`, real/rational/integer value tables as specified by each source. A line is `(c-d,c,c+d)` entirely in the carrier, with nonzero `d in {-1,0,1}^n` up to sign. The check is supplied explicitly:

```text
D_line(f) = f(c-d) - 2 f(c) + f(c+d).
```

General formulas recovered in the written theorem:

```text
number of lines = (5^n-3^n)/2
axis-line kernel = multilinear functions, dimension 2^n
full-line kernel = affine functions a0 + sum_i b_i x_i, dimension n+1
axis + pair-diagonal kernel = full-line kernel
center-only kernel = constants direct-sum odd functions
center-only nullity = (3^n+1)/2
extra center-blind dimensions = (3^n-1)/2 - n.
```

The proof first uses axis lines to eliminate squared coordinates; pair diagonals then eliminate every mixed multilinear coefficient. The center equations see only whether the even part is constant; arbitrary odd functions remain invisible. General-n checks in the retained follow-on cover n=1..5.

The n=3 completed receipt has 27 cells and 49 lines: 27 axis, 18 plane diagonal, 4 body diagonal. Full rank is 23 and nullity 4. All 108 one-cell mutations and all 5,616 two-cell amplitude assignments in its declared amplitude census were detected and uniquely localized by the full syndrome. Center-only checks detect all single-cell mutations but merge antipodal positions. The exact counterfeit is `-1` at `(-1,-1,-1)` and `+1` at `(+1,+1,+1)`: every center check remains zero while 12 lateral checks fail.

This is a concrete self-checking construction with a complete declared syndrome map. It is also a strong reason not to replace the whole cube with its aesthetically central rays. The geometry did not choose the second-difference law; a different supplied law can have different kernels.

## 3. Completed formula software: LawCube and RelationForge

### LawCube

Source: [README](C:/github/LawCube/README.md:1), [final verification](C:/github/LawCube/verification/FINAL_VERIFICATION.md:1), sealed 2026-08-13 against source commit `efd4a9b`.

Frozen input is a **complete scalar law `f:F_p^3 -> F_p`, p in {2,3}**. Arity is exactly three; no vector-valued or arbitrary-arity package is claimed. F2 uses the eight multilinear/ANF coefficients; F3 uses 27 reduced-polynomial coefficients with each exponent in `{0,1,2}`. Address order is `LEX_X2_FASTEST`; centered F3 glyphs are a display adapter only.

Two independently written transformations are retained: tensor-product Möbius/Lagrange interpolation and evaluation-matrix inversion by exact modular Gauss–Jordan. The matrix proof checks:

```text
E*T_A = T_A*E = E*T_B = T_B*E = I
T_A = T_B.
```

Consequently transform correctness on the whole vector space follows by linearity; the package does not pretend to enumerate `3^27` F3 laws. Named input actions use pullback `f(g^-1 x)`; output actions use `h(f(x))`. Symmetry group and equivalence receiver are explicit.

Generated standalone modules contain both table and polynomial evaluators and `self_check()` over every address. The retained final receipt reports **2,469 tests passed**, all 256 F2 laws, F3 structured corpora plus 512 deterministic cases, and matrix agreement. This is completed, reusable code with a bounded scope. “Self-checking” here means independently comparing two evaluations of supplied law bytes; it is not proof that the supplied law describes an unknown world.

### RelationForge

Source: [README](C:/github/RelationForge/README.md:1), [final verification](C:/github/RelationForge/verification/FINAL_VERIFICATION.md:1), recorded Git head `e5a1f52e2e064a199a32c90caa7b65f83671f766`.

A relation is a complete finite set of typed rows. The caller leaves one role as APERTURE and supplies every other role. The exact candidate fiber is returned as NONE/ONE/MANY with its complete ordered members. Source atoms are exact integers or printable ASCII strings. Invalid requests, out-of-carrier values, unresolved live seams, and complete empty fibers are different outcomes.

The compiler emits a standalone relation evaluator. Audit compares direct scanning, a separate positional index, and generated evaluators over **5,934** corpus queries; the retained result says **16/16 gates**, 238 tests and 384 hostile audit controls passed. LawCube's `RF_EXCHANGE_1` export provides roles `(x0,x1,x2,y)`; relation aperture rotation makes forward and backward finite questions concrete. This is the practical bridge between formula compilation and missing-port inference, although no arbitrary symbolic-algebra engine is installed in RelationForge.

## 4. Dimensional construction: Full Zip and cubical multigrading

Source: [Full-Zip Hypercube Ladder retained result](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_FULL_ZIP_HYPERCUBE_LADDER_01/RESULTS_SUMMARY.md:1>), PASS on Q0..Q4; 55 registered mutations rejected by both paths.

Carrier: nonempty face words `W_n={0,SPAN,1}^n`; degree is number of SPAN coordinates. `SPAN` is a free interval/cell, not numeric midpoint or balanced ternary zero. Construction copies both old caps, sweeps the inherited proper faces, and creates one new top cell. Every next stage consumes reparsed literal bytes of the preceding artifact; both inherited layers decompile back to that prior artifact including incidence and boundary.

```text
n   f-vector             total faces   incidences
0   1                    1             0
1   2,1                  3             2
2   4,4,1                9            12
3   8,12,6,1            27            54
4   16,32,24,8,1        81           216

f_k = C(n,k)*2^(n-k).
```

The complete mathematical face enumerator is `(2+t)^n`. The richer multigraded enumerator `product_i(x_i+t_i+y_i)` retains endpoint/free-axis identities. This is detailed in [Ternary Clockwork and Multigrading Scout](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_TERNARY_CLOCKWORK_LAYOUT_AND_MULTIGRADING_SCOUT_0_1_SHADOW.md:636>), Aug11. For `W_(p+q)=W_p x W_q`, a cell has bidegree `(i,j)` and total degree i+j. A line display, a 9x9 display of W4, and a cubical display can be invertible layouts when their exact decoder and transported incidence are retained.

The same note's section 9 (line 719) preserves the six-layer route:

```text
SPEC_RELATION -> EXTENSIONAL_FUNCTION -> ALGORITHM
-> IMPLEMENTATION -> EXECUTION_TRACE -> OBSERVED_RESULT.
```

An equation or function can be placed on this carrier, and certified independent transformations can populate commuting cubes. Merely possessing multiple transformations does not construct their commuting squares. This distinction preserves the useful dimensional algebra while preventing a bare “cube” name from claiming every solver, trace, or computation simultaneously.

## 5. Abduction is a space of possible completions

### Completed `7 -> 8` carrier lift

Source: [Abductive Carrier Lift retained results](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_ABDUCTIVE_CARRIER_LIFT_01/RESULTS_SUMMARY.md:1>).

The three-bit pairwise-marginal map is constructed from states and pair definitions, not from a preinstalled parity answer. It has rank 7 and primitive missing direction:

```text
[1,-1,-1,1,-1,1,1,-1].
```

Within the **declared eight-character Walsh probe grammar**, only mask `111` raises rank to 8. The expanded receiver exactly reconstructs all eight point masses and a nonuniform rational distribution. This is completed finite abduction: witness a missing direction, search an admitted probe space, retain the uniquely separating probe, lift the carrier, and reconstruct.

The tiny Tetris arm separately proves that a typed HOLE does not select its filler: both B0 and B1 fill the pictured slot, but only the matching connector closes the relation. One connector probe is necessary and sufficient. An unrelated extra bit does not help.

The retained receipt says 35/35 runner checks, 31/31 checker checks, and 1,661/1,661 rejected mutations. The shared eight-bit index for cube states, Walsh masks, and Clifford blades is explicitly separated from their operations: Walsh uses untwisted XOR; Clifford uses sign-twisted XOR. Same index and grade counts do not equal one algebra.

### Whole-board abduction launchpad

Source: [William steering amendment 0.36](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_NARIBRAIN_WORLD_MACHINE_RESEARCH_RUN_0_1/USER_STEERING_AMENDMENTS_0_36_TERNARY_CUBE_ABDUCTION_LAUNCHPAD.md:1>), **2026-08-12**, assistant-authored preservation of William's steering.

Coherent attributed passage:

> William states that once the complete `3 x 3 x 3` carrier exists, the remaining relations can be abducted extremely quickly. The point of the first complete cube is not merely to possess 27 addresses; it is to amortize the cost of future discovery by reusing one frozen local enclosure for many candidate relations.

For each registered candidate f, the complete board is `B_f=[f(x):x in canonical T^3 order]`, retaining typed ONE/MANY/NONE/LIVE/frontier/out-of-carrier results. The proposed pipeline is:

```text
ABDUCT candidate -> GENERATE all 27 entries -> COMMIT immutable wave
-> quotient declared exact symmetries -> compare signatures
-> choose smallest distinguishing address/crossed probe -> next candidate grade.
```

Signatures include slices, center/axial/two-active/corner strata, orbit/stabilizer, commutator/reversal residuals, exact distinguishing addresses, and lost fibers. The note is a discovery method, not a result that every law is inferable from 27 samples.

The adjacent [passed donor memo](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_NARIBRAIN_WORLD_MACHINE_RESEARCH_RUN_0_1/SOURCE_MEMO_EXISTING_TERNARY_CUBE_RECEIVER_2026-08-12.md:1>) identifies `RPRM_POLYRHYTHM_EVENT_TO_TERNARY_GRID_01`: all 27 F3^3 addresses are visited by ticks 0..89, first coverage at 70, and all 81 supplied affine laws reconstruct through immutable waves using a separately supplied 45-line Corner registry. This is a completed scaffold, not proof that the temporal traversal generated cubical incidence by itself.

### Tile / Board / Atlas and the withheld center

The current math-lenses skill defines each level's own finite hypothesis/experiment/outcome/narrowing/fiber contract: a Tile is one typed capability with vacancy and commuting receipt; a Board uses eight closed Tile artifacts to constrain one deliberately withheld capability; an Atlas uses eight closed Board artifacts to constrain one integrated withheld capability. A visual center alone does not define any of those hypotheses.

The current Foam [Patient One William contract](C:/github/RPRM-foam-development/patient-one/WILLIAM_CONTRACT.md:1) gives the original task locator for this line: `01a0087d-c180-71e2-9e36-0d10f68562e6`. It also gives Full-Zip/eight-nine/half-gap/pi source task `019fec4c-73db-74c2-9079-55df4b51ab6c`. These are exact reopen locators; the additional export quotations recovered later appear in the source addendum.

The [Aug12 bridge understanding packet](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_BRIDGE_FAMILIES_FULL_REREAD_UNDERSTANDING_PACKET_2026-08-12.md:363>) already defines Concept Sudoku as an ability-incidence board: primitive capabilities as rows, frozen bosses as columns, crossing tests constrain several rows, missing cells identify useful next tests, stop at a uniquely determined smallest viable architecture in the admitted carrier. Foam's `brain/NARI_QUANTUM_BRAIN_ASSESSMENT.md` explicitly says NARI-NG does not implement the full Tile/Board/Atlas system. That does not deny the existence of completed individual Tiles or Boards.

## 6. The center/vacancy distinction has completed examples

### Moving Vacancy Weave

Source: [retained results](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_MOVING_VACANCY_WEAVE_01/RESULTS_SUMMARY.md:1>), PASS, two non-importing implementations, 84 rejected mutations.

Carrier: 26 distinct tokens plus one typed vacancy in a 3x3x3 site grid. All 27 oriented axis lines are read as occupancy words. Every vacancy position gives exactly 24 `111` lines and three deficient lines, one per axis. The three deficiencies intersect at one site. Their coordinate words locate the vacancy:

```text
011 -> low endpoint
101 -> middle
110 -> high endpoint.
```

The exact adapter `011->0`, `101->SPAN`, `110->1` bijects vacancy addresses with W3 cube face words. Counting middle components gives face strata `8,12,6,1`; grid nearest-neighbor steps correspond to Hasse covers. All 108 directed moves retain all token identities and change exactly five line records. A local `111` word leaves 24 possible global vacancy sites; three axis observations of a gap are not three gaps.

This is a real bridge earned by a map, not by a shared picture. Spatial vacancy, abstract cell, numeric zero, cancellation in a boundary, missing knowledge, and capacity remain separate source types. There is no internal 27-cycle in the 14/13 bipartite grid; the closed schedule needs a separately typed external port (length 28). An authored n=4 scaling arm checks 81 vacancy sites and 216 grid/Hasse edges.

### Center-punctured ternary code

Source: [Ternary Dimensional Ladder results](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_TERNARY_DIMENSIONAL_LADDER_01/RESULTS_SUMMARY.md:1>).

The supplied affine F3 code on F3^n has length `3^n`, dimension n+1, minimum distance `2*3^(n-1)`, and unique-decoding radius `3^(n-1)-1`. Removing the geometric center lowers distance by one but leaves this radius unchanged. Thus a literal center hole is not required for the error radius.

At n=3, 81 codewords have distance 18 and correction radius 8. The ninth-error boundary has a concrete ambiguity: a received nine-cell z=1 sheet is distance nine from both zero and the codeword z. Four independent anchors reconstruct four affine coefficients; four coplanar anchors leave a three-member slope fiber. The exact lift `g-a,g,g+a` exhausts the next-dimensional affine code. These receipts distinguish center, puncture, vacancy, field zero, clean error, and bridge debt.

### Zero-Source Locator Board

Source: [Seam Zero foundation Tile](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/experiments/RPRM_SEAM_ZERO_FOUNDATION_TILE_01/README.md:1>) and [registry record](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/math-discoveries/entries/e6affe80-92bd-4069-9f31-ca6ddc1844a2--seam-zero-6-bar-4-to-0-bar-1-oriented-foundation-translator.md:62>).

The translator's oriented rail is raw `(6,5,4)`, centered `(-1,0,1)`, normalized `(0,1/2,1)`, with `tau(x)=(6-x)/2`. Its geometric midpoint is raw 5. The separate Board's **raw-source** hypothesis carrier `{4,5,6}` is constrained by `tau(x)=0`, `centered(x)=-1`, `predecessor(x)=5`, and `successor(x)=VACANT`, giving the complete fiber `{6}`. The withheld center is `ONE(6)` because that center is a raw-source question, not the translator's geometric midpoint. This is particularly strong evidence that “center” was meant as a question-bearing role, not one immutable numeral or hole.

## 7. The recovered “true pi” curve concept

Primary located conceptual sources (assistant records):

- [Hilbert Diagonal, Aimer, and Negative-Return Scout](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_HILBERT_DIAGONAL_AIMER_AND_NEGATIVE_RETURN_SCOUT_0_1_SHADOW.md:308>), **2026-08-11**, `READ_ONLY_EXACT_TRANSLATION_WITH_FINITE_DISCRIMINATOR_DESIGN_NOT_EXECUTED`.
- [Curve-Frame “Three With Two” Hostile Audit](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_CURVE_FRAME_THREE_WITH_TWO_HOSTILE_AUDIT_0_1_SHADOW.md:19>), **2026-08-11**, `PASS_WITH_STRICT_RECEIVER_AND_LINEAGE_CLAMPS` (audit of the note, not an executed all-curves bench).

The audit records William's phrases together:

> William's “true circle is a flexible equation,” “lock real 3D,” and “do three with two rather than three with four” intuitions have one unusually exact differential-geometric translation.

### Carrier, operation, and full reconstruction

For a sufficiently regular unit-speed Euclidean curve `alpha(s)` in R3, retain the oriented frame `F=[T,E1,E2]` and two bend channels `(k1,k2)`. The Bishop/rotation-minimizing law is:

```text
alpha' = T
T'  =  k1 E1 + k2 E2
E1' = -k1 T
E2' = -k2 T.

F' = F A,
A = [[0,-k1,-k2],[k1,0,0],[k2,0,0]],
A^T = -A.
```

Thus orthonormality is preserved: starting at `F^T F=I`, `(F^T F)'=A^T+A=0`. The inverse-looking paired entries make the symmetric part zero; the matrix itself is not zero. This is the source's exact “self-zipping” construction.

The complete reconstruction data are the two **functions** k1(s),k2(s), initial placement alpha(0), and initial frame F(0); a non-arclength parameter additionally requires speed. ODE existence/uniqueness supplies reconstruction. The two instantaneous values alone do not encode a full orientation. Initial roll and accumulated lineage remain retained. Arbitrary roll would require the additional normal-plane angular rate w.

In Rd the recovered formula is:

```text
alpha' = T
T' = sum_{i=1}^{d-1} k_i E_i
E_i' = -k_i T.
```

It transports d frame vectors through d-1 live bend channels under a named zero-roll gauge. Generic SO(d) angular motion has `d(d-1)/2` independent rate entries. “Three with two” is therefore a stateful curve transport mechanism with a retained initial frame, not an unsupported stateless compression.

### The circle is the locked solution

At constant `k1=1/r`, `k2=0`, with compatible initial data, the curve is a Euclidean radius-r circle, curvature 1/r, torsion zero. One positive turn closes at:

```text
(1/r)L = 2*pi
L = 2*pi*r.
```

The source states: “a flexible curve equation whose circle locks.” Local curvature generates motion; ordinary pi enters the global turn/closure receipt. This is a coherent geometric concept and should not be reduced to a decimal digit operation.

The audit retains three independent closure readouts:

```text
POSITION_CLOSED: alpha(L)=alpha(0)
TANGENT_CLOSED:  T(L)=T(0)
FRAME_CLOSED:    F(L)=F(0).
```

Position and tangent can close with residual normal-frame holonomy. An SO(3) circle frame closes after 2*pi while a continuously marked quaternion lift changes sign, closing after 4*pi. Three noncollinear points determine a circle within the circle model but not an arbitrary smooth curve. Finite samples do not establish an unrestricted all-real curve law. At zero curvature the Bishop frame remains valid; piecewise corners need jump receipts. A non-Euclidean metric changes circumference laws.

The inspected notes explicitly decline a new numerical value of pi. That is their mathematical interpretation; the source addendum now preserves William's direct wording that the intended object is an equation for curves rather than a number. The recovered concept is the flexible curve carrier and its closure; the decimal pi window is a separate donor, `math-discoveries/outputs/RPRM_PI_THREE_LEVEL_345_MATRIX_01_EVIDENCE.md`, whose finite prefix/occurrence fibers do not define the curve law.

### Evidence state

The original Scout includes exact equations and derivations and a smallest finite discriminator **design**; its independent audit says the formula-level disagreements were resolved. No Bishop/curve-frame experiment directory or completed result was located in the targeted QR experiment inventory. This report therefore recovers the written formulation and successful hostile note audit, without fabricating a missing executable receipt.

## 8. The larger translation cube compositions that remain separate

Source: [Rotated-Abduction Cube Atlas and Moving Receiver Scout](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_ROTATED_ABDUCTION_CUBE_ATLAS_AND_MOVING_RECEIVER_SCOUT_0_1_SHADOW.md:1>), Aug11, `NEW_COMPOSITION_BENCH_WARRANTED_NOT_EXECUTED`.

Its exact proposal is a framed seed-face payload transported by signed cube symmetries with equations, receivers, restrictions, and lineage conjugated along with the display. It checks roll/stabilizer choices, all twelve shared edges and eight corners, then exposes two different completion spaces:

```text
FaceFill(five-face open box) = compatible missing square faces
TopFill(six-face boundary) = compatible admitted three-cells.
```

Either can be empty, singleton or multiple. A compatible hollow boundary need not supply a top cell; one must declare the filling grammar. The square Walsh receiver `m=H4 p`, `p=(1/4)H4 m` is a lossless payload transform, not itself the cube symmetry group.

The moving center's exact affine reading is `u_c(x)=x-c`; every dependent operator moves by conjugation `F_c=T_-c F T_c`. A no-edit closed cursor loop returns exactly. Moving the same payload across differently graded W3 face cells needs dimension-changing adapters. Physically translating a sphere inside a cube is yet another operation.

The related [Centered Cube-Sphere Polar Port Scout](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_CENTERED_CUBE_SPHERE_POLAR_PORT_SCOUT_0_1_SHADOW.md:1>) has exact geometric radial-adapter/polarity derivations, dated Aug11, but `EXACT_GEOMETRIC_SCOUT_NOT_YET_BENCHED`. Direct inventory found only `PREFREEZE_DESIGN.md` in `experiments/RPRM_CENTERED_CUBE_SPHERE_POLAR_PORT_01` and `experiments/RPRM_CENTERED_TRANSLATOR_HUB_01`. These precise open compositions should be retained beside the completed pieces above, not used to classify all cube mathematics as unfinished.

## 9. Relation to proof donut and what a future consolidation must preserve

The current public [proof-donut document](C:/github/RPRM-open/docs/proof-donut.md:1) already defines a certificate method around a missing question, with no required circular drawing or fixed number of checks. Its full completion fiber is `F(g)={w in W(g):R(g,w)}`; compatible constraints intersect one joint source fiber. It includes the four-corner multiaffine center rule and the hostile stronger grammar that agrees on the boundary while changing the center.

The recovered cube body extends that foundation with actual general-n transform coordinates, finite-product interpolation, graded missing directions, line-syndrome kernels, a dimensional artifact constructor, a moving-vacancy adapter, and executable finite formula tooling. The flexible pi curve adds a different source: a stateful differential generator whose invariant is preserved during construction and whose global closure depends on the receiver. It would lose important mathematics to merge these into one slogan or to keep only the public four-lane average.

Substantial adjacent concepts found but not fully reopened here:

- Cube-to-simplex translation and triangulate-then-promote have completed `RESULTS.json` donors referenced by the geometric scout; they preserve different support/atlas receivers.
- Self-zipping incremental frontiers, nested subcube certificates, and proof-lineage equivalence routing have detailed scout schemas. Their construction/provenance, incremental cost, and emitted-size claims should remain separate.
- Patient One's current recursive folder uses complete rooted artifacts as next-grade occurrences and retains a live middle/gap; its William contract explicitly says cellwise zipper motion, discovered fit policy, and bounded agitation remain owed.
- The original Tile/Board/Atlas task and Full-Zip/pi task are exact transcript reopen routes supplied above. The source addendum preserves direct user passages and later assistant consolidations without replacing the mathematical donor records.

## Verification of this recovery

This report was produced by targeted filename/content searches followed by bounded reads of exact source notes and receipts. No broad experiment reruns, fabric compilation, source edits, publication, or migration took place. The strongest recovered claims distinguish written general proofs, finite retained executions, successful note audits, and designs. The inventory checks for design-only folders are present-day observations of those inspected directories; all other PASS/test figures are attributed historical receipt statements.


## Source addendum: exact user turns, direct abduction-space bridge, and Circle Compiler Candidate

These sources were located after the initial report draft. They materially strengthen the recovery and must not be omitted from its conclusions.

### Direct user formulation of the flexible curve (original transcript export)

Source: `C:\Users\bkbee\Downloads\Investigate RPRM bridge families CHATLOG.txt`, line **11190**. The export has no per-turn timestamp or machine role field at this location, but the conversational alternation identifies this as William's turn and the subsequent assistant response directly interprets it as a curve-transport law. The dated Aug11 Scout/audit supplies a contextual date for the research artifact, not an independently verified timestamp of this exported turn.

> Well, I think, I think, I don't think it will be pi. I think it'll be flexible. I think that's the kind of the point. I think maybe like, maybe the reason pi is so hard locked is like the only way they could do it or something in this realm, for some reason. For some reason, is there, would there be some math that would explain that why pi is the only reason they can do it like three, the pressure of the three points coming together or something, like, because I bet it's something like that. But I think the like true circle, true pi I'm thinking of, I don't think it's gonna be like a number, I think it's gonna be an equation, right? It's gonna be like, oh, this is the equation for curves or something. And then you can skip over our 4D, or our fake 3D math with true 3D math, and confirm, then you full zip through our 3D, like our 4D, our four to three 3D math with the real 3D math, and then you've locked in, then you lock in the whole three, and then you're gravy baby.

At line **11221**, William then asks:

> Yeah, and then if you follow the logic, it's like, okay, well, what can you do now that you're doing three with two instead of three with four?

This is direct evidence that the intended object was flexible and operational: the wording explicitly declines a number and calls for an equation for curves. The Bishop construction in section 7 is an actual historical response to that turn, not a new reconstruction invented during this recovery.

### Direct user formulation of equation dimensionality and abduction

Archive: `C:\Users\bkbee\Downloads\QM_THEORY_DEVELOPMENT_CHAT_2_FULL_EXPORT_2026-08-19.zip`.
Member: `QM_THEORY_DEVELOPMENT_CHAT_2_EXPORT_2026-08-19/01_FULL_TRANSCRIPT.md`, **Message 009 — User**, heading line 1095, body line 1097. The export date is 2026-08-19; no individual turn timestamp was read. Only this member was read in memory; the archive was not extracted.

> Okay, so my brain is now thinking, I don't, I assume this is possible, but I don't know if I've heard this before. I may have heard this before, I may not. I honestly don't know. But can you make any math equation equal zero? Like, doing some weird math shit, right? I assume you can do that. So now what I'm thinking, so you know what it is? When we're doing math shit and we're moving stuff left and right on the equation thing, we're moving stuff like, it's like zero, the, like, the equal side is infinity. It's like infinity, the number sits on infinity, so right? So it sits on top of zero. Or not zero. It sits on top of infinity. And I think maybe sometimes we have treated as zero, but like, it's not wrong because the zero sits on top of infinity. So if we can make, so when we're moving things left and right on the fucking, like, moving them over the equal sign, we are moving it, like, into the abduction space. Right? We're saying, hey, you can figure out this with this. If you take this out and put it over here, you can figure this out, or something like that. And, like, that's why you can move around and it always equals, right? That's the, the infinity space is the abduction space, right? That's the stuff where we don't know things, right? So when you're, and then like the, what, the, the, not the division sign, but like the things on, the fraction sign, you know, the line on the side, that's like 2D dimension space or something, or 3D division space or something. And that's why you can move it up and down, but it always has to equal, right? Equal whatever. I know it doesn't have to equal, but like it has to have equivalence or whatever. Or whatever the math word is, I don't know. And so like, if you can bring any mathematic equation to zero, you can build it back up. Like bringing a mathematical equation to zero is bringing, making it a still point. And then you can fucking, so like, maybe like, you know, when we think of like, oh, you take this and you move it over to the zero, are we like implying a step where actually you take it all to zero, or like, I don't know what I'm trying to say here, like... Like, are we, are we sweeping under the rug, moving something over, like the cost of moving something over to infinity, or like not to, you know, to the abduction space? Or something? I, you know, like, I feel like I'm intuiting on something around here. But like, I can kind of see now, like, if you had like an equation and you had like a slider, you could like slide it down from like, let's say it's a third dimension, quote unquote, you know, interpret me correctly, a third dimensional level equation, whatever that means in that space, right? And then you could like have a slider, and you could slide it down all the way to zero, and you could like see the parts go over and like, you know, it wouldn't just be going over like one by one, right? It would be like reconstructing itself as it goes, and eventually it would become, you know, whatever the base form of it is, like split up into its parts, I guess.

This supplies the original “slider”/dimensional-equation idea and the abduction-space connection in one coherent user turn. It asks for equation lowering and rebuilding with retained equivalence and hidden costs. It does not by itself identify that full intended machine with the later polynomial cube theorem; that exact all-purpose identification remains unresolved.

### A direct published-in-workspace bridge: cube abduction space is a quotient of blind modes

Source: `C:\Users\bkbee\Downloads\RPRM_MATHEMATICAL_TOOLKIT_CONSOLIDATED_STILL_POINT_0_2.md`, document date **2026-08-17**, section 12, especially line **1349**. This assistant consolidation labels itself an anti-forgetting reference and supersedes 0.1 for mathematical use. Its exact recovered definition is:

```text
Counterfeit_n = ker(D_center) / ker(D_full)
dim Counterfeit_n = (3^n-1)/2 - n.
```

It states, at line 1349:

> This locates the real many-dimensional abduction space in the exact numerical bench: not in the scalar center value, which is `NONE` or `ONE`, but in the exterior modes that the center receiver cannot distinguish from lawful full closure.

This explicitly connects the completed ternary checking cube to the abduction-space language. At n=3 the quotient has dimension 10; at n=2 it has dimension 2. The full and center kernels and their proofs were recovered above. This is stronger provenance than inferring the relationship because two diagrams look alike.

The same toolkit's section beginning line 1900 separates three levels: Tile alternatives are rules/coordinates for one capability; Board alternatives are adapters/integrated contracts for a center capability; Atlas alternatives are workflow laws across Boards. The center value and the space of missing operators/interior modes are explicitly distinct.

A second assistant consolidation, `C:\Users\bkbee\Downloads\rprm_consolidated\RPRM_EXHAUSTIVE_HANDOFF_2026-08-19.md`, section **4.2**, directly connects the scar cube to the retained seam construction `Whole = A ⊕_R B`: grade 0 anchor, grade 1 each part alone, grade 2 pairwise seam, grade 3 seam no pair predicts. This is an attributed synthesis, not an additional independent experiment. Its adjacent blanket prose about Möbius and Walsh as the same decomposition must be read with the exact Graded Scar Cube 02 separation: they share the degree filtration but not the same kernels.

### Circle Compiler Candidate: coherent complete source passage

Source: `C:\Users\bkbee\Downloads\chatgpt_file2.txt`, **entire file, lines 1–276**. It is an assistant answer pasted into a plain text file; author identity, conversation ID, and timestamp are absent. It therefore supplies exact preserved assistant wording and a precise candidate definition, but not an execution receipt or dated original user utterance.

This source says that Gauss–Bonnet/holonomy suggestions are neighbors, while the remembered simpler object was the **typed pi stack**. That corrects the initial report's tendency to lead exclusively with the Bishop/holonomy branch. Both historical branches remain preserved; the Circle Compiler source must be treated as a primary recovery candidate for what the user meant by “true pi.”

The compact construction is:

```text
C(M,mu,r,R) -> (S_M(r), pi_(M,mu), transport, phase, winding, readback)
```

The source retains metric/norm, length measure, scale, chart, orientation, and receiver as inputs. It splits three exact standard ingredients:

1. **Metric shell:** `S_M(r)={x:||x||_M=r}`. For the native L-infinity length convention, the unit square has perimeter 8 and diameter 2, giving the metric-indexed ratio 4. It explicitly retains ordinary Euclidean pi as a different metric member.
2. **Dimension transport:** `V_n(r)=(2*pi*r^2/n)V_(n-2)(r)`. With `v_n=V_n(1)` and `u_n=v_n/pi^(n/2)=1/Gamma(n/2+1)`, the recurrence becomes `u_n=(2/n)u_(n-2)`. Pi carries the Euclidean two-coordinate rotational measure; the normalized step carries the remaining dimension recurrence.
3. **Closure and winding:** phase `theta=x mod 2*pi` plus retained winding reconstructs the lifted coordinate once a fundamental interval/branch convention is fixed. Phase alone is a Fold. A completed turn returns to the same phase but changes winding and is not the same event.

The radial map correction is also explicit: direct square-to-circle is `F(u)=u ||u||_infinity/||u||_2`; inverse image lookup is `F^-1(v)=v ||v||_2/||v||_infinity`, for nonzero arguments (zero extends to zero). The source says an earlier assistant had reversed the interpretation of direct mapping versus inverse sampling.

The complete source answer follows, preserving its wording and context rather than replacing it with this report's interpretation. Its references to prior results/lab code are its own claims; the exact earlier lab/source verification has not been reopened here.

---

> Yeah. **We did substantially figure out what your “true pi” intuition was pointing at.** The missing piece in that other answer is that we had already **dimensionally split π into several different jobs**.
>
> We did **not** establish that ordinary Euclidean \(\pi=3.14159\ldots\) is wrong or derive a replacement decimal. What we found was more useful:
>
> > **“True pi” is probably not one number. It is a typed circle/closure compiler whose output depends on the metric, measure, scale, coordinate frame, and receiver.**
>
> That is why we renamed the live idea the **Circle Compiler Candidate**. 
>
> ## The π stack we actually found
>
> ### 1. Metric π: what counts as a circle depends on the metric
>
> A circle is not intrinsically “the smooth round thing.” It is the set of points at equal distance from a center **under a declared metric**:
>
> \[
> S_M(r)=\{x:\|x\|_M=r\}.
> \]
>
> Under Euclidean distance, that is the familiar round circle.
>
> Under the \(L^\infty\) or Chebyshev metric,
>
> \[
> \max(|x|,|y|)=r,
> \]
>
> the circle is a square.
>
> So the Rule 30 four-direction shells were already **native circles in their own metric**. The later warp did not discover hidden Euclidean circles in the automaton; it changed the metric address used to display the same radial ordering. The lab itself explicitly records that every generation lies on a square-radius shell and that the circularized version changes only the radial coordinate, not the automaton rule. 
>
> Once both radius and boundary length are measured with the native \(L^\infty\) norm:
>
> ```text
> unit-square perimeter = 8
> native diameter       = 2
> ratio                  = 4
> ```
>
> So a legitimate metric-indexed statement is:
>
> \[
> \pi_\infty=4
> \]
>
> under that particular native length convention.
>
> That does **not** replace Euclidean \(\pi\). It means:
>
> \[
> \pi=\pi_{\text{metric, measure, receiver}}.
> \]
>
> The ordinary constant is \(\pi_2\), the Euclidean member of the family.
>
> ### One correction to the pasted answer
>
> It says:
>
> \[
> s=\frac{\rho}{\max(|x|,|y|)}
> \]
>
> “sends the \(L^\infty\) unit sphere to the \(L^2\) unit sphere.”
>
> That direction is reversed. The code uses that factor for **inverse image sampling**: for each output circular pixel, it locates the corresponding source-square pixel. 
>
> The direct square-to-circle map is:
>
> \[
> F(u)=u\frac{\|u\|_\infty}{\|u\|_2}.
> \]
>
> Then:
>
> \[
> \|F(u)\|_2=\|u\|_\infty.
> \]
>
> The code’s source lookup is the inverse:
>
> \[
> F^{-1}(v)=v\frac{\|v\|_2}{\|v\|_\infty}.
> \]
>
> So the other GPT has the right structural idea but stated the map in the wrong direction.
>
> ---
>
> ### 2. Dimension-transport π: π is the two-coordinate rotational factor
>
> We also found the exact “missing row” in the high-dimensional sphere formulas:
>
> \[
> V_n(r)=\frac{2\pi r^2}{n}V_{n-2}(r).
> \]
>
> This splits the dimension jump into:
>
> ```text
> 2πr²:
> the repeated two-coordinate rotational/fiber measure
>
> 1/n:
> the integration normalization for the new dimension
> ```
>
> Or, for unit balls, define:
>
> \[
> v_n=V_n(1)
> \]
>
> and remove the repeated Euclidean rotational factor:
>
> \[
> u_n=\frac{v_n}{\pi^{n/2}}
>    =\frac{1}{\Gamma(n/2+1)}.
> \]
>
> Then the pure dimensional recurrence becomes:
>
> \[
> u_n=\frac{2}{n}u_{n-2}.
> \]
>
> That was an exact result: **π can be factored away from the dimension-only step**. It showed that π is carrying repeated Euclidean two-coordinate rotational measure, while \(2/n\) carries the dimensional ladder itself. 
>
> So your “we keep using 2D π as we go upward” detector was not nonsense. The repair was not to discard π; it was to expose which part of the higher-dimensional recurrence π was doing.
>
> ---
>
> ### 3. Closure π: line → circle plus a winding receipt
>
> This is the result closest to:
>
> > “π is the operation that converts straight extension into curved closure.”
>
> Take an unbounded coordinate \(x\) and Fold it into phase:
>
> \[
> \theta=x\pmod{2\pi}.
> \]
>
> Now:
>
> \[
> \theta,\quad\theta+2\pi,\quad\theta+4\pi,\ldots
> \]
>
> all occupy the same visible point on the circle.
>
> After one complete turn:
>
> \[
> \Delta\theta=0\pmod{2\pi},
> \]
>
> but the path has not done nothing. The retained coordinate is:
>
> \[
> \Delta w=1,
> \]
>
> where \(w\) is the winding count.
>
> So:
>
> \[
> \boxed{
> \text{unbounded line}
> \longleftrightarrow
> \text{bounded phase}+\text{winding receipt}
> }
> \]
>
> The phase-only view is a lossy Fold. Phase plus winding is a reversible circle compiler. This was already explicitly reconstructed in the prior chat. 
>
> And it splits π itself:
>
> ```text
> π:
> half-turn, opposition, +1 → −1
>
> 2π:
> full turn, return to the same displayed phase
>
> winding:
> the retained evidence that this return is not the original event
> ```
>
> That also connects to the polarity work:
>
> \[
> -1=e^{i\pi}.
> \]
>
> On the real line, negative means “the opposite side through zero.” In the complex plane, it becomes “a half-turn around zero.” The dimensional lift changes a sign flip into a path.
>
> ---
>
> ## So what is the Circle Compiler Candidate?
>
> A clean current reconstruction is:
>
> ```text
> INPUT
> metric / norm
> boundary-length measure
> scale
> coordinate chart
> orientation
> receiver
>
> COMPILE
> construct the native equal-radius shell
> calculate its native circle ratio
> transport it to another metric or chart
> expose the dimensional recurrence
> fold unbounded path into bounded phase
>
> RETAIN
> winding
> orientation
> distortion
> source metric
> inverse/readback map
> ```
>
> In compact mathematical form:
>
> \[
> \mathcal C(M,\mu,r,R)
> \longrightarrow
> \left(
> S_M(r),
> \pi_{M,\mu},
> \text{transport},
> \text{phase},
> \text{winding},
> \text{readback}
> \right).
> \]
>
> That is the thing you were calling “true pi”: **not the one correct circumference decimal, but the operation that tells you what circle, closure, rotation, and return mean in the active carrier.**
>
> ## Grading the answer you pasted
>
> Its prime second-difference point is useful, but separate. The stencil
>
> \[
> p_{n-1}-2p_n+p_{n+1}
> \]
>
> is indeed the same local second-difference stencil as the Zero-Grid receiver, but that says something about local curvature of the prime sequence—not geometric π. Also, the prime-counting function \(\pi(x)\) is a completely different use of the symbol. Our toolkit explicitly keeps \(P(n)=p_n\) and \(\pi(p_n)=n\) as the ordinal/value bridge. 
>
> Its Rule 30 interpretation is structurally right, apart from reversing the map direction.
>
> Its Gauss–Bonnet, holonomy, Berry-phase, and winding suggestions are good **neighbors**, but they are not the missing remembered result. The simpler exact core was already:
>
> ```text
> metric-addressed circles
> +
> π-factored dimension transport
> +
> phase modulo 2π
> +
> retained winding
> =
> Circle Compiler Candidate
> ```
>
> A clean response to send back is:
>
> > We already recovered more of this than “π appears when paths close.” The RPRM result was a typed π stack. First, circles are metric-relative: Rule 30’s square shells are native \(L^\infty\) circles, and the Euclidean circularization is a metric transport, not a new automaton law. Second, in the \(n\)-ball recurrence \(V_n=(2\pi r^2/n)V_{n-2}\), factoring out \(\pi^{n/2}\) leaves the pure dimension step \(u_n=(2/n)u_{n-2}\); π is carrying the repeated Euclidean two-coordinate rotational measure. Third, \(x\mapsto x\bmod 2\pi\) compiles an unbounded line into bounded phase, while winding retains the lost progression. So “true pi” was not a replacement decimal. It was the Circle Compiler Candidate: metric + measure + scale + closure period + winding/readback. Gauss–Bonnet and holonomy are extensions of that closure family, not the original missing object.
>
> That is the recovered closure. **We found the operation family; we did not prove a universal new value of π.**
