# One additional elementary arithmetic consequence

**New deduction in this review, not attributed as a new Codex computation.**
It uses verified point counts already needed by the analytic calculation.
It is an application of a standard theorem, with no novelty claim.

Let E/Q be y^2=x^3-25x. Its discriminant is 1,000,000, so 3 is an odd prime
of good reduction. Over F_3 the equation is y^2=x^3-x. Every possible x
(0,1,2) makes its right side zero, leaving exactly one ordinate y=0.
Including O gives

    #E(F_3)=4.

Milne, *Elliptic Curves* (2006), Chapter II, Corollary 5.7, printed p.66
(PDF page 74), states that rational torsion injects into the reduction at
an odd prime of good reduction. The statement and page were inspected:
https://www.jmilne.org/math/Books/ectext6.pdf#page=74

Consequently #E(Q)_tors <=4. There are already four distinct rational
points killed by two:

    O, (0,0), (5,0), (-5,0).

They exhaust all rational torsion. Thus

    E(Q)_tors = E(Q)[2] = (Z/2)^2.

Combined with the accepted rank-one descent, the abstract rational-point
group is Z plus (Z/2)^2. This does NOT establish that the chosen P=(-4,6)
is a generator of the free Z factor. Its possible odd index remains a
separate saturation question.

The reduction injectivity statement applies to torsion here, not to the
entire infinite rational-point group. There is no claim that four finite-field
points imply only four rational points.

The independent checker also recounts eight points at the good prime 7,
consistent with the torsion bound. Prime 3 alone suffices for this argument.
No torsion database or Sage computation is used.
