# Changing the estimate while retaining the physical question

12 September 2026. Research continuation; publication remains on hold.

The previous estimate can be improved. Two exact joint calculations reduce
its constants, and a conditional-response argument carries the gap beyond
the point where the simple curvature formula becomes inconclusive. Merely
restarting the old estimate does not do this.

## What is repeating, and what would count as being stuck?

A statement such as "the relative excitation energy is at least 1/2 for
every finite lattice size" uses one rule across arbitrarily many sizes.
It does not require a computation that repeats forever. A lower bound
that survives every larger size is exactly the desired coverage.

The vacuum construction is a different operation: successive approximations
must approach an actual function. A contraction factor q<1 gives an error
bound proportional to q^n, so an indefinitely extendable sequence converges
to a definite result. Once an estimated factor reaches one, the estimate
only says that errors need not grow. It no longer guarantees that they
shrink. That is failure of this guarantee, not proof that the actual
iteration cycles, the vacuum fails to exist, or the energy gap vanishes.

The geometric formula was conditional on a proved bound Y for the actual
vacuum. It cannot keep certifying larger interaction ratios after the
hypothesis supplying Y has run out. Repeating its positive numerical output
without supplying that hypothesis would add no evidence.

## The inverse/restart idea has been tested

The old equation was u=r T^-1 S+B(u,u)/2, with
||T^-1 S||_*<=8m and ||B(u,v)||_*<=(8/3)||u||_*||v||_*.
Writing u=u0+v around an already constructed interacting vacuum gives

```text
v=(r-r0)T^-1 S+B(u0,v)+(1/2)B(v,v).
```

This is an exact recentering, not a change of model. But if all we know
about u0 is the old upper bound Y0, the maximum extra source allowance
is h*=(1-(8/3)Y0)^2/(16/3). Since the old source satisfies
t0=Y0-(4/3)Y0^2,

```text
t0+h*=3/16.
```

Thus the same worst-case estimates reproduce the same boundary however
often they are restarted. A separately established smaller bound on u0
could help; a relabeling of the same bound does not. The genuine weighted
Poisson inverse is also distinguished from its missing uniform Fourier
norm estimate in [RECENTER_AND_INVERSE.md](RECENTER_AND_INVERSE.md).

There is one immediate endpoint correction: finite-graph spectral
continuity closes the old strict boundary. The old proof already implies
gap/E_el>=1/4 at r=3/(128m), by approaching that parameter from below
for each fixed graph. No endpoint log-vacuum norm is assumed. This small
extension is proved in the same note and is superseded by the stronger
interval below.

## Exact joint information improves the estimate

Two replacements were proved and independently reviewed:

```text
source:     ||T^-1 S||_* <= 4m             (formerly 8m),
bilinear:   ||B(u,v)||_* <= (16/9)||u||_*||v||_*
                                             (formerly 8/3).
```

The source calculation uses the actual square holonomy with two forward
and two inverse link occurrences. Its Fourier coefficient has four
nonzero singular values, all one. Its trace norm is exactly four; the old
term-by-term upper bound was eight. The full index calculation and the
orientation-sensitive hostile case are in
[SOURCE_NORM_REFINEMENT.md](SOURCE_NORM_REFINEMENT.md).

The bilinear calculation retains the joint structure of two coefficient
inputs while combining their three SU(2) derivative directions. The
unrestricted worst channel has size three, but that channel's full weight
cannot occur in a product of the rank-one input vectors used in the
coefficient calculation. Their exact joint bound is two. Separate
singular-value expansions extend the result to arbitrary complex
coefficient matrices, including correlations among links within each
input. No unentangled physical-state assumption is introduced. See
[SIGNED_AND_CONTRACTED_AUDIT.md](SIGNED_AND_CONTRACTED_AUDIT.md).

This is a concrete realization of retaining a joint before bounding its
parts separately. It does not assert a universal cancellation rule for
every RPRM problem or reduce the broader RPRM concept to this example.
The completed new estimates are in the same function-space contract as
the accepted proof, so its regularity and actual-vacuum identification
continue to apply.

## Combined construction and explicit bounds

The carrier remains every finite connected nearest-neighbor subgraph of
Z^d, d=2 or 3, with distinct elementary square plaquettes, positively
oriented coordinate links, all spins, and gauge invariance at every
vertex. At least one square is retained when a nontrivial physical excited
sector is requested. Equality is Haar almost-everywhere equality. Shared
edges remain shared occurrences. The operator and units are unchanged:

```text
H_G/E_el = T_G+r sum_p(1-a_p),
E_el=alpha hbar^2>0,   r=beta/E_el>=0,   m=2(d-1).
```

The requested readout is a lower bound above the exact ground energy
on every vector in the physical form domain, uniformly in the finite
graph. No full eigenfunction fiber or continuum theory is supplied.

Put t=4mr and b=8/9. The smaller invariant-ball radius is

```text
Y(t)=(9/16)(1-sqrt(1-32t/9))
    =(9/16)(1-sqrt(1-128mr/9)).                         (E1)
```

