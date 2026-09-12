# Return to William — Absolute Distinction 0.1, first consolidated run

This is the only active assignment. Archived ZIPs under `provenance/previous_packages/` were not treated as jobs. Their receipts are not user-side runs. There was no `AGENTS.md` in this workspace. This package, not RPRM Alpha, is the authority for the run.

## What the method now means

**Absolute Distinction** is an inspection policy with a small exact core, not a claim that mathematics is false or that the observer is unbiased.

- **Policy:** no relevant step is exempt because it is familiar, prestigious, aesthetic, or RPRM-branded. Unfamiliarity does not make a step wrong.
- **Scope:** a human still supplies the source, the question, the candidate representations, the dependency boundary, and the allowed experiments. The code does not discover which experiment is scientifically salient, missing physics, or every unlisted dependency.
- **Exact core:** on a declared carrier X, retained map C, and question Q, a decoder g with Q = g ∘ C exists on the reached image if and only if C(x)=C(y) implies Q(x)=Q(y). That is ordinary factorization through fibers, reused here, not a new theorem.
- **Operational core:** equal summaries must also agree on whether a declared partial operation is enabled and on the retained successor when it is.
- **Evidence:** proof, exact finite verification, software test, and source citation stay separate. A refuted representation is often an expected successful audit. An unexpected test error is different.

The method does not prove BSD, does not prove a general rank decoder, and does not measure research success. William’s remark that “about 60% of the work feels like this” remains a self-description, not a statistic from this run.

## Typed proposals, frozen before calculation

These names are not licenses to skip a counterexample.

| Name | Typed proposal | What it is not |
|---|---|---|
| Prestige / rebirth | Inspection policy: status is not a mathematical hypothesis. | Not an operator on curves or a rebirth of a number. |
| Two rails | Pair `(A,B)` with `(A,B)*(C,D)=(AC+FBD, AD+BC)` in `K[x]×K[x]`, the multiplication of `A+yB` in `K[x,y]/(y^2-F)`. | Not elliptic group addition, not a second independent number line, not automatic promotion to a higher tier. |
| Five / Six | Concrete carriers: the field F5 of the E0/E1 fixtures; the unit contrast that 2 is invertible modulo 5 and not modulo 6. | Not a mystical Five/Six, not a rank label, not a hop mechanism recovered from an archive. |
| Number operationality | A numeral is an address. Before composing, freeze whether a glyph is coordinate, value, operation, boundary, readout, or fiber, on a bounded carrier. | Not intrinsic meaning of a bare integer. |

Packaging (putting data in a pair or a hash), quotienting (identifying fiber-equivalent states), coordinate transport (e.g. `(X,Y)=(4x,8y)` over Q), and actual higher-tier promotion (a new receiver with a new question) are kept distinct. Transport is not promotion.

Abstract fixture rank is an input. The x-difference is extra information, not a free oracle.

## Three required traces

### 1. Original object → lossy summary → failed receiver → witness → repair

**Object.** Affine points of `E: y^2 = x^3 - x + 1` over F5, ordered pairs `(P,Q)` with `x(P) ≠ x(Q)` (36 pairs).

**Summary.** `C(P,Q) = (x(P), x(Q))`.

**Question.** `Q = x(P+Q)` under the group law.

**Failed receiver.** AD04: `REFUTED_ON_DECLARED_CARRIER`, 6 conflicting classes.

**Separating witness** (`runs/cursor_001` and `runs/candidate_001`, identical):

- `(P,Q) = ((0,1),(1,1))` and `((0,1),(1,4))`
- same retained `(0,1)`
- answers `x(P+Q) = 4` versus `3`

The two second points are `Q` and `-Q`. The summary forgot the y-sign, which translation needs.

**Repair.** AD05 retains the extra coordinate `x(P-Q)` on the same 36 pairs. Status: `SUFFICIENT_ON_DECLARED_FINITE_CARRIER`. An explicit decoder `x_add_with_difference(xP, xQ, x(P-Q), a, b, p)` matched the group-law x-sum on all 36 pairs.

That difference coordinate was built with the reference group law. It is additional information. It is not a matched-input prediction win, and it is not a complete Montgomery ladder.

Family B independently records 174 x-only collisions on a larger admitted set (1024 ordered pairs, 207 coincident-x exclusions) with the same repair identity.

