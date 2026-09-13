# What the teacher and BSD results supply to a vacuum handoff

12 September 2026. Read-only donor audit and bounded derived mapping. The
sources below are specific completed local artifacts; this is not a claim
to have read all RPRM research. No donor implementation was changed, no old
tests were replayed, and no provisional result from the active BSD
new-prime investigation is imported.

**The donors supply a concrete handoff rule: carry the reference, inverse,
operations and joint relations together.** Applied to YM, this permits a
positive trial function to become a new coordinate reference, with its
actual residual retained. Neither donor supplies the missing uniform YM
residual estimate or an enlarged coupling interval.

## 1. The precise transferable statements

The teacher formalization fixes a finite source carrier, calibrated maps
and a specified receiver. [THEORY P1–P3](accepted/donors/liar-teacher-formalization-2026-09-12/THEORY.md)
proves that a retained panel must preserve its requested observations on
every fiber, agree on whether an operation is enabled, and agree on its
retained successor. A correct current answer alone need not preserve the
next operation. P7 proves the moving-reference example: translating the
relative address while transporting the anchor and decoding frame
preserves the source and transported operations. Forgetting the anchor
leaves several possible absolute states. The
[plain-language account](accepted/donors/liar-teacher-formalization-2026-09-12/README.md)
also keeps a reference, a receiving vacancy, and a filled student value as
different roles.

These propositions motivate the YM contract below. The finite binary
carrier, seven/eight counts, Hamming code and XOR operation do not become
YM objects. The YM multiplication map and its operator identity need their
own proof on their own domains; that proof is elementary and is given
below.

The BSD donor makes the need to preserve future and joint operations
particularly explicit. Its
[operational bridge](accepted/donors/bsd-operational-03/OPERATIONAL_BRIDGE.md) retains
two distinct point occurrences with one present shadow. Appending the
deterministic negative of that shadow leaves the ambiguity intact. The
shadow after doubling distinguishes the occurrences and supplies an
explicit inverse at its admitted inputs. Its 4,096-point torsion carrier
is distinct from its rational free-basis height calculation.

For the height receiver, the same note makes a stronger distinction:
individual heights agree for a point and its twin, but adding the same
rational point gives different quadratic-height residues, 4 and 3 modulo
5. A list of individual scalar heights therefore fails to retain the
mixed pairing. This is the relevant donor for overlapping YM blocks:
shared variables, derivatives and conditional interactions must remain
joint. Separate local summaries can agree while their combined response
differs.

The completed
[BSD return](accepted/donors/bsd-operational-03/RETURN_TO_WILLIAM.md) and
[height audit](accepted/donors/bsd-operational-03/PADIC_HEIGHT_AUDIT.md) also supply an
exact alignment-versus-scale distinction. In the stated MST convention,
the matrix is `[[1,2],[2,2]] mod 5`, with determinant `3 mod 5`, so it is
nondegenerate. The arithmetic vector `W=adj(G) ell` is uniquely determined
by its full pairing equation. The cited BKS comparison places the
canonical derived class in its arithmetic line, including the zero
multiple. Its exact multiplier involving the real analytic leading
coefficient remains open in these completed sources. This audit imports
that stated result and its boundary; it does not independently re-prove
the cited arithmetic theorems.

There are two separate lessons here. Matching direction or a selected
readout does not determine the remaining scalar. Also, a change of pairing,
period or tensor convention requires its explicit conversion. In YM,
normalizing a trial wavefunction fixes its amplitude scale, but does not
make its local energy residual constant or determine its spectral effect.
The two missing quantities live in different mathematical carriers;
their common role is an obligation that a partial comparison cannot erase.

## 2. A positive YM reference is an exact new chart

Fix one of the admitted finite open lattice graphs from the
[overlap result](accepted/overlap/RESULT.md): unit-round SU(2) link
variables, Haar probability measure `mu`, all spins, and gauge invariance
at every vertex. There are no boundary charges or periodic
identifications. Keep the same physical Hamiltonian and coupling. Write

```text
S = sum_p a_p,             T = -Delta/2,
A = T-rS.
```

The original dimensionless Hamiltonian is `A+r|P|`, so it has the same
gap. The new reference port is a smooth strictly positive gauge-invariant
function `phi` with `integral phi^2 dmu=1`. Put

