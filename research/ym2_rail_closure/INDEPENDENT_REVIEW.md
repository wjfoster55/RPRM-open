# Independent review of the conditional-rail theorem

12 September 2026. Bounded read-only mathematical review of
[CONDITIONAL_RAIL.md](CONDITIONAL_RAIL.md), performed in a separate lane
from that note's author. This reviewer authored [CHAIN_ESTIMATES.md](CHAIN_ESTIMATES.md);
the review of CR5 checks its application and rechecks the weighted argument,
and is not a claim of independent authorship of that underlying argument.

**Reviewed file:** `research/ym2_rail_closure/CONDITIONAL_RAIL.md`

**Reviewed SHA256:**
`30D65BE6AF0424DA4544FEA5037C6A2476278850C2131180A85F274979CDA7E2`

**Disposition:** the reconstruction equivalence, gauge argument, CR3,
CR4, and CR5 are correct under their displayed assumptions and accepted
finite-volume dependencies. No unresolved mathematical correction was
identified in the reviewed version. This approves the written conditional
implications, not a new actual-vacuum construction or an enlarged YM gap
domain. The hash identifies the reviewed bytes; it is not proof of their
contents.

## 1. One precision correction was applied before this review closed

The initially inspected version called the one-link gradient Poincare
constant `c_*` common, but expressly called only the influence rate
graph-uniform. The reviewer requested that the intended uniformity of
`c_*` be stated across graphs, links, and every exterior.

The author applied that clarification. The reviewed final version now
requires `c_*<infinity` uniformly over precisely those ports. Without it,
CR5 remains a fixed-graph inequality with a possibly graph-dependent
constant, and would not certify a positive bound uniform in graph volume.
The correction changes the explicit hypothesis, not the numerical factor
or the proof. The final SHA256 above covers the corrected wording.

## 2. Rectangle compatibility is sufficient as well as necessary

The carrier is a finite product of compact groups, with globally smooth,
strictly positive, normalized full conditional densities. The proof uses
arbitrary coordinate replacements, not only infinitesimal changes or a
finite sampled collection of rectangles.

For a joint density `p`, conditional normalization cancels from every
single-coordinate ratio, giving `r_i(x,y)=p(y)/p(x)`. This proves necessity
of CR2 immediately.

For sufficiency, adjacent replacements of different coordinates can be
exchanged using CR2. Their replacement values stay fixed, and their common
endpoint is unchanged. A finite word of replacements can consequently be
sorted by coordinate. Consecutive replacements of the same coordinate
telescope by the kernel-ratio definition. These two operations reduce
every path to one update per coordinate with its final value. Thus the
path product depends only on the endpoints, including paths with repeated
updates or coordinates later returned to their starting values.

The chosen ordered product `F` is smooth and strictly positive. Compactness
makes its integral finite and nonzero. For a fixed exterior, the equality
of every ratio `F(y)/F(x)` with the corresponding kernel ratio forces `F`
to be proportional to that kernel as a function of the remaining
coordinate. Normalizing the conditional gives the prescribed `k_i`.
The scalar joint normalization `Z` is legitimate and need not be known in
closed form for this existence theorem.

For uniqueness, the ratio of two positive candidate joint densities is
constant along each coordinate fiber. Since any two product configurations
are connected by at most `N` arbitrary coordinate replacements, it is
constant everywhere. Normalization selects one joint law. No additional
continuous-loop or topological assumption is missing: global replacement
ratios and all replacement rectangles supply a stronger, explicitly
global condition than vanishing infinitesimal curvature alone.

Strict positivity is load-bearing. If it is removed, a two-bit law
supported on `00` and `11` has deterministic full conditionals
`x_1=x_2` and `x_2=x_1`, while the relative masses of `00` and `11`
can vary. The claimed positive-kernel theorem excludes this failure of
uniqueness and excludes divisions by zero.

Therefore ONE for the complete joint-law fiber when the universal CR2
condition is established is justified. One explicit violated rectangle
establishes NONE for that same proposed kernel family. Finitely many
passing checks do not establish universal CR2 on the smooth carrier.
Neither disposition claims that a unique sample configuration was forced.

## 3. Gauge covariance gives the claimed invariant joint density

For a fixed vertex gauge transformation `g`, each edge transformation
`U_e -> g_(s(e)) U_e g_(t(e))^(-1)` is an invertible map of that edge's
coordinate and preserves its Haar measure. Although vertices couple the
choice of transformation parameters, once `g` is fixed this remains a
coordinatewise product map on the configuration space.

Consequently the transformed joint density has transformed full
conditionals, obtained with the corresponding transformed exterior and
no Jacobian factor. The stated covariance identifies these kernels with
the originally supplied kernels. Uniqueness from section 2 identifies
the two joint densities, proving gauge invariance.

The note correctly keeps this assertion separate from invariance of a
single conditional while its exterior is frozen. The latter generally
does not follow and is not needed.

## 4. CR3 has the correct derivatives, sign, and factor

