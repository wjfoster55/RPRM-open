# Independent review of the gauge-averaged heat comparison

12 September 2026. Bounded mathematical review of the refinement in
[VACUUM_COMPARISON.md](VACUUM_COMPARISON.md). This review uses the accepted
full seven-link, six-vertex source contract in
[GAP_BRIDGE.md](accepted_sources/ym2_global_phase_joint/GAP_BRIDGE.md). It does not rerun
the old graph or quantum checkers and does not promote this graph to a
uniform lattice family.

**Finding:** the proposed bound

```text
R_actual <= exp(32r/3) (104207/52043)^2,
gamma >= 6 alpha hbar^2 exp(-32r/3) (52043/104207)^2
```

follows under that full source contract. The pruning is valid before the
positive ground-state comparison because the ground state is gauge
invariant. The written reasoning and exact constants were independently
checked below. The new comparison is a stronger sufficient bound, not an
exact vacuum or spectral-gap calculation.

The completed Section 2a and the exact-arithmetic source
[check_vacuum_comparison.py](check_vacuum_comparison.py) were inspected
after the refinement was written. Their support, tail, and normalization
statements agree with this independent derivation; no blocking issue was
found. The implementation uses degree-16 Taylor sums, which are stronger
than the smaller sufficient degrees recorded below.

## 1. What is being averaged

Let `s=kappa t`, where `kappa=alpha hbar^2/2`. The free seven-link heat
kernel against normalized product Haar measure is

```text
K_s(x,y)=product_e q_s(x_e y_e^-1).
```

Let `T_g` be the full vertex action and let `dg` denote normalized Haar
probability on all six vertex groups. Define

```text
K_s^phys(x,y)=integral K_s(x,T_g y) dg.                  (H1)
```

The comparison note instead averages `K_s(T_g x,y)`. These are the same
kernel: simultaneous gauge invariance gives
`K_s(T_g x,y)=K_s(x,T_g^-1 y)`, and Haar inversion preserves `dg`.

For every invariant integrable `f`, Haar invariance and the substitution
`z=T_g y` give

```text
integral K_s^phys(x,y) f(y) dmu(y)
 = integral K_s(x,y) f(y) dmu(y).
```

Thus this averaged kernel computes exactly the original free heat action
on the physical function class. It does not install a new measure or a
gauge-fixing prescription. In particular it can replace the free kernel
in the Feynman--Kac comparison applied to the invariant `psi_0`.

## 2. Independent support proof without a new spin cutoff

Put `h_s=q_s-1`. Its Haar integral is zero. Suppose
`|h_s(g)|<=d_s` uniformly. Expand the finite seven-factor product in (H1)
as a sum over the `2^7` subsets `S` of edge occurrences. A term is

```text
integral product_(e in S) h_s(x_e (T_g y)_e^-1) dg.      (H2)
```

If `S` has a degree-one vertex `v`, only its single active incident factor
depends on `g_v`. Every inactive edge contributes the constant one.
Integration in `g_v`, using left/right invariance of Haar and
`integral h_s=0`, kills this factor. This proves exact leaf cancellation
directly. The argument needs no interchange with a new spin series; the
standard full heat expansion is only needed to supply the uniform `d_s`.

The two-square source graph is a theta graph with three internally disjoint
paths of lengths `3,1,3` between the two degree-three vertices. A nonempty
support without leaves must contain each length-three path either in full
or not at all: an endpoint of a partial segment would be an internal
degree-one vertex. At the common endpoints it must then contain at least
two complete paths. Thus its possible nonempty supports are exactly:

| Chosen paths | Support size |
|---|---:|
| first length-three path and length-one path | `4` |
| second length-three path and length-one path | `4` |
| both length-three paths | `6` |
| all three paths | `7` |

The bound on the absolute value of (H2) is at most `d_s^|S|` since `dg` is
a probability. Some spin assignments on an allowed support can still
vanish by the gauge constraints; retaining them in this upper bound is
harmless. The empty support is exactly one. Therefore

```text
|K_s^phys(x,y)-1| <= 2d_s^4+d_s^6+d_s^7.                (H3)
```

