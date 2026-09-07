# Handbook comprehension assessments

This packet makes three small handbook assessments inspectable and reusable. It contains the questions, scoring criteria, scored answers, exact handbook versions, and the limits of the resulting evidence.

| Assessment | Handbook actually supplied | Result | Evidence |
| --- | --- | --- | --- |
| [A: core concepts](questions-a.md) | [Version 1](handbooks/v1.md) | 40/40; acceptance criterion met | One respondent, 20 questions, manual grading |
| [B: transfer cases](questions-b.md) | [Version 2](handbooks/v2.md) | 24/24; acceptance criterion met | A fresh respondent, 12 different questions, manual grading |
| [C: final-version cases](questions-c.md) | [Version 3](handbooks/v3.md) | 24/24; acceptance criterion met | A fresh respondent, 12 questions, manual grading |

See [the results and limitations](results.md), [machine-readable metadata](results.json), [rubrics](rubrics.md), and the answer keys [A](answer-key-a.md), [B](answer-key-b.md), and [C](answer-key-c.md). The scored mathematical responses are retained as [A](responses/a.md), [B](responses/b.md), and [C](responses/c.md), with source-location and execution headers removed.

Version 2 addressed four clarifications suggested by response A. Version 3 then made finite complete state and action tables with exact comparisons explicit for its finite algorithms. C supplied that complete third version, including a question testing those premises. At the recorded review, it was byte-identical to the current [agent handbook](../AGENT_HANDBOOK.md). Its 12 answers do not test every possible use of the book. Results belong to the exact supplied versions, not automatically to every later handbook revision.

## Repeat the assessment

1. Choose one handbook and one question file. Record their SHA-256 hashes before the run. The versioned handbook copies and historical question files here retain the assessed bytes.
2. Start a fresh respondent context with no prior conversation from the project. Supply only the chosen handbook and questions. Ordinary prior mathematical knowledge and reasoning are permitted; reading the handbook does not erase that knowledge.
3. Instruct the respondent not to read other repository files, answer keys, rubrics, prior responses, other tasks, or web sources. Give an explicit rule for permitted tools. If technical isolation is required, configure and verify it separately; an instruction alone is not a sandbox.
4. Freeze the rubric, acceptance threshold, critical questions, and treatment of ambiguity before receiving an answer. Keep the rubric and answer key outside the respondent's available inputs.
5. Ask for all answers, relevant hypotheses and evidence scope, plus any missing handbook concepts or ambiguous questions. Retain the unedited response and input hashes privately if it contains execution metadata; publish only an appropriately sanitized mathematical response.
6. Grade every answer manually against the rubric. Record per-question scores, critical errors, reasons for any deductions, the grader's access to prior scores, and any adjudication. Do not replace scoring with the respondent's own claim of understanding.
7. Report the exact tested version, respondent configuration when captured, context and tool restrictions, whether restrictions were enforced or merely instructed, and any deviations. Separate successful answers from evidence that the handbook itself caused learning.

Once these questions or keys have been read, they are no longer unseen material for that respondent. Use newly frozen transfer questions for a new held-out assessment. Repeating a published test can check consistency or regressions, but should not be described as fresh blind evidence.

The three recorded passes show that these respondents produced correct, scoped answers to these questions while instructed to use the supplied handbook and ordinary mathematics. They do not establish universal comprehension, mastery of every domain, an arbitrary theorem prover, or the framework's correctness. They also do not compare learning gains against a no-handbook control.

All original material in this directory is offered under CC0-1.0.