```text
w = log phi,              dnu_phi = phi^2 dmu,
U_phi f = phi f,          K_phi = T-grad w dot grad,
R_phi = (A phi)/phi
      = T w - (1/2)|grad w|^2 - rS.
```

`U_phi` is a unitary map from physical `L2(nu_phi)` to physical
`L2(mu)`. Its inverse is multiplication by `1/phi`. Positivity and
compactness on this fixed graph ensure that these smooth multipliers
transport the relevant form and operator domains. The product rule gives
the exact operator identity

```text
U_phi^-1 A U_phi = K_phi + R_phi.
```

Indeed, `T(phi f)=phi T f-grad phi dot grad f+f T phi`;
division by `phi` gives the displayed identity. Integration by parts gives
the joint physical form

```text
<f,(K_phi+R_phi)g>_(nu_phi)
 = (1/2) integral grad(conj(f)) dot grad(g) dnu_phi
   + integral R_phi conj(f)g dnu_phi.
```

Thus a new positive reference is usable immediately as an exact
representation. The multiplication inverse recovers the complete source
wavefunction. If another positive normalized reference `chi` is used,
the transition `f_chi=(phi/chi)f_phi` recovers the same source and
conjugates the complete transported operators. This is the direct YM
realization of the calibrated-reference handoff pattern.

It is essential to retain `R_phi`. It is a multiplication function, not an
arbitrary scalar normalization. It becomes constant exactly when `phi`
satisfies the eigenfunction equation for `A`; the usual positive-ground-
state conclusion then uses the admitted compact elliptic setting. A
chosen reference is not established as the actual vacuum merely because
the constant function is the zero mode of `K_phi`.

The exact chart fiber is `ONE(f=Psi/phi)` for supplied `Psi` and `phi`.
Without the reference, the same relative function can represent different
source wavefunctions. This chart inverse solves the coordinate question;
the spectral and graph-uniform estimate questions remain separate.

## 3. Ports a usable vacuum continuation must carry

| Port | What must be supplied and preserved |
|---|---|
| Source and normalization | Fixed graph, gauge action, Hamiltonian, coupling, physical domains, and normalized positive `phi`; adding a constant to `w` is fixed by the normalization. |
| Exact decoding | `Psi=phi f`, its inverse, and the transition map to any next reference. |
| Transported dynamics | The full operator `K_phi+R_phi`, not only its diffusion part; the joint energy form above. |
| Joint block data | The same link occurrence in every containing block; the actual conditional law under `nu_phi`; derivatives and interactions crossing block boundaries. |
| Residual control | An estimate on the nonconstant part of `R_phi`, or a stronger appropriate form estimate, with its graph dependence stated. |
| Continuation control | The inverse and source/bilinear bounds in the norm actually used to construct the vacuum. A physical `L2` gap alone does not supply these bounds. |
| Requested readout | A physical gap for the original Hamiltonian and, if requested, an actual-vacuum construction interval uniform over the declared graphs. |

The residual port is substantive even for a normalized positive trial
function. If `g_phi` is a lower bound for the physical gap of `K_phi`,
the min–max comparison and the constant trial vector give, on a graph
with a nonempty physical excited sector,

```text
gap_phys(A) >= g_phi + inf R_phi - nu_phi(R_phi)
            >= g_phi - osc R_phi.
```

The first inequality follows from
`lambda_1(K_phi+R_phi)>=g_phi+inf R_phi` and
`lambda_0(K_phi+R_phi)<=nu_phi(R_phi)`. It does not replace the actual
vacuum by `phi`: it bounds the spectrum of the exact conjugated operator.
The bound is useful only when its right side is positive. A residual
oscillation that grows with the number of plaquettes can exhaust this
particular comparison even when the trial function is locally accurate.
Proving a better uniform residual or form estimate is additional YM work.

The earlier
[overlap inverse note, OI10–OI13](accepted/overlap/OVERLAP_INVERSE.md)
states a distinct sufficient target for continuation in the anchored
Fourier norm: an approximate weighted inverse with defect below one,
together with bounds on the driving source and quadratic gradient term.
It also preserves the all-spin failure of a naive additive block inverse.
The present donor mapping supplies no value for those constants. Keeping
the residual in a new chart and controlling that nonlinear inverse are
related obligations with different readouts.