This is a complete support argument for the specified graph. It is not the
incorrect inference that passing the no-leaf condition guarantees a
nonzero invariant for every assigned spin.

## 3. All-spin tail and rational arithmetic at `s=2/3`

In the accepted `i sigma_k` normalization, dimension `n=2j+1` gives
Casimir `n^2-1`. Unitarity bounds the character magnitude by `n`, hence

```text
d_s = sum_(n>=2) n^2 exp[-s(n^2-1)]
```

bounds the entire nonconstant heat series. At `s=2/3`, write the positive
summands as `a_n`. The leading term and first remainder term satisfy

```text
a_2=4 exp(-2) < 40/73,
a_3=9 exp(-16/3) < 9/200.
```

For every integer `n>=3`, the exact consecutive ratio obeys

```text
a_(n+1)/a_n
 = ((n+1)/n)^2 exp[-(2/3)(2n+1)]
 <= (16/9) exp(-14/3)
 < 4/225.
```

The exponential lower bounds used here are certified by positive Taylor
partial sums: degree `6` suffices for `exp(2)>73/10`, degree `10` for
`exp(16/3)>200`, and degree `8` for `exp(14/3)>100`. Higher degrees are
also valid. The infinite tail is therefore bounded by an actual geometric
majorant, giving

```text
d_(2/3) < 40/73 + (9/200)/(1-4/225)
        = 76633/129064 < 3/5,
3/5 - 76633/129064 = 4027/645320 > 0.
```

The monotone polynomial in (H3) then gives the exact rational majorant

```text
eta = 2(3/5)^4+(3/5)^6+(3/5)^7 = 26082/78125 < 1,
1-eta <= K_(2/3)^phys(x,y) <= 1+eta,
(1+eta)/(1-eta) = 104207/52043.                         (H4)
```

Each of these fractions was independently recomputed with Python's
standard-library `Fraction`. The general ratio bound supplies coverage
for every omitted spin; a finite partial sum by itself would not do so.

## 4. Check the time and density exponents

The heat time in (H4) corresponds to semigroup time
`t_*=(2/3)/kappa`, with inverse-energy units. For the supplied potential,
`osc(V)=4 beta`. The ground-state semigroup comparison cancels the common
eigenvalue factor and gives

```text
max psi_0 / min psi_0
 <= exp[t_* osc(V)] (104207/52043)
 = exp(16r/3) (104207/52043),
r=beta/(alpha hbar^2).
```

Squaring is required because the comparison density is `psi_0^2`, so

```text
R_actual = max psi_0^2 / min psi_0^2
 <= exp(32r/3) (104207/52043)^2.                        (H5)
```

The accepted physical Haar gradient gap is `12`. Its direct density
comparison gives `gamma>=12 kappa/R_actual=6 alpha hbar^2/R_actual`.
This proves the reviewed energy bound. Applying the separate patch
mixing and local comparisons loses two density-ratio factors instead;
the stronger direct route should retain only one `R_actual`.

## 5. Hostile controls and evidence boundary

- **Missing vertex gauge integration:** if a leaf's vertex is not gauged,
  its factor need not integrate to zero. A boundary-charge or partial-gauge
  model does not inherit (H3) without a new proof.
- **Different graph:** the exponents and multiplicities `2,1,1` come from
  these three paths. Other graphs require their actual allowed supports;
  an increasing count of loops can defeat `eta<1` at the same heat time.
- **Different receiver:** the averaged kernel acts correctly on invariant
  functions. Replacing the free kernel by it for arbitrary gauge-dependent
  inputs is generally false.
- **Potential replaced by a classical law:** (H5) bounds the actual
  Schrodinger ground-state density through its eigenfunction equation.
  No identification with `exp(-V)` is used or implied.
- **Unbounded parameter limit:** the normalized reviewed bound decays as
  `r` increases. It remains a finite-graph sufficient bound and does not
  establish the required uniformly positive physical-energy ratio.

The support cancellation, kernel transport, Taylor-tail estimate and
semigroup scaling have written mathematical checks. Their implementation
receipt is maintained alongside the comparison note. This review does not
formally verify Peter--Weyl completeness, Feynman--Kac, or the inherited
source operator domain. The graph-family and continuum obligations remain
OPEN.
