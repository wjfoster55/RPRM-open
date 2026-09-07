# Assessment C: scored mathematical response

## 1. Addition on two carriers

On `Z/6Z`, all ports are residue classes, written with representatives `0,...,5`, and addition and equality are modulo 6. With `z=2`, the complete ordered-pair fiber is

`MANY({(0,2), (1,1), (2,0), (3,5), (4,4), (5,3)})`.

For each of the six possible `x`, exactly one `y=2-x mod 6` works. This establishes both correctness and coverage.

On the integer carrier `{0,1,2}`, with ordinary addition and all three ports restricted to that carrier, the complete fiber is

`MANY({(0,2), (1,1), (2,0)})`.

Here `y=2-x` exhausts the three admitted choices of `x`. The contracts differ in carrier, equality, and addition law: for example, `(3,5,2)` is a lawful modular row and is not an admitted row of the second contract.

The second fiber's two marginals are both `{0,1,2}`. Their product has nine pairs and introduces the six false completions `(0,0), (0,1), (1,0), (1,2), (2,1), (2,2)`. The product preserves each marginal's possibilities but loses the joint constraint required by this aperture. These are exact finite results; no handbook gap is needed to resolve them.

## 2. Converse of integer squaring

Assume both ports are integers and the relation is exactly `y=x^2`.

- `y=-1`: `NONE`, because an integer square is nonnegative.
- `y=4`: `MANY({-2,2})`. Factoring `x^2-4=(x-2)(x+2)` over the integers establishes coverage.
- `y=0`: `ONE(0)`, because only zero has square zero.

The forward function `f:Z→Z` is total. Its converse relation is neither a total function on `Z` nor single-valued: negative integers and positive nonsquares have no preimage, while every positive square has two integer preimages. Thus it is not a total single-valued inverse.

Restricting the target to the image makes the converse everywhere inhabited, but still leaves the two signs. Restricting the source to nonnegative integers and the target to nonnegative perfect squares gives a bijection and a genuine square-root inverse. Admitting complex numbers would change the `-1` fiber. Such changes require declaring a different carrier, rather than silently changing the current answer. The handbook supplies the required distinction between converse and inverse.

## 3. Endpoints and path witnesses

Take the source objects to be paths retaining their middle-point identity, and let the representation send `(x,y,z)` to `(x,z)`. Its reached image records which endpoint pairs have at least one compatible path. It preserves endpoint values and any question that is constant on every endpoint fiber.

It does not generally preserve the middle point, the number of paths, or a question that distinguishes the two given paths. In particular, `(x,m,z)` and `(x,n,z)` have identical summaries while `m≠n`. A unique endpoint pair therefore does not establish a unique path.

If the source consists of exactly the two stated paths, its fiber over `(x,z)` is exactly

`MANY({(x,m,z), (x,n,z)})`,

and its middle-point completion fiber is `MANY({m,n})`. If the statement merely exhibits those two paths in a larger relation, it establishes at least two witnesses; completeness of that displayed family remains `OPEN` until the whole admitted path relation is supplied or characterized.

Recovering all compatible middles requires retaining the witness triples or a complete reopen route to the exact relations that generate them. Recovering the particular originally selected middle additionally requires information distinguishing that selected witness, such as its retained middle value or path identity. A complete candidate family alone does not identify which member was originally chosen. A source hash without the source bytes or reconstructing generator is insufficient. The only qualification here is an ambiguity in the question's exhaustiveness, not a missing handbook rule.

## 4. Least refinement and reusable tags

The old parity fibers are `{0,2,4}` and `{1,3,5}`. Since `C(0)=C(2)=0` but `Q(0)=1≠0=Q(2)`, `Q` does not descend through `C`.

Use `C'(x)=(C(x),Q(x))`. Its reached values and fibers are:

| Reached value | Complete fiber |
|---|---|
| `(0,1)` | `{0}` |
| `(0,0)` | `{2,4}` |
| `(1,0)` | `{1,3,5}` |

Both old questions are decoded by coordinate projection. For any other representation `R` from which both `C` and `Q` can be decoded, their two decoders together decode `C'`. This proves that `C'` is the least informative refinement retaining both, up to mutual definability on reached images. It is still lossy for full source recovery.

The minimum reusable repair-tag alphabet has size **2**: the even fiber contains two distinct `Q` values, forcing two different tags there, and the odd fiber contains just one. The tag `T(x)=Q(x)` attains the bound with `{0,1}`; old parity plus tag is exactly the displayed refinement. Different old fibers may reuse tags because `C` already separates them.

For empty `X`, the empty tag carrier suffices, so the minimum size is **0**. This is a representational distinguishability bound, not a claim about how quickly tags or answers can be computed or accessed. Any runtime claim also needs an input encoding, algorithms, and cost model. No handbook gap affects this answer.

