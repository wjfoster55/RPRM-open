# Mathematical glossary

This glossary defines the vocabulary of the core and operator contracts.
Definitions specify objects; family definitions require a supplied carrier
and law. Model-dependent quantities have no universal value or transition
law. Theorems, formal proofs, finite tests and interpretations retain their
separate evidence grades.

CAR, FOLD and ADAPTER are compatible properties. A question FOLD may be
injective; a strict FOLD is lossy. FIVE.future, TRACEBACK.loss and
TRACEBACK.preimage have distinct witness contracts. Each entry links to its
definition or theorem, with no external context required.

The book's [short reference guide](../MANIFESTO.md#reference-guide-special-terms-and-where-to-find-them)
provides a compact route through its core and applied terms, including clamp
transport, return depth, the coherence receiver and strong lumpability. This
glossary retains the detailed core/operator entries and their existing anchors.
Symbols are local to each supplied model: their carrier, units and equations
fix their meaning, even when another chapter reuses the same letter.

<a id="supp-aba-failure"></a>

### ABA failure

A stale candidate sees equal payload A before and after an intervening A-to-B-to-A history and is incorrectly accepted as bound to the current occurrence.

Fresh revision identities and atomic compare-and-install address this within the specified store boundary; a repeated payload hash may not.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="term-abduction"></a>

### Abduction

Propose a law, representation, operation or experiment that could explain or solve a specified task. Freeze a hypothesis carrier and evaluation rule before claiming exact narrowing of its survivors.

