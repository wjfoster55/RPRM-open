# Context and question selection

**EXPERIMENTAL — NEWLY PROPOSED synthetic mathematical application lead.**
This executable toy selects a useful next question inside a fully specified
four-rule family. It contains no real conversations, people, personal data,
diagnoses, therapeutic intervention, or measured communication outcome.
Its current result is exact finite model checking, not evidence of efficacy
when communicating with people.

## Run the example and checks

Python 3.10 or newer; standard library only. From the repository root:

```sh
python -I -B experimental/context-communication/example.py
python -I -B experimental/context-communication/check.py
python -I -B -O experimental/context-communication/check.py
```

Each command prints JSON and accepts optional `--output ABSOLUTE_JSON_PATH`.
Replace that placeholder with an absolute filename. The checker returns a
nonzero exit code on failure; its checks use explicit exceptions and continue
to run with Python optimization enabled. After argument admission it writes
`PENDING` before importing or executing the model, then writes `PASS` or
`FAIL`. An interrupted run that does not finish keeps `PENDING`, not a reused
passing result. A receipt is not accepted as a substitute for executing code.
Source hashes use public repository-relative names.

## The declared model

There are two abstract contexts, `C={0,1}`, and two response symbols,
`A={0,1}`. A context is a supplied index with a fixed meaning; it is not a
summary inferred from natural language. Plain integer bits are required:
booleans, strings and floating-point substitutes are rejected.

The hypothesis carrier contains **all four** deterministic functions `C→A`:

| ID | Answer in context 0 | Answer in context 1 | Function |
|---|---:|---:|---|
| `00` | 0 | 0 | constant zero |
| `01` | 0 | 1 | identity |
| `10` | 1 | 0 | complement |
| `11` | 1 | 1 | constant one |

The ID is an encoding of two ordered response ports. It does not designate
a personality, belief, intent, or psychological category. The response law is
`R(h,c,a) iff a=h(c)`. Identification assumes that one fixed `h` governs every
record and that every recorded answer equals `h(c)`. “Truthful” here means
compliance with that table, not a moral judgment about a source.

Additional selection assumptions are explicit: both contexts can be queried,
each query has equal unit cost, querying does not change the function, answers
are returned, and the context meanings stay fixed. No prior probabilities,
noise process, memory effect, or time-varying behavior are supplied.

## Ports, complete fibers and retained history

A history is an ordered list of 0–32 records with exactly two keys:
`{"context": c, "answer": a}`. The position is the occurrence identity.
Repeated answers remain separate occurrences. `append_answer` returns a new
history and never rewrites its input. At the 32-record capacity it rejects
an append without dropping observations.

| Interface | Supplied ports | Requested result |
|---|---|---|
| `answer(h,c)` | admitted rule and context | its deterministic bit |
| `fiber(history)` | every observed context/answer pair | all compatible rule IDs |
| `predictions(history,c)` | history and requested context | all compatible next bits |
| `minimax(candidates)` | an explicitly supplied subset of the four rules | every optimal informative question and a declared tie break |
| `analyze(history)` | full history | retained history, rule fiber, predictions, question selection and all conflict occurrence pairs |

The complete rule fiber is

`F(H) = {h in {00,01,10,11}: for every (c,a) in H, h(c)=a}`.

The implementation checks every candidate against every record. A candidate
is retained exactly when it satisfies all supplied constraints, and all four
candidates are tried. These two facts supply the finite completeness argument.
`NONE`, `ONE`, and `MANY` classify the cardinality of this **rule** fiber. They
do not classify which histories generated it, and `ONE` does not prove an
external source belongs to the model.

The prediction map returns `{h(c):h in F(H)}`. A `MANY` rule fiber can have a
`ONE` prediction at a queried context. For example, after `(0,0)`, both `00`
and `01` remain, but both predict 0 at context 0. If `F(H)` is empty, prediction
returns `NONE` with no values. The model does not infer a response from vacuous
agreement over an empty set.

The history `(0,0),(0,1)` is validly typed but inconsistent with every fixed
rule. Its fiber is `NONE`, both records remain, and analysis identifies their
conflicting occurrence pair `[0,1]`. It does not label either record wrong or
explain why the disagreement happened. Further valid records remain stored;
they cannot restore a rule eliminated by a retained contradiction. Continuing
with a changed response model requires a separately declared contract.

## Minimax question selection and worked example

For nonempty candidate set `S`, question `c` partitions it into
`S_(c,0)` and `S_(c,1)`. Its score is the largest number of remaining rules:

`score(c,S) = max(|S_(c,0)|, |S_(c,1)|)`.

`minimax` computes both partitions and both scores, then retains **all**
questions attaining the least score while strictly reducing `|S|` in the
worst case. The deterministic example chooses the smaller context on a tie.
This tie break is a declared convention. It is not additional evidence that
one equally scoring context is intrinsically better. The `choice_fiber`
reports the full set of optimal informative contexts separately from that
single choice.

