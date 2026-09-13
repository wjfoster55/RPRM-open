# Connect to a new reference, carrying its correction

12 September 2026. The next bounded YM2 research step. Publication remains
on hold; the prior interacting-sector results and exported proofs are
accepted starting evidence and remain unchanged.

**Two useful conclusions survive this investigation.** First, the
0.6/0.4 and -0.2 intuition has an exact relation to the proved 1.5 cover
factor. Second, changing to a new positive vacuum reference is a valid
route. We constructed one, proved a gap for its reference operator, and
derived precisely what would transfer that control to the actual field.
The transfer's uniform analytic estimate remains open.

![The compensator and calibrated reference handoff](vacuum_handoff.png)

## 1. What the numbers mean here

Our cover has a total physical variance contribution W=1.5 and a maximum
energy load Lambda=1. Normalize those two quantities by their sum:

```text
p = 1.5/(1.5+1) = 0.6,
q = 1/(1.5+1)   = 0.4,
p/q = 1.5,
-p+q = -0.2.
```

That is an exact adapter from this proved cover to your complementary
pair. Relative to the midpoint (0.5,0.5), the coordinates are offset by
(+0.1,-0.1); the oriented difference has magnitude 0.2. With discrepancy
delta=p-q, the general relation is

```text
(p,q)=((1+delta)/2,(1-delta)/2),
p/q=(1+delta)/(1-delta).
```

This explains how the ratio, halves and offset can describe the same
relationship. The adapter preserves that ratio; it does not add an
extra physical amplification. Nor are p,q the original three block
weights, which remain (0.5,0.5,0.5). We proved that inserting 0.6 and
0.4 into two of those weight slots gives a maximum factor of 1.4,
whatever positive third weight is chosen. The third weight must be 0.4
to attain that maximum. With a common block estimate, equal weights
already exhaust the three-direction optimum.

[COMPENSATOR.md](COMPENSATOR.md) contains the full algebra, reference
shift, complete scalar and weight fibers, and hostile cases. These are
typed rational-coordinate operations. They do not replace the broader
RPRM meanings of pressure, retention, centered coordinates or the
teacher framework with one narrow numerical interpretation.

## 2. What the BSD and liar/truth tasks contributed

I inspected **Run BSD E5 test 01** and **Locate liar-truth framework**,
including their latest three returned turns and their relevant completed
source notes. [RELATED_TASKS.json](RELATED_TASKS.json) records that scoped,
read-only inspection. The other tasks were not modified or interrupted.
No previous donor checkers were rerun.

The teacher result supplies a useful rule: a newcomer can become the
reference when its decoding is calibrated and the next operations remain
recoverable. Keeping today's answer alone is insufficient. The finite
seven/eight and Hamming constructions are its original examples; no
binary-state identification with SU(2) is being inferred.

BSD supplies a complementary test. Its completed operational work has
points whose separate heights agree but whose heights after combination
with the same other point differ. It must retain the mixed pairing.
It also distinguishes agreement along a line from knowing the exact
multiplier. These are attributed donor results, not new arithmetic
proofs performed in this task.

Transferred to YM, the lesson is concrete: the new reference must carry
the field's full operator and the joint response of overlapping groups.
Matching a picture or normalizing a function does not establish that
calibration. [DONOR_HANDOFF.md](DONOR_HANDOFF.md) records the source
mapping and exact donor hashes.

The BSD task's later prime-seam continuation was still active at the final
status check. It reported a candidate multiplier `(12+5i)/13` and was
testing what it preserves. That update is preserved separately in
[BSD_STATUS_SNAPSHOT.json](BSD_STATUS_SNAPSHOT.json); it is not promoted
here to a completed comparison theorem or a YM estimate.

## 3. The new reference and why a correction travels with it

Keep the finite open SU(2) lattice Hamiltonian, all spins and every vertex
gauge constraint. In the existing energy units, remove the harmless
constant and write A=T-rS, where S is the sum of the plaquette traces
and T=-Delta/2.

For any positive, smooth, normalized, gauge-invariant function phi, write
a physical wavefunction as Psi=phi f. In the measure nu_phi=phi^2 mu,
this is an exact change of coordinates. The original Hamiltonian becomes

```text
reference motion + residual energy,
K_phi + R_phi,
K_phi = T-grad(log phi) dot grad,
R_phi = (A phi)/phi.
```

If phi is the exact vacuum, R_phi is constant. Otherwise it is a function
of the field configuration and must be retained. Changing to another
positive reference is still allowed: f changes by the ratio of the two
references and the full operator is transported with it.

This establishes your proposed alternative. We need not insist that one
old formula describe the vacuum everywhere. We can use another reference
or another construction, provided we prove its connection. On the same
fixed finite Hamiltonian, two normalized strictly positive *exact* vacua
are the same vacuum; the freedom here is in the reference and construction.
An infinite-volume theory would require its own further analysis.

We made the new reference explicit:

