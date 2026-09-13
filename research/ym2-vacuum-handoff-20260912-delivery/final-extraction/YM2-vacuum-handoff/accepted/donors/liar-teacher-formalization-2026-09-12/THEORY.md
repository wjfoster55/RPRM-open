# Seven/eight teacher transfer: exact models and written proofs

Research note, 12 September 2026. Evidence grades: **definitions, written proofs, derived synthesis, and separately reported finite tests**. These are not Lean-checked proofs or additions to the published theorem counts. [PANEL-RESULTS.json](PANEL-RESULTS.json) and [SAT-RESULTS.json](SAT-RESULTS.json) record the executable checks; the scripts do not import the historical experiment's implementation.

The exact result is a lawful growth/replacement/reference-transfer construction for specified binary carriers. Its seven-answer code is dual to Hamming-7. This realizes several recovered proposals while preserving the distinction between transformation roles, observation functions, source states and receiving ports.

Historical anchors are [RECOVERY.md](../liar-teacher-recovery-2026-09-12/RECOVERY.md), especially its links to amendments 0.28 (movable vacant student and retained handoff) and 0.29 (Boolean cube and movable anchor), and [SELECTED-PASSAGES.md](../liar-teacher-recovery-2026-09-12/SELECTED-PASSAGES.md), P08–P10 (retain three, add four, reduce, replace and recalibrate). The existing [boundary-syndrome note](C:/github/RPRMResearch/RPRM_LIAR_TEACHER_BOUNDARY_SYNDROME_01/NOTE.md) supplies the calibrated-view and Hamming interpretations. The results below implement specified parts of that proposal; they do not identify every historical meaning with one model.

## 1. Receiver and handoff contract

Fix a finite, completely supplied source carrier X, exact equality, deterministic calibrated views g_i:X→Y_i, and requested observation Q:X→B. A panel I returns C_I(x)=(g_i(x))_{i∈I}. Given outputs y, its complete joint fiber is F_I(y)={x∈X:C_I(x)=y}; report NONE, ONE or MANY only after complete coverage. Unknown map laws or unfinished search are OPEN. Equal outputs do not merge occurrence identities unless explicitly allowed.

**P1 — Exact teacher panel.** A decoder h:C_I(X)→B satisfying Q=h∘C_I exists iff Q is constant on every panel fiber. Proof: a decoder forces constancy; conversely define h(y)=Q(x) for any x in the nonempty fiber. Constancy makes this definition independent of the choice. Full source recovery is the special case Q=id_X, hence exactly injectivity.

**P2 — Calibrated expansion and replacement.** Adding known views can only shrink each compatible source fiber. Replacing I by J preserves Q iff the P1 condition holds for J. Preserving all old panel answers additionally requires C_I to factor through C_J. Neither teacher count nor agreement proves these obligations.

For a candidate newcomer in a finite map family G, observations leave the version space G_D={g∈G:g matches every supplied labeled example}. Its law on a needed domain D* is uniquely calibrated iff this nonempty family agrees pointwise on D*. Exhaustive labeled coverage of X suffices for unrestricted deterministic maps. If any x remains unobserved and two output values are admitted, two unrestricted maps can agree on every observed point and differ at x; global calibration then fails. A separating old panel can decode each supplied x, but cannot invent an unobserved newcomer's output. A compositional law proved from calibrated maps is another valid calibration route.

**P3 — Operational student handoff.** Let T_a be supplied deterministic partial updates. A retained student state C(x) supports exact quotient updates, their enabledness and Q iff, whenever C(x)=C(x′):

1. Q(x)=Q(x′);
2. T_a is enabled at both or neither;
3. if enabled, C(T_a(x))=C(T_a(x′)).

Necessity follows because one summary cannot have two answers, domains or successors. Sufficiency defines each quotient operation using any representative; the conditions make it well-defined. Induction on an action word preserves execution and observations. This is an iff for updating the chosen summary, stronger than merely answering all future questions.