For an empty set, selection reports `INCONSISTENT`, with no next-question
guarantee or numerical worst-case score. For a singleton it reports
`IDENTIFIED` and stops; both possible partitions remain inspectable. Because
the four IDs denote distinct functions, any set of two or more contains a
pair distinguished at at least one context, so an informative question exists.

The worked example supplies synthetic rule `01`:

| Retained answers | Compatible rules | Next selection |
|---|---|---|
| none | `00,01,10,11` | contexts 0 and 1 both score 2; convention chooses 0 |
| `(0,0)` | `00,01` | context 0 scores 2; context 1 scores 1; choose 1 |
| `(0,0),(1,1)` | `01` | identified within the supplied family; stop |

Under the fixed truthful-response assumptions, this policy identifies each
of the four rules in two questions. One binary question has at most two
answer classes and cannot distinguish all four. Querying both contexts
achieves the lower bound. This proves optimal worst-case **query count for
this family**, not optimal human communication or general optimal decision
trees. The selector itself minimizes a one-step cardinality objective;
equal total costs or general multi-step optimality are not inferred for
other contexts, query prices, priors or response laws.

## What representations preserve and lose

The candidate set preserves the current possible answers and the declared
minimax scores. It also supports the filter update
`S'={h in S:h(c)=a}`. It forgets record order, multiplicity and the occurrence
pairs that caused a contradiction. Those questions need the retained history.

The **number** of candidates alone is weaker. Histories `(0,0)` and `(1,0)`
both leave two candidates. The first requires context 1 to distinguish its
rules; the second requires context 0. A count does not determine the policy.

With this API's finite capacity, the candidate set alone also loses append
enabledness. One copy and 32 copies of `(0,0)` have the same candidate set,
but only the first history admits another record. Retaining candidate set
and length repairs that enabledness/readout question; retaining the full
history also preserves the richer occurrence receiver used by `analyze`.
This pack keeps the complete history rather than claiming a unique inverse
from its candidate set.

## Frozen hostile cases and model boundaries

- **Context erasure:** `(0,0),(1,1)` is consistent with rule `01`. Treating the
  answers as if they came from one context creates a false contradiction.
- **Changed response:** `(0,0),(0,1)` gives `NONE` under a fixed rule. It can
  arise from a changing or noisy process; the empty fiber does not choose
  among those explanations or establish dishonesty.
- **Undetectable change:** a first answer from `01` at context 0 and a second
  from `10` at context 1 produce `(0,0),(1,0)`, uniquely fitting `00`. A unique
  static fit does not establish that the process stayed static.
- **Excluded answer:** a response such as `undecided`, an unanswered query,
  or a third context is outside the binary ports. It is rejected as an
  admission error, not converted to bit zero or a rule `NONE` result.
- **Model completeness:** there is no missing fixed binary function on these
  two contexts: all four are included. What remains unmodeled includes time,
  changing meanings, stochastic answers, hidden contexts and richer replies.
- **Other objectives:** unequal query cost, response burden, unavailable
  questions, or a probability-weighted objective require a different selection
  contract. Smaller candidate count alone says nothing about those costs.

When applying an idea like this to people, the fixed deterministic table and
truthful-return assumptions would need independent justification. People can
change their answers or interpret contexts differently; this toy does not
model that process. No diagnosis, therapy, deception detection, or improved
communication outcome follows from its mathematical consistency checks.

## Verification, baseline and next experiment

The independent checker uses four handwritten Boolean functions and intersects
allowed responses per context. It compares all 5,461 histories of lengths
0–6, their complete fibers and conflict pairs, both prediction questions,
and all 21,844 single-record append transitions from those histories. It
checks all 16 candidate subsets, including subsets not reached from the full
initial family, against separately formed question partitions. All four
truthful policy runs, tie sets, contradictions, type failures, nonmutation
and selected 32/33-record capacity cases are included. It does **not** enumerate
every history through the API maximum of 32 records. The written filtering
argument and explicitly reported finite tests are separate evidence grades.

The ordinary baseline is enumeration of four response functions and two
questions. For history length `n`, the fiber performs at most `4*n` response
comparisons. Question partitions inspect at most four hypotheses per branch
and context. Full conflict-pair output can grow quadratically in `n`;
`analyze` deliberately repeats some validation/filtering for transparency.
No timing benchmark, optimized implementation or speedup is claimed.

A next mathematical experiment could supply a finite state that changes
between questions, an explicit error budget, or unequal question costs,
then compare a newly defined policy against exhaustive decision-tree search.
Preserve inconsistent histories and expose any added assumptions. A later
empirical study would separately need a target, permitted data, held-out
evaluation and appropriate baselines; synthetic success is not that study.

This follows the finite teacher/question model in the
[conceptual discussion](../../docs/concepts.md#teachers-questions-and-abduction)
and the explicit carrier, fiber, and receiver contract in the
[agent handbook](../../AGENT_HANDBOOK.md).
