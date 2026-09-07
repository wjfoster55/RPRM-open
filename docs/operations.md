# Operator contracts

The contracts use ordinary sets, relations and typed maps. Each theorem has a
written proof below. Formal and finite-test coverage is stated separately in
[verification.md](verification.md). Established constructions and their derived
compositions are not assigned mathematical novelty by these operator names.

## Reading an operator contract

An operator occurrence consists of a name/expression, context version, typed inputs, semantic kind, admission condition, and denotation. Its advertised guarantee also names its receiver, retained witnesses, inverse or complete fiber, and coverage. These are different fields: neither a name nor a filled contract proves the advertised guarantee.

The semantic kinds used here are `REL`, `PARTIAL`, `NONDET`, and `KERNEL`. A total map is a `PARTIAL` map whose domain is its whole input carrier. These are explicit tags even when one kind has a faithful encoding in another. Composition `g∘f` means first `f`, then `g`. A word printed in execution order `a₁…a_n` acts by `T_{a_n}∘…∘T_{a₁}`; the empty word acts by identity.

A map's source equality, equality of its retained output, and equality under a receiver are distinct. A fiber contains all admitted preimages under the declared equality; it does not select which preimage actually occurred. Source-occurrence and proof-ticket identities must be retained explicitly when the receiver asks for them.

## 1. EXECUTE and COMPOSE by semantic kind

For matching typed interfaces `X→Y→Z`, the four laws are:

| Tag | Input data | Composite | Identity |
|---|---|---|---|
| `REL` | `R⊆X×Y`, `S⊆Y×Z` | `(x,z)∈S∘R ⇔ ∃y, (x,y)∈R ∧ (y,z)∈S` | Diagonal relation on `X`. |
| `PARTIAL` | `f:D_f→Y`, `g:D_g→Z`, with `D_f⊆X,D_g⊆Y` | Domain `{x∈D_f:f(x)∈D_g}`; output `g(f(x))`. | Total `id_X`. |
| `NONDET` | `N:X→P(Y)`, `M:Y→P(Z)` | `(M∘N)(x)=⋃_{y∈N(x)}M(y)` | `x↦{x}`. |
| `KERNEL` | Finite normalized tables `K(y|x)`, `L(z|y)` | `(L∘K)(z|x)=Σ_y L(z|y)K(y|x)` | Point mass `δ_x`. |

`REL` states compatibility. `NONDET` adds the declared reading of a successor set, including `∅` as deadlock here; it still does not supply a scheduler, multiplicity, probability, or fairness law. `KERNEL` returns a distribution, not one realized sample. A normalized table has nonnegative entries whose row sum is one. Partial random operations must name a domain or a failure outcome; a zero row is not a probability distribution.

<a id="o01"></a>

**O01 — composition laws.** Each row defines an associative law with its stated identity. Both relation bracketings are the same two-intermediate-witness existence statement. Union gives the same proof for nondeterminism. Both partial-map bracketings have the same three-stage admission predicate and value. Both kernel bracketings have the same finite double sum; finite distributivity and reassociation identify them. The kernel composite stays normalized because summing its rows first over `z` leaves `Σ_y K(y|x)=1`. Identity follows by direct substitution. ∎

A partial map embeds into `REL` by its graph; graphs preserve composition, domains, and equality of partial maps. A total map embeds into `KERNEL` by point masses; these also preserve composition. The relation of positive-probability entries is a lossy view of a kernel: `(1/2,1/2)` and `(1/4,3/4)` on `{0,1}` have the same support and different laws.

An executable realization of `REL` or `NONDET` additionally supplies a selection/ticket mechanism whose output belongs to the declared successor set. Returning one member of a two-member set is not a proof that the set has one member. For a kernel, the mechanism must have the specified law if a distributional execution claim is made; an example sample or deterministic seed is not that proof by itself.

### Witness-aware composition

The retained composition object for two relations is

`W(R,S)={(x,y,z):(x,y)∈R and (y,z)∈S}`.

The endpoint relation is its projection `e(x,y,z)=(x,z)`. Its fiber at `(x,z)` consists of the possible intermediate witnesses. It can have `NONE`, `ONE`, or `MANY` even when the terminal-output fiber has a different disposition.

**Example.** Let `X={x}`, `Y={0,1}`, `Z={z}` and admit both routes `x→0→z` and `x→1→z`. There is `ONE` endpoint pair and `MANY(2)` intermediate witnesses. An endpoint receiver permits their merger; a path receiver does not. If witnesses themselves have separate derivation tickets, put those tickets in `W` before projection.

