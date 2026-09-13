# Relation experiment 10 — contract before computation

Target: the canonical derived Kato class for E34: y²=x³−1156x, connected
real period, minimal differential dx/(2y), p=5, and the cyclotomic coordinate
chi(gamma)=6. Apply BKS Theorems 5.6 and 6.2 with explicit transport to
the Mazur–Stein–Tate (MST) height. No real BSD identity is an input.

Compute fresh exact rational multiples of P=(-2,48), Q=(-16,120), a
classical modular-symbol measure, and their combined class residue modulo
125. No stored result is an input. Earlier written rank, saturation and
5-primary Sha proofs are attributed theorem-admission dependencies.

The additional arithmetic precision depends on proving sigma(it)=i sigma(t)
over Z5 by uniqueness, hence sigma(t)/t in 1+t^4 Z5[[t]]. Preserve a failure
if that proof or any arithmetic check fails; do not silently replace it by
the expected result. An independent audit checks the evaluated formal-log
tail, including denominators divisible by 5.

Carrier: M=Z5 tensor E(Q)/torsion, with ordered basis (P,Q). Equality is
exact 5-adic equality; finite output is the quotient M/125M. The readout
receiver is the normalized canonical class, not an exact rational point.
The preimage of a computed vector k is k+125M (MANY). Incomplete global
BSD/Sha obligations remain OPEN.

The operation is a theorem-backed analytic-to-arithmetic transport, enabled
under checked BKS admission and nondegenerate height. Controls include
inverse points, torsion, basis change, wrong derivative/period factors, and
a singular Gram matrix where inversion must be rejected. No test extends
the theorem to unrelated curves or Millennium problems.
