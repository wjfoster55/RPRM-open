# RPRM agent handbook

**Version 6 — relational-layer and application-scope revision.**

This is a self-contained guide to the core reasoning contract. It defines
the vocabulary needed to frame, solve, audit and explain an RPRM problem.
It does not contain every domain theorem or turn an agent into an arbitrary
theorem prover. A domain pack supplies its own laws and evidence. Reading
this handbook is enough for the core comprehension assessment; no private
context or companion file is assumed by that assessment.

## Reading map

Sections 1–6 define relations, loss, operations and faithful transport.
Sections 7–9 connect the conceptual vocabulary to complete worked examples.
Sections 10–13 state the arithmetic, probability, physical and computational
scopes needed to interpret applications. Section 14 gives a working format.
The core examples and mathematical rules used here are explained here;
long domain proofs and software installation instructions belong to their
separately supplied artifacts. When those artifacts are absent, report that
limit instead of inventing their contents or execution status.

## 1. Purpose and foundations

RPRM stands for **Relational Pressure Retention Model**. Its name originates
in the motivating physical proposal about underlying relations, pressure
and retention; it remains the framework's name. Each physical model must
define those terms through its own variables, units and laws. Section 12
states the relational-layer proposal and its observation limits.

RPRM is a relational framework for mathematical unification. It describes
existing mathematics using explicit types, relations, operations, interfaces
and observations, then asks what a representation preserves. It uses
ordinary sets, functions, equality and logic as its metalanguage. It does
not establish a new physical law merely by redescribing a system.

A unification claim names the source class and a faithful interpretation.
For a supplied many-sorted structure with a finite finitary signature,
functions can be represented by their graphs and predicates by relations.
Injective sort encodings, preservation and reflection of atomic statements,
and quantifiers restricted to the encoded images allow a structural-induction
proof that translated first-order statements have the same truth values.
This is semantic preservation. It supplies neither a decision procedure for
every theorem nor a faster solver for every instance.

Do not assume a concept is new because its RPRM name is new. Give ordinary
mathematical names and attribution where applicable. Treat proofs, tests,
conjectures and interpretations as different evidence grades.

## 2. The problem record

Before operating, write the following record in ordinary language or a table:

1. **Carrier and context:** which objects are admitted, with what equality,
   units, bounds, parameters and side conditions?
2. **Ports:** which named roles have values, what types do they have, and
   which are missing?
3. **Law and operation:** which relation holds, or which update can act?
   Specify direction and enabledness.
4. **Receiver:** which observations, questions or later continuations must
   the answer preserve?
5. **Fiber:** what are all compatible completions/preimages? Is an inverse
   or retraction actually available?
6. **Closure and evidence:** why is coverage complete, what hostile case
   could break the claim, and what has been proved or merely tested?

A **sort** gives a named carrier and equality. Two ports may contain equal
numerals while having different types. A count and a duration need an
explicit unit-aware operation to yield a rate. An **occurrence** additionally
has identity and context: two equal-valued measurements or two uses of one
symbol need not be the same event or shared variable.

## 3. Relations, apertures and complete answers

A relation is a set of admitted joint rows. An **aperture** chooses which
ports are supplied and what is requested. Its completion fiber contains
exactly the missing-port tuples that extend the supplied values to a lawful
row. Changing the aperture changes the question; it need not change the law.

For `a+b=c` on `{0,1,2,3,4}`, ordinary addition without wrap, `c=3` has four
joint completions `(0,3),(1,2),(2,1),(3,0)`. Supplying `a=4,c=0` has none in
that carrier, although another carrier admitting negative integers would
change the answer. Supplying all ports yields either the singleton empty
tuple `{()}` for a true row, or the empty set for a false row.

Use these dispositions precisely:

- **NONE:** the complete admitted fiber is empty.
- **ONE(value):** the complete fiber has exactly one member.
- **MANY(family):** the complete fiber has several members, represented
  completely and at the declared scope.
- **OPEN:** a needed law, coverage argument, computation or other obligation
  remains unresolved. An unfinished search is OPEN, not NONE.