For a four-port relation R⊆∏_{p∈P}X_p and movable vacancy v, the teachers supply P\{v}; the student receives the complete compatible v-fiber. A ONE completion fills v. Rotating v changes the aperture, not the law. Folding to the filled value preserves only receivers satisfying P1/P3. Reconstructing teacher occurrences requires retained information that separates them or a complete reopenable preimage; a unique student value alone need not do so.

Hostile example: X=F₂², C(x₁,x₂)=x₁, Q=C, and T swaps coordinates. States 00 and 01 share the retained answer but have different successor summaries. A present-only student fails the update contract.

## 2. Three teachers, four newcomers, seven available checks

For each fixed finite k≥1, take V=F₂^k with XOR addition and a retained coordinate frame. For u∈V define the bit check ℓ_u(x)=u·x mod 2 and the equivalent sign character χ_u(x)=(-1)^{ℓ_u(x)}. Source vectors and dual checks are different types; coordinates identify their labels here.

**P4 — Rank determines the complete fiber.** A panel of checks with row matrix A has fibers either empty or affine translates x₀+ker A. If rank A=r, every nonempty fiber has 2^{k-r} states. Thus it separates V iff r=k. Proof: Ax=Ax₀ iff A(x−x₀)=0; a kernel basis gives exactly 2^{k-r} choices.

**P5 — Exact seven-to-three rule.** For k=3, there are seven nonzero checks. A triple of distinct checks separates all eight states iff its labels are linearly independent. There are 7·6·4=168 ordered bases, hence **28 of the 35 unordered triples** separate. The other seven are precisely {a,b,a+b}: each distinct pair determines one such triple, and each triple contains three pairs, yielding 21/3=7. Every distinct panel of at least four checks separates, since a proper subspace contains at most three nonzero vectors.

Start from a calibrated basis a,b,c. Retain its three checks and derive the four newcomers a+b, a+c, b+c, a+b+c through XOR of bit answers, equivalently multiplication of sign characters. This establishes all seven maps without four independent raw calibrations. These derived views add no source information beyond the basis; they provide alternative panels and consistency constraints.

**P6 — Anchored replacement.** Holding two distinct checks a,b fixed, the admissible third checks are exactly the four vectors outside span{a,b}. If c is one, its other three valid replacements are c+a, c+b, c+a+b. The newcomer a+b fails: its answer is determined by the anchored pair. Thus “any of seven” can mean selecting a suitable panel from seven; it cannot mean every triple suffices on this carrier. Hostile triple {100,010,110} gives identical answers for 000 and 001.

At k=2 the three nonzero checks have the stronger property that **every distinct pair** separates all four states. This property changes at k=3; carrying it upward unchanged is invalid.

**P7 — Moving the anchor.** For absolute state x and old/new anchors a,b, t_a=x+a and t_b=x+b satisfy t_b=t_a+(a+b). This bijection is self-inverse, with χ_u(t_b)=χ_u(t_a)χ_u(a+b). Transporting frame and anchor therefore preserves every source question and transported operation. Forgetting the anchor leaves eight possible absolute states for a given three-bit relative address. An occupied anchor, a vacant receiving role and an extra silent ninth position are distinct contracts.

## 3. What four/eight and Hamming seven/eight share

**P8 — Question capacity.** A deterministic depth-d binary interrogation has at most 2^d answer leaves, even when adaptive. Identifying all four/eight unrestricted states requires at least two/three such answers. Known calibration alone does not reduce this bound. A previous-instance result or other source-dependent memory can restrict the current live fiber; the bound then applies to its remaining distinguishable requested answers. One question returning a four-valued structured payload has a different alphabet from one binary question.

**P9 — Hamming check geometry.** Let H have the seven nonzero vectors of F₂³ as columns, labeled by seven error positions, and let C=ker H⊆F₂⁷. For y=c+e with c∈C, syndrome Hy=He. Under weight(e)≤1, syndrome zero names no error and each nonzero column names exactly one error. For distinct column labels a,b, two errors have syndrome a+b, identical to a third single error. A single-error correction then creates the nonzero lawful weight-three error supported on {a,b,a+b}.

