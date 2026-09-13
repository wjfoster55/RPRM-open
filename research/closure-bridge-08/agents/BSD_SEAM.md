# BSD: an exact forward/backward seam from joint height refinements

Date: 2026-09-12 America/Denver. Evidence: a written polynomial argument,
fresh exact rational point calculations, and exact formal-polynomial checks.
No new analytic precision calculation was performed. E34's real comparison,
total Sha identification, and general BSD remain **OPEN**.

The concrete result is a source-generated necessary interaction term. The
actual first duplications of P and Q force a nonzero rectangular difference
in the regulator. An additively separable potential of the form
`F(m)+G_P(i)+G_Q(j)+G_S(ell)` cannot reproduce that difference on the declared
refinement carrier. Storing the three heights separately is sufficient if
the decoder is allowed to form their joint products. The
required pair terms are given explicitly below. This locates a constructive
joint port for a bridge; it does not establish its terminal boundary.

## 1. Contract and the selected seam

The source is E34, `y^2=x^3-1156x`, and the actual rational points
`P=(-2,48)`, `Q=(-16,120)`, and `S=P+Q=(2178/49,65472/343)`.
Use the exact analytic expansion, full logarithmic x-height convention,
primitive coordinates, minimal differential, and period over both real
components in [EXPLICIT_IDENTITY_TARGET.md](../../bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md).
That note supplies the convergent expressions and correction bounds reused
here; the arithmetic rank, integral basis, analytic order, and period facts
remain attributed dependencies of that note.

Fix a candidate positive integer `sigma`, without identifying it with the
order of any group. Write `Omega>0` for the specified period. The requested
comparison is the real defect

\[
\mathscr D_\sigma=c^{\rm an}_2-\Omega\sigma\mathcal R.
\]

This seam explicitly enlarges a single locked refinement path to the
asynchronous carrier

\[
z=(m,i,j,\ell)\in\mathbb N_0^4.
\]

The first coordinate selects the analytic partial sum `A_m`; the other
coordinates select independent refinement depths in the three *fixed*
source-point height sequences. Put

\[
p_i=4^{-i}\log H_x(2^iP),\quad
q_j=4^{-j}\log H_x(2^jQ),\quad
s_\ell=4^{-\ell}\log H_x(2^\ell S),
\]
\[
R(p,q,s)=pq-\frac{(s-p-q)^2}{4},\qquad
D(z)=A_m-\Omega\sigma R(p_i,q_j,s_\ell).
\tag{1}
\]

Each forward edge increments one cutoff. Its source calculations are
enabled for every admitted state, including projective point exceptions.
Backward traversal decrements a positive cutoff and reopens that earlier
source record. This is reversal of a retained refinement record; it is not
an assertion that an arbitrary rational elliptic-curve point has a rational
half. Equal displayed heights do not merge the distinct source occurrences.

Asynchronous partial sums need not themselves form a canonical-height Gram
matrix or satisfy positivity. They are finite approximants to the same
three fixed limits. Their explicit polynomial readout is admitted for this
test; convergence when all three cutoffs grow follows from the source
height estimates. No group relation `2^ell S=2^iP+2^jQ` is imposed.

The receiver retains analytic cutoff, source point, individual height
cutoffs, primitive coordinate corrections, and the joint regulator readout.
The missing object is a source-derived comparison rule with the required
initial and limiting boundary conditions. An unfinished search for it is
OPEN. A candidate restricted to a single locked diagonal is outside the
rectangular claim below and needs its own continuation proof.

## 2. The exact rectangular condition

Hold the analytic cutoff and S refinement fixed. Let a P step change `p`
by `u`, and a Q step change `q` by `v`. The four states are genuine
refinements of the same retained source records. Expanding the determinant
gives

\[
R(p,q,s)=\frac{pq+ps+qs}{2}-\frac{p^2+q^2+s^2}{4}.
\tag{2}
\]

Subtract its values around this rectangle in the indicated order:

\[
\begin{aligned}
&R(p+u,q+v,s)-R(p+u,q,s)\\
&\qquad-R(p,q+v,s)+R(p,q,s)=\frac{uv}{2}.
\end{aligned}
\tag{3}
\]

Every single-variable term and every pair term missing one of the two
updated slots cancels. Only `pq/2` contributes, giving (3) for all real
slots and increments. The same positive cross coefficient holds for the
P/S and Q/S pairs. Two increments of the *same* slot instead give `-uv/2`.
This is a written polynomial identity, independently checked by exact
formal coefficient arithmetic in the executable below.

Consequently the finite comparison defect obeys

\[
\boxed{\Delta_P\Delta_Q D=-\frac{\Omega\sigma}{2}uv.}
\tag{4}
\]

Any potential `V(z)` matching the source edge differences
`V(z+e)-V(z)=D(z+e)-D(z)` must satisfy (4), independently of whether its
terminal value vanishes. In particular, a candidate of the form