### 2. Original lossy summary that is correct

**Object.** The same curve’s full 8-point group, including O.

**Summary.** `xview`: O tagged separately, otherwise the x-coordinate (sign discarded).

**Question.** `x(2P)`.

**Result.** AD01: `SUFFICIENT_ON_DECLARED_FINITE_CARRIER` (8 states, 5 classes, 0 conflicts). OP03: the doubling *operation* is also well-defined on this x-quotient (enabledness and retained successor agree).

On this carrier, discarding y really does preserve doubling. The audit is required to keep that positive result, not to treat every compression as a defect.

AD09 is a second valid compression: endpoints determine the midpoint for degree-at-most-one polynomials on the declared coefficient box, via `(left+right)/2`. The same observation on quadratics (AD08) is refuted.

### 3. Context change that invalidates a formerly lawful operation

Over Q, `φ(x,y) = (4x, 8y)` is a group isomorphism `y^2=x^3-x+1 → Y^2=X^3-16X+64`. Inverses divide by 4 and 8, units in Q. The lens audit checks that this transport preserves the listed sums. The original isomorphism theorem is not being called false.

Change the context to reduction modulo 5, and replace the scaling by `X=25x`, `Y=125y` (the model `Y^2 = X^3 - 625X + 15625`). Then 25 ≡ 0 (mod 5), so the intended inverse is not a field operation, and the displayed scaled model is singular at `(0,0)` over F5. The good unscaled model is not singular there.

A companion unit change: `pow(2,-1,5) = 3`, while `pow(2,-1,6)` raises `ValueError`. Invertibility is carrier-dependent.

## Corrections, nulls, known mathematics versus new implementation

**Known mathematics reused (not novelty claims):** fiber/factorization criterion; Weierstrass group law; Fermat descent for rank(`y^2=x^3-x`)=0 as a cited dependency; Lutz–Nagell as a cited dependency; structure theorem giving `|G/nG|/|G[n]|=n^r`; monic division giving unique `A+yB` in the coordinate ring; rational-root theorem on two explicit polynomials; the differential-addition identity under `x≠u`.

**New in this package as software, not as a new law:** a finite auditor that, given X, C, Q, searches for a same-summary/different-answer witness; the bundled S/L/B fixtures; context hashing of declared fields; negative controls of the auditor.

**Nulls / not established:** automatic dependency discovery; salience selection; a general rank decoder; speed advantage; Sage confirmation; proof-assistant verification; Selmer/Sha/L-functions; exact rank of EM; blinded workflow comparison; BSD.

**Expected refutations (successful audits):** AD02, AD04, AD06, AD07, AD08, AD10, AD11, OP01, OP02, and the S-family snapshot-as-rank-decoder claim. Do not fold 7 question-refutations, 4 sufficiencies, 3 operation audits, and 16/17 controls into one “accuracy” percentage.

**Important precision:** uniqueness of `A+yB` is in `K[x,y]/(y^2-F)`, not uniqueness of functions on a finite point set. Finite evaluations are a necessary check. They do not prove a full symbolic identity.

## Independent checks of three identities

These are separate from the bundled suite. No proof assistant ran.

### Coordinate-ring normal form

**Hypotheses.** K a field; F ∈ K[x]; work in K[x,y]; divide by the monic polynomial `y^2-F` in the variable y.

**Argument.** Any G has remainder of y-degree < 2, hence of the form `A(x)+y B(x)`. If two remainders differ by a multiple of `y^2-F`, the difference already has y-degree < 2, so it is zero. Uniqueness is in the quotient ring.

The 2250 pointwise product checks in family B are consistency on F_p-points, not this uniqueness proof. A second implementation of the same pair-multiplication formula would still not be an independent proof.

### Differential-addition identity

**Hypotheses.** Affine points P=(x,y), R=(u,v) on `y^2=x^3+Ax+B`, `x≠u`, char ≠ 2.

Let λ₊ = (v-y)/(u-x) and λ₋ = (-v-y)/(u-x). Then

```text
x(P+R) + x(P-R) = λ₊² + λ₋² - 2(x+u)
                = 2(F(x)+F(u))/(u-x)² - 2(x+u).
```

So `x(P+R) = total - x(P-R)`, which is the implemented formula.

