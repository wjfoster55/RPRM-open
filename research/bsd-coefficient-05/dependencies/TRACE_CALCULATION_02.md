# Exact trace calculation and the 5-primary conclusion

The new result for E: Y²=X³−1156X is

    Sha(E/Q)[5^infinity] = 0.

This follows from a finite exact calculation and the published criterion
specified below, using the earlier proved algebraic and analytic ranks2.
It does not identify the total Sha group or prove the complex BSD identity.

## What was computed

For the distinguished period-defined rho on E': y²=x³+289x, put

    T = Tr_(H_f1/K)(2rho^5+289rho),
    K=Q(i), f=68, f1=34(1−i), [H_f1:K]=256.

The corrected CLS formula and the explicit period scaling give

    c5_plus(E) = ±16T/68^5.

The multiplier is a unit at5. This is a noncentral critical Hecke value,
not a calculation of L''(E,1)/2. The model, conductor and normalization are
derived in the previous [odd-prime admission](../bsd-identity-01/ODD_PRIME_ATTEMPT.md).
The [new action proof](TRACE_FORMULA_AUDIT.md) checks the square-D case and
identifies the actual orbit. The faulty direct even-D conductor substitution
recorded earlier is not used; the odd auxiliary model supplies f=68.

For a certified primitive P in E[68], define r(P)=Y/(2X). The dual
2-isogeny has x-coordinate r(P)^2 and doubles the uniformizing parameter.
Consequently r at the distinguished primitive point equals ±rho. Fresh
point counts at5 and13 give Gaussian Frobenius actions −1±2i and−3±2i.
They generate the complete arithmetic image G of order512 modulo68.

The involution j=33+34i fixes r and moves P. Every r value has exactly two
point occurrences. Hence the quantity evaluated by the main program is

    S(P) = (1/2) sum_(g in G) [2r([g]P)^5+289r([g]P)].

Every primitive seed is a Galois conjugate of the distinguished seed,
multiplied by one Gaussian unit. Both terms of the integrand transform by
that same unit, so S(P)=epsilon T for epsilon in {1,−1,i,−i}.
This is a proof of valuation preservation, not a guess about the seed.

The fresh default run obtains

    S(P) = 100 modulo125,       v5(S(P)) = 2.

All fifteen nonconstant coefficients in the extension-ring result vanish.
The companion run modulo25 obtains0 and its lifted point agrees with the
modulo125 point after reduction. In particular, coarse zero did retain a
nonzero next-level remainder. Since100=4·25 is nonzero modulo125, these
exact residues prove the valuation is2; there is no numerical recognition.

## Finite field, torsion lift and exceptional cases

The implementation uses R_m=(Z/mZ)[z]/(z^16−2), for m=25 and125. It
certifies irreducibility over F5 by Rabin's criterion: z^(5^16)=z and
gcd(z^(5^8)−z,z^16−2)=1. The only prime divisor of16 is2, so this is the
complete criterion. The integral polynomial gives the unramified degree16
lift. The chosen i is57, whose square is−1 modulo125.

A deterministic finite-field search constructs an on-curve seed. Its
Frobenius-based cofactor is only a search aid. Admission depends on direct
checks:

    [68]P=O,
    [34−34i]P != O, [16−4i]P != O, [16+4i]P != O.

These test each Gaussian prime dividing68. They certify the complete CM
annihilator, including both split17 components. A point of integer order68
on only one split component is rejected.

The lift solves the curve equation and y([34]P)=0. First, Newton's method
corrects y with x held fixed. A dual-number calculation differentiates the
second equation along the curve, with dy/dx=(3x²−1156)/(2y). Its derivative
is a unit at5; each Newton correction raises the precision. In the recorded
run the residual valuations are1,2,3, where3 means zero modulo125.

The final point is checked on the curve, checked to reduce to the original
seed, checked by all four torsion/primitivity tests, and checked to have
[34]P among the three explicit nonzero two-torsion points. Thus the result
is the prime-to5 torsion lift, independently of trusting Newton's history.
Finite etaleness of E[68] at5 makes that lift unique.

The affine group law treats O, inverse pairs and doubling separately.
An inverse is accepted only when its denominator has nonzero reduction;
the implementation checks the resulting product is1. On the lifted
prime-to5 torsion group, equal/opposite reductions lift to exactly
equal/opposite points. Therefore there are no silently accepted divisions
by multiples of5. Primitive points cannot reduce to the poles O or(0,0)
of r. The concrete orbit additionally checks512 distinct points,256
distinct r values, fiber size2, and the explicit involution.

## Independent checks and their precise limits

The [character-weighted construction](DIVISION_ORBIT.md) uses a separate
group law on E', a primitive17 point, two chord identities and the
quadratic character of Norm(alpha) modulo17. It obtains25 modulo125,
up to the coherent overall sign. That is the negative of the first residue
and has the same valuation. It reads only the supplied point witness,
then verifies its own torsion conditions; it does not read the saved trace
or status. The finite-ring class is shared and is explicitly attributed.

The separate readback uses independently implemented ring multiplication
to recompute the terms and Newton sums from the complete supplied orbit.
It checks the leading five polynomial coefficients and the signed trace
identity. It does not independently establish which orbit is arithmetic:
that identification is supplied by the written CM proof and point checks.

For this seed those five coefficients, in descending monic order, are
0,30,36,57,120 modulo125. Since a1=0 at this precision, the signed Newton
combination reduces to10(a2 a3−a5)=10(30·36−120)=100 modulo125.
Only the reductions of a2,a3,a5 modulo25 are needed for this last step.

The portable runner snapshots the executable source into a fresh run
directory and creates all its numerical evidence there. Existing receipts
are not inputs. The new result is a reproducible computation supporting a
written proof with explicit theorem dependencies, not a formal proof.

## Applying the theorem

[Coates–Liang–Sujatha I, Theorem2.2](https://arxiv.org/pdf/0901.3832#page=5)
applies to this CM curve at5. Good reduction, splitting in Q(i), the
period-factor unit condition, and primality to the roots-of-unity order
hold. The two ranks are2, so their required parity agrees. Direct counting
gives #E(F5)=8, prime to5; also5 is prime to6. Finally the newly computed
valuation equals the algebraic rank2. The theorem therefore gives trivial
5-primary Sha over K. Restriction followed by corestriction is multiplication
by2, invertible on a 5-primary group, so the rational-field group is trivial.
The rationality of T covers both primes of K over5; the arbitrary seed's
Gaussian unit does not change either valuation.

The critical trace normalization uses [CLS II, equation(77)](https://arxiv.org/pdf/1005.4206#page=19),
which corrects the older factor4. The orbit proof uses its conductor-field
statements at their stated hypotheses, including the allowed square17².
No odd-valuation lemma is applied to that square.

The earlier rank proofs remain attributed dependencies, not new runs of
this experiment. Copies are supplied in `dependencies/`. The earlier
two-primary conclusion combines with the new result to exclude2 and5
from any nontrivial Sha-primary component. All other primary components,
the finiteness/total order of Sha, and the full complex BSD leading
coefficient formula remain unproved by this calculation.