- **OPEN_NEW_CARRIER:** continuing requires a new type, coordinate, operation
  or receiver contract; it must be declared rather than silently introduced.
- **REJECT:** a well-formed proposed certificate/map fails its obligation.
  **Admission error** means malformed or out-of-carrier input.

A witness search that found two solutions without proving completeness has
found at least two witnesses; it has not returned the complete MANY fiber.
A complete infinite example is `a+b=c` over integers with fixed integer c:
`{(t,c-t): t is an integer}`. Every generated pair satisfies the law; every
solution has t=a and therefore appears in the family. Those two directions
establish correctness and coverage without enumerating an infinite list.
A MANY fiber can nevertheless settle a requested readout: if every member
has the same readout, that readout is determined. An empty fiber is not a
vacuously determined answer about an actual source whose membership is unknown.

Keep missing ports joint. From `{(0,0),(1,1)}`, the two marginal sets are each
`{0,1}`; their product incorrectly adds `(0,1)` and `(1,0)`. Correlation is
structure. In a composed relation `R:X↔Y`, `S:Y↔Z`, the middle witness must
be the same `y`. The endpoint relation forgets which middle witness was used.
Store triples `(x,y,z)` if the receiver needs that identity or multiplicity.
Guard `y` to an encoded image when translating between different carriers.

## 4. Representations, CARs, folds and questions

A representation is a map `C:X→Z`. Its fiber over `z` is all `x` with `C(x)=z`.
The **receiver** is the declared family of questions or behaviors to preserve.
For one question `Q:X→B`, an exact decoder on reached values exists exactly
when `C(x)=C(y)` implies `Q(x)=Q(y)`. Then `Q=h∘C`; `h` is uniquely determined
on the reached image. Unreached target values may require extra conventions.

A **CAR** is invertible between its stated source and target carriers.
An encoding `E` with retraction `D` satisfying `D∘E=id` is injective and
recovers every source; `E∘D=id` additionally requires that the target has no
extra states outside the encoded image. A **FOLD** or lossy **ADAPTER** may
merge sources while faithfully preserving a stated receiver. It retains an
explicit preimage family or a reopen route when later questions might need it.
The word “adapter” is not evidence that its preservation equation holds.

Example: `C(n)=n mod 2` preserves parity but cannot recover an arbitrary
integer. A representation retaining `n` preserves parity and more. A short
label may require expensive computation to obtain; label size, access cost,
running time and retained-information order are distinct quantities.

To repair a failed question, use `C'(x)=(C(x),Q(x))`. This is the least
informative refinement retaining both old `C` and the requested `Q`, up to
mutual definability on their images. For a finite carrier, a reusable repair
tag needs at least the maximum number of distinct Q-values in any old fiber.
Different old fibers can reuse the same tags because C already separates them.
The bound is attained by assigning a distinct tag to each Q-value separately
inside each old fiber and reusing tags between fibers; decode using the pair
of old summary and tag. For an empty source, the empty tag carrier suffices.

A usable reopen record identifies the source bytes or reconstructing generator,
its exact version, the admitted context and map, and a way to recover the
forgotten fiber. A hash can bind that source version but does not supply
missing bytes or prove the generator's law. Retained witness triples are one
simple complete record for a finite relational composition.

## 5. Operations and future preservation

Separate a relation, a function, a partial function, a set-valued transition
and a stochastic kernel. A converse relation always reverses pairs; it is a
single-valued inverse only under additional conditions. A partial operation
also has an exact enabled domain.

For a deterministic partial machine with observations `O`, operations `T_a`
and summary `C`, an exact quotient preserving updates and observations exists
on the reached summary states exactly when, for every `C(x)=C(y)`:

1. `O(x)=O(y)`;
2. each `T_a` is enabled at both or neither;
3. when enabled, `C(T_a(x))=C(T_a(y))`.