```text
phi_r = exp(rS/6) / ||exp(rS/6)||_2.
```

It cancels the first-order source exactly. The remaining residual is

```text
R_phi = -(r^2/72)|grad S|^2.
```

We then proved a physical gap for K_phi for r<1/m, where m=2(d-1):

```text
g_phi >= [d/(d-1)](3/2)(1-mr) exp(-2mr/3).
```

This reference estimate covers a larger interval than the old actual
vacuum construction, r<9/(128m). It is not yet an enlargement of the
actual YM interval, because the residual has to be transferred too.

## 4. The first transfer estimate fails in a specific, useful way

The min-max principle gives a direct actual-gap bound through an
approximate reference:

```text
actual gap >= reference gap
              - [mean reference residual - minimum residual].
```

Thus a reference route can establish a physical gap without first solving
the exact vacuum equation. This application uses the established
[min-max theorem and comparison principle, Teschl 4.10–4.11](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf#page=131).

But for N disjoint square plaquettes connected by tree paths, the residual
oscillation is exactly Nr^2/18. Even the sharper mean-minus-minimum loss
is at least Nr^2/72. This is an exact witness in the admitted SU(2)
graph family. As N grows, the estimate charges all those contributions
against one excitation and becomes inconclusive.

That does not show the actual gap gets smaller. It identifies waste in
this comparison: many local energy contributions can shift the vacuum
and an excited state together. Charging their entire bulk variation
discards that common shift. A better transfer needs to bound their effect
on the *difference* between the two energies.

[TRIAL_REFERENCE.md](TRIAL_REFERENCE.md) gives the construction, residual,
gap comparison and exact witness. Its [independent mathematical review](INDEPENDENT_REVIEW.md)
checks the signs, factors, graph admissibility and mean conventions.

## 5. A local handoff criterion exposes the next two missing estimates

Write the actual vacuum as psi=phi_r exp(v), up to normalization. The
reference supplies the main shape; v is the actual correction. We
derived a sufficient gap theorem using two properties of this correction:

1. **One-link response, d_v:** how much 2v can change when a single link
   changes, with every possible exterior configuration admitted.
2. **Combined influence, b_v:** how strongly all the other links together
   can change that one-link response, measured by a sum of mixed
   oscillations.

If d_v<=D stays bounded across graph sizes, and b_v<=B satisfies a uniform
strict margin mr+B/4<1, then

```text
actual physical gap / E_el
 >= [d/(d-1)](3/2)(1-mr-B/4) exp(-2mr/3-D).
```

This is a written conditional theorem about the actual vacuum. It permits
a different reference to carry most of the variation; the complete log
vacuum need not fit the earlier small norm ball. What remains open is
proving these bounds for the actual correction beyond the current window.

The distinction between the two estimates matters. Imagine every small
region is individually easy to move, but the entire field tends to choose
one of two coordinated arrangements. Local freedom does not guarantee
an inexpensive transition between the arrangements. We constructed a
smooth, gauge-invariant reference-measure family illustrating this
exactly: every one-link density ratio stays bounded, while a collective
physical fluctuation has gap at most a constant divided by N. This is a
control against an insufficient handoff assumption, not a counterexample
to the retained local YM Hamiltonian. [VACUUM_ATLAS.md](VACUUM_ATLAS.md),
section 8, gives the complete proof and that scope boundary.

The correction itself satisfies the exact reference equation

```text
K_phi v = -Q_phi R_phi + (1/2)Q_phi |grad v|^2,
Q_phi h = h-mean_(nu_phi)(h).
```

We therefore have two substantive routes to pursue: control this actual
correction locally and collectively, or compare excitation energies
through the residual without a growing bulk penalty. Applying exactly
the old absolute norm estimate in the new chart reproduces the old
construction ceiling; that attempt was checked and retained too.

## 6. What is closed, and what remains

The ratio/offset adapter, weight optimum, exact chart handoff, explicit
new reference, reference gap, residual comparison, and separating
witnesses have written derivations. The transfer theorem has explicit
hypotheses. The new checker passed **19,621 exact assertions**, including
8,000 weight triples, the residual-sensitive two-state control, chart
composition, scalar restart identities and finite collective-dependence
controls. These corroborate bounded calculations; the general SU(2)
claims rest on the written arguments and their admitted inputs.

The unresolved research target is now: **make the calibrated handoff
uniformly accurate for the actual field, including its collective
response.** Neither a further numerical coincidence nor normalization
of a trial function supplies that estimate. The current actual coupling
window is unchanged. Continuum existence, control along the physical
scaling trajectory, and a positive continuum mass gap remain further
obligations. This turn narrows a route toward them; it does not solve them.

The packet labels established spectral/conditional ingredients, accepted
project evidence, new written derivations, finite checks and open ports
separately. It makes no literature-priority claim. The final portable
export includes source snapshots and the preceding frozen overlap ZIP;
only the new checker is executed during final replay.
