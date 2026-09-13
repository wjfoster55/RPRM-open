# Independent review of the conditional remainder port

12 September 2026. **Disposition: no blocking finding in (CP1)–(CP8).**
The factor scopes, incidence bound, constants and quantifiers support the
stated conditional row estimate. It retains an explicit unknown response
of the actual vacuum remainder. It does not establish that this response
is uniformly small or invoke a spectral-gap implication.

Reviewed [NEXT_CONDITIONAL_PORTS.md](NEXT_CONDITIONAL_PORTS.md) and
[check_conditional_head.py](check_conditional_head.py). This reviewer wrote
only this review and ran the new checker once in its read-only default mode.
No proof/checker file was changed and no accepted-source suite was rerun.

## 1. Exact density and receiver

The carrier is the full product of SU(2) link occurrences on the specified
finite open square/cubic lattice graph. The conditional fixes actual exterior
links. It is not a conditional constructed from independent trace coordinates
or separately generated plaquette states.

Writing `F_G=log rho_G=F_head+R_G` is an exact definition of `R_G` for the
actual positive vacuum. It is valid throughout `0<=r<=1` even where the
elementary graph-dependent analytic disk does not cover that coupling.
Outside that disk it is not justified to call the remainder small; the source
explicitly avoids that inference. Additive normalization scalars do not
affect the exterior-change oscillations.

Smooth strict positivity on each fixed compact source supplies a canonical
continuous conditional density at every exterior. Thus (CP6) can take the
stated supremum over all exterior pairs, not merely almost-everywhere
versions chosen independently for different conditionals. Compactness makes
each fixed-graph quantity finite; it does not bound the supremum over graph
sizes or the sum over all exterior edges uniformly.

## 2. Factor oscillations and shared support

For `f(a)=ra/3-r^2a^2/144`, the smallest derivative on `[-1,1]` is
`r/3-r^2/72>=0` on the stated coupling interval. Its endpoint difference
is exactly `2r/3`. The pair factor has oscillation at most `4r^2/351`
by the previously proved full two-square coefficient bound.

The single-plaquette scope contains four edges. The pair scope is the
seven-edge union, not only its outer six-edge loop: the product of the two
plaquette half traces can depend on their shared edge. This is the correct
scope for the incidence bound even if a particular exterior reduces the
factor's actual range.

For exterior pairs differing only at `j`, a factor independent of `e`
contributes an inside-independent scalar; a factor involving `e` but not
`j` cancels identically. For every remaining factor,

```text
osc_{U_e}[F_A(U_e,omega')-F_A(U_e,omega)] <= 2 osc F_A.
```

The factor two is necessary for this unrestricted comparison. Summing these
terms gives the head bound `b_ej` in (CP4). The use of the same edge identities
in the factor functions and the two exteriors preserves the shared witness.

## 3. Incidence count and constants

Let `m=2(d-1)`, so `m=2` or `4`. An edge lies in at most `m` elementary
plaquettes. Each plaquette has at most `4(m-1)` adjacent plaquettes, since
distinct elementary squares share at most one edge. An adjacent pair whose
union contains `e` has at least one member containing `e`; choosing that
member first bounds the number of unordered incident pairs by
`4m(m-1)`. Counting only pairs with both members through `e` would omit
valid factors.

For the full interior star, the only double counts have both plaquettes
through `e`, and their number is `binomial(m,2)`. Thus the exact counts are
`8-1=7` in dimension two and `48-6=42` in dimension three. Boundary removal
or selecting a subset of plaquettes can only remove these factors. The
source uses the conservative counts `8` and `48`, so the exact-star
correction is not needed for the all-graph bound.

Each incident single factor exposes three exterior edges and each incident
pair factor exposes six. Interchanging the two finite sums therefore gives

```text
sum_{j!=e} b_ej
 <= 2*m*3*(2r/3) + 2*[4m(m-1)]*6*(4r^2/351)
 = 4m*r + [64m(m-1)/117]*r^2.
```

This checks every factor in (CP5). The bound is independent of the total
number of plaquettes because only factors incident to the chosen update
edge enter this count.

## 4. Actual remainder and conditional tilt

The remainder port is precisely

```text
epsilon_ej = sup_{omega,omega' differing only at j}
  osc_{U_e}[R_G(U_e,omega')-R_G(U_e,omega)].
```

For each exterior pair, the exact log tilt has oscillation at most
`b_ej+epsilon_ej`; normalizing the conditional only subtracts a scalar.
Applying the accepted bounded-tilt inequality at its stated total-variation
normalization gives

```text
c_ej <= tanh((b_ej+epsilon_ej)/4)
      <= (b_ej+epsilon_ej)/4.
```

Taking the exterior supremum and then summing preserves the inequality.
Dividing the preceding incidence bound by four reproduces (CP1), with
quadratic head coefficients `32/117` in two dimensions and `64/39` in
three. No cancellation between separately optimized exterior pairs is
assumed.

For `rho_head` the remainder is only a scalar, so its epsilon terms vanish.
For the actual vacuum they remain present. Equation (CP8) is explicitly a
sufficient additional estimate to prove, not an accomplished bound. Even
if it were supplied, the source correctly leaves the spectral criterion,
update rates, electric-form comparison and physical limits as further
contracts.

An `L^2` wavefunction or log-density tail cannot fill this port: narrow
regions can retain large exterior-change oscillation while contributing
little to `L^2`. Fixed-graph smoothness or local `C^k` existence also does
not imply summability over all `j` and uniformity over all admitted graphs.
The source preserves both distinctions.

## 5. Checker review and execution grade

The checker canonically represents lattice edges and enumerates both
elementary plaquettes through each transverse direction. Taking the
plaquette neighbors of every incident plaquette covers exactly the local
pair star relevant to the chosen edge. Unordered-pair deduplication checks
the `7/42` counts against the separate double-count formula. Its per-exterior
edge exposure sum independently checks the factor-size count, and exact
rational arithmetic checks the bound constants. The hostile count records
the `6/36` omitted factors if only pairs with both plaquettes through the
updated edge are retained.

Executed from the packet directory:

```powershell
python -I -B check_conditional_head.py
```

Result: `PASS: exact 2D/3D local incidence stars and conditional-head rational bounds`.
The default also compared the full saved deterministic receipt. Conditions
raise exceptions rather than relying on removable assertions.

This is execution evidence for the finite star/rational checks. The complete
all-graph counting argument and all-exterior inequality are the written
proofs reviewed above. The checker neither evaluates the actual vacuum
remainder nor verifies its uniformity or any analytic spectral theorem.

## 6. Reviewed byte receipt

Paths are relative to this packet directory. Each retrieval binds its own
bytes; these hashes are provenance, not mathematical proof.

| File | Retrieved UTC | SHA-256 |
|---|---|---|
| `NEXT_CONDITIONAL_PORTS.md` | `2026-09-12T18:49:57.4433088Z` | `0467fdbf3a3690eaa6b58b30213d7f1f2a642204b69cc7c84a960bb14e2026a4` |
| `check_conditional_head.py` | `2026-09-12T18:49:57.7438567Z` | `67c266363d9dec2fdf44d2f1590729ed2f0b2115e69681a0005f9544a889d98d` |
| `RESULTS_CONDITIONAL_HEAD.json` | `2026-09-12T18:51:07.1263229Z` | `22a9bbc61ddc933d7a6be8b5d70f4adaf985db5d6bfa7bec275111a6eee6e829` |
