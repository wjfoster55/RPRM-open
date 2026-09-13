# The next joint: two neighboring interacting cells

I read the relevant recent discussion in both **Review Missing Concepts**
and **Explore Birch Swinnerton Dyer Conjecture**. Two ideas were useful:
preserve the compatibility at a shared boundary, and retain a way to reopen
what a coarser description sets aside. I used them to obtain a spatial
result: an exact shared-edge witness and a closed dynamical joint for two
neighboring SU(2) cells on their regular domain.

This is new work in this task using established lattice gauge theory and
ordinary invariant geometry. It is a finite classical lattice model with
seven moving links and Gauss constraints at all six vertices. It is a new
declared model, distinct from the earlier exact homogeneous continuum sector.

## What the geometry is doing

Imagine each cell carries a little instruction for how a color frame turns
after going around that cell. The mathematical instruction is an SU(2)
matrix, called a loop holonomy. Its trace tells us the amount of the turn
without retaining the direction of its color axis.

Each separate cell can therefore give the same reading in two arrangements.
But when the cells share an edge, their instructions act on that same edge.
We have to compare their axes in a common frame. That comparison requires
transport along a specified connector: the field itself tells us how the
frames at different places are related.

In that common frame let the two color vectors be u and v. The shared edge
feels their difference, u−v. The strength of that force contains

    |u−v|² = |u|² + |v|² − 2 u·v.

The dot product u·v is the missing relationship. It measures their alignment.
The other six edge forces are fixed by the separate cell readings. This
explains why the relative angle matters even when those readings do not move.

The new visual has two controls for a reason. Changing the relative angle
changes this actual joint. Rotating the common frame rotates the whole
picture together and leaves every displayed physical readout unchanged.
The color-plane picture is an internal-space diagram, not a claim that
color vectors point along those directions in ordinary physical space.

## The exact test

Both checked states start with zero electric fields, total magnetic energy
4/5, and zero instantaneous transfer. Both have genuinely noncommuting loop
matrices. Their magnetic energies begin bending at different rates:

    State A: B''(0) = −128/25.
    State B: B''(0) = −544/125.

These are exact fractions from differentiating the actual constrained
Hamiltonian. State B minus state A has

    B_B(t)−B_A(t) = (48/125)t² + o(t²).

So this is a difference in future behavior. It is not an artifact of choosing
different gauges or drawing a straight line through a curved landscape.

We also solved the whole initial-angle question. For fixed separate loop
readings, all admitted relative angles give one explicit closed interval of
possible B''(0) values. A bound excludes values outside that interval and
an explicit construction realizes every value inside. This implements the
positive/negative approach from the other chat without checking every state.

## The positive repair is a dynamical joint

Let a and b be the separate half traces, and w the half trace around the
joined outer boundary. Those three numbers determine the joint configuration
up to the admitted gauge transformations. They retain both the cell readings
and their relative relationship.

For motion, retain three conjugate momenta as well. These momenta encode
motion of the joint shape; they are not three extra energy totals. There is
an explicit Hamiltonian for those six coordinates:

    H = 1/2 pᵀ M(a,b,w) p + 2−a−b.

The matrix M is written out in PHASE_CLOSURE.md, along with all six evolution
equations and the reconstruction of a complete physical state. Its entries
come from which loops share which links. The numbers 4, 4 and 6 count the
edges of the two squares and the outer rectangle; cross terms express their
overlaps. Other entries depend on the current joint geometry.

This gives a precise example of your relational-coefficient intuition.
One derived rule updates the coefficients as the shape changes. We do not
have to fit a fresh set of coefficients at each state. And because the
Hamiltonian stays within these six coordinates, repeated evolution does
not keep asking for another omitted derivative.

The proof holds while the two color vectors are independent. Six is the
number of physical phase coordinates for this regular two-cell model; we
have not shown a reduction below its physical degrees of freedom or a speed
advantage over conventional reduced coordinates.

## What becomes reusable across size, and what still needs work

**Ordered joining already has a uniform law.** The same SU(2) multiplication
works when a factor is itself an earlier product. We proved a sufficient
joint for every supplied finite tuple: scalar parts, mutual dot products,
and oriented triple products. The rule is algebraic and respects
parenthesization. No fixed eight/nine/four count was imposed on it.

**Three factors expose handedness.** With three independent color axes,
all pairwise angles can agree in two mirror arrangements, yet an ordered
triple loop has a different trace. There is an exact rational witness in
STATIC_JOIN.md. Thus a joint that works for two factors must preserve the
orientation needed by a later third factor. This is a change in the
receiver's requirements, not a refutation of the earlier homogeneous energy
joint, whose energy receiver did not distinguish its mirror branches.

**The outer boundary does not determine the inside energy.** Even the full
matrix W=UV, stronger than its trace, can be identical for two splits with
fine magnetic energies 26/25 and 18/25. We solved the entire split:

    choose U freely; then V=U⁻¹W.

That is the recovered-information idea in a concrete form. Keep W for the
outer question and U as the reopening port. If U is not supplied, the full
possible energy interval remains available. For some threshold questions
the interval already settles the answer; others require reopening the split.
An outer-loop formula with one new overall coefficient cannot reproduce
different fine energies at the same W.

**The regular chart has an explicit boundary.** When all links are identity,
a nonzero electric circulation can still satisfy Gauss. The trace coordinates
have zero first derivatives there, so our finite canonical coordinates
cannot encode every such state. The physical field is perfectly meaningful;
the chosen chart is insufficient. The next local obligation is an overlapping
phase description that handles those aligned or central configurations and
has a proved transition map back to the regular one.

The next composition obligation is equally concrete: attach another region
while matching transported electric flux, preserving the shared constraints,
and counting the shared edge's energy once. Then determine whether the
required interface remains manageable as the region grows. Static associative
joining is established; a uniform economical dynamical blocking law is open.

## Scaling and the larger physics ambition

Uniform positive electric and magnetic prefactors can be normalized once
through a derived clock/momentum transformation. All the separating states
remain separating under that transformation. Changing lattice resolution,
region shape or which cells have been combined is a stronger operation.
RELATIONAL_SCALING.md distinguishes these maps and proves the surviving
coarse-energy interval. Relational scaling is a productive requirement on
the construction, not an automatic guarantee that every requested scale
change preserves the same effective Hamiltonian.

This advances the concrete construction question: we have moved from an
interacting homogeneous sector to a spatial shared-edge effect, and obtained
an explicit regular dynamical repair. A continuum quantum mass-gap result
would additionally need a quantum construction and control of resolution
and volume limits. The present work establishes neither its existence nor
its absence. The useful work here is specifying what a larger construction
must retain and giving a case where that retention actually closes.

The proofs and exact finite checks are separate evidence. The checkers use
standard-library rational arithmetic, independent Pauli-matrix evaluations
where noted, full-link differentiation, gauge controls and a singular hostile
state. No numerical trajectory campaign, installation, publication or git
mutation was needed. SOURCES.md distinguishes the established literature
from formulas and witnesses derived in this task.
