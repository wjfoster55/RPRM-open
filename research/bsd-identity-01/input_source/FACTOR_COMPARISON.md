# E34: the remaining BSD factor comparison

This is a rigorous interval comparison, not a determination of the order
of Sha. The curve is always E: y²=x³−1156x. It is not y²=x³+34x.

## The period and its convention

Use the minimal differential ω=dx/(2y) on the integral minimal model
proved in `LOCAL_ANALYTIC_INPUTS.md`. The real period used here is
Ω=∫_{E(R)}|ω|, including both real components. Translation by a point
on the other component preserves this differential, so the two
components have equal volume.

Writing n=34, the component through infinity has volume

    I = integral_n^infinity dx/sqrt(x(x²−n²)).

The two branches y=±sqrt(x(x²−n²)) each contribute half this integral.
The substitution x=n/u² gives

    I = (2/sqrt(n)) integral_0^1 du/sqrt(1−u⁴)
      = 2 K(1/sqrt(2))/sqrt(2n).

For the last identity one can set u=sin(θ)/sqrt(2−sin²(θ)); its
Jacobian gives du/sqrt(1−u⁴)=dθ/sqrt(2−sin²(θ)). Thus

    Ω = 2I = 4K(1/sqrt(2))/sqrt(68)
      = 2π/(sqrt(68) AGM(1,1/sqrt(2))).

The relation K(k)=π/(2 AGM(1,sqrt(1−k²))) is the standard AGM
identity ([DLMF 19.8](https://dlmf.nist.gov/19.8#E5)).
`work/factor_frontier.py` bounds square roots by integer squares and π
by alternating rational Machin series. Seven arithmetic/geometric
iterations preserve lower and upper bounds on the AGM. All rounding
is outward on a rational grid. The result is

    0.899358321446 ≤ Ω ≤ 0.899358321447.

## The regulator and local factors

`GENERATOR_PROOF.md` proves that P=(−2,48), Q=(−16,120) are an
integral basis modulo K={O,(0,0),(34,0),(−34,0)}. Its height is

    q(R)=lim_j 4^(−j) log H_x(2^jR),
    B(R,S)=(q(R+S)−q(R)−q(S))/2.

The regulator here is det(B(P_i,P_j)), using the full x-height limit.
Equivalently, if hhat=q/2, the pairing for this determinant is
hhat(R+S)−hhat(R)−hhat(S). A convention which instead halves that
pairing must adjust the displayed BSD formula accordingly. This is the
normalization used in [Cremona, chapter 3, §3.4, pp.71–72](https://johncremona.github.io/book/fulltext/chapter3.pdf#page=10).
The exact interval calculations give

    7.099053962 ≤ Reg ≤ 7.100201634.

The factor script reassembles this determinant from the three certified
height intervals; it does not use the regulator's rounded display as
an exact number. The local proof gives c_2=c_17=4, and the complete
torsion group has order 4. Hence (product_p c_p)/|E(Q)_tors|²=16/16=1.

## What the quotient proves, and what it does not

Let c₂ denote the analytic coefficient L''(E,1)/2, distinguished from
the local Tamagawa number c_2 above. The analytic proof gives

    6.38511803 ≤ c₂ ≤ 6.38518585.

The full BSD formula for these conventions would say

    c₂ = Ω Reg #Sha(E/Q).

Using the exact rational intervals behind each display, the factor
script obtains

    0.999920542 ≤ c₂/(Ω Reg) ≤ 1.000092816.

This contains just one positive integer, namely 1. It also contains
infinitely many nonintegers. No result in this experiment identifies
the quotient with #Sha or proves it integral. Consequently the
unconditional conclusion is the interval comparison only. If an
independent applicable theorem established the exact BSD identity,
this interval would then force #Sha=1.

The arithmetic proof already establishes Sha[2^∞]=0. It does not
establish the odd-primary groups, total finiteness, or the displayed
identity. `FULL_BSD_FRONTIER.md` records the bounded theorem review
and actual missing hypotheses. The published low-rank theorem used
to identify analytic rank does not supply the leading-coefficient
formula in rank two.

## Checks and limits

The factor script binds the fresh analytic and generator receipt bytes
to their source bytes before comparing them. Its dependencies still
include the written local, saturation, and analytic proofs. A hash
does not prove these mathematical dependencies.

Controls using one real component, a halved height pairing, and a
hypothetical index-three subgroup move the quotient by factors 2, 4,
and 1/9 respectively. They show sensitivity to convention errors;
matching 1 is never used to choose a convention or prove an identity.

Evidence grade: written proof plus exact rational interval computation;
standard theorem dependencies are cited. No proof assistant was run.
