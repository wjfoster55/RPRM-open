# Independent review of the forest-complement cover

12 September 2026. Written audit of
[BLOCK_COVER.md](BLOCK_COVER.md), especially (O5)-(O13), using the accepted
[conditional gap proof](accepted/estimate/CONDITIONAL_GAP_EXTENSION.md).
No old verifier, simulation, spin cutoff, installation, publication or git
operation was run. Only this review file was written in this audit.

**Disposition: the direction-cover physical gap improvement is supported
at the stated finite open-graph scope.** The forest identity, uniform
conditional block constant, energy counting and endpoint passage are
compatible. They strengthen the physical form bound within the existing
constructed-vacuum interval. They do not extend that construction interval
or supply the weighted local Fourier inverse considered in
[OVERLAP_INVERSE.md](OVERLAP_INVERSE.md).

## 1. Conditional expectation and the gauge constraint

Let `nu` have a smooth strictly positive gauge-invariant density on
`SU(2)^E`, and let `P_B` condition on the exterior `F=E\B`. For each fixed
vertex gauge transformation `g`, the induced operator on `L2(nu)` is
unitary and preserves the closed subspace of functions measurable in
`U_F`. This is because each transformed exterior link depends only on
that same exterior link and its two fixed endpoint gauge elements.
The orthogonal projection onto that subspace therefore commutes with
the gauge action. Hence `P_B f` is invariant when `f` is invariant.

If `F` is a forest, the full vertex gauge group acts transitively on
`SU(2)^F`: fix a root gauge element in each component and solve recursively
along its edges to transform every forest link to identity. There is no
cycle constraint. A smooth invariant function depending only on `F` is
therefore constant. Since conditional expectation preserves the mean,

```text
P_B f = nu(f),                    f physical.            (IR1)
```

The smooth statement extends to all physical `L2(nu)` functions by
smooth approximation followed by compact gauge-group averaging and
boundedness of `P_B`. This addresses the almost-everywhere convention.

The important distinction is covariance when the exterior is transformed.
The conditional law with one particular exterior frozen need not be
invariant under the full gauge group. The proof does not assume that it
is, and it introduces no independent gauge group or vacuum for a block.
The phrase "any density" in this result must retain the hypothesis
"gauge invariant". Positivity and smoothness supply the stated regular
conditional representatives and approximation argument.

## 2. The conditional analytic bound remains uniform

For the actual vacuum suppose `||u||_*<=Y<3/4`, as in the accepted proof.
Conditioning on a block exterior and then on all other links of the
block leaves exactly the original one-link conditional law. Its internal
influence matrix has entries bounded by the corresponding full-matrix
entries, so its maximum row sum is at most `4Y/3`. Its one-link log-density
oscillation remains at most `8Y/3`.

The accepted reversible conditional-update argument thus applies on
each fixed compact block with spectral rate at least `1-4Y/3`. Its
oscillation prefactor can depend on block size; the spectral-measure
argument only requires a finite prefactor for each continuous test
function and preserves the uniform rate. Combining with the one-link
Haar gradient constant `1/3` and the tilt factor gives

```text
Var_(nu_B(.|z))(f)
 <= C_grad(Y) integral sum_(e in B)|grad_e f|^2 dnu_B(.|z),
C_grad(Y) = exp(8Y/3)/[3(1-4Y/3)].                       (IR2)
```

This is uniform in the block and every exterior configuration `z`.
It requires neither a bound on the oscillation of the entire block
density nor that blocks be connected or of bounded size. The transpose
and row-sum convention remain those of the accepted conditional proof.

## 3. Weighted form bound and physical spectrum

For forest-complement blocks with nonnegative weights, define

```text
W = sum_B w_B,
load_e = sum_(B:e in B) w_B,        Lambda = max_e load_e.
```

For a centered physical function, (IR1) gives the exact identity
`sum_B w_B ||(I-P_B)f||_2^2 = W ||f||_2^2`. Integrating (IR2) and
counting each original edge once with its accumulated load yields

```text
W Var_nu(f) <= C_grad(Y) sum_e load_e nu(|grad_e f|^2)
            <= C_grad(Y) Lambda nu(|grad f|^2).
```

