# BSD operational donors for the YM joint-response seam

Read-only donor audit, 12 September 2026 (America/Denver). Initial source
hashes were sampled at approximately 2026-09-13 00:29 UTC while the
coordinator's inspection showed **Run BSD E5 test 01** active. The latest
compact task wait subsequently reported that task completed. Section 7
records its newly available column-handoff result, read at approximately
00:45 UTC. Task completion is an attributed workflow status; full BSD
and the exact comparison remain OPEN. This audit reads source artifacts
without rerunning BSD programs, messaging that task, or changing its
files. Later source changes require a new attributed snapshot.

The useful transfer is already concrete: retain the relation that changes
under the next operation while reusing the part proved invariant. In the
current YM example, separate plaquette traces retain today's values but
lose their shared-edge response. BSD supplies both a working invariant/fiber
split and a separating mixed-operation example. The equations below define
the adapters; equality of displayed numerals does not perform the transfer.

## 1. Preserve what “operational value” meant

[OPERATIONAL_VALUE_RECOVERY.md](accepted/research/bsd-operational-03/OPERATIONAL_VALUE_RECOVERY.md)
recovers two related objects from attributed historical sources:

- The rooted operation-and-relation profile of an object in an admitted
  mathematical structure already exists. Its evaluations, relations and
  definedness are not created by choosing an aperture. The profile is not
  asserted to be fully stored, finite, or computable without cost.
- An aperture-specific operational state retains enough of that profile
  for its observations, enabled operations and future observations.
  This is a projection of the broader profile, not a replacement definition.

Its exact reusable split is a CAR
`phi: X <-> H_hot x K_locked` satisfying

```text
phi T phi^-1(h,k) = (F_k(h),k).
```

The locked part is invariant under this operation; the hot part retains
the required dependence on it. Branches, operation direction and the
requested landing/readout remain supplied. Original fiving, shadow,
centered-coordinate and dimensional meanings are not reduced here to
this one YM realization. This audit reuses the recovery note's explicit
attribution; it does not claim a new historical-source recovery.

## 2. What experiment 06 actually established

The starting BSD occurrence is the residue ball
`b2 in 426 + 625 Z_5`, with the model, normalization and precision from
experiment 05. The numbers are coefficient representative and modulus,
not the real fraction `426/625`. See
[PREFREEZE.md](accepted/research/bsd-carry-key-06/PREFREEZE.md) and
[OPERATIONAL_PROOF.md](accepted/research/bsd-carry-key-06/OPERATIONAL_PROOF.md).

### Locked digits and moving fiber

On the finite carrier `Z/625Z`, multiplication by `b=426=1+25*17`
has the exact chart

```text
x = a + 25t,     0 <= a,t < 25,
M_b(a,t) = (a, t+17a mod25).
```

The inverse is multiplication by `201 mod625`, equivalently subtracting
`17a` from the hot coordinate. This is an actual total invertible map.
The low two base-five digits `a` are invariant. Each fixed `a` has the
complete 25-element `t` fiber; when `a` is a unit modulo five, multiplication
runs through the whole fiber. The saved exhaustive census has 25 fixed
points, 20 cycles of length five, and 20 cycles of length 25.

The retained carry is operational:

```text
b^5 = 1   mod125,
b^5 = 251 mod625.
```

A return in the coarse quotient therefore leaves a finer response. The
written argument also proves `v_5(b2^(5^j)-1)=2+j` for every finite
`j>=0` in the separately stated 5-adic contract. This uniform valuation
law does not follow merely from the finite cycle table. It holds for
every admitted principal unit whose difference from one has valuation
two, so it cannot select the next coefficient digit.

### Ordered roles and the failed precision extension

The mixed-representation identity is exact:

```text
426 (decimal) -> reversal -> 624 (decimal)
624 = 4444 (base five) -> add one -> 625 = 10000 (base five).
```

The source also constructs a seven-state role chart. For `m=1,...,7`,
set `g=2`, endpoints `m-1,m+1`, and outer value `c=m+2`. Then
`alpha=(m,2,c)` and `beta=(c,2,m+1)` are invertible views, giving
`426 <-> 625` at `m=4`. Gap alone has seven possible records. Full beta
625 determines alpha 426 within this declared chart. The chart is a new
candidate inspired by historical midpoint/gap/corner roles; it has no
proved curve law selecting its membership. The separate endpoint chart
reflects `(4,2,6)` to `(3,2,5)` and assigns the digit 4 a different role.

