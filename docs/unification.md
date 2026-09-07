# Mathematical unification through relational presentation

This document gives a positive mathematical content to the proposed unifying
framework. Its first result is a faithful relational presentation: the stated
source mathematics can be expressed through typed relations without changing
the truth of its statements. Its further results explain when apertures,
operations and distinct source systems can share an interface.

These results use established mathematical constructions. RPRM's proposed
contribution here is their explicit organization around context, direction,
receivers, retained distinctions and continuation. A new name for a familiar
construction is not a claim of a new theorem. The usefulness of an individual
bridge comes from the questions and operations it makes available.

The principal result concerns finitary many-sorted first-order structures.
“Finitary” concerns the number of arguments of each symbol, not the number
of elements of a carrier. Infinite groups, fields and other supplied
structures can fall within this result. Effective finite solving is a
separate, narrower claim.

## U01. Faithful relational presentation

**Grade:** written mathematical proof, using ordinary set and first-order
semantics. U01 is a written proof. The accompanying Lean declarations prove selected
relation laws and fiber transport; the exact correspondence is listed in
[formal-proofs.md](formal-proofs.md).

### Data and construction

Let a supplied signature consist of sorts, constants, total function symbols
of finite arity, and predicate symbols of finite arity. For this release the
declared signature is finite. A structure M supplies a set M_s for each sort s,
a value for each constant, an interpreted function

    f^M : M_s1 × ... × M_sk → M_t

for each function symbol f, and an interpreted relation for each predicate.
Each sort has ordinary equality. Empty sorts are permitted when all supplied
interpretations exist; in particular a constant requires an element of its
sort. A nullary input product is the singleton containing the empty tuple.

For each sort s choose an injection e_s:M_s→Y_s and retain its image
E_s=e_s(M_s). Tagged copies Y_s={(s,x):x∈M_s} are one always-available choice.
This choice gives an explicit inverse d_s on E_s. More generally the inverse
on the image is the unique x with e_s(x)=y; this is mathematical existence,
not automatically an effective decoding procedure.

Define a relational target M^rel with:

* a unary image predicate E_s in each sort;
* a unary graph G_c={e_s(c^M)} for each constant;
* a graph G_f containing exactly the tuples
  (e_s1(x1),...,e_sk(xk),e_t(f^M(x1,...,xk)));
* for each predicate P, exactly the image tuples of P^M.

The target may have additional elements outside the E_s. No claim about
those elements is imported into the source. All graphs above are exact
images, not merely supersets containing the source tuples.

### Term translation

For a source term t of sort s, construct a formula V_t(v,y) that says that
y is its encoded value under the encoded variable assignment v. Every
introduced variable below is fresh and has the displayed sort. In the variable
clause, v(x) denotes the corresponding target object-language variable;
it is schematic notation for that variable, not an additional function symbol.

* For variable x, V_x(v,y) is y=v(x).
* For constant c, V_c(v,y) is G_c(y).
* For t=f(t1,...,tk), V_t(v,y) is

      ∃z1 ... ∃zk [
        E_s1(z1) ∧ ... ∧ E_sk(zk)
        ∧ V_t1(v,z1) ∧ ... ∧ V_tk(v,zk)
        ∧ G_f(z1,...,zk,y)
      ].

We may additionally conjoin E_s(y); it is already forced by this
construction on encoded source assignments. Nullary f uses its graph without
intermediate variables. The source constant case is the same construction.

**Term lemma.** For every source assignment a to the free variables, every
source term t:s, and every y∈Y_s,

    M^rel ⊨ V_t(ea,y)  iff  y=e_s(t^M(a)).

**Proof.** A variable follows from equality. A constant follows from its
singleton graph. For the inductive step each subterm formula, by induction,
forces z_i=e_si(t_i^M(a)); these witnesses exist. The exact function graph
then forces y to the encoded function value and includes precisely that
tuple. This proves both directions and uniqueness. A context with no
admissible source assignment has no instance of the assertion. ∎

### Formula translation

Translate an atomic equation t=u by introducing guarded witnesses y,z for
the terms and requiring y=z. Translate P(t1,...,tk) by introducing guarded
term-value witnesses and requiring the target predicate on them. A nullary
predicate retains its truth value. Translate Boolean connectives recursively.
Translate quantifiers as follows:

    (∃x:s φ)^rel = ∃x:s [E_s(x) ∧ φ^rel]
    (∀x:s φ)^rel = ∀x:s [E_s(x) → φ^rel].

Free variables are assigned encoded source values. Renaming bound variables
prevents capture. The formula translation is determined by the signature and
the selected encoding.

**Faithfulness theorem.** For every source first-order formula φ and
admissible assignment a to its free variables,

    M ⊨ φ[a]  iff  M^rel ⊨ φ^rel[ea].

