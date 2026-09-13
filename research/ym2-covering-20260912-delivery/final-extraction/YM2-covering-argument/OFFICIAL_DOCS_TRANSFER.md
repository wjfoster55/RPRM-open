# Official RPRM transfer into the YM covering question

Read-only source retrieval and derived adapter, 12 September 2026. This note
owns only this file. It does not publish or edit a paper, change another
research lane, run an earlier checker, or write a registry or Memory Fabric.
The `rprm-math-lenses` procedure was used to keep the source carrier,
receiver, operator, completeness direction, and evidence ceiling explicit.

## Result of the retrieval

The official material supplies a substantive **one-sided complete enclosure**
rule. It does not require reconstructing the entire true vacuum to exclude
all cheap physical excitations. Its strongest concrete candidate application
is to place the physical gauge-invariant Hilbert space inside the full
product of edge Hilbert spaces and prove a uniform spectral bound for the
actual operator on that larger space. Such a bound covers arbitrary
collective gauge-invariant excitations automatically, provided the same
interacting ground state is used on both spaces.

The missing substantive theorem is then a product-ground-state stability
theorem applicable to this unbounded onsite, bounded finite-range perturbation
operator. This note checks the available source adapter and its constants;
it does **not** claim that RPRM itself proves that stability theorem or its
threshold. The parent research task must inspect and apply the primary
theorem with its complete hypotheses.

This is stronger than continuing only the order-two vacuum expansion: a
uniform operator inequality can exclude every normalized excitation even
when the actual wavefunction is not reconstructed. It is still a small
magnetic-to-electric coupling route unless a further argument extends it.

## The exact inherited problem

For a finite open square/cubic lattice graph, take actual edge occurrences
`E_G`, distinct elementary square plaquettes `P_G`, normalized Haar measure,
and the metric/generators specified in
`research/ym2_global_phase_joint/GAP_BRIDGE.md`, Q2/Q8. No spin cutoff,
periodic identification, duplicated plaquette, or boundary charge is added.

```text
H_kin,G = tensor_(e in E_G) L²(SU(2), Haar),
H_phys,G = gauge-invariant subspace of H_kin,G,
h_e = -Delta_e/2,
H_G/(alpha hbar²) = sum_e h_e + r sum_p (1-a_p),
r = beta/(alpha hbar²),    a_p = (1/2)Tr(U_p).
```

Equality is Hilbert equality almost everywhere. The operator is the
self-adjoint product Laplacian plus bounded real plaquette multiplication;
its closed form domain is inherited from the product Laplacian. The requested
readout is a lower bound on the full quadratic-form Rayleigh quotient above
the interacting vacuum, uniformly over the stated graph family at fixed
admitted `r`. It is not a request for finitely many eigenvectors or a
finite-dimensional trace-coordinate ansatz.

The existing `research/ym2_relative_exclusion/RELATIVE_WEB_AND_EXCLUSION.md`,
R2/R3, already proves the exact equivalence between a positive relative gap
and absence of any sequence of normalized vacuum-orthogonal form-domain
vectors whose relative energy tends to zero. R4 already states the
one-sided lower-envelope implication. Those elementary results are reused,
not reintroduced as a new theorem here.

## Selected official premises and their actual operator transfer

