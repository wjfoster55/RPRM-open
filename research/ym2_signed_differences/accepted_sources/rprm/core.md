# RPRM: core definitions

A relational framework for mathematical unification.

For the connected exposition, begin with [Part I of the book](../MANIFESTO.md#part-i-the-object-the-question-and-what-must-survive).
Chapters [II.1](../MANIFESTO.md#ii1-relations-occurrence-and-exact-completion)
and [II.2](../MANIFESTO.md#ii2-what-a-representation-preserves) develop
complete fibers, recovery and sufficient representations. This reference
keeps the detailed definitions and section anchors used by the tools.

## 1. The purpose and the mathematical claim

RPRM aims to connect mathematical representations, methods and constructions
through the relations and operations they preserve. Existing mathematics is
the source of structures to retain, use and connect. The aim is to expose
assumptions that are often left implicit in a working representation—what is
known, what is missing, what is observed, what may happen next—and provide
tools for solving and transporting the resulting questions.

“Underneath” has a precise meaning in this account. We describe a supplied
mathematical system through typed carriers, relation instances, operations,
interfaces and observations. We then prove when this description recovers the
source's statements and behavior. [The unification theorem](unification.md)
constructs a faithful relational presentation of any supplied many-sorted
structure with a finite finitary signature at its stated scope. It explains exactly how ordinary
functions, predicates, composition and quantification survive that presentation.

An embedding of a familiar problem into this language may make a different
aperture or receiver available. That creates a useful question or method only
when its map, admission and correctness are supplied. Expressibility alone
does not solve the question or prove a cheaper algorithm. The framework's
unifying purpose and each proved unification bridge are distinct assertions.

The separate [relational-layer proposal](relational-layer.md) gives
“underlying” a physical research meaning: observable behavior may arise from
relations and continuations in a source model. Exact closure of a description
can leave that source nonidentifiable through the admitted observations.
It does not establish the existence of a physical substrate or make its
distinctions inaccessible to every possible intervention. Part I, section 7,
states this proposal before the gravity and black-hole applications.

The term **theory** here means the definitions, admitted structures and laws
in this version. It does not designate an additional physical law. “Unifies
all human mathematics” would require a specified class of source mathematics,
an interpretation for each member and a preservation result of the requested
strength. This version states a broad relational-presentation result and
separately scoped application bridges; it does not infer universal coverage
from the ability to write a tuple.

Four kinds of gap are kept distinct:

| Gap | What the framework can do |
|---|---|
| A missing value under a supplied law | Define and solve its complete fiber. |
| A missing distinction in a representation | Exhibit a separating observation and refine the representation. |
| A missing connection between representations | State the adapter and commuting obligations, then prove or refute them. |
| A missing mathematical law or theorem | Form a declared hypothesis space or proof obligation; do not claim it solved by naming it. |

Each preservation claim below has an explicit mathematical scope.
The rest of this document fixes the vocabulary needed to do that work.

## 2. What is primitive, and what is defined

This version uses ordinary sets, finite tuples, functions, relations, equality
and classical logic as its mathematical metalanguage. It is expressed within
that mathematics; it does not claim to have reconstructed logic or set theory
from an untyped primitive. The relation calculus itself can be presented in
other foundations, but an equivalence with such a presentation would need its
own proof.

A finite **signature** supplies sort names, operation names with ordered input
and output sorts, and predicate names with their arities. A **sort** `τ` has
an explicitly supplied carrier `|τ|` and equality. A typed value is the pair
`(τ,x)` with `x∈|τ|`. Distinct sort names remain different types even if their
carriers have equal cardinalities or happen to use equal underlying numerals.
An alias or conversion is declared explicitly.

Extra structure is supplied when used: an order, topology, metric, vector-space
law, group operation, units, probability law or encoding. A bare set does not
come with these structures by default. An **admission predicate** restricts
the carrier to the inputs accepted by a particular operation or problem.
Well-typed does not mean admitted, and admitted does not mean a relation has
a solution.

Empty carriers are allowed in the general relation calculus. An existence
theorem or algorithm requiring a nonempty carrier says so. The product over
no ports is the singleton `{()}`, not the empty set. Consequently a completely
specified valid relation instance has the singleton completion `ONE(())`.

The declaration order is:

```text
sorts and supplied mathematical structure
→ typed roles and relation instances
→ operations and their interpretation
→ observations and receiver interfaces
→ preservation conditions and certificates
→ versioned evidence and state-management contracts
```

This order prevents circular explanations such as “an aperture is what the
receiver receives” followed by “a receiver is what observes an aperture.”
Inductively defined structures and recursive programs remain possible when
their formation or execution semantics are separately specified.

## 3. Context is explicit data, not shared intuition

A **context** `Θ` is a versioned mathematical specification containing the
signature, carriers, equality relations, admitted states, interpreted
operations, observations, failure contract and any parameters on which a
claim depends. Its identifier is a reference to that data; the identifier
alone supplies none of the mathematical content.

The specification can be assembled in the dependency order above. A receiver
is defined from already declared observations and operations, then recorded
in the completed context. This avoids using the context record as an
unexplained self-definition of all its fields.

If time, remaining budget, history, external state, randomness, permissions or
source identity affects an operation, it must be represented in the state or
fixed by `Θ`. A change to a fixed field creates a new context version. Whether
an old result transfers depends on a proved adapter or unchanged dependency
projection. A later timestamp alone does not establish semantic compatibility.

**Example.** The decimal digits `0,…,9`, the cyclic group `Z/10`, and a digit
with positional carry can display the same ten symbols. Linear successor
fails at 9; cyclic successor sends 9 to 0; positional increment sends 9 to
digit 0 and carry 1. Their signatures or output types differ. A context that
records only the displayed symbol omits the distinction.

“Full context” in a theorem means this inspectable collection of mathematical
dependencies. Every required operation, hypothesis and source interpretation must be supplied.

## 4. Values, occurrences, addresses, roles and ports

An **occurrence carrier** consists of a supplied set `Id` of occurrence
identifiers, a type function `type:Id→Sort`, and a value assignment
`val(i)∈|type(i)|`. Optional incidence, ancestry, position and source maps are
additional structure on this carrier. Identifiers distinguish occurrences;
they do not infer semantic uniqueness, ownership or authenticity.

A **role** is a named position in a specified relation or construction. A
**port** is a role together with its type and declared interface behavior.
For a relation with a finite port set `I`, the assignment type is

$$
\operatorname{Asn}(I)=\prod_{i\in I}|\tau_i|.
$$

An occurrence can be assigned to a port through a typed map. Multiple roles
may reference the same occurrence only when the incidence model permits it.
Two different occurrences may have equal values. Forgetting their identifiers
is a projection whose fiber and receiver sufficiency must be checked.

An **address** is a coordinate in a supplied addressing scheme. It may be a
path in a tree, a tuple of grid coordinates, an ordinal in an enumeration or
an occurrence identifier. Converting one address system to another is a map;
equal printed addresses from different schemes do not establish that map.

The following equalities are distinct:

| Equality | Required data |
|---|---|
| Same occurrence | Equality in the supplied occurrence-ID carrier. |
| Same value | Equality in a declared value sort. |
| Same expression | Equality of retained syntax under a stated syntax equivalence. |
| Same denotation | Equality of interpreted values, relations or functions. |
| Same receiver behavior | Equality of the receiver's declared observations/futures. |
| Same artifact bytes | Equality of byte strings, or a hash check under its stated assumptions. |

For instance, two independently stored occurrences both valued 0 are not
interchangeable for an ancestry receiver. The values of `1+1` and `2` may be
equal while their expression trees and computation traces differ.

## 5. Relations, environments and complete fibers

A **typed relation** is a specified subset

$$
R\subseteq\operatorname{Asn}(I).
$$

The relation itself does not choose an input/output direction. A direction
selects which ports are supplied and which are requested. A partial typed
**environment** `η` assigns values to a subset `K⊆I`. Missing assignment is
not a distinguished numerical value, an empty collection or an error result.

For a vacant block `A=I\setminus K`, define the complete joint fiber

$$
\operatorname{Fib}(R,K,\eta)
=\{r|_A:r\in R,\ r|_K=\eta\}.
$$

When no completion exists, its disposition is `NONE`. A singleton is
`ONE(a)`. More than one completion is `MANY(F)` with the complete family `F`
or a proved exact description of it. These are statements about cardinality,
not about probability or whether a process has selected an outcome.

**Empty cases matter.** If `R` is empty, every fiber is empty. If all ports
are supplied and the resulting row belongs to `R`, the fiber is `{()}`.
If a deterministic query returns the empty set as its value, the output
fiber is `{∅}` and the answer is `ONE(∅)`. This is different from no solution.

**Joint correlation matters.** For `R={(0,0),(1,1)}`, the two-port fiber has
two members. Each one-port projection is `{0,1}`, but their Cartesian product
has four members. Reconstructing the joint fiber from those marginals admits
two false completions. Independent holes are justified only when a proved
factorization supplies that independence.

**Exactness and computation differ.** The displayed set defines the fiber
even when no algorithm for it is supplied. Complete effective finite carrier
enumerations and decidable relation membership permit exhaustive solving.
For an infinite carrier, a symbolic theorem can give an exact fiber. An
unfinished search remains unfinished even if it has found no witness.

## 6. Aperture has several precise profiles

The common idea is an explicitly selected interface at which a specified
question or continuation is exposed. This common description is not itself
a universal operation. Each use names one of the following profiles.

### 6.1 Relation aperture

A **relation aperture** is the record

$$
\mathsf{Apt}_{rel}=(\Theta,R,I,K,\eta,A,\rho),
\qquad A=I\setminus K.
$$

`R,I,τ` are retained, `η` is the supplied typed environment, and `ρ` is an
explicit readout on the missing assignment carrier. The full answer is the
fiber from Section 5; the requested answer set is its image under `ρ`.
The identity readout returns full completions. A lossy readout may merge
different completions into one displayed answer, so uniqueness of the display
does not establish uniqueness of the source completion.

Apertures can contain zero, one or several vacant ports. A port is one role;
an aperture is the complete question specification. A relation aperture
cannot silently omit the law, supplied coordinates, context or requested
readout and retain the same meaning.

**Rotation** selects another supplied/vacant partition of the same retained
relation. It is a change of question. The full relation row can be retained
through reindexing, but unique pointwise inversion requires singleton fibers
on the chosen domain. The relation `y=x²` over `{-1,0,1}` has a unique forward
answer and a two-member inverse fiber at `y=1`.

### 6.2 Observation or query aperture

An **observation aperture** supplies a probe family `Q_p:X→B_p`, a selected
probe `p`, an admitted source or source fiber, and the requested answer type.
For fixed `p`, its graph

$$
G_{Q_p}=\{(x,b):b=Q_p(x)\}
$$

turns the output question into a relation aperture. This is an explicit
encoding, not an assertion that observing a source and physically opening a
boundary are the same event.

A **window** is an observation selected by a footprint, coordinate map and
readout. Cropping, reindexing and contraction are different maps. A window
retaining a region's pixels does not automatically retain the region's
ancestry, geometry outside the footprint or all future edit behavior.

**Passive observation** returns `Q_p(x)` without changing `x`. A state-replacing
observation has an additional state map `M_p` and returns `(M_p(x),Q_p(x))`.
They coincide only if the specified state-update and receiver conditions make
them coincide. This distinction is mathematical; it asserts no physical
measurement theory.

### 6.3 Hypothesis or rule aperture

A **hypothesis aperture** supplies a hypothesis carrier `H`, experiment carrier
`E`, typed outcomes, a known evaluation relation or function `ev`, and an
evidence record. Its vacant role is `h∈H` satisfying that record. A rule is
therefore a value in an explicitly supplied rule carrier. This does not mean
the framework has generated every conceivable rule.

For deterministic finite `ev:H×E→O`, restriction by observed experiment/outcome
pairs gives exactly the consistent hypothesis fiber. If the true rule is not
in `H`, a singleton survivor need not be true of the world. A noisy observation
law requires its own stochastic or error model.

A syntax hole is a special case only after a grammar and interpretation are
supplied. A graph encoding of `ev` preserves the declared problem; it does not
choose the grammar, evaluation law or intended meaning.

### 6.4 Construction boundary and moving vacancy

An **exposed construction boundary** is a specified set of typed attachment
sites on a retained component, together with a compatibility predicate and
the data an attachment consumes, joins or exposes. It may be represented as
relation ports, but geometric edges and abstract value roles are different
types until that representation is supplied.

A **moving vacancy** is a state variable recording a currently empty site in
a declared occupancy system. In a one-token/one-vacancy swap, filling the
vacant site moves that token's previous site into the vacancy role. Thus the
token and vacancy exchange positions. This is a proved fact of that swap
operation. Creation, deletion or multiple occupancy requires a different
state model and need not conserve the number of vacant sites.

A **zipper head** is a named active frontier in a sequential construction,
with retained completed seams and an explicit step rule. It is not supplied
by drawing a gap. Its exact data structure and inverse requirements belong
to the chosen construction.

These profiles share typed interface discipline while retaining distinct semantics.
Connections between them require the stated encodings and preservation laws.

## 7. Operations are typed semantic objects

An **operation name** is syntax in a signature. Its **denotation** is a
declared mathematical object of one of the following kinds:

| Profile | Data and meaning |
|---|---|
| Relation | `R⊆X×Y`; every related output is a possible completion. |
| Deterministic partial map | `T:D→Y`, `D⊆X`; each enabled input has one output. |
| Finite nondeterministic transition | `N:X→P(Y)` with enabledness `N(x)≠∅`; possibilities carry no probability. |
| Finite stochastic transition | A normalized nonnegative mass row `K(x,−)` on finite `Y`; a law, not a selected realization. |
| Declared implementation | A program with specified input/output types, operational semantics and correctness obligation relating it to a denotation. |

A `k`-ary operation uses the ordered input product `X₁×⋯×X_k`. A nullary
operation is a constant or an admitted event with supplied context, not an
unexplained generator of arbitrary structure. An effectful operation includes
the affected state, emitted trace or effect description in its mathematical
output. Omitting a relevant effect changes the receiver promise.

**Definedness** is the operation's admission predicate. Deciding definedness
is an additional computational capability. A partial map can exist
mathematically without a decidable domain.

**Direction** identifies the requested leg of a relation or map. **Inverse**,
**converse**, **retraction**, **negation**, **complement** and **reversal** are
different definitions. **Identity operation** means `id_X(x)=x`; it does not
mean identity of every expression, occurrence or implementation trace.

Composition is profile-specific. Relations compose by an existential middle
witness; partial maps by sequential evaluation on the domain where both steps
are defined; finite stochastic kernels by summing the product of transition
masses over the middle carrier. [operations.md](operations.md) gives the exact
laws, retained-witness construction and counterexamples.

An expression tree describes how operations are composed. Equal denotations
can have different syntax, costs and traces. A rewrite is allowed for a receiver
only when its requested observations—including costs or effects if requested—
are preserved. An algebraic identity alone does not establish a performance
claim about an implementation.

## 8. Receivers specify what counts as the same answer

A **question receiver** is an indexed family of typed observations
`(Q_p:X→B_p)_{p∈P}` on an admitted source. Two states are equivalent for it
when all those observations agree. `P` may be a supplied finite set or another
explicitly delimited family. A finite family has a tuple-valued combined
observation. No decoder complexity follows from the family alone.

An **operational receiver** additionally supplies operation names and
parameters, transition profile and denotations, observation timing, failure
semantics, allowed future language or horizon, and any retained trace/effect
observations. It determines which continuations can distinguish states.

The receiver is the question specification. A **representation** `C:X→Z` is
the actual retained data. An **observation** `O:X→Y` is one readout. A
**decoder** maps retained data to a requested readout. These objects are not
interchangeable, even if a small example uses the same map for two roles.

For a representation, replace `Z` by the reached image when discussing unique
decoders. Its kernel relation is `x~_C y` iff `Cx=Cy`. Its source fiber at a
reached value may contain one or many states.

For a question `Q:X→Y`, the central factorization theorem remains:

$$
\exists g:C(X)\to Y,\quad Q=g\circ C\text{ on }X
\quad\Longleftrightarrow\quad
Cx=Cy\Rightarrow Qx=Qy.
$$

The decoder is unique on `C(X)`. This characterizes exact sufficiency, not
computability, physical accessibility, byte size or speed. A receiver can
require every source distinction, in which case no strict loss is possible.

## 9. FOLD, CAR and ADAPTER are compatible properties

A **CAR** is a bijection between a declared source and its admitted image,
with the inverse and the transported relevant structure specified. For a
function `C`, this is equivalent to injectivity onto its reached image. It
need not be surjective onto a larger displayed ambient codomain.

A **question FOLD** is a representation together with proved sufficiency for
a named question receiver. It may be injective. A **strict FOLD**, or **lossy
FOLD**, is a noninjective such representation. This inclusive definition
repairs the case where the canonical receiver quotient preserves every state.

An **operational FOLD** additionally supports the retained operations with
matching domains and the required successor/trace semantics. For deterministic
partial operations it requires agreement on observations, enabledness and
compressed successors within every fiber. Equality of present and one-step
observed answers is weaker. Even equality of all future observed answers does
not guarantee exact updating of an arbitrarily more detailed summary.

An **ADAPTER** is a typed translation with a declared preservation contract.
The contract says whether the map is invertible, sufficient for questions,
sufficient for operations, approximate under a supplied metric, or only a
candidate. A correct type signature alone does not prove that contract.

These are not mutually exclusive kinds of magic operation. An injective map
can be both a CAR and a sufficient FOLD. A lossy map can be an ADAPTER and an
operational FOLD. A map may be sufficient for one receiver and fail another.

A storage system promising later source recovery must retain a retrieval route
when source distinctions are omitted from its working representation. The **mathematical quotient** and the **storage package
with a recovery route** are separate objects. The full storage system has not
lost information that remains in its cold store. Availability, provenance and
cost of that store need their own assumptions.

## 10. Refinement, saturation and future tests

Given `C:X→Z` and a separating question `Q:X→B`, the representation

$$
C'(x)=(C(x),Q(x))
$$

has kernel `ker C∩ker Q`. It is the **coarsest refinement** retaining the old
representation and that question: any representation decoding both has a
kernel contained in this intersection. This statement concerns information
partitions; it does not choose unique byte labels or an optimal implementation.

**REFINE** means a specified refinement with a declared target. Adding a
question repairs that question. An operationally stable result requires
checking the transition congruence again or continuing a proved closure
algorithm. The first repaired output can expose a later separating future.

**FIVE.future** is a distinguishing-future search within a declared operational
receiver and witness order. In the finite deterministic profile with an
effectively given finite alphabet, shortlex orders finite words by length and
then a fixed alphabet order. The shortest witness is well-defined whenever
one exists. The n-state theorem bounds it by n−1 for the tagged partial-system
profile in [O07](operations.md#o07). Changing the cost order requires its own minimum-existence
conditions. An infinite family with costs `1/n` need not have a cheapest
distinguishing experiment.

**TRACEBACK.loss** locates an earliest lost distinction within a supplied
ordered transformation/evidence trace. It is not a future experiment.
It has a different input and witness type from distinguishing-future search.
A ten-cycle half-turn is a separate arithmetic operation, defined in the glossary.

**Receiver saturation** means that a specified additional observation family
introduces no distinction beyond the retained representation, or that a
specified operational refinement has stabilized. Which meaning is intended
must be stated. Saturation is relative to the source and receiver family; it
does not mean that all possible future questions have been exhausted.

## 11. Attachment, seams and retained witnesses

Suppose component states `x∈X` and `y∈Y` have boundary observations `b_X(x)`
and `b_Y(y)`. Supply a compatibility relation `M` and any interface maps.
The admissible attachment carrier is

$$
J=\{(x,y,m):m\text{ is a declared witness that }M(b_X(x),b_Y(y))\}.
$$

When compatibility is a Boolean predicate with no extra witness data, retain
`(x,y)` and the precise matched-interface record. When several witness choices
matter, the witness coordinate must remain. A **seam** is that retained record:
which occurrences/sites matched, through which maps, with what orientation,
and which agreement was checked. It is not automatically a midpoint, a zero
or a geometric line.

**ATTACH** returns a constructed component together with enough lineage to
recover the agreed inputs or the complete forgotten fiber. Whether attachment
is invertible depends on that output. Erasing middle witnesses, equal-valued
occurrence identifiers or unused boundaries can make it lossy.

**Expose** and **hide** select the next interface. Hiding is a projection; it
does not destroy the underlying seam when that seam is retained elsewhere.
Replacing a compound by an external summary requires a separate sufficiency
proof. Compatibility at one seam does not establish global consistency or
closure of the whole construction.

In a geometric gluing problem, additional assumptions include the topology,
maps on the overlap, agreement of formulas and any injectivity/coverage claims.
The retained-interface construction supplies a place to state those
obligations. It does not derive a gluing theorem from a diagram alone.

## 12. Closure and frontiers have distinct senses

| Term | Exact meaning in a declared context |
|---|---|
| Transition closure | Every admitted successor of a state in a specified set remains in that set. |
| Search completeness | Every candidate in the declared search carrier has been covered by the decision procedure or proof. |
| Invariant closure | Initial coverage, preserved invariant and target conclusion cover every admitted finite continuation. |
| Receiver closure | A specified observation/operation quotient is sufficient or stable. |
| Boundary completion | All required interface/seam obligations for a specified compound are discharged. |
| Topological closure | The closure in a supplied topology; an established mathematical operation with its own definition. |
| Workflow closure | The task or audit obligations have a complete recorded disposition. |

A **frontier** is an explicitly identified boundary of current coverage. It
may be a set of unvisited graph nodes, open attachment sites, unresolved proof
obligations or exit states from a verified enclosure. These are typed sets,
not interchangeable metaphors.

**Frontier localization** has a useful exact form. If all states in a covered
region fail a target and every first departure crosses a listed frontier,
then any later target-reaching route must continue through that frontier.
This is stronger than saying “the search timed out” and weaker than proving
the target unreachable everywhere. The entry/exit coverage and no-target
interior statements must be proved.

An **EVENT** is a tagged transition or unresolved seam occurrence in a declared
state model. An event can be fully described and still fail the stable-state
admission of its intended output type. A `STATE→EVENT→STATE`
notation records transition admission; it does not deny that an intermediate
value exists. A physical event interpretation requires an additional model.

A chosen checkpoint, a sufficient certificate's failure, a true invariant
failure and the last possible continuation are different boundaries. A
failed sufficient check may leave the property open rather than false.
An exact counterexample can establish failure. An altered path can be admitted
through a separately checked seam.

## 13. Finiteness, bounds, recurrence and dimensional promotion

Four quantities must not be interchanged:

1. The cardinality of a state carrier.
2. The size of a finite description of a carrier or map.
3. A spatial bound in a supplied metric.
4. The length or cost of an admitted operation horizon.

`[0,1]` is bounded in its usual metric but has infinitely many points. The
rule `x→min(1,2x)` there has arbitrarily late distinguishing observations.
Thus finite description and boundedness do not imply finite-state closure.
Conversely a fixed finite state machine can admit arbitrarily long finite
words whose behavior is covered by an induction theorem.

Notation such as `[1/2,Ω_R]` can describe an ordered numerical enclosure.
It does not define an arbitrary carrier: an arbitrary typed set
may have no order, no half and no greatest element. A literal interval requires
an ordered numerical carrier. A “last structurally new case” requires a
specified equivalence and a proved stabilization or recurrence criterion.

A **recurrence** is an explicitly stated relation between stages, with initial
conditions and a preservation proof. A few repeated observations do not
establish it for every future stage. A proof may quantify over every finite
stage without asserting that an infinite computation is physically performed.

**Dimension** always names its definition: vector-space dimension, number of
ports, embedding dimension, number of independent coordinates in a specified
model, or fixed-width addressing capacity. These are not equal merely because
their displayed numbers match.

**Promotion** creates a compound or next-stage type through a declared
constructor, then exposes it through a specified interface. A complete
`Tile(X)` is not automatically a value of `X`. A re-entry map must explain
which distinctions it preserves and which it forgets. Scaling an existing
shape, adding independent coordinates and increasing its topological
dimension are different operations.

## 14. Lift, internal operation and landing

Supply a lift `L:X→Y` and a partial landing `P:D_P→X` with
`L(X)⊆D_P` and `P(Lx)=x`. Here `L` is a section of `P`, and `P` retracts
its domain onto `X`. The lift is injective, but the landing may be lossy.

For an internal operation `H:D_H→Y`, the landed operation is

$$
T=P\circ H\circ L,
\quad D_T=\{x:Lx\in D_H,\ H(Lx)\in D_P\}.
$$

**LIFT–SPIN–LAND** is this pattern with the intended target and preservation
obligation supplied. “Spin” names the declared internal operation, not a
universal rotation. To implement a requested source operation `F`, prove
`D_T=D_F` and `T(x)=F(x)` on that domain, or prove precisely the weaker
receiver equality requested.

An invertible internal operation need not give an invertible landed map.
Take `X={0,1}`, `Y={0,1,2}`, inclusion `L`, and `P(0)=0,P(1)=1,P(2)=0`.
Let `H` swap 1 and 2. Although `P∘L=id_X` and `H` is an involution, the
landed map sends both source states to 0. The lost fiber must be retained or
accepted at the named receiver; calling the internal step reversible does
not repair it.

## 15. Residual, balance, pressure and negative views

A **residual** is a declared readout `δ:X→D` with a specified reference value
`0_D` or target subset. A statement such as `δ(x)=0_D` is equivalent to a
desired property only when that equivalence is proved. Residual sign, norm
or magnitude needs the corresponding order, metric or algebra on `D`.

**Balance** means satisfaction of a specified equality or conservation law.
**Zero** can be a numerical element, identity, residual value, missing
observation code or boundary tag; those uses have different types. Missing
assignment is never converted into numerical zero without a declared map.

**Half** is a coordinate or value relative to a declared unit. On one binary
axis, centering maps `0,1` to `−1/2,+1/2`. On two unit-total complementary
lanes, `(1/2,1/2)` has difference zero. Two coordinate occurrences of `−1/2`
are not their sum unless a summation operation is supplied. For `k` equal
unit-total lanes, the balanced coordinate is `1/k`.

**Pressure** has no universal scalar definition in this core. A model may
define a constraint count, residual norm, live-fiber cardinality, resource
deficit or another quantity, with units and intended use. These are different
pressure readouts. `log₂|F|` on a finite nonempty candidate fiber is an
information-capacity measure; it is not Shannon entropy without a probability
law and does not apply unchanged to an empty or infinite fiber. No pressure
minimization law is inferred for every RPRM construction.

**Retention** has an exact information reading through the distinctions kept
by `ker C`. Storage size, access cost and persistence are extra implementation
properties. **Conservation** requires a named quantity and an equation proved
under the stated operation. Reusing that word does not connect information,
physical energy and a count of vacancies.

An **alternative view** is a separately specified transformation or projection. Negation, complement in a fixed universe, order reversal, role swap,
reflection, reciprocal, relation converse and lossy projection each have their
own domain and laws. Some are involutions; some are partial; some are lossy.
Their composition order is retained. Two involutions need not commute.

## 16. Evidence, seals, inheritance and atomic successors

A **claim** is a statement with hypotheses, context, scope and evidence grade.
A **certificate** is a witness in a specified format with a separately stated
verification predicate and soundness implication. A **receipt** records the
subject, method, inputs, result and dependencies of a check. A checker's
successful output does not prove its soundness merely by existing.

A **seal** binds a claim/context/evidence package to fixed bytes and versions.
Hash equality is evidence of byte identity under its assumptions. Mathematical
truth, source authenticity and permission are separate predicates. A local
content hash alone does not identify an author or grant reuse authority.

**INHERIT** reuses a valid result when its complete relevant dependencies have
not changed. [O13](operations.md#o13) proves selective recomputation on a
fixed finite acyclic evaluation graph with complete read masks and admitted
old/new inputs. It does not certify the completeness of arbitrary masks or
the semantic validity of an untrusted old cache.

**FLICK** is an atomic state-store contract: construct a candidate from a
specific valid parent version, validate the exact candidate/context, and
install it only if the required parent version is still current. A failed
attempt performs no state-store update; it does not restore a stale parent
over an intervening committed successor. Version tokens must prevent a stale update from
being accepted after an intervening history relevant to the receiver. A
content hash that repeats after an A→B→A sequence may not capture that history.

The state-store contract in [O14](operations.md#o14) is a computational
specification with separately stated atomicity assumptions. It supplies no
additional mathematical theorem about the stored claim.

## 17. A connected small example

Take four tagged sites in a line, values in `{0,1}`, and exactly one vacant
site. State retains the site IDs, occupied values and the vacancy index.
There are `4·2³=32` states. The fixed move alphabet consists of the three
undirected adjacent edges `(0,1)`, `(1,2)` and `(2,3)`. A move is enabled
exactly when its edge contains the vacancy; it swaps that vacancy with the
other endpoint's payload. An enabled move has one exact successor; repeating
the same edge reverses it.

At each move, a relation aperture asks for the new assignment under the swap
law. The construction boundary is the adjacent pair; the seam record retains
their IDs and the selected swap. The vacancy moves opposite the selected
payload. This establishes a local conservation of one vacancy for this carrier.

Now choose a question receiver observing only the count of payload value 1.
Every swap preserves it. A summary by that count answers this question.
It cannot generally decide which adjacent move is enabled because it forgets
the vacancy's position. Adding the vacancy index gives the summary
`C(x)=(count(x),vacancy(x))`. This is an exact operational FOLD for the
declared count receiver and fixed edge alphabet: enabledness depends only on
the vacancy index, the count is unchanged, and the new vacancy is the other
endpoint of the selected edge. Induction therefore gives all finite-word
count answers and tagged failures. It still need not recover the payload
arrangement for a receiver that later asks which value moves. Adding that
observation requires a new sufficiency check and may refine the state again.

If an operation asks to create another vacancy, it leaves the one-vacancy
carrier. This is an explicit new operation/type boundary, not a failure of
the swap conservation theorem. A different occupancy model can admit it,
with a newly proved rule.

Finally, a recorded sequence of swaps can be compiled into a macro operation.
Its endpoint permutation does not identify the sequence: swapping twice gives
identity while retaining a two-step trace. A trace receiver needs that history;
an endpoint-only receiver can ignore it. The macro can be reused after checking
the same admission and receiver contract, and installed as a checked successor
through the separate state-store rule.

The conformance examples implement these distinctions on a declared finite
carrier. They demonstrate how the vocabulary supports one connected mechanism
instead of requiring the reader to infer links between disconnected metaphors.

## 18. Evidence and document map

Definitions specify objects and conventions. An established theorem refers to
existing mathematics; a derived synthesis composes stated results; a finite
test establishes only the declared checked cases. A conjecture is unproved,
and an interpretation is not a proof premise. The written arguments in these
documents keep those distinctions. Formal proofs and executable checks have
their separate coverage in [verification.md](verification.md) and
[formal-proofs.md](formal-proofs.md).

[operations.md](operations.md) gives the operator laws, their proofs and
counterexamples. [unification.md](unification.md) proves relational presentation
and exact bridge results. [glossary.md](glossary.md) defines the vocabulary used
here. A new receiver or mathematical class can require a new bridge; existing
proofs retain their original hypotheses.

## 19. The affine aperture chart

**Grade: established elementary algebra, with written proof.** Work over the
reals and declare an admitted subset for each port of

$$
x=(1-u)L+uR.
$$

The four single-port fibers are as follows. Intersect every generic answer
with that missing port's admitted set.

| Missing port | Nonzero coefficient | Zero coefficient |
|---|---|---|
| `x` | `{(1-u)L+uR}` before admission. | There is no denominator. |
| `u` | `{(x-L)/(R-L)}` when `R≠L`. | When `R=L`, all admitted `u` if `x=L`; otherwise none. |
| `L` | `{(x-uR)/(1-u)}` when `u≠1`. | When `u=1`, all admitted `L` if `x=R`; otherwise none. |
| `R` | `{(x-(1-u)L)/u}` when `u≠0`. | When `u=0`, all admitted `R` if `x=L`; otherwise none. |

**Proof.** A nonzero coefficient can be divided out. A zero coefficient leaves
an equation independent of the missing variable, either true or false. The
fiber is then respectively the entire admitted missing carrier or the empty
set. An entire carrier can itself be empty, singleton or larger. ∎

Thus `L=0,R=2,x=3` has no completion if `u` is restricted to `[0,1]`, despite
its algebraic answer `3/2`. Equal endpoints with `x=L` retain every admitted
parameter. Three supplied values therefore need not determine one fourth.

For oriented endpoint pairs with `L≠R` and `L'≠R'`, let
`q(u)=(1-u)L+uR` and `q'(u)=(1-u)L'+uR'` on the same admitted parameter
carrier `U`. Both maps are injective. The map `q'∘q⁻¹` is a CAR from `q(U)`
to `q'(U)`, with inverse `q∘(q')⁻¹`. It retains `u` while transporting the
endpoint values. A collapsed endpoint pair, or a change of admitted parameter
carrier without a matching restriction, does not satisfy this contract.

This is one four-port law. Relations with other arities and laws remain
within the general completion definition.
