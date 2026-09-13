# Signed differences expose the exact missing mixing operator

12 September 2026. Written derivation and a separate exact finite certificate.
The prior [glue lemma](accepted_sources/ym2_global_phase_joint/NEXT_GLUE_LEMMA.md) and
[quantum bridge](accepted_sources/ym2_global_phase_joint/GAP_BRIDGE.md) are accepted evidence
at their declared scopes. Their old tests were not rerun.

The useful mathematical version of "stacked differences" is the stack of
conditional residuals `f-E[f | exterior]`. Its squared norm is exactly the
sum of patch conditional variances. The missing mixing constant is the
inverse lower spectral bound of this stack's Gram operator. This identifies
what the differences must detect and why local subtraction can miss a
collective mode. It does not estimate the interacting `SU(2)` vacuum by
itself.

## 1. Contract and the actual full-source gauge restriction

Use the source contract of the glue lemma: a specified finite connected
graph `G`, the configuration carrier `Q_G=SU(2)^(E_G)`, product Haar
probability `mu_G`, all vertex gauge transformations, and the source
Schrodinger operator and domain supplied there. Its normalized strictly
positive gauge-invariant ground state is `psi_0`, and the probability here is
the actual joint vacuum `nu_G=psi_0^2 mu_G`. Equal functions mean equal
elements of `L^2(nu_G)`. The Hilbert space may be real or complex; all inner
products below use complex conjugation where required.

Supply the finite family of edge-patch occurrences `B`; duplicates retain
their multiplicities. Put `F_(B^c)=sigma(U_e:e outside B)`. Define on all of
`L^2(nu_G)`

```text
P_B f = E_nu[f | F_(B^c)],       R_B = I-P_B,
A = sum_B R_B,                  D f = (R_B f)_B.        (D1)
```

`P_B` is conditional expectation under the same full source law, rather
than a separately invented patch vacuum. It is an orthogonal projection;
therefore `R_B` is also an orthogonal projection. These are bounded operators
defined on the whole Hilbert space. The direct-sum target of `D` retains one
residual occurrence for each supplied patch occurrence.

The physical restriction is justified, even though individual outside links
are gauge dependent. For fixed vertex gauge assignment `g`, let `T_g` act
on each oriented link by `U_e -> g_(s(e)) U_e g_(t(e))^-1`, and set
`U_g f=f o T_g^-1`. Haar invariance and gauge invariance of `psi_0` make
`U_g` unitary on `L^2(nu_G)`. Moreover `T_g` and its inverse transform every
outside link using that same outside link and fixed group elements. Hence
they preserve the outside-link sigma algebra as a sigma algebra. The
subspace `L^2(F_(B^c),nu_G)` is mapped onto itself by `U_g`. Uniqueness of
the orthogonal projection gives

```text
U_g P_B = P_B U_g,   for each fixed g.                    (D2)
```

Thus `P_B`, `R_B`, and `A` preserve and reduce the closed physical subspace
`H_phys={f:U_g f=f for all g}`. This is a statement of equivariance in
`L^2`, with its ordinary almost-everywhere convention. It does not require
the conditional law at one frozen exterior to be invariant under a gauge
transformation that changes that exterior. For a physical `f`, its
conditional expectation is physical as an `L^2` function on the full source.

Each `P_B` preserves constants and means, so the operators also reduce
`H_phys,0={f in H_phys:E_nu f=0}`. This is the needed invariant restriction,
not an assumption that conditioning on link coordinates automatically
commutes with every possible symmetry. The proof uses the linkwise full
vertex action and the actual invariant source vacuum.

The requested receiver is the original variance inequality and its quantum
gap implication, plus conditional-update continuations. The missing port
is a useful positive lower bound on `A` for the actual graph/vacuum family.
The operator is specified; the unknown general bound remains **OPEN**.

## 2. The exact difference, Gram, and gap identities

For every square-integrable `f`, conditional orthogonality gives

```text
v_B(f) = ||R_B f||^2 = <f,R_B f>,
sum_B v_B(f) = ||D f||^2 = <f,A f>,    D*D=A.           (D3)
```

This also has a literal signed-difference interpretation. Given the outside
links, draw two inside configurations independently from the same full
vacuum conditional law, obtaining `Q,Q'` with identical outside links.
The conditional two-copy variance identity, then integration, gives

