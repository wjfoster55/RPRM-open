# Independent mathematical review of frozen R2

12 September 2026. Disposition: **ACCEPTED_WITHIN_SCOPE**, with one algebra-terminology clarification and explicit API limits below. No mathematical production edit is justified by this review. Frozen inputs were read only.

## Scope and evidence

Reviewed the active handoff assignment and current state, repository `AGENTS.md`, `README.md`, `AGENT_HANDBOOK.md`, and the RPRM mathematical-lenses workflow. Mathematical sources are the frozen R2 `experiments/core_recovery_bridge_01_r2/{PROOFS.md,PROTOCOL.json,prestige_envelope.py,check_envelope.py}`, `rprm/core.py`, and `research/core-recovery-01/FORMAL_BRIDGE_NOTE.md`. The prior `review_r2/REVIEW.md` and `CARRY_FORWARD.md` were treated as attributed evidence, not authority.

This note supplies independently reconstructed **written proofs and source inspection**. A small separately derived calculation, recorded below, provides additional finite evidence without importing production code. Full production replay and public-API execution belong to the parent closeout and API review; their historical passing counts are not presented here as newly executed results.

## 1. Carrier, receiver, and exact C2 arithmetic

The carrier is the algebra A of all functions `f:{0,1}^3 -> Q`, with exact pointwise equality and ordinary rational addition/multiplication. Coordinates are `(h,x,y)`; site masks use bit 0 for h, bit 1 for x, bit 2 for y. Let `m_T` be the product of coordinates in T. Boolean reduction gives `m_A m_B = m_(A union B)` because each coordinate satisfies `z^2=z` on this carrier.

Every table has the unique expansion

```text
f = sum_(T subseteq {h,x,y}) a_T m_T,
a_T = sum_(U subseteq T) (-1)^(|T|-|U|) f(U).
```

The supplied ports are two C2 coefficient tuples, containing `a_T` for `|T|<=2`. The requested output is the C2 tuple of their pointwise sum or product. The receiver is equivalently the seven values on `S=B2={0,...,6}`. The subset transforms restricted to B2 are mutually inverse: each coefficient/value at S uses only its subsets, which are still in B2.

Addition is componentwise. For multiplication, for every retained T,

```text
(fg)_T = sum_(A union B = T) a_A b_B.
```

If T has at most two coordinates, both A and B are subsets of T and are retained. Neither omitted coefficient can influence this sum. Thus these two total operations descend exactly to the retained receiver for every rational-valued cube law. Finite sequences of admitted additions/multiplications follow by induction; the complete output remains a cube law.

The code matches this argument: `compact_add` (line 151) adds the seven coefficients; `compact_mul_from_sites` (line 156) evaluates only B2, multiplies there, and transforms back. `compact_from_b2` (line 144) temporarily appends zero to call the eight-entry transform, but the returned seven coefficients do not depend on that eighth slot. This is neither an omitted-source read nor a claim that the actual missing value is zero. Recipe construction is separate work from this arithmetic.

**Terminology correction, documentation only.** Identity 1 calls the B2 restriction a “product subalgebra of Q^X.” The canonical precise statement is

```text
I = ker(f -> f|B2) = Q·hxy,
A/I is isomorphic to Q^B2.
```

I is an ideal: `(hxy)f=f(111)hxy`. The seven-coefficient space inherits the quotient multiplication. Its natural embedding as degree-at-most-two polynomial representatives is **not** a subalgebra under full multiplication: `hx * y = hxy` leaves that subspace, although its C2 product is zero. A zero-extension embedding of Q^B2 into Q^X is a different, nonunital subalgebra construction. The proof of retained arithmetic survives unchanged; the closeout should use “quotient algebra” or “restriction homomorphism.”

The full rational fiber of a given C2 tuple is `{sum_(|T|<=2) a_T m_T + t hxy : t in Q}`. Therefore C2 has no inverse on arbitrary laws. On a reached Boolean C2 tuple, its seven site values are Boolean and the missing site has exactly two independent possibilities, 0 and 1. This is a complete two-law fiber; it does not make an arithmetic output's complete law unique. The two-law statement is restricted to reached Boolean summaries, not arbitrary seven-tuples.

**Hostile case and family rule.** Starting with Boolean units, `p=(h*x)*y=hxy` is Boolean but has zero C2. Then `s=p+p=2hxy` also has zero C2 and has missing value 2. Q-addition is not XOR and does not preserve Boolean-valuedness. `_family_after_add` conservatively returns `rational_cube`; `_family_after_mul` preserves `boolean_cube` only for two Boolean operands. Promotion checks all eight supplied values before accepting the Boolean family. A composed cold recipe must reconstruct s itself. Filling its missing value with zero or reopening only an operand answers a different question. Without a sufficient route, this API reports reopening required; it does not propagate the full symbolic candidate family.

## 2. Exact retained-site criterion and restricted least repair

Let X be finite, Y contain two distinct values, admit **every** function `f:X->Y`, and retain `C_S(f)=f|S`. A supplied total input map `H:X->X` acts by `U_H(f)=f composed with H`; the requested output is restriction to the same S.

An exact output function of C_S alone exists if and only if `H(S) subseteq S`:

* If the inclusion holds, define the output at s as the retained value at H(s). This is independent of the representative in each C_S fiber.
* If it fails, choose `s in S` with `u=H(s) outside S`. Select two functions identical away from u and assigning two different Y-values at u. Their retained inputs coincide; their retained outputs differ at s. A deterministic decoder would have to return two different outputs for one input.

