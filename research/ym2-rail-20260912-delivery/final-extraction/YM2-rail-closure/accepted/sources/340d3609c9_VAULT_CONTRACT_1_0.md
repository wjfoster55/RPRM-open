# Vault Contract 1.0

Contract identifier: `RPRM_VAULT_CONTRACT/1`

Status: **normative candidate; unexecuted and not Vaulted.**

This contract defines the `+1` receiver-and-authority transaction in the RPRM
Vault Process package. It does not grant authority and is not satisfied by a
document that merely says "Vaulted."

## 1. Scoped subject

The subject of a transaction is

```text
Vault_(L,d,R)(artifact_version)
```

with an exact artifact identifier, version, SHA-256 digest, declared future
language `L`, tested causal depth `d` when applicable, and actual downstream
receiver `R`. The transaction also freezes:

- objective, scope, non-goals, assumptions, observables, equivalence rule, and
  resource bounds;
- proportionality level and permitted ceremony;
- source lineage and compatible source versions;
- promised receiver interface and frozen downstream continuation;
- runtime dependencies and separately declared Archive references;
- recursion node, lineage, finite budget, and decreasing parent budget;
- optional child composition identity and parent-level seam obligation;
- side-effect and authority seams;
- declared reopen conditions.

Changing any material member before commit creates a different transaction.
Changing it after a result reopens evaluation and cannot repair the old
transaction in place.

## 2. Parties and separation

The contract distinguishes:

- **Producer:** creates the exact Shadow candidate and interface promise.
- **Challenger/verifier:** runs named checks without silently repairing the
  producer artifact.
- **Receiver:** the real downstream consumer; it gets only the exact artifact,
  promised interface, frozen continuation, and context allowed by the contract.
- **Decision authority:** owns the consequence of adoption.
- **Vault registrar:** validates the gate, applies one Flick, and atomically
  retains the receipt.

One implementation may automate more than one role only when the frame permits
it and the resulting independence limit is explicit. The producer cannot
replace the real receiver by self-report. A Leap proposer cannot grade or
Vault its own Leap.

## 3. Precondition predicate

Let:

```text
C  = exact artifact has internal Closure for L and d
R  = actual receiver accepted through only the promised interface
S0 = real shared-seam defect count is exactly zero
D0 = successor defect count over L through d is exactly zero
A0 = global unique-destination accounting defect is exactly zero
X  = every claimed check actually executed on this exact artifact and points to evidence
N  = a credible frozen negative probe ran and was detected
I  = replay is idempotent and the pending authority transaction is unique
M  = semantic validation passed independently of byte-identity validation
P  = local authority, safety, irreversibility, and side-effect gates authorize adoption
```

The Vault gate is the conjunction

```text
G = C and R and S0 and D0 and A0 and X and N and I and M and P
```

Every term is required. There is no weighted score and no average that can
offset a false term. `D0` is indexed by `L`, `d`, the candidate state key, and
the observable rule. It does not imply a zero defect outside that frame.

## 4. Required check records

Each non-null check record has exactly:

```text
executed: true
passed: true
artifact_sha256: sha256:<64 lowercase hexadecimal digits>
evidence_ref: <nonempty immutable or content-addressed reference>
defect_count: 0
```

The receipt requires separate records for:

- `closure`;
- `receiver`;
- `seam`;
- `successor`;
- `global` accounting;
- `negative_probe`;
- `replay` / idempotence;
- `semantic` validation; and
- `byte_identity` validation.

`parent_seam` is also required as a field. It is `null` only when there is no
child-to-parent composition in the declared frame. When a closed child is used
to close a parent, `parent_seam` MUST be a newly executed passing check; child
Closure alone cannot close the parent.

All non-null `artifact_sha256` values MUST equal the subject artifact digest.
The receiver's artifact version and digest MUST also equal the subject.
JSON Schema validates the record shape; the semantic validator enforces these
cross-field equalities and the real evidence relations.

### Executed-check rule

A check can enter a Vault receipt only if it ran on the exact artifact version,
captured its observed result, and points to that evidence. Historical or
inherited evidence may be listed in lineage, but it cannot be relabeled as a
new execution. An asserted-but-unrun check is `unrun_check_claim`, contributes
a global defect, and blocks `G`.

