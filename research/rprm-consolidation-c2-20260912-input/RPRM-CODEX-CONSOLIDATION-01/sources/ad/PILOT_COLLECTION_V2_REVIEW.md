# Review of pilot_collection_v2 — retain the tie; distinguish scope and provenance

## Verdict

Accept the delivered first-response collection as a reproducible **artifact** and preserve the original scoring unchanged. The submitted primary outcomes are tied: conventional 14/16 families, protocol 14/16, with the same two families marked failed. This is not evidence of a measured benefit from the added protocol. It is not proof that the method can never help.

Do not call this an independently verified isolated experiment on the basis of this zip alone. It contains answer artifacts, metadata, and scoring records, but not the exact v2 candidate packets, evaluator keys, one-window parent prompt, isolation-limit document, or original execution transcripts. No allegation of fabrication or contamination follows from those missing materials.

Two failed case labels require a scope annotation: both arms explicitly give the correct equal outputs on the supplied instances, then reject schema-wide equivalence using valid counterexamples. Their mathematics is not wrong at that stated scope. Whether the task unambiguously demanded an instance-only label must be checked against the exact dispatched inputs, not a reconstruction of v1.

## 1. Fresh checks performed

All checks were run read-only on the original archive, or against separate copies. No candidate response, instruction, or submitted score was edited. No new candidate generation was performed.

- All 71 listed inventory entries match. The only unlisted file is the inventory itself, explicitly exempted from its self-hash. There are 72 payload files.
- All 32 Markdown/JSON answer pairs match the dispatch log's recorded hashes, lengths, family IDs, arm IDs, and session labels.
- There are 16 matched families, with the recorded first-arm allocation balanced 8/8. This is the recorded intended order, not a timestamp-verified execution chronology.
- The primary semantic payloads were read and checked: 19 per arm, 38 total. Ambiguous-item linguistic adjudication is not replaced by this arithmetic check.
- All 52 SQL case verdicts in the raw responses match their entries in PAIRED_OUTCOMES.json.
- All 26 SQL reference cases were independently reproduced with Python sqlite3 and exact Fraction arithmetic, using the earlier attached sampler's family definitions and the collection's original/candidate ID mapping. For the ordering case, the check covers permitted tie orders rather than accepting one incidental fetchall order.
- The original 14/16 versus 14/16 family tally is reproduced. There are no discordant family outcomes under the retained scoring.

Important source distinction: the earlier sampler provides actual tables and SQL statements that match the described answer examples. It is **not** substituted for the absent exact v2 candidate context when judging what the solver was asked to do.

Environment and detailed outputs are in evidence/SQL_INSTANCE_CHECKS.json. Review tools do not import submitted worker or evaluator programs. There are no such programs in this collection archive.

## 2. What the score says

| Primary outcome | Conventional | Protocol |
|---|---:|---:|
| Families passing under retained keys | 14/16 | 14/16 |
| Eligible semantic answers | 19/19 | 19/19 |
| SQL case verdicts matching keys | 24/26 | 24/26 |

Both arms miss C03-03 and C05-01 according to the supplied scoring record. The seven meaning-unresolved semantic items and one assertion item remain outside decisive primary accuracy. The supplied ambiguity adjudication gives A05 partial credit in both arms for treating an explicitly conditional complex-multiplication reading as supported. No new linguistic score is installed here.

The case variants are related within families; the 19+26 item tally is not 45 independent treatment-effect trials. The 32 saved responses are not a sample across independently verified model implementations.

## 3. The observed extra output

The raw Markdown outputs contain:

| Measurement | Conventional | Protocol |
|---|---:|---:|
| UTF-8 bytes | 56,800 | 117,158 |
| Unicode characters | 56,556 | 116,678 |
| Whitespace-separated words | 7,703 | 16,738 |

Protocol raw bytes are 2.06264 times conventional bytes. Every one of the 16 protocol responses is longer than its conventional partner; the median paired byte ratio is 2.04827.

This includes headings, repeated protocol explanations, metadata, code blocks, and formatting. It is not a token, latency, monetary-cost, hidden-computation, or human-reading-time estimate. Those quantities are not supplied. More explicit prose could help a reader audit or reuse an answer, but that benefit was not measured by this pilot.

## 4. The two 'misses' are scope disagreements, not failed calculations

### C03-03: distinct values versus repeated occurrences

On the supplied rows (P,5), (Q,8), SUM(units) and SUM(DISTINCT units) both equal 13. Both candidate arms explicitly state this.

On the legal alternative (P,5), (Q,5), they give 10 and 5. The ordinary raw answer supplies precisely that counterexample. The protocol answer also distinguishes instance agreement from schema-wide equivalence and deliberately chooses the wider scope.

Thus both statements are true:

- ACCEPT for the given two-row table.
- REJECT for all schema-admitted tables.

### C05-01: local tray IDs versus full identity

On the all-L supplied tables, joining on tray and joining on (bench,tray) return the same two rows. Both arms say so.