| Source/result | Exact supplied premise | Transfer into this operator problem |
|---|---|---|
| `docs/proof-donut.md`, aperture/enclosure | Forward inclusion of concrete completion fibers in abstract fibers is enough for abstract emptiness to imply concrete emptiness. Reverse inclusion is needed for lifting existence, not for this exclusion direction. | Every actual physical bad trial state is also an ambient bad trial state when the quadratic form, ground energy and vacuum orthogonality agree. An ambient exclusion therefore suffices. |
| `MANIFESTO.md`, II.5.2 | Coverage of every intended source, faithful transitions, invariant preservation, and a landing implication carry the quantifier. Finite tables test only their own abstract obligations. | The uniform stability theorem must cover every admitted finite graph, all onsite spins, and all form-domain vectors. Checking several finite spectra or support stars is insufficient. |
| `MANIFESTO.md`, II.5, strict descent; `docs/core.md`, sections 11–12 | Regions may overlap, but they must cover every exceptional case; any returned smaller obstruction must be an actual admitted witness in a well-founded rank. | A future elimination/renormalization construction must control every support and preserve the operator domain and spectral question. A decreasing coefficient or smaller drawing is not a descent rank on actual low-energy states. |
| `docs/operations.md`, O03; `docs/core.md`, attachment | Fixed global port identities and the same full conjunction of seam predicates give associative retained attachment. Independent local consistency does not prove global consistency. | Shared lattice edges remain one tensor factor. Plaquette interactions are evaluated on those same occurrences; no product of independent plaquette Hilbert spaces or independently chosen local vacua is substituted. |
| `docs/operations.md`, O05/O05F/O06 | Exact operational folds preserve observations, enabledness, successor summaries; matched folds compose. Present-only sufficiency is weaker. | A compressed quantum representation must preserve the specified operator/form or required functional calculus. A trace quotient that only preserves the classical potential does not establish a spectral bound. |
| `MANIFESTO.md`, III.1.1–III.1.3; `docs/proof-donut.md`, prime-region certificate | Every composite `n<=B²` has a prime factor `<=B`; a complete certified prime list therefore covers every candidate in the enlarged region, at every finite stage. | The useful donor is an all-input rule rather than an expanding numerical census. The spectral analogue needs a theorem with graph-independent constants, not a prime label or arithmetic metaphor. |
| `MANIFESTO.md`, II.5.1 and hostile boundary example | Multiaffine interpolation has positive weights over the whole square; enlarging the grammar to quadratic terms destroys the inferred interior bound. | A finite head or sampled local sector is a valid enclosure only when all remaining operator contributions are rigorously included or bounded. This directly identifies the omission risk in an uncontrolled vacuum tail. |

The exact one-sided embedding is inclusion `i:H_phys,G -> H_kin,G`.
For the fixed finite compact source, positivity improvement gives a unique
positive ambient ground state. Gauge symmetry and uniqueness make it gauge
invariant, so ambient and physical ground energies and vacuum vectors agree.
For a normalized physical `f` orthogonal to that vacuum,

```text
<f,(H_G-E_0,G)f>_form >= Delta_ambient,G ||f||²
implies Delta_physical,G >= Delta_ambient,G.
```

This uses no inverse gauge-coordinate reconstruction. The singular loci of
a reduced trace chart are therefore not omitted exceptional excitations:
the ambient form covers the complete physical form-domain inclusion. In the
existing two-square exact quotient, `GAP_BRIDGE.md` Q3–Q7 already treats the
singular boundary through Haar pushforward and an inherited closed operator
domain; point values on a null stratum are not extra L² states.

## Concrete local data for the stronger stability candidate

The following are exact consequences of the accepted operator convention:

```text
h_e >= 0,   ker h_e = C*1,
spec(h_e) = {2j(j+1): j=0,1/2,1,...},
gap(h_e)=3/2,
||a_p||_infinity=1,
support(a_p) has four edge occurrences,
#{p: e in support(a_p)} <= m=2(d-1),  d in {2,3}.
```

Subtracting the scalar `r|P_G|` preserves every gap and leaves
`sum_e h_e-r sum_p a_p`. The global perturbation norm estimate is extensive,
`<=|r||P_G|`; its **local** norm sum is instead

```text
sup_e sum_(p containing e) ||-r a_p|| <= 2(d-1)|r|.
```

This is a bound on the actual Hamiltonian terms, not a supposition about
`log(rho_G)`. It is the natural quantitative port for a finite-range
product-ground-state stability theorem.

