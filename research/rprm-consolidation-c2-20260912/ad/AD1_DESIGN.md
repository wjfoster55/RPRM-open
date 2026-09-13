# AD1 scoped aggregate reuse specimen

Design and case definitions were written before the first specimen/check run.
`CASES.json` freezes the named development sequence and bounded reference family.
The historical SUM example is exposed material, so all resulting executions are
development evidence. The frozen pilot remains 14/16 versus 14/16 with its scope
disputes; no candidate session, pilot rescore, C1 restart or BSD work is involved.

## Contract

- **Carrier:** JSON row lists of length 0–4, each row `[occurrence_id,value]`.
  IDs are unique nonempty strings. Values are strict integers from
  `{-1,0,1,5,8}`; booleans, floats and NULL are admission errors. Equal values
  at distinct IDs remain separate occurrences. Duplicate values are admitted.
- **Statement and quantifier:** for this validated immutable snapshot, compute
  `S=sum(all row values)` and `D=sum(distinct row values)` and decide `S=D`.
  Empty sums are **0**, explicitly the finite-bag convention, implemented in
  the independent SQL reference with COALESCE. Native SQL SUM on empty input
  returns NULL; this is a declared difference, not an inferred SQL equivalence.
- **Ports:** the admitted snapshot supplies all rows; the requested aggregate
  pair or equality is the only missing readout. Occurrence lookup is a separate
  continuation requiring the actual row-to-ID map.
- **Representation:** a sorted value bag plus its exact aggregate pair; source
  SHA-256, relative cold-file locator and contract accompany each claim.
  Row order and ID-to-value assignment are omitted from hot storage. They are
  recoverable only by actually reading the named cold file and verifying its
  hash and admission. Hash identity binds bytes; neither that hash nor a
  locator proves the arithmetic or availability of the backing source.
- **Enabled operations:** hot readout of the identified immutable snapshot;
  promotion of a newly supplied source by an actual read and validation;
  semantic-bag cache lookup after that promotion; application of the conditional
  distinct-value rule after checking the retained bag; hash-checked occurrence
  lookup. An unrecognized operation is OPEN_NEW_CONTRACT.
- **Receiver/fiber:** aggregation is constant on each value-bag fiber. IDs and
  order generally are not. There is no inverse from aggregates/bag to the
  original full table; ONE denotes the unique requested output, not a unique
  entire source. No complete full-source reconstruction fiber is returned.
- **Evidence failures:** missing or hash-altered cold backing yields OPEN for
  occurrence lookup. It does not invalidate a previously justified hot answer
  about the saved snapshot, and does not establish mathematical NONE. A request
  about current file contents must use promotion, not historical hot readout.

## Written arithmetic obligations

If `m(v)` is multiplicity, then `S-D=sum_v (m(v)-1)*v`, by collecting equal
terms in a finite sum. Thus distinct values imply equality in every admitted
table. This sufficient condition is not necessary: duplicate zero values, or
balanced repeated -1 and 1 values, also give equality. The universal claim over
all admitted tables is refuted by `(P,5),(Q,5)`, yielding 10 and 5. Instance
equality for `(P,5),(Q,8)` remains true. The conditional rule transports to a
new qualifying table; its numeric aggregate is recomputed when its bag changes.
Reordering and bijective relabeling preserve the bag, hence both readouts.
These are written finite-sum arguments, not machine-formal proofs or a new
arithmetic theorem.

## Comparison and frozen checks

`ScopedStore` uses a sorted-bag cache and a compact explicit claim record.
`OrdinaryCache` is a conventional memoized aggregate implementation using
multiplicity keys. Both receive the same paths, bytes, operations and query
IDs. Both can retain exact bags/results and recover rows from the same source.
The ordinary baseline has the same freshness, admission and failure contract.
Its aggregate calculation is independent (weighted frequency sums). Shared
I/O/admission mechanics are disclosed; baseline decision logic is separate.

`reference_checks.py` imports neither implementation. It evaluates all 126
sorted bags of sizes 0–4 over the frozen five-value domain with SQLite, direct
Python arithmetic and the multiplicity equation. Sorted representatives cover
all aggregate bags in this bounded carrier; named transport cases separately
exercise order and ID changes. `check_ad1.py` compares both implementations to
those full aggregate pairs and runs the frozen case sequence, including the
six required task families, positive/negative cold reopening and admission
edges. Null and malformed cases are checked as admission errors, not sums.

Report source read attempts, successful reads, actual bytes read, decoded rows,
aggregate-pair recomputations and cache hits. A recomputation is one invocation
that calculates the pair, not one CPU instruction; sorting, hashing, parsing,
validation and cache lookup still do work. Logical retained bytes are the UTF-8
size of the serialized hot records and cache; this is not Python heap usage.
Report cold file count/bytes separately. SQL reference reads and calculations
are separate validation overhead, not charged to either candidate arm. No time,
token, asymptotic or storage advantage is inferred from these simple counts.

## Run and output boundaries

From this directory, using standard-library Python only:

```text
python -I -B check_ad1.py --output /external/fresh/ad1.json
python -I -B reference_checks.py --output /external/fresh/reference.json
```

Each entrypoint requires `--output`, refuses an existing report and never
overwrites it. The combined checker also reserves a fresh sibling directory
`<report-stem>.artifacts` containing its real cold backing, reference report
and retained hot records; it refuses an existing artifacts directory. Final
export replays can place both outside the extracted tree. Initial development
evidence is stored under `ad/evidence/`. Top-level PASS, row success and process
exit status must agree. No dependency installation or source-tree modification
occurs during an external replay.
