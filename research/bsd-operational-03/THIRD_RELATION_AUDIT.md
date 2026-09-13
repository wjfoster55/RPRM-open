# E34: third relations, operational shadows, and a new regulator calculation

Date: 2026-09-12. Scope: the fixed curve `E: y²=x³−1156x` over Q,
with the proved integral free basis `P=(-2,48), Q=(-16,120)` and
`S=P+Q=(2178/49,65472/343)`.

**Result.** A common arithmetic object can carry several faithful readouts,
and the proposed two-shadow point reconstruction is a valid example. It
does not yet supply the analytic comparison. This audit also obtains a
new concrete input for the published comparison route: the ordinary
cyclotomic 5-adic height pairing is nondegenerate. In the precise
Mazur–Stein–Tate normalization below its Gram determinant is `3 mod 5`.
This calculation uses exact rational points and a proved sigma-function
remainder bound, without evaluating a p-adic infinite series numerically.

The real identity and total Sha remain **OPEN**. The old trace supplies
`Sha[5^infinity]=0`; it is a different calculation of a different invariant.

## 1. Contract and inherited inputs

The carriers are rational points with their group law; the free lattice
`Gamma=E(Q)/E(Q)_tors`; real canonical heights; 5-adic heights; finite
residue rings; and specified cohomological determinant lines. Equality in
one carrier does not identify values in another. The operation receiver
names whether it retains a point, its raw shadow, its height, or a limiting
comparison. Missing ports are the analytic comparison element and its
normalization/integrality theorem, followed separately by the actual total
Sha order.

The inherited sources are:

- [Exact analytic and height target](../bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md),
  including the real period over both components and full x-height regulator.
- [Existing theorem frontier](../bsd-identity-01/EXACT_IDENTITY_THEOREMS.md).
- [Exact trace and 5-primary result](../bsd-trace-02/TRACE_CALCULATION.md).
- [Integral basis proof](../bsd-identity-01/input_source/GENERATOR_PROOF.md)
  and [local factors](../bsd-identity-01/input_source/FACTOR_COMPARISON.md).

These give rank two, torsion order four, Tamagawa numbers four at both
bad primes, and `#E(F5)=8`. The new finite replay below checks its own
rational operations. It does not reprove the inherited rank, saturation,
local-factor, or trace theorems. Evidence grades are stated separately:
elementary written proofs; cited domain theorems; exact finite arithmetic;
and explicitly unproved comparison targets. There is no formal proof here.

## 2. A useful third object must constrain the two outputs

A precise arithmetic normalizing line is already available. Put

`D_Z = Z e_Omega tensor (wedge² Gamma) tensor (wedge² Gamma)`.

Here `e_Omega` is a specified period symbol whose evaluation is the total
real period `Omega`, including both real components. It is not silently
identified with a primitive Betti cycle. The real height determinant defines
an evaluation `rho_infinity:D_R -> R` with

`rho_infinity(e_Omega tensor (P wedge Q) tensor (P wedge Q)) = Omega Reg`.

The lattice generator is independent of a change of integral basis:
`det(U)²=1` for `U in GL_2(Z)`. The positive real evaluation fixes its sign.
This object retains the normalization, basis saturation, and determinant
law. Its construction uses no analytic Taylor coefficient.

**Integral comparison lemma — written proof.** Let `D_Z=Z e` be a rank-one
lattice, and let `rho:D_Z tensor R -> R` be a linear isomorphism with
`rho(e)>0`. Suppose an element `z` has been constructed independently of
the desired equality, and prove both

1. `z in D_Z`;
2. `rho(z)=c_an` for the actual analytic coefficient.

Then `c_an/rho(e)` is an integer. If its certified interval lies inside
`(0,2)`, that integer is one and `z=e`. Indeed `z=n e` for one integer n;
linearity gives the quotient n and the interval forces n=1. This proves
the lemma. Membership in `(1/d)D_Z` instead yields denominator dividing d;
a sufficiently narrow interval gives the corresponding separation test.

