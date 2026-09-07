# A reader's guide to RPRM

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

Read the main paper for the compact argument, the [conceptual chapter](docs/concepts.md)
for a fuller bridge between the examples and the mathematics, and the
[core definitions](docs/core.md) for exact contracts. The [agent handbook](AGENT_HANDBOOK.md)
is self-contained for agents and technically curious readers. [Verification](docs/verification.md)
shows how to run the code and exactly what the checks cover.

The material is free to reuse and fork under its stated licenses. Its value
can be tested one concrete question at a time, without adopting every proposed
application or treating the framework's ambition as an already proved result.