Parallel composition uses its own declared law. For kernels, independent conditional draws use the product of probabilities. Sampling one fair bit and copying it gives only `(0,0),(1,1)`, each with probability `1/2`; sampling two independent fair bits gives all four pairs, each with probability `1/4`. Marginal views agree and joint views differ. Shared randomness and independent randomness have distinct types/assumptions at this interface.

## 2. SOLVE

**Input:** a typed relation `R⊆∏_{i∈I}X_i`, missing ports `A⊆I`, and a supplied assignment `a` at `I\A`. **Admission:** every supplied port and value matches the declared signature. **Output:** the exact fiber

`F={u∈∏_{i∈A}X_i:a⊕u∈R}`,

represented extensionally or by a proved complete symbolic description. Direction is selected by `A`; no port is globally the input or output unless the instance declares that convention.

`NONE`, `ONE(u)`, and `MANY(F)` classify the exact fiber. Unresolved solving is `OPEN`; a malformed request is a validation failure. When no ports are missing, the missing-product carrier is `{()}`, so a satisfying full assignment yields `ONE(())`. If a queried output is itself the empty set, a graph query can return `ONE(∅)`; this is distinct from no completion.

<a id="o02"></a>

**O02 — complete finite solving.** Complete effective finite port enumerations, exactly decidable relation membership, and exact value equality suffice for a terminating complete solver: enumerate assignments and keep exactly those satisfying the supplied values and relation. Retained assignments are sound by membership; every solution appears by complete enumeration. Removing duplicate missing tuples preserves the set. ∎

All missing ports are solved jointly. The two-port equality relation `{(0,0),(1,1)}` has two completions, not the four obtained by multiplying its unary projections. A solver may expose those projections as additional observations, but cannot call their independent product the complete original fiber.

SOLVE does not infer a missing operation law from an unspecified family. `SOLVE.hypothesis` first declares `H`, experiments, and their evaluation law, then solves the corresponding consistency relation. Its `ONE` means unique in that family under the chosen syntax/semantic equality.

## 3. ATTACH and exposed-boundary composition

**Input:** compound/source carriers `L,R`; typed boundary occurrence families `B_L(l),B_R(r)`; and a compatibility predicate `K(l,b,r,c,t)` whose optional ticket `t` records a particular compatible matching realization. Without ticket distinctions, use a singleton ticket carrier.

**Output:** the retained attachment carrier

`J_K={(l,b,r,c,t): b∈B_L(l), c∈B_R(r), K(l,b,r,c,t)}`.

The ordered boundary pair `(b,c)` and ticket are the seam record. Direction and orientation are parameters of `K`; equality of payload numerals does not determine compatibility. If input occurrences with equal values must remain distinct, they are different elements of their boundary carrier. A value projection is applied only later.

A construction selecting an attachment from a request computes that request's fiber in `J_K`. No match is `NONE`; several compatible seams are `MANY`. A chosen attachment is one supplied witness, not an automatic collapse to `ONE`.

**Example.** Two left boundary occurrences `b₁,b₂` both have payload 5; one right occurrence `c` also has payload 5. If either match is admitted, there are two attachment records `(b₁,c)` and `(b₂,c)`. Replacing the occurrences by the value-only set `{5}` before attachment loses which boundary was used.

The next exposed boundary is another supplied map/family on `J_K`. If a construction internalizes the matched seam and exposes the unmatched ports, that operation must specify the exact occurrence names, ownership, orientation, and any compatibility debts. A geometry or drawing obtained from the joined records is another typed representation `render:J_K→G`, with its own fibers.

<a id="o03"></a>

**O03 — associative attachment in the fixed-seam case.** Suppose several finite relation records have fixed global port identities and fixed compatibility predicates on the final tuple, and each attachment retains every source row and seam witness without selecting, renaming, or deleting them. Any two bracketings that enforce the same complete list of predicates have canonically bijective retained output carriers, by tuple rebracketing.

**Proof.** Under either bracketing an admitted object consists of exactly the same source records and seam witnesses satisfying exactly the same conjunction of predicates. Flattening nested tuples gives the same common carrier; unflattening gives inverse maps. ∎

This theorem does not apply when the first attachment changes the later fit law, generates a different boundary, resolves ties, or erases a witness. Such a moving-boundary construction requires its own composition proof. Merely having a compatibility predicate does not establish geometric gluing, uniqueness, associativity, or the next carrier's dimension.

## 4. OBSERVE, PROJECT, CAR, and ADAPTER

