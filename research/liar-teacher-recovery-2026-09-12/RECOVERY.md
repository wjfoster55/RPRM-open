# Recovered liar → teacher construction

Recovered on 12 September 2026 from original local user messages, historical research notes, and existing executable evidence.

**The remembered construction is present much more explicitly than the pasted answer suggests.** The strongest match is William's 21 August exchange: learn three liars as teachers, retain them while introducing four newcomers, form seven teachers, return to smaller groups chosen from those seven, and vacate the student/reference position so a newcomer can enter. The two-question/four-role and three-question/eight-role wording is also present in an original 13 August turn.

The passages establish what was proposed. Historical notes give specific mathematical models of several parts; an existing liar/teacher experiment tests finite instances. No single recovered artifact proves the whole expansion, replacement, reduction, and speedup procedure for arbitrary problems.

## The closest original passages

The accompanying [SELECTED-PASSAGES.md](SELECTED-PASSAGES.md) preserves the full selected user turns, their original session locations, message timestamps, and text hashes. Excerpts below are shortened; the source wording and corrections remain intact there. Calendar dates below use America/Denver. Machine-readable records retain UTC.

| Original passage | What it settles |
|---|---|
| P01–P02, 11 August | Four guards, one truth and three liars; William then asks about nonbinary/structured questions and says the questioner occupies the fourth space. |
| P03, 11 August | The corrected larger picture is “seven liars, one truth-teller, and one dead guy.” The silent/vacant position was an additional role in this version. |
| P04, 12 August | “turn the seven Liars into seven teachers” and “seven teachers and one kid,” explicitly correcting an accidental “eight teachers.” |
| P05, 12 August | Truth tellers/liars become teachers/students; three liars become teachers, the truth teller becomes the student, and the student retains the result during the return to sparse transit. |
| P06, 13 August | “three liars one truth teller with two questions” and “7 liars one truth teller 3 questions”; learn at the larger level, then bring the construction back down. The proposed reduction to one question is a research claim in this turn. |
| P07–P10, 21 August | The detailed calibration, four-newcomer expansion, reduction, student removal, and continuing teacher process. |
| P11, 6 September | Explicit recollection of the teacher/liar expansion and return as a “transfer path,” proposed “all four ways, all around the helix.” |

The decisive 21 August passage, P08, says:

> “we can gather four more liars, keep our three liars, you know, our three mentors, our three exemplars”

and later:

> “you can scale back down from eight back to three with any of those seven now. And that's how you teach different things.”

P09 then resolves the student versus empty-slot memory directly:

> “in that eighth spot where the student is, you can take the student out”

> “The one something leaves, and in that spot enters a liar.”

P10 adds that the initial three are hardest to establish; after that the teachers can handle new cases, and a larger family can force revision of the common rule. This is a richer proposal than a permanently fixed truth-teller surrounded by repeated checks.

## The written teacher/student mechanism already existed

[Amendment 0.28, “audit-to-generate role transfer”](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_NARIBRAIN_WORLD_MACHINE_RESEARCH_RUN_0_1/USER_STEERING_AMENDMENTS_0_28_AUDIT_TO_GENERATE_ROLE_TRANSFER.md:48>), internally dated 12 August, explicitly defines:

```text
Four typed ports P; one receiving/vacant port v.
TEACHERS = P minus {v}
STUDENT  = v
```

Its cycle is: the three teachers constrain the missing student port; a uniquely compatible completion fills it; that completed student carries the result while teacher details are folded; the next frontier becomes the new student; the former student can become a teacher. Lines 80–130 explicitly discuss retention, reopening, and this rotation.

**So “student” and “empty slot” were both part of the account.** Student names the receiving role; vacancy names its unfilled state. The separate nine-cell guard picture instead adds a silent center to eight live roles. These two arrangements should retain their distinct counts.

Amendment 0.28 calls itself a *typed role-transfer candidate*. Its affine relation is a concrete donor for four-port completion, with a typed adapter still required for other kinds of roles. A filled student value alone need not reconstruct the complete teacher state; a retained lineage or preimage family is required for that stronger recovery.

## The movable anchor also predates the pasted answer

[Amendment 0.29, “one anchor and seven shadows”](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_NARIBRAIN_WORLD_MACHINE_RESEARCH_RUN_0_1/USER_STEERING_AMENDMENTS_0_29_ONE_ANCHOR_SEVEN_SHADOWS.md:7>), also internally dated 12 August, explicitly starts from one truth teller, seven liars, and three questions. It represents the eight roles by three binary coordinates:

```text
000 = current anchor
001, 010, 100 = single-coordinate differences
011, 101, 110 = two-coordinate differences
111 = three-coordinate difference
```

Its three binary readouts identify an address. Its section “Shadow becomes new anchor,” lines 86–106, explicitly translates all addresses relative to a newly selected anchor using XOR. Lines 131–145 connect this to the seven shadows acting as teachers, the anchor acting as student/bearer, and rotating those assignments.

This recovers a historical mathematical model of the moving reference; it was not first introduced by the pasted reply. The note's exact cube translation and its proposed discovery/training cycle have different evidence grades. Identifying a cube address from three coordinate readouts is not, by itself, a fully specified interrogation protocol for arbitrarily behaving guards.

## A dedicated executable liar/teacher packet survives

The exact existing packet is [RPRM_LIAR_TEACHER_BOUNDARY_SYNDROME_01](<C:/github/RPRMResearch/RPRM_LIAR_TEACHER_BOUNDARY_SYNDROME_01/README.md>).

