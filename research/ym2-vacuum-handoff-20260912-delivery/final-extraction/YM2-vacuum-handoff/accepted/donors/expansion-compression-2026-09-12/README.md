# Expansion, compression, and the next expansion

12 September 2026. **The connection is substantive, and RPRM already contains several exact parts of it.** The closest new live example is Yang–Mills: its log-density calculation cancels disconnected combinations while retaining a connected orientation term. The closest historical dynamic example is Audit99: a new operation reopens exactly a calculable part of the old remainder. The still-missing general result is a uniformly affordable way to select, construct and update such sufficient records across the intended growing problem family.

This investigation continues the [seven/eight and SAT work](../liar-teacher-formalization-2026-09-12/README.md). It preserves William's suggestion that the growth/reduction pattern need not have a fixed factor. Mathematical statements below distinguish existing source results, new written synthesis and new finite checks. Source metadata and exact local locators are in the companion notes.

## 1. What is already formalized

The current core already proves that an operational Fold must preserve the requested observation, whether the next operation is enabled, and the next retained state. Matched folds compose; a finite refinement procedure finds a stable future quotient. Its minimum number of states is the number of distinguishable future behaviors. These are [O05, O05F, O06 and O07](../../docs/operations.md#o05), not new results of this task.

The historical [Foundation](C:/github/RPRM-foam-development/atlas/FOUNDATION.md:127) also explicitly says that scaling should depend on the live frontier and touched dependencies, with exact ancestry retained through a separate access route. It supplies a design obligation rather than a universal complexity bound.

Three operations must remain distinct:

| Operation | Exact example | Effect |
|---|---|---|
| Add source information | Append another independent bit or attach another component | Enlarges the source histories or configuration carrier |
| Change coordinates without losing information | Common/detail split; carry plus signed residual; shared DAG with retained children | Changes access or storage organization; the relevant source remains recoverable |
| Retain only a sufficient answer/state | Sum instead of ordered increments; boundary relation instead of private witnesses | Merges sources that the admitted receiver cannot distinguish |

These can alternate in one process. A claimed growth factor must say whether it counts source possibilities, retained states, encoded bits, intermediate computation, or unresolved interactions.

## 2. Your −0.6/+0.4 stack has an exact small model

Take a finite ordered history `b₁,…,bₙ`, each bit zero or one, and **explicitly choose addition** of increments `bᵢ−3/5`. This is a new worked specialization of the recovered offset and common/relative constructions, not an assertion that every use of those coordinates is a sum. Put `k=Σbᵢ`. Then

```text
Sₙ = Σ(bᵢ−3/5) = k−3n/5.
append b:  (n,k) -> (n+1,k+b).
```

For a total-sum receiver with the length supplied, the `2^n` possible histories collapse to exactly `n+1` totals. Every class k contains `binomial(n,k)` histories. The exact retained bit requirement is `ceil(log₂(n+1))`; a variable-length process also needs its length or equivalent information when the receiver asks for the mean. Thus the number of histories can double at each arrival while the sufficient encoded record grows only at occasional bit boundaries. No cancellation of actual source occurrences has been assumed.

| Increments n | Possible histories | Distinct totals | Minimum bits for total, n supplied |
|---:|---:|---:|---:|
| 2 | 4 | 3 | 2 |
| 4 | 16 | 5 | 3 |
| 8 | 256 | 9 | 4 |
| 12 | 4,096 | 13 | 4 |

The record `(n,k)` also determines every permutation-invariant question on this fixed two-symbol history. It does not determine order: `01` and `10` have the same record and different first bits or dyadic locations. Their complete original history fiber must remain MANY unless retained lineage selects one.

For any supplied finite cap N, maintaining the binary counters uses O(log(N+1)) working bits and at most O(N log(N+1)) elementary bit work for N arrivals under ordinary binary arithmetic. Retaining the original word for promised order recovery separately costs N bits. This is a proved resource bound for this simple additive family; the exhaustive tests below cover N≤12.

The carry form is equally exact. Write

```text
5Sₙ = 5w+r,     0≤r<5.
Sₙ = w+r/5.
append b:
    c,r′ = divmod(r+5b−3, 5)
    w′ = w+c.
```

Here w is winding and r/5 is the bounded phase. Since `r=(-3n) mod5`, **phase alone contains no information about k at fixed n**. The two possible increments differ by one full turn; the variation moves into winding. Dropping winding makes all histories of one length look identical even when their totals differ. This directly connects the +0.4/−0.6 seam to the need to retain a remainder when condensing.

The historical [Audit116](C:/github/RPRM-foam-development/experiments/RPRM_ANTICIPATORY_SIGNED_CARRY_TENSION_AUDIT_116/REPORT.md) separately proves early carry `bq+d=b(q+1)+(d−b)` and tests cascades with a terminal parent and signed residual. Its negative residual records the remaining margin. It has a stated local cost and tie rule; the signs do not choose the compression schedule by themselves.

## 3. A recovered growth rule that is not repeated doubling

[Audit99](C:/github/RPRM-foam-development/experiments/RPRM_VERSIONED_OPERATOR_REOPEN_BIG_PEEK_AUDIT_99/REPORT.md) already establishes an exact version-change rule for a supplied additive operator language. For `h∈Z/MZ`, current actions K give a quotient with `g=gcd(M,K)` and `h=gq+r`. Adding k gives

```text
g′=gcd(g,k),     d=g/g′,
r=g′s+r′,
q′=dq+s.
```

Only the tag s reopens from the old residue; r′ stays outside the working quotient. Each old class splits into d new classes. The factor is determined by the admitted operations. The report proves the specified rule and records a much larger finite audit, with arbitrary new operator languages still open.

Our new small illustration holds the **same sixty source states** fixed and initially observes `floor(h/12)`. It repeatedly computes the coarsest stable partition from the actual operation table, independently of the gcd formula:

| Admitted cyclic additions | g | Required working states | Fixed-width bits |
|---|---:|---:|---:|
| 12 | 12 | 5 | 3 |
| 12,18 | 6 | 10 | 4 |
| 12,18,20 | 2 | 30 | 5 |
| 12,18,20,25 | 1 | 60 | 6 |
| 12,18,20 | 2 | 30 | 5 |
| 12 | 12 | 5 | 3 |

The refinement factors are **2,3,2**; the later coarsenings are lawful because those stronger futures were explicitly retired. If +25 must remain executable, its needed distinctions cannot be removed merely to keep the record small. This is a versioned operation example; the offset stack in §2 instead grows the source history itself.

Audit99's mixed nonunit example is an even closer selective-reopening result: one new operator requires a **ternary residue**, while the rest of the old residue remains cold. [HISTORICAL-RESULTS.md](HISTORICAL-RESULTS.md) records its exact formulas and scope.

## 4. The recurring pattern as an explicit contract

For each finite stage n, supply source Xₙ, requested observation Qₙ, current representation `Cₙ:Xₙ→Zₙ`, new-input carrier Uₙ and a partial growth/attachment operation `Eₙ:Xₙ×Uₙ⇀Xₙ₊₁`. The same supplied input u must have the same identity and meaning in each comparison. If its compatibility depends on a hidden source relation, that joint dependence belongs in Eₙ's domain.

The exact compressed update exists precisely when:

1. Qₙ is constant on Cₙ-fibers;
2. for equal Cₙ states and the same u, Eₙ is enabled for both or neither;
3. for every such enabled pair, their Eₙ outputs have equal Cₙ₊₁ values.

Then define the update using any representative. These conditions make it well-defined and give

```text
Cₙ₊₁(Eₙ(x,u)) = Updateₙ(Cₙ(x),u).
```

Conversely any exact update with matching domains forces those conditions. Induction preserves observations and admittedness through every finite stage. This is the existing operational-descent proof applied to a supplied family of stage carriers. It establishes when expansion and compression can be interleaved; it does not establish how cheaply the maps can be discovered or evaluated.

The resource claim must be added explicitly. For input length L and relevant frontier size w, name bounds on **retained bits, temporary peak bits, update/normalization work, operator selection, and any source reopening**. Total work is the sum over stages, including construction. Stored cold history is counted separately; a small handle does not make the backing record constant size. To claim polynomial total cost, the number of stages and these bounds must jointly be polynomial in the original input length. Polynomial work in an already enormous intermediate object is insufficient.

Normalization also needs a stated law. A strictly decreasing rank can prove that reduction terminates; unique output requires appropriate confluence or a supplied selector, and semantic preservation remains separate. The historical Round23 result and its same-rank nonconfluent control are recorded at [CLAIM_LEDGER.md](C:/github/RPRM-foam-development/atlas/CLAIM_LEDGER.md:491). A normal form can still be large or expensive to construct.

There is therefore no need to posit a universal numeric multiplier. The useful general pattern is **attach → preserve the shared relation → reduce to a sufficient executable state → reopen only what the next operation requires**, with its own quantitative bound for each family.

## 5. What the other research contributes

The dated inspection is [LIVE-RESEARCH.md](LIVE-RESEARCH.md). These are source-attributed results; their campaigns were not rerun here.

- **Yang–Mills is the closest current cancellation example.** The actual-vacuum expansion passes from `ψ=1+ru₁+r²u₂+…` to a log-density coefficient `2u₂−u₁²`. Disconnected pair products cancel; an adjacent orientation term survives. An actual-vacuum witness shows that separate loop readings omit a necessary joint relation. What remains open is an all-order/conditional estimate controlled uniformly as the graph grows. The current analytic radius shrinks with graph size. This explains why merely adding all absolute contributions can grow uncontrollably and why discarding every interaction would lose the object being studied.
- **BSD E5 supplies a different coverage mechanism.** Its newest completed continuation settles the particular curve's primitive generator and BSD formula, with a published theorem among its dependencies. Finite binary quotients by themselves miss an odd-index obstruction. A proved height bound reduces the missing-generator question to a complete finite enumeration. The general BSD task is active. Its contribution here is a justified cutoff and retained quotient remainder, not a universal compression ratio.
- **Fluid F2 supplies a concrete failure of premature compression.** Two moving cells temporarily support one another during a single update, defeating a proposed static support certificate. The admitted temporal relation had been omitted. The earlier finite replay remains valid on its tested scenes; it does not rescue the refuted general certificate.

The common obligation is closure under the **next relevant operation or boundary change**. The domain-specific mechanisms are different: arithmetic coverage, connected cancellations, and temporal support need their own proofs.

**The YM continuation completed during this investigation.** Its new [conditional-port result](../ym2_connected_vacuum/NEXT_CONDITIONAL_PORTS.md) already bounds the calculated local terms using nearby plaquette incidence, independently of total graph size. It retains the exact full-remainder contribution beside that bound. Thus one part of the requested scaling law is now proved there; uniform control of the retained remainder is the specific next obligation. [LIVE-RESEARCH.md](LIVE-RESEARCH.md) records the final refresh and source-export checks.

## 6. The especially relevant earlier SAT work

This search recovered substantial prior work beyond the new parity pilot:

- [Audit60 future-congruence census](C:/github/RPRM-foam-development/experiments/RPRM_AUDIT60_UNIT_FUTURE_CONGRUENCE_CENSUS_01/REPORT.md) shows that current nonemptiness, count or least witness need not preserve later restrictions. Its finite formula image is not even operation-closed until eighty additional semantic states are admitted.
- [UTCCC costed-closure preflight](C:/github/RPRM-foam-development/experiments/RPRM_UTCCC_COSTED_CLOSURE_SEAM_PREFLIGHT_01/REPORT.md) already compares affine, 2-CNF, Horn, model-list and decision-diagram languages. Its three-variable witness `affine mask 105 AND 2-CNF mask 43 = mask 41` exits all three compact logical languages. Parity is its positive compact control. It separately retains order selection, conversion and intermediate construction peaks.
- [The corrected R1 source/Apply bridge](C:/github/RPRM-foam-development/experiments/RPRM_AUDIT60_ROBDD4_COSTED_SOURCE_APPLY_BRIDGE_01/REPORT.md) records exact graph compilation and update costs for 679,121 fixed four-variable formula occurrences. R0 remains HOLD; R1 has the repaired independent verifier. Equal final graphs can have different construction and peak costs. The compiler explicitly examines sixteen assignments, so this is a finite precursor, not a uniform succinct-input algorithm.

These results sharpen the continuation: a useful candidate must preserve joint solutions while moving between representations, retaining the source/operation interface and paying for conversion and peaks. The earlier study should be reopened before building another generic representation-comparison census.

A terminal SAT bit remains a legitimate final answer. It generally cannot serve as the whole state for subsequent constraints. Our small group control makes the same distinction: both pairs of nonidentity elements `(a,a)` and `(a,b)` look like `(false,false)` under “is identity?”, yet their products differ. Exhausting all sixteen Boolean update tables confirms that no update on those two bits can implement the supplied four-element group product receiver. Retaining the group element resolves it.

## 7. What was checked and where to continue

[TEST-SPEC.md](TEST-SPEC.md) was written before the new implementation. [verify_connections.py](verify_connections.py) passed **34,936 assertions**: all 8,191 bit histories through length twelve, exact rational sums and carry updates, complete binomial fibers, all sixty states across six operator versions, independent Moore partitions versus the gcd classes, terminal-Fold failure and joint-correlation controls. The latter distinguishes independent fair-bit variance 1/2 from repeated-source variance 1 despite equal single-bit marginals.

Reproduce with standard Python:

```powershell
python -I -B research/expansion-compression-2026-09-12/verify_connections.py
```

The [result receipt](RESULTS.json) binds the script and frozen spec hashes. The assertions are finite checks, not 34,936 independent proofs. Historical PASS counts remain source reports, and the zero/offset symbols do not establish an unprovided physical composition law. In particular, the historical oriented/double-negative zero remains a typed candidate with unresolved closure semantics; this note has not assigned it a universal recurrence.

The next useful synthesis is a **versioned sufficient-state controller with a declared resource bound**: begin with the proved affine/carry cases, preserve non-affine or connected residuals explicitly, and test how a required operation forces refinement. Use the historical UTCCC size/peak controls and the YM connected-term examples as separate tests of that contract. A general efficient controller is still an open construction, with meaningful exact components already available.

This record is indexed in the [knowledge base](../../recovered-concepts/README.md) and [paper backlog](../../recovered-concepts/NEXT-PAPER-BACKLOG.md). [VERIFICATION.json](VERIFICATION.json) records file bindings and checked links. The historical Memory Fabric snapshot was inspected read-only; retrieval here followed current local reports and exact corpus locators. No compile/cache write, database ingestion, historical campaign rerun, or paper publication was performed.