```text
v_B(f) = (1/2) E |f(Q)-f(Q')|^2.                        (D4)
```

Independent conditional copies in this formula are an integration device.
They do not replace the shared source edge by independent patch variables
in the original graph. The relevant difference is typed by its conditional
law and patch occurrence; a bare minus sign does not supply either.

Assume `H_phys,0` is nonzero and define

```text
delta_phys(A) = inf_(0 != f in H_phys,0)
                  <f,A f>/||f||^2.                     (D5)
```

The sharp constant in the glue inequality `(G2)` is exactly

```text
C_mix* = 1/delta_phys(A),                              (D6)
```

with `1/0=+infinity`. Indeed subtracting `E f` leaves every residual
unchanged, so `(G2)` is precisely `||f||^2 <= C <f,A f>` on this mean-zero
space. Taking the infimum proves both directions, including sharpness.
Here "gap" means the bottom on the complement of the constants. One must
not discard an additional nonconstant kernel and call the next eigenvalue
the mixing gap. Since `A` is bounded and positive, the infimum is the bottom
of its spectrum on the indicated space; an eigenfunction attaining it is
not required. A dense physical form core suffices because `(G2)` extends
by `L^2` continuity of this bounded quadratic form.

There are two distinct failure mechanisms. A nonzero `f` with all
`R_B f=0` is an exactly unseen physical mode; the kernel is
`intersection_B range(P_B)` within the physical space. Even with no such
nonconstant mode, a sequence of normalized physical `f_n` with
`sum_B||R_B f_n||^2 -> 0` destroys a positive lower bound. Kernel triviality
alone is insufficient in an infinite-dimensional space.

When `delta_phys(A)>0`, `D` is bounded below on `H_phys,0` and has closed
range. The exact recovery on that reached range is
`f=A^-1 D* D f`. Without a positive lower bound, an inverse can be unbounded;
when a kernel exists, a reached residual tuple has affine completion fiber
`f+ker(D)`. Centering fixes the constant ambiguity but need not remove other
kernel directions. This describes the residual receiver's inverse boundary.

For `M` patch occurrences, the random single-patch refresh operator is

```text
K = (1/M) sum_B P_B = I-A/M.                            (D7)
```

It is a positive self-adjoint Markov operator, and
`||K|H_phys,0||=1-delta_phys(A)/M`. Therefore repeated conditional refresh
contracts that norm by the exact operator factor
`[1-delta_phys(A)/M]^n`. Continuous refresh at rate one per patch has
generator `-A` and norm `exp[-t delta_phys(A)]` on this space. These are
auxiliary conditional-update dynamics. They are not the quantum real-time
evolution. The glue lemma relates them to the quantum energy only when its
local derivative estimate `(G3)` and overlap count `(G4)` are also supplied:

```text
gamma_G >= alpha hbar^2 delta_phys(A)/(2 C_loc m).        (D8)
```

## 3. A sharp two-projection correlation criterion

On a nonzero mean-zero Hilbert space, let `P,Q` be orthogonal projections
with nonzero ranges `M,N`. Define their maximal normalized correlation

```text
c = sup {|<u,v>| : u in M, v in N, ||u||=||v||=1}.      (D9)
```

Then the sharp lower bound of `2I-P-Q` is `1-c`. Consequently its variance
constant is exactly `1/(1-c)`, with infinity at `c=1`. On unrestricted
probability spaces these ranges are the centered functions measurable
with respect to the two conditioning sigma algebras, so (D9) is their
maximal correlation. On the invariant subspace it is the correlation
restricted to physical functions. These are different admissible
optimization classes.

Here is a direct proof in the present normalization. Set
`L:M direct-sum N -> H`, `L(u,v)=u+v`; then `LL*=P+Q`. For every pair,

```text
||u+v||^2 <= ||u||^2+||v||^2+2c||u||||v||
           <= (1+c)(||u||^2+||v||^2).
```

Choosing unit `u,v` with inner product approaching `c`, and changing the
phase of one vector to make that inner product nonnegative real, attains
this bound arbitrarily closely. Hence `||P+Q||=||L||^2=1+c` and
`inf <f,(2I-P-Q)f>/||f||^2=2-||P+Q||=1-c`. This proves the claim without
assuming compactness, an attained angle, or a discrete spectrum. If exactly
one range is zero, the gap is `1`; if both are zero it is `2`. If the ranges
have a shared nonzero vector, `c=1` and that vector is a kernel witness.
An unrefreshed common exterior can produce exactly this obstruction.

