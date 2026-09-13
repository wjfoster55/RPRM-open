# Relational reference web and an inverse gap question

12 September 2026. A bounded continuation prompted by William's questions
about relating both length scales, using linked energy references, and asking
what a system cannot be. These are elementary written derivations and an
explicit research reformulation. They do not supply a new Yang–Mills gap bound.
Earlier delivered packets remain unchanged.

## 1. The two length ratios already determine a third relationship

The carrier is positive length triples (ell,L,d), with the same length unit
on all three ports. Let ell denote cell spacing, L box extent, and d a
declared reference distance. Put

```text
x=ell/d,       y=L/d,       N=L/ell=y/x.
```

This is a joint relation, not two unrelated observations. For supplied
x,y>0 its complete source fiber is

```text
{(ell,L,d)=(lambda*x,lambda*y,lambda) : lambda>0}.
```

Thus it retains the whole positive triple modulo common scaling. The third
pairwise ratio N is determined, rather than an independent new coordinate.
The cycle law is (ell/d)(d/L)(L/ell)=1.

Changing the reference to d'=c d, with c>0 supplied, gives
x'=x/c, y'=y/c. The inverse uses c, and y'/x'=y/x. If c is not supplied,
recovering the previous reference remains an open port. A consistent change
of length units instead rescales ell,L,d together and leaves x,y unchanged.

Retaining only N loses a distinction needed for a physical limiting question.
For n>1 the two positive triples

```text
(ell,L,d)=(1/n,1,1)       and       (1,n,1)
```

both have N=n. The first refines within a fixed reference-sized box; the
second enlarges the box at fixed reference-sized spacing. N alone cannot
distinguish them. All numbers here are illustrative dimensionless unit values.

## 2. Energy can be carried in the same reference web

Supply a nonnegative excitation gap Delta and two positive energy references
E_A,E_B. Their dimensionless ratios obey

```text
u=Delta/E_A,       v=Delta/E_B,       c=E_B/E_A,
u=c*v.
```

With u,v,c supplied this relation is a compatibility check. It is not a
method for computing an unknown Delta from unrelated references. At fixed
positive references, Delta>0 is equivalent to u>0 and to v>0. No universal
absolute energy unit is required.

A consistent energy-unit conversion divides Delta,E_A,E_B by the same
positive conversion factor. Every ratio is unchanged, even when a different
conversion is used at each index of a family. This must be distinguished
from changing the physical reference quantity itself.

For example, the family

```text
(Delta_n,E_A,n,E_B,n)=(1/n,1/n,2/n)
```

has constant pairwise ratios. Those ratios cannot determine its behavior
relative to a separately retained reference E_*=1, for which Delta_n/E_*→0.
This is an exact illustration of a co-scaling ambiguity, not evidence of
collapse in the actual Yang–Mills theory. An independent physical observable
can supply the reference; it need not be an absolute metaphysical scale.
Choosing the unknown gap itself as the sole reference cannot prove a claim
about that gap's relationship to another retained physical scale.

We can explicitly join the length and energy webs by declaring the energy
scales associated with lengths s through E_s=hbar*c_light/s. This uses the
supplied relativistic constants and a scale convention, not a claim that
the Hamiltonian's excitation energy equals E_s. Define

```text
g_d=Delta*d/(hbar*c_light),
g_ell=Delta*ell/(hbar*c_light)=x*g_d,
g_L=Delta*L/(hbar*c_light)=y*g_d.                         (R1)
```

On a family with g_d fixed and positive, refinement x→0 makes g_ell→0,
while increasing extent y→infinity makes g_L grow. These are compatible
descriptions of the same declared gap/reference relationship. A small
number in cell-energy units does not alone imply physical gap collapse.

Under d'=c d, g_d'=c*g_d, x'=x/c and y'=y/c. Both x*g_d and y*g_d are
unchanged. The full web transports the reference change exactly. This is
the concrete benefit of retaining the relationships jointly.

E_ell is not silently substituted for our packet's energy normalization.
The accepted quantum packet uses H/(alpha*hbar^2), so its relative gap is
Delta/(alpha*hbar^2). A comparison with E_ell must retain the conversion
factor alpha*hbar^2/E_ell and its coupling dependence.

## 3. The inverse question has an exact mathematical form

Fix a declared physical Hilbert space and self-adjoint H with attained
lowest energy E0. Put A=H-E0>=0 and let V=ker A be the complete vacuum
subspace. Supply E_ref>0 and assume the excitation set

```text
S={f in Dom(A^(1/2)) intersect V-perp : ||f||=1}
```

is nonempty. Equality is Hilbert-space equality. Use the closed quadratic
form a[f]=||A^(1/2)f||^2, which is defined on the form domain; the expression
<f,Af> alone requires the smaller operator domain. Define

```text
q(f)=a[f]/E_ref,       g=inf_(f in S) q(f).
```

The positive-relative-gap statement has the exact inverse form

```text
g>0 iff there is no sequence f_n in S with q(f_n)→0.    (R2)
```

Proof: a positive lower bound excludes such a sequence. If g=0, the
definition of infimum supplies f_n with q(f_n)<1/n for each positive n.
Those two directions prove the equivalence. It does not require an
eigenvector attaining the infimum.

Thus a usable negative question is: can non-vacuum distinctions become
arbitrarily cheap in the declared relative energy? A proof excluding all
such sequences would establish a gap without solving every eigenfunction.
The nonexistence proof remains a mathematical obligation; changing the
wording does not complete it.