A verifier that modifies the subject produces `verifier_modified_subject`.
The modified bytes are a new candidate and all affected checks must rerun.

## 5. Real receiver gate

The receiver record MUST state:

```text
kind: real_downstream
receiver_id
context_contract
promised_interface
frozen continuation
artifact version and digest
used_only_promised_interface: true
undeclared_history_used: false
accepted: true
evidence_ref
```

Acceptance means the receiver natively succeeded under the frozen downstream
observable. These substitutions are invalid:

- producer self-test for receiver use;
- a hypothetical receiver or producer-authored acceptance bit;
- success after reading undeclared producer history;
- success on a repaired or different artifact version;
- isolated component success for the real composed seam;
- a named receiver that did not execute the continuation.

Any substitution yields `receiver_not_real`, `receiver_failure`,
`undeclared_history_dependency`, or `artifact_version_mismatch` and blocks the
Flick.

## 6. Unique-destination accounting contract

Every material requirement, input, source, assumption, constraint, decision,
result, dependency, defect, side effect, authority change, receipt identity,
and shared seam has an `item_id` and one accounting entry.

For `divisibility: indivisible`:

```text
debit = 1
exactly one destination has typed_credit = 1
consumption_count = 1
balanced = true
```

For `divisibility: divisible`, destination credits use exact integer units,
sum to the debit exactly once, and each subcredit has one typed destination.
The consumption count reflects the declared unit semantics and may not be used
to hide duplication.

The accounting validator, beyond JSON Schema, MUST enforce:

1. unique `item_id` values;
2. exactly one entry for every material item;
3. exact credit/debit equality;
4. the indivisible one-credit/one-consumption rule;
5. no duplicate destination for the same typed subcredit;
6. a shared seam event identifier appears once across producer and receiver
   endpoint descriptions;
7. one and only one authority-change entry for the Flick;
8. one and only one receipt-identity entry for this `vault_id`; and
9. `global_defect = 0` only after all preceding checks pass.

An explicit destination may be `accepted_output`, `archive`, `deferred`,
`rejected`, `residual_defect`, `rollback`, or another frame-defined type.
Naming a destination does not make a blocking defect non-blocking.

## 7. Atomic commit

The registrar performs the following logical transaction:

```text
1. lock the candidate version, authority pointer, transaction_id, and receipt destination
2. verify exact candidate bytes and all semantic gate terms G without mutation
3. construct the receipt preimage with receipt_digest omitted
4. canonicalize and compute receipt_digest
5. compare-and-set Authority from the declared prior pointer to artifact_version
6. append exactly one immutable receipt under vault_id
7. commit both writes, or retain neither
8. verify the committed authority pointer and exact stored receipt bytes
```

Steps 5 and 6 are one atomic Flick/receipt transaction. A receipt without its
authority change is `orphan_receipt`; an authority change without its receipt
is `unreceipted_flick`. Either condition rolls back or leaves a blocking fault,
never a success report.

The `transaction_id` is an idempotency key. Replaying a completed transaction
with the same subject and frame returns the existing `vault_id` and digest and
applies no new accounting credit or authority change. Reusing the identifier
for different bytes or a different frame is `transaction_identity_collision`
and is rejected.

No preview, dry run, proposed receipt, or successful preflight may be reported
as the commit.

## 8. Canonical serialization and digest

The serialization identifier is

```text
canonical-json-utf8-compact-sorted-v1
```

It means:

- JSON object keys sorted lexicographically at every level;
- UTF-8 encoding;
- compact separators `,` and `:` with no insignificant whitespace;
- JSON-standard string escaping;
- arrays retained in their semantically declared order;
- no byte-order mark; and
- no terminal linefeed.

`receipt_digest` is `sha256:` followed by the lowercase SHA-256 of the
canonical receipt object with the `receipt_digest` member omitted. The stored
receipt is the full canonical object including that digest.

Two checks remain separate:

1. **Byte identity:** the stored bytes exactly match the declared canonical
   serialization and digest calculation.
