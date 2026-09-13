# RPRM Vault Process 1.0

Package identifier: `RPRM_VAULT_PROCESS_1_0`

Status: **Shadow candidate; design and conformance target only. This synthesis
has not been behaviorally validated or Vaulted.**

This document is the normative register of a candidate process package. It
does not replace either frozen source:

- `CLOSURE_LOOP.md`, SHA-256
  `fbf1e398d506934d46e70e227ed17142ee09878bd045432a948ce6db4668c2fe`;
- `RPRM_PORTABLE_PROCESS.md`, SHA-256
  `ff67e4e32c81ccbf4aeddee3e0179d77784e5ca28b0ae8ff8bbfc8c0dfe004b2`.

Those hashes identify exact source bytes. They do not establish semantic
validity. Source authorship is not inferred. The frozen copies and the
clause-level reconciliation are separate lineage artifacts.

## 1. Authority, scope, and language

Repository-local authority, system and developer instructions, explicit user
instructions, legal and safety duties, and authoritative domain methods
outrank this process. A conflict is preserved as a typed defect or limit; it
is never averaged away. This process organizes work. It does not grant
authority, replace domain evidence, or make a result true forever.

Normative words have their ordinary specification meanings: **MUST** is
required when applicable, **SHOULD** is the default unless a recorded reason
justifies deviation, and **MAY** is optional.

Two registers MUST remain distinct:

1. The public guide uses ordinary, audience-appropriate language and only the
   amount of process visible enough to help its receiver.
2. This normative kernel records frames, gates, statuses, evidence, defects,
   lineage, and receipts precisely.

A trivial deliverable MUST NOT acquire Vault or RPRM vocabulary merely because
the worker used this kernel. Ceremony that changes no decision and protects no
outcome is a defect of proportionality.

## 2. The core 3+1 architecture

The candidate package has three process layers and one transaction:

1. **Human-facing Closure Loop.** Proportionate instructions that a person can
   use without prior RPRM knowledge.
2. **Normative Portable Kernel.** Formal obligations, lanes, checks, status
   axes, recursion bounds, and reopening rules.
3. **Frozen Conformance Profile.** Immutable cases, mutations, observables,
   resource bounds, and grading rules applied to immutable candidate bytes.
4. **+1 Vault Contract and Receipt.** A real receiver handoff followed by one
   atomic authority change and an immutable scoped receipt.

The `+1` is not a fourth advice document. Without its actual receiver event,
gate evidence, Flick, and receipt, the other three remain a process candidate
and MUST NOT be called Vaulted.

## 3. Scale and frame

Use the lightest level that protects the outcome:

- **Level 0 / direct:** low-risk, reversible, one-step work; answer and sanity
  check without process vocabulary.
- **Level 1 / light:** small multi-step work; state the important success
  condition or assumption and check one meaningful failure mode.
- **Level 2 / full:** complex, durable, or cross-component work; freeze the
  frame, seams, negative check, and receipt.
- **Level 3 / critical:** high-stakes, irreversible, externally visible,
  security-sensitive, or authority-changing work; add current authoritative
  evidence, containment or rollback, explicit authorization, independent
  verification where feasible, and a durable audit.

Cost of being wrong, not apparent effort, selects the level. Under pressure,
retain an actual-state check and one tripwire first; any deferred record MUST
be labeled as backfilled.

Before forming a nontrivial candidate, freeze or explicitly mark open:

```text
objective and decision owner
artifact identity and version
actual downstream receiver and measurable done condition
future language / scope / causal depth / non-goals / bounds
observable and equivalence rule, including stochastic tolerance if relevant
authoritative sources, observations, assumptions, and lineage
input, output, dependency, shared-state, side-effect, and authority seams
positive check, credible negative probe, and reopen triggers
resource and recursion bounds
```

Hard constraints are gates. An unresolved hard constraint cannot be converted
to an assumption by prose.

## 4. Four lanes and four independent status axes

The logical lanes are:

- **Active:** the smallest unresolved item and the evidence it presently
  needs.
- **Shadow:** reversible drafts, simulations, hypotheses, Leaps, comparisons,
  and candidates. Shadow is structurally unable to mutate Authority.