It satisfies Y=t+bY^2. The fixed-point map is a strict contraction for
r<9/(128m), with contraction factor (16/9)Y<1. The same actual-vacuum
construction as before yields ||u||_*<=Y. At Y=1/4 the closed interval
is r<=7/(144m), giving the familiar curvature lower bound 1/2. In three
spatial dimensions this improves r<=1/192 to r<=7/576, a factor 7/3.

The actual remainder estimate also improves on this interval. With
W=Y-t-(8/9)t^2, the unchanged support-count proof gives
sum_j epsilon_ej <= (16/3)W. At its endpoint W=16/729. Combined with
the accepted head, the conditional row is bounded by

```text
7/144 + 49(m-1)/(151632m) + 64/2187 < 1/12
```

for m=2,4. Thus the earlier CP8 bound remains valid on the enlarged
half-gap interval; it is not only a statement about a truncated vacuum.

## A positive gap does not require the simple curvature bound to stay positive

The previous geometric certificate is gap/E_el>=1-2Y. It becomes
inconclusive at Y=1/2, while the improved contraction factor is still
8/9. The actual vacuum is still constructed there.

We tested the conditional route instead of treating that event as a
physical gap closure. For any constructed vacuum with ||u||_*<=Y<3/4:

1. The complete conditional influence row is at most q=4Y/3.
2. A conditional update process contracts the total coordinate
   oscillation at rate at least 1-q. Reversibility and the spectral
   theorem turn this into a conditional-update spectral gap.
3. Each one-link conditional measure differs from Haar by a log-density
   oscillation at most 8Y/3. Haar's gradient Poincare constant 1/3
   therefore gives a conditional constant at most exp(8Y/3)/3.
4. Combining the two inequalities with the exact ground-state form gives

```text
gap_physical/E_el >= (3/2)(1-4Y/3) exp(-8Y/3).           (E2)
```

Every step covers all form-domain states, not just a selected eigenvector.
The conditional update process is an auxiliary proof device; it is not
identified with physical real-time evolution. The full proof, including
the transpose in the influence matrix and the dense-domain spectral
argument, is in [CONDITIONAL_GAP_EXTENSION.md](CONDITIONAL_GAP_EXTENSION.md).

At the construction boundary Y tends to 9/16. Equation (E2) still has
the positive limit (3/8)exp(-3/2). Finite-graph spectral continuity closes
that endpoint. The final uniform result of this continuation is

```text
0<=r<=9/(128m)
  ==> gap_physical >= (3/8)exp(-3/2) E_el.               (E3)
```

In d=3, the interval is r<=9/512, and the displayed bound is about
0.08367 E_el. A useful stronger value on a smaller interval is
r<=1/64 => gap_physical >=3/(4e) E_el, about 0.2759 E_el.
These are conservative sufficient bounds, not optimal energies or
physical transition points.

The conditional proof is an independently derived route around the loss
of the curvature certificate. It confirms a positive gap farther along
this finite-lattice family. It does not license extending the interval
indefinitely. The improved fixed-point estimate itself still stops, and
the recentering calculation explains why repeatedly using that same
estimate cannot remove its boundary.

## The two changes of scale in concrete terms

Start with a two-metre-wide square divided into one-metre cells.

- **More cells:** keep the one-metre cells and extend the modeled square
  to four metres across. The present all-size inequality covers this
  growth at a fixed admitted local ratio.
- **Finer cells:** retain the same two-metre region, divide it into
  half-metre cells, and then finer cells. To represent the intended
  continuum theory, one must also relate the parameters and observables
  between these descriptions. That relation is not supplied by drawing
  a finer grid.

A change of numerical energy unit transforms coefficients (1,0.01) to
(100,1); their ratio stays 0.01. A change of the model coefficients from
(1,0.01) to (1,0.1) changes the ratio to 0.1. These illustrative numbers
are not computed Yang-Mills couplings. They show why changing units and
changing a physical parameter are different operations.

In the primary convention already checked, E_el=g_b^2/(4a) and r=8/g_b^4.
The usual weak-bare-coupling continuum direction has g_b tending to zero,
so r grows outside the finite interval proved here. This is why "a new
lens needs a proved comparison" means transporting the actual energy
form, gauge constraint and vacuum measure correctly. It does not mean
choosing one scaling number and hardcoding it at every level.

## Attribution, remaining work, and evidence

"No literature-priority claim" meant only that we have not established
that this particular derivation is the first of its kind. Fourier
analysis, spin addition, contraction, weighted curvature and conditional
mixing are established tools. The specific estimates and their assembly
are derived here. Their historical novelty has not been established.

The next mathematical requirement is an estimate for a continued actual
vacuum that improves on the present worst-case invariant ball, or a
different reference construction with a uniform comparison in the
required local norm. A positive L2 spectral gap alone is not that local
inverse estimate. The inverse note provides a high-spin distinguishing
case. Infinite-volume dynamics, continuum existence and positive gap
survival in fixed physical units remain separate, unfinished work.

New finite rational matrix, spin-pair and scalar controls accompany the
written proofs. They check the explicit source partial isometry, the
fundamental swap calculation, new constants, restart boundary and a
transpose error. They do not certify unrestricted analytic theorems.
No accepted checkers, simulations, publications, installations or git
mutations were performed. The previous portable packet remains unchanged.
