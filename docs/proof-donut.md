# Proof donut: checks around a precise question

The proof donut is a proof-certificate method: identify the unresolved port,
then arrange enough compatible constraints, maps, and coverage arguments to
answer it. The enclosure can be a graph, a table, an atlas, or a derivation.
Its name does not require a circular shape or a fixed number of checks.

The method is useful for checking RPRM claims themselves. The supplied rules
and ordinary mathematical proof principles remain visible when it does so.
Its implementation passing tests does not certify all its own claims.

## The aperture and its enclosure

An aperture supplies given inputs `g` in G, a witness carrier W(g), a relation
R(g,w), and a requested answer. Its complete fiber is

`F(g) = {w in W(g) : R(g,w)}`.

Existence, nonexistence, uniqueness, one witness, all witnesses, and a readout
are different requests. MANY witnesses can settle a readout if they all agree.
An empty fiber has no answer about an unknown actual source unless membership
in the declared grammar is already established.

| Obligation | What must be supplied |
|---|---|
| Types and context | Carriers, equality, givens, witnesses, operations, and assumptions |
| Coverage | Why every intended source belongs to the handled grammar or cases |
| Transport | What each map preserves and the complete forgotten fiber |
| Seams | Shared witness identity and joint compatibility of local constraints |
| Continuation | A proved invariant, induction, descent, or other extension rule |
| Landing | An answer to the original requested port |

For maps `alpha:G->G'` and `beta_g:W(g)->W'(alpha(g))`, the exact witness
contract is `F'(alpha(g)) = beta_g(F(g))` for each original g. Forward inclusion
allows an empty abstract fiber to prove the original empty. Reverse inclusion
supplies the lift needed to infer original existence from abstract existence.
Uniqueness or full reconstruction requires stronger fiber conditions.

Shared witnesses must survive composition. Factoring `a=w^3` into `u=w^2`
and `a=u*w` is exact. Forgetting which w was used admits `1^2*2=2`, a false
cube completion. Three binary constraints `x=y`, `y=z`, `z=1-x` also have
inhabited local projections while their joint fiber is empty.

## Inferring an unvisited position from retained observations

An observation lane may expose only part of a shared source. Write its map
as `O_i` and its observed value as `o_i`. Within an admitted source grammar H,
the compatible completions are

`H_o = {h in H : O_i(h)=o_i for every supplied lane i}`.

Alternating which lane is observed or which port is requested can add useful
constraints. Retain the earlier constraints and the same source identity.
Adding an observation intersects the previous fiber with one more condition;
it cannot create new compatible completions. If the observations are faithful
and the source belongs to H, the actual source remains in that intersection.

For a requested unvisited value Q(h), compute its values over the complete
remaining fiber. If the fiber is nonempty and every completion gives the same
Q, that value is forced even if several full sources remain possible. If Q
varies, identify the missing distinction and choose another observation.
This is the precise inference step behind using retained views, or shadows,
to settle an unobserved port. The views must constrain one joint completion.

A square gives a concrete positive example. On `[-1,1]^2`, suppose the law is
multiaffine: `f(x,y)=a+b*x+c*y+d*x*y`, with real coefficients. Four corner
values determine every interior value by interpolation. In particular,

`f(0,0) = (f(-1,-1)+f(-1,1)+f(1,-1)+f(1,1))/4`.

No separate visit to the center is needed. Averaging the four expressions
cancels the x, y and xy terms and leaves a. The full interpolation formula
uses weights `(1+epsilon*x)*(1+eta*y)/4` on corner `(epsilon,eta)`, for
`epsilon,eta in {-1,1}`. Those weights are nonnegative and sum to one in the
square, so positive corner values imply positivity throughout it.

The exact extent of the observations matters. Visiting only the opposite
corners `(-1,-1)` and `(1,1)` does not determine the other corners or center,
even in this same grammar: `f=1` and `f=x*y` both give 1 at those two visits,
but their center values are 1 and 0. A diagonal route alone has not supplied
the missing constraints.