- **Authority:** adopted interfaces, decisions, facts-as-relied-upon, and
  approved actions. Authority is permission or live state, not truth.
- **Archive:** prior evidence, receipts, rejected candidates, and lower
  history. It is available for audit but MUST NOT be a silent runtime
  dependency.

Each artifact records four independent axes exactly:

```text
work_status:
  complete | partial | open | blocked | reopened

evidence_grade:
  sanity_checked | tested_conformance | bounded_exhaustive | formally_proved

authority_status:
  shadow | promoted | superseded

vault_status:
  candidate | gate_pending | vaulted | reopened | revaulted | rejected
```

Promotion and Vaulting MUST NOT raise `evidence_grade`. Reopening changes the
current work and Vault projections; it does not erase the evidence grade or
scope stated by an earlier immutable receipt.

The lifecycle fixes the other three axis projections while leaving
`evidence_grade` independently earned:

| Lifecycle state | `work_status` | `authority_status` | `vault_status` |
| --- | --- | --- | --- |
| `unframed`, `framed` | `open` | `shadow` | `candidate` |
| `shadow_candidate`, `challenged` | `partial` | `shadow` | `gate_pending` |
| `closed`, `receiver_accepted` | `complete` | `shadow` | `gate_pending` |
| `vaulted` | `complete` | `promoted` | `vaulted` |
| `reopened` | `reopened` | `promoted` | `reopened` |
| `revault_candidate` | `open` | `shadow` | `gate_pending` |
| `revaulted` | `complete` | `promoted` | `revaulted` |
| `superseded` | `complete` | `superseded` | predecessor's `vaulted` or `revaulted` value |
| `rejected` | `blocked` | `shadow` | `rejected` |

`reopened` retains the historical authority projection until a new authority
decision; it does not pretend the affected scope is still closed. Beginning a
Revault creates a new Shadow candidate while the predecessor receipt remains
immutable.

## 5. Closure, acceptance, Flick, and Vault

### 5.1 Closure

A **Closure** is a lower-level artifact internally sufficient for a declared
downstream use under declared assumptions, scope, observables, and bounds.
Closure is indexed by the declared future language. It is not completion for
all future uses.

For deterministic work, equivalence can require exact output and successor
behavior. Stochastic, measured, or generative work MUST instead freeze a
tolerance, allowed outcome set, distributional property, or semantic rubric.
Merely describing uncertainty is not a check.

### 5.2 Receiver acceptance

**Receiver acceptance** occurs only when an actual declared downstream
consumer receives the exact artifact version and promised interface, is denied
undeclared lower history, executes a frozen downstream continuation, and
succeeds under its declared observable. A producer self-test, a producer-side
`accepted` flag, a hypothetical receiver, or another read of the producer
context is not receiver acceptance.

### 5.3 Flick

A **Flick** is one atomic authority change that adopts a closed,
receiver-accepted candidate. It has one transaction identity and MUST be
idempotent: replay either returns the existing result without a second change
or is rejected. A preview is not a Flick. Shadow MUST NOT perform a Flick.

### 5.4 Vault

To **Vault** an artifact is to seal its current implementation, prove its
declared receiver handoff, perform one atomic authority change, and retain an
immutable scoped receipt so the result can be used as one unit downstream.

Use the scoped notation

```text
Vault_(L,d,R)(artifact_version)
```

where `L` is the declared future language and scope, `d` is the tested causal
depth when relevant (otherwise explicitly not applicable), and `R` is the
actual receiver. Vaulting requires, in one composite transaction:

1. internal Closure of the exact artifact version;
2. actual receiver acceptance through only the promised interface;
3. seam defect count `0` at the real producer/receiver handoff;
4. successor defect count `0` over `L` through `d` under the frozen observable;
5. global accounting defect `0`;
6. exactly one Flick; and
7. exactly one immutable Vault receipt for the transaction.

A Vault is accepted only for its receiver, future language, causal depth,
assumptions, evidence grade, and version. It is neither "true forever" nor a
synonym for "done."

## 6. Vault vocabulary

- **Vault candidate:** an exact, versioned Shadow artifact with a frozen frame
  and declared receiver. It has no authority merely because it is a candidate.