For `W,Lambda>0`, the actual ground-state form is one half of the last
gradient integral. Since multiplication by the positive invariant vacuum
maps physical functions to physical quantum states, this proves

```text
gap_phys/E_el >= W/[2 Lambda C_grad(Y)].                 (IR3)
```

Smooth physical functions are dense in the physical form domain: smooth
form approximation can be followed by gauge averaging, which is bounded
in the weighted gradient norm because the gauge action preserves both
the metric and `nu`. Thus the estimate covers the whole physical form
domain, including complex states by real and imaginary parts.

For the `d` direction forests on a finite subgraph of `Z^d`, assigning
`1/(d-1)` to each complement gives `Lambda=1`, `W=d/(d-1)`. At
`Y` tending to `9/16`, this yields

```text
gap_phys/E_el >= [d/(d-1)] (3/8) exp(-3/2).
```

In three dimensions the endpoint is therefore
`(9/16)exp(-3/2)` on `0<=r<=9/512`, as claimed. The endpoint passage
must use the first two eigenvalues of the **physical restriction**, not
substitute the first ambient excitation. That restriction reduces the
operator and inherits compact resolvent; the potential is bounded and
the domain fixed. Min-max continuity therefore supplies the endpoint
separately for each finite graph, with a common resulting constant.
An empty physical excited complement retains the vacuous form statement.
No endpoint Fourier-norm construction is needed.

## 4. Cube count and optimality within this cover class

For the cube, `|E|=12`, `|V|=8`, so every forest complement has at least
five edges. For any such weighted cover,

```text
5W <= sum_B w_B |B| = sum_e load_e <= 12 Lambda,
W/Lambda <= 12/5.                                        (IR4)
```

All spanning-tree complements have exactly five edges. Cube symmetry
acts transitively on edges and permutes the complete family of spanning
trees. Consequently, if that family has 384 members, each edge belongs
to `384*5/12=160` complements. Weights `1/160` then give load one and
`W=384/160=12/5`, attaining (IR4).

The supplied tree count is independently consistent with the matrix-tree
formula: the cube graph Laplacian has eigenvalues `0`, three copies of
`2`, three copies of `4`, and `6`, obtained from the eight parity
characters on `{0,1}^3`. Their nonzero product divided by eight is
`2^3*4^3*6/8=384`. This is a written count; the root task's separate
enumeration should be reported with its own receipt and execution status.

The optimization claim is exactly for `W/Lambda` among cube forest-
complement covers. It is not optimality of the physical gap, of every
block method, or of an arbitrary graph's cover. More generally the same
counting argument gives `W/Lambda <= |E|/(|E|-|V|+1)` on a connected
graph of positive cycle rank, but equality requires a suitably balanced
forest-complement family; it does not follow from that bound alone.

## 5. Distinguishing checks and claim ceiling

An exterior cycle is an exact hostile case. At the free vacuum, take the
nonconstant character of that cycle's holonomy as `f`. It is physical,
centered and exterior measurable, so `P_B f=f`, refuting (IR1) when
"forest" is dropped. Periodic coordinate-direction loops, retained
boundary charges, or a weakened gauge constraint need a new argument.

A free single square supplies a sharp normalization check. Its four
one-link blocks each leave a three-edge forest. With unit weights,
`W=4`, `Lambda=1`, and `C_grad(0)=1/3`, (IR3) gives six. This equals
the actual free physical gap: a nontrivial invariant spin support cannot
have a degree-one occupied vertex, so on the square it occupies all four
edges and costs at least `4*(3/2)=6`; the fundamental loop character
attains it. The full-link free gap of `3/2` is a different receiver and
does not contradict this physical improvement.

There is likewise no conflict with the failure of a positive sum of
partial Poisson inverses in `OVERLAP_INVERSE.md`. The present proof
estimates conditional variances against derivative energy. It does not
identify a sum of block kinetic inverses with the global weighted inverse.

The review supports a written physical gap improvement on the existing
finite-lattice parameter window. The blocks may be extensive; the result
does not establish efficient block sampling, a stronger construction
interval, a graph-uniform local Fourier inverse, an infinite-volume
representation or a continuum mass gap.