2. **Semantic validation:** fields, status relations, check targets, receiver
   isolation, accounting equations, lineage, and authority event satisfy this
   contract.

A matching hash does not imply semantic validity. Semantically valid JSON
serialized with different allowed source whitespace is not the exact canonical
receipt byte stream.

## 9. Receipt fields and invariants

The machine contract is
`../schemas/rprm-vault-receipt-1.schema.json`. Its top-level fields have these
roles:

| Field | Contract role |
| --- | --- |
| `schema_version` | fixed value `rprm-vault-receipt/1` |
| `vault_id` | immutable identity of this one Vault transaction |
| `canonicalization` | exact byte contract above |
| `artifact` | exact identifier, version, and SHA-256 subject |
| `frame` | objective, `L`, `d`, scope, assumptions, observables, equivalence, bounds, proportionality, dependency boundary, recursion boundary, optional parent composition, and declared reopen conditions |
| `receiver` | actual downstream receiver, allowed context, interface, continuation, exact subject, result, and evidence |
| `source_lineage` | typed provenance entries; mirrors do not become independent sources |
| `checks` | executed passing records for every gate coordinate |
| `accounting` | all unique destinations, shared seams, and typed global zero |
| `authority_change` | exactly one `flick`, `shadow` to `promoted`, applied once |
| `status_axes` | independent work, evidence, authority, and Vault statuses |
| `prior_vault_id` / `prior_receipt_digest` | both null for first Vault; both non-null for Revault |
| `reopen_triggers` | observed immutable trigger objects; empty for an initial Vault and nonempty for a Revault |
| `residual_defects` | visible, scoped, non-blocking limits only |
| `receipt_digest` | digest of the canonical preimage |

The status axes of a successful first Vault are `complete`, the evidence grade
actually earned, `promoted`, and `vaulted`. For Revault they are the same except
`vault_status: revaulted`. Neither operation changes the evidence grade.

## 10. Immutability, reopening, and Revault

Receipts are append-only. Reopening writes a separate trigger record that
names the old `vault_id`, old receipt digest, smallest witness, classification
of the new evidence, and affected scope. It cannot alter any old field.

An affecting event is classified as `superseding`, `narrowing`,
`contradicting`, `supplementing`, or `outside_frame`. The first four reopen the
smallest Vault only when they affect its declared frame. `outside_frame` starts
separate work and does not retroactively falsify the old scoped receipt.

A Revault:

1. creates a distinct artifact version in Shadow;
2. cites exactly one `prior_vault_id` and `prior_receipt_digest`;
3. reruns every applicable check on the new exact bytes;
4. repeats the real receiver gate;
5. performs a new atomic Flick with a new transaction identity;
6. appends a new receipt; and
7. marks the prior version superseded only in the current authority/status
   index, without rewriting its receipt.

Each observed trigger object preserves `witness_id`, the witness description,
`affected_vault_id`, and `prior_receipt_digest`. The declared future conditions
that should cause reopening remain separately frozen in
`frame.reopen_conditions`.

If the new candidate fails, the old receipt remains immutable and the current
reopened defect remains visible. A failed Revault does not silently restore the
old scope.

## 11. Failure output

A failed gate returns no successful receipt and no Flick. It retains at least:

```text
failure kind and location
smallest concrete witness
artifact identity/version/digest
affected scope and receiver
executed evidence references
authority and side effects actually observed
next disposition or resource stop
```

Primary failure kinds include `internal_defect`, `receiver_not_real`,
`receiver_failure`, `undeclared_history_dependency`, `seam_defect`,
`successor_defect`, `global_accounting_defect`, `unrun_check_claim`,
`negative_probe_missing`, `hash_used_as_semantic_proof`,
`shadow_authority_violation`, `archive_runtime_dependency`, `double_flick`,
`orphan_receipt`, `unreceipted_flick`, `mutable_receipt`,
`receipt_lineage_break`, and `parent_seam_unchecked`.

## 12. Current evidence boundary

This contract and its schemas define a candidate. No successful Vault receipt
for the process synthesis is claimed here. Design, schema validation, or a
matching digest alone cannot establish receiver completeness, portability, or
universal fitness.