The full next precision fiber is
`{426,1051,1676,2301,2926} mod3125`. None satisfies the unchanged rule
`reverse_decimal(r)+1=3125`. The completed computation reports
`b2=2301 mod3125`, whose reversed value plus one is 1033. This refutes
that precise extension while preserving the finite identity and the
role chart. It is a useful example of testing a proposed continuation
on the complete old fiber rather than selecting a convenient lift.

### A quotient failure and an honest repair

Write an integer `n=10w+5h+r`, with `h in {0,1}`, `0<=r<5`.
Addition by five changes `(w,h,r)` to `(w+h,1-h,r)` and descends modulo
625. Holding the decade fixed instead defines
`f(n)=n+5(1-2h)`. This operation fails to descend:

```text
426 = 1051 mod625,
f(426) = 421,       f(1051) = 1056 = 431 mod625.
```

Keeping `n mod1250`, equivalently `n mod625` and one parity bit, repairs
the involution. Parity is added integer information; it is not supplied
by a 5-adic residue. Merely selecting the canonical representative does
not restore the claimed involution: `620 -> 0 -> 5` is a hostile case.

### Coordinate transport preserves a ratio, not an unknown scalar

For `u=log_5(-4)/log_5(6)`, the change of cyclotomic coordinate from
character 6 to -4 multiplies both the rank-two analytic coefficient
and the matching scalar height determinant by `u^-2`. Their quotient
is invariant. The saved finite calculation has `u=1544 mod3125` and
transported coefficient `1091 mod3125`; transport back recovers 2301.
This supplies a calibration law. It does not provide a new independent
analytic value or the missing BSD comparison scalar.

## 3. The BSD mixed-response donor is closer to the YM seam

[OPERATIONAL_BRIDGE.md](accepted/research/bsd-operational-03/OPERATIONAL_BRIDGE.md)
uses the actual curve `Y^2=X^3-1156X`. For admitted generic points,
the shadow `r(P)=Y/(2X)` identifies the two occurrences
`P` and `tau(P)=-P+(0,0)`. Appending the deterministic mirror `-r(P)`
does not split that fiber. The continuation `r(2P)` does:

```text
P=(-2,48),       tau(P)=(578,-13872),
r(P)=r(tau(P))=-12,
r(2P)=20447/3480,       r(2 tau(P))=-20447/3480.
```

With `r1=r(P)` and `r2=r(2P)`, the written inverse is

```text
V=(r1^4-289)/(2r1r2),
X=2(V+r1^2),       Y=2r1X,
```

enabled where its denominators are nonzero. The saved finite test uses
4096 points in a precisely specified doubling/tau-closed torsion carrier;
the scalar shadow has 2048 two-point classes, while the shadow plus
continuation has 4096 singletons. The broad generic rational formula and
that finite test have different carrier scopes.

Canonical heights of `P` and `tau(P)` agree even through pure doubling.
The first shadow therefore does preserve that narrower height receiver.
Mixed addition reveals what separate values lose: for the same rational
`Q=(-16,120)`, the saved MST 5-adic height calculation gives
`h5(P+Q)=4 mod5` and `h5(tau(P)+Q)=3 mod5`. The finite torsion census
does not include addition by this rational Q. These are separately
declared rational witnesses, and torsion-point recovery does not recover
the free basis or prove BSD.

The reusable mechanism is a mixed quadratic response. Knowing two
separate quadratic values does not in general determine their polarized
cross term. Keeping a deterministic reflection of a missing relation
cannot add the needed information. A separating combined operation can.

## 4. Exact candidate adapters to the current YM issue

The target is the two-square, seven-link open SU(2) graph in
[CONDITIONAL_OBSTRUCTION.md](accepted/research/ym2_conditional_construction/CONDITIONAL_OBSTRUCTION.md).
Retain all group values, vertex gauge constraints, the unit-round metric,
and `T=-Delta/2`. Based holonomies `P=eA`, `Q=Be^-1` give

```text
a=Tr(P)/2,       b=Tr(Q)/2,       c=Tr(PQ)/2,
Gamma(a,b)=c-ab,
T(ab)=13ab-c.
```