`OBSERVE.Q` has type `Q:X→B` and returns a specified answer. A partial query uses a stated domain or total tagged answers with failure included. It need not change the stored state. `PROJECT.C` has type `C:X→Z` and names a retained representation; reading and retaining the same map are different uses.

Restrict decoding to the attained image `Z₀=C(X)`. The full inverse request at `z` is `C⁻¹(z)`. The forgotten source pairs are `ker C={(x,y):Cx=Cy}`. Here kernel means equality kernel; a stochastic kernel is a different typed object.

<a id="o04"></a>

**O04 — question descent.** A decoder `g:Z₀→B` satisfying `Q=g∘C` exists iff `Cx=Cy⇒Qx=Qy`. It is unique on `Z₀`. Necessity follows by applying `g` to equal arguments. For sufficiency define `g(Cx)=Qx`; the condition makes its value independent of preimage. ∎

`CAR` certifies a bijection between its declared source and attained image, with a two-sided inverse. If `C` is partial, its CAR source is its actual domain. `CAR` transports a question by `Q_C=Q∘C⁻¹` and a partial operation by `C∘T∘C⁻¹`, including its transported domain. The equations follow by cancellation.

`ADAPTER` is a typed translation equipped with a named preservation guarantee. For maps its guarantee can be O04 or an operational commuting condition. For relations it must specify whether it preserves existence, all witnesses, or a receiver quotient; a map theorem cannot be inferred merely from the word adapter. A proposed adapter remains an unproved candidate until its exact equations are established.

**Example.** On `X={0,1}`, the CAR `C(x)=2x` has image `{0,2}`. The question `[x=1]` transports to `[z=2]`; reusing `[z=1]` changes the answer. Carrying values without carrying the target is an incorrect adapter.

## 5. FOLD, including lossless cases

**FOLD is inclusive**: it certifies sufficient retention for a named receiver. A **strict FOLD** additionally merges at least two distinct source states. CAR, FOLD, and ADAPTER are overlapping certified properties, not mutually exclusive species.

The algebraic predicate does not itself assert a cold store exists. A deployed fold promising recovery additionally supplies rooted cold data, its binding, a retrieval domain, and the relevant availability assumptions. The combined hot-plus-cold system retains whatever distinctions those data recover.

### FOLD.question and FOLD.family

`FOLD.question(C,Q)` means O04. For a family `(Q_p)`, `FOLD.family` means every probe descends, equivalently `ker C⊆⋂_p ker Q_p`. More required probes can only reduce the set of admissible folds. Pairing all available readouts is one sufficient representation; the theorem does not promise compression.

### FOLD.operational for partial deterministic maps

Freeze `X`, current observation `O:X→B`, action alphabet `A`, and partial maps `T_a:D_a→X`. Then `C:X→Z₀` is an exact operational fold iff the following separately quantified conditions hold:

1. For every pair `x,y` with `Cx=Cy`, require `O(x)=O(y)`.
2. For every action `a∈A` and every pair `x,y` with `Cx=Cy`, require `x∈D_a ⇔ y∈D_a`.
3. For every action `a∈A` and every enabled pair `x,y` with `Cx=Cy`, require `C(T_a x)=C(T_a y)`.

The observation condition is independent of whether there are any actions. For `X={0,1}`, `A=∅`, constant `C`, and `O=id_X`, conditions 2–3 are vacuous but condition 1 fails. Thus the representation is neither a question fold for `O` nor an operational fold, despite the empty alphabet.

<a id="o05"></a>

**O05 — operational descent.** These conditions are necessary and sufficient for a decoder `Ō`, quotient domains `D̄_a`, and partial maps `T̄_a` with exact enabledness and `O=Ō∘C`, `T̄_a(Cx)=C(T_a x)`.

**Proof.** Necessity follows because the same retained input cannot give different answers, admission decisions, or retained outputs. Define the decoder by O04, the quotient domain as `C(D_a)`, and the quotient transition by `T̄_a(Cx)=C(T_a x)`. Conditions 2–3 make them well-defined and ensure that being in `C(D_a)` is equivalent to source admission. Substitution proves the commuting square. Induction gives the same success/failure and retained final value for each finite action word. ∎

The identity representation is an operational fold and a CAR. If `O(x)=x`, any exact question fold must be injective. Conversely an equally observed pair with an action enabled at only one fails condition 2 even if all jointly legal runs look the same.

### FOLD.future and its limit

Define `F_w(x)=OK(O(T_wx))` when the word succeeds and `FAIL` otherwise, with disjoint tags. `FOLD.future(C)` means every `F_w` descends. Any exact operational fold is future sufficient by O05. The converse for a particular detailed representation `C` is false.