- **Vault gate:** the conjunction of the seven requirements in section 5.4
  plus the executed-check and accounting rules below.
- **Vault receipt:** the immutable, canonical, hash-addressed claim record
  created by a successful Vault transaction. Its existence is not proof; its
  cited evidence supplies the checks.
- **Vaulted:** the state of an artifact version whose Vault gate passed and
  whose one Flick and receipt were atomically retained.
- **Reopened:** a current status applied when an in-frame counterexample,
  expired assumption/evidence, changed authority, scope expansion, or seam
  failure affects the smallest relevant Vault. The old receipt remains intact.
- **Revaulted:** the state of a new artifact version that independently passed
  the current Vault gate, cites its predecessor receipt, and received a new
  Flick and new receipt.
- **Superseded:** a prior version no longer selected by current authority
  because a named accepted successor replaced it. Its receipt and historical
  scoped claim remain immutable and auditable.

## 7. Process operations and their distinct roles

For nontrivial work, the operation order is:

```text
Notice
Leap (optional)
Ground
Fold
FutureTest
Five
Refine / Refold
Receive
Vault
```

`Leap` MUST occur before the Fold it informs and MUST remain Shadow. If there
is no Leap, grounding applies to the supplied model language. The ordinary
select/map, activate/register, compose, retain, and stop duties of the source
kernels remain in force around these named operations.

| Operation | State-machine role | Permitted intervention | Required check | Typed failure signature |
| --- | --- | --- | --- | --- |
| Notice | frame the smallest pressure and actual state | read current state and declare a future-relevant missing distinction | observed state and authority are current | `unframed_work` or `assumed_actual_state` |
| Leap | propose a language extension | add a candidate coordinate, object, operator, equivalence, frame, correspondence, or discriminating experiment in Shadow | proposal was absent from the supplied language and cannot write Authority | `leap_not_novel`, `shadow_authority_violation` |
| Ground | connect a Leap or supplied term to an observable intervention | derive, measure, or operationalize the candidate without grading it by target labels | independent challenge can read its construction and falsifier | `ungrounded_leap` or `target_leakage` |
| Fold | merge cases for declared future use | apply the frozen equivalence rule | all allowed observables through declared bounds are preserved to stated grade | `reopened_merge` |
| FutureTest | seek failure rather than confirmation alone | positive, negative, boundary, mutation, replay, and real-seam probes in proportion to scope | shortest/earliest claims name the search order that supports them | `undetected_mutation`, `unsupported_shortest_claim` |
| Five | localize a failure backward | trace to the earliest supported missing distinction or seam | preserved witness changes at the named location and not before it | `mislocalized_defect` |
| Refine / Refold | repair only what the witness supports | add the missing typed distinction and recompute affected work | witness closes and unaffected regression behavior remains | `speculative_overrepair` |
| Receive | test the promised handoff | fresh downstream receiver uses exact artifact and interface without undeclared history | receiver continuation passes and context contract is audited | `receiver_failure` or `undeclared_history_dependency` |
| Flick | perform the authority change | one atomic compare-and-set from Shadow candidate to promoted version | exactly one transaction identity is committed; replay is idempotent | `double_flick`, `preview_reported_as_commit` |
| Vault | bind Closure, Receive, Flick, and receipt | seal the exact artifact and append its immutable receipt atomically | every Vault-gate check actually ran and has evidence | `false_vault`, `mutable_receipt` |

Flatten is separate: it compiles a verified multi-step routine into one exposed
interface while keeping live internals inspectable. Archive is not permitted
to become a hidden part of that runtime interface.

## 8. Frozen lifecycle state machine

The state of an artifact version is one of:

```text
unframed
framed
shadow_candidate
challenged
closed
receiver_accepted
vaulted
reopened
revault_candidate
revaulted
superseded
rejected
```

Transitions not listed below are illegal. A failed guard performs no listed
transition; it retains a typed defect and the source state unless a listed
repair, reopen, or reject event follows.

