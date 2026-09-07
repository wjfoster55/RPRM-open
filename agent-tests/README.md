# Handbook comprehension assessments

This packet retains six bounded handbook assessments: questions, frozen criteria, scored mathematical answers, exact handbook versions and evidence limits.

| Assessment | Supplied handbook | Result | Scope |
|---|---|---|---|
| [A: core concepts](questions-a.md) | [Version 1](handbooks/v1.md) | 40/40; declared criterion met | 20 questions |
| [B: transfer cases](questions-b.md) | [Version 2](handbooks/v2.md) | 24/24; declared criterion met | 12 new questions |
| [C: finite-algorithm cases](questions-c.md) | [Version 3](handbooks/v3.md) | 24/24; declared criterion met | 12 new questions |
| [D: expanded handbook](questions-d.md) | [Version 4](handbooks/v4.md) | 79/80 | 20 questions; one requested explanation omitted |
| [E: targeted clarity follow-up](questions-e.md) | [Version 5](handbooks/v5.md) | 16/16 | Four new questions targeting three known clarity changes |
| [F: relational-layer transfer](questions-f.md) | [Version 6](handbooks/v6.md) | 24/24 | Six questions; frozen-key arithmetic erratum disclosed |

The current [agent handbook](../AGENT_HANDBOOK.md) is byte-identical to [version 6](handbooks/v6.md). [Assessment F](questions-f.md) scored 24/24 on six targeted transfer questions, using the [frozen rubric](rubric-f.md) with a disclosed [arithmetic erratum](rubric-f-erratum.md). E remains attached to version 5 and D to version 4. Different questions and versions do not measure a controlled improvement.

See [results and limits](results.md), [machine-readable bindings and item scores](results.json), and [rubrics](rubrics.md). Mathematical responses are retained for [A](responses/a.md), [B](responses/b.md), [C](responses/c.md), [D](responses/d.md) [E](responses/e.md) and [F](responses/f.md). The supplied handbook and question bytes remain unchanged. Response execution declarations were removed as described in each result; every mathematical answer was retained.

## Repeat the assessment

1. Choose one handbook and one question file. Record their SHA-256 hashes before the run. The versioned handbook copies and historical question files here retain the assessed bytes.
2. Start a fresh respondent context with no prior conversation from the project. Supply only the chosen handbook and questions. Ordinary prior mathematical knowledge and reasoning are permitted; reading the handbook does not erase that knowledge.
3. Instruct the respondent not to read other repository files, answer keys, rubrics, prior responses, other tasks, or web sources. Give an explicit rule for permitted tools. If technical isolation is required, configure and verify it separately; an instruction alone is not a sandbox.
4. Freeze the rubric, acceptance threshold, critical questions, and treatment of ambiguity before receiving an answer. Keep the rubric and answer key outside the respondent's available inputs.
5. Ask for all answers, relevant hypotheses and evidence scope, plus any missing handbook concepts or ambiguous questions. Retain the unedited response and input hashes privately if it contains execution metadata; publish only an appropriately sanitized mathematical response.
6. Grade every answer manually against the rubric. Record per-question scores, critical errors, reasons for any deductions, the grader's access to prior scores, and any adjudication. Do not replace scoring with the respondent's own claim of understanding.
7. Report the exact tested version, respondent configuration when captured, context and tool restrictions, whether restrictions were enforced or merely instructed, and any deviations. Separate successful answers from evidence that the handbook itself caused learning.

Once these questions or keys have been read, they are no longer unseen material for that respondent. Use newly frozen transfer questions for a new held-out assessment. Repeating a published test can check consistency or regressions, but should not be described as fresh blind evidence.

The recorded responses support use of the tested handbook versions for these bounded exercises under the supplied-input instructions. They do not establish universal comprehension, an arbitrary theorem prover, a learning gain over a no-handbook control, or correctness of every framework claim. Automatic repository verification checks reproducible artifacts; it does not repeat these comprehension assessments.

All original material in this directory is offered under CC0-1.0.