\[
V(m,i,j,\ell)=F(m)+G_P(i)+G_Q(j)+G_S(\ell)
\tag{5}
\]

has zero mixed rectangular difference. It therefore fails wherever
`Omega*sigma*u*v` is nonzero. The separate functions may retain arbitrarily
rich records for their individual source point; separability across the
two changing cutoffs is the rejected restriction. No conclusion is drawn
about an untested nonseparable potential or about a locked-diagonal rule.

This is not a nonzero sum of edge increments around a closed loop. The
exact edge increments are a gradient, and either order has the same total.
Equation (3) says the P-edge increment changes when the Q record advances:
the interaction must be retained to make both orders commute correctly.

## 3. Actual E34 source data make the condition nonzero

For primitive abscissa `(a:b)`, the actual duplication ledger retains

\[
F=(a^2+1156b^2)^2,\quad G=4ab(a^2-1156b^2),\quad
g=\gcd(F,G),\quad H_1=\max(F,|G|)/g.
\]

The first refinement increment is exactly
`(1/4) log(H_1/H_0^4)`. Fresh rational calculations give:

| Source | `H_0` | Raw `F` | Raw `G` | Removed gcd | Primitive next abscissa | `H_1/H_0^4` |
|---|---:|---:|---:|---:|---|---|
| P | 2 | 1345600 | 9216 | 64 | `(21025:144)` | `21025/16` |
| Q | 16 | 1993744 | 57600 | 16 | `(124609:3600)` | `124609/65536` |

The independent rational chord-law duplication agrees with both
projective outputs. Since both exact positive rational ratios exceed one,

\[
u_0=\tfrac14\log(21025/16)>0,\qquad
v_0=\tfrac14\log(124609/65536)>0.
\]

Thus, for the actual first P/Q rectangle at *any* fixed analytic and S
cutoffs,

\[
\boxed{\Delta_P\Delta_Q D
=-\frac{\Omega\sigma}{32}
\log(21025/16)\log(124609/65536)<0.}
\tag{6}
\]

No numerical logarithm, observed BSD quotient, or coefficient digit was
used. Inserting a proposed separable backward potential gives the exactly
different answer zero. This supplies an immediately falsifiable symbolic
certificate, derived from the curve's own first source updates.

## 4. The interaction that a candidate must carry

At fixed analytic cutoff, equation (2) gives the exact decomposition

\[
D=A_m+\frac{\Omega\sigma}{4}(p^2+q^2+s^2)
-\frac{\Omega\sigma}{2}(pq+ps+qs).
\tag{7}
\]

The first three square terms can be assigned separately to individual
height records. The last three products supply the required joint ports.
For example, the exact P refinement satisfies

\[
R(p+u,q,s)-R(p,q,s)=\frac{u}{2}(q+s-p)-\frac{u^2}{4}.
\tag{8}
\]

After Q advances by `v`, the same P refinement costs `uv/2` more. A
forward or backward rule retaining only P's current record cannot recover
that correction unless the relevant joint context is supplied elsewhere.

An equivalent centered form makes the smallest missing interaction in a
local separable expansion explicit. Around fixed baseline `(p_0,q_0,s_0)`,
let `x=p-p_0`, `y=q-q_0`, `z=s-s_0`. Subtract from D its baseline value and
its three separate one-slot changes. The remaining term is exactly

\[
-\frac{\Omega\sigma}{2}(xy+xz+yz).
\tag{9}
\]

This is a necessary algebraic interaction, not a constructed bridge to
the analytic moments. Adding it repairs the finite determinant update.
It does not prove that the repaired potential tends to zero.

## 5. What backward propagation can validly do

For a finite source path `z_0,...,z_N`, write
`h_t=D(z_{t+1})-D(z_t)`. If a proposed potential has exact matching
increments and an independently supplied terminal interval `V_N in I_N`,
then its full backward fiber at stage K is the translated interval

\[
V_K\in I_N-\sum_{t=K}^{N-1}h_t.
\tag{10}
\]

This is a complete interval preimage for the supplied scalar recurrence.
It can be intersected with a forward certificate at stage K. Disjoint
certified intervals refute those joint constraints. Agreement at a finite
stage shows compatibility at that stage, with the same source edge data;
it does not independently establish the proposed terminal condition.

Setting `V_N=0` at an arbitrary finite cutoff is an extra assumption. The
desired identity concerns the limiting real defect, so even if it is true,
its finite D values normally retain nonzero tails. A valid conditional
backward demand for that target must keep those tails.

Here is an explicit asynchronous version using only existing source
bounds. Set `e_r=log(C0)/(3*4^r)` with `C0=5345344`, and put

\[
b=(s_\ell-p_i-q_j)/2,\qquad t=(e_i+e_j+e_\ell)/2,
\]
\[
E^{\rm ht}_{i,j,\ell}
=|p_i|e_j+|q_j|e_i+e_ie_j+2|b|t+t^2.
\tag{11}
\]

