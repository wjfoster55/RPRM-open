# A reader's guide to RPRM

RPRM means **Relational Pressure Retention Model**. The name comes from the
physics idea that motivated the work: observable behavior may arise from
underlying relations, with pressure and retention involved in their change
and persistence. The name is retained; the science sections explain the
proposal and what remains to establish it.

RPRM asks a practical question: **what do we need to keep in order to answer
the question we actually care about?** It uses mathematics to make that
question precise, especially when we change how a problem is represented.

The main work is called *The RPRM Manifesto*. Its purpose is mathematical
unification: connect useful descriptions and methods while preserving their
meaning. The title names a statement of the program and its methods. Each
mathematical result still needs its own assumptions and proof.

You do not need to learn the vocabulary before understanding the starting
examples. This guide introduces the terms as they become useful. It gives
the core argument in one place; the repository supplies the detailed proofs,
code, glossary and experimental leads.

## The same rule can answer different questions

Imagine a receipt recording a price, a delivery charge and a total. The rule
is `price + delivery = total`. If you know the first two amounts, you can find
the total. If you know the total and delivery charge, you can find the price.
If you know only the total, several pairs may fit.

RPRM calls the choice of what is supplied and what is requested an
**aperture**. The arithmetic has not changed. The open question has.

The set of all compatible answers is the **fiber**. No answer, one answer
and several answers are different outcomes. So is “we have not finished
checking.” An unfinished search does not establish that no solution exists.

The permitted amounts matter too. If refunds or negative adjustments are
excluded, an answer requiring one is outside the admitted model. The word
**carrier** names the objects and values allowed in the problem. It includes
the assumptions needed to decide what counts as an answer.

## A good summary depends on its purpose

A map showing railway connections may be excellent for choosing a route
while being poor for measuring a walk across the city. It keeps some facts
and simplifies others. Neither purpose can be evaluated from the drawing's
appearance alone.

RPRM calls the questions that must survive a **receiver**. A summary is exact
for a receiver when every original situation that it merges has the same
answer to those questions. If merged situations need different answers,
the summary has lost a necessary distinction.

This gives a precise rule for simplification. It does not demand that every
representation keep everything. It demands that the retained information
be enough for the stated use—and that a change of use reopens the question.

## Looking the same now is not enough

Imagine two machines showing the same green light. One will stop when you
press its button; the other will continue. A summary containing only the
light's current color cannot predict what happens next.

To support continued operation, a summary must preserve which actions are
available and how their results are represented. If those conditions hold
at every admitted state, mathematics can prove the summary continues to
work for every finite sequence of actions in that model.

That is one of the framework's central results. The finite tools can check
the conditions, find a sequence exposing a bad merge, and split the summary
until the necessary distinctions are retained.

## One number has several descriptions

The integer 1000 can be written as `10^3`, as a decimal string with four
positions, or as the result of multiplying 1 by ten three times. Those
descriptions answer different questions: amount, scale, written length,
or a path of operations.

Recognizing several descriptions is useful. Treating their features as
interchangeable is not. Three zero symbols do not by themselves establish
a three-dimensional geometric space. A geometric application needs its own
coordinates and a map showing what is preserved.

Large numbers make this especially clear. “One followed by a million zeros”
describes a very long numeral exactly. You can answer many digit questions
without writing it out. But that does not make every question about every
equally long number easy. A compact expression and a cheap computation are
different achievements.

## Three pieces can recover a fourth—under a law

Suppose four switches are required to contain an even number of ones. If
three positions are known, the fourth is forced. Three known pieces plus
the parity rule are enough.

Now suppose all four values are reported but one unknown position is wrong.
The parity check can reveal that something is inconsistent. It cannot tell
you which switch was wrong. Recovering a missing value and correcting an
unknown error are different tasks.

The same care applies to agreement. Three reports can all agree because
they copied the same mistaken source. Agreement is useful evidence only
with a stated reason that those reports constrain the truth independently
or satisfy a known error bound. Internal consistency alone is not external
authenticity.

## What an unseen part can tell us

Suppose a table records the possible pairs (0,0) and (1,1). You have not
learned which pair is present, but you already know the two values are equal.
The whole situation is uncertain while that one question is settled.

Now list the possible first values separately from the possible second
values. Each list contains 0 and 1. If you combine the lists freely, you
accidentally admit (0,1) and (1,0). A summary has lost the relationship that
made the equality answer certain. Keeping the possibilities together is
what the book means by keeping a **joint fiber**.

The four observation lanes use the same principle. Each lane supplies a
specified view of one source. Keep the views together, and every new
observation can rule out incompatible possibilities. An unvisited value is
known when at least one possibility remains and every remaining possibility
gives it the same value. If none remain, the model and observations conflict.
The law connecting the views does the work.

The paper gives a geometric example on a square. Restrict the surface to a
formula that is linear in either coordinate when the other is fixed. Its
four corner heights determine the surface throughout that square; the center
is their average. If the corners are all above zero, the surface is above
zero everywhere inside the square and on its boundary. Allow a more general
surface, however, and a depression can hide between the same corners. The example includes both constructions. That makes the boundary
of the inference visible, instead of asking readers to trust the picture.

## How the proof donut helps

The proof donut is a way of organizing the checks around an open question.
What objects are admitted? Have all possibilities been covered? Do the
different views preserve the same shared information? Does the reasoning
continue under the allowed operations? Does it answer the original question?