These conditions make quotient definitions independent of the chosen fiber
representative. Induction then preserves execution definedness and final
observations for every finite action word. A present-only observation match
does not imply them. A failed execution is tagged separately from a successful
execution returning a value that happens to look like “failure”. Failure
position or a full history must be added if the receiver needs them.

The **future quotient** merges exactly states with equal tagged observations
after every finite word, including the empty word. For the finite algorithms,
both the state set and action set are finite and supplied as complete tables;
observation and transition comparisons must be exactly decidable. Such a
machine admits partition refinement: start from present observations, repeatedly split by
enabledness and successor classes, and stop when stable. To retain an old
summary too, start from `(C,O)`. This produces the coarsest stable refinement
of that initial partition. Refining for only one question need not stabilize
all later operations.

The shortest separating word can be found by breadth-first search on pairs
of states, including an absorbing failure state. Order outgoing actions by
the declared alphabet order. The first distinguishing path is shortest, and
lexicographically least among those shortest paths. Complete exhaustion means
NONE; exhausting a time budget means OPEN. A nonempty n-state machine has a finite distinguishing bound of n−1.
To see the count, let r be the number of distinct source observations.
Adding failure gives n+1 completed states and r+1 initial blocks, because
FAIL differs from every OK value. After j refinement rounds, two states
share a block exactly when their answers agree through words of length j,
by induction on the first action. Every strict round increases the block
count, so there are at most n−r≤n−1 strict rounds. A nonsplitting round is
stable and no later distinction appears; an implementation may perform
one extra comparison to detect that stability. Empty alphabets still have
the empty word and therefore still distinguish present observations.

For a nondeterministic quotient, compare the **sets of successor summary
classes** in each source fiber, with observations. Counts are different from
sets. For a stochastic quotient, compare the **total probability mass into
each summary class**, with observations. Equal supports or equal expected
values alone do not ensure equal output laws. For a supplied homogeneous finite Markov model, the exact block-mass
condition also preserves finite block-path distributions for every initial
distribution; section 11 states and explains that stronger result. Hidden
source paths and more general interventions are additional receivers.

Future answers and updating a chosen summary are distinct obligations.
For example, take p→p, q→r, r→r under one total action, with every observation
zero. Let C(p)=C(q)=0 and C(r)=1. Every future answer is zero, so C answers
the entire observation receiver. Yet summary 0 has successors 0 and 1,
so its own update is not well defined. The canonical future quotient is
constant and updates correctly. Additional retained details must themselves
satisfy the update equation.

## 6. Transport, composition and controlled change

Transporting an aperture through encodings must preserve and reflect the
relevant joint relation and cover the target fiber. An injection without
reflection can introduce spurious solutions. A lossy output encoding may
preserve existence while losing uniqueness or reconstruction.

**Lift–motion–land:** choose an embedding `E:X→Y`, a retraction `D:Y→X`, and
internal motion `P:Y→Y`. The landed operation is `D∘P∘E`. The identity
`D∘E=id` does not make this landed map an arbitrary desired operation, or
even invertible. Prove the requested equation with P included. If reversibility
is claimed, provide its inverse and domain.

**Compilation:** an endpoint compiler preserves the final partial map and
failure disposition. A trace compiler retains the requested intermediate
states, actions or events too. Equal endpoint functions need not have equal
traces or costs. Compose operations only when their intermediate types match.

**Atomic successor:** validate a candidate against its specific parent and
install it only if that parent is still current. Failed validation leaves
the prior state unchanged. An integer version that strictly increases on each accepted update
distinguishes returning to an old value from still being at the old state; equal payloads do not defeat a
stale-parent check. Concurrent valid candidates do not both inherit the same
unique successor position.

## 7. Conceptual reading without losing types

One number can have many lawful descriptions. Integer 1000 is `10^3`; its
base-ten numeral has four positions, a leading 1 and three zeros. In base
two its numeral differs. A string of four digits, a three-step multiplication
path and a geometric three-dimensional object are different carriers.
Use “dimension” with a definition: independent coordinates, vector-space
dimension, manifold dimension, or an explicitly defined operational grade.
Counting symbols does not establish any of the others.

