# Certified square-frontier expansion

**ESTABLISHED MATHEMATICAL MECHANISM inside an experimental application pack.**
The coverage and iteration argument below uses classical factorization and
sieve reasoning. Its RPRM interpretation identifies the retained source,
the certified region, the new boundary and the exact observation preserved.
It supplies no new primality theorem, speedup or unrestricted Fermat proof.

## One complete list certifies a larger region

Supply an integer B>=2 and the complete certified list of primes at most B.
The requested observation is the prime/composite status of an integer c in
the interval 2<=c<=B^2, together with a factor when composite.

Every composite c has a factorization c=uv with 2<=u<=v, so u<=sqrt(c).
Some prime p dividing u therefore satisfies p<=sqrt(c)<=B. Completeness of
the supplied list guarantees that this divisor is available. Testing all
primes through sqrt(c) consequently decides every candidate in this region.

The ordering of the early tests matters:

```text
for p in the complete increasing prime list through B:
    if p*p > c: return PRIME
    if c is divisible by p: return COMPOSITE with factor p
return PRIME
```

The final return is justified by the same factor bound, even when no early
return occurs. Checking p*p>c first also prevents treating a prime as
composite merely because it divides itself. Perfect squares stay admitted.

Equivalently, mark each listed prime's multiples beginning at its square.
If m=pk<p^2 with k>=2, k<p has a smaller prime factor, so that multiple was
already covered by an earlier prime. Among integers above one in the stated
region, the unmarked values are precisely the primes.

## The continuation rule is proved for every finite stage

Classify the complete region through B^2 and retain the resulting complete
prime list. It now satisfies the input contract with B'=B^2. Reapply the
same theorem. Thus the recurrence is

```text
B_(k+1) = B_k^2, with a complete certified prime list through B_k.
```

The initial list supplies the base case. The factor theorem and complete
enumeration supply the induction step. Starting with any B_0>=2, these bounds
eventually exceed every fixed positive integer. Each stage still requires
finite computation and storage; the theorem does not make an uncomputed
list available or establish a performance advantage.

For example, the complete list through 5 is 2,3,5. It certifies all candidates
through 25, yielding the complete list

```text
2,3,5,7,11,13,17,19,23.
```

That list then certifies the region through 25^2=625. The values 5,25,625 are
instances of the relational rule, not universal numerical cutoffs.

## Failure outside the certified region remains visible

The original list 2,3,5 cannot classify arbitrary larger candidates just by
checking whether one of those primes divides them. The composite 49=7^2
escapes every original divisor. It lies outside the certified region through
25. The expanded list includes 7 and catches it in the next stage.

This is a failure of an insufficient prime list for the enlarged question.
It is not a failure of the square-frontier theorem. Completeness of the list,
the candidate bound and exact divisibility are all required premises. A
picture of repeated gaps or a selected collection of prime-like survivors
does not establish those premises by itself.

## The precise contribution to the Fermat argument

This mechanism can certify the primes used in the
[auxiliary-prime argument](../../docs/fermat.md#auxiliary-primes-the-precise-first-case-theorem).
That is a concrete mathematical dependency. The
[frontier audit](../../checks/prime_frontier.py) reconstructs complete prime
lists along `5 -> 25 -> 625 -> 390625`, verifies them through independent
integer-divisor enumeration, and checks that every bundled auxiliary p and q
belongs to the resulting list. The original Fermat checker retains its own
ordinary trial division, and the audit also reruns its residue obligations.

For an odd prime exponent p and a distinct auxiliary prime q, that argument additionally
requires the complete nonzero pth-power residue set R modulo q, with
R intersect (1-R) empty and p modulo q outside R. Certifying that p and q
are prime does not establish these two residue conditions. The release
checks them separately for its 302 listed pairs.

Those premises exclude the first case, in which p divides none of the three
roots. A uniform completion would also need appropriate coverage for every
remaining exponent and an exclusion for the remaining case where p divides
a root. Prime-list expansion supplies certified arithmetic ingredients;
the application must prove the specific property that rules out its target.

The general reuse principle illustrated here is exact: retain a complete
certificate for the current question, prove that one stage supplies the
next stage's premises, and invoke induction on that same property. For
primes the property is complete prime/composite classification. A Fermat
continuation needs a corresponding zero-exclusion invariant.

## Reproduce the finite enclosure

Run from the repository root:

```sh
python -I -B checks/prime_frontier.py
```

The [producer](square_frontier.py) and the checker are separate implementations.
The checker uses the generic [proof-donut APIs](../../docs/proof-donut.md#a-prime-region-certificate)
for complete classification relations and the
actual stage path. A classification comparison includes every integer in the
declared region; a prime count alone would not identify an omitted or
substituted value. Returned composite factors are checked separately.

Corrupted lists, boundary errors, false prime verdicts and invalid stage
transitions are retained as rejection controls. The finite receipt states
what was computed. It does not stand in for the general induction proof.