If the theorem expects sites of `Z^d` rather than edge sites, group the `d`
positively oriented outgoing edge factors at each vertex `x`. The onsite
space becomes `L²(SU(2)^d)`, its onsite Hamiltonian is the sum of those edge
`h_e`, its ground is still a unique product, and its gap is still `3/2`.
The plaquette anchored at `x` in directions `i,j` is supported on vertex
blocks `{x,x+e_i,x+e_j}`. Grouping the anchored terms gives

```text
phi_x = -r sum_(i<j, admitted anchored plaquette) a_(x,i,j),
||phi_x|| <= binomial(d,2)|r|,
support(phi_x) subset x+{0,e_1,...,e_d}.
```

The interaction range and this bound do not grow with graph volume.
For graph subfamilies obtained by deleting sites/edges/plaquettes, an
embedding into a finite box can add unused edges as decoupled free factors
and set absent local plaquette terms to zero. The exact theorem must allow
these spatially varying bounded perturbations/boundaries; translation
invariance must not be silently assumed. Any added decoupled factor has gap
`3/2`, so a proved ambient lower bound may be reduced to its minimum with
that number without changing the desired physical conclusion.

**Candidate claim ceiling:** after the parent verifies an applicable theorem,
there may be constants `r_*(d)>0` and `c(d,r)>0` such that for every admitted
finite graph and `|r|<r_*(d)`,

```text
H_G-E_0,G >= alpha hbar² c(d,r) (1-P_0,G)
```

as a quadratic-form inequality on the full edge Hilbert space, and hence on
the physical sector. This would directly exclude all arbitrarily cheap
collective excitations at that fixed coupling/energy normalization. No
numerical threshold, all-coupling claim, continuum construction or physical
scale-uniform bound is asserted by this retrieval note.

## Current completed YM material: what is actually closed

`research/ym2_connected_vacuum/RETURN_TO_WILLIAM.md` and the independent
conditional review report a completed two-square actual-vacuum orientation
witness and an order-two connected head on the open square/cubic graph
family. The final export evidence reports three new checkers run from the
final extraction, all successful, with 68 matching payload files. These are
source-reported executions; none was replayed here.

1. Gauge integration of zero-integral one-link residuals kills open-ended
   supports. On the two-square graph, the four nonempty no-leaf support
   shapes are a complete finite graph census; no-leaf alone is not a
   sufficient spin-intertwiner criterion.
2. The absolute envelope on `N` edge-disjoint squares obeys
   `eta_G(d) >= (1+d^4)^N-1`. This refutes the volume-uniform usefulness of
   that particular absolute envelope. It is not evidence of a vanishing gap.
3. In the order-two log-density coefficient, edge-disjoint pair terms cancel;
   adjacent pairs retain `(4w-3ab)/702`. The actual-vacuum witness controls
   its entire remainder on the stated two-square small-coupling interval.
4. For a supplied positive factorization, normalization cancels all factors
   wholly outside a patch. Only factors joining the updated inside variable
   to the changed exterior occurrence contribute. The bounded log tilt gives
   `TV<=tanh(L/4)`.
5. `NEXT_CONDITIONAL_PORTS.md` CP1–CP8 proves

```text
sum_(j!=e)c_ej <= m r + [16m(m-1)/117]r²
                  + (1/4)sum_(j!=e)epsilon_ej.
```

   Its full local support count includes 7 incident adjacent pairs in two
   dimensions and 42 in three. Counting only pairs whose two plaquettes
   both contain `e` misses 6 and 36 factors respectively. The actual
   `epsilon_ej` is a full exterior-change oscillation of the exact vacuum
   log-density remainder. Its graph-uniform summability remains OPEN.
6. `NEXT_GLUE_LEMMA.md` already proves that actual-vacuum variance
   factorization with constant `C_mix`, integrated conditional Poincare
   constant `C_loc`, and patch-overlap multiplicity `m_patch` imply
   `gamma_G >= alpha hbar²/(2 C_mix C_loc m_patch)`. The two-spin correlation
   control shows that bounded local constants and bounded overlap alone do
   not supply uniform `C_mix`.