For a fixed-width numeral, retaining the width makes leading zeros meaningful
as representation data; converting to an integer can forget them. A compact
constructor such as `1` followed by N zeros determines all positions and
allows cheap local digit queries without expanding the whole string. That
does not allow cheap arbitrary queries on every huge integer. The expression
uses zero-based positions: position0 is 1 and positions1 throughN are 0.
Here “cheap” means avoiding full expansion; comparisons of binary-encoded N
and the index still cost work in their bit lengths. No constant bit-time
claim follows merely from the compact notation. The expression
`2^p−1` determines a Mersenne integer; prime p alone does not prove it prime:
`2^11−1=2047=23·89`.

**Three plus one** can describe three supplied roles and a fourth constrained
role. Its validity comes from a specified law. A parity equation on four bits
lets any three reconstruct an erased fourth. It detects a single changed bit
when all four are present, but does not locate and correct an arbitrary wrong
bit without more redundancy. Erasure, error, consistency and source truth
are different questions.

**Three truth-tellers and one liar:** if four channels report the same binary
proposition and the assumptions guarantee at most one incorrect report,
majority is correct. Three agreeing reports generated from the same wrong
source do not meet that truth guarantee just by agreeing. Without a constraint
on errors, agreement shows consistency only. Teacher/student examples may
model question selection and learning a supplied finite rule; that model does
not establish a person's beliefs or psychological traits.

An analogy may suggest a carrier or experiment. To turn it into a theorem,
give an explicit map and preservation equation. For example, complementing
symbols and reversing order are definable operations on strings. A picture
of two helices does not establish that arbitrary symbolic processes obey a
biological law. Keep a visual explanation, a mathematical model and a physical
interpretation separately identified.

## 8. Proof donut and evidence

The proof donut organizes constraints around an unresolved question. Its
obligations are: admitted types and givens; coverage of intended sources;
faithful maps; compatible shared witnesses; a continuation rule such as
induction or well-founded descent; and an answer to the original port.
Local satisfiability does not imply a jointly consistent solution.

For a finite invariant, check every admitted seed enters the safe set and
every required transition keeps it there, with bad states excluded. This
supports every finite run **of that model** by induction. To apply it to an
external system, establish the model's coverage and transition bridge.
A descent proof needs a well-founded measure and a correct smaller instance;
an endlessly decreasing real number by itself is not a well-founded descent.

The donut can check RPRM examples; a separate core implementation can check
the same tables. Agreement is useful independent implementation evidence.
It does not prove a checker's soundness by assuming that same soundness, nor
remove the proof system's axioms. A finite test, a written universal proof,
a machine-checked declaration, an experimental hypothesis and a metaphor
must be labeled at their actual grades.

## 9. Four lanes as a complete inference

Four lanes mean four declared maps `O_i:H→B_i` from a common admitted source
family H. For supplied results o_i, retain
`H_o={h in H: O_i(h)=o_i for every supplied i}`. A later lane following an
operation T observes `O_i(T(h))`; its observation map from the original
source therefore includes T. Views generated from one source can constrain
that source without becoming independent measurements. Keep the source
identity and earlier constraints while alternating lanes.

For a requested Q, compute the complete set `{Q(h):h in H_o}`. A nonempty
H_o with one Q-value determines Q, even when the source fiber is MANY. Zero
Q-values means incompatible model and observations; several mean that the
requested answer remains ambiguous. This conclusion relies on the source
belonging to H and the observations obeying their declared maps.

An exact geometric example admits only
`f(x,y)=a+bx+cy+dxy` on `[-1,1]^2`. Its four corner values v_(e,t), where
e,t each equal -1 or 1, determine

```text
f(x,y) = sum over (e,t) of ((1+e*x)(1+t*y)/4) * v_(e,t).
```