For E34 the accepted quotient interval
`[0.999920542,1.000092816]` would finish this argument immediately.
The new theorem obligation is the existence of the independently defined
`z` with those two properties. Defining `z=rho^(-1)(c_an)` proves the
comparison by definition and leaves lattice membership entirely unresolved.
Retaining `(c_an,Omega Reg)` in a product object likewise preserves both
numbers without restricting their ratio.

Thus the third object is mathematically useful when it brings an integral
lattice, a nontrivial comparison theorem, or a conserved relation. A common
container with two decoders is only the first part of that construction.

## 3. Operational comparison and joint shadows

**Operational comparison lemma — written proof.** Let X be a reached state
carrier with partial actions `T_a`, observations `A,B:X->R`, and a retained
correction `V:X->R`. Suppose:

- every initial state satisfies `A-B-V=0`;
- each admitted update satisfies
  `(A-B-V)(T_a x)=(A-B-V)(x)`;
- a specified execution is enabled at every stage, covers the intended
  approximants, and has `A(x_n)->A_*`, `B(x_n)->B_*`, `V(x_n)->0`.

Then `A_*=B_*`. Induction proves the invariant for every finite prefix;
the three proved limit statements give the conclusion. A quotient state
used to run the proof must preserve enabledness and successor classes as
well as the named observations. These conditions are the precise extra
work beyond placing both approximants in a shared state.

Applied to the existing analytic/height series, this recovers the exact
matching and terminal-boundary obligations in that note. Defining V to be
the current defect makes the invariant automatic but supplies no new
terminal estimate. A bounded symbolic family of corrections is a valid
place to search; passing finitely many instances is not its continuation
proof.

**Joint-shadow criterion — written proof.** For maps `s_i:X->Y_i`, the
joint map `s=(s_i)` preserves a requested readout Q exactly when

`s_i(x)=s_i(y) for every i  =>  Q(x)=Q(y)`.

Necessity follows from any decoder; sufficiency defines the decoder using
any fiber representative. For additive error carrier M and homomorphisms
`s_i`, exact recovery of an error is equivalent to
`intersection_i ker(s_i)={0}`. Indeed equal shadows mean that the difference
lies in that intersection. A restricted admitted error family only needs
separation of differences that can actually occur in that family.

Statistical independence is not required for this deterministic theorem.
Two dependent maps can jointly separate points. Conversely, two separately
implemented calculations may share a wrong orbit, normalization, or
theorem hypothesis. Evidence diversity and mathematical separation are
different obligations. Each claimed shadow needs calibration against the
actual source, and shared witnesses must stay joint.

For example, finitely many modular residues cannot separate arbitrary
integers: the joint kernel contains their modulus least common multiple.
A complete size bound can make the same residues separating on a bounded
carrier. The size bound is part of the mathematical contribution.

## 4. Audit of the actual E34 two-shadow repair

Write `r(R)=Y/(2X)` and `T0=(0,0)`. Away from the exceptional points,
the other occurrence with the same r is

`tau(R)=-R+T0=(-1156/X,-1156Y/X²)`.

It has the same r, while `[2]tau(R)=-[2]R`. Thus
`r([2]tau(R))=-r([2]R)` whenever both finite values are defined. This is
an exact obstruction to updating the **raw r summary** under doubling.

The second readout removes that ambiguity. Set `r1=r(R)`, `r2=r([2]R)`
and

`V=(r1^4-289)/(2 r1 r2)`.

Then the inverse is

`X=2(V+r1²),   Y=2 r1 X`.

To check it, the curve equation gives `r1²=X/4-289/X`. Consequently
`V=X/4+289/X=X/2-r1²`, and `V²=r1^4+289`. Substitution of the
ordinary duplication formula gives
`r2=(r1^4-289)/(2 r1 V)`, which proves the displayed inverse wherever
its denominators are nonzero. Under tau, V changes sign.