Expansion of the product and square bounds every height error jointly,
so `|mathcal R-R(p_i,q_j,s_ell)| <= E^ht`. With the already-proved full
analytic tail `T^an_m` from the identity target, put

\[
E_z=T^{\rm an}_m+\Omega\sigma E^{\rm ht}_{i,j,\ell}.
\]

Unconditionally, `|mathscr D_sigma-D(z)| <= E_z`. The *candidate target*
`mathscr D_sigma=0` therefore propagates the necessary backward constraint

\[
|D(z)|\le E_z.
\tag{12}
\]

Rejecting (12) with certified outward bounds rejects that candidate target.
Passing it at finitely many cutoffs is compatible with the target. A
source-generated proof of (12) along an unbounded cofinal schedule, with
`E_z -> 0`, would establish the exact real identity. Such a proof has not
been supplied here. For evaluation, the positive period in a tail bound
must be replaced by a certified upper endpoint, and every finite real
quantity must be enclosed with outward rounding.

The local potential freedom makes the boundary issue especially clear.
The refinement grid is connected. All exact edge potentials form the
complete family `V(z)=D(z)+c`, `c in R`: subtract D and every edge difference
vanishes; connectivity forces a constant. Conversely every such function
matches all edges. The initial condition `V(z_0)=D(z_0)` fixes `c=0`.
Vanishing at the cofinal limit then requires precisely
`mathscr D_sigma=0`. Choosing `c=-mathscr D_sigma` to force the terminal
boundary only moves the unknown defect into the initial boundary. It is
valid backward constraint propagation, but it is not a proof of the
compatibility of both boundaries.

## 6. Exceptions, scope, and the earlier carry records

- The nonzero obstruction requires `Omega*sigma*u*v != 0`. Zero period,
  zero sigma, or either zero increment makes this rectangle inconclusive.
  Zero sigma is outside the selected positive-integer candidate contract;
  zero period is outside the actual positive period contract. They are
  retained algebraic hostile controls, not discarded by division.
- At O, all increments are zero. At a two-torsion point, duplication is
  projective and reaches O; its first raw correction `delta` is
  `-4 log H_0`, while the normalized first refinement increment is
  `delta/4=-log H_0`, followed by zero. The fresh check includes O and all
  three two-torsion abscissas.
- Coordinate gcds must be retained. Here P removes 64 and Q removes 16.
  At `(34:1)` the full constant `C0=2^6*17^4` is attained. Dropping these
  factors changes the exact log arguments used in (6). Source sign
  normalization and curve admission are checked independently.
- The full-height convention is fixed. Halving every height scales this
  rank-two determinant by one quarter. Period over one real component
  differs by two from the period used here. A changed point basis of index
  d changes the determinant by `d^2`. Each such adapter must carry its
  factor; the symbolic test does not waive normalization.
- The test concerns the real analytic-height target. The current 5-adic
  coefficient `2301 mod 3125` and its multiplicative carry law concern a
  different carrier, as established in
  [OPERATIONAL_PROOF.md](../../bsd-carry-key-06/OPERATIONAL_PROOF.md).
  Its proposed next-digit equation `Ub=sR` genuinely selects a unique
  digit only after independently justified U, R, and target s are supplied
  at the required precision. This test does not manufacture those ports.
- The exact digit compression and retained wrap quotient in
  [COLUMN_HANDOFF.md](../../bsd-carry-key-06/COLUMN_HANDOFF.md) are useful
  models of retaining successor information. The new determinant cross
  term is the analogous *domain-derived* information requirement for this
  BSD receiver. No numeral resemblance is used to identify the two maps.

Even a proved `mathscr D_1=0` would still require finiteness and identification
of the actual cohomological Sha group to become the full claimed E34 BSD
formula. Neither a 5-adic component nor a named positive integer supplies
that missing identification.

## 7. Fresh execution and result disposition

From the repository root:

```powershell
python -I -B research/closure-bridge-08/work/check_bsd_seam.py --output research/closure-bridge-08/evidence/bsd_seam.json
```

The command passed: seven source points; six formal rectangle identities
(three distinct-coordinate and three same-coordinate cases); exact joint
decomposition; source admission and rational chord-law checks; projective
torsion, maximal-gcd and zero-factor controls; and a two-order path check.
The exact log arguments remain rational strings and were never numerically
approximated. See the [script](../work/check_bsd_seam.py) and
[fresh receipt](../evidence/bsd_seam.json).

**Derived and checked:** equations (3), (4), (6), (7) and (9), with a
source-generated rejection of separable matching potentials on the stated
asynchronous rectangle. Equations (10)–(12) give exact backward propagation
or justified tail constraints at their explicitly conditional scope.

**OPEN:** an actual source-derived analytic-to-height identity with matching
initial and vanishing terminal boundaries; its unbounded continuation;
the total Sha identification; general BSD. The new seam identifies and
repairs a precise finite information loss without claiming those closures.
