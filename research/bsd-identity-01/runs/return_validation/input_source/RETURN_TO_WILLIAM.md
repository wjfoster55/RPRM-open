# The rank-two experiment: what we proved and what remains

We have a checked rank-two case and a precise version of your midpoint
operation. We have not obtained a proof of general BSD, or the full BSD
formula even for this new curve. The completed results below are written
proofs supported by fresh exact computation and established theorems.

## Your correction: a full move and a half move

Your latest example tracks direction and distance:

    start       full move          endpoint
      0.6        −0.2                0.4

    start       half move          midpoint
      0.6        −0.1                0.5

Stopping at the midpoint does not carry the first endpoint across to the
other side. We have preserved that distinction. You were not asserting
that opposite squared displacements cancel.

The exact rule we can prove from the example is to retain a midpoint m
and a directed gap δ. Then both endpoints are recoverable:

    first endpoint  = m − δ/2,
    second endpoint = m + δ/2.

With m=0.5 and δ=−0.2, these are 0.6 and 0.4. Retaining the midpoint
and one original endpoint also suffices. Keeping only 0.5 loses the gap:
0.7 and 0.3 have the same midpoint. This distinguishes an invertible
change of coordinates from throwing away information.

`MIDPOINT_BRIDGE.md` proves those statements, distinguishes first-slot
motion from moving both endpoints, and connects the center 0.5 to the
actual completed L-function by F(z)=Λ(2z). The identities were tested
with exact fractions on 441 ordered pairs. The earlier tentative carry
and sign sequence is retained as an open specification, not filled in
with an invented recurrence.

## The completed curve calculation

The new test curve is

    E34: y²=x³−1156x.

Its rational points have exactly two independent integer directions:

    E34(Q) = Z·(−2,48) ⊕ Z·(−16,120) ⊕ {O,(0,0),(34,0),(−34,0)}.

Here O is the identity at infinity. Every rational point is an integer
combination of the two displayed generators plus exactly one of the
four torsion points. Once this basis is fixed, that description is
unique. The basis is not a claim that one coordinate is the smallest
number: a generating step is a property of the elliptic-curve group.

We established the number of directions by complete 2-descent. We then
proved the two points generate the whole free part. A uniform height
bound forced any missing generator to occur among 38,205 rational
x-coordinates. Exact enumeration found 25 affine points, all accounted
for by our generators and torsion. That closes every possible missing
finite index at once, including odd indices.

On the analytic side, L(E,1)=L'(E,1)=0 exactly, and

    6.38511803 ≤ L''(E,1)/2 ≤ 6.38518585.

The positive interval proves that the first nonzero term is the quadratic
term: analytic rank two. Thus the arithmetic and analytic ranks match.
The lower zeros use the established theorem that analytic rank zero or
one must equal arithmetic rank, together with our arithmetic rank two.
They are not inferred from decimals close to zero.

The interval includes a bound on the entire omitted infinite series.
The first two prescribed tail bounds were too wide and remain recorded
as unresolved attempts. The third cutoff succeeded. We have not changed
the failed records into successes.

## The remaining gap in this case

Sha, pronounced “shah,” is an arithmetic group measuring certain failures
of passing from solutions over all completions to a rational solution.
Our descent proves its 2-primary part is zero: there is no nontrivial
element killed by a power of 2. It does not settle elements associated
with odd primes such as 3, 5, or 7, or prove the total group finite.

For E34, the full BSD formula would identify the analytic coefficient
with the real period times the regulator times the order of Sha:

    L''(E,1)/2 = real period × regulator × #Sha.

The local correction factors and the torsion correction cancel for this
curve. The period measures the real curve; the regulator measures the
two independent generating directions through canonical heights. We
verified their conventions, including both real components and the
full integral basis. The resulting rigorous comparison is

    0.999920542 ≤ [L''(E,1)/2] / [period × regulator] ≤ 1.000092816.

This is compatible with #Sha=1. It does not prove #Sha=1: we still need
an independent proof that the quotient equals the order of that group.
The interval contains nonintegers as well as 1. The bounded theorem
review did not establish an applicable result closing this gap; its
actual failed and missing hypotheses are in `FULL_BSD_FRONTIER.md`.

Your follow-up asks what would establish the order. There is a precise
arithmetic answer: prove that, for every odd prime p, all p-Selmer
classes come from rational points. Given the group we proved, this
amounts to showing the p-Selmer group has exactly p² elements for every
odd p. Together with the completed 2-descent, that would force Sha to
contain only zero, without assuming BSD. `SHA_ORDER_CRITERION.md`
proves this reduction and explains the still-open uniform premise.

## The precise obstacle for the general argument

Your midpoint and directed gap give us a recoverable coordinate system.
For a BSD proof, we additionally need a relation tying the arithmetic
directions of the curve to its particular analytic coefficients.
Changing where we describe the center preserves the existing zero order;
it does not yet determine that order from the rational points.

The analytic reflection does force one parity of coefficients to vanish.
For a plus sign, the odd powers vanish. However, both a fourth-power
term and a fourth-power term plus a small quadratic term respect that
same reflection. These are analytic control examples, not claims that
they are elliptic-curve L-functions. They show exactly what reflection
alone leaves undetermined: whether an allowed lower coefficient is
exactly zero.

The next missing mathematical ingredient is therefore a proved rule
connecting the directed operation to the curve's actual coefficient
weights or height data. It must preserve the relevant signs, factors,
and information, and force the required exact identities. That is a
concrete open obligation we can iterate on. It is not resolved by the
rank-two calculation, which used existing low-rank theorems for its
lower zeros. General BSD also requires the full leading-coefficient
identity and the appropriate Sha finiteness argument.

## Evidence and scope

Seven computational stages were rerun from copied source into a fresh
directory, with no saved receipts copied in. All completed successfully.
The audit independently recomputed Euler coefficients, derivative
identities, signed quadrature bounds and the complete tail ledger. It
did not independently reevaluate every quadrature panel. A separate
factor audit reconstructed the AGM period, height determinant and quotient.
This is reviewable written and computational mathematics, not a formal
proof-assistant verification or a claimed new general theorem.

The material is suitable to share as a reproducible case study and a
precise account of the open proof obligations. It should not be presented
as a solution or candidate complete proof of general BSD.

Start with `BSD_REBRIEF.md` for the concise result, `README.md` for the
file map and replay command, and `runs/final_validation/RUN.json` for
the fresh execution record. The earlier E5 deliveries and other research
lanes were not modified. This return ends the rank-two experiment.
