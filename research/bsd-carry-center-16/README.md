# Atoms, zero/one, and retained turns: experiment 16

The current proposal led to an exact connection between the preceding
hinge operation and an existing RPRM digit map. It also gives a concrete
conditional route from a circle-closing condition to the desired BSD
equality. The word connection is proved; the circle condition for the
actual BSD quantities remains an open premise.

The user's clarification is retained: the meaning of `0/1` depends on
context. None of the interpretations below is declared the uniquely
intended meaning.

## The direct 59 / 01 connection

The operational-number translator already has the involution

```
P = (0 5)(1 9)(2 8)(4 6), with 3 and 7 fixed.
```

Its action changes labels reversibly; it is not ordinary scalar equality.
In particular `P(5)=0`, `P(9)=1`, and applying P twice recovers the source.
For ordered decimal words it acts on each digit, with leading zeros kept:

| Source | P-labelled view |
|---|---|
| `59` | `01` |
| `95` | `10` |
| `595` | `010` |
| `55` | `00` |

Let F be experiment 15's maximal reverse-overlap operation: take a
two-digit word, reverse it, and join the copies using the longest equal
suffix/prefix, admitting full overlap. We now have the commuting square:

```
59  --F--> 595
 | P        | P
 v          v
01  --F--> 010
```

**Proof.** A bijective symbol permutation preserves every equality and
inequality between symbols. Thus every candidate overlap length matches
before applying P exactly when it matches afterwards. It also commutes
with reversing positions. The maximal length and the resulting joined
word are therefore preserved: `P(F(w))=F(P(w))`. This is a written proof,
supported by fresh checks of all 100 two-digit words in
[p-hinge.json](evidence/p-hinge.json).

The supplied port is the exact word; the requested receiver is the joined
word and retained source. The operations are total on their declared
carriers, P is its own inverse, and the first two characters recover the
source from F(w). There is one source over every attained target and none
over unattained targets in the two-/three-digit output carrier. This does
not make every possible 0/1 interpretation equivalent.

In the typed record `59 | 2 | 595`, the middle field is experiment 15's
chosen two-view opcode. Relabelling the two payload fields yields
`01 | 2 | 010`. Relabelling every digit indiscriminately instead gives
`018010`, because `P(2)=8`. The role of the opcode must be retained.
Neither serialization has been established as the process that generated
the earlier BSD interval endpoint 592595.

Injectivity matters. A hostile symbol map h collapsing both 0 and 1 to
0 gives `h(F(01))=000`, while `F(h(01))=00`. Thus the commuting law is
not licensed for arbitrary information-losing relabellings.

## Five as zero, and nine as a carry boundary

There is also an independent recovered centered-zero construction.
The [local recovery note](../../recovered-concepts/ZERO-AND-RAILS.md)
records this oriented source rail:

| Raw source x | Centered coordinate z=5-x | Normalized coordinate (6-x)/2 |
|---:|---:|---:|
| 6 | -1 | 0 |
| 5 | 0 | 1/2 |
| 4 | +1 | 1 |

That is an exact contextual sense in which five is zero. It is distinct
from the P permutation above. Explicitly extending z to the decimal
digit carrier sends 9 to -4, so it keeps 5 and 9 different. Indeed
`z(a)-z(b)=-(a-b)`, with inverse `x=5-z`. Choosing a separate origin for
each value can display both as zero, but the two origins retain the
original difference. Discarding them loses the equality question.

One candidate meaning of `0|1` is the ordered record
`(current digit=0, completed row=1)`. In the bounded decimal model,

```
value(d,q) = 10q+d
(9,0) --increment--> (0,1)
value(0,1) = 10
```

The fraction `0/1` instead has rational value zero. An endpoint pair
`(0,1)` is a third type. The slash glyph alone selects no adapter.

For d,q in {0,...,9}, the full pair reconstructs every value 0 through
99 uniquely. Every displayed digit alone has ten possible row sources.
There are 99 admitted successor steps. At 99 a further step requires an
explicit larger carrier. Forgetting q also loses enabledness: digit 9
at row 8 has a successor in this carrier, but digit 9 at row 9 does not.
All of these claims were checked in [carry-center.json](evidence/carry-center.json).

The original increment must change when digit labels change. Under P,
the same physical state transition becomes `(1,0)->(5,1)`, decoded by
`10q+P(d)`. It is not ordinary increment on the renamed digit. Likewise,
P turns the word `59` into `01`, but preserves the original rational
readout only through `P_inverse(0)/P_inverse(1)=5/9`. Evaluating the new
word as the fraction zero discards that transported question.

Adding the ordinary fraction 0/1 to both A and B leaves `A-B` unchanged.
Adding the same +1 also leaves it unchanged. These were tested on every
ordered decimal pair. Neither common addition supplies a zero-discrepancy
proof.

## What the atom comparison contributes