A separate Python replay of that identity on the same admitted pairs as family B scored 1024 matches and 0 mismatches. That is a second implementation sharing the formula, stronger than no replay, not an independent proof of the formula.

### Quotient identity

**Hypotheses.** G ≅ Z^r ⊕ T with T finite abelian, n ≥ 2.

Then `G/nG ≅ (Z/n)^r ⊕ T/nT` and `G[n] ≅ T[n]`. For finite abelian T, `|T/nT|=|T[n]|` (structure theorem: both sides multiply `gcd(m_i,n)`). Hence `|G/nG|/|G[n]| = n^r`.

The 48 lens_audit rows set `index = n^r · |T[n]|` and check `index / |T[n]| = n^r`. That is cancellation of supplied sizes. Rank is not discovered.

A separate enumeration of nine small T and n ∈ {2,3,5} (27 checks) found `|T/nT|=|T[n]|` with 0 mismatches. The free-part factor `n^r` is not enumerable on Z^r; it remains the algebraic argument above.

## Finite-snapshot obstruction, with Lutz–Nagell used as cited

On `EM: y^2=x^3-x+M^2`, `P=(0,M)`, `M>0`. Slope of doubling is `-1/(2M)`, so `x(2P)=1/(4M^2)`, not an integer. Independent Fraction recalculation matched both user-side receipts (`M=105` and `M=100280245065`).

Lutz–Nagell (cited, not proved here): affine rational torsion on this integral nonsingular model has integral coordinates. Therefore 2P is not torsion, so P is not torsion. Mordell–Weil then gives rank(EM) ≥ 1. The code does not compute the exact rank.

Rank(E0)=0 is Fermat’s area-one descent, a sourced dependency, not a Python result.

Selected odd primes dividing M have identical good reductions, so identical counts. S3 collides at 3,5,7 and separates at 11. S10 collides at all ten primes through 31 and separates at 37. No fixed finite snapshot of this kind is uniformly rank-sufficient over the unrestricted constructed family. That is not an impossibility theorem for every finite algorithm or every restricted-family decoder.

## BSD frontier (identified, not implemented)

- **Sufficiency is not identification.** Even if the whole sequence of good Frobenius traces determined rank via Faltings-isogeny plus isogeny-invariance of rank, that would not identify BSD’s particular decoder `r = ord_{s=1} L(E,s)`. A truncated Euler product that is positive at s=1 is not a certified value of the continued L-function there.
- **Selmer ≠ local point-sets.** `0 → E(Q)/ℓ^n E(Q) → Sel_{ℓ^n} → Sha[ℓ^n] → 0` is about global cohomology classes with local conditions, not a Cartesian product of local points, and not “missing the identity.”
- **Finite-depth lifting leaves an obstruction.** `0 → G_n → I_{n,k} → ℓ^k A_{n+k} → 0`. Actual rational-point classes lift; the remaining term is a Sha piece. No splitting is assumed.
- **Persistence is not an exponent bound.** `image(S_{n+e}→S_n)=G_n` if Sha[ℓ^∞] is killed by ℓ^e. Watching a finite tower stabilize does not prove e. A divisible contribution can keep lifting.
- **Nullity is not analytic multiplicity.** For finite square A(t), dim ker A(0)=r and the induced map ker→coker by A'(0) an isomorphism imply `ord_{t=0} det A(t)=r`. Kernel dimension alone fails: `diag(t^2,1)` has nullity 1 and determinant order 2. No arithmetic family `A_E` with `L(E,1+t)=u(t) det A_E(t)` is supplied here.
- **Full BSD needs more than rank.** Periods, regulator, Tamagawa numbers, torsion, and Sha enter the leading coefficient. Pairings and normalizations must survive.

No fake Selmer, no fitted ranks, no `E.sha().an()` as independently known Sha, no full proof claim. The optional real-curve rank/L-series panel was not launched, not deleted, and not pretended.

## Verifier coverage

Declared controls that **do** reach executed arithmetic/auditor paths: omitted O; one-root-per-x; `(0,2)` off-curve versus group doubling; count-8 ⇏ cyclic-8 (E0 kernel 4 vs Z/8Z 2-torsion 2); K25(5)=K25(0); t^8 jet not exact zero; valuation of t^2 vs t; chart exclusions of O and x=0; AD07 tail cancellation; AD08 endpoints; context-hash changes of carrier/receiver/curve; JSON key order; dropped AD02; duplicate sources.

