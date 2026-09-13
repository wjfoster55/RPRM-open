# Codex task — E5 arithmetic/analytic certificate test 01

**Active task:** one bounded BSD arithmetic verification and extension on
`E/Q: y^2 = x^3 - 25x`. This prompt supersedes only conflicting launch language
inside the bundled historical notes. Those notes are evidence, not extra jobs.

## 0. Purpose, ownership, and stopping boundary

William wants to test the recent descent, the analytic nonvanishing argument,
and the exact cube representation, then obtain one stronger quantitative result
if the mathematics permits it. Do real calculations and return a comprehensible
mathematical explanation, not just a new roadmap or an inspection checklist.

This is a separately authorized BSD task. Do not interrupt or change Codex's
Yang–Mills work, Cursor's fluids work, or the other conversation's P-versus-NP
work. Inspect local AGENTS instructions and existing work first. If equivalent
E5 work already exists, inspect it and continue the relevant unfinished part;
do not duplicate a completed run. Use an isolated sibling directory or worktree
without touching another lane's working files. Do not edit global routing.

Lind–Reichardt review005 and the old AD 14/16-versus-14/16 pilot stay closed.
No paper, publication, full-BSD claim, generic verification platform, paid
service, large dependency installation, commit/push/merge, or other-lane dispatch.
Do not expand to new curves, generator saturation, Cassels pairings, or odd-primary
Sha in this task. Their mathematical questions remain open in this work, not
forgotten or assumed solved.

Read `README.md`, `TEST_PLAN.json`, the two input notes, and `RPRM_CONTEXT.md`.
`context/` retains the actual supplied scope documents. Preserve the original
source files and historical receipts byte-for-byte. An input hash establishes
which bytes are present, not the truth of a theorem.

## 1. Replay, then independently check

Run from this package's root:

    python -B tools/replay_inputs.py --output runs/codex_replay

This runs the two source programs to new receipt paths and checks their stated
finite outputs. It is a replay, not a new independent mathematical verifier.
`preflight/` is an assistant-side replay only; do not present it as a Codex run.
The optional mpmath decimal illustration is not required by the exact certificate.

Then implement an independent checker under `work/` or the actual local experiment
directory. It must not obtain expected answers by importing source checkers or
reading the archived result fields. Reading the mathematical proof is allowed
and necessary: this is a transparent mathematical verification, not a blind
benchmark. Distinguish independently written mathematics/code, a backend
comparison, and a fresh execution of the same implementation.

If two independent workers are actually available, arithmetic and analytic
verification can proceed separately and reconcile at the end. The analytic
calculation must not use the arithmetic rank or a BSD-predicted quantity as an
input. If separate workers are unavailable, use one worker and clearly separated
implementations; do not invent sessions, independence, or runs.

Use exact integers/rationals for the algebra. An installed Sage, PARI, SymPy, or
rigorous interval backend can be an extra comparison after inspecting its real
API and assumptions. Ordinary floating-point agreement, even at many precisions,
is not a rigorous enclosure. Missing optional backends are `NOT_RUN`; finish the
standard-library mathematics rather than turning the assignment into installation.

## 2. Arithmetic question: have we accounted for every doubling class?

Primary source: `inputs/descent/E5_DESCENT_NOTE.md` and `e5_descent.py`.

Independently check:

1. The Kummer signature `([x],[x-5],[x+5])`, including O and the three y=0 points.
   Explain the cited kernel theorem `ker(delta)=2E(Q)` and the all-place Selmer
   condition; neither is proved by a finite point test.
2. The support argument, real-sign condition, 64-to-32 candidate restriction,
   and homogeneous covering equations. Show why a Q_2 point gives a primitive
   integral representative and hence a necessary solution modulo 4/8.
3. The eight rational representatives and their distinct signatures. Recompute
   the complete mod-4/mod-8 filter, or equivalent exact exclusion arguments,
   using an independent arithmetic route. Preserve the distinction between
   surviving a necessary test and having an actual rational witness.
4. The four disjoint cosets, with the three rejected representatives
   `(2,2,1)`, `(1,2,2)`, `(2,1,2)`. Explain why excluding a representative excludes
   its entire coset: local admissibility is a subgroup containing the witnessed H.
5. The conclusions `Sel_2 = G/2G`, size 8, rank 1, and `Sha[2]=0`; then the
   all-n consequence `Sha[2^n]=0`. Record the standard theorem dependencies.
   Do not infer a total Sha order or an odd-prime conclusion.