In the familiar atom icon, the central cluster represents the nucleus
and the surrounding marks represent electrons. Modern orbitals describe
wavefunctions and position probabilities, rather than fixed planetary
paths. [DOE, Quantum Mechanics](https://www.energy.gov/science/doe-explainsquantum-mechanics);
[NIST, atomic wavefunctions](https://www.nist.gov/news-events/news/2019/05/jqi-researchers-shed-new-light-atomic-wave-function).

A useful mathematical question is what a probability-density picture
leaves out. The [independent atom/phase note](agents/ATOM_PHASE.md) proves
that the five circle waves `exp(i*n*theta)`, n=-2,-1,0,1,2, all have
density one, while their winding counts are n and their dimensionless
derivative energies are n squared. Same density does not imply same
state or energy. This toy circle model is not a model of an atom or BSD.

On the corresponding Fourier span, orthogonality gives
`norm_squared=sum |c_n|^2` and `energy=sum n^2 |c_n|^2`.
Removing the constant component gives `energy >= norm_squared`.
Merely requiring a nonconstant wave does not: `1+epsilon*exp(i*theta)`
has energy/norm ratio `epsilon^2/(1+epsilon^2)`, arbitrarily close to zero.
The finite tests cover all 243 coefficient vectors in {-1,0,1}^5;
the written proof, not the finite sample, establishes the stated formula
on the whole declared Fourier span.

The transferable lesson is specific: retaining position and accumulated
turns can preserve information that a repeated endpoint or density
picture forgets. No map identifying an atom, a keyring, and the two BSD
measurements has been supplied.

## A precise conditional closing relation for BSD

Keep the earlier normalization for E34, `y^2=x^3-1156x`:

```
A  = L''(E,1)/2
B1 = Omega_all * Reg_full
Q  = A/B1
K  = Q-1
```

B1 is the candidate Sha-order-one arithmetic quantity; establishing
the actual finite order of Sha remains a separate obligation. The
attributed intervals from experiment 05 give the exact bound

```
-253697/3192812712 <= K <= 118519/1276918651
```

which lies strictly between -1/2 and +1/2.

Define `f(theta)=exp(i*K*theta)` on the interval [0,2*pi]. If a proof
from the actual BSD constructions establishes that f descends to an
ordinary single-valued circle function, then

```
f(2*pi)=f(0)
  iff exp(2*pi*i*K)=1
  iff K is an integer.
```

The only integer in the known K interval is zero. Thus this additional
premise would prove `K=0`, `Q=1`, and `A=B1`. This conditional implication
is proved. Its periodicity premise for actual BSD is OPEN. Defining the
exponential on an interval does not establish endpoint compatibility.
This is the earlier missing integrality condition written as a phase
closure; it does not bypass that condition.

For a hostile control, the admissible hypothetical pair
`A=6.38515`, `B1=6.38505` gives `K=2/127701`, which is nonzero and not an
integer. It fails the ordinary periodicity condition, although it fits
both numerical intervals. These are abstract values consistent with the
interval premises, not alternative actual BSD values.

The boundary law itself matters. With twist t measured in turns,
`f(theta+2*pi)=exp(2*pi*i*t)f(theta)` instead requires `K-t` to be an
integer. `K=t=1/100000` passes that altered condition within the same
small interval. A twisted condition cannot be silently substituted for
the ordinary one. [Fresh phase checks](evidence/phase-bridge.json) retain
both controls and the exact rational interval arithmetic.

The related stopping law is equally explicit: if `D/delta` is an integer,
delta>0 and `|D|<delta`, then D=0. Our D1 bounds lie inside (-0.001,0.001),
but no 0.001 lattice for actual D1 has been established. The interval
still admits D1=0.0001. On a 0.0001 grid it admits eleven different values,
so choosing a finer grid does not automatically solve the equality.
Refining the decimal representation of 0.0001 preserves its nonzero
value. The example step size is illustrative, not a discovered BSD unit.

## Replay and scope

Run with Python 3 and its standard library from this directory, choosing
new evidence paths:

```powershell
python -I -B .\work\check_carry_center.py --output .\replay\carry-center.json
python -I -B .\work\check_phase_bridge.py --output .\replay\phase-bridge.json
python -I -B .\work\check_p_hinge.py --output .\replay\p-hinge.json
python -I -B .\work\verify_bindings.py
```

The number scout runner additionally needs the local RPRMLexicon source
and prior translator receipt. Its [four full outputs](evidence/number-scouts.json)
are retained here. It compared all four source hashes to the existing
114-check receipt and reused that verification only because the bytes
were unchanged. Fresh scouting did not rerun the whole translator suite.
Syntax for `0/1` is explicitly ambiguous in that output; normalization to
the digit word `01` does not select its mathematical meaning.

Evidence grades: definitions, written proofs, exact finite tests, and
explicit conditional statements. No new analytic/height computation,
Sha determination, real BSD identity, or cross-problem physical theorem
is claimed. Previous packets and other research lanes remain unchanged.

An [independent review](agents/INDEPENDENT_REVIEW.md) checked the phase
condition, exact interval control, all 100 P/hinge rows and 99 conjugated
carry steps. The ZIP manifest verifies bytes only.