Expanding the four terms recovers a,b,c,d uniquely. At the center the four
weights are 1/4. Throughout the square the weights are nonnegative and sum
to one, so positive corners imply positivity everywhere in this grammar.
Two opposite corners alone are insufficient: f=1 and f=xy both give 1
there, but give 1 and 0 at the center. Even the full boundary is insufficient
after enlarging the grammar: f=1 and f=1-(1-x²)(1-y²) agree on the boundary
and differ at the center. Geometry supports the proof through its supplied
function family; it does not supply that family by appearance.

This is how an unvisited location can be inferred. A rotation or reflection
must transport the function, coordinates, supplied ports and requested
readout together. A fixed count of transformed pictures is not a universal
coverage theorem. The enclosure is complete when its mathematical
obligations are complete, whatever number of lanes or moves that requires.

## 10. Arithmetic scope and the signpost at infinity

A proof can cover an unbounded family by a recurrence, invariant or descent.
Its scope comes from the quantified rule, not from how many initial pictures
look similar. For example, if all primes up to M are known, with integer
M≥2, mark multiples of those primes starting at p² through M². Every
composite k≤M² has a prime factor at most sqrt(k)≤M; its least prime factor
p also satisfies p²≤k. Thus every composite is marked and no prime is
marked. This proves the next complete stage. Repeating from the new bound
covers unbounded finite stages; each actual sieve still has finite cost.

The supplementary [independent Fermat study](docs/fermat-study.md) admits
positive integer a,b,c and integer n>2. Its bounded result is:

```text
min(a,b) ≤ 4000  implies  a^n + b^n ≠ c^n.
```

There is no additional independent cap on b,c or n. The proof derives finite
remaining branches from that smaller-base condition and supplies their
premises. The study retains the complete descent and certificate proof.
Its independent unrestricted derivation remains OPEN. Established FLT is
credited as comparison mathematics; importing it does not complete this
independent research goal.

A different proved aperture fixes integer n≥2 and positive integer gaps
s,d. Define `D(a)=a^n+(a+s)^n-(a+s+d)^n`. On positive real a, D(a)/a^n
is strictly increasing: it is one minus a polynomial in 1/a with positive
coefficients. Indeed, subtracting the binomial expansions of
`(1+(s+d)/a)^n` and `(1+s/a)^n` gives positive coefficients at every
nonconstant power. At a=0, D(0)<0. The derived integer
`M=2*n*(s+d)` has D(M)>0: the shell divided by M^n is less than
`(1+1/(2*n))^n-1 < exp(1/2)-1 < 1`.
Binary search for the first integer k with D(k)≥0 therefore gives ONE(k)
if D(k)=0, and NONE otherwise. Strict monotonicity of the normalized sign
excludes every other positive integer, not merely the searched segment.

The existence of this per-tuple decision does not prove every tuple returns
NONE. At n=2,s=1,d=1 it returns ONE(3), since 3²+4²=5². A fifth-power example
n=5,s=2,d=1 has D(11)=-5480 and D(12)=27281 and therefore returns NONE for
every positive integer a. A reparameterization w=a-1 admits w=0. Excluding
that endpoint changes the source problem.

An independent unrestricted completion needs an invariant covering every
remaining tuple, or a same-target integer descent with strictly decreasing
positive integer height. The per-tuple decision alone supplies neither.

Repeating decimals and physical infinities have separate meanings. The
partial decimals 0.3,0.33,0.333,... converge to the finite value 1/3. Their
repeating digit is a description of an infinite expansion, not an infinite
numerical value. An eventual cycle, a limit, divergence and a coordinate
singularity each require their own definition. A proved continuation rule
can be a useful signpost; its interpretation must preserve that distinction.

## 11. Probability laws and approximate retention

For a finite row-stochastic matrix P on S and a surjective partition map
r:S→B, set `K_x(b)=sum(P[x,y] for y with r(y)=b)`. The partition gives one
common reduced Markov matrix Q for every initial source distribution exactly
when K_x=K_y whenever r(x)=r(y). In that case `Q[r(x),b]=K_x(b)`.
Necessity follows by comparing point-mass initial states. For sufficiency,
any conditional mixture of source states in one block has the same next
block law. Iterating this conditional statement preserves every finite
block-state path distribution, and hence its finite-time events. It does
not reconstruct paths inside a block.

