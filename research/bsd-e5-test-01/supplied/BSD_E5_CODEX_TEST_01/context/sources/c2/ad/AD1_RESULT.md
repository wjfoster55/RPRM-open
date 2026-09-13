# AD1 result — scoped reuse demonstrated; conventional tie

**ACCEPTED_WITHIN_SPECIMEN_SCOPE. Development evidence.** The frozen run passed
all **30 named cases and 126 bounded aggregate-bag representatives for both
implementations**. SQLite and a separate direct calculation agree on both
numeric outputs throughout the 126-bag reference family. This demonstrates a
working scoped reuse policy. Its behavior coincides with competent ordinary
typed caching; no general improvement or performance advantage is established.

The design and named case definitions preceded the first specimen run. Their
hashes are in `CASE_FREEZE.json`; the checker verifies the case hash. The freeze
binds the definitions, while the execution history supplies the order evidence.
It is not a cryptographic proof of chronology. The source SUM example was
already exposed development material. The retained historical pilot stays
**14/16 versus 14/16**, with its existing scope disputes and missing provenance;
no old scoring, answers, dispatch records or closed arithmetic work was changed.

## What happened

| Frozen task family | Observed scoped and ordinary result | Actual work per arm |
|---|---|---|
| Valid repeat | Saved `(13,13)` reused for its immutable snapshot | 0 reads, 0 aggregate recomputations |
| Harmless reorder / ID relabel | New bytes bind a new source; the equal value bag reuses `(13,13)` | Each: 1 read of 18 bytes, 0 recomputations |
| Changed values `(5,5)` | Returns `(10,5)`, equality false | 1 read of 18 bytes, 1 recomputation |
| Changed quantifier | Universal equality rejected with admitted `(P,5),(Q,5)` | 0 source reads; 1 counterexample aggregate calculation |
| Positive conditional reuse | Distinct-valued replacement `(-1,1,8)` gives `(8,8)`; the same equality rule applies | Promotion: 1 read of 27 bytes, 1 recomputation; conditional check: 0 reads/recomputations |
| Evidence failure | Historical hot `(13,13)` survives missing or altered cold backing; new ID lookup returns OPEN | Hot: 0 reads; missing lookup: 1 failed attempt; altered lookup: 1 successful 18-byte read then hash rejection |

Available, hash-checked occurrence lookup returns ONE(8) for Q; a complete scan
returns NONE for absent ID Z. That is an empty **lookup** fiber, not a conclusion
that the whole source or mathematical possibility family is empty. An unknown
operation returns OPEN_NEW_CONTRACT. No solved full-source fiber is claimed.

Duplicate values are legal. Duplicate IDs, NULL, booleans, floats, malformed
rows, empty IDs, out-of-domain values and excess row counts are admission errors.
The empty bag returns `(0,0)` under the explicit finite-sum/COALESCE convention.
The independent oracle records native SQL empty SUM as `(NULL,NULL)`.
Duplicate zeros and `(-1,-1,1,1)` give `(0,0)`, preserving the distinction between
a sufficient distinctness assumption and a necessary condition for equality.

The numeric answer and the claim must both change appropriately: the conditional
rule survives a new distinct-valued instance, but the old numeric answer 13
does not. Harmless byte changes are not mathematical invalidity; validating
their new source still costs a read. Already retained values suffice to reject
the duplicate-instance conditional assumption without reopening the source.

## Actual accounting

| Measure, per arm unless noted | Scoped | Ordinary |
|---|---:|---:|
| Named-sequence read attempts / successful reads | 22 / 21 | 22 / 21 |
| Named-sequence bytes read | 376 | 376 |
| Named-sequence decoded admitted rows | 25 | 25 |
| Named-sequence aggregate-pair recomputations | 7 | 7 |
| Named-sequence semantic cache hits | 4 | 4 |
| Full run read attempts / successful reads | 148 / 147 | 148 / 147 |
| Full run bytes read / decoded admitted rows | 4,073 / 445 | 4,073 / 445 |
| Full run aggregate-pair recomputations / cache hits | 127 / 10 | 127 / 10 |
| Final hot records / cache entries | 136 / 126 | 136 / 126 |
| Logical serialized hot bytes | 105,538 | 30,845 |

