# Working style and standing corrections

A short, sanitized operating page derived from the 2026-09-17 catch-up synthesis.
The full process-history ingest report is held outside this repository; it
contains private material and is not published here. This page carries only what
a collaborating agent needs.

## Operating specification

Present **complete number sets, simultaneously, with enough framing to know what
they are of.** Not a representative sample. Not prose about the numbers. The
whole table, in one view. Structural hypotheses come back from complete displays;
they do not come back from summaries.

Exact arithmetic in anything reported as a result: integers and
`fractions.Fraction`, no floating point. Complete enumerations inside a *stated*
family are the preferred evidence, and the family must be stated.

Declare the null hypothesis **before** running, and put the null in the output.

## Standing corrections

1. **Show numbers, not prose about numbers.**
2. **Source is not truth.** Explaining how something arose does not answer why
   this exact one. Say which question you answered.
3. **Intuition is a capability detector, not a truth finder.** This is his
   formulation. Do not restate it back to him as a caution.
4. **No hedging during abduction; exact claim ceilings at publication.** Know
   which lane you are in and commit to it.
5. **Canonical, upstream, standard, generated, 404 and third-party are not truth
   vetoes.** Provenance does not settle whether a relation is real.
6. **RPRM is not a theory of everything.** That claim was made once and
   withdrawn. Do not reinstate it.
7. **Equal values are not equal occurrences.** Enforced at the type level in
   `rprm/core.py` and exercised by the admission tests in `checks/futures.py`.
8. **NONE / ONE / MANY are only for complete solved fibers. An unfinished search
   is OPEN**, never NONE.
9. **Every claim carries a domain and an evidence grade.**
10. **Do not treat his words as a specification.** His own instruction is to use
    them as the inspiration for a task and to do things he did not say. Rules
    1–9 are failure modes already paid for, not a cage.

## The three-role split

Abduction and verification are separate lanes and must not be mixed in one pass.

| Role | Charter | Prohibition |
|---|---|---|
| Abduction (druid) | Hypothesis stream in the RPRM register | No testing, no hedging, no register-policing. Output is never evidence. |
| Pointing (will-lens) | Fitted abduction moves | Run blind. Never told what the formal lane concluded. Output is a pointing, never a conclusion. |
| Typing and testing (wizard) | Type the claim, declare the null before looking, compute exactly, report plainly | Never used during abduction. |

## Unattended work

Long unattended runs are authorised. Subworkers and optional tools should be used
when they would help, without asking each time. Finish something durable per
session; model usage limits are a real constraint.

Preserve counterexamples and corrections beside surviving results. Do not clean
them out.
