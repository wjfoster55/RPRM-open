# What would establish the order of Sha here?

The user's follow-up asks what would establish “the order, Sha thing.”
The order is the number of elements of the group. To establish order 1
means to prove that only the zero element exists. This note states an
exact completion criterion; it does not claim to have discharged it.

## A direct arithmetic criterion, with no BSD assumption

For this E34, the completed arithmetic work gives

    G=E(Q)=Z² ⊕ (Z/2)²,     Sha(E/Q)[2]=0.

Here is a precise remaining condition equivalent to Sha(E/Q)=0:

    For EVERY odd prime p, the p-Selmer group has exactly p² elements.

The Selmer group is the finite group of descent classes satisfying the
local conditions at every place, including the real place. For the
standard multiplication-by-p descent, the relevant exact sequence is

    0 → G/pG → Sel_p(E/Q) → Sha(E/Q)[p] → 0.

Both this sequence and the fact that Sha is a torsion group are stated
in [Milne, Elliptic Curves, IV §2, equation (23), printed p.110](https://www.jmilne.org/math/Books/ectext6.pdf#page=118).

**Proof of the criterion.** For odd p, multiplication by p is an
automorphism of the four-element torsion group. Therefore
G/pG=(Z/p)² and has p² elements. Its injection into Sel_p accounts for
all classes exactly when Sel_p has p² elements; by exactness this is
equivalent to Sha[p]=0.

If the condition holds for every odd prime, the existing p=2 result
gives Sha[p]=0 for every prime. A nonzero element x of a torsion group
has some finite order n>1. For any prime p dividing n, (n/p)x has order
p, contradicting Sha[p]=0. Thus Sha=0, and its order is 1. This
argument does not require a prior assumption that the whole group is
finite. Conversely, Sha=0 makes each displayed exact sequence an
isomorphism and yields the claimed Selmer sizes.

The proof above is complete. The quantified input about EVERY odd p is
OPEN for E34 in this investigation. This separates a proved reduction
from the unsolved premise.

For example, a complete 3-descent proving |Sel_3|=9 would close only
the 3-primary part. No such new 3-descent is claimed here. The results
at 2 and 3 would still leave every other prime to cover. A way to make
the global task finite would be a theorem proving vanishing outside an
explicit finite exceptional set, followed by complete checks inside
that set. The hypotheses giving that uniform coverage must themselves
be proved. Checking many primes is not the same quantifier.

## A second route for this particular curve

An independently applicable theorem proving the exact full BSD identity
would identify the quotient in `FACTOR_COMPARISON.md` with the finite
order of Sha. Its rigorous enclosure

    [0.999920542, 1.000092816]

contains only the integer 1. With that theorem supplied, the order would
therefore be 1. Without it, the quotient is a real number in an interval
and is not proved integral. Using the conjectured identity as an
assumption while claiming to prove general BSD would be circular.

The direct arithmetic route would establish Sha=0 independently, but
would still leave the exact analytic identity c₂=Ω Reg to prove.
Even knowing all factors to tight intervals does not force equality
of real numbers.

## Where the user's directed operation could enter

A relevant new construction would need to start with an actual locally
soluble descent class and produce a rational point whose Kummer image
is that class. It must work for every class in the admitted domain,
respect the equations and equivalences, and specify exceptional cases.
If established for every odd prime, this would prove the surjectivity
G/pG→Sel_p required above. A coordinate re-expression alone does not
yet supply that construction. The midpoint/gap identities remain valid
within their stated recovery contract.

Evidence grade: a written deduction from the cited exact sequence,
torsion property and this experiment's proved group structure. No new
odd-prime calculation, total-Sha result or full-BSD promotion is made.