**Example.** Let `X={p,q,r}`, all current observations 0, and one total action with `p→p,q→r,r→r`. Set `C(p)=C(q)=0,C(r)=1`. Every future observation is 0, so `C` is future sufficient. Yet its retained state 0 would have to update to both 0 and 1. A constant representation is a lawful operational fold; this more detailed representation is not. Future sufficiency determines what can be answered, while exact operational descent also constrains the chosen storage update.

### The canonical future quotient

<a id="o05f"></a>

**O05F — minimal future quotient.** For the deterministic partial system above,
admit all finite words in the fixed alphabet and use the disjoint `OK`/`FAIL`
observation tags. Put `x≡y` iff `F_w(x)=F_w(y)` for every such word. Then
`π:X→X/≡` is an exact operational fold. A representation `C` answers every
future exactly iff `ker C⊆≡`, equivalently iff `π=h∘C` for a unique map `h`
on `C(X)`. If there are finitely many `m` equivalence classes, every sufficient
representation has at least `m` attained values, and `π` attains this bound.

**Proof.** Equality of every answer is an equivalence relation. The empty word
gives observation agreement. A one-letter word gives enabledness agreement,
since failure differs from every success. For enabled `a`, equality of every
answer for words `aw` gives `T_a x≡T_a y`. O05 therefore applies to the class
map. Applying O04 to each `F_w` gives the kernel condition. Under that condition
`h(Cx)=[x]` is well-defined and uniquely forced; conversely this equation
implies the kernel condition. Distinct classes require distinct retained
values, while the class map retains exactly one value per class. ∎

For `m≥1`, a fixed-width binary encoding therefore needs at least
`ceil(log₂ m)` bits. This is an information bound with no decoder-time claim.
For an empty source there are no attained values. Restricting the future
language requires checking that the prefix/continuation reasoning still
applies; the theorem uses all finite words.

### Nondeterministic and stochastic folds

For `N_a:X→P(X)`, exact set-valued descent requires

`Cx=Cy ⇒ C[N_a(x)]=C[N_a(y)]`.

For finite kernels `K_a`, exact probability-law descent requires, for all `z∈Z₀`,

`Cx=Cy ⇒ Σ_{u:Cu=z}K_a(u|x)=Σ_{u:Cu=z}K_a(u|y)`.

In each case also require the receiver's static observations to descend. These equations are necessary and sufficient for the corresponding quotient map/set/kernel, by defining its value using a representative and checking independence. The normalized-kernel proof sums over a partition into `C`-fibers. Finite iteration preserves the relevant quotient sets or probability laws by union substitution or finite-sum substitution.

These predicates certify the stated kind of behavior. A branch-count receiver requires multiplicity data; a probability receiver requires probabilities; a scheduler observing erased source state requires its own translation. Equal successor supports with probabilities `1/2` and `1/4` at the same retained block do not define one quotient probability.

### FOLD composition

<a id="o06"></a>

**O06 — matched folds compose.** Suppose `C:X→Z₀` is an exact partial deterministic operational fold and `D:Z₀→W₀` is one for the resulting quotient interface and decoder. Then `D∘C` is an exact operational fold.

**Proof.** Observation decoding composes. Both exact enabledness equivalences compose. For enabled `x`, `D(C(T_a x))=D(T̄_a(Cx))=T̃_a(D(Cx))`. Thus O05 applies. For set-valued or kernel folds, substitute their matching quotient equations and respectively regroup unions or finite sums. ∎

Matching is essential: a second map preserving an unrelated observation or operation on `Z₀` does not satisfy this theorem's premises. Strictness is separate: a composite can be strict because either stage loses source distinctions, but a second-stage loss entirely outside the first stage's admitted image is irrelevant and must not be counted.

## 6. FIVE.future and TRACEBACK

`FIVE.future` takes a proposed representation `C`, a frozen deterministic partial system, and its future observation receiver. Its successful output is a witness `(x,y,w)` with `Cx=Cy` and `F_w(x)≠F_w(y)`. If "shortest" is claimed, the word length is minimized over the declared pair or over all merged pairs, as specified; a fixed action order may break ties. The two objectives must not be interchanged.

The empty word is eligible and detects a present observation failure. A witness refutes future sufficiency for precisely the admitted receiver/context. It neither identifies the original cause of the loss nor supplies a complete repair.

<a id="o07"></a>