**Proof.** For atomic equality the term lemma reduces the assertion to
e_s(x)=e_s(y), equivalent to x=y by injectivity. For a predicate the term
lemma and the exact image definition give the required biconditional.
Negation, conjunction and the other Boolean connectives preserve a
biconditional. For an existential quantifier, a source witness maps to an
image witness; an image witness has a unique source preimage, to which the
induction hypothesis applies. For a universal quantifier, the guard asks
exactly about those image witnesses, which are in bijection with the source
sort. This also proves the empty-sort cases. Structural induction completes
the proof. ∎

### What this establishes

The source's first-order statements survive a common relation-based
presentation. Operations are recoverable from their single-valued graphs;
equality and all declared predicates are preserved and reflected. A family
of source models is handled model by model by the same syntactic translation.
Consequently semantic validity over that family is equivalent to semantic
validity of the translations over its constructed image family.

This is a semantic preservation and reflection result. This version does
not claim a proof-theoretic conservative extension between unnamed calculi.
It also does not say that every arbitrary structure of the target signature
is an image model: a target model must satisfy the graph and image conditions
to recover the designated source. A full axiomatization and calculus
correspondence would be a further, clearly stated result.

The theorem applies to any supplied source of this kind. It does not
independently formalize every branch of human mathematics, interpret
unrestricted higher-order quantification, choose a foundational system, or
settle a statement whose truth is unknown in the source. Higher-order
objects can be supplied as additional sorts, but the intended function or
subset carrier and its evaluation/membership laws must then be provided.
Relational notation does not choose full versus restricted higher-order
semantics for the author.

## U02. Aperture fibers transport exactly

**Grade:** written proof for arbitrary sets and finitely many ports. A
general inverse-map formulation of fiber transport is formalized in
[Relations.lean](../lean/Relations.lean); the whole U01 translation is not.

Let R⊆∏_(i∈I) X_i, let each e_i:X_i→Y_i be injective, and let
R'=e(R) be its exact componentwise image. Choose supplied ports K⊆I,
vacant ports A=I\K, and environment η on K. Then the componentwise map

    e_A : Fib(R,K,η) → Fib(R',K,e_Kη)

is a bijection.

**Proof.** A member of the source fiber extends η to a row of R. Its image
therefore extends e_Kη to a row of R', so the map is defined. It is injective
because each component map is injective, including the unique empty
assignment when A is empty. A target fiber member comes from an image row
e(r), since R'=e(R). Equality of its supplied coordinates with e_Kη and
injectivity imply r|K=η. Its vacant coordinates therefore have a source
fiber preimage. ∎

Thus NONE, ONE and MANY are preserved at the full-completion receiver. If
a target relation has unrelated tuples outside the image, first restrict it
to all component images and require that restriction to equal e(R). Leaving
target vacant coordinates unguarded can create spurious completions.

For readouts ρ:F→B and ρ':F'→B', a claimed answer transport additionally
needs a map b with ρ'∘e_A=b∘ρ. To infer source answer uniqueness from target
answer uniqueness by this transport, b must separate the attained source
answers; injectivity on that attained answer set suffices. Injectivity outside
that set is unnecessary. A lossy answer decoder can
merge many source completions even when the completion encoding is faithful.

## U03. Transport of operations and composition

**Grade:** written proofs; selected relation identities and graph composition
are formalized in [Relations.lean](../lean/Relations.lean). Finite conformance checks exercise
separate small cases.

An operation bridge needs more than matching printed values. For injections
e_X:X→X' and e_Y:Y→Y', the exact contracts are:

| Operation | Source and required target behavior on source images |
|---|---|
| Total function f:X→Y | f'(e_X x)=e_Y(f x). |
| Partial function f:D→Y | e_X x belongs to D' iff x belongs to D; when enabled, f'(e_X x)=e_Y(f x). |
| Relation R⊆X×Y | (e_X x,e_Y y)∈R' iff (x,y)∈R, with image guards whenever other target tuples are present. |
| Finite nondeterministic N:X→P(Y) | N'(e_X x)=e_Y[N(x)], including equality at an empty successor set. |
| Finite normalized stochastic K | K'(e_X x,e_Y y)=K(x,y), and zero mass outside e_Y(Y). |

The last row is stated for finite sets and nonnegative normalized mass.
A general measurable-space extension needs specified σ-algebras,
measurability and kernel hypotheses; it is not obtained by replacing a finite
sum with an unspecified integral.

For functions and partial functions, substitution in the commuting equations
proves transport of two sequential steps. For partial maps the domain
biconditionals prove that both sides are enabled exactly together. Induction
then proves the result for every finite admitted sequence.

For nondeterministic transitions, distribute image over union:

    e_Z[ ⋃_(y∈N(x)) M(y) ]
      = ⋃_(y'∈N'(e_X x)) M'(y').