If L and R reuse tray 1, joining on tray alone introduces cross-bench matches. The alternative counterexample is legal and the supplied calculations are correct.

Again, instance acceptance and schema-wide rejection are compatible claims.

### Why the key needs a scope annotation

The earlier v1 interface explicitly says 'at a scope you can justify', allows REJECT with a distinguishing dataset, and warns that sample agreement is not a theorem for all databases. The C03 protocol answer quotes substantially that instruction and states that the two readings diverge. Exact v2 packet bytes and the later parent dispatch instructions are absent here.

Allowing a finite-scope ACCEPT does not itself make a schema-scope REJECT wrong. A required instance-only target must actually be supplied. Conversely, if the actual dispatched task unequivocally required a per-instance label, these are valid labels marked wrong for answering a different task. That remains a communication/target failure, not an arithmetic one.

Preserve the frozen 14/16 report; do not silently rescore to 16/16, and do not rewrite the candidate answers. Add an explicit scope-dispute annotation. A future task should either fix the quantified claim or ask separately for instance equality and broader equivalence. A claim should be recorded as (statement, domain, quantifier, evidence, verdict), not just ACCEPT/REJECT.

## 5. Experimental provenance is incomplete in this delivery

The collection includes ONE_WINDOW_DISPATCH.md, which replaces the 32-window route with a separate gold-free candidate workspace and a parent prompt. It explicitly mentions a residual sibling-protocol glob risk and points to LIMITS.md outside this package.

A one-window orchestrator can potentially provide suitable independent contexts; its window count alone neither establishes nor refutes isolation. What matters is the content inherited by each candidate, actual accessible files/tools, visibility of sibling packets and answers, and whether the conventional arm could read the AD protocol.

Absent here:

- exact v2 task, arm instruction, output-schema, and protocol files as actually delivered;
- PARENT_PROMPT.md and LIMITS.md for the actual candidate kit;
- original candidate/subagent transcripts and tool-call logs;
- enforcement details for isolation and candidate context inheritance;
- actual model settings, numeric resource limits, tokens, and timing.

The visible model label is self-reported as 'Cursor Grok 4.6' in all 32 sidecars. A Boolean saying settings were recorded does not supply the values. The evaluator is also labeled with that model. An independent review can check mathematical content; it cannot reconstruct unavailable provider or session records.

EXECUTION_PROFILE.json is explicitly a historical precollection snapshot. Its NOT_RUN status does not mean the collection is empty. README.md is likewise a precollection instruction sheet, whereas DISPATCH_LOG.json and SCORING_REPORT.md describe the received answers. Do not conflate the document stages.

## 6. Secondary prose checks — not changes to primary scoring

The primary tally is not an audit of every sentence. Three secondary details are recorded separately:

1. The conventional C03 response says there are 34 multiset tables of sizes 0 through 3 over four row values. There are 35 including the empty table. Its main arithmetic and case verdict are unaffected.
2. The protocol C02 response reports 336,840 instances while describing all tables with up to three rows, four room-key values, and twenty stay-row values. The corresponding ordered-table count is 715,785; the bag count is 61,985. The reported number equals an ordered enumeration with only three left-table key values and twenty right-table row values. This is a count/description mismatch requiring the actual generator or execution log, not grounds to invent a hidden implementation or allege fabricated tests. Its general join-preservation argument remains separately checkable.
3. The conventional C08 introduction says that grouping preserves the line bag 'exactly when' keys are unique and never NULL. A table with the single row (NULL,4) is an explicit instance where the original and grouped query agree. NOT NULL is sufficient in the stated schema proof, not necessary for every instance. The four named C08 verdicts remain correct.

These examples appear on both arms. They are not a post-hoc win for either arm. Detailed fact checking and reuse quality would require their own prospective scoring rule.

## 7. Interpretation for the AD project

The incremental frozen intervention was the v0.1 six-step protocol on top of competent baseline instructions, strongly guided tasks, and a common output schema. It did not test the later scope key, explicit inspection-depth policy, transport gate, or the recovered core unit implementations.

The observed result is: no primary-score advantage, much more raw output, and shared scope conflicts. This does not refute the mathematical preservation criteria. It does not establish that the extra prose helps readers or that operational reuse will be faster.

For the next version, the most concrete design lesson is a scoped claim that can be reused—not mandatory narration of six steps for every elementary answer. The family can say both 'these outputs agree now' and 'this substitution is not valid on every admitted input'. Those statements should coexist in one compact record.

Do not rerun the 32 exposed packets merely to obtain a more favorable result. Retain this as development evidence. When available, attach the existing dispatch materials to resolve provenance and scope. If they were not captured, say so rather than generating retrospective evidence. New protocol features belong to a new version and later, independently specified tasks.

## Reproduction

Run from this package root:

```sh
python -B tools/review_collection.py --collection input/pilot_collection_v2.zip --earlier-families earlier_source --output fresh_evidence
```

This generates fresh artifact checks and mathematical comparisons. It does not repeat the candidate experiment or reconstruct its missing process records.