6. The compatible coordinates `G/2^nG ~= Z/2^n x (Z/2)^2`, the transition map,
   and the exact readback `R=mP+T+2^n R_n`. Check P, -P, O, the torsion points,
   and a modest finite selection of mP+T at levels 1..4. Bound coordinate growth.
   State why the odd free index of P is enough for these quotient coordinates,
   but not a proof that P is an integral generator of the full free part.

The provided 256 cases are exposed development fixtures, not independent
curve families. You need not inflate their number. Select a few exact spot
checks from a different route, such as rational x-search, where useful.

## 3. Analytic question: is the central zero provably simple?

Primary source: `inputs/analytic/ANALYTIC_NOTE.md` and `certify_e5.py`.

The source claims `L(E,1)=0` and `L'(E,1)>13/20`. Check these claims rather than
accepting the earlier assistant's conclusion or a saved `PASS`.

- Establish the exact curve identification, conductor N=800, sign epsilon=-1,
  local factor conventions, and alpha=2*pi/sqrt(800). Use a cited applicable
  theorem or an independently justified/backend local-data computation. Prime
  counts alone do not establish the conductor or root number.
- Check the bad primes 2 and 5 explicitly: the minimal singular reductions are
  additive, their L-factors are 1, and their coefficients vanish. Do not apply
  the good-prime recurrence to these bad-prime factors.
- Derive the normalization of the completed function and the Mellin split.
  It is the completed function that is odd about 1. Establish `L(E,1)=0`
  exactly from the sign, not from a tiny decimal or the rank label.
- Verify the sign-minus central-derivative identity

      L'(E,1) = 2 sum_{n>=1} (a_n/n) E1(alpha*n),
      E1(z) = integral_z^infinity exp(-t)/t dt, z>0.

  Explain why this representation is valid at the center. It is not substitution
  into the original Euler product outside that product's convergence region.
- Independently compute the prime counts and Euler coefficients through 20.
  The source reports only a1=1, a9=-3, a13=-6, a17=-2 as nonzero in that range.
  These are Fourier/Euler coefficients a_n; the central Taylor coefficient
  c1=L'(E,1) is a different kind of coefficient.
- Check EVERY link in the rational bound: 1/5<alpha<1/4, q=5/6 as an upper
  bound for exp(-alpha), |a_n|<=d(n)*sqrt(n)<=2n, the E1 bound, first-term
  positivity, retained negative contributions, and the all-n>=21 tail.
- Reconstruct the exact lower rational

      615556405007957768183 / 937494780448358006784 > 13/20.

  Recomputing this fraction alone does not verify the analytic premises that
  make it a bound. List each premise and its actual support.

A cited theorem may remain `THEOREM_CITED` after checking its hypotheses and source.
Do not pretend to re-prove modularity. Do not use E.sha().an(), a database rank,
or a rank-forced zero as independent analytic evidence. The source's 2.22737...
decimal is an exposed numerical illustration, not a certified target label.

## 4. RPRM construction tests: useful representation, not numerical pattern-fitting

Keep original RPRM meanings and the accepted C1 quotient correction in
`RPRM_CONTEXT.md`. Perform these finite checks without rebuilding the core engine:

- Form the five-bit map from delta(P), delta(T0), delta(Tplus), A, B to the 32
  candidate signatures. Verify it is a bijection AND transports componentwise
  squareclass multiplication to bitwise XOR (all 32^2 pairs are small).
- Reconstruct the admissible eight-vertex set from the independently established
  arithmetic filter. Only then compare it with `(1-u)*(1-v)`. The cube is a
  representation of the descent; it does not prove the local exclusions by shape.
- Transport a nontrivial invertible change of the five-bit basis together with
  the indicator/readout. Check unchanged results. Leaving the old indicator
  unchanged is a deliberate mismatched-transport control, not a counterexample
  to correct coordinate changes.
- Check `[P]=[-P] mod 2G`, but distinct classes mod 4G; likewise O and Q=2P
  merge at level one and separate at level two. Verify with exact points/halves
  or independent quotient coordinates, not just the supplied Boolean assertions.
- With the reconstruction remainder, a finer question is answerable. Without
  it or the original point, exhibit the collision proving that the coarse label
  alone does not choose the source's finer class. Keep old supported queries
  valid; lost backing is not an empty mathematical fiber.