The law matters too. If quadratic terms in each coordinate are admitted,
`1` and `1-(1-x*x)*(1-y*y)` agree on the entire square boundary but differ
at the center. The same surrounding observations then leave the center open.
These examples establish when indirect inference succeeds and expose exactly
what a stronger inference would need. A finite checker can enumerate a
declared finite H; the interpolation identity proves the separate general
statement for multiaffine functions.

## What the executable checks

[The module](../rprm/proof_donut.py) works from complete finite tables. It
imports no core implementation, proof-status flag, or private proof metadata.

| API | Contract checked |
|---|---|
| `fiber_disposition` | Complete admitted members and whether their typed readouts agree |
| `audit_finite_aperture` | Per-input abstract fiber equals the image of the concrete fiber |
| `audit_finite_induction` | Seeds enter safe states, total transitions preserve them, safe and bad are disjoint |
| `audit_finite_descent` | Core excludes bad states; each remaining bad case returns to a smaller-rank bad case |
| `audit_finite_path` | Every route edge is enabled and correct; an optional cycle returns the complete state after at least one edge |
| `audit_finite_quotient` | Equal summaries preserve observation, enabledness, and successor summaries |

Carriers are finite built-in tuples, lists, ranges, sets, or frozensets, copied
at admission. One-shot generators are rejected. Carrier members are exact
integers, strings, None, or recursively tuples/frozensets of those atoms;
bools and floats are excluded from states. Duplicate carrier atoms are rejected.
Paths can repeat states. Readouts additionally allow Booleans; `True` and `1`
remain distinct typed answers. None can be a decided answer, so consult
`decided`, not just `decision`.

Use complete dicts for readouts and maps declared total. Relation rows are
distinct ordered pairs. The aperture API takes a common witness carrier and
a total beta table keyed by `(g,w)`; relation membership supplies per-given
restrictions. This makes the complete finite input explicit.

Malformed or out-of-carrier inputs raise `AdmissionError`. A well-typed
certificate that fails an obligation returns REJECT, error codes, and concrete
witnesses. A partial transition is admitted for path/quotient checking and
rejected as a total-transition induction certificate. The module uses explicit
checks, which remain active under optimized Python. It does not offer an
unbounded search or return a partial enumeration as a complete fiber. The
caller must supply finite inputs small enough for the requested census.

## A finite mutual-use demonstration

[The example](../examples/proof_donut.py) gives all four states, a seed,
observation, summary, and transition:

```text
S = {0,1,2,3}, seed = 0
T: 0 -> 1 -> 0 and 2 -> 3 -> 2
q(s) = observation(s) = s mod 2
safe = {0,1}, bad = {2,3}
```

The core computes the quotient. The independent proof-donut implementation
checks every pair merged by q. Its invariant checker verifies safe closure
on the concrete carrier. Thus the core can organize a finite relation while
the donut checks a specified claim about that relation using a separate
implementation.

Changing only `T(2)` to 2 retains today's observation but breaks the proposed
quotient: states 0 and 2 have equal summaries yet their successors have
different summaries. This is the separating hostile case.

These concrete tables witness that the explicitly listed finite conditions
can be satisfied. They do not establish consistency of every statement called
RPRM. To ask a stronger consistency question, supply the exact axiom set and
the model or metatheoretic proof it requires. Checking a certificate cannot
assume its intended conclusion inside an adapter.

## A prime-region certificate

The [square-frontier construction](../experimental/primes/square-frontier.md)
supplies a second application with an expanding carrier. Its state is the
bound B together with the complete increasing list of primes through B.
The requested answer is the prime/composite status of every integer through
B^2, retaining a divisor for each composite.

The certificate has three connected parts:

1. Establish that the initial prime list is complete.
2. Classify the entire next region and compare each answer with an independent
   census of integer divisors. Check every returned factor. The aperture
   checker verifies equality of the two complete classification relations.
3. Carry the complete resulting list into the next state, check B'=B^2,
   and use the path checker to verify the actual sequence of states.

The [executable audit](../checks/prime_frontier.py) instantiates the path
`5 -> 25 -> 625 -> 390625`. These are declared demonstration bounds; the
general continuation rule is the factor theorem: a composite at most B^2
has a prime factor at most B. That theorem supplies the induction step for
every finite stage. The finite path is expanding and is not a closed orbit.