Appending one bit enforcing total even parity gives an eight-position code. The combined three-bit syndrome and total parity distinguish all eight single-error positions from no error. Every double error has even total parity and a nonzero three-bit syndrome, so is detected under an at-most-two-error promise, but cannot be uniquely located: label the new parity position 0; for each nonzero s the pairs {a,a+s} partition the eight positions into four pairs, all producing (syndrome,parity)=(s,0).

The seven dependent character triples of P5 are exactly the seven triples of labels producing Hamming weight-three codewords. This is a precise adapter through the declared binary linear structure. Nevertheless, cube vertices, dual checks and error positions remain different typed uses. Adding a free binary coordinate doubles a signal carrier from four to eight states. Adding an overall parity coordinate preserves the sixteen Hamming codewords and adds redundancy; it does not double message freedom.

**P9a — The seven-response code is the Hamming dual.** Keep exactly the column ordering of H from P9 and encode a source x∈F₂³ by E(x)=(ℓ_u(x))_{u≠0}=Hᵀx. Its image S⊆F₂⁷ is the row space of H, expressed as column words. For every z∈F₂⁷,

```text
z∈S⊥ ⇔ (Hᵀx)·z=0 for every x∈F₂³
      ⇔ x·(Hz)=0 for every x∈F₂³
      ⇔ Hz=0 ⇔ z∈C.
```

The coordinate dot product is nondegenerate, so taking orthogonal complements gives **S=C⊥**. H has rank three because it includes the three standard-basis columns; consequently E is injective, |S|=8 and |C|=2⁴=16. For x≠0, the nonzero functional u↦u·x takes value one on four of the eight vectors u∈F₂³. None is u=0, so E(x) has weight four. Differences of distinct response words are nonzero response words; S therefore has minimum distance four. This is the binary [7,3,4] simplex code, dual to the [7,4,3] Hamming code. The minimum distance three of C follows because H has no zero/repeated columns (excluding weights one/two), while {a,b,a+b} supplies weight three. The bridge is the displayed orthogonality equation; matching seven-coordinate counts alone would not establish it.

**P9b — Primal quartet replacement.** Now a,b,c denote source vectors, not check functions. Let a,b be independent in V=F₂³ and U=span{a,b}={0,a,b,a+b}. For any c, the coset c+U is disjoint from U iff c∉U: an intersection would express c as the sum of two elements of U; when c∈U the coset equals U. Thus choosing c outside U creates the disjoint four newcomers {c,a+c,b+c,a+b+c} and expands the four-state source enclosure to all eight states.

The new quartet W=span{a,c}={0,a,c,a+c} then satisfies U∩W={0,a}. Indeed, an element αa+βc in U cannot have β=1, since that would force c∈U. Reduction from U to W therefore retains the two source roles 0,a and replaces b,a+b with c,a+c. It does **not** retain two dual checks as P6 does. If c∈U\{0,a}, W=U and no new quartet is obtained; if c∈{0,a}, W has only two elements. These hostile cases show why independence must be checked.

This source expansion adds a genuinely free coordinate and doubles four states to eight. Hamming parity extension instead appends the determined bit p=∑ᵢzᵢ to each z∈C. That map is bijective onto its image and retains sixteen messages; it adds error-detection redundancy rather than a free source coordinate. The eight simplex response words in P9a are a third count, with their own encoding domain.

**P9c — Which XOR negations preserve an affine answer.** Fix finite A∈F₂^{m×n}, b∈F₂^m, and the exact predicate f_b(x)=[Ax=b] on all x∈F₂^n. If Ax=b is consistent, the masks t satisfying f_b(x+t)=f_b(x) for every x are **exactly ker A**. Sufficiency follows from A(x+t)=Ax+At. For necessity choose a solution x₀: invariance requires A(x₀+t)=b, hence At=0. If the solution set is empty, f_b is constant false and **every mask** preserves it. Consistency is therefore essential to the claimed kernel characterization.

