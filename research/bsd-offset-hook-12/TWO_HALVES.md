# Two incomplete closures: what can be proved

The user's “69” describes a shape, not the digits six and nine. We model
it as two directed pieces with openings that can join. Neither model
below is claimed to be the uniquely intended RPRM operation. The anchor
used in the actual calculation is **2.0340**.

## Two complementary arcs can force one complete turn

There is a positive, exact result for the shape interpretation. Take an
oriented circle with N discrete positions and two distinct marked seams.
One piece follows the circle forward from the first seam to the second;
the other continues forward back to the first. Require that both pieces
make no extra turns and that their interiors do not overlap. If the first
piece uses s steps, with 1 <= s < N, the other must use N-s steps. Their
total is exactly N: **one complete turn**.

The two pieces need not be equal halves. Their common direction, distinct
seams and complementary interiors are what establish the conclusion.
If extra turns are permitted, the same endpoints allow total winding
1+q1+q2 for nonnegative integers q1,q2. If the second piece merely
retraces the first, endpoint closure does not give the same result.

This is a theorem about the declared circle model, not yet a derivation
of that model from the displayed suffixes. It supplies an integer readout
that survives moving the seam or changing digit labels: the turn count
remains one. The circle's circumference, physical scale and a connection
to the BSD coefficient require additional data. Counting one turn does
not fix the radius or identify a real-valued multiplier.

## A relation that survives changing digits

Let the two certified bounds be L and U, and let x be the unknown value
between them. Its two gaps are

\[
\ell=x-L,\qquad r=U-x.
\]

They satisfy the exact joining relation

\[
\boxed{\ell+r=U-L.}
\]

Divide by the positive interval width w=U-L. The two normalized gaps are
t and 1-t. Their sum is 1, independently of the decimal suffixes. Their
orientation, endpoints and scale remain part of the record. Here “half”
means one of two pieces; the pieces need not have equal lengths.

For example, (0.4,0.6) and (0.3,0.7) both fit together under this rule.
The rule does not select which is the actual pair. Forgetting which gap
is on which side also merges t with 1-t. Retaining the labelled gaps and
L does determine x, because x=L+ell. These are different readouts.

For the new height enclosure,

\[
L=2.034004870820,\quad U=2.034007183803,\quad
w=0.000002312983.
\]

Every x in this interval satisfies the joining relation. On each of the
two tested enclosures, we checked seven distinct interior rational x
values. All seven have the same two-positive-gap shape; the full labelled
gap pair recovers each original x exactly. The unlabelled-pair fibers
have sizes 2,2,2,1, the singleton being the midpoint. This enumeration
is a finite illustration of the preceding algebraic proof.

These test x values are hypothetical states inside the certified bounds,
not seven candidates independently shown to equal the canonical-height
distance. The latter is one fixed quantity defined by its height limit.

## The two pieces can be transported through refinement

For a shared x inside the depth-10 enclosure, write

\[
x=L_9+w_9t_9=L_{10}+w_{10}t_{10}.
\]

Then exactly

\[
\boxed{t_{10}=\frac{w_9}{w_{10}}t_9+
\frac{L_9-L_{10}}{w_{10}}.}
\]

Its inverse exists since both widths are positive. The admitted t9 range
is [(L10-L9)/w9,(U10-L9)/w9], not all of [0,1]. Nine exact sample
readbacks, including both endpoints, passed. Thus this candidate shape
does survive the changed suffix digits under a specified coordinate
change. The coefficients come from the enclosure calculation; this
does not predict the next enclosure independently of that calculation.

## What makes an operational loop select one state

Let one piece carry state x to f(x), and the other carry it back by g.
With both operations enabled, exact closure at x means

\[
\boxed{g(f(x))=x.}
\]

Consider these two examples on x in [0,1]. Each has an outward and a
return operation:

| First piece | Second piece | Closed states |
|---|---|---|
| f(x)=1-x | g(y)=1-y | Every x in [0,1] |
| f(x)=1-x | g(y)=y/2 | Only x=1/3 |

In the second example, x=(1-x)/2 forces 3x=1. The unique answer comes
from the specified operations, not the outline of the two pieces. Both
maps take their admitted values into [0,1]. On the rational line, a first
leg x+1 and a return leg y-0.99 instead leave a residual 0.01 and have no
closed state. A small nonzero residual remains a nonzero residual.

More generally, for total maps on the rational numbers f(x)=a*x+b and
g(y)=c*y+e, closure is

\[
(ca-1)x+(cb+e)=0.
\]

If ca differs from 1, there is exactly one rational solution. If ca=1
and cb+e=0, every rational x solves it. If ca=1 and cb+e differs from 0,
there is no solution. For restricted domains, intersect this solution
family with the states where both legs are enabled. This proves the
complete fiber classification, including constant maps and failed loops.
The finite checker independently substitutes a nine-point rational grid
for each of 625 integer coefficient tuples; all comparisons pass.

The [independent two-piece report](agents/TWO_HALF_CLOSURES.md) also
distinguishes joined endpoints, paths that retrace, phase around a circle,
and retained whole-turn counts. A joined outline alone fixes none of
the transport coefficients. Pi can enter an actual geometric transport,
but the two-piece shape does not require that constant by itself.

## What remains for BSD

The two displayed bounds enclose **one arithmetic height distance**.
They are not themselves the analytic side and arithmetic side of BSD.
The comparison still needed for the fixed curve is

\[
\frac{L''(E,1)}{2}=\Omega\,\mathcal R\,\sigma,
\]

where Omega is the real period, R is the regulator from the full-height
convention, and sigma must separately be identified with the finite
cohomological Sha group order. The local and torsion factors cancel for
this curve under the previously fixed normalization.

A useful two-piece proof must supply actual maps or a joining equation
between those analytic and arithmetic objects, and prove that their
closed state determines this comparison. We have an explicit criterion
for what such closure would mean, and complete small examples where it
works. We have not yet constructed those BSD maps. The clarified shape
proposal stays OPEN; the vanished literal 123 hook is not its refutation.

Runnable source: [check_two_halves.py](work/check_two_halves.py).
Fresh result: [two-halves.json](evidence/two-halves.json).