## 5. Future equivalence

All stated transitions are enabled, with the sole action `a` and the supplied three-state table complete.

- `s` always observes `0` after every word `a^k`.
- `t` observes `0` for the empty word and `1` after every nonempty word.
- `u` always observes `1`, including for the empty word.

The future-equivalence classes are therefore `{s}`, `{t}`, and `{u}`.

For `s,t`, a shortest distinguishing word is **`a`**: the empty word gives equal observations, and `a` gives `0` versus `1`. For `t,u`, it is **the empty word**: their current observations already differ. These minimality arguments are complete.

Present observation alone would merge `s,t`, but their successors lie in different observation classes: `s→s` has summary `0`, whereas `t→u` has summary `1`. Consequently present observation is not a lawful operational quotient for action `a`. The handbook directly supplies this check.

## 6. Finite-algorithm premises

The two-state system with infinitely many enumerated actions does **not** meet the finite-table algorithm's premises. A finite number of states bounds the number of possible strict partition splits; it does not provide a terminating scan of all actions or certify that an unseen action cannot force another split. An enumerator that never announces completion supplies no such certificate. A stopped finite prefix leaves the all-actions stability obligation `OPEN`, absent an additional complete symbolic argument.

Likewise, finite tables whose prescribed observation equality is undecidable do not meet the premises merely because the tables have finite size. One cannot assume an exact equality decision procedure from a finite list of names when those names denote observations with a different, undecidable equality.

The actual contract is a finite state set, a finite action set, complete deterministic partial-transition tables, and exactly decidable observations and transition comparisons, including exact enabledness. Under that contract each full refinement pass terminates, and every nonstable pass strictly splits a finite partition. For a nonempty `n`-state set there are at most `n-1` strict increases in the number of blocks. For lexicographically least shortest witnesses, the finite action alphabet must additionally have the declared order used by breadth-first search. None of these facts extends the stated algorithm automatically to an incomplete action enumerator. The handbook is explicit enough here.

## 7. Failure is not a successful value named NONE

No. The execution outcomes must be distinguished as, for example,

`Failure` and `Success(NONE)`.

The ordinary observation value spelled `NONE` is inside a successful result; its spelling does not make the successful transition undefined. At `p`, action `a` is disabled. At `q`, it is enabled and reaches `r`.

Thus any proposed summary merging `p,q` fails the enabledness condition despite equal present observations. The word `a` separates their tagged execution outcomes, so a quotient preserving definedness and observations must separate them. If the receiver also asks where a longer execution failed or for its history, those additional data must be retained explicitly. No further assumptions about the spelling of observation values can repair the enabledness failure.

## 8. Support versus probability law

Call the two distinct receiver classes `A,B`. Both transitions have support `{A,B}`. Assuming the current observations agree, their successor-class sets agree, so this pair passes the local support-based, set-valued preservation check. A quotient for a whole nondeterministic machine would still require the corresponding checks for every relevant fiber and action.

For the stochastic receiver, however, the probabilities of reaching `A` are `1/4` and `3/4`, respectively. The class-mass vectors differ, so this pair fails the stochastic preservation condition. For example, the indicator of landing in `A` has different probabilities in the two cases.

Equal support determines which class outcomes are possible here, not their probability law. The supplied one-step facts alone also do not establish any stronger path-distribution preservation result. These distinctions are directly covered by the handbook.

## 9. Guarded quantification

Let the source be `{s}` with `P(s)` true. Let the target be `{e,t}`, with encoding `E(s)=e`, `P'(e)` true, and `P'(t)` false. Atomic truth is preserved and reflected on the encoded image `{e}`.

- The source statement `∀x∈{s}, P(x)` is **true**.
- The unguarded target statement `∀y∈{e,t}, P'(y)` is **false**, witnessed by `t`.
- The image-guarded target statement `∀y∈{e,t}, (y∈im(E) ⇒ P'(y))` is **true** and matches the source statement.

The guard prevents an extra target state from becoming a new source quantifier case. Injection alone does not license unguarded quantification over the entire target.

The handbook's faithful-presentation theorem establishes truth equivalence of appropriately translated first-order statements under its encoding, atomic preservation/reflection, and quantifier conditions. It does not provide an algorithm deciding arbitrary first-order truth. This particular finite statement is decidable by its supplied two-element table; that fact does not generalize to arbitrary structures and statements.

## 10. Erasure, error, and truth

Assume labeled bit positions, bits in `{0,1}`, and the even-parity law that the sum of the four bits is `0 mod 2`.

For `(0,1,?,0)`, the erased bit must be **1**, so the completion is `ONE(1)` and the complete word is `(0,1,1,0)`.

For received `(0,1,1,1)`, assume the original word had even parity and exactly one of its four bits was flipped. There are exactly four compatible originals:

| Flipped position, numbered 1–4 | Possible original |
|---|---|
| 1 | `(1,1,1,1)` |
| 2 | `(0,0,1,1)` |
| 3 | `(0,1,0,1)` |
| 4 | `(0,1,1,0)` |

Each has even parity and differs from the received word at exactly its indicated position. Every one-bit change must choose one of these four positions, proving completeness: this is a four-member `MANY` fiber. Parity detects the inconsistency of the odd received word but does not locate the wrong bit or identify a unique original. The known location in an erasure question supplies information absent from the unknown-location error question.

Three agreeing reports do not establish truth without an error constraint; all three could agree on the same false proposition. If four channels report the same binary proposition and at most one report is incorrect, majority is correct. The operative guarantee is the bound on incorrect reports; agreement alone, even if described as independent, does not supply that guarantee. Consistency, correction under a declared error model, and external source truth are different receivers.

## 11. Compact numeral and the proposed prime certificate

Let `N=10^12` and interpret the constructor as the base-ten digit `1` followed by exactly `N` zeros. Then:

- Integer value: `10^(10^12)`.
- Base-ten numeral length: `N+1 = 1,000,000,000,001` digits.
- Last digit: `0`.

With zero-based indexing, position `0` contains `1`, positions `1` through `N` contain `0`, and `N` is the final position. Indices must be admitted integers in `[0,N]`; an out-of-range index is not a digit position in this numeral.

These answers follow from the constructor without expansion. A local digit query checks the index against `0` and `N`. Under a usual binary integer encoding, reading and comparing variable bounds and indices takes work in their bit lengths, so avoiding full expansion is not a constant bit-time guarantee. Explicitly outputting the full numeral would require at least `N+1` digit outputs. The known constructor supports these digit questions; it does not establish cheap arbitrary queries about every huge integer.

The zero count is a count of symbols in this specified representation. It does not establish geometric dimension, independent coordinates, or vector-space dimension without a separately defined carrier and preservation bridge.

For the claimed prime certificate, `p=11` is prime but

`2^11-1 = 2047 = 23×89`.

Both factors exceed 1, so this is a certified composite example and exactly refutes the implication “prime exponent implies prime Mersenne value.” The compact expression determines an integer; it is not itself a primality certificate. The handbook includes all distinctions needed here.

## 12. Checker agreement, soundness, and the biological bridge

Assuming the supplied finite case set `K` is complete and output comparison is exact, the strongest directly supported result is

`for every k in K, checker_1(k) = checker_2(k)`.

This is exhaustive agreement on the declared finite model. It is useful corroborating evidence, especially if implementation independence is separately established, but agreement alone does not show either output is correct. Two checkers can share a mistaken rule or return the same incorrect answer everywhere. If correctness on `K` were independently established against the intended semantics, that would support a stronger finite correctness claim; it is not part of the supplied evidence.

General soundness requires connecting a checker's accepted results to truth in the stated semantics. Treating the checker's own acceptance of its soundness claim as sufficient, while assuming that acceptance is trustworthy, risks assuming the proposition under examination. Cross-agreement alone does not remove that circularity or prove a proof system's axioms.

The biological application additionally requires an explicit bridge from the model to the proposed biological system: what real objects and measurements the model covers, how model states and operations correspond to them, which observations are preserved, and which empirical evidence supports those correspondences. A finite abstract agreement result supplies none of those physical premises by itself. The claimed general soundness and biological application therefore remain `OPEN` on the stated evidence.

An honest continuation record should retain:

- The exact admitted finite carrier, cases, laws, equality, context, and receiver, including the complete finite coverage argument.
- The exact source bytes of both checkers and the model, or complete reconstructing generators, with versions and hashes that bind those versions; hashes alone are not a reopen route.
- Inputs, outputs, how agreement was checked, failures, negative results, disagreements, and any unresolved correctness assumptions.
- A clear separation between the established finite agreement result and the unproved soundness and biological claims.
- The proposed model-to-biology maps, preservation obligations, missing evidence, declared test scope, and concrete failure criteria for subsequent experiments or proofs.
- Any forgotten witnesses or source details needed by the future receiver, as complete retained fibers or an executable/reasoned recovery route.

Continuation should reopen these specific obligations. If a proposed continuation requires a genuinely new carrier or receiver, it should be marked `OPEN_NEW_CARRIER` and specified explicitly. No broader claim should inherit proof status merely from the finite agreement.

## Handbook gaps

I found no material handbook gap preventing answers to these twelve questions. The handbook supplies the relevant contracts; the calculations and small proofs above use ordinary mathematics. Question 3 does not explicitly say whether its two paths exhaust the source, so I gave both the complete two-path answer and the properly bounded answer when they are only examples. Question 12 leaves the actual checker semantics and biological model unspecified; those are missing application premises to preserve as `OPEN`, not facts to invent from the handbook.