For an arbitrary mask, substitute x=y+t. The transported equation is

```text
Ax=b ⇔ Ay=b+At,
```

and a requested source readout Q must become Q_t(y)=Q(y+t). Thus a non-kernel negation can preserve the represented problem through transported coordinates and right-hand side; merely changing the candidate bits while leaving the fixed predicate untouched generally fails. For any Boolean formula F, the same bijection yields SAT(F)=SAT(y↦F(y+t)), while witnesses translate by t. Preserving this final satisfiability bit through substitution does not compute it or find a witness. These distinguish a fixed-instance symmetry, a transported representation and a final decision readout when interpreting “negations don't negate the end.”

## 4. Exact affine messages and the next non-affine obstruction

**P10 — Projection and join retain the full affine boundary relation.** Let B be a finite set of shared Boolean variables and Z₁,Z₂ disjoint finite private sets, also disjoint from B. Each supplied block has equations

```text
A_i z_i + D_i b = e_i over F₂.
R_i = {b : there exists z_i with A_i z_i + D_i b = e_i}.
```

Row operations preserve each block's full solution set. Eliminate all private columns first. The remaining equations with no private coefficient are necessary boundary constraints. They are also sufficient: choose free private variables arbitrarily and solve each private pivot variable from its pivot row, since private elimination has removed that pivot from the other rows. Inconsistency is retained as `0=1`. Thus R_i is exactly an affine boundary relation or the empty relation, with no witness guessed or lost in the satisfiability readout.

The original conjunction is satisfiable iff `R₁ ∩ R₂` is nonempty. Necessity follows by restriction of a joint solution. For sufficiency take one b in both relations and choose its private completions z₁,z₂. Their disjoint scopes permit combination. If private coordinates overlap outside B, this implication can fail: two blocks requiring a shared omitted variable to be zero and one each have a nonempty empty-boundary projection, while their conjunction has no solution. The pilot rejects that malformed partition. For a fixed admitted b, the full original preimage is the product of the two private completion fibers. A decision or boundary row does not retain a particular private witness.

An independent system on |B| boundary coordinates needs at most |B| nonzero rows (or the single contradiction row). Store dense coordinates plus the source-ID mapping. For an explicit input matrix with m rows and n distinct variables, elementary elimination uses polynomially many coefficient and row operations on O(n+1)-bit augmented rows; a coarse O(m (n+1) (m+n+1)) bit-operation bound suffices, including zero-variable contradiction checks. Projection and join therefore have polynomial cost for this explicitly supplied affine representation. Arbitrarily large literal IDs must first be compressed to dense coordinates; integer masks indexed by uncompressed IDs do not inherit that bound.

The pilot's raw-CNF recognition has a separate contract. Group normalized clauses by identical support of size k≥1. A normalized non-tautological full-support clause excludes exactly one assignment. Exactly 2^(k−1) distinct excluded assignments of one parity are the entire forbidden parity class, so the group equals the opposite XOR equation. An empty clause is a direct contradiction outside this counting argument; this pilot keeps it as a residual. Recognizing that supplied group requires reading and checking its clauses; merely knowing that an affine equation would be compact does not supply the recognition. Unsupported residual groups produce UNRECOGNIZED, even if a stronger recognizer could discover an equivalent affine relation.

**P11 — Affine closure has an exact non-affine failure and an exact but potentially large repair.** An affine relation is closed under triple XOR: if x,y,z belong to x₀+K, then x+y+z does too. The OR3 relation contains 100,010,110 but excludes their triple XOR 000. The exactly-one relation contains 100,010,001 and excludes their triple XOR 111. Therefore neither relation is affine. Their affine hulls admit these missing assignments and can introduce false solutions when joined with a block demanding one of them. Both hostile joins are checked in the pilot.