These are supplied YM equations, not a claim that an elliptic point is
a gauge field. The common operation-preservation interface is enough
to make the following tests meaningful.

**Adapter A: retain the cross response.** The old representation is
`C=(a,b)`. Refine it to `C'=(a,b,Gamma(a,b))`, equivalently `(a,b,c)`.
Then `T(ab)=12ab-Gamma(a,b)` is an exact decoder. This already repairs
the specified one-operation receiver. The chart has inverse
`c=ab+Gamma(a,b)`; the original link configurations are not thereby
individually recovered. Closure for subsequent kinetic operations requires
the gradients and Laplacians on this joint image. The already accepted
TWO_SQUARE_GEOMETRY.md supplies that closed joint operator. The present
continuation resolves its kinetic channels and uses their actual supports
in the source estimate; the earlier closure is not credited to BSD.

**Adapter B: preserve the entire hot fiber.** At fixed `(a,b)` the exact
possible cross responses are

```text
xi=c-ab in [-s,s],       s=sqrt((1-a^2)(1-b^2)).
```

The complete fiber is ONE(0) when `s=0` and MANY([-s,s]) when `s>0`.
On the interior, `eta=xi/s in [-1,1]` is an invertible fiber coordinate
given `(a,b)`; at the boundary retain `xi=0` without dividing by zero.
This is a typed counterpart of retaining a moving higher-digit fiber
over a known base. It is presently a coordinate decomposition. To call
`(a,b)` locked under a proposed YM move, that move must actually preserve
them and descend to the stated hot update. The elliptic multiplier's
invariance does not prove this YM invariance.

**Adapter C: test mixed continuation before scalar collapse.** The actual
SU(2) witnesses `a=b=0,c=-1` and `a=b=0,c=1` have equal separate
plaquette values and different `T(ab)` values. They play the same
operation-preservation role as the BSD pair with equal shadows and
different next/mixed responses. Keeping `(a,b,-a,-b)` leaves the same
fiber. Keeping its midpoint `c=ab` chooses a representative and erases
the distinction. The source's Haar identity
`E[c-ab | a,b]=0` establishes a conditional average, not pointwise
kinetic descent. Its conditional variance
`(1-a^2)(1-b^2)/3` records the lost response exactly.

**Adapter D: transport the full operator with a changed reference.** BSD
scales both sides of its rank-two comparison. YM's existing reference
handoff must likewise carry the residual `(A phi)/phi` together with
the reference diffusion. A chart that simplifies one coefficient while
dropping the residual has changed the requested operator. The useful
candidate is to simplify the moving correction in a chart whose full
operator transport is proved, then bound the retained mixed response.
No BSD residue supplies that estimate.

## 5. Keep the failed shortcuts and the next missing port

The current YM source proves that, for nonzero coupling on this shared-edge
graph, no nonzero eigenfunction can depend only on `(a,b)`, even through
an arbitrary joint function. Rephrasing those same two traces as an
operational number cannot undo the fiber obstruction. Their actual
operation profile already contains the cross relation, which the chosen
representation forgot. This is exactly why the operational-number
direction points toward retaining it.

The BSD carry also clarifies what a local success cannot select. A coarse
return does not establish a fine return; the common carry law does not
select one analytic lift. Correspondingly, repairing `T(ab)` does not
by itself give the actual vacuum or a uniform physical gap. The target
[conditional rail](accepted/research/ym2_rail_closure/CONDITIONAL_RAIL.md) keeps three
separate obligations: CR2 reconstructs a joint law; constant CR3 selects
the actual vacuum; CR5 controls collective response uniformly across
graphs. A new connected joint is useful input to these tests.

The strongest donor-supported next step is to use the already closed
joint operator on `(a,b,c)` while retaining the separate kinetic channels
it exposes in the vacuum equation. Improving the subsequent volume-uniform
estimates remains explicit work. Experiment 06's full BSD
and total Sha are OPEN; the YM continuum existence and mass-gap
obligations gain no proof status from that task's completed finite run.

## 6. Evidence and source bindings

This donor audit executed file reads and SHA-256 comparisons only. It
freshly checked that the experiment 06 live `operational_probe.py` and
the analytic/finite-audit logs match their recorded RUN hashes. All
three comparisons passed. It did not execute a mathematical verifier.
The saved RUN reports all listed jobs completed with exit code zero,
including the translator's 114 checks; those remain attributed execution
evidence. The current proof was reread after hashing. Source hashes bind
bytes and neither prove contents nor freeze the donor task's later changes.

