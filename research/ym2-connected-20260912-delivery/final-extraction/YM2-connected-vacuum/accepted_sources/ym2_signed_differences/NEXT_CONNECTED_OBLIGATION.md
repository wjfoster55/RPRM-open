# The next obligation: retain connected vacuum responses

12 September 2026. Written continuation of the proved fixed-graph bound.
This note proves a limitation of the absolute-support estimate and a local
conditional-density comparison. It does not establish the required locality
properties of the SU(2) quantum vacuum.

## 1. Why the four-support argument does not repeat unchanged at every level

For a finite graph, the same zero-integral residual expansion gives

```text
|K_phys,s-1| <= eta_G(d),
eta_G(d)=sum_(nonempty edge supports S with no leaf) d^|S|,
|q_s-1| <= d.
```

This is an upper-bound envelope. The two-cell graph has exactly the four
supports described in [VACUUM_COMPARISON.md](VACUUM_COMPARISON.md).

Now suppose a larger graph contains `N` edge-disjoint square cycles.
Every nonempty union of those cycles is a different support without a
leaf, even if some cycles share vertices. If `k` cycles are selected its
support size is `4k`. Therefore

```text
eta_G(d) >= sum_(k=1)^N binomial(N,k) d^(4k)
          = (1+d^4)^N-1.                                 (C1)
```

This lower bound on an upper-bound envelope is not a lower bound on the
actual kernel deviation. With the certified one-link estimate `d=3/5`
used in this task, `N=6` already gives `(1+(3/5)^4)^6-1>1`.
Thus the particular inference `K_phys>=1-eta_G(d)>0` stops yielding a
positive lower bound at that fixed heat time on such a larger graph.
Actual cancellations or a different estimate can still work.

This is a concrete obstruction to simple repetition of the two-cell proof.
It does not assert that the physical gap vanishes after six cycles. The
product-law example in [STACKING_AND_SCALING.md](STACKING_AND_SCALING.md)
already shows that a worsening global comparison can coexist with a fixed
true auxiliary gap. Counting every disconnected combination by absolute
value can pay exponentially for effects that need not obstruct mixing.

## 2. What cancels exactly in a conditional joint

Let a strictly positive density on a finite product space with reference
product probability have the explicit factorization

```text
rho(U) = Z^-1 product_C w_C(U_C),     w_C>0.              (C2)
```

The carrier can include compact SU(2) coordinates. Supply a finite family
of factors and bounded logarithms, so normalization and all formulas below
are well-defined. This is an additional hypothesis about `rho`, not a
consequence of its origin as a quantum ground-state density.

For a patch `B` and fixed outside configuration `omega`, the normalized
conditional density on the inside variables is proportional to

```text
product_(C: C intersects B) w_C(U_(C intersects B),omega_(C outside B)).
```

Every factor entirely outside the patch cancels between numerator and
normalization. Suppose two exteriors differ only at edge `j outside B`.
The log of their *unnormalized* inside-density ratio is

```text
h_B,j(U_B) = sum_(C: C intersects B, j in C)
              [log w_C(U_B,omega')-log w_C(U_B,omega)].  (C3)
```

Thus only factors that connect the changed exterior occurrence to the
patch enter this conditional comparison. Independent distant factors
cancel exactly, irrespective of their number or bias. This is the useful
joint operation: retain the shared variables and cancel factors that are
common to the two complete conditional constructions.

## 3. An exact bounded-tilt lemma

Let `eta` be any probability and let
`deta'=exp(h)deta / integral exp(h)deta`, with finite
`L=ess sup h-ess inf h`. Then

```text
TV(eta',eta) <= tanh(L/4).                               (C4)
```

Here total variation is `sup_A |eta'(A)-eta(A)|`, equivalently half
the integral absolute density difference. To prove (C4), put
`z=exp(h)`, `a=ess inf z`, `b=ess sup z`, `c=E_eta z`.
When `a=b` the measures agree. Otherwise `a<=c<=b`, and the chord
bound for the convex function `|z-c|` gives

```text
TV = E|z-c|/(2c)
   <= (b-c)(c-a)/[c(b-a)]
   <= (sqrt(b)-sqrt(a))/(sqrt(b)+sqrt(a))
    = tanh(log(b/a)/4).
```

The middle expression is maximized at `c=sqrt(ab)`: after multiplication
by `b-a`, it is `a+b-c-ab/c`, and `c+ab/c>=2sqrt(ab)`.
The two-point law on `z in {a,b}` with mean `sqrt(ab)` attains the bound,
so this is sharp over the supplied bounded-tilt class. The proof applies
to continuous carriers without discretizing them.

For (C3), if `osc(log w_C)` denotes the full factor oscillation, then

```text
osc_(U_B) h_B,j <= 2 sum_(C: C intersects B, j in C) osc(log w_C).
```

Combining with (C4) yields a proved conditional influence bound that
depends on factors connecting `j` to `B`, not on every factor in the
whole system. The exact response can be smaller. No uniform bound on
the displayed sum is supplied by this algebra alone.

## 4. The actual Yang–Mills vacancy

Our quantum density is `rho=psi_0²`. The Hamiltonian potential is a sum
of local plaquette terms, but this does not prove that `log rho` is the
same local sum, or even a uniformly controlled sum of local interactions.
It is not permissible to substitute the classical density `exp(-V)`
for the ground-state measure.

The next usable result would establish a uniform response estimate for
the true vacuum conditionals, either directly or through a rigorously
controlled connected-factor description. A claimed description must carry
its full remainder or an error bound adequate for the variance receiver.
If an influence criterion is then used to infer a spectral estimate,
its hypotheses and update rates must also be checked on this carrier.

The distinction between global bounded perturbations and local weak
dependence is established in functional-inequality research. For context,
[Caputo, Menz and Tetali, Lemma 2.2 and Theorem 2.1](https://arxiv.org/pdf/1405.0608)
separate a crude global comparison from conditions on conditional laws.
Their theorem is not asserted to apply to this unknown SU(2) vacuum merely
because the Hamiltonian itself has local terms.

The exact small controls are retained in `check_stacking.py`: the
six-cycle envelope and sharp rational two-point tilt examples. The
general support and tilt statements have the written proofs above.
Uniform quantum-vacuum control, physical scaling, and continuum
construction remain OPEN; no new physical interaction law is postulated.