**O07 — finite witness decision.** For an effectively given finite `n≥1` state carrier, finite effective alphabet, exactly evaluable domains/transitions/observations, and decidable equality, FIVE.future can either find a shortest separating word or certify that no such word exists for the declared merged pair set. Complete observation partition refinement, with a distinct absorbing failure state, stabilizes in at most `n-1` strict rounds; a separating word, if one exists, has length at most `n-1`.

**Proof.** Depth-zero blocks record current answers and distinct failure. At each round record each state's previous block and all successor blocks. Induction shows that equality at depth `j` means equality of all word answers of length at most `j`. With `n+1` completed states and at least two initial blocks, at most `n-1` strict splits can occur. A nonsplitting round is stable under every action, hence no later word can split it. Recording the first predecessor/letter explaining a split reconstructs a shortest witness; a breadth-first search using the same exact tables also does so. ∎

FIVE.future cannot expose a representational update failure that leaves every admitted future answer equal: the three-state example in Section 5 has no such witness. `CHECK.operational` can instead return an enabledness or retained-successor inconsistency. These are different witness types.

`TRACEBACK.loss` takes a reproducible later failure/counterexample, a retained route or dependency trace, a declared finite ordered carrier of possible repair locations, and exact predicates/certificates specifying what counts as a failed seam or lost required distinction at each location. It returns the earliest *supported* location under that declared order, together with the full retained trace. A search visits the historical route backward if desired; a claim of earliest location still requires checking every earlier admitted location relevant to that order.

<a id="o07l"></a>

**O07L — bounded loss localization.** For an effectively given finite ordered location carrier and decidable exact local failure predicates, enumeration returns the least location satisfying those predicates, or `NONE` if none does. A partial search can return a supported witness but cannot claim earliestness before all earlier admitted locations are ruled out. This follows directly from finite ordered enumeration. The conclusion is local to the declared diagnostic predicates and route; it is not a global causal-origin theorem. ∎

**Example.** Retain two source occurrences `0,1` and the route `C₀=id`, `C₁=constant`, `C₂=constant`. The later required question is source identity `Q=id`. The earliest representation merging this witnessed pair while their required answers differ is stage 1. The later symptom at stage 2 does not require repairing stage 2 if the declared source distinction is to survive the pipeline. A broader claim about why stage 1 was selected would require separate causal evidence.

An ordinary inverse request can additionally be named `TRACEBACK.preimage`: given a fixed word `w` and terminal value `y`, return `{x:T_wx=y}` or its full trace-witness fiber. If the word is missing, declare its admitted carrier too. This inverse-query profile has a different input and output contract from loss localization. Minimum-cost preimage search needs a cost law and complete route coverage. Reversing a relation produces compatible predecessors, not the actual historical predecessor.

For a constant map `{0,1}→{*}`, the terminal preimage fiber has two sources. If all admitted future observations are constant, no FIVE.future witness exists. If a later requirement newly demands source identity, TRACEBACK.loss can localize the merger only under that explicitly reopened receiver and its retained evidence.

## 7. REFINE.question and REFINE.stable

`REFINE.question(C,Q)` constructs `C'(x)=(C(x),Q(x))` on its attained image. It retains the old representation plus the new answer. The forgetful map `(z,b)↦z` recovers `C`; the inverse fiber lists the admitted new distinctions above an old value.

<a id="o08"></a>

**O08 — least question refinement.** `C'` is the least refinement of `C` making `Q` decodable, in the information preorder `D` refines `C` iff `C=h∘D` on attained images. Indeed both `C` and `Q` project from `C'`. If both decode from any `D`, their pair decodes by pairing those decoders, so `C'` also decodes from `D`. ∎

This is an information-order statement, not a smallest byte count or fastest representation theorem. If `Q` did not descend through old `C`, the new answer cannot be reconstructed from old `C` alone: doing so would contradict O04. Refinement therefore needs source access, a cold reopen route, or an additional experiment that supplies it.

<a id="o08r"></a>

**O08R — minimum finite repair alphabet.** Let `X` be finite and let
`C:X→Z` and `Q:X→B`. A tag `R:X→A` repairs the question when `(C,R)` is
sufficient for `Q`. For each reached fiber `K=C⁻¹(z)`, let `c(K)=|Q[K]|`.
The smallest possible alphabet cardinality is `0` when `X=∅`, and
`max_K c(K)` otherwise.

**Proof.** Within any one `K`, unequal `Q` values require unequal tags,
giving the lower bound. Number the `Q`-classes separately inside each fiber,
using at most the maximum number of tags. Tag labels can be reused between
fibers because `C` already separates those fibers. Then `(C,R)` determines
the `Q`-class and hence its answer. For empty `X`, the unique empty map to an
empty tag carrier suffices. ∎