**Gaps recorded after `runs/cursor_001` (which already PASSed):**

1. Source-list order invariance was required in the prompt and was not an executed control (only dict key order was).
2. `bad_scaling_stays_invertible_mod5` used `25 % 5 != 0` and never attempted a modular inverse or the scaled model.

**Patch (not a failure-repair):** `src/distinction_audit.py` now attempts `pow(25,-1,5)` and requires the scaled model `(15625,-625,0,1)` singular at `(0,0)` mod 5; adds `source_order_changes_verdict`. Register text updated sixteen → seventeen controls. New manifest `MANIFEST.candidate.json` (the original `MANIFEST.json` was not rewritten). Re-run: `runs/candidate_001`, PASS, 17 controls.

**Residual gaps, not patched:** AD’s F25 control still does not compare `5 % 25` (lens_audit does). The ramified control compares two valuations rather than composing `t=u^2` as a substitution. Display-name and equivalent-equation invariance are not named controls; the auditor’s maps do not read display names. No E0/E1-keyed exceptions were installed.

## What was actually run

Python **3.14.5** (`tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)]`, optimize flag 0, assertions enabled. Platform: Windows-11-10.0.26200-SP0. Working directory: `C:\Users\bkbee\rprm-bsd-absolute-distinction`. Standard library only. No Sage install. No commit, push, merge, or paid compute.

| Command | Output | Result |
|---|---|---|
| `python -B run_all.py --output runs/cursor_001` | `runs/cursor_001/` | PASS, original `MANIFEST.json` sha256 `043b3d605994f21124c3fdb71409b77d569ed0cd8186508c25b382912d22b875` |
| `python -B sage_crosscheck.py --output runs/sage_cursor_001.json` | `runs/sage_cursor_001.json` | **NOT_RUN** — `sage` not on PATH; `No module named 'sage'` |
| `python -B tools/freeze_manifest.py --output MANIFEST.candidate.json` | `MANIFEST.candidate.json` | 18 files; created after the coverage patch, not a backdated pre-registration |
| `python -B run_all.py --manifest MANIFEST.candidate.json --output runs/candidate_001` | `runs/candidate_001/` | PASS, candidate manifest sha256 `28885f21146065783c06efe9703c85ae818036850c52f87833c8e962e6850b21` |

`sage -python ...` was not used because Sage is absent.

Stage execution (both user-side runs): `snapshot_3_primes`, `snapshot_10_primes`, `lens_audit`, `branch_layer`, `absolute_distinction` all **PASS**. No unexpected test errors. Expected refutations preserved. Post-run source integrity PASS.

`receipts/build_validation/` is assistant-side package validation from the zip, **not** this user-side execution.

Elapsed seconds are recorded in the receipts and are **not** a speed comparison.

## Next experiment proposal (not launched)

**Task.** On one fixed curve with a published 2-descent (independently tabulated 2-Selmer and an independent list of 2-coverings), treat each covering as a source object. Question: which classes lie in the image of `E(Q)/2E(Q)`. Representation: local-solubility bits at a **frozen** set of places, declared before looking at global generators.

**Conventional comparator.** Standard 2-descent as in Stoll’s notes, or an ordinary implementation such as mwrank / Sage `simon_two_descent`, using the **same** covering list and the **same** local tests.

**Matched information and cost.** Both sides receive those coverings and local tests. The proposed method may not take unpaid extras: extra places, a known generator, a height bound, or `E.sha().an()`. Cost is counted as the number of local solubility tests plus whether a global point is actually constructed.

**What would count against it.**

1. Two globally distinct Selmer classes with the same frozen local-solubility vector.
2. An apparent cost win that disappears once extra places or a known point are charged.
3. Treating finite-depth stability of the 2-power tower as an exponent bound for Sha, or reporting `G_n` while only dimensions were computed.

This assignment stops before that study. No Selmer code was added here.

## Stopping point

The bounded suite ran. Absolute Distinction is now a precise, finite, human-scoped inspection method with verified contracts on known fixtures. Open BSD and Selmer obligations remain open. Valid compressions and concrete failures are both retained. Uncertainty is preserved.