Both arms share the same actual cold backing: **143 files, 4,001 bytes** remain
after the deliberate missing-file test. Repeated records and cache keys are
counted in the hot serialization. The explicit claim repeats contract metadata,
so it is larger in this encoding. These figures describe this accumulated test
store, not minimal storage or Python heap size. A recomputation counts a paired
aggregate calculation, including the explicit universal-claim counterexample;
it is not a full operation-cost model. Parsing, sorting/frequency construction,
hashing, validation, set construction and cache access still perform work.
Reference calculations, checker orchestration, fixture definitions and result
receipts are separate validation overhead. No time or model-reasoning costs
were measured, and zero source reads never means zero computation.

## Evidence, review and limits

- `evidence/development.json`: full result rows, per-action counters, totals and
  actual retained-state counts; top-level PASS agrees with exit status 0.
- `evidence/development.artifacts/reference.json`: independently calculated
  SQLite/direct/multiplicity results; imports no candidate decisions.
- `evidence/development.artifacts/scoped-hot.json` and `ordinary-hot.json`:
  actual serialized retained records/cache. Each source route is relative to
  this artifact directory; cold recovery actually reads the named file.
- `evidence/OUTPUT_GUARDS.json`: both existing-report guards and the existing
  artifact-directory guard reject with Python exit 2; prior report hashes
  remain unchanged. These CLI checks are separate from mathematical evidence.
- Independent child review `ad1_reference_review`: the preliminary mathematical
  review was **accepted within scope**, deriving the multiplicity equation and
  checking 156 ordered tuples of lengths 0–3 plus the cancellation example with
  stdlib SQLite 3.50.4. Those scratch checks produced no file receipt and are
  attributed reviewer testimony, not substituted for the packaged 126-bag
  reference artifact. The final read-only code/evidence audit was **ACCEPT
  within the frozen specimen scope**, with no blocking defect and no extra
  execution. Its two reporting clarifications are incorporated here: the
  `decoded_rows` counter means **admitted decoded rows** (rejected tables may
  already have been JSON-parsed), and hot records have the in-process trust
  boundary stated below. The audit reviewed 156 case rows / 312 arm results;
  it did not claim independent full runner-soundness verification.

The full scope is integer tables of at most four rows over the declared five
values. Sorted representatives cover its aggregate bags, not arbitrary Python
inputs, all ID spellings, every file failure, unbounded SQL, concurrency or
arbitrary future operations. The written distinctness argument is an elementary
finite-sum proof within the admitted class; finite tests are not promoted to an
unbounded theorem or checker-soundness proof.

Hot claims are trusted immutable objects created by this in-process store.
There is no API claiming to authenticate arbitrary imported or hand-forged
claim objects; saved JSON is an audit export, not a verified import format.
The baseline shares source I/O and admission code but independently implements
the aggregate/cache and conditional decisions. Its matching result is a useful
functional comparison, not an isolation experiment between autonomous agents.

The retained hot result answers a saved snapshot, not current disk contents.
Source identity, arithmetic evidence and requested-answer sufficiency remain
separate: a verified hash is not a proof; a missing file is not mathematical
NONE; a unique aggregate pair does not select a unique entire source. Full
identity/order recovery and any new unsupported receiver remain dependent on
their own source and contract.

No acquisition mechanism, broad AD method, full RPRM framework, bias-free
observer guarantee, new arithmetic theorem, speedup or publication result is
claimed. C1 acceptance and its wider unimplemented concepts remain unchanged.

## Reproduction

Use an output outside the extracted deliverable for final replay:

```text
python -I -B ad/check_ad1.py --output /external/fresh/ad1.json
```

The independent reference alone also accepts a fresh external report path:

```text
python -I -B ad/reference_checks.py --output /external/fresh/reference.json
```

Both use standard-library Python/SQLite only, refuse overwrite, and need no
installation, model session, donor tree, manuscript edit or git operation.
