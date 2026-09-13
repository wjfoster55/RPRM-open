# Where this covering argument stops, precisely

12 September 2026. A research obligation, not a claim that a physical gap
vanishes. See [COVERING_RESULT.md](COVERING_RESULT.md) for the proved carrier.

## The first failure is in our certificate

There are two different numbers in the direct proof:

```text
construction:  y <= t+(4/3)y^2,       t=8mr,
geometry:      gap/E_el >= 1-2y.
```

The construction works by choosing a ball of radius Y that the exact
fixed-point map preserves and contracts. A sufficient radius solves

```text
t = Y-(4/3)Y^2.
```

The right side has maximum 3/16 at Y=3/8. Thus this contraction argument
has a strict endpoint r<3/(128m). At that endpoint its contraction
factor reaches one. Yet the curvature-based energy bound there would
still be 1-2(3/8)=1/4, strictly positive.

This is an informative mismatch: the method loses its ability to certify
the vacuum before its geometric lower bound would become zero. The
inequality y<=t+(4/3)y^2 itself does not exclude large y; the smaller-root
ball and contraction argument are the load-bearing construction. Absence
of a suitable ball after the discriminant becomes negative is not
nonexistence of the actual vacuum. Every finite compact graph still has
its actual ground state.

The safe closed interval used for the headline result is smaller still,
r<=1/(48m), so that the proof has a contraction factor at most 2/3 and
a stated lower gap of 1/2. These are sufficient margins. None of the
thresholds is presented as a physical transition point.

## What the local norm sees and overestimates

For each link, the norm adds the absolute sizes of every Fourier component
touching it, weighted by that component's electric energy. It covers
arbitrary collective supports and high spins. It does not need to know
which excitation will be the cheapest.

Its cost is that opposite signed contributions are bounded separately.
The proof may charge for a large positive and negative contribution even
when their sum cancels substantially in the actual function. Multiplying
Fourier components can also cancel a link's representation and shrink
support; the union-of-supports bound deliberately permits the larger
union. Both choices are safe but can overestimate accumulated response.

William's emphasis on retained joints has a precise possible use here:
keep the coefficient correlations and support cancellations needed for
the derivative or conditional receiver, and prove a replacement for

```text
||T^-1 Q <grad u,grad v>||_* <= (8/3)||u||_*||v||_*.
```

A smaller certified constant, a smaller exact source norm, or a reference
vacuum that absorbs the dominant interactions could enlarge the interval.
Ordinary subtraction identities alone do not bound these matrix-valued
joint contributions. A proposed cancellation must survive the complete
sum over supports and all boundary conditions, not only selected cases.

## A change of lens must carry the energy form

A pure coordinate change rewrites the same metric, density and operator;
it cannot alter whether a physical low-energy direction exists. Choosing
a new comparison metric or interacting block vacuum can change how well
we prove a bound, but then it creates a new comparison obligation.

One explicit sufficient target at stage s is:

Let D_s be the **dimensionless** form q_(H_s-E_0,s)/E_el,s after the actual
ground-state transform. Let a_s>0 and kappa_s>0. Require the following for
every function in the transformed actual physical form domain, included
in the reference form domain:

```text
actual ground-state form D_s(f) >= a_s D_reference,s(f),
D_reference,s(f) >= kappa_s Var_(actual nu_s)(f),
inf_s [E_el,s a_s kappa_s / E_physical_reference] > 0.     (N1)
```

All forms here must use the declared actual-vacuum measure and compatible
domains, or a further proved measure-transport comparison must be supplied.
The physical reference energy in (N1) is fixed by the continuum question;
it cannot be defined to equal the very gap being proved. Both a_s and
kappa_s may vary relationally. Their product in physical units is the
quantity that must retain a positive lower bound.

An interacting block reference must also retain boundary gauge data and
all interactions generated between blocks. The joint cannot be replaced
by separately chosen block vacua unless an exact inclusion or controlled
comparison proves that every relevant physical trial state is covered.
This is where the official enclosure and operational-fold conditions
remain useful beyond the present realization.

## Two scale questions that now have different statuses

**More cells at the same admitted local ratio:** the current proof covers
every finite size with one constant. It forbids the gap from shrinking
merely because the number of possible collective directions grows.

**Finer cells while tuning toward continuum physics:** the coefficient
ratio changes along the usual bare-coupling path. The current estimate
does not follow that path through arbitrarily large r. It also does not
construct the limiting field theory, physical observable algebra or
limiting dynamics. These require actual transport and convergence proofs.

The next bounded investigation can therefore be specific: choose an
interacting reference or sharper signed/support norm, derive its exact
replacement for (C4)-(C7), and test whether its construction interval
extends. That would address the first known certificate failure. It
would not by itself justify claiming the whole continuum problem solved.