Its [NOTE.md](<C:/github/RPRMResearch/RPRM_LIAR_TEACHER_BOUNDARY_SYNDROME_01/NOTE.md:3>) makes a precise interpretation:

- The full addressed source is the reference.
- A “liar” is a lossy view: several source states can produce its answer.
- A “teacher” is that view after its map, scope, ambiguity, and dependencies have been established.
- Several teachers identify the requested state only when their joint compatible-state family has one member.

The note's “first three are expensive; later instances can be cheap” section directly preserves the bootstrap-and-reuse idea. It requires the raw source to remain reopenable and calls for renewed calibration when the carrier or common rule changes.

**Fresh replay on 12 September:** the existing verifier exited successfully and reported **62 passing receipts, 310,462 passing assertions, zero failures**. Its code hash matches the historical RESULTS.json; the existing zip and stored-output hashes also match the recorded source pins. These are finite implementation checks, not a proof of general verifier soundness.

Useful concrete findings:

| Fixture | Recorded result, reproduced by the verifier |
|---|---|
| Eight addressed Lo Shu boards | Three particular views together still leave four possible boards. A suitable pair of views identifies one. Teacher count alone is insufficient. |
| Frozen 4×4 Sudoku clues | All three constraint families give one board; dropping one family leaves 64, 16, or 4. |
| Hamming-7 | Three check bits locate a single flipped position among seven under the declared single-error promise. The tested double-error cases defeat that decoder. |
| Extended Hamming-8 | The additional parity coordinate detects the tested double errors, but their locations remain ambiguous. This eighth coordinate has a different meaning from the eighth cube vertex. |

Replay command:

```powershell
python -I -B C:\github\RPRMResearch\RPRM_LIAR_TEACHER_BOUNDARY_SYNDROME_01\verify_liar_teacher_boundary_syndrome.py
```

The run also checks larger Hamming fixtures, a finite generating-function example, and finite Hilbert reindexings. Those are separate examples. The Hamming-15 output's zero-valued ordinary-double-miscorrection counter is not a tested zero-error claim: that enumeration is skipped for that fixture. Some illustrative hostile assertions are weaker than exhaustive tests; do not inflate the aggregate assertion count into a universal theorem.

## What the different “liars” mean

The source history contains several precise interpretations. They should remain distinguishable when reconnecting the concept.

| Historical construction | Actual mechanism | Evidence recovered here |
|---|---|---|
| Three cyclic liars + one identity report | On three answer values, three repetitions of the same registered cycle return to identity. | Written R8 argument in the [11 August involution scout](<C:/Users/bkbee/OneDrive/DOCUME~1-DESKTOP-06BJRV0-219031/ChatGPT/Quantum Research/RPRM_RETAINED_INVOLUTION_OVERLAY_AND_ZERO_DEFECT_SCOUT_0_1_SHADOW.md:604>); different from binary toggles. |
| Four reversible views I/O/M/F | Four XOR routes; any two distinct character-sign checks identify the route. | [Audit28 report](<C:/github/RPRM-foam-development/experiments/RPRM_V4_CHARACTER_MOBIUS_KEYRING_AUDIT_28/REPORT.md:12>), freeze dated 24 August; stored PASS, not rerun here. Only four of eight possible sign triples are legal. |
| One anchor + seven shadows | Three binary coordinates, nonzero difference masks, XOR recentering. | Amendment 0.29's exact coordinate construction plus candidate operational interpretation. |
| Three teachers + student | Three supplied ports constrain the fourth; the receiving role rotates. | Amendment 0.28's typed candidate, with a specified affine donor. |
| Calibrated lossy teachers | Intersect complete inverse families to identify a source or retain ambiguity. | Dedicated boundary-syndrome packet, freshly replayed here. |

The public [concepts chapter](<C:/github/RPRM-open/docs/concepts.md:103>) gives majority decoding and four binary response functions. Those examples preserve useful narrower questions, but do not contain the full original growth-and-handoff proposal.

## Recovered conclusion and remaining gap

The historically grounded account is: **establish a small set of interpretable views; let them constrain a receiving role; retain the resulting relation; add and calibrate new views; rotate or vacate the reference; use a suitable smaller panel for the next question.** All of those ingredients occur in the original discussion or contemporaneous notes.

Still unresolved in the material recovered here: a single completed general procedure proving that every proposed newcomer can be calibrated from the existing panel, that any chosen three of seven suffice, that larger-scale learning always reduces a four-way identification to one binary answer, or that the complete helix route guarantees a speedup. The sources preserve those as proposed continuations; the finite packet supplies examples and counterexamples that delimit them.

## Search and verification record

The local memory-fabric packet had 406 lexical candidates but selected unrelated material; its scoped omission search for “liars teachers” found no omitted matches. The relevant findings came from direct source searches. Fabric packet ID and snapshot are recorded in SOURCES.json; lack of retrieval from that packet is not absence from the corpus.

The native-session pass searched 978 lexical candidate files, excluded 883 subagent-source files, and parsed 95 native/user session files. Its narrow filter retained 65 distinct user-record candidates across 22 files after excluding a current-search occurrence. These included two pasted assistant-context records and one reposted external user input, which were excluded from the curated original set. No archived-session lexical hits were found. Exact neighboring turns were then reopened separately; the 11 passages delivered here were each rechecked against their original JSONL text, role, and timestamp. They are not claimed to be an exhaustive history. Copied assistant explanations were not counted as independent user statements.

Only this recovery folder and task scratch were written. Historical files and the public manuscript were left intact. No corpus ingestion, registry promotion, publication, or new research campaign was performed.
