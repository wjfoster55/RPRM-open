# The carry/swap route: what would make it a mathematical bridge

This note retains William's proposed ordered trace

    (0,1) -> (2,1) -> (3,4) -> (6,4)

and the earlier description of carry, reversal and signs. It does not assign
a general recurrence, interpret `--0`, or identify an ordered pair with its
scalar ratio. The full operation remains OPEN. The previous exact partial
trace and equation-changing examples are in
[COORDINATE_NOTE.md](../bsd-e5-completion/COORDINATE_NOTE.md).

The following are *proposed requirements for an adapter*, not claims that
William's operation already satisfies them.

## A concrete reconstruction bridge to test

For a stated class of curves E/Q, supply the curve parameters and define
states S_(E,n) with all required carry and phase fields. Supply an exact map
rho_(E,n) from reached states to E(Q)/M_n E(Q), with M_n dividing M_(n+1).
Every quotient must be a quotient of the same curve's group. A switch of
Weierstrass equation requires the proved curve isomorphism too.

1. State the transition and its enabledness. Prove that reducing the decoded
   next state agrees with decoding the preceding state. If a reverse has
   several preimages, retain the full fiber or an explicitly selected branch.
2. Supply rational realization of the decoded finite-level classes. A
   locally soluble Selmer class is not automatically such a realization;
   its image in Sha is the exact obstruction.
3. For a proposed common source point, produce one independently justified
   finite bound B on rational representative height at **every level**.
   The bound must cover source height, including rational denominators.
   Small register labels or bounded digits do not imply this without a
   proved estimate relating them to source height.

If these requirements hold, Proposition 1 of RECONSTRUCTION.md proves a
common rational point exists. The full fiber is the point plus
intersection M_n E(Q). Factorial moduli give uniqueness; one-prime moduli
retain prime-to-that-prime torsion ambiguity. This is an actual implication
with an explicit inverse/fiber, not a claim of efficiency or a completed
general operation.

Two distinguishing tests must remain in view. The inverse-of-three binary
tower has every finite rational realization but no common rational point.
The tower represented by (2^n+1)P does have the common point P despite those
particular representatives growing. A proposed height rule must reject the
first and accept the second for the correct reason.

## What would additionally be needed for BSD

The reconstruction bridge concerns rational points. To become an argument
for rank equality, another proved relation must connect their independent
directions to the completed L-function coefficients in ANALYTIC_BRIDGE.md.
Transporting group addition or replacing a generator label by (0,1) does not
yet supply that relation. For the full formula, the adapter must also retain
Sha, a saturated basis and its height pairing, the minimal period, local
factors and torsion normalization. General Sha is not assumed to vanish.

No historical source was reopened to fill in the missing recurrence. These
requirements tell us what evidence would advance this specific route while
the general Selmer and analytic work can proceed independently of its syntax.
