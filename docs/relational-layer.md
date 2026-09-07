# The relational-layer proposal

**RPRM means Relational Pressure Retention Model.** The name comes from the
physics idea that motivated the research. Pressure and retention name
proposed roles in how relational states change and persist; a physical model
must define those roles precisely, including any units and evolution laws.
The framework retains that name as its mathematics develops.

**Physical hypothesis and mathematical observation limits.** RPRM proposes
that observable objects, forces and geometry may arise from an underlying
organization of relations and lawful changes. The physical identification is
open. The preservation and nonidentifiability statements below concern
specified mathematical models.

Read [Part I, section 7](../MANIFESTO.md#7-the-relational-layer-proposal-and-limits-of-observation)
for the connected argument. The [core definitions](core.md) and
[operational laws](operations.md) supply the formal terms.

## What “underlying” means

A relational layer is a proposed source of observed behavior: states with
typed roles, constraints, interactions and allowed continuations, together
with a map to measurements. It is an explanatory ordering. It does not by
itself assert an extra spatial dimension, a discrete network, a substance,
a preferred numeral base or an unmeasured energy.

In the mathematical unification result, a relational presentation encodes an
already supplied structure and preserves its statements. In the physical
proposal, we ask which structure describes the source of observations.
The second task requires physical premises and evidence as well as a
correct encoding. Expressibility in the common language does not answer it.

## Closed observations can leave an open source question

Let `S` be an admitted state carrier, `T_a` deterministic partial actions,
`O` an observation and `C` a retained description. If equal C-values have
equal observations, matching enabledness and equal successor C-values,
the updates and observations descend to C's reached image. Induction gives
equal retained outcomes after every finite action word from equal summaries.

Consequently, a source property Q that differs between two states with equal
summaries cannot be recovered from those summaries and their permitted
future responses. This is a direct application of question factorization
and operational factorization. It is a limitation relative to the stated
actions and observations, not a theorem about every possible experiment.

Here “closed” means sufficient for continuation of a specified description.
Source recurrence, topological closure, proof coverage and causal trapping
are separate notions with separate definitions. None implies the others
merely because the same word is used.

## A complete four-state example

Admit `S={(r,h): r,h in {0,1}}`. Read only `r`, and allow one total action
`tick(r,h)=(1-r,1-h)`. Use `C(r,h)=r` as the summary.

Starting from `(0,0)` or `(0,1)` gives the same visible sequence
`0,1,0,1,...`. Both hidden bits flip at every step; their values remain
different. The formula after k ticks is
`(r XOR (k mod 2), h XOR (k mod 2))`, so this agreement follows for every
finite k, not from inspecting an initial sample. The summary update is
`r -> 1-r` and needs no value for h.

The current hidden bit has a complete MANY fiber at each visible value.
Within this supplied model, its alternation law is nevertheless known.
Knowledge of a relation therefore need not recover every participating
value. That conclusion is conditional on the supplied model and observation
contract.

Now admit another action, `reveal(r,h)=(h,h)`. Applied to `(0,0)` and `(0,1)`,
it gives different visible outputs. The old summary ceases to support all
admitted actions. A new sensor reading h has the same separating effect.
This is why “never distinguishable” must name its intervention family.

There is a second hostile control: a two-state source with only r and the
update `r -> 1-r` produces the same original read/tick observations. Those
observations cannot establish that the extra h-coordinate physically exists.
An unseen coordinate can be consistent with evidence without being required
by it. A candidate layer needs its own justification and comparison with
such alternatives.

## What abduction can establish

A constructive example uses real coordinates x,y,z with observed
differences `y-x=2` and `z-y=3`. The complete source fiber is
`{(a,a+2,a+5): a in R}`. Every member gives the unmeasured difference
`z-x=5`, while the common offset a remains undetermined. The cycle sum
`(y-x)+(z-y)+(x-z)=0` is a compatibility law, not an observation of an
absolute origin. This is exact conditional inference on a supplied carrier;
a physical use still needs a justified measurement law and uncertainty.

Declare a candidate family H and how each candidate predicts each admitted
observation. A record y defines the joint compatibility fiber F_y. Source
selection and the inference of a source property are different questions:

| Complete fiber | Lawful conclusion |
|---|---|
| Empty | The observations and supplied candidate contract are incompatible; inspect the premises and measurement model. |
| One member | The candidate is identified within H, conditional on the source belonging to H and the observation model being correct. |
| Several members with the same Q-value | Q is determined within the model even though the full explanation is not. |
| Members with different Q-values | The available observations do not determine Q. Retain the alternatives or find a separating observation. |

Abduction generates or ranks possible explanations. Deducing a shared
property from a complete fiber is a conditional logical consequence. A
ranking additionally needs its stated criterion; it does not change MANY
into a proof of ONE. No finite hand-picked family proves that all possible
physical explanations have been considered.

For stochastic models, compare predicted observation distributions under
the specified interventions. A finite sample is not exact equality of
distributions; uncertainty, measurement error and statistical power require
their own model. The deterministic example above supplies no shortcut
around those requirements.

## Gravity: a precise target for a source law

The [gravity chapter](../MANIFESTO.md#iii10-gravity-magnetic-motion-and-cosmic-expansion)
derives the exact radial receiver `(r,u,j)` for a supplied Newtonian pair.
It retains separation, radial velocity and squared specific angular
momentum. Its fibers consist of simultaneous rotations of the full relative
position and velocity. The written equations continue these radial values
without retaining spatial orientation.

A proposed deeper state s, evolution `Psi_t` and readout C must establish
`C(Psi_t(s)) = Phi_t(C(s))` if it claims exact agreement with the supplied
radial flow Phi. An exact operational bridge also needs
`s in dom(Psi_t) iff C(s) in dom(Phi_t)` throughout the stated comparison
regime, with initial-state coverage, clock, units and parameters. Equality
only when both sides happen to exist can conceal different stopping times.
Approximation needs domain guarantees and an error bound. Establishing that
equation by definition gives an encoding; deriving it from independent
physical premises would supply further explanatory content.

The same rule must address infall, circular motion and outward escape.
Different hidden sources could share every radial future; a spatial or
other measurement may distinguish them. Radial sufficiency alone therefore
proves neither universal invisibility nor a unique physical source.

## Black holes: observation, continuation and escape

The [black-hole chapter](../MANIFESTO.md#iii8-return-depth-exterior-observations-and-black-holes)
keeps a changing internal depth behind a constant address, then treats
finite graph reachability and a supplied spacetime separately. This makes
three questions explicit: what changes, what can be observed, and what
paths can reach an exterior.

In the supplied Schwarzschild geometry, the horizon is a causal boundary,
and an ingoing chart is regular there. A choice to discard information in a
summary is not itself that causal boundary. [Tong, sections 6.1.2–6.1.3](https://davidtong.org/teaching/general-relativity/grhtml/S6)

Identifying the return model with a black hole would require physical
states and units, a clock, a map to events and paths, and coverage of the
escape question. Exterior agreement could constrain a candidate while
leaving its internal history unresolved. It cannot establish that the
particular depth variable in our toy model exists in nature.

The proposal is usable as a research question now: specify a relational
source, derive what its observations force, retain what they leave open,
and seek the experiment or further theorem that distinguishes competing
explanations.
