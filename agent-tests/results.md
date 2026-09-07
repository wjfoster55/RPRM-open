# Recorded results and their limits

A, B and C met their respective predeclared acceptance criteria. D scored 79/80; E scored 16/16 on a targeted follow-up. F scored 24/24 on six targeted transfer questions and meets its declared 22/24 plus critical-question criterion, with a disclosed key correction. D and E have no separately recorded acceptance threshold, so none is supplied retroactively.

| Run | Exact handbook | Questions | Score | Grading outcome |
|---|---|---|---|---|
| A | [Version 1](handbooks/v1.md) | [20 core questions](questions-a.md) | 40/40 | Meets the declared 36/40 criterion; no critical error |
| B | [Version 2](handbooks/v2.md) | [12 transfer questions](questions-b.md) | 24/24 | Meets the declared 22/24 criterion; no critical error |
| C | [Version 3](handbooks/v3.md) | [12 finite-algorithm questions](questions-c.md) | 24/24 | Meets the declared 22/24 criterion; no critical error |
| D | [Version 4](handbooks/v4.md) | [20 expanded questions](questions-d.md) | 79/80 | One explanation criterion missing in question 5 |
| E | [Version 5](handbooks/v5.md) | [Four targeted questions](questions-e.md) | 16/16 | All sixteen frozen criteria satisfied |
| F | [Version 6](handbooks/v6.md) | [Six transfer questions](questions-f.md) | 24/24 | Declared criterion met; key erratum retained |

The [JSON record](results.json) retains every item score, original input hash, public response hash and grading scope. All A–C scores and deductions are preserved. Their second mathematical reviewer agreed with the release editor, with access to the initial totals as documented there; no blinded grading is claimed. D and E were graded by the release editor against their own frozen rubrics. No second-grader result is recorded for those two runs.

## The retained deduction and follow-up

F received version 6 and six new transfer questions. Two graders separately
recorded 24/24 before comparing their grades. Both identified the same
arithmetic error in the frozen rubric: for n=2,s=2,d=2, the named bound is
16, not 32. The respondent correctly derived 16. The original
[rubric](rubric-f.md) is unchanged, with the [post-response erratum](rubric-f-erratum.md)
and correct credit explicitly recorded. F supplies targeted comprehension
evidence; it is not a controlled improvement estimate or a new science result.

D question 5 gives the correct shortest word, both outputs and the n−1 bound. It does not derive the requested block-count reason: adding the failure state also adds an initially separate observation block. Citing the bound and noting that a larger bound is looser does not supply that derivation. It earned 3/4; the other nineteen answers earned 4/4. The original answer and this deduction remain inspectable in [response D](responses/d.md) and [rubric D](rubric-d.md).

Version 5 adds that counting explanation and clarifies two further points: accepted version stamps must strictly increase, and inward vector acceleration is different from the second derivative of radial distance. E used four new questions about those known clarity changes with a fresh respondent context. Its complete derivations earned 16/16 under [rubric E](rubric-e.md). This is a targeted follow-up, not an independently selected general benchmark, a repeat of D, or evidence that every use of version 5 has been tested.

## Exact versions and portable exports

All six versioned handbooks and question files retain their assessed bytes. D and E's public rubrics also retain the original frozen bytes. A–C's public rubric prose expands the historical frozen notes without substituting its hash for theirs. Each original hash is recorded alongside the actual published file binding.

The public D response adds only a title and removes its final execution declaration. The E response retains its original title and removes its final input/tool declaration. Every preceding mathematical answer byte is unchanged. Public response hashes therefore differ from the original response hashes; both are recorded. Source paths, internal task identities and private scoring files are not part of this packet.

Version 2 followed four clarifications suggested in A. Version 3 made complete finite state/action tables and exact decidable comparisons explicit. Version 4 expanded the mathematical handbook; version 5 makes the three clarifications above. Version 6 adds the relational-layer proposal, full-name origin, domain-matching requirement, scientific comparison scope and executable fixed-gap decision. The [current handbook](../AGENT_HANDBOOK.md) is exactly the version-6 file supplied in F. E's match to version 5 and C's former match to version 3 remain historical.

## Context and evidence limits

Each respondent started in a fresh context without inherited project conversation and was instructed to use only the supplied handbook, its questions and ordinary mathematical reasoning. Rubrics, prior responses, other project files and external references were excluded by instruction. Respondents declared their limited input/tool use. This was context separation with instructional restrictions, not operating-system sandbox enforcement or independent telemetry proving every possible host access absent. General platform instructions and prior mathematical knowledge were not removed.

The exact respondent model version was not captured. No model-level reproducibility, blind grading or causal learning effect is claimed. There was no no-handbook control. These different question sets and handbook versions do not yield a paired improvement estimate. Published questions and keys are no longer unseen for anyone who reads them.

The results support usability of these exact handbook versions for these bounded exercises, including a retained missing explanation. They do not establish universal comprehension, mastery of every application, general theorem-proving ability, or correctness of all RPRM mathematics. Use the [repeat protocol](README.md#repeat-the-assessment) and newly frozen questions for further evidence.