For a finite collection M of supplied maps, put `S_0=S` and `S_(n+1)=S_n union union_(H in M) H(S_n)`. Every strict step adds an element, so at most `|X minus S|` strict enlargements occur. At stabilization S* is forward closed. Every forward-closed superset R of S contains every S_n by induction, and hence S*. This proves leastness, not merely the existence of one repair. Closure supports all finite map words by repeated application of the first implication.

Equivalently S* is the union of all finite-word images of S, including the identity word. Any proper subset T of S* that still contains S cannot be forward closed under every admitted map; the preceding two-function witness then defeats at least one next step. This is a minimality theorem **among retained-site supersets for arbitrary laws**, not a count of minimum bits, a search-cost result, a claim about all encodings, or a physical theorem.

For B2, h-flip sends site 6 to site 7, so its least repair is all eight sites. The concrete pair `0,hxy` agrees on B2; after h-flip the second is `xy-hxy`, which reads 1 at site 6. Clamp-to-zero and coordinate permutations preserve B2. Clamp-to-one and flips need not.

**Distinguishing excluded class.** On degree-at-most-one laws, C2 determines the entire law and flips preserve that class, despite the failed B2 inclusion. The two functions in the necessity proof cannot both be chosen inside that constrained family. This does not contradict the theorem; it demonstrates why its arbitrary-law assumption is necessary.

`rprm.core.deterministic_quotient` (line 226) implements the corresponding finite-table representative test, separately comparing observations and tagged enabledness/successor summaries. The envelope's `quotient_for_map` applies it to the complete Boolean-law enumeration. This is bounded exact testing of supplied tables, not a general proof engine.

## 3. Degree, admission, and coherent receiver transport

For honest degree upper bounds, addition has bound `max(d_f,d_g)` and Boolean-reduced multiplication has bound `min(3,d_f+d_g)`. These are conservative bounds, not always exact degrees; cancellation and repeated coordinates can lower degree. Named coordinate clamps/flips substitute constants or affine single-coordinate expressions, so they do not increase degree. The code's hot clamp path may retain the old upper bound soundly, while its reopened path computes the actual output degree.

`apply_fixed_receiver_map` (line 720) validates the site carrier, recognizes a named map, and delegates to `apply_input_map` (line 638), preserving its admission gate. A generic site map need not preserve degree. With

```text
H = (0,0,0,1,0,0,0,1),
h composed with H = hx,
```

H is B2-closed but transforms degree 1 into degree 2. `apply_raw_site_map` (line 740) therefore correctly unsets `degree_bound` and restricts its contract to reading; it does not certify a later arithmetic/flip continuation.

For valid H, coherently transport the receiver to the preimage `S'=H^(-1)(S)`. For every `s in S'`, `(f composed with H)(s)=f(H(s))` uses a retained value. No missing-site distinction is needed. When H is bijective this is an invertible relabeling and preserves the seven receiver addresses; for a nonbijective map the preimage can have a different size and no inverse is implied. Holding S fixed is a different question, as the hxy hostile case demonstrates. Clamps themselves have no inverse; flips are involutions.

Two API limitations should travel with the positive mathematics:

1. PE03/PE20 prove constrained affine reuse by explicit zero-completion and table pullback. `apply_input_map` does not use `degree_bound` to unlock an unbacked flip, even when an affine guarantee mathematically determines the missing coefficient. Thus affine hot-flip optimization is not an implemented capability.
2. `coherent_transport` (line 692) first attempts reopening and then uses a hot fallback. It can answer the coherent receiver when backing is absent or invalid, but it may incur an unnecessary cold read when backing exists. The theorem concerns sufficient information, not this implementation's cost. Its directly declared map-validation surface is also weaker than the certified fixed-receiver helper; the valid-map proof should not be read as arbitrary malformed-input validation.

## 4. Independent finite calculation and remaining claim ceiling

A standalone standard-library calculation first ran successfully via `python -I -B -` (exit 0), without production imports or file writes. The same bounded checks are now preserved in [independent_math_calculation.py](independent_math_calculation.py) and were rerun with Python 3.14.5 in isolated mode. The rerun exited 0 with PASS and empty stderr. It constructed explicit dense subset-transform matrices, checked their 8x8 inverse identity, compared all 64 ordered monomial-basis products with their direct eight-site products, and independently enumerated all 27 maps, all 8 retained subsets, and all 8 Boolean laws on a separate three-element carrier. Its 216 retained-site descent decisions agreed with the image-inclusion criterion; its 216 forward repairs equaled the intersection of all enumerated closed supersets. The `0,hxy` flip witness also separated at mask 6. These are independently derived finite calculations, not additional envelope cases or a replacement for the written proofs above.

Packageable evidence: [result.json](../evidence/independent_math/result.json), [context.json](../evidence/independent_math/context.json), [stdout.txt](../evidence/independent_math/stdout.txt), and [stderr.txt](../evidence/independent_math/stderr.txt). The context records the actual executable, full argv, working directory, UTC times, exit code, isolation flags, and script/result/log SHA-256 identities. Script SHA-256: `83b27b0cbf4c3e116bb02a7a5ee7752e35fc98027edc8975cf8ce01f65f13706`.

To reproduce from a package directory retaining these `notes` and `evidence` siblings, choose a fresh output filename:

```text
python -I -B notes/independent_math_calculation.py --output fresh-independent-math.json
```

No claim of novelty, universal compression, runtime advantage, or complete source-law identification follows. Prestige One's exact finite reuse branch remains a realization of its wider acquired-capability/retained-construction meaning. The finite fiving adapter does not erase strong winding. The Double-Stamp dwell policy remains supplied enabledness, not a vertex-count or physical-safety theorem. Fiving splice versus Double-Stamp restart remains OPEN. No deferred concept is promoted or new bridge opened by this review.