For full source recovery replace `c(K)` by `|K|`. Tag-alphabet cardinality,
encoded length, access cost and update time remain different objectives.

One question refinement need not close the operational obligations.

**Example.** On `{p,q,u,v,r}`, let `O` be 0 except `O(r)=1`, and use the total action `p→u,q→v,u→r,v→v,r→r`. The one-step question separates `u,v`. Set `C'=(O,O∘T)`. Still `C'(p)=C'(q)=(0,0)`, while `C'(Tp)=(0,1)` and `C'(Tq)=(0,0)`. The witnessed distinction was repaired; the representation still cannot update exactly.

`REFINE.stable` starts from `(C,O)` and repeatedly splits retained classes by enabledness and successor classes until the required operational congruence holds. Its output is an exact operational fold that retains all distinctions in the old `C`.

<a id="o09"></a>

**O09 — least stable refinement on finite systems.** Under O07's effective finite assumptions, this process terminates and yields the coarsest equivalence relation contained in `ker C∩ker O` that preserves enabledness and successor classes.

**Proof.** Refinement only splits finite classes, so it terminates. A fixed point satisfies O05. If another equivalence `E` refines the initial partition and is stable, induction shows `E` refines every successive partition: equal `E`-states have equal previous blocks, equal enabledness, and `E`-equivalent successors, hence equal successor blocks. Thus `E` refines the final partition, proving coarseness. ∎

An arbitrary continuum can fail to admit a finite stabilizing depth. On `[0,1]`, `T(x)=min(1,2x)` and `O(x)=[x=1]` distinguish `2^{-m}` from `2^{-(m+1)}` first at depth `m`. Boundedness does not supply a finite refinement receipt.

## 8. COMPILE.endpoint and COMPILE.trace

A compiler is a map from a declared source language/program carrier into an artifact carrier, together with a semantics-preservation equation. The tag states which semantics is preserved. Producing code, a table, a formula, or a receipt is not itself a correctness proof.

For a word language over typed deterministic actions, `COMPILE.endpoint` may return the composite partial map `T_w` with its exact domain. Its guarantee is that evaluating the compiled artifact gives the same final state and success/failure as executing `w`. If failure position, error class, material identity, or intermediate states are required, those belong in the observation and are additional obligations.

<a id="o10"></a>

**O10 — endpoint compilation law.** For concatenated execution-order words `uv`, `T_{uv}=T_v∘T_u`, with identical domains. This follows by splitting execution after `u`; induction on word length establishes both domain and final-value equality. The empty word compiles to identity. ∎

`COMPILE.trace` instead preserves a declared trace object, such as `(x₀,a₁,x₁,…,a_n,x_n)` together with failure position or proof tickets when applicable. A compiler may keep the trace itself or an invertible encoding relative to that trace receiver. Projecting its endpoint gives an endpoint compiler. Recovering the trace from an endpoint compiler requires a complete inverse fiber or an additional retained record.

**Example.** On the singleton state carrier `{s}`, words `a` and `aa` under the identity action have the same endpoint map and different action counts, costs under unit cost, and traces. A table storing only the endpoint map merges them. It is correct under endpoint semantics and incorrect under the trace receiver.

For `REL`, compilation can preserve complete output sets or full derivation witnesses; for `KERNEL`, it can preserve the exact output law or the joint law of paths. These must be stated separately. Compiling a finite rule relation into an executable solver additionally proves that solver's soundness, completeness, and termination on its admitted inputs. No general compiler over unspecified mathematical languages follows from the operator name.

## 9. LIFT–SPIN–LAND

This is a typed construction/search pattern. Supply a lift `E:X→Z`, an internal partial operation `U:Z⇀Z`, and a landing `L:Z⇀Y`. The composite candidate is `F=L∘U∘E`, on exactly the source inputs where all stages are defined.

The original goal may be a specified source map `T:D→Y`, a relation `G⊆X×Y`, or a receiver answer. The landing claim must state its actual target: `dom F=D` and `F=T`; or `G(x,Fx)` for every promised source; or an exact receiver equation. These are different strengths. A search family `U_h` additionally declares its hypothesis carrier and retains all surviving candidate witnesses until its chosen acceptance rule is met.

When `Y=X` and `L∘E=id_X`, the lift/land pair is a retraction. This ensures that an unmodified embedded source is recoverable. It does not prove that an arbitrary internal operation satisfies the source target.