Exact image successor equality makes the index sets correspond. This proves
transport of composition; induction treats finite sequences.

For finite kernels, terms outside the middle image contribute zero. The
remaining sum is indexed by a bijective copy of the source middle carrier:

    Σ_y' K'(e_X x,y') L'(y',e_Z z)
      = Σ_y K(x,y)L(y,z).

Again this extends by finite induction. Preserving only which masses are
nonzero would not prove this equation.

For relations, the exact *image* relation composes correctly:

    e_(X,Z)(S∘R) = e_(Y,Z)(S) ∘ e_(X,Y)(R),

where the composite convention is first R and then S. The target intermediate
witnesses are confined to e_Y(Y). Membership on either side is equivalent
to the existence of y∈Y with xRy and ySz.

**Why middle-image guards are necessary.** Let source carriers be
X={x}, Y={y}, Z={z}, with R and S both empty. Let the target add a middle
element u outside the image and edges e_X(x) R' u and u S' e_Z(z).
Both target relations agree exactly with the empty source relations on
source-image endpoint pairs. Their unrestricted composite nevertheless
contains (e_X(x),e_Z(z)). Atomic agreement on images alone does not preserve
unrestricted target composition. Exact image relations, or explicit middle
guards, repair the statement.

## U04. A shared interface for two mathematical systems

**Grade:** derived written theorem, using the deterministic operational
factorization in [O05](operations.md#o05), with the induction given below.

Let systems i=1,2 have state carriers X_i, the same supplied operation
alphabet A, deterministic partial operations T^i_a, and observations
O_i:X_i→B. Supply a shared interface (Z,A,S_a,V), representations
C_i:X_i→Z and a readout V:Z→B. Require for every source state and operation:

    O_i(x)=V(C_i(x));
    T^i_a enabled at x iff S_a enabled at C_i(x);
    C_i(T^i_a(x))=S_a(C_i(x)) whenever enabled.

If operation names, parameters or answer types originally differ, supply
their explicit translations first; equal labels do not supply them.

**Theorem.** Whenever C_1(x)=C_2(y), the two systems give the same tagged
success/failure result and the same observation after every corresponding
finite operation word.

**Proof.** For the empty word the shared state and its decoded observation
agree. Assume shared retained states agree before a step. The two domain
biconditionals make both steps enabled or disabled together. Disabled
execution gives the same failure tag. When enabled the commuting equations
give equal shared successor states. Induction gives the claim for the word,
and the observation equation gives the final answer. ∎

If observations include intermediate states, apply the same argument to each
prefix. Trace, cost or resource equality follows only when those quantities
are included in the state or readout contract. This theorem does not equate
unobserved source structure.

If both C_i are bijections onto the same Z, then C_2^(-1)∘C_1 is an exact
source correspondence for these declared operations and observations.
If either is lossy, its fiber replaces an inverse source function. The
common interface may still be useful: it proves that distinct constructions
support the same specified questions and continuations.

### A complete two-source example

Let X_1=Z/4 with T_+(x)=x+1 and T_−(x)=x−1 modulo 4, and observation
O_1(x)=x mod 2. Let X_2={ab,bc,cd,da}, where each label denotes its
two-element subset of {a,b,c,d}, with T_+ moving one step forward in this listed
cycle and T_− one step backward. Define O_2(ab)=O_2(cd)=0 and
O_2(bc)=O_2(da)=1. The listing is the supplied cycle structure; mere subset
membership would not determine these operations.

Take Z={0,1}, S_+(z)=S_−(z)=1−z and V=id. Define C_i=O_i.
All operations are enabled everywhere. Both source operations flip the
displayed parity, so the commuting equations hold. Every word of length k
therefore displays initial parity plus k modulo 2 in both sources.

The shared interface forgets which member of a parity pair was present and
forgets the distinction between + and − at the endpoint parity receiver.
Each fiber contains two source states. It cannot answer which labeled subset
was visited, nor reconstruct a direction trace. Current labeled-subset identity
requires a refined state interface. A direction history requires the word or
trace to have been retained, or an extended state carrying that history:
even a full four-state endpoint cannot distinguish the empty trace from four
successive forward steps. A full four-state cyclic encoding also exists,
but it makes a different, stronger preservation promise.

## U05. Common records retain different operation kinds

Any supplied finite relation has an exact table of typed rows. Any supplied
finite partial function has its exact enabled graph. Any supplied finite
nondeterministic transition has its exact relation of possible successors.
Any supplied finite stochastic kernel has its table of masses, including
the zero-mass convention. These can share a typed record format with a
retained operation-kind tag, carrier identifiers and equality conventions.

**Representation fact.** If a complete table is retained with its
interpretation, decoding recovers the supplied object. This follows by
extensionality: relation membership, defined outputs, successor sets or
individual masses agree at every admitted input.

This fact does not identify their compositions. Boolean existential
composition of support relations, natural-number counting of paths, and
probabilistic composition by weighted sums give different results. Their
algebras must be retained. Nor does a finite table of arbitrary real masses
guarantee a finite exact byte encoding: the representation must specify
rationals, exact symbolic numbers, an oracle, or an approximation contract.
Our executable kernel checks use exact rational numbers.

## Three ordinary mathematical problems as apertures

These examples preserve their familiar laws. The additional interface
discipline exposes which variables, source distinctions and directions a
particular question needs.

### Addition in a group

For any supplied group G, retain the ternary relation R={(x,y,z):xy=z}.
With x and y supplied, z is unique. With x and z supplied, y=x^(-1)z
is unique. With y and z supplied, x=zy^(-1) is unique. These equations
follow by the appropriate left or right group cancellation; changing their
order in a noncommutative group can be wrong.

This rotates the aperture of one law. It does not replace the group law or
claim that all relations have group-like inverse fibers. In additive Z/5,
the same construction reads x+y=z modulo 5.

### Multiplication modulo 6

Retain R={(x,y,z)∈(Z/6)^3:xy=z}. With x=2 and z=2, the y-fiber is
{1,4}. With x=2 and z=1 it is empty. With x=1 and any z it is {z}.
Thus all three dispositions occur under the same stated relation as its
supplied context changes. A rule “divide both sides” without a unit
condition would erase valid ambiguity or produce a false answer.

### Linear equations

Let A:V→W be a supplied linear map over a field. If b has no preimage,
the solution fiber is empty. If Ax_0=b, then

    {x:Ax=b} = x_0 + ker A.

Indeed A(x_0+v)=b exactly when Av=0; conversely Ax=b implies
A(x−x_0)=0. This is an exact symbolic fiber, including infinite spaces;
its definition does not require enumerating those spaces. A source-complete
encoding preserving addition, scalar multiplication and A transports it
by U02. A receiver asking only A(x) identifies the whole solution fiber;
a receiver asking x does not.

For a finite example over F_2, A(x1,x2)=x1+x2 has fiber {(0,0),(1,1)}
at b=0 and {(0,1),(1,0)} at b=1. The two free-coordinate marginals are
both {0,1}; taking their product forgets the equation's correlation.

## What can go wrong with a proposed bridge

| Missing condition | Small hostile case | Consequence |
|---|---|---|
| Injectivity when preserving equality | Map two unequal source elements to one target element. | A false source equation becomes true. |
| Predicate reflection | Empty source predicate, target predicate true on its image. | A one-way inclusion is misreported as equivalence. |
| Image guards on quantifiers | Source has one element a; target adds b. | “Every x equals a” changes truth if target quantification is unrestricted. |
| Guards on intermediate witnesses | U03's extra middle element u. | Target composition invents a source path. |
| Partial-map domain reflection | Merge one enabled state and one disabled state. | A decoded value alone cannot predict failure. |
| Probability masses | Rows (1/4,3/4) and (3/4,1/4). | Equal support hides different outcome laws. |
| Retained witness receiver | Two different middle witnesses yield the same endpoints. | Existential projection cannot recover the path or its count. |
| Requested operation equation | A retraction exists but an arbitrary internal permutation is applied before landing. | The landed map can differ from the requested map or become many-to-one. |

These cases delimit stronger claims without negating the valid bridge
results. Each failed case identifies the missing structure that a revised
bridge must retain.

## A unification program with inspectable obligations

A growing unification atlas can represent source structures as nodes and
proved interpretations as edges. Every edge records its domain, operation
profile, statement fragment, receiver, image and inverse or fiber. Edges
compose when their intermediate types and guards match. Two different
routes are interchangeable only after their resulting interpretations
commute at the requested receiver.

This gives a concrete reading of “underneath mathematics”: a common semantic
account in which the represented mathematics remains valid, and omitted
roles, distinctions and transitions can be made explicit. It gives a
concrete reading of “more tools”: rotate a lawful relation question, expose
an exact fiber, find a lost distinction, build a sufficient quotient,
transport an operation, or prove that a proposed transport cannot preserve
the requested information.

It does not yet give one theorem saying every mathematical tradition has
been fully interpreted, or one decision procedure for every mathematical
question. Those are different claims with different obligations. RPRM is a relational framework for mathematical unification, with each
interpretation and preservation claim stated at its proved scope.

## Relationship to established mathematics

Relational presentations, operational semantics, sufficient quotients and
finite stochastic kernels are established constructions. The proofs here
state the precise versions needed by this framework. Scholarly sources and
formal-proof correspondence are documented in the repository's [references](references.md)
and [verification materials](verification.md). No priority claim follows from the notation or
from a successful implementation check.
