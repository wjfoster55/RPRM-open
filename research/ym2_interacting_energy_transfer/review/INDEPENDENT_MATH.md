# Independent witness derivation

2026-09-12. Read-only subagent `/root/independent_witness`; this file captures
its returned mathematics, formatted by the payload owner. It did not edit the
payload or rerun YM1. Its derivation was conducted alongside the owner's work.

For `g=V=1`, the diagonal invariant sector has
`W=Σ_{i<j}q_i²q_j²/2`, `dot q=p`, `dot p=−f`, with

`f_i=q_iΣ_{j≠i}q_j²`, `M_ii=Σ_{j≠i}q_j²`, `M_ij=2q_iq_j`.

The independently derived identities are

`J=f·p`, `K=pᵀMp−|f|²`,
`L=∇³W[p,p,p]−4pᵀMf`,
`∇³W[p,p,p]=6Σ_{i<j}(q_i p_i p_j²+q_j p_j p_i²)`.

The proposed base pair `q=(1,1,0)`, `p=(0,0,1)` and
`p=(2/3,−2/3,1/3)` gives `(E,B,J)=(1/2,1/2,0)` and `K=0,−8/3`.
The recommended all-nonzero-commutator refinement pair `q=(1,1,1)`,
`p=±(1,1,−2)` gives `(E,B,J,K)=(3,3/2,0,−12)` and `L=±36`.
An additional unequal-amplitude pair `q=(1,2,0)`, `p=±(1,−2,0)` gives
`(E,B,J,K)=(5/2,2,0,−28)` and `L=±48`.

A separate Python `Fraction` calculation used

`(n+2)(n+1) q_i[n+2] = −[t^n](q_i Σ_{j≠i}q_j²)`

and direct multiplication of the resulting series into `W`, without the
derivative formulas. It reproduced:

- A: `1/2−5t⁴/6+O(t⁶)`.
- B: `1/2−4t²/3+71t⁴/54+O(t⁶)`.
- Refined ±: `3/2−6t²±6t³+33t⁴/2∓33t⁵/5+O(t⁶)`.
- Planar refined ±: `2−14t²±8t³+97t⁴/3∓178t⁵/5+O(t⁶)`.

Gauss vanishes termwise. `dot E=−J` proves total-energy conservation.
Within each pair the initial gauge fields and spatial holonomies are identical.
Unequal gauge-invariant derivatives exclude gauge equivalence. The velocity
sign reversal is time reversal, not a gauge identification, and the receiver
fixes the same future direction.

For general `g,V`, define derivatives using the magnetic density
`W=g²Σq_i²q_j²/2`, then multiply `J,K,L` by `V`. Canonical integrated momentum
is `Π=Vp`, not `p` before volume is set to one. Polynomial dynamics and the
first unequal Taylor coefficient supply exact nearby-time separation.

This independent check supports the stated counterexamples. It does not
enumerate the full unconstrained source fiber, certify general checker
soundness, or establish a quantum spectral result.