Its finite software checks supplied tables and certificates. A separate
implementation can check the same example, helping expose bugs. The tool
does not prove itself correct simply by printing PASS, and its results do
not establish an unstated connection to a physical system.

This is also how a negative result stays useful. A failed check can identify
the exact missing distinction, incorrect map or unsupported assumption.
That gives the next attempt something concrete to repair.

## How a finite argument reaches farther

A finite calculation can contribute to an unlimited statement when a proof
explains why it covers the rest. Think of a rule for climbing a ladder:
show how to reach its first rung, and show that being on any admitted rung
lets you reach the next. The argument is about every step allowed by the
rule, even though an actual climb uses only finitely many steps.

The prime chapter gives an arithmetic version. If you know every prime up
to seven, those primes can mark every composite number through forty-nine.
Why? Every composite in that interval has a prime factor no larger than
seven. Forty-nine is caught by seven times seven. Repeating the proved
construction extends the certified region. The useful result is the
coverage argument and its repeatable rule.

For a longer optional example, the [independent Fermat study](docs/fermat-study.md)
proves that a^n+b^n=c^n has no positive integer solution when the integer
exponent exceeds two and the smaller of a,b is at most 4000. The other
input and exponent have no separate assumed cap. The independent argument
does not yet cover all larger inputs. The established Fermat theorem is
credited separately; using its proof would not finish this independent study.

## Looking carefully at the science examples

The idea motivating these chapters is that what we observe may be the
visible behavior of an underlying organization of relations. That is the
**relational-layer proposal**. The word “underlying” means that this
organization would explain the behavior; it does not mean an extra place
underneath space.

The mathematics explains how a description can be sufficient for every
question it is meant to answer while leaving details of its source hidden.
Suppose a display alternates between zero and one. One model has only that
display state. Another has the same display plus an unseen bit that also
flips. Watching the display forever cannot choose between those two models
under their stated rules. A new interaction that copies the unseen bit to
the display could distinguish them. The original observations therefore
establish neither that the extra bit exists nor that it could never be
observed.

That is the role of abduction here: propose possible relational sources,
work out their consequences and ask what the evidence actually distinguishes.
Several explanations may remain, even when they agree on something useful.
The [relational-layer guide](docs/relational-layer.md) develops this example
and connects it to gravity and black holes.

The physical chapters begin with stated scientific models and ask which
representations keep their predictions. That produces mathematical results
within those models. A further proposal about how nature works needs its
own connection to measurements.

For gravity, attraction tells us how velocity changes. It does not require
an object to be moving inward at that instant. A circular orbit is a useful
control: gravity points toward the center while the instantaneous motion
points along the orbit. An object moving outward can also slow under
attraction. Keeping position, velocity and the force law makes the question
precise. Calling all three situations simply 'drift toward something' would
lose distinctions the model needs.

The two-path example gives another kind of useful reduction. For a stated
family of interference measurements, two real numbers retain the entire
phase pattern. The chapter derives why that is enough, and shows an
operation after which it is no longer enough. It also keeps selected
outcomes together with their frequencies. If two equally likely selected
groups have plus-output rates 90% and 10%, their combined rate is 50%.
Showing only the first group would answer a different question.

The black-hole chapter separates a mathematical return process from a
specified spacetime model. Connecting them physically remains a research
question. Likewise, carrying from one numeral position to the next is an
exact arithmetic operation, but its threshold changes with the numeral
base. To identify it with a cosmic event, we would need an explanation of
which physical quantity changes and what predicts that change.

The research section applies the same care to information lost in molecular
and other models. Two source states can share a label while having different
next-step probabilities. A smaller model must preserve those probabilities
if it is meant to predict the future. A demonstrated failure of that kind
can identify useful information to retain. Whether retaining it improves a
real scientific prediction is a further experiment.

These examples are meant to be useful even when a proposed extension fails.
The book supplies exact successes, explicit counterexamples and open tests.
The broader ambition is pursued through those individual results.

## What is established, and what is proposed

The repository contains several kinds of work:

| Kind | What it means |
|---|---|
| Definition | An explicit convention or construction. |
| Written proof | An argument that a statement follows from stated premises. |
| Formal proof | A precisely encoded declaration checked by a proof system under its stated foundations. |
| Finite test | A computation checking specified cases. |
| Experimental lead | A proposed use, with a test and an unresolved outcome or bridge. |
| Interpretation | A way of understanding or applying a model that needs further justification to become a factual claim. |

The core establishes specific preservation and reconstruction results. An
experimental protein, ray-tracing, music or psychology example must earn its
own application claim. It can be worth sharing before that claim is proved,
provided readers receive enough detail to test it and see what remains open.

The same distinction applies to origins. A mathematical model can specify
a starting state and show what follows from its rules. That alone does not
explain how the physical universe began. The framework helps expose the
starting assumptions and the observations that could distinguish models.

## Where to go next

Read Part I of the main paper for the opening argument and the later chapters
for full proofs, applications and research questions. Use the [conceptual chapter](docs/concepts.md)
for a fuller bridge between the examples and the mathematics, and the
[core definitions](docs/core.md) for exact contracts. The [agent handbook](AGENT_HANDBOOK.md)
is self-contained for agents and technically curious readers. [Verification](docs/verification.md)
shows how to run the code and exactly what the checks cover.

The material is free to reuse and fork under its stated licenses. Its value
can be tested one concrete question at a time, without adopting every proposed
application or treating the framework's ambition as an already proved result.