The audit also connects the resulting prime list to every bundled Fermat
auxiliary pair. It then checks their full residue conditions separately.
This makes an actual dependency inspectable: prime classification supplies
ingredients to the auxiliary lemma. To exclude Fermat solutions in a new
region, a corresponding zero-exclusion argument is still required.

## Choose transformations for the stated relation

A finite transformation family belongs to a specified carrier and relation.
Enumerating all its members can exhaust that family. It does not establish
that this family covers every intended mathematical case. Its size follows
from its definition; there is no universal requirement of 24 moves.

For example, in `a^n+b^n=c^n`, exchanging the two positive summands preserves
the equation. Exchanging b and c while leaving their equation roles fixed
does not: it asks whether `a^n+c^n=b^n`. Transporting the equation roles and
values together can instead give a faithful new presentation, provided the
map and inverse are retained. The exponent port also has its own role;
moving a root value into it requires a separate mathematical contract.

A useful audit therefore states each move, its inverse or forgotten fiber,
its admitted inputs, and the exact requested answer it preserves. Repeated
presentations may expose a missing seam or a simpler argument. The number
of presentations does not multiply the evidence or force an empty fiber.

## Why a finite enclosure can support a theorem

**Invariant rule.** Suppose every intended source has a finite construction
word in a declared grammar. Every seed maps into I; each concrete transition
is faithfully represented by an abstract transition preserving I; and I
implies the desired answer. Induction on construction length proves the
answer for every intended source. The table checker tests only the finite
abstract obligations. Grammar coverage, concrete-to-abstract soundness, and
target sufficiency remain separate proof obligations.

For example, quotient-ring laws let the two residues modulo two determine
`n^2-n mod 2`. Both give zero, proving `n^2-n` even for every integer. The
coverage and ring laws, rather than an integer sample, carry the quantifier.
The same parity readout cannot decide `n=2`, because 2 and 4 collide.

**Descent rule.** Let the bad cases outside a certified core be completely
covered. Suppose each such case has an actual admitted bad return with a
strictly smaller rank in a well-founded order. A minimal-rank bad case would
have a smaller one, a contradiction. Hence the bad set is empty. The return,
type-correct landing, preservation, coverage, and rank law must be proved for
the intended source family; the checker does not discover them.

For example, if positive integers satisfy `a^2=2b^2`, parity makes a even;
substitution makes b even. The pair `(a/2,b/2)` is another positive integer
solution with smaller rank `a+b`. Well-foundedness of positive integer rank
excludes every such pair. This is the classical irrationality proof expressed
with explicit return obligations.

**Cycle rule.** If a fixed deterministic transition satisfies `T^m(s)=s` for
an integer m>=1, composition gives `T^(m+k)(s)=T^k(s)` for every k>=0. A
predicate checked on that entire orbit holds on its future repetitions. The
carried state must include any clock or history affecting the transition.
A scalar returning is insufficient when the transition carries an ordered
pair. Other source orbits require coverage of their own.

The assumptions behind these arguments are ordinary sets, relations,
equality, classical logic, and the stated induction principles. The finite
code is neither a proof assistant for arbitrary formulas nor its own
foundation. Agreement of two implementations helps find errors; shared
assumptions and possible common mistakes remain inspectable.

## Reproduce the checks

From the repository root:

```sh
python -I -B checks/proof_donut.py
python -I -O -B checks/proof_donut.py
python -I -B examples/proof_donut.py
python -I -B checks/prime_frontier.py
```

`checks/proof_donut.py --output /absolute/path/proof-donut.json` also writes
its result to an absolute JSON path. The census includes 256 aperture
certificates, 256 invariant certificates, 512 descent certificates, and
4,096 comparisons with the independently implemented core quotient, plus
named hostile and malformed-input controls. Counts describe finite checks,
not independent proofs or a probability that arbitrary future code is correct.

No geometric, topological, or physical result follows from the word donut.
See [initial states and origins](origins.md) for the separate model boundary.