A positive k-literal disjunction has an exact disjoint cover by k affine pieces: first bit 1; first bit 0 and second 1; continuing through the piece with its first k−1 bits 0 and last bit 1. Signed literals use the corresponding complemented coordinates. A union of r affine pieces remains an exact union after existential projection; conjunction with a union of s pieces is the union of at most r·s pairwise affine intersections. Each individual piece is tractable by P10. Repeated conjunction can nevertheless grow the number of pieces multiplicatively, and projections may overlap them. This is a valid exact extension of the message language, **not a polynomial bound on its size**. Affine hull replacement avoids that growth by weakening the relation, which fails the hostile controls.

Consequently the next substantive question is how to retain the non-affine residual or an exact shared representation of these pieces economically, including the work needed to select, construct and operate on it. A conventional CNF/XOR solver should receive the same algebraic capability in any comparison. [SAT-PILOT.md](SAT-PILOT.md) gives the frozen implementation contract and results.

## 5. Computational claim ceiling

These proofs give exact receiver selection, compositional calibration, transport and error-model boundaries. They supply no general fast algorithm for constructing a separating panel, computing its answers, learning arbitrary maps or solving SAT. A useful amortized accounting is calibration cost plus N times per-instance observation, update and decoding costs; source reopening and failures belong in that accounting. A constant-size answer can still be expensive to compute. A P=NP argument would require a uniform polynomial-time algorithm for an NP-complete problem, including constructing and evaluating these representations. That obligation remains OPEN here.

## Finite verification and provenance

[verify_panels.py](verify_panels.py) enumerates the three-bit carrier and codewords afresh, with a separate rank calculation and error-syndrome calculation. Some assertions reuse the same readout function; their count is not a count of independent proofs. The bounded suite covers:

- Enumerate all 35 distinct character triples: 28 fiber patterns of eight singletons; seven patterns of four pairs. Count 168 ordered bases and seven dependent triples.
- For every ordered independent pair, count four separating third labels; for every ordered basis, test the three replacement identities and failure of a+b.
- Enumerate every panel of size 4–7 and check injectivity; verify all three distinct pairs at k=2.
- For all anchors a,b and sources x, verify P7 and character transport; erase the anchor and recover the complete eight-element absolute fiber.
- Enumerate Hamming-7 codewords and errors of weight at most two; verify 16 codewords, unique promised single-error decoding and every double-error alias.
- Enumerate the extended code and all 28 double-error pairs; verify seven nonzero syndromes with four pairs each, all detected but ambiguous.
- Verify the 00/01 coordinate-swap hostile handoff; independently check a partial-update example with equal present output but unequal enabledness.
- Test source-quartet expansion both outside and inside the old span, including the degenerate two-role cases; test extended-code single-error locations including the parity bit.
- Enumerate all 256 three-bit Boolean predicates for translation-stabilizer closure. Test the kernel/empty distinction and transported equations for every distinct nonzero three-row system and its right-hand sides, plus zero-row, rank-zero/one and repeated-row fixtures.

The [raw-CNF pilot](SAT-PILOT.md) separately validates P10's implementation on its declared finite scopes. P11's union-of-affine construction is a written argument; no general mixed-SAT benchmark or complexity theorem was tested here.

Primary mathematical context: Hamming's [original 1950 paper](https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1950.tb00463.x) establishes the coding-theory setting. Affine Boolean satisfiability is an established tractable class in [Schaefer's 1978 paper](https://www.khoury.northeastern.edu/home/lieber/courses/csg260/f06/materials/papers/max-sat/p216-schaefer.pdf). SAT solvers combining clause reasoning with parity reasoning are developed in [Laitinen, Junttila and Niemelä (2012)](https://arxiv.org/abs/1207.0988). The displayed proofs supply the specific adapters used here; none of these sources establishes novelty or a general speed advantage for this recovered construction.
