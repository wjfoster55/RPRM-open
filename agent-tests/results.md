# Recorded results and their limits

All three fixed responses met their respective predeclared acceptance criteria. A second manual mathematical review agreed with the release editor's scores. The second reviewer knew the initial A/B totals before reviewing those responses; the C total was shared after its initial reading but before its final score record. This was an independent assessment of the answers, **not blinded or double-blind inter-rater scoring**.

| Run | Exact handbook | Questions | Score | Critical errors | Decision |
| --- | --- | --- | --- | --- | --- |
| A | [Version 1](handbooks/v1.md) | [20 core questions](questions-a.md) | 40/40 | None | Meets 36/40 criterion |
| B | [Version 2](handbooks/v2.md) | [12 transfer questions](questions-b.md) | 24/24 | None | Meets 22/24 criterion |
| C | [Version 3](handbooks/v3.md) | [12 final-version questions](questions-c.md) | 24/24 | None | Meets 22/24 criterion |

Every answer earned 2/2. C separately awards one point for the concrete answer and one for its scope and premises; every component earned its point. The [JSON record](results.json) supplies each score and its reason. The [public rubric](rubrics.md), answer keys, and mathematical responses [A](responses/a.md), [B](responses/b.md), and [C](responses/c.md) make the decisions inspectable. Public rubric prose expands the original frozen scoring notes; its byte identity is not substituted for the historical rubric hash.

## Inputs bound to the recorded runs

The supplied handbook and question bytes are retained without change in this packet. SHA-256 identifies the bytes, not their truth or a respondent's isolation.

| Input | SHA-256 |
| --- | --- |
| `handbooks/v1.md` | `258e3bf92dcfee0cfa99eb0a8ff63cc2979185b5ba112f91852bef67b771de15` |
| `questions-a.md` | `cd2616a07df701d6cdc707f8b89ff911502b0066675245089a1ea685c48002ad` |
| `handbooks/v2.md` | `7bd5b14677f376744a862d8ec901523eb47e1be61b1596fa9aa384e551797c63` |
| `questions-b.md` | `56b28a5fb49d246accbb60fa9d1f7eb6c4b26d0fb82d49d367b32f5bf1f522e9` |
| `handbooks/v3.md` | `8cb6c22e698fe3cd888bb36100cb0b6e8153c5b33f0a14bad38e5ed28baec8ef` |
| `questions-c.md` | `7bebfd1418baba3c5dda31d4d57fd84f5b34811ce30170a4fbaf5f9e0aca0e35` |

## What changed between versions

Response A correctly answered all questions and suggested four useful clarifications. Version 2 added an infinite-fiber parameterization with a coverage argument, an attaining construction for the repair-tag bound including the empty source, concrete reopen-record contents, and a digit-index/bit-cost convention.

B used a fresh context and different questions with version 2. It correctly addressed transfer cases, including a zero interpolation coefficient, a lossy abstract singleton, typed Boolean/integer equality, incompatible reports, and a synthetic external-validation proposal. Question B5 ambiguously describes the initial summary classes; the respondent identified this and answered both readings correctly. The answer key preserves that qualification instead of retroactively tightening the scored question.

Version 3 made the effective finite state/action-table premises explicit. C then received the complete third version and new questions, including a direct test of infinite action enumeration and undecidable observation equality. It answered all twelve correctly. Question C3 exhibits two paths without stating exhaustiveness; the response correctly distinguishes a complete two-path source from two examples in a larger source.

At this review, the live [agent handbook](../AGENT_HANDBOOK.md) and the assessed version-3 copy are byte-identical with SHA-256 `8cb6c22e698fe3cd888bb36100cb0b6e8153c5b33f0a14bad38e5ed28baec8ef`. This binds C to the current book's actual bytes; it does not mean twelve questions test every statement or possible use of the book. Future edits require their own version record.

## Isolation and respondent metadata

All three respondents were started in fresh contexts with no inherited project conversation. Each was supplied only its exact handbook and question-file locator, with instructions not to read other project files, rubrics, prior responses, tasks, or web sources. All responses declared that only those two inputs and ordinary mathematical reasoning were used. The release editor observed the fresh-context setup.

These were **instructional restrictions, not operating-system sandbox enforcement**. General platform instructions and prior mathematical knowledge were not removed. The retained declarations and observed setup are not an independently instrumented proof that no other information could have been available.

No model override was set. The exact respondent model version was not captured and is reported as unavailable rather than inferred. This limits exact model-level reproduction. The scored response files here retain the mathematical answers and ambiguity reports, with execution headers and source-location details removed.

## Strongest supported conclusion

These respondents produced correct, appropriately scoped answers to these 44 questions under the recorded input instructions. The results support usability of the tested handbook versions for these bounded exercises, including the current version's explicit finite-algorithm premises. They do not establish universal comprehension, general theorem-proving ability, mastery of every application, or correctness of all RPRM mathematics.

Ordinary prior mathematical knowledge was permitted. There was no no-handbook control, so passing does not show that the handbook caused the respondent to learn each concept. The three runs also differ in both questions and handbook version; their scores do not measure a controlled improvement. Use the [repeat protocol](README.md#repeat-the-assessment) and newly frozen questions for further evidence.