## 4. Hostile controls and closure boundary

The following failures distinguish a successful handoff from a change of
labels:

1. Drop the teacher anchor: one relative address admits several absolute
   sources. Drop `phi`: one relative wavefunction likewise fails to
   specify its source.
2. Preserve a teacher's present answer but drop its successor, or preserve
   BSD individual heights but drop the mixed pairing: the next operation
   can differ. In YM, replacing the joint conditional laws by unrelated
   block laws has the same logical defect and needs its own test.
3. Set `R_phi` to a constant without proving it is constant: this changes
   the transformed operator. Wavefunction normalization does not repair
   the omitted function.
4. Infer a graph-uniform conclusion from successful finite instances. The
   [BSD carry bridge](accepted/donors/bsd-general-01/CARRY_BRIDGE.md) explicitly requires
   a common source-height bound across all finite levels and retains a
   tower with finite realizations but no common rational point. In YM,
   the analogous obligation is an actual uniform bound across the stated
   graph family. No arithmetic compactness result transfers as a YM
   theorem.
5. Treat duplicated observations as independent information. The BSD
   shadow and its deterministic mirror do not separate its two-point
   fiber. The accepted YM overlap result similarly charges shared edges
   only once and proves its gain from gauge-invariant conditional
   residuals; duplication alone cannot improve the estimate.

**Evidence disposition.** The cited teacher statements are written proofs
on their declared carriers, with separately reported finite tests. The BSD
claims are attributed completed arithmetic results and theorem audits.
The positive-reference unitary and product-rule identities above are new
written YM transport proofs on each admitted fixed finite graph. The
identification of which ports to retain is a derived methodological
mapping. A stronger uniform physical bound, an extended actual-vacuum
construction interval, and a continuum limit are **OPEN** here.

## 5. Exact read locators and source hashes

The following SHA-256 values bind the donor bytes read for this audit.
They do not establish the truth of those bytes. Paths are portable
relative to this note; a delivery may copy these exact sources and remap
the links while retaining the original source path and hash.

| Source | SHA-256 |
|---|---|
| [Teacher THEORY](accepted/donors/liar-teacher-formalization-2026-09-12/THEORY.md) | `E91276DEBFCCD8AF6BD62E1A497142A5D27C563AADCC4A312B7619DFEE83D925` |
| [Teacher README](accepted/donors/liar-teacher-formalization-2026-09-12/README.md) | `F8AC13FE5A76F26881E2BF062FB39C906E88F52D986EFADCD66C48E56294075F` |
| [BSD OPERATIONAL_BRIDGE](accepted/donors/bsd-operational-03/OPERATIONAL_BRIDGE.md) | `DC089747CB4D3A7F9AAE47C9131B779B5B1E2C650A1B127D71C09AC380EDADAE` |
| [BSD RETURN_TO_WILLIAM](accepted/donors/bsd-operational-03/RETURN_TO_WILLIAM.md) | `04F51425BB6DAE24458B1307E176CC1817C93491553C5692F80867F75783AE4B` |
| [BSD PADIC_HEIGHT_AUDIT](accepted/donors/bsd-operational-03/PADIC_HEIGHT_AUDIT.md) | `8DB3ED9B53C6BD114BC54E142CFCEBE2A99233D65B0CC03671025EA023F0E66E` |
| [BSD CARRY_BRIDGE](accepted/donors/bsd-general-01/CARRY_BRIDGE.md) | `A7590966734087B29AB08906B22BE10E71C49E57A5018F4C3E9A855C352F98BC` |
| [YM overlap RESULT](accepted/overlap/RESULT.md) | `A61EE10E73D784DDC273383E54EFE823E0DDDD269F9AF37C42CB99430A73DFF7` |
| [YM OVERLAP_INVERSE](accepted/overlap/OVERLAP_INVERSE.md) | `C0C237AD8A1B0D91B8FF7F56C462A618D0654317F6B7EBA8460B7F1DF1C4F7B7` |

The repository instructions, README, agent handbook, recovered-concepts
entrance and RPRM math-lens procedure supplied the reading and evidence
contract. They are not additional mathematical donors. Existing links
inside the donor files retain their original scope and attribution;
reading this selected set is not a claim to have reopened every deeper
historical source.
