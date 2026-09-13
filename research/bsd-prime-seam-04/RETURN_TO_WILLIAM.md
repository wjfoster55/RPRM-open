# A real multiplier connection between prime paths

We found an exact connection. On the current curve, the local factor at 5
is(4−3i)/5, and the factor at 13 is obtained by multiplying it by
(12+5i)/13:

\[
\boxed{\frac{4-3i}{5}\;\frac{12+5i}{13}
       =\frac{63-16i}{65}.}
\]

Here i²=−1. The 3–4–5 and5–12–13 triangles come directly from the
curve's formula. The connection exists because a Frobenius-minus-one
factor at 13 contains a Gaussian prime above 5. We verified that shared
factor exactly, along with the actual order-five points after reduction
at 13. The detailed derivation is in `PRIME_SEAM_PROOF.md`.

The search also found the direction information you have been emphasizing.
Prime 29 removes the common5-factor by multiplying by C5; prime 37 removes
it by dividing by C5. Keeping just the shared prime loses that distinction.
Keeping a sum and signed difference recovers both underlying branch
valuations exactly. That is a concrete operational relation we can use.

Lucky numbers were included in a fresh bounded search. Lucky membership
does not determine this direction: lucky 13 and lucky 613 have opposite
local 5 exponents. The exact arithmetic branches supply the missing data.

The remaining obstacle is the **overall scale connecting the analytic
coefficient to the arithmetic regulator**. Our new identities determine
local relative factors. We proved that relative path agreement can
survive a common rescaling, so it cannot select that overall scale by
itself. An independently normalized analytic coefficient is the next
quantity that can distinguish the possibilities; its calculation and
exact comparison remain OPEN.

All three fresh stages completed, including 166 independent readback
checks. The scout covered79 good ordinary primes through 1000. Runnable
source, full outputs, theorem conditions and the failed implications are
included. This experiment establishes no new primary part of Sha and
does not close the full or general BSD identity.
