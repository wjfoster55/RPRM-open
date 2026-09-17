# 04 â€” Coverage gaps after the synthesis pass

**Date:** 17 September 2026
**Author:** synthesis lane (fourth pass, after the three ingest lanes)
**Purpose:** record what was searched for, what was found, and what remains
unavailable. No search is claimed that was not run. Every path below was
resolved on this machine.

## 1. The ChatGPT gap â€” partially closed

The process-history lane's largest declared hole was that ChatGPT was William's
primary research partner and no local export was found. That is **half right**.
There is no platform-native raw export. There *is* a substantial, labelled,
self-describing ChatGPT corpus on disk that the earlier pass did not fully
characterise.

### 1.1 What was searched

| Search | Method | Result |
|---|---|---|
| `conversations.json` anywhere under the user profile, depth 8 | recursive filename search | **none found** |
| ChatGPT desktop app data under `AppData\Roaming` and `AppData\Local` | directory name match `*ChatGPT*` | **none found** â€” no desktop-app local store exists |
| Chat/export archives in Downloads, Documents, Desktop | recursive, extension and name filter | **found**, see 1.2 |
| `*CHATLOG*` / `*CHAT_EXPORT*` across the user profile | `dir /s /b` | **found**, see 1.2 |
| OneDrive `ChatGPT\` project tree | full recursive inventory | **found, but not conversations**, see 1.3 |

### 1.2 What exists: two real ChatGPT artifacts

**(a) `%USERPROFILE%\Downloads\RPRM_CHAT_EXPORT_FOR_GPT_2026-08-19.zip`**

A curated, fidelity-labelled export that William built on 2026-08-19 for exactly
the purpose this corpus exists for â€” handing the thread to another model. 21
entries. Its own `MANIFEST.json` declares three fidelity classes: `verbatim`,
`transcribed_visible_text`, `reconstructed_summary`.

| Entry | Bytes | Fidelity, per the package's own README |
|---|---:|---|
| `01_EXACT_PRIOR_TRANSCRIPT_2026-08-03.md` | 121,133 | **Exact visible transcript, 33 messages** |
| `01_..._2026-08-03.html` | 125,483 | same, HTML rendering |
| `02_POST_AUG03_RECONSTRUCTED_TRANSCRIPT.md` | 23,757 | **Reconstructed**, role-separated, chronological |
| `03_RECENT_VISIBLE_TURNS_TRANSCRIBED.md` | 52,864 | Manually transcribed from the live conversation; *"not claimed byte-identical"* |
| `04_CURRENT_RECEIVER_HANDOFF.md` | 9,335 | Handoff state |
| `05_SOURCE_AND_ARTIFACT_INDEX.md` | 1,979 | Index |
| `06_MESSAGE_LEDGER.jsonl` | 155,533 | Exact early messages + reconstructed later entries, each with an explicit `fidelity` field |
| `..._ALL_IN_ONE.md` | 209,827 | Concatenation |
| `supporting/` | 8 files, ~139 KB | Mathseed audit, closure loop, portable process, dimensional split protocol |

Created `2026-08-19T19:18:34Z`. `exact_prior_message_count: 33`. Exclusions
declared: hidden system/developer instructions, private chain-of-thought, tool
calls, account metadata. Every file carries a SHA-256 in the manifest.

The README states the reason for reconstruction plainly:

> "The reconstruction is necessary because the current runtime does not have a
> raw byte-for-byte export endpoint for the entire very long conversation, and
> some earlier spans are compacted/skipped in the active context. **This package
> does not pretend otherwise.**"

That last sentence is the correct evidence grade, stated by the producer, in
August, unprompted. Treat `01_...` as verbatim-grade for 33 messages, `03_...`
as transcription-grade, and `02_...` and the later ledger rows as
reconstruction-grade.

**(b) `%USERPROFILE%\Downloads\Investigate RPRM bridge families CHATLOG.txt`**

1,838,190 bytes, **279,537 words** of ChatGPT conversation. This is the single
largest ChatGPT artifact on the machine. It is also mirrored into the repository
at `research/ym2_rail_closure/accepted/sources/ba3416025c_Investigate RPRM bridge
families CHATLOG.txt` and at the parallel `ym2-rail-20260912-delivery` path,
where it is an *accepted source* for the YM2 rail-closure work.

It is the only place in the corpus where "Dark World" appears alongside the
master context guide, which is why Chapter 5 of the thesis-defence document
grades that vocabulary as abduction-lane dialect.

**Revised estimate of available ChatGPT material:** roughly 280,000 words in the
bridge-families log plus roughly 60,000 words across the August export package,
against 1,150,000 words of Codex-side William speech. So the ChatGPT lane is
**approximately 23-25% covered by volume**, concentrated in two threads, with
explicit fidelity labels. It is not zero and it is not complete.

### 1.3 The OneDrive `ChatGPT\` tree is a workspace, not an archive

`%USERPROFILE%\OneDrive\DOCUME~1-DESKTOP-06BJRV0-219031\ChatGPT\`

| Measure | Value |
|---|---|
| Project folders | **13** (Education Reforge, NARI, NARI 2, NARI-NG, NARI3, NariLounge, New project, New project 2, Quantum Research, RPRM, RPRM Alpha, RPRM Dev, RPRM-Spark) |
| Files | 267,042 |
| Size | 77.89 GiB |
| Top extensions | `.o` (77,930), no-extension (36,605), `.json` (26,850), `.bin` (19,206), `.rs` (10,212), `.md` (9,692), `.py` (9,536) |

**Correction to the process-history lane:** it reported 11.35 GiB. The tree is
77.89 GiB. The difference is almost entirely Rust build output under
`NARI\target\`, which the earlier pass presumably excluded or did not reach.
Neither number changes the conclusion: the `.o`/`.rs`/`.bin` mass is compiler
artifacts, and a filename scan for `transcript|chatlog|conversation|export|thread`
returns only NARI workbench session documents, duplicated across build
transaction directories. **There are no ChatGPT conversation archives in this
tree.** It is where ChatGPT's *outputs* were written, not where its *dialogue*
was stored.

**Second correction:** `ChatGPT\RPRM-Spark` was last written **2026-09-16 at
17:08**, roughly five hours before this pass. William told the process-history
lane on 2026-09-08 that he had *"completely just unlinked and disabled
OneDrive."* The tree is live. Either the unlink did not take, or it was
re-enabled.

### 1.4 The Downloads tree is a large, uningested secondary corpus

440 files, **166 zip archives**, 10.24 GiB. Named by lane and date, most recent
first: `NARI_SPARK_SYSTEMS_RESEARCH_2026-09-16`, `RPRM_SPARK_05_RESULTS_2026-09-16`,
`RPRM_SPARK_04_RESULTS_2026-09-16`, `RPRM_SPARK_03_RESULTS_2026-09-16`,
`BSD_cross_problem_pilot`, `BSD92_through81_review_and_factorization_gate`,
`BSD90_Overnight_Attack`, `bsd-full-source-height-receiver-88`,
`bsd-moving-relative-adapter-87`, and a long tail of
`RPRM_BSD_Public_to_NN_Catchup` packets.

These are the ChatGPT â†” Codex handoff packets. They are the closest thing on disk
to a record of the *interface* between the two lanes, and **none of the three
ingest lanes opened them.** They are the highest-value remaining ingest target
after a platform export.

### 1.5 What would actually close the gap

A platform export from `chatgpt.com` â†’ Settings â†’ Data controls â†’ Export data.
Only William can request it. Nothing on this machine substitutes for it.

## 2. The memory fabric â€” closed

The process-history lane reported that the fabric could not be queried. It can.
No `rprm-memory-fabric` MCP namespace is exposed to any of these sessions â€” that
part was correct â€” but the skill points at a local implementation with a
documented read-only CLI, and using that CLI is what the skill instructs.

| Item | Resolved path |
|---|---|
| Implementation | `<local>\RPRM-foam-development\tools\rprm_memory_fabric\` |
| Seeded store | `...\OneDrive\DOCUME~1-...-219031\ChatGPT\RPRM Alpha\output\rprm_memory_fabric_stage1\alpha_seed.sqlite3` |

`current-snapshot`:

| Field | Value |
|---|---|
| `snapshot_root` | `944da1fef7bb71be819df694599f9908b878cd50e515bd02f973c50fa69adb2e` |
| blobs | 115 |
| occurrences | 1,932 |
| relations | 1,817 |
| relation ports | 3,634 |
| relation schemas | 8 |
| **claims** | **0** |
| packet cache | 155 |
| search FTS rows | 3,634 |

Two `compile-context` calls with the canonical minimum receiver, namespace
`rprm-alpha`:

| Query keys | Packet | `match_fiber` | Members admitted |
|---|---|---|---|
| liar teacher Hamming simplex seven eight movable vacancy calibrated checks | `packet:58731cf9â€¦` | MANY(210) | 9 |
| ternary cube second difference kernel vacant center graded scar Newton interpolation | `packet:041b7abcâ€¦` | MANY(293) | 9 |

**The single most consequential thing it returned** â€” a grading William made in
August that both ingest lanes missed, and that changed the synthesis lane's
research recommendation:

> "**Center-blind ternary-grid closure:** the full-line second-difference kernel
> is affine; the center-only kernel is constants plus odd functions; the
> invisible quotient has dimension `(3^n-1)/2 - n`. This is established
> finite-dimensional mathematics, not a novelty or physics claim."
>
> "**Boolean-cube graded scar decomposition:** the MÃ¶bius/scar transform is
> unitriangular, and a grade-`k` receiver forgets exactly the monomials of degree
> greater than `k`. This is established mathematics under a project receiver
> reading, not a novel theorem claim."

**Remaining fabric gap, stated honestly.** The search is a lexical FOLD. The two
packets reported 210 and 293 policy-visible candidates before packing and
admitted nine each. Declared open seams include `CANDIDATE_CAP` and
`PAYLOAD_OR_CANDIDATE_OMISSIONS`. `search_omissions` was not called. The aperture
was not widened. **And the `claims` table is empty**, so `trace_claim` and
`show_conflicts` have nothing to operate on: the fabric is currently an
occurrence-and-relation index, not a claim ledger.

## 3. Gaps that remain open

| Gap | Size | Why it matters | Cost to close |
|---|---|---|---|
| ChatGPT platform export | ~75% of the primary research lane by volume | The framework was invented there | William requests it; one click, then ingest |
| Downloads handoff packets | 166 zips, 10.24 GiB, untouched | The ChatGPT â†” Codex interface record | One ingest pass, a few hours |
| BSD campaign interior | ~900 files under `research/bsd-*` | Only the checkpoint-92 state was read; no individual argument was evaluated | Large; requires a specialist |
| Fabric below the candidate cap | 503 candidates seen, 18 admitted | Unknown what is under the cap | Widen aperture, call `search_omissions` |
| `.claude\projects\` sessions | 982 files, inventoried, unread | The Claude/druid side of the wizard-druid split | Medium |
| `<local>\RPRM-foam-development` | 198 commits | Implementation history for Audit99 / 105 / 116 | Medium; only the fabric subtree was opened |
| Lean formal suite | 20 declarations | `verify.py --lean` not run in any lane; nobody outside the project has executed it | Small; run it |
| `papers/process-mechanics`, `papers/absolute-distinction` | manuscripts | Read by the first-party and independent lanes; not re-opened by the synthesis lane | Small |

## 4. What the synthesis lane added that was not in the three reports

1. The fabric is reachable and populated, with counts (Section 2). The claims
   table is empty.
2. The ChatGPT gap is ~75%, not 100%, and the two surviving artifacts carry
   producer-declared fidelity labels (Section 1.2).
3. The OneDrive `ChatGPT\` tree is 77.89 GiB, not 11.35, and contains no
   conversation archives (Section 1.3).
4. `ChatGPT\RPRM-Spark` was written 2026-09-16 17:08 â€” the tree William said he
   had disabled is live.
5. 166 handoff zips in Downloads are an uningested secondary corpus that no lane
   opened (Section 1.4).
6. William's own August grading of the ternary-grid and graded-cube work as
   *established, not a novelty* â€” which both ingest lanes recommended as research
   targets, and which the synthesis lane consequently rejected.
7. Independent exact recomputation of the ternary-grid nullities, the withheld-
   centre determination table, the graded-cube kernels, and the 845-machine
   census family count. All confirmed. Scripts retained in `_tools/`.