- Eight classes include their identity. A wrapper is not a ninth class.
  Five bits, group rank, interaction degree, and analytic zero order have different
  meanings. No 9/4 alternation, unformalized sixing, or universal shadow law is
  to be invented. This is one scoped acquired-access realization, not a complete
  definition of Prestige One.

## 5. One new mathematical target: a certified interval for c1

After confirming or repairing the baseline argument, try to replace the coarse
one-sided bound with a **rigorous two-sided interval**

      a < L'(E,1) < b,    a>0,    b-a <= 1/100,

with rational endpoints and an explicit error ledger.

This is a bounded quantitative extension on the SAME curve, not a full BSD
leading-coefficient-formula computation. It tests whether the finite-head plus
certified-unopened-tail construction is actually reusable for a stronger readout.

Use the predetermined coefficient cutoffs `M=40,80,160`, in that order, stopping
when the requested interval is proved. Where a numerical backend is used, start
at 80-bit working precision and permit one refinement to 160 bits. For exact
quadrature, declare a finite refinement budget before running it. Do not search
for a favorable displayed answer or continue to arbitrarily large cutoffs.

Account separately for:

1. Enclosing alpha (pi and sqrt2).
2. Enclosing each retained E1 evaluation or its defining integral.
3. Rounding, if any, in multiplying and adding signed terms.
4. The entire infinite coefficient tail, using an all-term theorem.

A constructive option is exact/outward-rounded quadrature of exp(-t)/t, whose
monotonicity/convexity can provide bounds, plus a proven exponential tail. An
installed rigorous ball backend is also acceptable after checking its guarantees.
See `INTERVAL_CONSTRUCTION_HINT.md`; it is guidance, not an executed interval.

If only floating E1 values are available, retain them as `NUMERICAL_ONLY` and
build the enclosure from exact inequalities, or report the best rigorously
established interval and the precise remaining obstruction. A budget-limited
interval wider than 1/100 is a legitimate scoped outcome; do not relabel an
uncertified estimate as success. The previously proved sign certificate can
remain valid even when this stronger precision request is unresolved.

Show William what the interval means: it bounds the number multiplying t in
L(E,1+t), rather than listing digits that merely appear stable.

## 6. A small fixed set of controls — no open-ended mutation campaign

Execute the six controls in TEST_PLAN.json. Each must affect a real supplied
input, representation, or claim on the relevant path, not only a Boolean flag
that says the control should fail. Report an actual wrong-value witness,
contract rejection, or unresolved stronger request, as appropriate. Harmless
transport must pass. A changed-curve control demonstrates the old certificate's
non-applicability; it does not prove the changed curve has a different rank.

Do not add a registry, UI, or generic validator because a small local check
would suffice. Separate a rejected false claim from a failed program execution.

## 7. Return and stop

Return one runnable ZIP containing the actual source used, preserved supplied
inputs, independent checker, fresh command logs/receipts, and:

- `RETURN_TO_WILLIAM.md`: readable mathematical account of what held up, any
  correction, and the new interval result or precise obstruction. Define a
  coefficient and a tail bound briefly; avoid unexplained dense notation.
- `CLAIM_LEDGER.json`: claim ID, input identity, conclusion, evidence kind,
  checked hypotheses, source, and one of CONFIRMED/REFUTED/CONDITIONAL/NOT_RUN.
  Separate the standard cited theorem from its exact specialization.
- `INDEPENDENT_CHECKS.json` and `CONTROLS.json`, including all required entries.
- `DERIVATIVE_INTERVAL.json` plus its short derivation and error breakdown.
- `BSD_REBRIEF.md`: concise new mathematical outcome and remaining arithmetic
  frontier; do not substitute a roadmap for the result.
- One delivery inventory generated after final files are written, excluding only
  itself; omit caches. Supply actual source bytes, not a run-only directory.

Every required task/control needs a disposition. Do not derive the list of
obligations from only whichever rows were emitted. Distinguish missing optional
software from an unsupported theorem claim or a failed identity. Preservation
hashes do not certify meanings, chronology, or arithmetic.

If the baseline has a genuine mathematical defect, preserve the counterexample,
make the smallest justified correction, and update the claim ledger rather than
forcing the advertised result. Success is a checked, intelligible arithmetic
outcome, not a predetermined PASS. Stop after this one E5 experiment.