The hostile distinction is exact zero versus arbitrarily near zero. On
the declared infinite carrier C*Omega plus ell^2(N), define the bounded
nonnegative operator

```text
A Omega=0,       A e_n=(1/n)e_n.
```

Every nonzero excited vector has positive quadratic-form energy, since
sum_n |f_n|^2/n>0. Nevertheless q(e_n)=1/(n E_ref)→0. There is no excited
zero eigenvector, but there is no positive gap. Restriction to
Omega,e_1,...,e_N has gap 1/N, so every finite restriction is positive
without a uniform positive family gap. This is a mathematical control;
it is not a spectrum assigned to Yang–Mills.

For a declared graph/scale family indexed by I, replace S by the disjoint
union of pairs (i,f) with f in S_i. Then

```text
inf_(i in I, f in S_i) q_i(f)>0
iff no sequence (i_n,f_n) has q_i_n(f_n)→0.              (R3)
```

The same proof applies. If only a specified scaling trajectory or its
tails are relevant, restrict I accordingly. This is not a claim about
every possible Hamiltonian, reference choice, or continuum trajectory.

Under a ground-state transform with a unique positive vacuum, orthogonality
becomes mean zero under the actual vacuum probability. It is not Haar
mean zero in the interacting problem. The accepted
[quantum bridge](../ym2_connected_vacuum/accepted_sources/ym2_global_phase_joint/GAP_BRIDGE.md)
and [residual-stack derivation](../ym2_signed_differences/DIFFERENCE_PROJECTION.md)
already preserve this distinction. Its conditional residual stack D has
the corresponding requirement ||Df||^2>=delta||f||^2 on the physical
vacuum-mean-zero space. Excluding exact invisible modes is weaker than
excluding normalized modes whose combined residual tends to zero.

## 4. A less specific enclosure can prove the answer

Let X be the complete collection of actual admissible model/state pairs for
a stated receiver. Supply a larger candidate carrier C, a map i:X→C, and
a certified lower estimate b(i(x))<=q(x) for every x in X. If

```text
inf_(c in C) b(c)>=delta>0,                              (R4)
```

then q(x)>=delta for every actual x. This is immediate by inclusion and the
lower-estimate premise. C need not determine the full vacuum or distinguish
all its states. It only needs enough constraint to answer the gap question.
This is the one-sided coverage direction described by the repository's
[proof-donut contract](../../docs/proof-donut.md).

If inf_C b=0, the test is inconclusive: extra candidates or a loose lower
estimate may cause that zero. It does not prove an actual gapless state.
A sound exclusion removes only candidates known not to be actual; an
unfinished exclusion search is OPEN. A finite list of excluded examples
does not cover every approximate-zero sequence.

Here is a complete small example of useful less-specific glue. For real
x,y with x^2+y^2=1 and rho in [-rho_max,rho_max], 0<=rho_max<=1, define

```text
q_rho(x,y)=x^2+y^2-2*rho*x*y.
```

Since 2|xy|<=x^2+y^2,

```text
q_rho(x,y)>=1-|rho|>=1-rho_max.                         (R5)
```

For fixed rho, equality is attained with |x|=|y|=1/sqrt(2) and the
sign of xy matching rho. Hence inf q_rho=1-|rho| exactly. A known
rho_max<1 excludes every low-energy cancellation below 1-rho_max while
allowing a whole continuum of unknown correlations and states.

The individual directions (1,0) and (0,1) both have energy 1 for every
rho. Yet the collective direction has energy 1-rho when rho>=0 and can
approach zero as rho→1. Looking only at each individual direction misses
the joint cancellation. The family bound on rho is what supports the
positive conclusion; no precise value of rho is needed. This example is
ordinary quadratic-form mathematics, not an asserted SU(2) effective model.

## 5. When a lens needs another port

The exact decision rule is receiver-based: if two admitted sources have
identical retained data but different answers to the requested question,
the retained data do not determine that answer. Add a distinguishing
relation, strengthen a justified law, or change the question explicitly.

The length web illustrates a redundant third ratio: L/ell follows from
ell/d and L/d. Our SU(2) witness illustrates an independent missing relation:
at a=b=0, w can be any value in [-1,1]. A new numeral's position in a list
does not decide which case applies. William's prime-seam and geometric
language remains a candidate organizing lens; a universal claim that the
third quantity always triggers a prime rule has not been proved here.

The next actual YM question remains whether the full vacuum admits enough
control to exclude arbitrarily cheap collective distinctions along the
required physical family. The current
[conditional-response obligation](../ym2_connected_vacuum/NEXT_CONDITIONAL_PORTS.md)
is one sufficient route: bound the worst local remainder responses with
a sum that stays controlled over that family. A direct form inequality or
another proved exclusion could also serve the receiver. No exact full
vacuum reconstruction is required by (R2)–(R4).

## Evidence and source boundary

The ratio identities, rebase laws, obstruction equivalences and enclosure
implication are written elementary proofs. The two operator/quadratic-form
examples are explicit controls. [check_relative_web.py](check_relative_web.py)
performs only new finite rational checks of the ratio/energy web and the
two-coordinate form identity; its [receipt](RESULTS_RELATIVE_WEB.json)
does not prove infinite-sequence coverage by finite testing.

The spectral-gap meaning and continuum construction remain those in the
[Jaffe–Witten problem statement](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).
The underlying lattice operator, domains and earlier YM results are reused
as accepted evidence. These reformulations are derived here without a claim
of mathematical novelty. No earlier checker, simulation, publication,
installation or other-lane mutation was performed.