For example, on S={a,b,c}, let A={a,b}, B={c}. The rows

```text
P[a,*] = (1/2, 1/4, 1/4)
P[b,*] = (1/4, 1/2, 1/4)
P[c,*] = (0,   0,   1)
```

have aggregate A-row `(3/4,1/4)` and absorbing B-row `(0,1)`. Starting at
either a or b, the chance of B by step two is `1-(3/4)^2=7/16`. Replacing
the b-row by `(1/4,3/4,0)` breaks the quotient: starting at a gives next-B
probability 1/4 and starting at b gives zero. Equal possible-state labels,
similar averages or one specially chosen initial distribution cannot repair
the required every-initial-distribution statement.

For exact refinement, retain the old block and split by the entire vector
of sums into old blocks. On n finite states starting from k nonempty blocks,
there are at most n-k strict splitting rounds. Any stable refinement of the
initial partition refines every stage by induction, so the final partition
is the coarsest stable refinement retaining the initial observations. An
executable version must admit exactly decidable numbers, such as rationals;
arbitrary real equality is not an algorithm.

For distributions u,v, total variation is `TV(u,v)=sum|u_i-v_i|/2`.
If a proposed Q has `TV(K_x,Q[r(x),*])≤epsilon` for every source state,
convex mixing and contraction by a stochastic matrix give

```text
TV(source distribution after t steps, projected to B;
   reduced distribution after t steps) ≤ min(1,t*epsilon).
```

The initial reduced distribution is the projection of the same source
distribution. This bound concerns single-time marginals. It is not itself
a bound for every path statistic or an infinite-horizon hitting time.
If P was estimated, the statement is about that supplied matrix; uncertainty
in the estimate needs its own treatment.

A related finite reconstruction law takes nonempty finite X, real scores
q(x), and representation C. The smallest possible worst absolute error of
a decoder on C(X) is half the largest score range inside any C-fiber. The
triangle inequality gives the lower bound from the fiber extremes; decoding
to each fiber's midpoint attains it. For scores 0,2 in one fiber and 5,5 in
another, the error is 1. A single merged fiber has error 2.5. These are exact
reconstructions of supplied finite scores, not held-out predictive results.

## 12. Two-path and physical applications

The **relational-layer proposal** is a physical hypothesis: observable
objects, forces and geometry may arise from an underlying organization of
relations and lawful continuations. “Underlying” names explanatory
dependence, not an extra spatial dimension or an already demonstrated
substance. The common mathematical presentation preserves supplied
structures; it does not prove that a particular source model exists in
nature.

The precise observation limit follows from sections 4–5. Equal retained
summaries with observation, enabledness and successor congruence give equal
outcomes after every finite admitted action word. A property differing
within such a fiber cannot be recovered from those responses. The limit
is relative to those actions and observations. A new sensor or intervention
can split the old equivalence; universal physical inaccessibility would need
a justified account of every possible experiment.

For a complete example, admit states `(r,h)` with both coordinates binary,
read only r, and allow `tick(r,h)=(1-r,1-h)`. States `(0,0)` and `(0,1)`
have identical visible futures under every finite tick sequence. Their h
values differ. Add `reveal(r,h)=(h,h)` and one action separates them through
r. A simpler source containing only r and the same visible flip also matches
all original observations. Closure therefore proves neither that h exists
physically nor that it is forever inaccessible.

Abduction proposes and compares candidate explanations in a declared family.
Within a complete nonempty compatibility fiber, a property common to every
candidate is conditionally determined even when source identity remains
MANY. Selecting a preferred explanation requires its own criterion and does
not prove uniqueness or completeness of the candidate family. In stochastic
models, compare observation distributions under the admitted interventions;
finite observations need an uncertainty model, not an assertion of exact
distributional equality.