The formula admits `E\E[4]` over a characteristic-zero field for a single
read. That domain alone is not doubling-closed: order-eight points leave
it. Rational nontorsion points, or the retained finite torsion carrier
with nonzero primitive 17-component, supply appropriate closed domains.
Exceptional points require their own tags or a separate branch.

The exact replay gives:

| Source | r1 | r2 | V |
|---|---:|---:|---:|
| P | -12 | 20447/3480 | -145 |
| Q | -15/4 | -23359/42360 | -353/16 |
| S | 496/231 | -762373664513/215381110560 | 939905/53361 |

There is a consequential receiver distinction. Canonical height satisfies
`q(tau(R))=q(R)` because sign and torsion translation preserve it. Hence
`q([2]^n tau(R))=q([2]^n R)` for every n. The old r shadow therefore
preserves the height-only doubling receiver even though its **own** raw
update is not well defined. The two-shadow repair is an earned point and
trajectory reconstruction; it is not evidence that height was previously
undefined on each r fiber. This is the handbook's distinction between
answering all future observations and updating an unnecessarily detailed
summary. Mixed additions, occurrence recovery, and raw trajectory readouts
can demand the stronger representation.

Restoring a point from its two shadows also restores the possibility of
computing its heights. It does not select a unique arithmetic generator
corresponding to the analytic coefficient. Integral basis changes, period
scalings, finite-index sublattices and analytic normalizations retain their
separate determinant factors until proved compatible.

There is also an actual source boundary: the critical trace uses finite
torsion points in `E[68]`, whereas P and Q generate the rational free
lattice. Extending canonical height to algebraic points still gives zero
on that torsion carrier: its doubling orbit is finite, so its unscaled
heights are bounded and division by `4^n` tends to zero. The repaired
torsion representation does not by itself produce P, Q, or their positive
regulator. A construction of arithmetic classes crossing that boundary
would supply additional mathematical content.

## 5. An exact 5-adic regulator calculation