| Source relative to `C:/github/RPRM-open/` | SHA-256 |
|---|---|
| `research/bsd-carry-key-06/PREFREEZE.md` | `58ce28bf2433f65695d8c012bdcea4bf7641471df86210d7d62cd09a6c77c41c` |
| `research/bsd-carry-key-06/OPERATIONAL_PROOF.md` | `794f5f175aa9a8b1186bbd258bee3b7a5932b265649866e346ba0e2dc8868ac6` |
| `research/bsd-carry-key-06/work/operational_probe.py` | `0bb292f1fd5095b49f058095d91f4aadeabb6d9be54a7de55dac5bf3553ad894` |
| `research/bsd-carry-key-06/runs/fresh_validation/evidence/operations.json` | `5b35474e06bfcc0fd037f2eb0fe689af06cdc7572d787a261e3e59620da257d3` |
| `research/bsd-carry-key-06/runs/fresh_validation/RUN.json` | `204a6efddbe9bcb26fe5824a61133e6511f1203c155f0f29930cde88404a1f85` |
| `research/bsd-carry-key-06/runs/fresh_validation/logs/analytic.log` | `7a3034824e11737184a18c47a49703ae26cd84d8259b92c35e5c781ed3435e66` |
| `research/bsd-carry-key-06/runs/fresh_validation/logs/finite_audit.log` | `77ba973f1b12247e414ffac5e5c3b3642c767e43cbd2983456dcbdd68c1f5d39` |
| `research/bsd-operational-03/OPERATIONAL_VALUE_RECOVERY.md` | `c0a050a0bbf3f26b495b48e79da8fc203a44775f0d3581e7321f6606e224c2ce` |
| `research/bsd-operational-03/OPERATIONAL_BRIDGE.md` | `dc089747cb4d3a7f9aae47c9131b779b5b1e2c650a1b127d71c09ac380edadae` |
| `research/bsd-operational-03/evidence/operational_sources.json` | `934f4e58a23d02ca241d7abcee64ed40eab36139a87ff2bf079b8cdc0c259e12` |
| `research/bsd-operational-03/runs/return_validation/RUN.json` | `4b6ce50969c156d33e95c7a37b335c9891da4d9c95b21a6f5267a52dbd2fd95a` |
| `research/ym2_conditional_construction/CONDITIONAL_OBSTRUCTION.md` | `e45e29b0162e5fdcbece541fa33e15466c13e96544bb60fe1bbea913ee282542` |
| `research/ym2_rail_closure/CONDITIONAL_RAIL.md` | `30d65be6af0424da4544fea5037c6a2476278850c2131180a85f274979cda7e2` |

The historical-source receipt in this table is a locator and byte binding;
its complete archived quotation set was not reopened in this donor audit.
The original meaning above is reused through the explicitly read recovery
note. Saved run creation times are `2026-09-13T00:21:56.731801+00:00`
(experiment 06) and `2026-09-12T20:50:50.087980+00:00` (experiment 03).

## 7. Latest completed-task donor: column weights carry the next response

Added 12 September 2026, approximately 18:45 America/Denver
(`2026-09-13 00:45 UTC`). The coordinator's latest compact wait reported
**Run BSD E5 test 01** completed and pointed to the new
[COLUMN_HANDOFF.md](accepted/research/bsd-carry-key-06/COLUMN_HANDOFF.md). This section
uses that note, its scoped source, and its saved extended evidence.
They were read; the BSD executable was not rerun. The operation below
remains the BSD task's explicit candidate for the user's intended
handoff, and 566 remains an intermediate stage without a supplied
terminal-readiness criterion.

The finite source carrier is every width-four decimal word, including
leading zeros, with ordinary values `0,...,9999`. For digits `a,b,c,d`,
the fold is

```text
F(1000a+100b+10c+d)=100a+10(b+c)+d,
F(n)=10 floor(n/100)+(n mod100).
```

Its reached output carrier is `0,...,1089`; it is not uniformly a
three-digit word. The current retained coefficient and modulus give
`2301+3125=5426`, with `F(2301)=231`, `F(3125)=335`, and
`F(5426)=566`. For `n+m<10000`, the exact addition rule is
`F(n+m)=F(n)+F(m)-90k`, where
`k=floor(((n mod100)+(m mod100))/100)`. The current operands have `k=0`.
The hostile `99+1` has folded-input sum 100 but folded total 10.