For a proposed relational gravity source s with evolution `Psi_t` and radial
readout C, an exact bridge to an admitted radial flow `Phi_t` requires
`C(Psi_t(s))=Phi_t(C(s))` when defined, matching domains
`s in dom(Psi_t) iff C(s) in dom(Phi_t)` throughout the stated comparison
regime, and coverage of the intended initial radial states. Equality only
on common defined times can conceal different stopping behavior. Supply
physical time, units and parameters. Defining
Psi by copying Phi gives an encoding; deriving the bridge from independently
motivated premises would be a further result. A radial receiver may forget
orientation that a spatial measurement can distinguish. A black-hole causal
horizon is likewise a claim about allowed spacetime paths, not a consequence
of discarding a coordinate in a summary.

In the manuscript's two-path quantum model, a reduced density matrix is

```text
rho = [[p, conjugate(chi)], [chi, 1-p]],
0≤p≤1,  |chi|²≤p(1-p).
```

For its declared phase measurements,
`P_plus(theta)=1/2+Re(exp(i*theta)*chi)` and `P_minus=1-P_plus`.
The complex number chi is an exact minimal receiver for all those phases:
theta=0 recovers Re(chi), and theta=pi/2 recovers -Im(chi). Equal complete
phase answers therefore force equal chi.

The full reduced-state fiber is NONE if |chi|>1/2. Otherwise p ranges over
`[(1-sqrt(1-4|chi|²))/2, (1+sqrt(1-4|chi|²))/2]`. At |chi|=1/2 this is
ONE reduced density matrix; inside the disk it is MANY. Even ONE here does
not identify an arbitrary joint path-plus-marker preparation. The carrier
has changed when that additional system is requested.

This receiver has a precise operational limit. At chi=0 the states p=1
and p=0 have identical phase answers. Apply the Hadamard path operation
`H=(1/sqrt(2))*[[1,1],[1,-1]]`. Their new coherences are respectively 1/2
and -1/2, so the same later phase question distinguishes them. A summary
preserving the earlier phase family does not automatically support H.

A trace-preserving operation on the marker alone leaves the unconditioned
path marginal unchanged. Selecting a marker outcome can change the
conditional pattern, but it has a selection weight. For equal weights,
conditional plus probabilities `(1+cos(theta))/2` and
`(1-cos(theta))/2` recombine to 1/2. Dropping one outcome or its denominator
changes the question. These are consequences of the supplied quantum model,
not a new experimental result or a change to quantum mechanics.

Other physical chapters preserve the same distinction between a supplied
model and its interpretation:

- In an attractive central-force model, an inward acceleration vector is
  compatible with outward motion or a circular orbit. Position, velocity,
  angular momentum, units and the law of evolution all matter.
- A charged particle in a uniform, time-independent magnetic field can have
  circular or helical motion under its stated force law. This does not
  automatically describe every magnet, material or field configuration.
- A coordinate singularity and a physical singularity are different. A
  return-depth construction needs a physical state map, clock and causal
  correspondence before being identified with a black hole.
- Numeral carry depends on base. A cosmic interpretation needs a physical
  state and dynamics, with representation invariance or an independently
  justified physical choice of base.

These paragraphs describe scope; they do not supply all domain derivations.
For a new physical claim, demand its actual variables, map, source equations
and observable test rather than filling missing premises from an analogy.

## 13. Computational examples and experimental proposals

The main scientific proposals develop folding dynamics and BRCA1 cellular
function. Dynamics asks whether a reduced state preserves the declared
future probabilities at a fixed lag and horizon. The assay question asks
whether a representation omits context needed for a supplied cellular score.
Both are unexecuted; neither a synthetic example nor perfect recovery of
training scores establishes biological prediction. Compared methods need
the same available inputs, outcome space, held-out groups and total cost
accounting. Immune mechanisms remain a supporting evidence-map proposal;
the stability-study pointer is further reading, not an executed or reviewed
research specification. Cancer relevance does not make an assay score a
tumor, treatment or individual-risk outcome.