Mazur–Stein–Tate give an odd integral sigma function and, for suitably
prepared points, the height formula
`h_5(R)=log_5(sigma(t_R)/d_R)/5`, with
`h_5(R)=-(R,R)_5/2`. Their cyclotomic functional is `log_5/5`.
[Theorem 1.3 and equation (1.1)](https://wstein.org/papers/pheight/pheight.pdf#page=3),
[Algorithm 3.4](https://wstein.org/papers/pheight/pheight.pdf#page=16).

Here take `m=lcm(4,4,8)=8`. Thus 8R is in the identity component at both
bad primes and reduces to O at 5. Write its exact primitive coordinates
as `(a/d²,b/d³)`, with `d>0`, and put `t=-ad/b`, `u=t/d=-a/b`.
The replay finds `v5(t)=1` for R=P,Q,S.

Since the model has `a1=a3=0`, group inversion sends t to -t. Oddness and
integrality therefore give

`sigma(t)/t in 1+t² Z5 subset 1+25 Z5`.

The logarithm of this factor lies in `25 Z5`. Quadraticity and m²=64 give

`h_5(R) = (1/320)log_5(sigma(t)/d)`

and hence

`h_5(R) = (1/320)log_5(u) mod 5`.

The congruence is justified because the discarded logarithm is divisible
by 25 while `v5(320)=1`. For a 5-adic unit u,
`log_5(u)=log_5(u^4)/4`; the usual logarithm expansion gives
`log_5(u^4)=u^4-1 mod 25`. Thus the entire residue calculation is

`h_5(R) = 64^(-1) * ((u^4-1)/5) * 4^(-1) mod 5`.       (H)

Use `u^4 mod25` before dividing its difference from one by five. Changing
its integral representative by a multiple of 25 changes that quotient
by a multiple of five, so (H) is well defined.

| R | u mod25 | u^4 mod25 | h_5(R) mod5 |
|---|---:|---:|---:|
| P | 9 | 11 | 2 |
| Q | 19 | 21 | 4 |
| S | 19 | 21 | 4 |

For the quadratic form h, polarize with a half:
`b_h(P,Q)=(h(S)-h(P)-h(Q))/2`. Its Gram matrix is

`[[2,4],[4,4]] mod5`, with determinant `2 mod5`.

For MST's bilinear pairing `( , )_5=-2 b_h`, the matrix is

`[[1,2],[2,2]] mod5`, with determinant `3 mod5`.

Both determinants are units. This proves nondegeneracy over Q5. The
literal residue is tied to the named normalization; changing a cyclotomic
coordinate can change it. Nonvanishing survives any proved nonzero scalar
change of normalization.

This is a finite calculation of a new BSD-relevant input. It is not a
numerical comparison with the real regulator, and it does not claim the
two regulators take values in the same field.

## 6. Relation to the cohomological third object

Burns–Kurihara–Sano provide a specific determinant-line formulation and a
derived Kato element. Their Proposition 4.14 identifies the needed
rank-two comparison as their still-conjectural Generalized Perrin–Riou
identity. Their Theorem 5.6 gives
`<x,R_Boc>_5=log_omega(x) R_5`. Their Theorem 7.6 has additional main
conjecture and comparison hypotheses and concludes a p-part statement.
[Proposition 2.6](https://kurihara.math.keio.ac.jp/bks4.pdf#page=13),
[Proposition 4.14](https://kurihara.math.keio.ac.jp/bks4.pdf#page=28),
[Theorem 5.6](https://kurihara.math.keio.ac.jp/bks4.pdf#page=34),
[Theorem 7.6](https://kurihara.math.keio.ac.jp/bks4.pdf#page=56).

The new computation advances a concrete hypothesis. Independent point
counting at the good prime three gives `a3=0`. Its Frobenius polynomial
`X²+3` is irreducible over F5, since its discriminant is `3 mod5` and
the squares modulo five are `0,1,4`. Thus E[5] is irreducible: an invariant
line would give a Frobenius eigenvalue in F5. Their Remark 2.3 supplies
the required freeness for `T=T5(E)`. Positive rank is inherited and
`Sha[5^infinity]=0` supplies the primary finiteness required by their
Hypothesis 2.2. Their comparison with the classical ordinary cyclotomic
pairing transports the nondegeneracy just computed. The nonzero rational
point P has nonzero local logarithm: on the good-reduction formal group
at five the logarithm is injective, and multiplication by eight moves P
there. Otherwise 8P would be O, contradicting its infinite order.
The displayed pairing identity therefore implies `R_Boc != 0`.

This implication is a deduction using the cited height-comparison theorem,
not a claim that the two regulator residues are literally identical in
different coordinate conventions. It supplies the previously uncomputed
Bockstein nonvanishing input. It does not establish their conjectural
comparison or a full main-conjecture specialization.

The strongest surviving third-object candidate is consequently concrete:
an arithmetic cohomology/determinant object with its integral lattice,
norm-compatible zeta data, and regulator comparison maps. Its exact new
constraint would be a theorem identifying the independently defined
derived zeta element with the normalized arithmetic regulator element.
An element defined from the analytic coefficient is useful notation, but
its integrality or equality to independent zeta data remains the theorem.

## 7. A hostile limit test on the actual curve

The proved 5-primary vanishing and Kummer exact sequences identify each
`Sel_(5^n)(E/Q)` with `Gamma/5^n Gamma`, compatibly with reduction. The
inverse-limit carrier is therefore the 5-adic lattice `Gamma tensor Z5`.
This is a legitimate common arithmetic object with explicit operations.

It cannot support a continuous real canonical-height decoder extending
the height on Gamma. In that carrier `5^n P -> 0`, while quadraticity
gives `q(5^n P)=25^n q(P) -> +infinity`, since P is nontorsion.
Continuity at zero would require convergence to `q(0)=0`, a contradiction.

This refutes one precise adapter, not every possible arithmetic–analytic
bridge. Retaining the integral source lattice, a real embedding, or a
different comparison object changes the carrier and can preserve the
missing information. The point is to state those added ports explicitly.

## 8. Reproduction and remaining theorem

The durable [main height calculation](work/padic_height.py) has a separate
[independent readback](work/padic_height_readback.py), which imports none
of its arithmetic. The readback uses the closed duplication polynomials

`x(2R)=(x²+1156)²/(4y²)`

`y(2R)=(x^6-5780x^4-5*1156²*x²+1156³)/(8y³)`.

It reconstructs P+Q, repeats three duplications, verifies all three
eightfold point witnesses and their primitive coordinates, checks the
bad-prime connected-component reductions, and recomputes the height
residues and Gram determinant. Its fresh
[receipt](evidence/padic_height_readback.json) also records the complete
point counts at three and five and the Frobenius irreducibility test.
It never reads the main calculation's saved status or theorem conclusion.
The ring of exact rational arithmetic and the cited domain theorems remain
shared dependencies, stated openly.

Run with a previously unused output path:

```powershell
python -I -B research/bsd-operational-03/work/padic_height_readback.py --witness research/bsd-operational-03/evidence/padic_height.json --output research/bsd-operational-03/evidence/padic_height_readback_fresh.json
```

The following standard-library replay reconstructs the three points and
the residues from their rational coordinates. It reads no prior PASS or
trace value. It was executed successfully for this audit.

```python
from fractions import Fraction as F
from math import isqrt

def add(A, B):
    if A is None: return B
    if B is None: return A
    x,y=A; z,w=B
    if x==z and y==-w: return None
    s=(w-y)/(z-x) if x!=z else (3*x*x-1156)/(2*y)
    u=s*s-x-z
    return u,s*(x-u)-y

def v5(q):
    n,d=q.numerator,q.denominator
    if not n: raise ValueError('zero has no finite valuation')
    v=0
    while n%5==0: n//=5; v+=1
    while d%5==0: d//=5; v-=1
    return v

P=(F(-2),F(48)); Q=(F(-16),F(120)); S=add(P,Q)
h=[]
for name,R in [('P',P),('Q',Q),('S',S)]:
    R8=R
    for _ in range(3): R8=add(R8,R8)
    x,y=R8
    d=isqrt(x.denominator)
    assert d*d==x.denominator
    a=x.numerator; b=y*d**3
    assert b.denominator==1
    b=b.numerator
    assert b*b==a**3-1156*a*d**4
    assert v5(-x/y)==1
    u=(-a*pow(b,-1,25))%25
    H=((pow(u,4,25)-1)//5)*pow(4*64,-1,5)%5
    h.append(H)
    print(name,u,H)
p,q,s=h
b=(s-p-q)*pow(2,-1,5)%5
assert h==[2,4,4]
assert (p*q-b*b)%5==2
assert (4*(p*q-b*b))%5==3
print('polar-half determinant mod5:',(p*q-b*b)%5)
print('MST pairing determinant mod5:',4*(p*q-b*b)%5)
```

**Verified here:** the rational two-shadow inversion at P,Q,S; its
universal algebra and receiver distinction; the written comparison and
joint-shadow lemmas; the exact mod-five height residues and regulator
nonvanishing. The p-adic height interpretation and Bockstein implication
have the explicit published dependencies above.

**Next theorem-bearing calculation:** construct or calculate the rank-two
derived zeta class in the normalized cohomological line and compare its
coordinates with the now-nonzero Bockstein regulator. Finite congruences
would test a proposed relation; proving it requires compatible all-level
construction and its exact comparison law. The missing complex identity
is still the rank-two analytic coefficient comparison, or the weaker
effective bounded-rationality/integrality statement sufficient to invoke
Section 2. Total Sha additionally needs complete primary coverage or a
theorem identifying the real coefficient with its actual finite order.

No paper, prior lane, dependency file, or commit was changed by this audit.