The complete total fiber over 566 contains
`4796,4886,4976,5066,5156,5246,5336,5426,5516,5606`. Subtracting the
known modulus 3125 gives ten admissible canonical coefficient candidates.
Retaining either the coefficient's zero tens digit or its prior residue
426 modulo 625 selects ONE(2301) within this completed fiber. This
reconstruction uses retained data; it does not independently predict the
analytic coefficient or prove a law forcing its zero mask.

Let `M(d)=9-d`, `N(d)=(-d) mod10`, and use the directed map
`S=N after M`, so `S(d)=d+1 mod10`. Apply this uniformly to the four
source digit occurrences. The equal folded observations below have
different lawful next values:

| Source word | Current fold | Source after S | Next fold |
|---|---:|---|---:|
| `5426` | 566 | `6537` | 687 |
| `4796` | 566 | `5807` | 587 |

The complete next-fold fiber at 566 is `{587,687}`. Applying S to the
three displayed digits of 566 instead gives 677 and is a different
operation. Likewise the correctly transported width-four complement
is `F(M_4 n)=1089-F(n)`, sending 566 to 523; the three-digit complement
would give 433. The column weights determine the changed mirror center.

The exact retained operational state is the ten-component weighted
occurrence record

```text
W_j=100[a=j]+10[b=j]+10[c=j]+[d=j],
sum_j W_j=121,                 F(n)=sum_j j W_j,
F(S_4 n)=F(n)+121-10 W_9,
W'_j=W_((j-1) mod10) under S,   W'_j=W_(9-j) under M.
```

Keeping `W_9` supplies the immediate missing wrap contribution. Keeping
the whole W supplies every future uniform S/M continuation. Its reached
carrier has exactly 5,500 states: it retains the two outside digits and
the unordered middle pair with multiplicity. The source has 10,000
words. The quotient forgets only the middle positions' order; an
operation treating those positions differently needs additional data.

Minimality for this declared receiver has a written proof: ten future
folds `y_k=F(S^k n)` determine
`W_(9-k)=(121-y_(k+1)+y_k)/10`, with indices modulo ten and `y_10=y_0`.
Conversely W produces those folds and all S/M words. The saved extended
census checks every source word and all ten cyclic continuations and
reports 5,500 W states and future signatures. For the retained source
5426 the path begins `566 -> 687 -> 808` and completes

```text
566 -> 687 -> 808 -> 929 -> 1040 -> 161
    -> 182 -> 303 -> 324 -> 445 -> 566.
```

This strengthens the donor mechanism relevant to YM: a present scalar
can have a complete known value while its lawful next response depends
on retained weighted occurrences. In YM, the new source calculation
likewise retains full spectral blocks and their actual support before
applying the next norm operation. These are typed applications of the
same preservation question; W is not identified with a Fourier block,
and no decimal carry is inserted into the YM Hamiltonian.

The following fresh file hashes bind the inspected latest donor. The
current script hash equals `source_sha256` in the saved evidence, whose
creation time is `2026-09-13T00:32:05.197058+00:00` and status is
`COMPRESSION_CARRY_AND_CONDITIONAL_HANDOFF_AUDITED`.

| Source relative to `C:/github/RPRM-open/` | SHA-256 |
|---|---|
| `research/bsd-carry-key-06/COLUMN_HANDOFF.md` | `7c75f84dae917d718e18e07d3aedf433d2e16ebaf7f61df857a5e81044fd77bf` |
| `research/bsd-carry-key-06/work/column_handoff.py` | `d1c999598b40f1056073927ea839f2752aa14af854e88db957525f4614b659ce` |
| `research/bsd-carry-key-06/evidence/column_handoff_extended.json` | `5df84c3ba6eca77c41f851ec4152a1b9ddd445fce9fb37b129cabee263a469c1` |

The exact finite fold, carry correction, repaired inverse, and complete
operational quotient are the surviving mathematical claims. Which
operation is forced by the analytic/arithmetic BSD objects and what
marks the terminal readout remain unresolved. The completed task does
not close BSD, independently establish the coefficient's digit mask,
or turn 687 into an unqualified next-number answer.