Conditional-expectation operators, maximal correlation, and Gibbs-update
norms are standard probability/operator theory. See
[Liu, Wong, and Kong (1994), Section 2 and Theorem 3.2](https://www2.stat.duke.edu/homeweb/scs/Courses/Stat376/Papers/ConvergeRates/GibbsSampling/LiuWongKongBiometrika1994.pdf)
for the mean-zero Hilbert-space and two-component Gibbs framework.
[Halmos (1969), *Two Subspaces*](https://www.ams.org/tran/1969-144-00/S0002-9947-1969-0251519-5/S0002-9947-1969-0251519-5.pdf)
is classical context for the geometry of pairs of subspaces. The proof above
derives the exact normalization needed here. Recasting the RPRM missing
port in this language is a task synthesis; no new general projection theorem
or newly solved Yang--Mills correlation claim is asserted.

## 4. Complete four-state calculation: the slow collective mode

Use the explicitly different carrier `(x,y) in {-1,+1}^2` and

```text
nu_rho(x,y)=(1+rho*x*y)/4,     -1<rho<1.                (D10)
```

All four states have positive mass. The original control corresponds to
`rho=1-2epsilon` with `0<epsilon<=1/2`. Let `P_x` refresh `x` conditional
on `y`, and `P_y` refresh `y` conditional on `x`. Direct conditional means
give `P_x x=rho*y`, `P_x y=y`, `P_y y=rho*x`, `P_y x=x`, and
`P_x(xy)=P_y(xy)=rho`. Thus `A=2I-P_x-P_y` has the complete orthogonal
eigenbasis

| Observable | Squared `L^2(nu_rho)` norm | Eigenvalue of `A` |
|---|---:|---:|
| `1` | `1` | `0` |
| `x+y` | `2(1+rho)` | `1-rho` |
| `x-y` | `2(1-rho)` | `1+rho` |
| `xy-rho` | `1-rho^2` | `2` |

The four vectors are nonzero and orthogonal for every admitted `rho`, so
they span the entire four-dimensional function space. This proves the
complete spectrum, including its multiplicities, and the sharp result

```text
delta(A)=1-|rho|,       C_mix*=1/(1-|rho|).             (D11)
```

For nonnegative correlation the slow mode is the joint sum `x+y`; the
signed contrast `x-y` is the fast mode. For negative correlation their roles
switch. Inspecting only one sign orientation can therefore miss the slow
direction. Binary centered single-coordinate functions each span one line,
so their maximal correlation is exactly `|rho|`, in agreement with (D9).

For the original positive-correlation control,

```text
Var(x+y)=2(1+rho)=4(1-epsilon),
v_x(x+y)+v_y(x+y)=2(1-rho^2)=8epsilon(1-epsilon).
```

The variance is bounded by `4`. The ratio diverges because the local
conditional residuals tend to zero while the collective fluctuation
persists. It is relative failure of the local readouts to detect this mode,
not unbounded absolute variance on this fixed carrier.

Here `K=(P_x+P_y)/2` has complete spectrum
`{1,(1+rho)/2,(1-rho)/2,0}`. Its mean-zero operator norm is
`(1+|rho|)/2`, and its `n`th power has exactly that norm to the `n`th power.
A systematic full sweep `T=P_x P_y`, with matrices acting on observables,
instead satisfies, for `Jf=E f`,

```text
(T-J)^2=rho^2(T-J),
T^n-J=rho^(2n-2)(T-J),
||T-J||=|rho|,
||T^n-J||=|rho|^(2n-1), n>=1.                          (D12)
```

The last formula also holds at `rho=0` since the sweep then equals `J`.
For nonzero `rho` its mean-zero spectral radius is `rho^2`; this is distinct
from its one-sweep operator norm `|rho|`. Indeed `T-J` maps `f` to
`rho*y*<x,f>`, a rank-one operator between unit vectors `x,y`, proving its
norm, while a second application multiplies by `rho^2`.

At `rho=+/-1` the measure loses full support and `L^2` identifies values
off the remaining two states. The four-vector argument is then no longer
admitted. Each coordinate determines the other on the support, all
singleton conditional residuals vanish, and nonconstant supported functions
remain. This boundary has gap zero, consistent with the limiting bound.

## 5. What a minus can change, and what it preserves

There are several distinct operations:

1. **Negation:** `Nf=-f` is an involution, `N^2=I`. It preserves variance
   and every squared residual, so it preserves the same mixing ratio.
2. **Centering:** `f -> f-c` leaves variance and all residuals unchanged.
   On the binary coordinate `t=(x+1)/2`, `t-1/2=x/2` rescales the old
   signed coordinate; the inverse is `x=2(t-1/2)`. Applying `-1/2` twice
   is an affine translation, not double negation. Two coordinates each
   equal to `-1/2` remain two occurrences until a readout adds them.
3. **Conditional residual:** `R_B f=f-P_B f` is a projection. Repeating
   the same difference gives `R_B^n=R_B` for `n>=1`; it does not become
   negation or build a new lower bound. Different residuals need not
   commute. In the binary model, `[R_x,R_y]` is nonzero for `rho!=0`.
   Alternating these residuals is also different from conditional refresh:
   `(R_x R_y)(xy-rho)=xy-rho`, so it retains the interaction mode.
4. **Changing the update:** modifying which states a patch can refresh
   changes `P_B`, hence changes the mixing question even if the source
   probabilities have simply been expressed in new coordinates.

For an exact reencoding `z=F(q)` with pushforward probability, the pullback
`U:h -> h o F` is unitary. Transporting the conditioning sigma algebras and
operators gives `P'_B=U^-1 P_B U`, `A'=U^-1 A U`; spectra and sharp constants
are identical. The receiver also needs the transported physical subspace.
The two-coordinate encoding

```text
s=x+y, d=x-y;          x=(s+d)/2, y=(s-d)/2             (D13)
```

is exactly invertible on its four-point cross. Keeping `d` alone folds the
two states `(-1,-1)` and `(+1,+1)` together while their `s` values differ;
it fails the collective-sum receiver. Retaining both coordinates repairs
that loss. This is an information statement, not a mixing improvement.

There is a particularly sharp update control on the same four-point cross.
Replace the conjugated old refreshes by the new rule "refresh `s` given
`d`, or refresh `d` given `s`." At `d=0` only the two nonzero `s` states
interchange; at `s=0` only the two nonzero `d` states interchange. There is
no connection between these two components. The centered indicator of
`s=0` is a nonconstant kernel vector for the new `A`, so its mixing gap is
zero at every admitted `rho`. The original gap is positive. This proves
that choosing updates by the newly drawn axes is a changed operation;
invertible sum/difference coordinates alone do not license it.

Refreshing the whole pair jointly instead gives `P_all=J`,
`A_all=I-J`, and sharp mixing constant `1`. That is another update change.
For the quantum glue task, a whole-graph patch merely moves the difficult
bound into its whole-graph local derivative constant. Neither regrouping
nor a change of notation removes the need to bound the actual physical
energy ratio.

## 6. Verification and remaining port

[check_differences.py](check_differences.py) uses only exact rational
arithmetic and the Python standard library. The new
[RESULTS_DIFFERENCES.json](RESULTS_DIFFERENCES.json) retains all four-state
probabilities and the full conditional, residual, Gram-input, refresh,
commutator, and changed-coordinate matrices at seven rational correlations
`-99/100,-3/4,-1/2,0,1/2,3/4,99/100`. Matrix equalities cover every function
on each checked carrier. The independent written basis calculation proves
the formula for all real `-1<rho<1`; the seven cases are not an unbounded
parameter proof.

```powershell
python -I -B research/ym2_signed_differences/check_differences.py
python -I -O -B research/ym2_signed_differences/check_differences.py
```

Both commands recompute and compare the saved receipt without writing.
`--write-results` is the explicit receipt-writing option. Verification uses
exceptions rather than assertions and remains active under `-O`. The
receipt's source hash binds checker bytes; it does not prove the checker or
the written claims. No previous checker, simulation campaign, spin cutoff,
numerical eigensolver, or package installation is used.

The physical spectral identification (D6), the gauge restriction (D2), and
the two-projection criterion have written proofs. The exact rational checks
support the finite four-state formulas and hostile operation controls. The
binary law is not asserted to be an `SU(2)` vacuum law. Estimating the
actual family of physical residual operators with useful constants and
energy scaling remains the next substantive mathematical obligation.
