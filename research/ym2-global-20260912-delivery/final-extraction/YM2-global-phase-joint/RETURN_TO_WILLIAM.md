# What moved, and where the gap is now

The proof donut did help: it exposed an actual missing part of the
dynamical proof, and we repaired it. We also took a direct quantum step.
For the same two interacting cells, we now have a proved lower bound on
the quantum excitation gap. The remaining problem can be stated more
sharply as an inequality about the joint vacuum across many cells.

## The geometric hole was real

Think of the two loop holonomies as having internal direction arrows
`u` and `v`. These are directions in the SU(2) color space, not arrows
drawn in ordinary physical space. The previous chart used their lengths
and angle as coordinates. That is useful while they are independent. At
alignment, or when an arrow shrinks to zero, a coordinate system built by
dividing by their angle loses its footing.

The actual field can go there. We found an exact state with both loop
holonomies equal to the identity but two nonzero, independent electric
directions. Close to that instant,

```text
|u(t) cross v(t)|² = 225 t⁴ + O(t⁵).
```

It is regular immediately before and immediately after, and its old
configuration chart is singular at the central instant. This is not a
numerical near-miss. The nonzero coefficient proves the crossing. The
physical phase state at that particular crossing still has independent
electric directions; chart failure need not mean a singular physical
phase orbit.

The repair is to keep the relations among **all four directions**:
the two loop vectors and their two electric momenta. We retain their
lengths, pairwise dot products, and oriented triple products, along with
the two scalar parts of the loops. That is sixteen redundant scalar
entries with explicit compatibility and Gauss constraints. Redundancy is
helpful here: we no longer need one angle-based coordinate frame to work
everywhere.

There is an exact polynomial rule for updating this joint. It continues
through all ranks, including zero, without reconstructing a color frame.
The proof identifies its complete physical-state fiber and commutes with
the full seven-link Hamiltonian flow for every real time. It preserves
the future magnetic-energy readout and more. This closes the particular
global continuation obligation left by the earlier calculation.

Orientation is a real part of the joint. Two lawful states have all the
same dot products and energy, but the outer loop trace starts moving with
derivatives `+6` and `-6`. The signed triple products distinguish them.
So even a complete list of pairwise angles can miss how the whole tuple
is oriented.

## We obtained a quantum gap on the finite graph

We supplied a quantum Hamiltonian explicitly: the standard compact SU(2)
link Laplacian plus the two magnetic plaquette terms, with gauge invariance
at every vertex. The Hilbert space contains every spin representation;
there is no spin cutoff or numerical spectral estimate here.

Write `alpha` for the electric coefficient, `beta` for the magnetic
coefficient, and keep `hbar` explicit. Then

```text
gap >= 6 alpha hbar² - 2 beta.
```

It is a positive lower bound when `beta < 3 alpha hbar²`. For the
explicit reference choice `alpha=beta=hbar=1`, it says **gap at least 4**
in those reference energy units. It is a bound, not a computed exact gap
or a measured mass.

The proof has an intuitive core. Gauge invariance prevents an isolated
nontrivial electric edge from ending at an otherwise empty vertex. A
nonconstant physical state therefore needs support containing a closed
loop. The shortest loop here uses four links, and the smallest nonzero
SU(2) electric cost per link is three in our normalization. Multiplying
by the kinetic prefactor gives an exact free electric gap of
`6 alpha hbar²`.

The magnetic potential is nonnegative, so the first ordered excited
eigenvalue cannot fall below that free threshold. Meanwhile, the constant
wavefunction is a legal trial state with mean potential energy `2 beta`,
so the true vacuum energy is no greater than that. Subtracting gives the
bound. We did not assume that the interacting vacuum itself is constant.

The geometry-to-quantum bridge includes the measure and operator domain.
The three configuration traces carry a uniform Haar pushforward measure
on their curved allowed region. The Hamiltonian and its boundary behavior
are transported from the compact source by a unitary map. A choice of
coordinate boundary condition is therefore not secretly producing the gap.

## Why this does not yet find the continuum mass gap

The finite-graph result is a real quantum spectral statement. A finite
compact graph also has an isolated vacuum for every fixed finite magnetic
coefficient; that fact alone gives no useful bound uniform in system size.
The challenge is survival through enlargement and the continuum limit.

Our simple estimate exposes its own limit. For `N_p` plaquettes it becomes

```text
gap >= 6 alpha hbar² - N_p beta.
```

The vacuum trial-energy allowance grows with the number of cells while
the first local loop cost stays fixed. The lower bound eventually becomes
uninformative. This does not show that the true gap closes: it shows that
this comparison stops measuring the excitation relative to the actual,
correlated vacuum accurately enough.

Your point about relational scaling matters here. Dividing all energies
by `alpha hbar²` leaves the ratio `beta/(alpha hbar²)`. A change of units
does not remove that interaction ratio. Changing lattice spacing and
coupling is a physical change of the family, and the ratio must travel
with it. The usual weak-coupling route also leaves the positivity region
of this particular bound. We cannot keep the number “4” by silently
renormalizing a different model back to our reference choice.

## What the joint idea must do next

We derived a precise sufficient rule for combining patches. Three
quantities enter it: a local conditional fluctuation bound `C_loc`, a
joint correlation bound `C_mix`, and the maximum number `m` of patches
using the same edge. If their stated inequalities hold for the actual
vacuum measure, then

```text
gap >= alpha hbar² / (2 C_mix C_loc m).
```

The conditional theorem is proved in [NEXT_GLUE_LEMMA.md](NEXT_GLUE_LEMMA.md).
The useful constants for the Yang–Mills family remain to be established.

Here is the missing issue in a tiny exact example. Two signs can usually
agree: `++` and `--` are common, while disagreement has total probability
`epsilon`. Each individual sign barely fluctuates once the other is
held fixed. But the pair as a whole can distinguish the two common
collective states. For the readout `x+y`, the whole variance divided by
the sum of the two conditional variances is exactly `1/(2 epsilon)`.
It becomes arbitrarily large even though the local variance estimates
stay bounded.

That example is not an SU(2) vacuum. It isolates the logical mistake a
successful joint proof has to avoid: small local fluctuations do not by
themselves control a collective fluctuation. The same vacuum, shared edge
occurrences, and correlations must survive the assembly.

The next mathematical work is therefore concrete:

1. Derive conditional patch bounds for the true vacuum, including how the
   exterior configuration affects a patch.
2. Prove the joint correlation estimate without losing control as the
   number of patches increases.
3. Carry the resulting energy bound through lattice spacing and coupling
   changes in physical units, with the required quantum theory and
   observable convergence supplied in the limit.

The proof-donut analogy is useful exactly at this point: it keeps those
three obligations around the same unresolved question. It cannot fill
them merely because the surrounding finite pieces have been solved.

## What was actually verified

The derivations use established lattice Hamiltonians, compact-group
representation theory, and spectral principles, with explicit calculations
and proofs supplied here for our chosen graph. They are not claimed as
new-to-literature theorems. RPRM provides the joint/coverage/continuation
discipline and preserves its broader meanings beyond this realization.

The new checks use exact rational or integer arithmetic: 28 full-graph
vector-field comparisons, six regular bridges, 3,008 invariant controls,
and all 128 support subsets plus Pauli/drift identities. Independent
review found no substantive defect within the stated claims. These are
written proofs with bounded executable corroboration, not new Lean
certification. Final-export sidecars record replay from the delivered ZIP.

No publication, installation, large simulation, paid compute, git mutation,
or other-lane work was used. The earlier accepted evidence remains intact.
