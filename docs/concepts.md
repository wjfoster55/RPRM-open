# Reading the same object through different questions

**Status: mathematical definitions and worked examples where stated;
cross-domain applications remain interpretations until their bridges are supplied.**

This chapter explains the conceptual work between a formal definition and a
useful application. The idea is to make a change of question explicit enough
that it can be used, checked and challenged. Several descriptions can be true
of one object while answering different questions about it.

The expanded treatment is [Chapter II.6 of the book](../MANIFESTO.md#ii6-operational-coordinates-and-conceptual-models).
This reference keeps the short number-description, parity, learning and
paired-string examples. The [reader's guide](../LAYPERSON_GUIDE.md) supplies
a gentler entry point, and the [agent handbook](../AGENT_HANDBOOK.md) gives
a reusable reasoning procedure.

## Structure and meaning

RPRM does not assign intrinsic significance, purpose or intention to a number,
pattern or physical relation. A formal model supplies definitions and a context
for interpreting its symbols. Preserving that interpretation does not decide
what an event means to a person or community. Personal, cultural and existential
meaning lie outside what the core mathematics determines. Studying a specified
interpretation requires its own assumptions and evidence; broader philosophical
questions remain open. The [opening account in the book](../MANIFESTO.md#7-the-relational-layer-proposal-and-limits-of-observation)
states this boundary alongside the relational-layer proposal.

## Value, written form, address and operation

Take 1000. As an integer it is one thousand. As a base-ten numeral it has four
positions: a leading 1 and three zeros. As a power it is `10^3`. As a process
from 1, it can be reached by three multiplications by ten. Each is precise.

The digit string has a position carrier, the integer has arithmetic structure,
the power has a base and exponent, and the process has ordered intermediate
states. Switching descriptions becomes useful when a question needs one of
those structures. It becomes misleading if information from one description
is silently assigned to another.

For example, `0001000` and `1000` denote the same integer in base ten. They
have different lengths and different first positions. Parsing the string
as an integer preserves arithmetic value and forgets leading-zero metadata.
To reconstruct the string, retain a width or a complete formatting rule.

“Three-dimensional” needs another definition. A vector space with three
independent coordinates, a three-dimensional manifold, a three-stage operation,
and three zero symbols have different structures. An operational grade can be
defined for the multiplication path; a geometric interpretation requires an
additional carrier and a proved map. The numeral observation is useful without
silently making that geometric claim.

## A huge object can have a small exact description

Consider the word consisting of `1`, followed by N zeros. Its length is N+1,
its first digit is 1, and every later admitted digit is 0. These answers follow
for any natural N from the constructor. There is no need to materialize all
the digits to answer those questions.

The guarantee is conditional on that constructor. If all we know is that an
arbitrary word has the same length and two matching sampled digits, its other
positions remain undetermined. A shortcut for one supplied grammar is not a
shortcut for all strings with similar visible samples.

The same distinction matters for a Mersenne expression `M_p=2^p−1`. One
parameter determines an enormous integer. That is an exact representation
fact. Primality asks another question. Prime p is necessary but insufficient:
`M_11=2047=23·89`. A compact final answer label can still be expensive to compute.

Representations also carry operational paths. The succession
`1→10→100→1000` has the same endpoint as multiplication by 1000, but a receiver
counting transitions distinguishes them. Replacing the succession by the macro
is exact for the endpoint and insufficient for the full trace unless the
micro-path remains recoverable.

## Three supplied roles and a fourth relation

There is a useful recurring **three-plus-one** arrangement: three supplied
roles constrain a fourth. The number of roles alone does not supply the law.

For four bits constrained by

`b1 XOR b2 XOR b3 XOR b4 = 0`,

any three determine the fourth. This is true for every assignment of those
three bits: XOR with the known bits cancels them and leaves the missing one.
The law supplies the exact adapter between the three-bit input and the four-bit
codeword. All eight legal codewords can also be enumerated independently.

The arrangement supports different requests with different answers:

| Request | What the parity law provides |
|---|---|
| One labeled position erased | Recover that bit uniquely. |
| All positions retained, one bit changed | Detect inconsistency. |
| One changed position unknown | The nonzero syndrome alone cannot identify it. |
| All four agree with a different legal codeword | Internal checks accept that other codeword. |
| Recover the true external message | Need a source/error model in addition to internal consistency. |

This example explains why “three views and one completion” is a productive
construction while “any three things determine a fourth” is not a theorem.
The relation, role labels, admission and receiver do the work.

## Truth-tellers, errors and shared sources

Suppose four reports concern the same binary proposition. Under the supplied
assumption that at most one report is incorrect, a three-to-one split identifies
the correct answer by majority. The conclusion follows from the error bound:
at least three reports are correct, so a value with only one report cannot be
the truth under that premise.

Remove that premise and three agreeing reports establish only agreement.
They may share an input, copied computation or hidden assumption. A fourth
disagreeing report is not automatically the liar. Likewise, three consistent
coordinate transformations of a wrong input can all be internally correct
transformations and still describe the wrong source.

This is not an argument against multiple checks. It explains how to make
them useful: name what each independently constrains, what inputs and
assumptions they share, and what error model the conclusion needs. Use a
hostile shared-source error as well as isolated single-channel errors.

The “liar” is a role in this finite model. It is not a psychological diagnosis
or a method for identifying dishonest people from numerical patterns.

## Teachers, questions and abduction

A teacher example can make an inverse problem concrete. Let the admitted
hypotheses be four functions on `{0,1}`: constant zero, constant one, identity,
and bit complement. Asking for the output at 0 divides them into two pairs.
Asking for the output at 1 then distinguishes each remaining pair.

The learner's state is the set of functions compatible with the answers.
Question selection chooses an operation on that uncertainty. Under this
finite grammar and truthful answers, two queries identify the supplied
function. One query cannot identify all four because it has only two possible
answers. The lower bound and the construction match.

If the actual teacher uses a function outside the supplied grammar, the
learner may reach an empty fiber or make an unjustified identification.
If answers can be noisy, retain an explicit noise model or error budget.
If queries cost different amounts, minimum query count and minimum total
cost become different optimization questions.

This separates two complementary activities:

- **Deduction:** derive consequences within a supplied law and hypothesis.
- **Abduction:** form and compare candidate explanations for observations.

Abduction can propose a new carrier or relation when the old grammar fails.
That proposal does not inherit proof status from the deductions made inside
the old grammar. Freeze candidate and evaluation rules, then test the proposed
bridge, its coverage and its cost. A useful next question is an operation;
an appealing explanation is a candidate until its obligations are met.

## Paired strands and order

Let an alphabet be `{A,T,C,G}` with the involution exchanging A with T and
C with G. Complement acts on each symbol; reversal changes positional order.
Their composition is reverse complement. Applying it twice restores the
original string because each operation is an involution and they commute.

The named alphabet gives a familiar way to picture paired information and
opposite orientation. The mathematical statement is about strings under a
declared symbol rule. A biological use requires specifying which molecular
objects, orientation convention and observation the strings represent.
String compatibility alone does not determine molecular geometry, energetics,
folding dynamics or biological function.

One can also define an actual pair of geometric helices,
`h0(t)=(r cos(t),r sin(t),ct)` and
`h1(t)=(r cos(t+π),r sin(t+π),ct)`, for fixed r>0 and c≠0.
Their shapes are not derived from having two symbol strings. Mapping positions
or symbols to the helix parameters is additional structure. A helix drawing
can explain order and paired tracks while its caption preserves that boundary.

## What travels between domains

The transferable principle is often a question rather than an answer:

- Which observation is constant on the fibers of this representation?
- Which continuation distinguishes states that look equal now?
- Which missing role has a unique completion under the supplied law?
- What source or correlation disappeared when a simpler picture was made?
- What extra measurement would repair the failed question at the lowest cost?

These questions apply wherever suitable carriers and maps can be supplied.
A cross-domain example becomes a theorem only after the relevant bridge is
proved. Experimental packs keep useful proposed bridges available together
with tests, baselines, failure criteria and their current evidence. The main
paper can state that route without pretending to enumerate every application.
