# Operational continuation: what helped and what remains

I inspected **Run BSD E5 test 01** read-only and followed the operational
number idea into a concrete Yang-Mills estimate. The useful connection is
to keep the information an operation will need next, even when the current
scalar answer does not show it. Its broader RPRM operation-and-relation
profile meaning is preserved in [BSD_DONOR.md](BSD_DONOR.md).

BSD supplied an exact example: an operation returns to one at a coarse
precision and leaves a nonzero remainder at a finer precision. A proposed
decimal reversal rule failed its full next-precision fiber. Both results
helped select the question to ask here; neither supplies a gauge-field law.
Its completed turn added an even closer example: 5426 and 4796 both fold
to 566, but the same operation on their original columns produces next
displays 687 and 587. A retained weighted digit record restores every
specified future display. This is the same preservation question tested
below with kinetic components, on a separately declared physical carrier.

## What we found

On two actual adjacent SU(2) squares, their cross response splits into
two kinetic components with energies 9 and 13. They can cancel at one
configuration and still have a nonzero response under the next operation.
One exact example has zero current cross response but inverse-kinetic
response 1/156. Two distinct response scales recover the two components
exactly. The original two-square trace geometry was already established
in the preceding packet; this continuation uses its operation structure.

Keeping those components separate exposes a second useful distinction:
the energy-9 component no longer depends on the shared link. The old
local estimate charged it to that link. Removing that charge, while also
retaining the actual orientation of bent pairs, lowers the cubic-lattice
source coefficient from 29.5 to approximately 24.875 (about 16%).

This changes a proof of the actual vacuum, not just a trial state. Using
the accepted all-spin contraction and conditional-cover argument gives:

| Three spatial dimensions | Previous simple certificate | This continuation |
|---|---:|---:|
| Gap lower bound through r=1/12, in E_el units | about 0.129 | about 0.2853 |
| Further proved interval | — | r<=7/80, gap>=0.12746 E_el |

The latter interval is 5% larger than the preceding stated endpoint.
The model, metric, coupling normalization, all spins, full gauge
constraints and volume-uniform quantifiers remain the same. These are
sufficient lower bounds, not observed spectral values or sharp transitions.

The derivation is in [COMBINED_RESULT.md](COMBINED_RESULT.md), the exact
coefficient calculation in [CHANNEL_SOURCE.md](CHANNEL_SOURCE.md), and
the continuation law and hostile cases in
[SPECTRAL_CHANNEL.md](SPECTRAL_CHANNEL.md).

## The remaining problem, in the lens language

Changing the magnification really can help. For a kinetic component with
energy lambda, one particular scale adjustment multiplies its response
by lambda/(lambda+z). A fixed positive z suppresses a small lambda, but
barely affects a lambda much larger than z. The exact one-square family
in the proof contains arbitrarily large lambda, and its improvement
factor tends to one. That gives an explicit reason the fixed adjustment
cannot control every scale uniformly.

A relational adjustment could keep z comparable to lambda, preserving
a useful ratio. What must now be proved is that such an adjustment
transports the **whole interacting equation** consistently. Multiplication
mixes components; a rule for one isolated component does not specify what
happens when two components combine. A successful next estimate must
retain those combinations and bound their total response across all
spins and all graph sizes. Possible quantitative routes are controlling
the actual vacuum's high-energy tail or exploiting cancellations within
one complete output coefficient. Neither is established in this packet.

This is why the obstruction is informative: it identifies a specific
missing relational bound rather than requiring a separate hardcoded rule
for every scale. A bare renaming of the scale would not supply that bound.

There is also a later physical obligation. Our present windows concern
finite lattice coupling. In the retained normalization the continuum
direction takes r=8/g_b^4 to infinity as the bare coupling tends to zero.
Even a bound that works at every graph size in our finite r window does
not cover that direction. We still need continuum construction and a
positive excitation scale in the limiting physical units. The full
quantum Yang-Mills mass-gap ambition remains OPEN.

## Evidence and attribution

The proofs are written mathematical derivations with an independent agent
review, not formal proofs or external peer review. The new standard-library
checker verifies exact sparse coefficient matrices, local incidence stars,
response identities, hostile examples and contraction constants. Prior
checkers were not replayed. [RESULTS.json](RESULTS.json) records its complete
receipt, and [OPERATIONAL_REVIEW.md](OPERATIONAL_REVIEW.md) binds the final
reviewed theorem bytes.

Established representation theory, spin addition and character geometry
are separately attributed in [LITERATURE.md](LITERATURE.md). The specific
source accounting, composed constants and separating uses above were
derived in this continuation; this does not claim priority over the
literature. The printed numerals are not offered as a new physical law.

The ZIP includes exact source snapshots, the preceding frozen YM packet,
new derivations, replayable checks, and the visual. Its adjacent final-export
evidence records fresh-extraction replay and byte integrity. Publication
remains on hold; no paper, installation, paid compute, simulation campaign,
git commit/push/merge, or other-lane mutation occurred.
