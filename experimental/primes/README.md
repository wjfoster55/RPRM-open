# Prime families, huge descriptions and cheap questions

**EXPERIMENTAL — exact constructions and a conventional small reference are
provided. No new Mersenne prime, record-size primality certificate, novel
primality test or performance improvement is claimed.**

## The question worth testing

A huge number can have a small constructor. A receiver may also have few
answer classes. Can we build the adapter from the constructor to a useful
answer more cheaply than ordinary computation, while preserving the exact
question? The cost of obtaining the label matters as much as its size.

## What the pack contains

[Certified square-frontier expansion](square-frontier.md) gives a complete
written coverage and iteration proof: primes certified through B suffice
to classify integers through B^2, and the resulting complete list supports
the next stage. It includes the outside-boundary composite 49 and identifies
exactly what this mechanism contributes to the Fermat auxiliary argument.
This is established sieve reasoning presented through the RPRM contracts.
The document supplies a general theorem and pseudocode; the executable
reference below retains its separately stated small bounds.

[model.py](model.py) provides a conventional Lucas-Lehmer reference capped at
exponents 2 through 31, independent trial division within a declared bound,
exact digit access for a specified zero-run constructor, and the invertible
scale coordinate `e=3k+r`, `0<=r<3`. [check.py](check.py) compares the primality
answers and checks the constructor and scale coordinates.

```sh
python -I -B experimental/primes/check.py
```

The digit tool knows the exact word is `1` followed by N zeros. It does not
infer unsampled digits of an arbitrary word. The scale grade counts groups
of three decimal exponent steps; it is not a geometric dimension.

## The retained Mersenne lead

For `M=2^p−1`, the recurrence `s→s²−2 mod M` supports a zero-observation
receiver. A class can be described by the first time the orbit reaches zero,
or by never reaching zero. Once that class is known, the future readout is
simple. Computing the class of the starting state is the difficult part.

This is an application of the [future quotient](../../docs/operations.md).
It does not independently provide a cheap adapter into the quotient.
The small reference uses the established Lucas-Lehmer criterion; the proposed
research target is to find and justify a more useful adapter or composite
certificate, including its construction cost.

The large expression `2^150003647−1` is retained as an **unproved candidate
example**. The inspected local record contains no completed primality
certificate. It is outside the executable reference's bound. Merely having
a larger exponent than a known prime supplies no primality evidence.

For conventional discovery and verification context, consult the
[GIMPS known-prime list](https://www.mersenne.org/primes/) and
[GIMPS mathematics](https://www.mersenne.org/various/math.php).
Live assignment or candidate status is not supplied by this offline pack.

## Several labels can describe one dependent fact

A Mersenne integer is a base-two repunit and therefore a base-two palindrome.
Those are exact related descriptions, not three independent tests of primality.
The composite `2047=23·89` has all three structural descriptions.

Likewise, a Sophie Germain/safe-prime pair is the same certified relation
`q=2p+1` with both numbers prime, read in opposite directions. A classifier
whose definition already assumes primality cannot prove that premise.

The recovered research also retained failed modular predictors and a
collision method that lost to ordinary baselines on its finite test set.
Those are useful cautions for the next experiment; their historical counts
are not republished as fresh test receipts for this new implementation.

## Proposed experiment and rejection criteria

Freeze a candidate adapter, admissible exponents, known-prime controls,
composites with and without easy factors, and a cost accounting plan before
looking at results. Compare exact outputs with independent established tests.
Measure representation construction, large modular operations, memory and
verification, not merely the final class lookup.

Reject a claimed exact adapter on any admitted wrong answer. Reject a claimed
speed improvement when its full cost does not beat the declared baseline.
A post-hoc residue correlation is a new statistical candidate requiring a
fresh holdout; it is not a proof receiver. A meaningful positive result would
include a general preservation argument, independent counterexample search
and measured cost within the declared workload.