These results are substantive local/summed facts. They do not close the
remaining conditional route. The direct operator-stability route uses the
same actual Hamiltonian and can be sufficient without first completing the
conditional density factorization.

## Latest expansion/compression continuation

The recovered-concept map and running backlog now route to
`research/expansion-compression-2026-09-12/README.md`,
`HISTORICAL-RESULTS.md`, and `LIVE-RESEARCH.md`. These were prioritized.
The dated live note's final refresh records the connected YM completion;
its earlier active-task statements are explicitly retained as historical
snapshots. They are not used as present-status facts in this note.

The new stagewise contract proves that exact compressed updates satisfy
`C_(n+1)(E_n(x,u))=Update_n(C_n(x),u)` precisely when observation constancy,
matching enabledness and successor constancy hold for equal current
summaries and the same supplied input. It separately requires bounds on
retained bits, peak bits, selection, update work and reopening. The reported
34,936 exact assertions are finite evidence for its stated small carriers.

The historical donor descriptions are useful but remain attributed:

- Audit99: an additive operator-language change yields `g'=gcd(g,k)`,
  `d=g/g'`, `r=g's+r'`, `q'=dq+s`; only the required migration tag reopens.
  The new worked factors `2,3,2` refute any assumption of a universal doubling
  ratio. Arbitrary new operator languages are outside that result.
- Audit116: `bq+d=b(q+1)+(d-b)` retains signed carry debt and its chart/radix;
  its specified local cost does not define a physical tension or universal
  compression schedule.
- Retained-child DAGs share repeated construction without unfolding it;
  their exact source scope and child access survive. A small root handle does
  not make its entire source or every question constant-cost.
- UTCCC and the corrected R1 Apply bridge distinguish semantic closure from
  representation construction/peak cost. Compact final answers alone do not
  bound the resources of growing intermediate descriptions.

For YM the exact transfer is to preserve actual interaction support, edge
identity, operator domain, energy normalization and the relevant remainder
or theorem hypothesis at each stage. None of these discrete donors proves
the vacuum's conditional response or a quantum spectral gap. The prior
source inspection already resolves this bounded donor question, so no new
historical Memory Fabric retrieval or Alpha/Quantum Research scan was needed.

## Retrieval boundary and verification

Read the repository README, handbook sections relevant to relations,
transport, coverage, probability and physical scope, recovered-concept
entrance and backlog; selected core/operations sections; Manifesto II.5 and
III.1; the whole proof-donut note; the named latest expansion/compression
notes; and the selected existing YM and BSD return/bridge reports listed
below. Searches were scoped to these official documents and the repository's
immediate research directory map. No claim is made that every official
document, every historical source, the full publications, or every current
research lane was read or semantically exhausted.

The BSD general return was inspected only for the coverage distinction:
bounded representatives permit a compatible tower to have an actual source,
whereas compatible finite labels alone do not; its total-Sha support and
general BSD obligations remain separate. No BSD theorem was transferred to
the YM operator. The current source files, rather than live task commentary,
are the evidence used here.

Verification here consists of source inspection, exact path resolution and
SHA-256 byte binding of selected sources. Hashes bind the observed files;
they do not prove the mathematical contents. No numerical simulation,
finite-spectrum calculation, new mathematical checker or earlier campaign
was executed by this retrieval subtask.

## Selected source byte bindings

All paths below are relative to `C:/github/RPRM-open`. The byte table was
generated from those exact existing paths after writing the note.