| Event | From | To | Complete guard |
| --- | --- | --- | --- |
| `frame` | `unframed` | `framed` | artifact/version, objective, decision owner, real receiver, future language, observables/equivalence, scope/bounds, assumptions, seams, falsifier, and resource bound are declared |
| `form_candidate` | `framed` | `shadow_candidate` | exact candidate bytes are frozen in Shadow with lineage; no Authority mutation occurred |
| `challenge` | `shadow_candidate` | `challenged` | applicable positive, negative, boundary, replay, accounting, and semantic checks actually ran and evidence references were captured |
| `refine` | `challenged` | `shadow_candidate` or `revault_candidate` | a preserved witness supports the smallest typed repair; a new artifact version is frozen before rechecking, retaining whether it has a predecessor Vault |
| `close` | `challenged` | `closed` | internal done condition and declared observables pass; no blocking defect or unverified load-bearing assumption remains; successor coverage and evidence grade are stated honestly |
| `accept_receiver` | `closed` | `receiver_accepted` | actual declared receiver uses only exact artifact plus promised interface and frozen continuation; accepted result and context audit are captured |
| `receiver_repair` | `closed` | `shadow_candidate` or `revault_candidate` | receiver failed; smallest seam or interface witness is preserved and a new candidate version is created, retaining whether it has a predecessor Vault |
| `vault` | `receiver_accepted` | `vaulted` | no predecessor Vault; all section 5.4 gates pass; one atomic Flick and one immutable receipt commit together |
| `reopen` | `vaulted` or `revaulted` | `reopened` | a named in-frame counterexample, changed/expired assumption or authority, larger future language, or real seam failure affects this smallest Vault; witness and trigger are appended outside the old receipt |
| `begin_revault` | `reopened` | `revault_candidate` | a distinct new version cites exactly one prior immutable receipt and starts in Shadow; this lineage edge does not rewrite the parent receipt |
| `challenge` | `revault_candidate` | `challenged` | the full current profile ran against the new exact version; inherited results are not represented as newly executed checks |
| `revault` | `receiver_accepted` | `revaulted` | exactly one predecessor receipt is linked; the new version independently satisfies every Vault gate; a new Flick and new receipt commit atomically |
| `supersede` | `vaulted` or `revaulted` | `superseded` | a named accepted successor receipt exists; only the current-authority/status index changes, never the old receipt |
| `reject` | `unframed`, `framed`, `shadow_candidate`, `challenged`, `closed`, `receiver_accepted`, `reopened`, or `revault_candidate` | `rejected` | proper authority records a reason, or a hard constraint/resource boundary makes the framed candidate inadmissible; rejection is not evidence of falsehood outside scope |

`rejected` and `superseded` are terminal for that artifact version. A new
candidate requires a new version identity. There is no direct transition from
`closed` to `vaulted`, from `shadow_candidate` to any Authority state, or from
`reopened` back to `vaulted` without a new version and receiver test.

Revault is an atomic lineage event: the new version changes from
`receiver_accepted` to `revaulted`, the current authority/status index records
the predecessor as superseded, and the predecessor receipt remains unchanged.
If the authority write, predecessor link, or new receipt append fails, no new
authority change is retained. The historical predecessor receipt is never a
write target. A prior `vaulted` or `revaulted` version may also be projected to
the terminal `superseded` state when its named successor is accepted.

## 9. Vault gate and failure signatures

The gate MUST reject, without a Flick, when any of these conditions holds:

| Gate coordinate | Passing evidence | Failure signature |
| --- | --- | --- |
| exact subject | artifact identifier, version, and SHA-256 match every check target | `artifact_version_mismatch` |
| internal Closure | declared done condition and internal checks pass | `internal_defect` |
| real receiver | named receiver result and audited context contract pass | `receiver_not_real` or `receiver_failure` |
| interface isolation | receiver read only promised interface and allowed context | `undeclared_history_dependency` |
| seam zero | one real handoff event has defect count zero | `seam_defect` |
| successor zero | no defect found over declared `L` through `d`, with coverage basis | `successor_defect` |
| global zero | all material items balance at one destination | `global_accounting_defect` |
| negative probe | a credible frozen break is detected | `negative_probe_missing` |
| executed checks | each receipt claim has execution, result, and evidence on the exact subject | `unrun_check_claim` |
| semantic verification | semantic validator passes independently of byte identity | `hash_used_as_semantic_proof` |
| lane separation | no Shadow or Archive path mutated Authority | `shadow_authority_violation` or `archive_runtime_dependency` |
| atomicity/idempotence | one Flick and receipt, replay applies no second change | `double_flick` or `orphan_receipt` |
| lineage | compatible source and predecessor versions remain distinct | `source_version_collapse` or `receipt_lineage_break` |