<a id="o11"></a>

**O11 — correct lift–operate–land.** If `U(E x)=E(Tx)` whenever `x∈D`, the richer operation is enabled at `E x` exactly on `D`, and `L∘E=id_X`, then the composite has domain `D` and equals `T`, provided `L` is defined on all these embedded successors.

**Proof.** Domain hypotheses give exactly the promised admitted source. For each `x∈D`, `L(U(E x))=L(E(Tx))=Tx`. ∎

The more general target-relation contract can succeed even when `U` leaves the lift image, but then its landing correctness needs an independent proof. A richer carrier makes extra operations expressible; the retraction alone does not make them correct.

**Example.** Let `Z={0,1}²`, `E(x)=(x,0)`, `L(x,b)=x`, and intended `T=id`. Internal `U(x,b)=(1-x,b)` lands at `1-x`. The retraction is exact and the proposed identity implementation fails. This is an explicit noncommuting landing seam.

## 10. PROMOTE and inherited capability

`PROMOTE.capability` is a family-specific typed adapter from a declared closed-compound subcarrier into a next-level carrier. Supply `Closed⊆Compound`, a map `P:Closed→Higher`, and the next-level receiver and operation interface. The admission predicate explains what closure means: complete seam matches, a complete solution fiber, an invariant, or a certificate. Those properties are not interchangeable.

To claim that a compound is usable as a higher-level capability, provide its higher-level observation decoders and operation commutation/domain equations. A retained record can also be promoted as an opaque artifact if the higher-level interface only observes that artifact and its checked receipt. This is a different interface from treating its internal value as a primitive port value.

<a id="o12"></a>

**O12 — conditional promotion.** If `P` satisfies the question factorization and operational equations for its explicitly declared higher-level interface, then it is the corresponding adapter/fold and composes under O06. The proof is exactly those factorization and substitution arguments; no geometric counting assumption is added. ∎

**Example.** A completed `Tile(X)` record containing four `X`-valued corners plus a law and proof is not automatically an element of `X`. Inserting it into an `X` port is ill-typed. A declared evaluator, encoding, or changed port sort can make the step meaningful, with its own loss and closure proof. The visual fact that both objects fit a square does not supply that adapter.

No universal arity, recurrence, geometric dimension, or scale law is established by PROMOTE. Those are explicit instance structures. If the next level requires a genuinely new type or generator, the old contract returns `OPEN_NEW_CARRIER` until that interface is specified and checked.

`PROMOTE.state` is a separate state-store convention: a candidate satisfying the supplied acceptance predicate becomes current through the conditional atomic FLICK operation. This installation contract and structural capability promotion have different hypotheses and conclusions.

## 11. SEAL, INHERIT, and FLICK

These operators connect mathematics to evidence and state management. Their guarantees are different from a relation being satisfiable or a map being invertible.

### SEAL

**Input:** a precise claim/context/receiver revision, its evidence, dependency identities, a verifier/admission procedure, and a stated soundness implication. **Output:** an immutable record binding those exact artifacts and the scope/grade of the conclusion. A digest can help bind bytes under the chosen integrity assumptions. It does not prove the claim, infer authorship, or authorize an external action.

For a checking relation `Verify_κ(claim,evidence)`, mathematical acceptance requires a separately justified statement

`Verify_κ(claim,evidence)=ACCEPT ⇒ Sat_κ(claim)`.

The implication can be proved for a narrow certificate language, assumed as part of an explicitly trusted checker, or remain open. A seal records which case applies. Hashing an invalid certificate cannot establish the implication. A correct theorem written in prose and a proved correct executable checker also have different assurance surfaces.

The seal's inverse is retrieval of its bound evidence under a declared route; a digest alone has a many-source mathematical preimage and supplies no general decoder. A receiver-sufficient hot record and the rooted cold artifact can coexist without claiming the source has been erased from the complete system.

### INHERIT

**Input:** an exact valid old evaluation of a finite acyclic dependency graph with fixed deterministic rules; complete base-input read masks; fixed contexts and dependency structure; and a new admitted base input with a set `W` containing every changed coordinate. **Operation:** recompute every node reading `W` and its graph successors; reuse every other node. The final gate belongs to this graph.

<a id="o13"></a>

**O13 — selective exact reuse.** If the changed set is complete and the rules, graph, masks, and contexts are fixed, the mixed recomputed/reused evaluation equals a full fresh evaluation wherever the latter is defined. If the complete new final gate accepts and the checker's soundness implication holds, the new claim follows.