The [fixed-gap implementation](docs/fermat.md) realizes section 10's decision
for supplied exact integers `n>=2, s>0, d>0`. Its complete NONE or ONE fiber
is per aperture; it does not prove uniform exclusion for all n>2 and gap
pairs. Zero is only a sign sentinel. Input types and domains must be admitted;
interruption or exhausted resources means unfinished computation, never
mathematical NONE. Exact integers have real time and memory costs despite
the absence of an arbitrary height cutoff.

The applied examples require their own retained structures:

| Example | What must be retained for its stated question |
|---|---|
| Mechanical motion | Units, assembly branch, lifted angle or chosen period, domain and full inverse fiber. Apply the branch transport before intersecting the requested domain. |
| Ray tracing | Admitted scene and rays, intersection convention, all tied nearest identities, and the exact dependency set for a changed object. Old hits alone do not locate every new hit after insertion. |
| Symbolic music | Voice identity and multiplicity for assignments; period, step and event order for timing. An unordered pitch-class set can forget these. |
| Lattice shape search | The declared lattice, occupied sites, self-avoidance, sequence and energy rule. An exact optimum of that toy does not establish a molecular structure. |
| Rule overlays | Rule table, seed, boundary, transform direction, output view and address map. A color match without a certified comparison label is not primality. |

A deterministic finite state with a fixed readout eventually repeats. A
fixed-width cellular automaton with fixed row-major readout therefore has
an eventually periodic output stream. It cannot equal the full prime
indicator: if that indicator had eventual period L>0, choose a prime q
beyond its start. Periodicity would mark q+qL=q(1+L) prime, a contradiction.
Growing state, an external unbounded counter or a different readout changes
the premises and must be counted in the new model.

An experimental pack is a testable proposal, not a proof grade borrowed
from the core. Report its actual endpoint, data/model availability, candidate,
baseline, rejecting outcome and execution status. Compare methods on the
same observable outcomes, input information, held-out population and cost
budget. A one-category output has likelihood one for its own category;
that makes its log loss zero without predicting a finer outcome well.
Project both methods to the same frozen outcome carrier before comparison,
or supply an explicit decoder and count its cost.

Preserve correlations when a hypothesis allows several joint assignments.
If h permits only {00,11}, allowing both values at each individual port
does not permit 01. Filter the joint assignments as observations arrive.
A repeated identical observation at the same fixed coordinate is idempotent;
conflicting exact values there give NONE. A genuinely new replicate or time
point requires its own coordinate or observation model.

For a finite supplied hypothesis family, a one-step minimax query minimizes
the largest compatible-hypothesis bucket over possible answers. Retain every
tied minimizer. A best bucket size equal to the current hypothesis count
means no guaranteed one-step reduction in that objective. It does not rule
out a useful sequence: if a allows {00,11} and b allows {01,10}, either first
bit leaves both hypotheses possible, while both bits distinguish them.
Catalogue identification is a conclusion about the supplied catalogue.

Missing targets and absent folds do not become zero errors. If model
selection returns OPEN, there is no selected model to refit. Preserve the
failure and any coverage restriction in the paired comparison. Synthetic
checks, recorded-data predictions and physical or clinical outcomes remain
different evidence. This handbook supplies no treatment or diagnostic rule.

## 14. Working procedure and response format

Generate candidate models before freezing the comparison. State selection,
holdout and cost measures before examining results when testing an empirical
or performance claim. Preserve failures and ordinary baselines. A useful
RPRM formulation need not outperform an equivalent conventional algorithm.

For a new task, return:

```text
Question and admitted carrier:
Law, supplied ports and missing ports:
Receiver and requested continuations:
Operation/map and preservation obligation:
Complete fiber or unresolved seam:
Evidence and hostile case:
Strongest supported conclusion and next test:
```

Give the answer directly where it is decidable. Do not invent an extra
approval ritual for ordinary reversible work. If evidence is insufficient,
state precisely which conclusion remains OPEN and continue independent work.
When explaining an experimental application, identify its proposal, supplied
test, observed result if any, and failure criterion; do not borrow proof status
from a different domain. Keep personal data and unrelated narratives out of
reusable mathematical examples.