| Exact source path | SHA-256 |
|---|---|
| README.md | ae52f9cd1dc31a58107c716e886622ee94e8d09b7ca6cf447eddef81bd10d6b0 |
| AGENT_HANDBOOK.md | e8a2c35794346956051afa153a2ac8fdca61c60a4b550834a0715d5cf9220a56 |
| recovered-concepts/README.md | 87a13153dbe084a62e9d6bbab5e7d0e7a14732f1677bc6d0f7ee47c04104b80f |
| recovered-concepts/NEXT-PAPER-BACKLOG.md | ed7ff6328b9d34eaf183994f7a51b4b149c3670b348e4ebed7bedaf51aedee04 |
| MANIFESTO.md | 1970db936f6b448c869e563559955e3199fdf688fceb9962fe2d47466510922e |
| docs/core.md | 7ef1490b41a59be92f42c5b6457e7ad1c40ceb43287d2d78a3ba6b3c767f2ca3 |
| docs/operations.md | 1f57f928e6bcb48b5d6c58b3abac0a1044edd99b050c7547c8522b7e4c61b4fd |
| docs/proof-donut.md | 7efda177fc3f4500842c88a7556dde6be3724b1f9194ee449da51c8ebcf5070a |
| research/expansion-compression-2026-09-12/README.md | 3d02e531f8581970ff11d09a4972a167bba12bde62e7224e9e6a0b03ec71ef02 |
| research/expansion-compression-2026-09-12/HISTORICAL-RESULTS.md | a735866e47e75268e8cc7272f1aa3e761f681a64c3b67b660cd7773372791b17 |
| research/expansion-compression-2026-09-12/LIVE-RESEARCH.md | a88760a237820d39ac4f6500e2092360a941e0a89d017a6fda6f93feeff53439 |
| research/expansion-compression-2026-09-12/RESULTS.json | ae7bfc0c9b3632d4c619430f97049c7d2b75a06a539da4ca7673903fc2c42e3f |
| research/ym2_relative_exclusion/RELATIVE_WEB_AND_EXCLUSION.md | 25ed4cf55045a61964f47e58914d52685296de271557d6f14379b0d6de8f6550 |
| research/ym2_relative_exclusion/RPRM_DONORS.md | 5816e807eea89798c06726a6b409898608bd5228deff6b0a2ea5a53257d95d6a |
| research/ym2_global_phase_joint/GAP_BRIDGE.md | 68e619f6e56b752e59609d52a9e2c5674a0ef47c1bdb8c9d06a3b6188d071a28 |
| research/ym2_global_phase_joint/NEXT_GLUE_LEMMA.md | fe9066999331a95bdc1ae31047ebf1a9ed0b173a5c3c5874b733128c0f1e0ef6 |
| research/ym2_signed_differences/NEXT_CONNECTED_OBLIGATION.md | ab0e55814b5a4575eec04707702c3bc5032367b85bc986bec5e918dadb68bec1 |
| research/ym2_connected_vacuum/NEXT_CONDITIONAL_PORTS.md | 0467fdbf3a3690eaa6b58b30213d7f1f2a642204b69cc7c84a960bb14e2026a4 |
| research/ym2_connected_vacuum/REVIEW_CONDITIONAL_PORTS.md | 5c3bcf16c4df27e437e78a1308e56763e91e97b42b5be90e1fc9a1ad9c0105bb |
| research/ym2_connected_vacuum/RETURN_TO_WILLIAM.md | 0f64d0cee3ceaa86adcb6c38ff9e0bbdf04224d8cd354652a476cb96daf3ab6d |
| research/ym2-connected-20260912-delivery/FINAL_EXPORT_EVIDENCE.md | 5bbd935773c22f16ce67764c17621aad31f0dffc440838d7898ae34ee988bd91 |
| research/bsd-general-01/README.md | ae59441bc80a32b5c534f98c25e5002c37a6060b443c71a6dd811c256613ef23 |
| research/bsd-general-01/RETURN_TO_WILLIAM.md | 14d319affa7a092d4d626ad43ed6dbbcd62d6ed12eb906b0ac36ad9e5082cbcb |
| research/rprm-consolidation-c2-20260912/PAPER_ROUTING_NOTE.md | 35dca7b04a23ff8e3a1cbf3177c8bc1202604e480e6efc300d7e5a9537e4f54a |
| research/liar-teacher-formalization-2026-09-12/RELATED-RESEARCH.md | fc8b002d65a06f4fc86889e26826393fa35e6a551651b8d49f03d487866544ae |