**Proof.** Induct in topological order. A recomputed node receives exact new predecessor values and exact new base reads. A reused node has no changed base read and no affected predecessor, hence exactly its old arguments under the same fixed rule and context. Its old exact result remains exact. A recomputed undefined node agrees with full evaluation's undefinedness and rejects that candidate. Otherwise all values and the final gate agree with full evaluation, so soundness gives the claim. ∎

**Example.** A node really reads `(a,b)` but declares only `a`. Changing `b` leaves the node outside the recorded dependency cone and permits a stale result. The theorem does not repair incomplete masks. Changing a rule or receiver likewise reopens its dependent obligations; it is not covered by pretending only the old data changed. The worst affected cone can be the whole graph.

INHERIT's exactness is conditional on the old evaluation's validity. Retrieving a digest-bound stale or invalid cache does not satisfy that premise. The semantic receipt records the complete dependencies actually used; it does not turn an incomplete source model into a complete one.

### FLICK

**Input:** a current committed state with a unique revision identity, a candidate successor bound to that parent, its complete acceptance result, and the runtime's authority/admission policy. **Operation:** prepare privately, validate, then perform an atomic compare-and-install only if the current revision is still the expected parent. Failure leaves current state unchanged.

The next revision must have a fresh identity within the admitted run. A payload digest reused after a state returns to equal bytes is not necessarily a unique revision identity. This distinction prevents an old candidate from being mistaken for one bound to the current occurrence of a state.

<a id="o14"></a>

**O14 — conditional single-successor installation.** Under atomic comparison/installation and fresh revision identities, two competing candidates expecting the same parent cannot both install directly from that parent, and a rejected or stale candidate cannot change current state through this operation.

**Proof.** The first successful atomic step changes current revision away from the expected parent. Every later step comparing that parent fails. A step whose validation or parent comparison fails performs no assignment by contract. ∎

This is a runtime atomicity contract, not a consequence of O13's mathematical cache theorem. It does not prove the verifier sound, make I/O transactional outside the stated boundary, or grant permission to publish/deploy/send. This is a typed specification; any implementation and effects beyond the store require their own contract.

## 12. Operator coverage and unresolved families

The positive common pattern is explicit: solve a typed relation, retain attachment and computation witnesses, represent them through a proved map, preserve the named receiver, carry the next operation through matching interfaces, and bind reuse to unchanged evidence and context. Each exact bridge lets existing mathematical instances share operations without erasing the structures their own receivers require.

The table distinguishes the minimum certified surface of each name:

| Name | Minimum result required before its strongest tag is used |
|---|---|
| `SOLVE` | Complete admitted fiber, not a sample of candidates. |
| `ATTACH` | Retained compatible source/boundary/ticket tuple; exposed-boundary map when claimed. |
| `CAR` | Exact two-sided inverse between source and admitted image. |
| `ADAPTER` | Typed preservation equation for the named target/receiver. |
| `FOLD.question` | Answer constant on every retained fiber. |
| `FOLD.operational` | Observation, enabledness, and retained-successor descent, or its kind-specific analogue. |
| `FIVE.future` | A separating future; shortestness/absence only with coverage proof. |
| `TRACEBACK.loss` | Earliest supported lost distinction or failed seam in a declared diagnostic route/order. |
| `TRACEBACK.preimage` | Complete predecessor/trace fiber for a declared route carrier. |
| `REFINE.question` | Old representation plus the named new distinction. |
| `REFINE.stable` | Stable operational refinement with exact coverage. |
| `COMPILE.endpoint` | Same domain/final answer under declared endpoint semantics. |
| `COMPILE.trace` | Same full declared trace semantics, including admitted identities/costs/errors. |
| `LIFT–SPIN–LAND` | Typed composite and proved landing target on its exact domain. |
| `PROMOTE.capability` | Typed closed-compound adapter into an explicitly defined next interface. |
| `PROMOTE.state` | Adoption of an eligible candidate under a supplied state policy; atomic installation is FLICK. |
| `SEAL` | Bound claim/evidence/context and explicit assurance scope. |
| `INHERIT` | Unchanged complete inputs or exact dependency-cone recomputation. |
| `FLICK` | Accepted parent-bound candidate and conditional atomic installation. |

Terms such as reflection, spin, zero, pressure, dimension, and compound capability require their separately declared carriers and laws when used as operators or capability types. A negation, reciprocal, complement, permutation, and order reversal have different domains and inverse fibers. Their generalization is an open family until the exact shared interface and preservation theorem are given. Nothing in these contracts silently selects a universal law from a name or a shape.