Generating a useful hypothesis family remains separate from finding a unique member of a supplied family.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 10](core.md#10-refinement-saturation-and-future-tests).

<a id="term-adapter"></a>

### ADAPTER

A typed translation carries a declared preservation contract: invertibility, question sufficiency, operational sufficiency, approximation under a metric, or a candidate obligation. Its input and output sorts and actual admitted domain are explicit.

An adapter may also be a CAR or FOLD. Correct types alone do not prove its preservation contract.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-address"></a>

### Address

An address is a coordinate in a supplied indexing scheme, such as a tree path or grid tuple. An address conversion is a map between the two schemes and their admitted images.

Equal printed addresses do not identify equal occurrences across schemes; addressing need not preserve adjacency.

See [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-admission"></a>

### Admission

An admission predicate restricts a well-typed carrier to inputs allowed by a particular problem or operation. Relation membership then determines compatible rows and their completion fiber.

Well-typed, admitted and solvable are three separate predicates. Domain decidability is an additional algorithmic assumption.

See [Core section 2](core.md#2-what-is-primitive-and-what-is-defined), [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 7](core.md#7-operations-are-typed-semantic-objects).

<a id="term-aperture"></a>

### Aperture

A selected typed interface exposes a relation question, an observation, a hypothesis, or a construction continuation. Each profile retains its own law, supplied data, missing roles and requested output.

The shared name does not establish an encoding or preservation law between profiles.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 2](operations.md#2-solve).

<a id="term-aperture-rotation"></a>

### Aperture rotation

Given a retained relation, choose a different supplied/vacant partition and solve that question's fiber. Its input is the relation and new environment; its output is the complete missing-role family or its requested readout.

A unique forward value can have several inverse sources. Rotation changes the question rather than proving a pointwise inverse.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 2](operations.md#2-solve).

<a id="term-assumption"></a>

### Assumption

An assumption is a stated premise accepted conditionally for a scoped derivation or test. It is an input to the claim and appears among its dependencies.

The conditional conclusion does not prove the premise. An established mathematical hypothesis need not be empirically verified to support a conditional theorem.

See [Core section 3](core.md#3-context-is-explicit-data-not-shared-intuition), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors).

<a id="term-atlas"></a>

### Atlas

In a declared hierarchy, an Atlas can be a compound of eight Board artifacts with one withheld integrated capability, using a separately supplied hypothesis carrier, experiment law and interface.

The eight-plus-center arrangement is an optional construction convention; no integrated capability or closure law follows from the count.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Operations section 10](operations.md#10-promote-and-inherited-capability).

<a id="term-attach"></a>

### ATTACH

Given two components, their boundary observations and a compatibility witness, construct the joined component while retaining matched sites, interface maps, orientation and enough lineage or forgotten-fiber data.

Projection of the joined object can be lossy. Local compatibility does not prove global geometry or whole-compound closure.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="supp-balance"></a>

### Balance

A state satisfies a specified equality or conservation relation, such as equal complementary lane readouts.

No single center or zero glyph supplies a universal balance law.

See [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="term-board"></a>

### Board

In a declared hierarchy, a Board can contain eight Tile artifacts constraining one withheld capability under its own hypothesis carrier, experiments, outcome model and closure predicate.

The compound has a new type. It does not inherit a component value type or fit rule from a diagram.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Operations section 10](operations.md#10-promote-and-inherited-capability).

<a id="term-boundary"></a>

### Boundary

A boundary may identify construction interfaces, current coverage, a chosen checkpoint, a certificate's limit or an actual failure locus. Specify which typed set and predicate defines it before using a continuation law.

A failed sufficient check can leave the property OPEN; it need not be a counterexample or last possible continuation.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="supp-boundary-completion"></a>

### Boundary completion

All required interface, matching and seam obligations of a specified compound have been discharged.

Geometric injectivity, global consistency and next-stage admission are additional obligations when not included in that predicate.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-boundary-elimination"></a>

### Boundary elimination

Project away specified boundary coordinates of a retained construction or relation. Input is the strong joined state; output is the selected exterior representation, with a fiber of compatible interiors.

A later receiver refinement cannot recover eliminated distinctions without additional retained evidence or a new observation.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="term-branch-and-rejoin"></a>

### Branch and rejoin

For finite incidence histories, retain shared-child links and intermediate identities. Natural matrix composition counts paths; Boolean composition records whether a path exists. Their outputs and inverse fibers differ.

Natural composition may leave a binary matrix carrier. Forgetting intermediate labels does not recover lost factorization or make orbit probabilities uniform.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-candidate"></a>

### Candidate

A candidate is an explicitly admitted option for evaluation: a state, law, artifact or proposed bridge. Its supplied candidate carrier and acceptance criterion determine the applicable test.

Candidate status neither guarantees truth nor authorizes use. A rejected candidate does not exhaust other options.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors).

<a id="term-capability-grade"></a>

### Capability grade

A grade is an ordinal stage of a specified bootstrap constructor: the rooted output at one stage becomes the typed input to the next through a declared interface.

It is not geometric dimension, physical maturity or an automatic increase in capability; the next-stage claim needs evidence.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Operations section 10](operations.md#10-promote-and-inherited-capability).

<a id="term-car"></a>

### CAR

A CAR is a bijection from a source to its admitted image, with inverse and relevant transported structure specified. For a representation map this requires injectivity, not surjectivity onto unused ambient values.

A CAR can also satisfy a FOLD contract. Exact invertibility alone establishes no speed or compression gain.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-carrier"></a>

### Carrier

A carrier is a supplied set of typed values or states, optionally with additional mathematical structure and admission predicates. Empty sets are allowed unless a theorem states otherwise.

Finite cardinality, finite description, spatial boundedness and a finite execution horizon are different conditions.

See [Core section 2](core.md#2-what-is-primitive-and-what-is-defined), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="term-carry"></a>

### Carry

Positional carry returns a normalized remainder and an outgoing coefficient under a fixed radix, digit/capacity carrier and destination valuation. Borrow is a separately specified signed normalization. Cyclic wrap returns a residue instead.

Linear successor, modular wrap, positional carry, winding lifts and real-limit decimal evaluation have different outputs and laws; none is a generic division-by-zero inverse.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 3](core.md#3-context-is-explicit-data-not-shared-intuition), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="term-cell"></a>

### Cell

A cell is a component in a supplied incidence/construction model, with typed interior, boundary and allowed attachments. Its completion and promotion depend on that model's law and receiver.

No universal square, four-state carrier, midpoint or geometric dimension is selected by the word.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="term-censoring"></a>

### Censoring

At a finite lineage horizon, a live frontier has unobserved continuation. A retained empty-generation event records another elapsed stage after extinction; it is different from leaving an unchanged tree without a rank.

A finite survival observation proves neither indefinite survival nor future extinction. State and event ranks must be retained when the receiver asks elapsed time.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="term-center"></a>

### Center

Specify a center by a carrier and rule: coordinate midpoint, balanced readout, fixed point, withheld capability or selected address. The rule gives its inputs and the center fiber.

A square boundary or 3x3 layout does not select an interior law. Different center definitions can share a numeral without agreeing.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="supp-certificate"></a>

### Certificate

A witness in a specified format has a verification predicate and a separately stated soundness implication connecting accepted witnesses to the desired claim.

An accepted byte string does not prove checker soundness or source interpretation by itself.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="supp-check-operational"></a>

### CHECK.operational

Check static observations, enabledness and retained-successor consistency on each merged source fiber and return the kind-specific discrepancy witness or a covered success result.

It can detect a retained-update inconsistency that no FIVE.future observation witness sees; complete success requires coverage.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="supp-claim"></a>

### Claim

A statement includes its hypotheses, context, quantified scope and evidence grade.

A label or receipt is not the proof; different scopes must not share an unqualified conclusion.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors).

<a id="term-clamp"></a>

### Clamp

In the affine relation x=(1-u)L+uR, the oriented endpoints L,R form a clamp. Noncollapsed clamps transport values through the same retained parameter u; see core section 19.

Here clamp transport is an invertible affine change of endpoint description,
not numerical clipping; see [Theorem II.1.2](../MANIFESTO.md#the-affine-chart-including-its-collapsed-cases).

All four single-port fibers retain their exact generic, singular and admission cases. Invertible value transport requires both endpoint pairs to be noncollapsed.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Affine aperture chart](core.md#19-the-affine-aperture-chart).

<a id="term-closure"></a>

### Closure

Specify transition closure, complete search coverage, invariant continuation, stable/sufficient receiver quotient, discharged boundary obligations, topological closure or completed workflow dispositions. Each has its own domain and proof predicate.

scoped Closure does not include actual receiver acceptance or an authority act. None of these senses means true forever.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="supp-coarsest-refinement"></a>

### Coarsest refinement

Among representations decoding both C and Q, the paired representation (C,Q) has the largest equality kernel and hence introduces only their required distinction.

Coarsest refers to information partitions, not unique labels, shortest bytes or fastest execution.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 7](operations.md#7-refinequestion-and-refinestable).

<a id="term-cold-reopen"></a>

### Cold reopen

Given a bound source/evidence root, retrieve the exact retained bytes needed by a changed obligation or receiver and recheck the affected claim. Output is recovered evidence or a visible retrieval/validation failure.

The recovery route, availability, provenance and cost are part of the storage contract; a hash is not the data itself.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="term-compile"></a>

### Compile

Compile a declared operation expression into an artifact preserving its endpoint or trace semantics. COMPILE.endpoint and COMPILE.trace specify the distinct guarantees.

A retained trace or inspection map is required when intermediate operations or witnesses belong to the receiver.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 17](core.md#17-a-connected-small-example), [Operations section 8](operations.md#8-compileendpoint-and-compiletrace).

<a id="supp-compile-endpoint"></a>

### COMPILE.endpoint

Compile a word/program into an artifact preserving exactly its composite partial domain and final state/success-failure under endpoint semantics.

Failure position, intermediate states, costs and proof tickets are additional receiver obligations, not recovered from the endpoint map.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 8](operations.md#8-compileendpoint-and-compiletrace).

<a id="supp-compile-trace"></a>

### COMPILE.trace

Compile while retaining the declared execution trace, identities, errors, effects or costs, or an encoding proved sufficient for that trace receiver.

Projecting endpoints gives an endpoint compiler. Recovering traces from endpoint-only code instead needs a full fiber or extra record.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 8](operations.md#8-compileendpoint-and-compiletrace).

<a id="supp-complement"></a>

### Complement

Given a fixed universe U and admitted subset A, complement returns U minus A; other complements require their own algebraic structure.

The universe/membership law is essential. One positive example does not determine an arbitrary complement boundary.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="term-completion-fiber"></a>

### Completion fiber

For a typed relation R and supplied environment eta, collect every compatible assignment to the requested missing block. For a representation output, collect every source mapped there. A readout may then project that full family.

Joint fibers retain correlation. ONE(empty set) and ONE(empty tuple) are possible values and differ from an empty solution fiber.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 2](operations.md#2-solve).

<a id="supp-compose"></a>

### COMPOSE

Apply the profile-specific composition: existential relation witnesses, sequential partial evaluation, successor-set union or finite kernel sum of products.

Matching sorts are necessary. Retained witnesses, multiplicities, laws and external effects require their own declared composite semantics.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-composition"></a>

### Composition

Compose partial maps on the domain where both stages are defined; compose relations by existence of a compatible middle witness; compose finite stochastic laws by summing products of masses over the middle carrier.

Existential relation composition forgets witnesses unless retained in a stronger join. Typed output/input matching is necessary but does not prove a preservation square.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-concept-sudoku"></a>

### Minimax experiment selection

Given finite hypotheses, experiments and typed predicted outcomes, choose a crossing experiment that minimizes the largest survivor bucket; declared tie rules can favor more buckets and then a fixed order.

This is one-step minimax discrimination in the supplied grammar, not a theorem of globally optimal experiment planning or discovery of hypotheses outside it.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 10](core.md#10-refinement-saturation-and-future-tests).

<a id="supp-conservation"></a>

### Conservation

A named quantity has an explicit equality preserved by a declared operation on its admitted domain.

Vacancy count, information distinctions and physical energy are different quantities and need separate laws/adapters.

See [Core section 15](core.md#15-residual-balance-pressure-and-negative-views), [Core section 17](core.md#17-a-connected-small-example).

<a id="supp-construction-boundary"></a>

### Construction boundary

Typed attachment sites, compatibility relation/witness and the data consumed, retained or exposed by joining a component.

A next-boundary law and geometric gluing properties require their own supplied structure and proof.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="term-context"></a>

### Context

A context is the versioned specification of signatures, carriers, equality, admission, operations, observations, failure rules and fixed parameters used by a claim. Changing determinants belong in state or a new version.

An identifier is only a reference to that data. A later timestamp or an unstated assumption is not a compatibility proof.

See [Core section 3](core.md#3-context-is-explicit-data-not-shared-intuition).

<a id="supp-converse"></a>

### Converse

For R subset X times Y, its converse relates y to x exactly when R relates x to y.

Converse is a relation; unique inverse recovery requires singleton fibers and the appropriate bijection contract.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-coupling"></a>

### Coupling

A probabilistic coupling is a joint law with specified marginals. A dynamical interaction instead requires a supplied state-transition law connecting components.

The two profiles need distinct interfaces. Marginals do not determine a joint law, and pairwise independence does not imply mutual independence.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="supp-declared-implementation"></a>

### Declared implementation

A program with input/output types, operational semantics and a correctness obligation relating its behavior to the intended denotation.

Merely producing executable code does not prove admission, termination, soundness or completeness.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects).

<a id="supp-decoder"></a>

### Decoder

A map from retained attained values to a requested answer, proving Q equals g after C.

It is unique only on C(X) under factorization. Existence does not entail effective or cheap computation.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="supp-denotation"></a>

### Denotation

The interpreted mathematical object assigned to an expression or operation name: map, relation, kernel or other explicitly specified semantic object.

Equal denotations do not force equal syntax, execution trace, effects or cost.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects).

<a id="term-dependency-cone"></a>

### Dependency cone

For a fixed evaluation graph with complete read masks, take the nodes reading changed base inputs and all graph successors. Recompute that cone and reuse exact unaffected values under the theorem's premises.

Completeness of masks and validity of the old evaluation are assumptions to establish. Worst-case work includes the entire graph.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="term-dimension"></a>

### Dimension

Name the particular definition: vector-space dimension, number of ports or independent coordinates, embedding/topological dimension, degree, address width or capability grade. Supply the carrier and structure determining it.

Equal numeric dimensions do not identify the corresponding objects or justify transport between them.

See [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="term-direction"></a>

### Direction

Choose which roles of a relation are supplied and which are requested, retaining their order and orientation. A map has a declared source-to-output leg within that relation.

Changing the requested leg yields a preimage problem, which need not have a single-valued inverse.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="supp-effect"></a>

### Effect

A state change, emitted trace or external-action description explicitly included in an operation's output/semantics when relevant to the receiver.

Omitting a relevant effect weakens the promise. Mathematical effect descriptions do not make real I/O transactional or authorized.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer).

<a id="term-enabledness"></a>

### Enabledness

For an operation with domain D, enabledness is membership in D. An exact partial-operation quotient must give the same membership answer for all sources it merges.

Deciding D is an extra capability. Comparing only operations legal at both sources can conceal enabledness loss.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-enclosure"></a>

### Enclosure

A stated subset or scope contains the states, operations or observations covered by a result.

Finite cardinality, finite description, metric boundedness and finite operation horizon are distinct.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="supp-environment"></a>

### Environment

A partial typed assignment eta to a declared subset of a relation's ports. The complementary block is withheld for joint completion.

Missing assignment is not a numerical zero, empty-set value or error result.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers).

<a id="supp-equality-kernel"></a>

### Equality kernel

ker C is the relation on source pairs with Cx=Cy; it states which sources the representation merges.

This use of kernel is distinct from a stochastic transition table.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="supp-equality-profile"></a>

### Equality profile

Specify occurrence, value, syntax, denotation, receiver-behavior or byte equality before comparing objects or forming fibers.

Equal denotations may have unequal syntax, costs and traces; none of these equalities silently substitutes for another.

See [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports).

<a id="term-event"></a>

### EVENT

An EVENT is a tagged transition or unresolved seam occurrence in a supplied state model. Its data may be exact while the desired output still fails stable-state admission.

STATE-to-EVENT-to-STATE is a typing convention for the construction, not a claim that an intermediate numeral does not exist or a physical event theorem.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-evidence-grade"></a>

### Evidence grade

Attach the kind and scope of support to a claim: established mathematics, derived synthesis, finite computation, conjecture or interpretation. Formalized coverage is identified separately.

Sanity checks, conformance, bounded exhaustion and formal proof describe verification methods, not permission. Do not silently translate one grade axis into another.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="supp-execute"></a>

### EXECUTE

Apply the declared semantic-kind operation to admitted inputs; an implementation claiming realization additionally supplies the needed selection/ticket mechanism.

A relation/set of outputs is not one actual selected output; a kernel law requires a correct sampler for distributional execution claims.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="supp-execution-trace"></a>

### Execution trace

A declared trace can retain the state-action-state sequence plus requested error position, identity, cost and proof tickets.

This is distinct from the first-witness term Trace; equal endpoints or denotations need not give equal execution traces.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 17](core.md#17-a-connected-small-example), [Operations section 8](operations.md#8-compileendpoint-and-compiletrace).

<a id="supp-expose"></a>

### Expose

Select a supplied next interface or family of visible boundary sites on a retained construction.

The exposed-boundary map is part of the constructor; a generic join does not derive it.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="supp-expression-tree"></a>

### Expression tree

Retained syntax records which operations and arguments are composed and in what arrangement.

A receiver observing syntax or costs can distinguish expressions with equal denotation.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects).

<a id="term-factorization"></a>

### Factorization

For C:X to Z and Q:X to B, a decoder g on C(X) with Q=g after C exists exactly when equal C values force equal Q values. On that reached image the decoder is unique.

This is an established mathematical criterion for sufficiency; it proves neither cheap decoding nor an algorithm when the relevant domains/equality are not effective.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-failure-receiver"></a>

### Failure receiver

Supply which operation failures are observed: at minimum distinguish failure from every successful answer. If error kind, failed step or effects matter, include them in the tagged observation.

A coarse FAIL convention deliberately merges other failure details and cannot later answer questions about them without refinement.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-fit"></a>

### Fit

Fit is a supplied compatibility predicate or witness relation on typed boundaries or candidate interfaces. Applying it returns acceptance witnesses, rejection or an unresolved verification obligation.

A drawing of touching components supplies no fit law. Particular research constructors may still have OPEN fit predicates.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="term-five"></a>

### FIVE

Use FIVE.future for a distinguishing-future search. Its witness consists of merged source states and a continuation producing different admitted observations.

Loss localization and preimage queries are distinct TRACEBACK profiles.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="supp-five-future"></a>

### FIVE.future

Search merged source pairs and admitted words for differing tagged future answers, minimizing length under a declared pair scope/order when claimed.

Fixed-pair shortestness and shortestness across all merged pairs differ. Finite coverage is needed for shortest/none certificates.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="term-flick"></a>

### Flick

Construct and validate an exact successor against a particular valid parent/context version, then atomically install it only while that parent version remains current. Rejection leaves the old state current.

Idempotency and stale-parent/ABA protection require explicit store semantics and version tokens. Mathematical validity does not authorize external publication.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="term-fold"></a>

### Fold

A representation is a FOLD when it is sufficient for a specified question or operational receiver. A strict FOLD additionally merges distinct admitted source states.

FOLD, CAR and ADAPTER are overlapping properties. Recovery from separately retained data is an additional storage contract.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 17](core.md#17-a-connected-small-example), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="supp-fold-family"></a>

### FOLD.family

Every observation in a specified family factors through the retained representation.

More probes restrict admissible folds; pairing readouts is sufficient but not necessarily compressive.

See [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="supp-fold-future"></a>

### FOLD.future

Every tagged answer after every allowed continuation word factors through the representation.

It need not allow exact updating of an arbitrarily more detailed retained summary; FOLD.operational is stronger.

See [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="supp-fold-operational"></a>

### FOLD.operational

Certify the kind-specific static observation, enabledness and successor/trace descent equations for the declared receiver and representation.

Use deterministic, set-valued or probability-law equations as appropriate; one kind's theorem does not supply another's guarantee.

See [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="supp-frontier"></a>

### Frontier

A typed boundary of current coverage: unvisited graph nodes, open attachment sites, unresolved obligations or exact exit states.

Which set it is determines its closure/continuation theorem; they are not interchangeable metaphors.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-frontier-localization"></a>

### Frontier localization

Prove no target occurs in a covered region and every first departure crosses an explicit frontier. Then any later target-reaching route must continue from that frontier, carrying its exit state/fiber.

This does not prove the target absent outside the region. A timeout without interior and exit coverage is weaker.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-future-equivalence"></a>

### Future equivalence

For a fixed deterministic partial system and all finite action words in its admitted alphabet, including the empty word, two states are equivalent if every word returns the same tagged observation. Failure is distinct from every successful output. The class map is the minimal sufficient future representation of O05F and [book Chapter II.4](../MANIFESTO.md#ii4-future-equivalence-distinction-and-stable-repair).

A restricted language requires its own closure assumptions. A more detailed future-sufficient summary can still fail to update exactly.

See [Minimal future quotient](operations.md#o05f).

<a id="term-future-scope"></a>

### Future scope

Supply the questions, operation words, consumers, horizons, errors, effects and counterfactuals a result promises to support. It is part of the receiver specification.

Every future quantifier is relative to this scope. A later new operation or question may require refinement or a new context.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-future-test"></a>

### Future test

Given merged states, a receiver and a declared witness order, search for an allowed continuation with unequal observations. Return its retained witness, a complete no-witness result, or OPEN search.

A found witness need not be shortest unless coverage establishes that claim; traceback of lost information is a separate computation.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="term-half"></a>

### Half

Half is 1/2 relative to a declared unit/coordinate. Binary centering maps 0,1 to -1/2,+1/2; two complementary unit-total lanes balance at (1/2,1/2).

Two coordinate occurrences of -1/2 remain a pair until a sum is requested. For k equal unit-total lanes the coordinate is 1/k.

See [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="supp-hide"></a>

### Hide

Project an interface out of the visible representation while declaring where its seam/witness data remains or what is lost.

Hiding is not evidence destruction when data remains elsewhere, and a sufficient exterior summary needs its own receiver proof.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="term-hostile-case"></a>

### Hostile case

Supply an input, mutation or counterexample designed to expose a missing assumption, preservation failure or implementation defect. Record expected behavior and exact comparison scope.

An out-of-carrier control tests rejection/boundaries; it is not automatically a counterexample to the in-carrier theorem.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors).

<a id="term-hot-state"></a>

### Hot state

The hot state is the currently retained representation and live obligations used for ordinary continuation, plus necessary bindings to cold evidence. Measure its size and access/update work under a declared model.

Small summaries can have expensive decoders. No constant-memory or frontier-proportional cost theorem follows without a constructor and cost proof.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="term-hypothesis"></a>

### Hypothesis

A proposed explanatory or predictive rule has a specified family, interpretation and experiments giving predicted outputs. Record which outcomes could contradict it.

Survival is consistency with supplied evidence/model, not exclusion of rules outside the family.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors).

<a id="supp-hypothesis-aperture"></a>

### Hypothesis aperture

Supply hypothesis/experiment carriers, typed outcomes, evaluation law and evidence; withhold the rule compatible with that evidence.

The rule family and grammar are supplied. A surviving rule outside a noise-free deterministic model need not describe the world.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles).

<a id="term-hypothesis-fiber"></a>

### Hypothesis fiber

Given hypotheses, experiments, an evaluation law and retained outcomes, collect exactly the hypotheses matching every outcome. This is relation completion with the rule withheld.

ONE is one survivor inside the family; NONE is inconsistency; MANY retains alternatives. Joint evidence remains correlated.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 2](operations.md#2-solve).

<a id="term-identification"></a>

### Identification

Express recognition as a relation between an object/source/law and its observed effect or context, then solve the requested source-role fiber.

Recognition can remain MANY. Matching labels or numerals does not establish faithful shared structure.

See [Core section 1](core.md#1-the-purpose-and-the-mathematical-claim), [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 2](operations.md#2-solve).

<a id="supp-identity-operation"></a>

### Identity operation

The map id_X sends each admitted x to itself; profile-specific identities are diagonal relations, singleton successor sets and point-mass kernels.

Identity endpoint behavior is not identity of syntax, occurrence or execution trace.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-inference"></a>

### Inference

An inference derives a conclusion from stated premises by a named rule or argument. Record the premises and the rule's applicable domain.

The conclusion inherits unresolved premises and their scope.

See [Core section 3](core.md#3-context-is-explicit-data-not-shared-intuition), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors).

<a id="term-inherit"></a>

### INHERIT

Reuse an exact valid old result when its complete relevant dependencies have not changed; recompute the justified affected cone for admitted edits.

The dependency theorem assumes complete masks, sound rules and valid old values; it does not authenticate arbitrary cached outputs.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="term-inner-frontier"></a>

### Inner frontier

Inside a fixed receiver enclosure, identify the live candidates, open sites or obligations sufficient for the current question, and update them through supplied refinement/coverage rules.

Moving this set is not extending the outer carrier. Reduced cost requires a representation and cost argument.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="term-interpretation"></a>

### Interpretation

A formal interpretation supplies encoded carriers, operations, predicates and a translation of the stated formula class, with a preservation claim. An explanatory interpretation is a separate reading of a construction.

Explanatory analogy is not a proof premise; formal preservation requires its equations or theorem.

See [Core section 1](core.md#1-the-purpose-and-the-mathematical-claim), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors).

<a id="term-invariant"></a>

### Invariant

A region contains the specified starts and is preserved by every admitted successor. If it excludes the target, induction excludes that target on every admitted finite reachable state.

Samples and a single closed orbit do not establish all-source coverage.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="supp-invariant-closure"></a>

### Invariant closure

Initial coverage, transition preservation and the target conclusion together cover every admitted finite continuation.

An invariant proof can cover more than explicit enumeration, but its hypotheses still require justification.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-inverse"></a>

### Inverse

A map inverse undoes a bijection on its image. A relation converse swaps roles and can have several preimages. A retraction undoes an embedding on its source image.

Name the construction; negation, complement, reciprocal and choosing a representative are different operations.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 14](core.md#14-lift-internal-operation-and-landing), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-joint-receiver"></a>

### Joint receiver

Given readouts on one source, retain their tuple. Its fibers are the actual intersections of component fibers, preserving their alignment and correlation.

Individual fiber sizes do not determine intersections. Joint readouts may identify an answer without recovering the whole source.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="supp-kernel"></a>

### KERNEL

The tag denotes a normalized nonnegative finite mass table K(y given x). Composition sums products over intermediate states; identity is point mass.

A zero row is not a normalized probability law. This is distinct from the equality kernel of a representation.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-lawful-mathematical-transport"></a>

### Lawful mathematical transport

A representation/interpretation transports source carriers, operations, predicates and targets with an explicit preservation theorem. A bijection E transports T as E after T after inverse(E), including its domain.

Source mathematics remains the obligation. Expressibility supplies neither a solver nor universal cross-domain preservation.

See [Core section 1](core.md#1-the-purpose-and-the-mathematical-claim), [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-lens"></a>

### Lens

Package a carrier/context, operation, receiver, retained/lost structure, inverse/fiber, boundary and evidence as one mathematical view/tool. Several lenses may remain concurrently available.

Composition requires typed proved adapters. Shared numerals do not make lenses identical or independent evidence.

See [Core section 1](core.md#1-the-purpose-and-the-mathematical-claim), [Core section 3](core.md#3-context-is-explicit-data-not-shared-intuition), [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties).

<a id="term-lift-spin-land"></a>

### LIFT-SPIN-LAND

Supply lift L and partial landing P with P(Lx)=x. Apply internal H and land P(H(Lx)) only where each stage is admitted. Prove the requested source operation or receiver equality.

Invertible internal H can still yield a lossy landed map. Mathematical landing and state-store adoption are separate.

See [Core section 14](core.md#14-lift-internal-operation-and-landing), [Operations section 9](operations.md#9-liftspinland).

<a id="term-lineage"></a>

### Lineage

Lineage is explicit typed predecessor/occurrence/source data needed by a receiver, such as matched-site identity or the input producing an artifact.

A label does not authenticate authorship. Equal values can have different lineage; dependent views can share one source.

See [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports), [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 8](operations.md#8-compileendpoint-and-compiletrace).

<a id="term-loss"></a>

### Loss

A representation loses distinctions between different sources in the same output fiber. State which identities, values, histories or observations merge and which readouts still decode.

Cold originals belong to the larger storage package; they do not change fibers of its hot projection or make retrieval free.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-many"></a>

### MANY

MANY(F) states that the complete admitted completion fiber has more than one member. A symbolic family requires an exact completeness argument.

No probability or realization is implied. ONE displayed readout may still hide MANY source completions.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Operations section 2](operations.md#2-solve).

<a id="supp-mathematical-quotient"></a>

### Mathematical quotient

The carrier of equivalence classes under a specified equivalence, with class projection from the source.

It is separate from a storage package providing cold recovery and from any presumed small byte encoding.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="term-minimum-repair"></a>

### Minimum repair

For finite X, representation C and requested Q, add a tag R so that Q decodes from (C,R). The minimum tag-alphabet cardinality is the maximum number of Q-values in a reached C-fiber; it is zero for empty X.

This is O08R. Alphabet cardinality, encoded length and runtime are different optimization objectives.

See [Minimum repair theorem](operations.md#o08r).

<a id="supp-moving-vacancy"></a>

### Moving vacancy

An occupancy state variable identifies an empty site. The declared swap exchanges the selected token and vacancy addresses.

Conservation follows for that swap model, not creation, deletion or multiple occupancy.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 17](core.md#17-a-connected-small-example).

<a id="supp-negation"></a>

### Negation

In a supplied additive structure, negation returns the additive inverse relative to the declared zero and addition law.

Do not equate it with order reversal, complement, reciprocal or a missing value.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="supp-nondet"></a>

### NONDET

The tag denotes N:X to the powerset of Y; its output is the admitted successor set and empty set means deadlock in this profile.

No scheduler, fairness, multiplicity or probability law is included unless separately supplied.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-none"></a>

### NONE

NONE means the complete admitted fiber is empty. In hypothesis narrowing it means no supplied hypothesis fits the full evidence record.

Incomplete search is OPEN. Ill-typing, denial, an empty-set value and numerical zero are different results.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 2](operations.md#2-solve).

<a id="term-number"></a>

### Number

A numeral denotes a value only through a sort and interpretation, and may also address a supplied enumeration or lens collection.

Rank, radix position, residue, ordinal and geometric coordinate remain distinct roles despite equal spellings.

See [Core section 2](core.md#2-what-is-primitive-and-what-is-defined), [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="term-observation"></a>

### Observation

A mathematical observation is Q:X to B. A captured observation binds source, method and outcome before interpretation. An intervention additionally updates state through M and returns (M(x),Q(x)).

Passive and state-replacing observations differ. Receiver, representation and decoder are also distinct objects.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="supp-observation-aperture"></a>

### Observation aperture

Supply a probe family, selected probe, admitted source or source fiber and answer type. The probe graph explicitly encodes it as a relation question.

Encoding a readout as a relation is not a physical boundary-opening event.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles).

<a id="supp-observe-q"></a>

### OBSERVE.Q

Apply the specified readout Q to an admitted source, using an explicit domain or total tagged failures for a partial query.

Reading does not automatically alter or retain state; an intervention has additional state/effect semantics.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-occurrence"></a>

### Occurrence

Supply identifiers, a type map and typed value assignment, adding incidence, position, ancestry/source maps as needed. Different occurrences may have equal values.

Occurrence, value, syntax, denotation, behavior and byte equality are distinct relations.

See [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="supp-occurrence-carrier"></a>

### Occurrence carrier

A set of identifiers with type and value maps; optional source, incidence, position and ancestry maps provide additional retained structure.

Identifiers alone do not prove uniqueness of meaning, ownership or authenticity.

See [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports).

<a id="term-one"></a>

### ONE

ONE(a) means the complete admitted fiber has one member a. A fully supplied valid relation returns ONE(empty tuple); a deterministic empty-set answer can return ONE(empty set).

Uniqueness applies to the declared role/readout, not every forgotten source history.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 2](operations.md#2-solve).

<a id="term-open"></a>

### OPEN

OPEN records an unresolved mathematical or verification obligation and its settlement condition.

It is not a numerical port value or a proof that a completion fiber is empty.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors).

<a id="term-open-landing-seam"></a>

### OPEN_LANDING_SEAM

The proposed lift/operation/landing composite has an unresolved type, domain, or target-preservation obligation.

One failed proposed landing does not prove that no valid landing exists.

See [Core section 14](core.md#14-lift-internal-operation-and-landing), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 9](operations.md#9-liftspinland).

<a id="term-open-new-carrier"></a>

### OPEN_NEW_CARRIER

Use when a new question needs a coordinate, operation, grammar, receiver or type outside the current context; record the new contract and missing transfer proof.

A legitimate new carrier cannot inherit an old guarantee by silent enlargement.

See [Core section 3](core.md#3-context-is-explicit-data-not-shared-intuition), [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Operations section 10](operations.md#10-promote-and-inherited-capability).

<a id="term-open-search"></a>

### OPEN_SEARCH

Use for incomplete or timed-out search or a grammar lacking completeness/minimality proof; retain witnesses and the explored boundary.

No candidate found is not NONE; no shorter one found is not globally shortest.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 2](operations.md#2-solve).

<a id="term-operation"></a>

### Operation

An operation name denotes a relation, partial map, finite nondeterministic successor map, finite stochastic law, or implementation with correctness semantics. Ordered input products fix arity; relevant effects/traces are outputs.

Supply types, parameters, admission, direction and composition. A law is not a realized event; syntax is not behavior.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-operation-alphabet"></a>

### Operation alphabet

The alphabet supplies named operations and fixed parameters for admissible continuation words. A fixed ordering supports canonical shortlex search.

Finite-state algorithms additionally need effective finite enumeration, exact transitions and equality.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="supp-operation-name"></a>

### Operation name

A syntactic symbol in a signature, with parameter and arity declarations identifying the requested operation occurrence.

A name does not determine a denotation, algorithm, domain or proof.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects).

<a id="term-operational-fold"></a>

### Operational fold

Merged sources must agree on observations, each operation's enabledness and required retained successors/effects, so operations descend to the representation.

Question or all-future answer sufficiency is weaker than exact updating of an arbitrarily more detailed summary.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="supp-operational-receiver"></a>

### Operational receiver

A question receiver plus operation names/parameters, semantic profile, timing, failures, future scope and required trace/effects.

Required probabilities, multiplicities, schedules and failure details cannot be discarded as if all operational receivers were deterministic endpoints.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="term-orbit"></a>

### Orbit

Iterate a named operation from a supplied start, retaining period, preperiod, fixed point, branch or exit according to its semantic profile. Multiple generators retain ordered words.

One returning orbit does not cover all starts. Two involutions need not commute.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="term-outer-enclosure"></a>

### Outer enclosure

The declared carrier and receiver delimit a result. A last structurally new class requires a specified equivalence and stabilization or recurrence theorem.

An arbitrary carrier need not have a half, order or greatest element; interval notation applies only after these structures are supplied.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="term-outside-scope"></a>

### Outside scope

An item violates the declared carrier, context, horizon or receiver admission; record which boundary it crosses and any proposed new context.

Outside scope does not mean false; an old claim needs an adapter before applying there.

See [Core section 3](core.md#3-context-is-explicit-data-not-shared-intuition), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="supp-parallel-composition"></a>

### Parallel composition

Supply a law for combining simultaneous components; independent conditional kernel draws use products, while shared randomness uses a supplied joint law.

Copying one random bit and sampling two independent bits have equal marginals but different joint outputs.

See [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="supp-partial"></a>

### PARTIAL

The tag denotes a deterministic map f:D to Y with D a subset of X. Composition admits x exactly when the first step and the resulting second input are admitted.

A total map uses D=X. A mathematical partial map need not have decidable domain or an implemented algorithm.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-partition-refinement"></a>

### Partition refinement

For an effectively given finite deterministic partial system, partition by tagged observations and split by successor-class signatures/definedness until stable, obtaining future equivalence.

Finite cardinality and exact evaluability matter; a bounded continuum need not have finite distinguishing depth.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 7](operations.md#7-refinequestion-and-refinestable).

<a id="supp-passive-observation"></a>

### Passive observation

Return a declared readout Q(x) while leaving the stored state x unchanged.

A physical or effectful observation needs its own state/effect model.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-payload"></a>

### Payload

The payload is the typed value/occurrence carried by a supplied construction step; retain identity and lineage when the receiver asks for them.

Opposite motion to vacancy belongs to a particular occupancy/swap law, not arbitrary creation or movement.

See [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports), [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="term-port"></a>

### Port

A port is a named role with a value sort and specified interface behavior; its indexed/ordered collection determines the assignment product.

It is not the full aperture specification, an automatic geometric hole, network socket or source occurrence.

See [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports), [Core section 5](core.md#5-relations-environments-and-complete-fibers).

<a id="term-possibility"></a>

### Possibility

Possibilities are a supplied relation fiber or set of successors admitted by the context and law.

Cardinality supplies no probability, independent choice or realization. Preserve joint correlation.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-pressure"></a>

### Pressure

A model may measure pressure by a constraint count, residual norm, resource deficit, live-fiber size or other typed state readout. Specify its units and decision rule.

No universal scalar/minimization law is adopted. Log2 fiber size is not entropy without a law and is not unchanged on empty/infinite fibers.

**Model-dependent:** supply the measurement and decision law; no universal law is asserted.

See [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="term-probability-law"></a>

### Probability law

A finite stochastic law assigns normalized nonnegative masses to a declared carrier. A receiver pushes it forward by summing masses inside output fibers.

The law does not choose a realized event; uniform labelled mass can yield nonuniform quotient/orbit mass.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="supp-project-c"></a>

### PROJECT.C

Apply C:X to Z as the retained representation, with reached image and source fibers explicit.

Using a map to retain data differs from merely observing its output. Receiver sufficiency requires a separate factorization proof.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="supp-promote-capability"></a>

### PROMOTE.capability

Map a declared closed-compound subcarrier into a higher-level carrier with explicit observation and operation-interface preservation.

Closure is a supplied predicate; no universal arity, dimension increase or re-entry from Tile(X) to X follows.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Operations section 10](operations.md#10-promote-and-inherited-capability).

<a id="supp-promote-state"></a>

### PROMOTE.state

A candidate satisfying a supplied acceptance predicate becomes current through the conditional atomic state-store operation FLICK.

This does not establish structural capability promotion or prove the stored mathematical claim.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 10](operations.md#10-promote-and-inherited-capability).

<a id="term-promotion"></a>

### Promotion

A constructor creates a new compound type and exposes it through a specified interface. PROMOTE.capability requires the observation and operation preservation equations of that interface.

A compound value is not automatically a value in a component port type. PROMOTE.state is the separate conditional state-store convention.

See [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 10](operations.md#10-promote-and-inherited-capability).

<a id="supp-question-fold"></a>

### Question FOLD

FOLD.question(C,Q) certifies that Q is constant on C-fibers and therefore decodes from C.

It may be injective. This predicate alone claims neither strict loss nor a cold store.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="supp-question-receiver"></a>

### Question receiver

An indexed family of typed observations on a supplied source; equality means agreement on every admitted probe.

The family is explicit and may be finite or separately delimited; decoding complexity does not follow from its existence.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer).

<a id="term-realization-ticket"></a>

### Realization ticket

A retained selection occurrence identifies which admitted successor occurs in a declared branching/selection construction. Include parameters/state needed for replay.

A probability law cannot reconstruct the ticket; a ticket does not establish physical randomness or independence.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-receipt"></a>

### Receipt

Record exact subject, context, method, inputs, check outcome and dependencies, binding bytes and checker identity where needed for audit/reopening.

A successful checker output or receipt's existence does not prove soundness, authenticity, novelty or authority.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="term-receiver"></a>

### Receiver

A question receiver supplies observations to preserve. An operational receiver also supplies operations, timing, parameters, failures, futures and required effects/traces, defining relevant behavioral equality.

Specification, representation, observation, decoder and actual consumer acceptance are distinct objects.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="supp-receiver-closure"></a>

### Receiver closure

A specified question/operation representation is sufficient or a declared quotient-refinement has stabilized.

Name the receiver/profile; it need not cover new future probes or imply an authority act.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-receiver-saturation"></a>

### Receiver saturation

Question saturation means a specified additional observation family makes no further split of retained fibers. Operational saturation means a specified refinement is transition-stable.

Name the profile. Saturation of a fixed family does not exhaust every imaginable future question.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="supp-recurrence"></a>

### Recurrence

A stated relation between stages has supplied initial conditions and a preservation/induction argument when claimed beyond observed stages.

Repeated examples alone do not prove all-stage behavior; quantifying over finite stages does not perform an infinite computation.

See [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion).

<a id="term-refine"></a>

### Refine

Given representation C and required question Q, retain (C,Q); its kernel is their kernel intersection, the coarsest information refinement decoding both. Other refinements declare their target.

Repairing this question does not stabilize all future operations. Recheck congruence; partitions do not select byte labels or optimal runtime.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 7](operations.md#7-refinequestion-and-refinestable).

<a id="supp-refine-question"></a>

### REFINE.question

Construct (C(x),Q(x)) and its attained image, retaining the old summary plus the new required answer.

If Q did not decode from C, refinement needs source access, cold recovery or an additional experiment to obtain it.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 7](operations.md#7-refinequestion-and-refinestable).

<a id="supp-refine-stable"></a>

### REFINE.stable

Starting from the retained representation and static observation, split classes by enabledness/successor classes until exact operational congruence holds under the effective finite assumptions.

A one-question repair need not be stable; a bounded continuum may never reach finite stabilization depth.

See [Operations section 7](operations.md#7-refinequestion-and-refinestable).

<a id="term-refold"></a>

### Refold

After adding a witnessed distinction, recompute the receiver quotient and retain changed merges/splits and renewed continuation obligations.

The new observation alone need not produce operational stability. Refold changes a quotient; Compile makes a verified sequence into a macro.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 7](operations.md#7-refinequestion-and-refinestable).

<a id="supp-rel"></a>

### REL

The semantic tag denotes a relation R subset X times Y; composition existentially quantifies compatible middle states and identity is the diagonal.

It records compatibility without selecting an output or retaining every derivation witness automatically.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-relation"></a>

### Relation

A relation is a specified subset of the product of typed port carriers. An environment/aperture selects direction; the relation itself has no inherent input/output split.

Empty relations are allowed, the empty product is a singleton, and no universal four-port/affine arity is assumed.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Operations section 2](operations.md#2-solve).

<a id="supp-relation-aperture"></a>

### Relation aperture

Retain context, relation, port set/types, supplied subset/environment, missing block and readout. Return the complete missing-role fiber or its readout image.

Unique readout need not mean a unique full completion; zero missing ports can yield ONE(empty tuple).

See [Core section 6](core.md#6-aperture-has-several-precise-profiles).

<a id="term-representation"></a>

### Representation

A representation C:X to Z retains actual data about sources. Use its reached image for decoders/inverses and its kernel for merged distinctions; retain any needed codebook.

Receivers specify questions and decoders answer them from C. These roles are distinct even when one example uses equal maps.

See [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="supp-residual"></a>

### Residual

A declared readout delta maps source state to a supplied diagnostic carrier with a reference value or target subset.

A zero residual characterizes the desired property only when that equivalence is proved. Sign, norm and units need additional structure.

See [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="term-residue"></a>

### Residue

Specify the algebraic readout and anchor: in a group, right residue p inverse times y forgets p, while retaining p restores y. Signed gap and centered sum are distinct digit readouts.

Equality can forget exact residue. Group side/order, base, width and orientation determine the inverse fiber.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="supp-retained-witness"></a>

### Retained witness

Keep the intermediate state, matching choice or derivation ticket that establishes a particular composition/attachment instance.

Existential endpoint projection can forget several witnesses while leaving ONE endpoint; witness identity is extra state if required.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="term-retention"></a>

### Retention

Information retention is described by the distinctions and observations recoverable from a representation, equivalently its equality kernel and admitted decoders.

Storage persistence, byte count, access cost and recoverability from separate data require their own contracts. Path dependence alone is not lossless memory.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views), [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="term-retraction"></a>

### Retraction

Supply L:X to Y and P:D to X with L(X) inside D and P after L equal to identity. L is a section; P returns its admitted lifted domain to X.

P may be lossy away from L(X). Reversible internal motion may yield an irreversible landed map.

See [Core section 14](core.md#14-lift-internal-operation-and-landing), [Operations section 9](operations.md#9-liftspinland).

<a id="term-reversal"></a>

### Reversal

Specify converse, endpoint/order reversal, role swap, negation, fixed-universe complement, reciprocal, reflection, projection or retained-seam reopening as separate typed operations.

Domains, inverses and fibers differ. Involution and commutation require proof rather than the word negative.

See [Core section 7](core.md#7-operations-are-typed-semantic-objects), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="supp-revision-identity"></a>

### Revision identity

A version token uniquely identifies a committed-state occurrence within the admitted run, rather than merely its payload bytes.

Freshness and atomic comparison are runtime assumptions. Equal content after intervening history need not be the same revision.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="supp-role"></a>

### Role

A named position in a specified relation or construction. Adding its type and interface behavior gives a port.

Roles and occurrences are separate; several roles may reference one occurrence only when incidence permits.

See [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports).

<a id="term-seal"></a>

### SEAL

Bind a claim/context/evidence package to fixed bytes, versions, verifier and scope for comparison and reuse. Output is the fixed package with identity/receipt data.

Hash equality supports byte identity under assumptions, not mathematical truth, authorship or permission.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="term-seam"></a>

### Seam

Retain which sites/occurrences matched, interface maps, orientation and compatibility witness. A live seam may additionally carry an unresolved interface obligation.

It is not necessarily a midpoint, zero or line. Local matching does not prove global injectivity, coverage or closure.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="supp-search-completeness"></a>

### Search completeness

Every admitted candidate is covered by a specified exact procedure or proof, allowing a complete fiber or exhaustive exclusion result.

A timeout or successful sample is not coverage; effective finite enumeration is one sufficient setting, not the only possible proof method.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Operations section 2](operations.md#2-solve).

<a id="term-section"></a>

### Section

A section L of P chooses an admitted preimage for each output with P after L equal to identity. It can supply a normal form for a larger fiber.

It need not recover the original; an effective selector is additional structure, and general existence can depend on choice assumptions.

See [Core section 14](core.md#14-lift-internal-operation-and-landing), [Operations section 9](operations.md#9-liftspinland).

<a id="supp-shortlex-order"></a>

### Shortlex order

Order finite operation words first by length and then lexicographically using a fixed alphabet order.

Shortest claims also name the source-pair set. Other cost orders may lack an attained minimum.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="supp-signature"></a>

### Signature

A supplied collection of sort names, operation names with ordered input/output sorts, and predicate names with arities; CORE uses a finite signature.

Names are syntax; interpretations and carriers must also be supplied. Finitary means finite arity, not automatically finitely many symbols in every other presentation.

See [Core section 2](core.md#2-what-is-primitive-and-what-is-defined).

<a id="supp-solve"></a>

### SOLVE

Given a typed relation, missing block and supplied assignment, return its exact joint completion fiber extensionally or with a proved complete symbolic description.

Admission, soundness, completeness and termination are separate requirements; finite enumerations plus exact membership suffice for the stated finite algorithm.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Operations section 2](operations.md#2-solve).

<a id="supp-solve-hypothesis"></a>

### SOLVE.hypothesis

Declare a rule family, experiments, evaluation law and syntax/semantic equality, then solve the consistency relation with the rule withheld.

ONE is unique within that family and record; this operator does not invent all mathematical laws.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Operations section 2](operations.md#2-solve).

<a id="supp-sort"></a>

### Sort

A named type with an explicitly supplied carrier and equality. Additional order, topology, algebra or units are separate structure.

Two names remain different sorts until an alias or conversion is declared, even if underlying sets coincide.

See [Core section 2](core.md#2-what-is-primitive-and-what-is-defined).

<a id="supp-soundness-implication"></a>

### Soundness implication

A stated implication says that acceptance by the named verifier on admitted data entails satisfaction of the scoped claim.

It may be proved, explicitly trusted or OPEN; hashing the evidence cannot decide which assurance holds.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="supp-state"></a>

### State

A state is an admitted element of the supplied state carrier containing every changing determinant required by its operations/receiver; fixed determinants belong to context.

If hidden time, history, randomness or external data affects the next step, the displayed state is not sufficient for the claimed deterministic function.

See [Core section 3](core.md#3-context-is-explicit-data-not-shared-intuition), [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports), [Core section 7](core.md#7-operations-are-typed-semantic-objects).

<a id="supp-state-replacing-observation"></a>

### State-replacing observation

Supply a state map M and readout Q and return (M(x),Q(x)).

It coincides with a passive observation only under the declared state/receiver preservation conditions.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles).

<a id="supp-strict-fold"></a>

### Strict FOLD

A sufficient question/operational FOLD that additionally merges at least two distinct admitted source states.

Loss outside the actual reached image is irrelevant; specify source equality and receiver.

See [Core section 9](core.md#9-fold-car-and-adapter-are-compatible-properties), [Operations section 5](operations.md#5-fold-including-lossless-cases).

<a id="term-target"></a>

### Target

The target is the exact readout, relation or property requested for preservation, attainment or exclusion; carry its source carrier/interpretation through transformations.

A changed coordinate with an unchanged expression may test a different property. Diagnostic zero means target satisfaction only under a proved equivalence.

See [Core section 1](core.md#1-the-purpose-and-the-mathematical-claim), [Core section 8](core.md#8-receivers-specify-what-counts-as-the-same-answer), [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses), [Operations section 4](operations.md#4-observe-project-car-and-adapter).

<a id="term-fiving"></a>

### Ten-cycle half-turn

On an oriented ten-cycle, write d=5h+r, with h in {0,1} and r in {0,...,4}. Adding five modulo ten preserves r and toggles h.

A lifted winding coordinate requires its own update law. This half-turn is distinct from a distinguishing-future search.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views), [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="supp-theory"></a>

### Theory

The definitions, admitted structures and laws of this version. The source class and preservation strength delimit a unification claim.

Not an additional physical law or universal success guarantee.

See [Core section 1](core.md#1-the-purpose-and-the-mathematical-claim).

<a id="term-tile"></a>

### Tile

A Tile is a capability artifact with its own finite hypothesis carrier, withheld role, experiments and commuting/closure receipt. Its interface declares inputs and outputs.

Tile(X) is a new type rather than automatically X; re-entry into a value port requires an adapter.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 13](core.md#13-finiteness-bounds-recurrence-and-dimensional-promotion), [Operations section 10](operations.md#10-promote-and-inherited-capability).

<a id="supp-topological-closure"></a>

### Topological closure

In a supplied topological space, the closure of A is the intersection of all closed subsets containing A, equivalently the smallest closed set containing it.

This standard operation is not fiber exhaustion, completed work or an authority transition.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-traceback"></a>

### Traceback

TRACEBACK.loss locates a supported lost distinction in a supplied diagnostic route. TRACEBACK.preimage computes the complete predecessor or trace fiber for a supplied operation route.

The two profiles have different inputs. Compatible predecessors need not identify an actual recorded history.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="supp-traceback-loss"></a>

### TRACEBACK.loss

Search a supplied ordered carrier of locations with exact diagnostic predicates for the earliest supported missing distinction/failed seam required by a reproducible failure.

The route and predicates bound the conclusion; it is not an unrestricted causal-origin theorem.

See [Core section 10](core.md#10-refinement-saturation-and-future-tests), [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="supp-traceback-preimage"></a>

### TRACEBACK.preimage

Given an operation word and terminal value, return the complete predecessor fiber or full trace-witness fiber; if the word is missing, supply its admitted carrier too.

It returns compatible predecessors under the supplied relation, not automatically an actually recorded predecessor.

See [Operations section 6](operations.md#6-fivefuture-and-traceback).

<a id="supp-transition-closure"></a>

### Transition closure

Every admitted successor of every state in a specified region stays in that region.

This is a conditional invariant-region property, not target exclusion or receiver acceptance by itself.

See [Core section 12](core.md#12-closure-and-frontiers-have-distinct-senses).

<a id="term-type"></a>

### Type

A named sort has a supplied carrier and equality. Role/operation signatures specify ordered sorts, units, orientation and interface refinements; a typed value pairs sort and element.

Equal numerals/cardinality do not equate sorts. Extra algebra, topology and conversions must be supplied.

See [Core section 2](core.md#2-what-is-primitive-and-what-is-defined), [Core section 4](core.md#4-values-occurrences-addresses-roles-and-ports), [Core section 7](core.md#7-operations-are-typed-semantic-objects).

<a id="supp-typed-value"></a>

### Typed value

The pair of a sort and an element of its carrier, subject to any separately declared admission predicate.

Value equality is evaluated in the declared sort and does not identify source occurrences.

See [Core section 2](core.md#2-what-is-primitive-and-what-is-defined).

<a id="term-typed-zero"></a>

### Typed zero

A zero is a particular numerical element, identity, residual reference, absence code or boundary tag with explicit sort and role; relate roles only through declared maps.

Missing assignment is not zero, NONE is not an empty-set output value, and diagnostic zero proves a target only under its theorem.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="term-unification"></a>

### Unification

Represent source mathematics through explicit typed relations and prove preservation of the stated structures, formulas, questions and operations.

A unifying purpose is broader than any one proved bridge; expression in a common notation does not solve every source problem.

See [Core section 1](core.md#1-the-purpose-and-the-mathematical-claim), [Core section 2](core.md#2-what-is-primitive-and-what-is-defined).

<a id="term-vacancy"></a>

### Vacancy

In an occupancy system, a vacancy is an explicit empty-site state variable. A one-token/one-vacancy swap exchanges their addresses and preserves the vacancy count.

Creation, deletion and multiple occupancy need another model. A geometric address encoding does not automatically represent an unknown value.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 17](core.md#17-a-connected-small-example), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).

<a id="supp-verification-predicate"></a>

### Verification predicate

A specified rule evaluates a claim/evidence/context instance as accepted or rejected, or has an explicitly partial domain.

The rule's implementation and applicability must be supplied; validation success is separate from its soundness proof.

See [Core section 16](core.md#16-evidence-seals-inheritance-and-atomic-successors), [Operations section 11](operations.md#11-seal-inherit-and-flick).

<a id="supp-window"></a>

### Window

An observation selected by an ambient coordinate map, footprint/mask and readout, with axis and boundary conventions retained.

Crop, reindex and contraction are different maps. Pixels inside a crop do not determine outside geometry or provenance.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles).

<a id="supp-witness-aware-composition"></a>

### Witness-aware composition

Retain the triple (source,middle,target) satisfying both component relations, adding ticket identities when required; endpoint projection forgets the middle.

ONE endpoint can correspond to MANY middle witnesses. Existential composition alone does not preserve path identity.

See [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Operations section 1](operations.md#1-execute-and-compose-by-semantic-kind).

<a id="term-zero"></a>

### Zero

Specify numerical value, algebraic identity, balanced residual, absence code, open capacity, singular coefficient, canonical receiver address or folded-fiber readout as separate typed roles.

These roles require separately typed maps; equal symbols do not erase a retained interior or identify a boundary with numerical zero.

See [Core section 5](core.md#5-relations-environments-and-complete-fibers), [Core section 15](core.md#15-residual-balance-pressure-and-negative-views).

<a id="term-zipper"></a>

### Zipper

Supply an active frontier/head and a local law matching boundary pieces, internalizing completed seams and exposing the next interface; retain incidence and required inverse lineage.

The name defines no universal algorithm. A partial construction can retain multiple fronts and unresolved debt under its model.

**Family definition:** its construction data and hypotheses are supplied per instance.

See [Core section 6](core.md#6-aperture-has-several-precise-profiles), [Core section 11](core.md#11-attachment-seams-and-retained-witnesses), [Core section 17](core.md#17-a-connected-small-example), [Operations section 3](operations.md#3-attach-and-exposed-boundary-composition).