Once compatibility has reconstructed `p`, the normalized full conditional
has the form `k_i=p/Z_i(x_-i)`. Differentiation in coordinate `i` removes
`Z_i`, so

```text
(1/2) grad_i log k_i = (1/2) grad_i log p
                    = grad_i log sqrt(p) = b_i.
```

For the positive smooth `phi=sqrt(p)`, the Riemannian product rule gives

```text
Delta_i phi/phi = div_i b_i + |b_i|^2.
```

With the accepted convention `T=-Delta/2` and `A=T-rS`, this proves
exactly

```text
(A phi)/phi = -(1/2) sum_i(div_i b_i+|b_i|^2)-rS.
```

Thus neither a factor of two from `phi=sqrt(p)` nor the negative potential
sign is missing. The gradients and divergences are those of the declared
SU(2) metric, and the conditional normalization is differentiated only
along the coordinate where it is constant. These statements would need
new justification for partial conditionals or another kinetic operator;
neither replacement is made in the note.

## 5. Constant CR3 proves the actual finite-graph vacuum

If CR3 is one constant `E` everywhere, then `A phi=E phi` as a smooth
identity. For smooth complex `f`, integration by parts and this eigenvalue
equation cancel the cross and potential terms, giving

```text
q_(A-E)[phi f] = (1/2) integral |grad f|^2 phi^2 dmu.
```

The right side is nonnegative. On the fixed compact manifold `phi` and
its reciprocal are bounded and smooth, so multiplication by `phi`
identifies the needed form domains and the identity extends from the
smooth core. This proves `E` is the lowest energy, independently of an
assumed lower eigenvalue or an asserted spectral gap.

Equality implies vanishing weak gradient of `f`; connectedness makes
`f` constant. The ground eigenspace is therefore one-dimensional, and
normalization plus strict positivity selects the stated unique positive
vacuum. Gauge covariance already made `phi` gauge invariant, so this is
also the physical vacuum in the retained gauge-invariant space.

The scalar shift from `A` to the dimensionless physical Hamiltonian does
not affect its excitation gap; restoring the accepted positive energy
unit rescales that gap. The note uses this distinction consistently.

Compatibility by itself establishes none of the constant-residual
premise. Its single-plaquette reference control correctly passes CR2 but
has residual `-(r^2/18)(1-a^2)` for `r>0`. At `a=1` and `a=0` the values
differ, so it fails the vacuum certificate as claimed.

## 6. CR5 follows from the collective certificate with its stated factor

For a dominating influence matrix `C` and positive weights `s` satisfying
`Cs<=q s`, the accepted heat-bath oscillation evolution under `C^T-I`
contracts the weighted oscillation sum at rate `1-q`. The weight direction
is correct because

```text
s^T C^T delta = (Cs)^T delta.
```

At each finite graph the positive weights compare this seminorm with
total oscillation using finite constants. Reversibility then gives a
positive spectral measure for `<f,P_t f>`; exponential decay excludes
spectral mass below `1-q`. This establishes the heat-bath form inequality

```text
Var(f) <= (1-q)^(-1) sum_i E Var_i(f).
```

The graph-dependent norm-comparison prefactors do not change the spectral
rate identified at each graph. A uniform strict upper bound on `q` still
is required for a uniform spectral lower bound. For conditional blocks,
the same positive weights restricted to the block work because the omitted
influence terms are nonnegative and the original bounds admit every
exterior.

The one-link gradient inequality, with the now explicit uniform `c_*`,
therefore yields block constant `c_* /(1-q)`. The accepted direction
cover has `W/Lambda=d/(d-1)`. Applying its physical forest identity and
the factor `1/2` in the actual-vacuum form gives

```text
gap_phys(A) >= [W/(2 Lambda c_*)](1-q)
            = [d/(d-1)](1-q)/(2c_*).
```

This checks CR5 without importing an extra `3/2` factor: any Haar
constant such as `1/3` enters through `c_*` itself. The physical cover
identity and extension to its form domain remain accepted dependencies,
not newly proved statements in this review.

The cosh-mixture control is used at the correct ceiling. Its reference
diffusion gap can shrink with graph volume despite compatibility and
bounded one-link ratios. It is not identified with the actual vacuum
of the retained local YM Hamiltonian, and the note does not claim such
an identification.

## 7. Evidence boundary and remaining work

This is a written proof audit. No old packet checker, numerical
simulation, continuum approximation, or repository-wide suite was run
for this review. The source's finite illustrative checks may corroborate
algebra and expose hostile inputs; they cannot verify all conditional
kernels, all SU(2) values, all exteriors, or all graph sizes by sampling.

The historical-literature attribution and the separate FLICK source
contract were outside this bounded mathematical audit. The note itself
distinguishes their roles from the mathematical theorem and states that
computational commit order supplies no security or physical-time result.

The reviewed theorem provides three correctly separated requirements:
global conditional compatibility, constant local energy for the actual
Hamiltonian, and graph-uniform collective control. Constructing a new
family that satisfies all three beyond the accepted YM window is still
OPEN. Neither this review nor source binding changes that status.
