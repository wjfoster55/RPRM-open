# Injectivity fails iff the three checks are a line

Written, 17 September 2026. This is **not** a new finite campaign. HT-28
already listed the seven failures. The requested iff is immediate from
THEORY P4 plus one fact about `F₂³`. Do not pad it.

## Carrier

Same as HT-28: source `V = F₂³`, checks the seven nonzero linear
functionals, panels the 35 triples of distinct checks. Hostile panel
`{1,2,3}`.

## Written lemma

**P4 (already written).** A panel with rank `r` has nonempty fibers of
size `2^{3-r}`. So the joint readout is injective iff `r = 3`.

**Line fact.** Let `a,b,c` be three distinct nonzero vectors in `F₂³`.
The following are equivalent:

1. `{a,b,c}` is linearly dependent (rank `< 3`);
2. rank equals 2;
3. `{a,b,c} = {a,b,a⊕b}`.

Proof. Rank 0 is empty. Rank 1 has a single nonzero vector, so it cannot
contain three distinct nonzero labels. Thus dependence means rank 2. A
2-dimensional subspace has exactly three nonzero vectors, and for any
two of them the third is their sum. Conversely `{a,b,a⊕b}` has rank 2
when `a,b` are distinct and nonzero (then `a⊕b` is the other nonzero in
their span).

**Corollary.** A 3-check panel fails injectivity iff its labels are
linearly dependent iff they are a line `{a,b,a⊕b}`.

That is P5's first sentence. The census ONE(28) is the *count* of
independent triples, not a separate reason the iff holds.

## Exact check

`verify_ht28.py` already enumerates all 35 triples and checks
injectivity, rank, and equality of the failing set with
`{{a,b,a⊕b}}`. The replay after this note adds the two biconditionals
on every triple, including hostile `{1,2,3}`:

```text
injective  ⇔  rank == 3
dependent  ⇔  panel == {a, b, a⊕b}
```

No new carrier. No SAT. No Hamming-8.

## Next claim

Because this lemma is immediate, the next recovered-concepts cut on this
branch is the **7/8 type split**: seven teacher answers, eight simplex
words, Hamming-8 positions, and free-toggle source eight are different
objects. Nulls for that cut are frozen in [NULL-78.md](NULL-78.md)
before its enumerator runs.