Zero is always typed and scoped. `successor_defect = 0` on a bounded future
language is not zero on an enlarged language. A finite test is not formal
proof. A resource stop is not a pass.

## 10. Unique-destination accounting

Every material requirement, input, source, assumption, constraint, decision,
result, dependency, defect, side effect, authority change, shared seam, and
receipt identity MUST have exactly one disposition.

For an indivisible item:

```text
one debit = one destination credit = one consumption
```

For a divisible item, typed subcredits MUST sum exactly once to its debit, and
each subcredit has one destination. A disposition such as `deferred`,
`rejected`, `residual_defect`, or `not_applicable` is allowed only when typed
and explicit; it is not disappearance.

A shared seam has one event identifier and one conserved accounting entry even
when producer and receiver give its endpoints different meanings. Publishing
the same seam twice is rejected or resolves idempotently to that one entry.
Source mirrors with identical lineage are one source contribution, not
independent corroboration.

The accounting validator MUST reject duplicate item identities, duplicate
seam credits, zero destinations, multiple destinations for an indivisible
item, unconsumed indivisible debits, and divisible totals that fail exact
arithmetic. Floating approximate balance is not sufficient where exact units
are declared.

## 11. Executed-check truthfulness

A Vault receipt MAY claim a check only when all three facts are present:

1. the named check executed against the exact artifact identifier, version,
   and digest being Vaulted;
2. its observed result was captured without verifier repair of the producer
   artifact; and
3. the receipt points to an immutable or content-addressed evidence record.

An asserted-but-unrun check is itself `unrun_check_claim`, contributes a
nonzero global defect, and blocks Vaulting. An inherited check may be cited as
historical context but MUST NOT be marked executed for a changed version.
Verifier mutation produces `verifier_modified_subject` and invalidates that
check. Byte equality and semantic validation MUST remain separate claims.

## 12. Reopening and revaulting

Classify new evidence as `superseding`, `narrowing`, `contradicting`,
`supplementing`, or `outside_frame`. Only an affecting in-frame event reopens
the smallest relevant Vault. Outside-frame evidence leaves the old scoped
receipt intact and starts separate work if pursued.

Reopening appends a trigger record containing the prior `vault_id`, immutable
receipt digest, witness, affected scope, and new status. It MUST NOT edit,
replace, or silently reinterpret the prior receipt. Revaulting MUST use a new
artifact version, new receiver result, new transaction identity, new receipt,
and an explicit predecessor link. A revault may narrow, expand, or otherwise
change scope, but it MUST state that difference and rerun every applicable
check on the new exact version.

## 13. Receipts, retention, and stopping

The normative receipt contract is in `VAULT_CONTRACT_1_0.md`; its machine
shape is in `rprm-vault-receipt-1.schema.json`. Canonical byte identity and
schema/semantic conformance are separate checks. The receipt retains enough
lineage and evidence references to reproduce, audit, or reopen the scoped
claim, while the receiver interface remains usable without routine access to
lower history.

Long-running work SHOULD maintain separate living `STATE`, `CLAIMS`, and
append-only `RECEIPTS` records. Guaranteed, assumed, hoped, disputed, unknown,
untested, rejected, and resource-stopped items MUST not blend.

Stop when the original acceptance criteria are met or a recorded authority,
safety, hard-constraint, or resource boundary is reached. Report the scoped
promise, residual defects, and open work; do not generate new work merely to
keep the process running.

## 14. Evidence boundary

This candidate package has not yet earned any portability classification and
is not Vaulted. Its definitions and schemas are design/conformance artifacts,
not behavioral evidence. Neither the source candidates nor this synthesis
prove universal process optimality, physical time, particles, dimensions,
cosmology, divinity, cognition, or a universal law of nature.
