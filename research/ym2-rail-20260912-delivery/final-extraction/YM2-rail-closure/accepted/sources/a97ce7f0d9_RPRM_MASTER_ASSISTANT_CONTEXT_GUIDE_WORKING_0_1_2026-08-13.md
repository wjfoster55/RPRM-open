# RPRM Master Assistant and Context Guide — Working 0.1

Status: `LIVING_DRAFT__USER_CORRECTION_LOOP_ACTIVE__NOT_FROZEN`

Date: `2026-08-13`

Purpose: give a new assistant the smallest honest packet needed to work with
RPRM, while developing the first practical context application. This file is a
living synthesis. It does not supersede sealed experiment bytes, the frozen
Still Point, or the separate assistant compiler synthesis.

## 1. Reading rule and claim labels

Authority descends in this order:

1. sealed experiment bytes and receipts;
2. the frozen kernel Still Point;
3. the main Shadow corpus;
4. exact source-turn wording and user corrections;
5. recovery packets;
6. later architectural inference.

Use these labels rather than promoting a useful idea by rhetoric:

- `FINITE`: exact only on the frozen finite carrier that was tested;
- `OPS`: exercised operationally, but not a universal theorem;
- `CONTRACT`: an adopted normative rule;
- `SCOUT`: an exact or abductive design that has not earned executable scope;
- `HYPOTHESIS`: a falsifiable proposal;
- `OPEN`: unresolved or outside the admitted carrier.

Agreement is not proof. A hash proves byte identity, not truth. A timeout does
not prove `NONE`. A finite example does not become a universal law merely
because its shape is suggestive.

## 2. The shape of the key

The smallest useful RPRM kernel is:

```text
typed relation
  + declared roles and one distinguished vacant role (APERTURE)
  + retained ports / orientation / incidence / lineage
  + completion fiber NONE | ONE | MANY
  + unresolved seam remains EVENT | OPEN
  + CAR for invertible representation change
  + ADAPTER or FOLD for receiver-faithful loss
```

The aperture is the question being asked of the relation. The fiber is the set
of values that can fill it without violating the declared relation. `ONE` is an
earned exact route; `NONE` is an earned impossibility inside the carrier;
`MANY` preserves ambiguity. Ill-typed, unavailable, timed out, out-of-carrier,
or not-yet-searched material stays `OPEN` and must not be folded into `NONE`.

RPRM is not numerology. Numbers are useful when they are typed coordinates,
phase addresses, state identifiers, counts forced by a constructor, or compact
names for proved equivalence classes. An untyped number has no magic semantic
authority.

The practical shortcut is compositional. Prove a small constructor, preserve
its boundary and receipt, then inherit it at the next scale. A symbolic rule can
describe an object much larger than the rule. This avoids replaying every
intermediate proof; it does not make the cost of materializing every requested
output disappear.

## 3. Trust, observation, and the missing manager

The working trust cycle is:

```text
OPEN -> PROVE -> SEAL -> FOLD -> INHERIT
                         ^          |
                         |          v
                    REOPEN AFFECTED CONE
```

Do not put eyes on every lane forever. Once an immutable region and its
interfaces are certified, later work revalidates the certificate, changed
addresses, touched interfaces, bound roots, and conserved obligations. It does
not replay the untouched interior from genesis. Any changed dependency,
receiver, policy, schema, adapter, verifier, orientation, or residual reopens
the dependent cone; disjoint certified regions remain reusable.

“No manager” does not mean “no clocks, queues, or coordinators.” A scheduler may
feed an aperture, but its tick cannot manufacture truth, permission, success,
or closure. Domain progress comes from local typed fit, events, and receipts.
The authoritative artifact remains the authority.

Observation is also a typed interaction with a cost. Prefer immutable
snapshots, passive receivers, and bounded telemetry. Containment limits blast
radius; it does not itself prove correctness.

## 4. Wizard and Druid

The Wizard asks whether the relation, constructor, proof, mutation suite,
receipt, and claim ceiling are exact.

The Druid asks whether the chosen receiver is the right one, whether the
carrier excludes something alive and important, whether the cost and
consequences are acceptable, and whether the system should close at all.

Neither is a decorative persona. Exact mathematics with the wrong receiver is
precisely wrong. Good purpose without a checkable mechanism is merely a wish.
Consequential work uses independent Wizard and Druid lanes, reciprocal review,
and a compiler/steward. Routine reversible work does not need ceremonial
overhead.

## 5. The context bottleneck

The immediate practical priority is repeated Codex context compaction. Codex
itself is patient zero: improve the assistants' own oxygen mask before applying
the system to Nari or any downstream project. The goal is not a giant “RPRM
philosophy prompt.” A local prompt comparison already produced a null result.
The goal is to carry the smallest receiver-sufficient state while retaining an
authenticated path back to the strong source.

The first privacy-safe runtime baseline confirms that this is a real bottleneck.
This task compacted three times in 47 minutes 23 seconds. Its active context was
approximately 233k, 229k, and 212k tokens immediately before those boundaries,
then approximately 22k, 25k, and 32k immediately after. The first two
compactions were about nine minutes apart. At a later measurement boundary,
194 model requests had accumulated about 21.23 million tokens, with about 95%
of input reported as cached. Caching changes economics but does not remove
context transport, context-window pressure, or compaction work.

A structural cold-aperture counterfactual strengthens the target. At a
4,096-character threshold, 98 local-tool outputs in this task occupied about
2.44 million serialized characters. Replacing each hot result with a bounded
1,200-character receipt would reduce that lane to about 118 thousand
characters, or 95.2%, before paying for selective source reopen. This is not a
token or quality result; it is the prefrozen size hypothesis for the evidence
aperture benchmark.

Codex's documented automatic-compaction threshold can count either the full
active context (`total`) or only growth after the carried compaction-window
prefix (`body_after_prefix`). This machine was using the default `total` mode.
The first controlled configuration change is `body_after_prefix`, with the
numeric threshold left at the model default. This should prevent the inherited
sealed prefix from immediately consuming the next window's growth allowance;
the claim remains operational until measured on subsequent tasks.

Subagent inheritance is another multiplier. Privacy-safe structural telemetry
found 833 unique compacted windows represented by 9,853 copied compacted
records across local task chains. Full-history forks therefore carry saturated
interiors into children repeatedly. Default delegation should use no inherited
turns or a small bounded tail plus a rooted task packet and explicit file
locators.

The current global reasoning gear is `ultra`, and the local model catalog ties
that gear to maximum reasoning with automatic delegation. This is a candidate
multiplier, not yet a demonstrated cause. Keep `ultra` for the present build;
later benchmark a receiver-selected gearbox so routine work does not pay for
wide branching when it is not needed.

The ordinary model path is approximately:

```text
TEXT -> TOKEN IDS -> EMBEDDINGS -> TRANSFORMER / KV STATE
     -> OUTPUT TOKEN IDS -> TEXT
```

If the public aperture is typed `TEXT`, decimal token IDs or vectors written in
the text box remain text and are tokenized again. Bypassing a layer requires an
input aperture actually typed for token IDs, embeddings, or authenticated model
state. Ordinary Codex and documented proprietary GPT request surfaces do not
expose arbitrary user-authored embedding or KV-state injection.

OpenAI does expose provider-generated opaque compaction items in the Responses
API. They carry prior state forward with fewer rendered tokens and are the
closest existing form of an accepted compact internal state. They are opaque,
must be passed as provider output, and are not application-authored proof
receipts.

Prompt caching is a separate shortcut: an exact stable prefix can be reused,
while a small dynamic suffix changes. It reduces repeated processing/cost but
does not change the semantic content or guarantee identical generated output.

## 6. Four different things called “compression”

### 6.1 Lossless byte code — CAR

Any finite text can be mapped bijectively to an integer or compressed bit
string and reconstructed. The decoder is part of the system. This preserves
bytes, not necessarily model token count; decimal or base-N text can tokenize
worse than the original.

### 6.2 Receiver-exact state — exact FOLD under a contract

Let `H` be histories, `W` an admitted family of future words/probes, and
`R(h,w)` the complete receiver-visible behavior, including tool actions,
errors, definedness, and open outcomes. Define:

```text
h ~_(R,W) h'  iff  R(h,w) = R(h',w) for every w in W
```

The equivalence class of `h` is the minimal receiver-complete state for that
contract. In a finite deterministic setting, classes can be assigned small
state IDs with compiled transition and output tables:

```text
q(h . e) = delta(q(h), e)
behavior = lambda(q(h), request)
```

The transcript can then leave the hot path. The transition table, decoder,
receiver root, and cold source still exist. If `W` includes “quote every omitted
character,” distinct histories remain distinguishable and exact semantic
compression collapses to identity. Compression is earned by naming a narrower
receiver contract, not by pretending arbitrary futures do not exist.

### 6.3 Empirical semantic key — approximate FOLD

A shorter ordinary-text prompt may produce equivalent behavior on a sealed
probe suite without a theorem for every future. This is useful, but it is an
empirical receiver-specific fold. A later separating probe must reopen the
source.

### 6.4 Provider latent — OPAQUE STATE

A provider may generate an encrypted compaction/reasoning state that its model
can reuse. We may pass it back through its typed aperture, but we cannot infer
that an arbitrary application-authored number or vector will be accepted as the
same kind of state.

## 7. “Zero” means canonical state, not absence

William’s `A -> zero -> C` intuition is represented as:

```text
A = raw natural-language history
Z = canonical typed state / receiver-equivalence address
C = desired receiver behavior

A --E--> Z --D--> C
 \--------------> C
```

The diagram commutes when the direct and factored routes agree for the declared
carrier and receivers. If updates also compose through `delta`, the system can
compile the middle out of the runtime hot path. The middle is not annihilated;
its law has become inherited machinery.

## 8. The inverse semantic shrinker

This is the central build hypothesis.

Do not first train a new receiver to understand a compact language. Freeze the
existing receiver and solve backward through it.

Let `R_Phi(x)` be a frozen receiver signature for message `x` under declared
future probes `Phi`. The inverse fiber of the original message is:

```text
Fiber(x) = { z : R_Phi(z) = R_Phi(x) }
```

The receiver-minimal semantic key is:

```text
z* = argmin_z token_length(z)
     subject to R_Phi(z) = R_Phi(x)
```

There are two related inverse tasks:

1. **message shrink:** find the shortest input equivalent to an existing
   message under `R_Phi`;
2. **behavior synthesis:** given desired behavior `y`, find the shortest input
   in `R_Phi^-1(y)`.

The inverse is generally a fiber, not a unique reversal. It may be `MANY`.

### 8.1 The room-and-door construction

Personified form:

1. Put any generator/searcher in a room with an accepted `n`-token message.
2. The only exit is an aperture admitting at most `n-1` tokens.
3. The door—not the generator—checks the frozen receiver signature, critical
   corrections, authority, open seams, and length.
4. A passing candidate becomes the sealed parent for the next room.
5. Repeat until the next aperture is proved empty or search remains open.

The interior may use deletion, rewriting, beam search, evolutionary search,
another model, or a future unknown method. The trusted computing base is the
typed boundary, probe suite, verifier, roots, and receipt—not an explanation of
how the interior thought.

### 8.2 Honest terminal outcomes

- `ONE`: exactly one passing candidate in an exhaustively admitted finite
  search;
- `MANY`: multiple passing candidates; choose only through a declared secondary
  law such as token count, stability, readability, or cross-version survival;
- `NONE`: no candidate exists in an exhaustively searched finite carrier;
- `OPEN_SEARCH`: the search failed to find one, timed out, or used an
  incomplete/infinite grammar;
- `OUT_OF_CARRIER`: the proposed code uses an unsupported input type.

“No shorter candidate was found” is usually `OPEN_SEARCH`, not proof of
minimality.

### 8.3 What “same semantic value” must mean operationally

Do not ask a single GPT, “Are these semantically the same?” and let that answer
open the door. Freeze a receiver signature with independent dimensions such as:

- intended action and output schema;
- referents, negation, polarity, time, ordering, and commitment;
- corrections and supersessions;
- user authority and prohibited actions;
- open obligations and unresolved ambiguity;
- required evidence/source roots and exact-quote availability;
- tool selection, arguments, and terminal-state behavior;
- declared future follow-up answers.

Use held-out separating probes and mutation twins. A collision produces a
shortest known distinguishing probe, which is added to the receiver and reopens
the affected candidates. This is counterexample-guided receiver refinement.

For stochastic model prose, equality of a few outputs is not equality of the
full conditional distribution. Exact claims belong first in deterministic
finite control receivers. Proprietary-model behavior remains an empirical lane
with repeated trials and a visible claim ceiling.

### 8.4 Concept inversion by rotating the aperture

The shrinker is one instance of a broader candidate mechanism. Learn, extract,
or declare one typed relation:

```text
C(concept, occurrence, context, polarity, effect)
```

Then rotate the vacant port rather than training an unrelated mechanism for
each direction:

- concept supplied, occurrence vacant: generate or retrieve examples;
- occurrence supplied, concept vacant: recognize/name concepts present;
- concept and occurrence supplied: verify membership;
- desired effect supplied: search for a concept coordinate that causes it;
- negative polarity supplied: test suppression/removal of that coordinate;
- frozen universe plus membership supplied: compute a logical complement;
- multiple compatible concepts: preserve `MANY` and their intersection.

This is the rigorous version of “give a model addition, invert it, and obtain an
addition detector.” The inverse is the preimage/fiber under a frozen receiver,
or the same relation with its aperture orientation reversed. It is not
automatically arithmetic negation.

If `E` is a pretrained representation and `c` a concept address, define:

```text
P_c = { x in U : Membership(E(x), c, context) is admitted }
```

`P_c` is the positive fiber. `U \ P_c` is the complement only after the universe
`U`, threshold, context, representation/model version, and membership receiver
are frozen. One positive example cannot identify an arbitrary concept boundary
from scratch. In a pretrained model, however, most of the learning may already
be inherited bulk; a name or exemplar can act as a probe into that bulk.

Concepts generally overlap. A Hangul passage explaining addition can contain
both an addition relation and Hangul script. Do not force it into one exclusive
branch. Give each item a multi-coordinate signature:

```text
sigma(x) = (addition?, contains-Hangul?, Korean-language?, instruction?, code?, ...)
```

Each new verified coordinate refines the intersections, forming a concept
lattice/Boolean incidence atlas rather than a single-label tree.

An apparent false positive receives four live hypotheses:

1. receiver/model error or adversarial collision;
2. a correlated proxy rather than the intended concept;
3. polysemy, context, or a carrier mismatch;
4. a genuine broader invariant that the human label did not yet name.

Find a minimal separating counterexample, add the missing coordinate, and
reopen the affected partition. A false positive becomes a promoted “positive
positive” only after an independent receiver and counterexamples support the
broader invariant.

Known neighboring mechanisms do pieces of this but do not establish the whole
RPRM claim:

- TCAV fits a concept direction from positive concept examples against random
  counterexamples and measures directional sensitivity;
- contrastive activation addition derives a residual-stream direction from
  positive/negative pairs and adds it with positive or negative coefficient;
- CLIP uses natural-language category descriptions for zero-shot visual
  classification in a jointly trained image/text space;
- one-class classification estimates a boundary from target examples, with the
  unavoidable risk of admitting too much of the unknown complement;
- concept-bottleneck models explicitly predict named concepts before a target
  and permit human intervention on those coordinates.

These are empirical learned adapters unless their carrier is finite and fully
checked. A direction that steers does not thereby prove that it is the only
representation of a concept, causally isolated, complete, or computationally
cheaper.

### 8.5 Stable Diffusion and image-generation branch

Image generation is a serious research branch, with an important reality
check: diffusion models already use an inverse-like operation. A forward noise
process is learned well enough to run a reverse denoising process. Stable
Diffusion's latent-diffusion ancestor already reduces cost by moving that
process from pixels into a compressed autoencoder latent. Classifier-free
guidance already combines conditional and unconditional score estimates;
textual inversion already learns a compact pseudo-word embedding for a concept
from a few images.

The RPRM opportunity is therefore not “discover inversion exists.” It is to
compose, type, certify, cache, and selectively materialize concept coordinates:

```text
strong image/example set
 -> concept address + receiver/root/negative-space receipt
 -> detect | add | remove | intersect | generate
 -> coarse scene macro
 -> refine only live or failed regions
 -> image + concept/latency/quality receipt
```

Possible speed mechanisms to benchmark are reusable text/concept embeddings,
specialized concept adapters, cached coarse latents, routing to a smaller
generator for a certified receiver, early acceptance of sealed regions, and
distillation of repeated multi-step trajectories into one/few-step macros.
Consistency models, latent consistency models, and adversarial diffusion
distillation already demonstrate one/few-step generation by training or
distillation. They are the speed baselines, not evidence that an RPRM wrapper
alone eliminates denoising FLOPs.

The first image experiment should freeze a small concept family with deliberate
overlaps, such as object, style, color, text/language, and arithmetic content.
Compare ordinary text conditioning, learned textual-inversion tokens, separate
positive/negative concept directions, and an RPRM concept ticket. Measure
concept precision/recall by intersection, prompt adherence, identity and
composition fidelity, diversity, FID/CLIP-like metrics only with their stated
limits, GPU time, denoiser evaluations, memory, training/amortization cost, and
hostile false positives. A fast output that loses an admitted concept or
silently fuses two coordinates fails the receiver.

## 9. Context architecture for Codex today

```text
append-only strong event ledger (cold, immutable)
        |
        v
typed Context IR + correction/supersession graph
        |
        v
sealed Context Ticket ---------> source-open(ticket, receiver, gear)
        |
        v
small receiver projection + live frontier (hot prompt)
```

Codex exposes a particularly useful lifecycle aperture. `PreCompact` can seal
the current ticket; `PostCompact` can receipt the boundary; and a
`SessionStart` hook whose source is `compact` runs before the next model request,
including an automatic mid-turn continuation. It can inject a bounded verified
ticket as developer context. `UserPromptSubmit`, local `PostToolUse`, and `Stop`
can capture exact occurrence bytes. Hosted or specialized tools may bypass tool
hooks, so that blind spot remains typed `OPEN`; the documented transcript path
is an unstable format and may be retained only as opaque cold bytes, never
silently parsed into authority.

The first build therefore has two coupled receivers:

1. **Continuity receiver:** preserve the live objective, scope, constraints,
   corrections, authority, decisions, obligations, evidence roots, and reopen
   triggers across compaction.
2. **Evidence aperture:** keep bulky shell, web, source, and agent evidence out
   of the hot path; return dispositions, roots, and only the receiver-requested
   slices. This is the main lever on repeated token transport.

A ticket should bind at least:

```text
ticket_id / state_id
schema_root, receiver_root, admitted_future_root
source_event_root, prior_ticket_root, transition/verifier roots
model, tool, policy, AGENTS, and environment roots or versions
current goal, target, authority, constraints
corrections and supersessions
open obligations and unresolved seams
evidence pointers and cold-span locators
known collision witnesses
epoch / TTL / reopening rule
```

Suggested adaptive gears:

- `G0`: exact control state—goal, target, authority, roots, open obligations;
- `G1`: compact readable ticket—current delta, corrections, anchors;
- `G2`: selected raw spans and tool receipts;
- `G3`: full transcript/source.

Upshift on a collision, missing citation/proof, changed root, correction,
authority question, tool disagreement, exact-quote request, or receiver change.
Downshift only after all live consumers and obligations factor through the
lower gear. Keep a stable cached prefix/codebook and append the smallest dynamic
event suffix.

## 10. First falsifiable build

Working implementation: personal skill `rprm-context` plus exact experiment
`RPRM_CODEX_CONTEXT_RECEIVER_01`. The inverse semantic shrinker remains a later
empirical lane behind this exact control-state compiler.

### Lane A — exact finite control receiver

1. Freeze a finite event alphabet: goal set/change, constraint, correction,
   supersession, authority change, source bind, tool result, obligation
   open/close, completion gate.
2. Freeze finite receiver operations and continuation words: current goal,
   active constraint, runnable action, source root, supersession status, next
   legal route, open obligations, completion status.
3. Interpret the full ledger as oracle; minimize histories by identical answers
   under every registered continuation.
4. Emit `state_id`, transition table, output table, roots, and separating
   witnesses.
5. Generate collision twins by changing one negation, hash, project, authority,
   tool result, supersession, attachment availability, or policy root.
6. Prove incremental update equals full replay on the complete frozen carrier.

Only this lane may initially use the word “exact.”

The first Codex-specific instantiation now passes as
`experiments/RPRM_CODEX_CONTEXT_RECEIVER_01`. Fourteen source roots and thirteen
incremental prefixes verified; a separately implemented supersession-graph
checker matched every prefix; eight questions were answered hot and three
correctly deferred; root-verified reopening resolved 11/11; 11/11 hostile twins
were distinguished; and eight isolated tests plus an independent result checker
passed. The 3,611-byte ticket is 96.35% smaller by bytes than its 99,040-byte
sealed source surface. Result root:

`D348A68C8EDC0F6EB5C9F5ACAA1C3A5A76946F7F243ECB54F0A766C59EE0B206`

This is a finite authored-control and byte-reopen result, not a hosted-Codex
quality, token, cost, latency, or usage result.

The corresponding Codex patient-zero implementation now exists at
`C:\github\rprm-context`. It installs a personal skill, marker-scoped lifecycle
hooks, a local append-only SQLite rollback-journal ledger, deterministic hot
tickets, exact root reopening, correction/supersession lineage, and bounded
post-compaction restoration. Its frozen local suite currently passes 68/68,
including atomic old/new publication, finite receiver-root resets, selected-task
isolation, SessionStart boundary movement, local publication rewind/orphan
detection, exact legacy-first-link compatibility, concurrent landing, typed
media/root drift, and Windows UTF-8 result output. The live pilot has been
explicitly re-reviewed under its nine registered receiver probes and verifies
with zero local ledger errors. Two independent read-only release reviews now
return `GO` for the exact frozen roots inside the declared local shadow ceiling;
the regenerated verification receipt and manifest form the pause still point.
Tool-output replacement remains off, and
Codex still requires the user to trust the exact hook definition through
`/hooks` before hooks execute. This is an installed shadow instrument, not yet
an empirical context-saving receipt. The full ticket still has an explicit
`O(history)` serialization floor, and coherent deletion of the local head,
successor ticket, and pointer together remains open until an external head
anchor exists.

### Lane B — black-box GPT text shrinker

Freeze the model snapshot/alias, reasoning setting, tools, system/developer
instructions, decoder settings, source corpus, receiver probes, and token
counter. Compare:

```text
B0 full raw message/history
B1 ordinary human concise rewrite
B2 narrative summary
B3 provider compaction
B4 inverse-shrunk ordinary text + source root/reopen tool
B5 inverse-shrunk ticket + provider compaction safety net
B6 aggressive approximate compressor as hostile baseline
```

Start with deletion/delta-debugging, token substitution, constrained rewrite,
beam/evolutionary search, and counterexample-guided refinement. Search cost is
part of the receipt. An expensive one-off shrink can lose overall; stable
instructions, repeated context, and reusable tickets are the first economic
targets.

Measure:

- whole-task and structured receiver agreement;
- retention of corrections, negations, authority, and open seams;
- false `ONE`, stale/superseded revival, and unsupported closure;
- token count using the actual model tokenizer;
- time to first token, total latency, requests, and search amortization;
- dynamic, cached, cache-write, reasoning, and output tokens;
- cost, repair turns, source reopen precision/recall, and reopen success;
- stability across fresh sessions and separately across model versions.

Promotion requires no new critical authority/supersession errors, no hidden
false closure, deterministic ticket bytes/root, successful reopening before an
action when a collision twin is presented, and a measured net token/cost or
quality win. Any numeric compression target is a prefrozen benchmark target,
not an RPRM theorem.

### Exploratory pilot already performed

One blind agent received only a compact mathematical packet, not the producing
conversation. It correctly reconstructed the core canonical-state idea, the
text-versus-internal-state boundary, the need for a typed aperture, and the
main falsifiable experiment. It also identified missing receiver/probe/model
definitions. This is one qualitative pass, not evidence of compression quality
or exact semantic equivalence.

## 11. Assistant operating standard — working form

1. Classify every admitted signal before granting action authority.
2. Preserve typed outcomes: impossible, unique, ambiguous, open, ill-typed,
   out-of-carrier, and terminal are not aliases.
3. Keep one immutable lineage and one user-visible terminal owner. Retries reuse
   stable identity.
4. Use deterministic machinery for settled routing, reconciliation, lifecycle,
   deduplication, and exact finite queries. Use GPT for residual judgment.
5. Move routine reversible work; escalate spend, credentials/consent, external
   commitment, subjective direction, irreversible security, and physical-world
   authority.
6. Keep the live middle visible. A timeout, missing tool, partial scan, or failed
   guard remains an obligation rather than counterfeit closure.
7. Earn look-away per lane/version/root/receiver/gate. Revoke only the affected
   cone on drift.
8. Treat summaries as FOLDs. Retain source identity and a reopening path.
9. Do not use generated memory as the sole source of must-follow rules; bind
   stable rules in authoritative project instructions.
10. Use Wizard and Druid independently for consequential claim promotion.

## 12. Software and project standard — working form

1. Declare mode: `OPEN FIELD`, `SELECTION`, `PREFREEZE`, or `AUDIT`.
2. Declare carrier, exclusions, claim ceiling, evidence floor, stopping rule,
   and unresolved seams.
3. Fence authority and blast radius before adding capability.
4. Make the canonical committed/rooted artifact—not a retelling—the handoff.
5. Type every transport and its loss: CAR, ADAPTER, or FOLD.
6. Compose literal child receipts; check new seams and parent law rather than
   replaying sealed children.
7. Verify the frontier, publish once, and conserve every obligation.
8. Reopen only the dependent cone; leave disjoint certified work intact.
9. Separate implementation from merge/deploy authority; canary and soak before
   unattended trust.
10. Never promote finite, operational, or abductive scope by rhetoric.

## 13. Polyrhythm and pipeline rule

For ideal integer cadence lane `i`, releases satisfy:

```text
t = phase_i (mod period_i)
H = lcm(period_1, ..., period_n)
```

The release-address pattern repeats over the hyperperiod `H`. Two lanes collide
exactly when their phases agree modulo the gcd of their periods. Coprime periods
therefore guarantee an eventual coincidence; they do not magically prevent
one.

RPRM can use the finite phase quotient and a proved constructor to reason about
large repetitions without enumerating every tick. But periodic releases do not
by themselves prove periodic pipeline state. Full closure needs the
hyperperiod transition to return the complete state—including queues, debt,
leases, retries, and cached state—to an equivalent starting state. External
load, runtime, clock, and provider behavior remain typed environmental
receipts.

The local polyrhythm experiment exactly demonstrates event-to-ternary phase
address coverage for frozen `(2,3)` and `(2,3,5)` schedules. It does not yet
prove universal scheduling efficiency, fairness, or a special prime law.

## 14. User correction ledger

These corrections are part of the working authority and must survive context
folding:

1. RPRM does not require checking every lane on every run. Trust is built into
   certified structure; attention moves to the live frontier and touched seams.
2. More repetitions alone do not earn trust. Proof, hostile tests, composition,
   and scoped receipts do.
3. Polyrhythm is not a numerological “prime cadence” trick. The value is a
   calculable phase quotient/constructor and compositional shortcut.
4. The `3 x 3 x 3` work is a finite proof-shaped key and shortcut donor, not a
   license to assert every large or environmental claim without typing it.
5. RPRM is a combinator/toolbox of typed dimensional shortcuts, not a philosophy
   prompt or worship of numbers.
6. Wizard and Druid mean exact intelligence plus receiver/purpose wisdom—thinkers
   and yearners—not merely multiple clever agents.
7. The master assistant guide is living and must be corrected interactively;
   do not prematurely finish, freeze, and merely hand it over.
8. Context management is the first current bottleneck, ahead of the broader
   interim package list.
9. “Zero” means a canonical receiver state/equivalence address, not deletion or
   scalar zero.
10. Sending token IDs or vectors through a text aperture does not bypass
    translation. The more promising inverse is the shortest accepted ordinary
    text in the same receiver-behavior fiber.
11. Do not train the receiver first. Put an unconstrained searcher inside a
    constrained room; let a trusted semantic-and-length door admit a one-token
    shorter output, then repeat.
12. A broader inverse rotates a learned concept relation: the same concept
    address may be queried for recognition, generation, verification,
    addition/suppression, and complement under a frozen universe.
13. Concept partitions are generally overlapping intersections, not exclusive
    buckets. Apparent false positives remain open evidence that may expose an
    error, proxy, polysemy, or a previously unnamed broader invariant.
14. Stable Diffusion/image generation is an explicit research branch, but
    inversion and few-step distillation already exist there. RPRM must win a
    frozen speed/quality/composition benchmark rather than claim automatic
    acceleration.
15. The Korean example meant supplying actual Hangul glyphs/text as positive
    occurrences, not supplying the English label “Korean.” Keep separate the
    receivers `contains Hangul code points`, `uses Hangul script`, `is Korean
    language`, and `looks Hangul-like`.
16. Naribrain is intentionally in maintenance and is outside this investigation.
17. The context patient zero is Codex itself, not Nari. Improve the assistants'
    own context efficiency before applying the method downstream.
18. Context work is the oxygen mask: preserve correctness across compaction and
    reduce repeated hot evidence transport before resuming the deferred list.
19. `RPRMZipperLab` predates the final key and is not authority. Reuse only
    implementation mechanics that have been re-derived against current RPRM.
20. A compaction ticket alone protects continuity but does not stop context
    regrowth. Bulky tool and research outputs need a typed cold evidence
    aperture with narrow by-root reopening.
21. Subagents should not inherit a saturated parent history by default. Give
    them a typed task packet, source roots, and only the minimum recent turns.
22. Count post-compaction growth after the carried prefix; do not let the
    already-folded interior consume the next compaction allowance again.
23. Reasoning effort is a receiver gear, not a virtue score. Benchmark routine
    work below `ultra`; reserve maximum reasoning and automatic delegation for
    tasks whose branching structure earns it.
24. The Codex context ledger must not use SQLite WAL on the present 3.50.4
    runtime. Hook concurrency plus an unfixed WAL-reset race is incompatible
    with a trust substrate; use rollback journaling until a fixed version is
    receipted.
25. The prime translator has the exact local radius-one definition
    `PrimeWindow(n,1) = (p_{n-1}, p_n, p_{n+1})`: predecessor, current prime,
    and successor. Preserve this as a typed local window donor. No scheduling,
    semantic-compression, or universal translation advantage follows without
    a separately named receiver and composition proof.
26. React is a promising RPRM-shaped software donor: parent/child ownership,
    one-way data flow, state-to-view projection, and effect boundaries resemble
    typed enclosures and receiver folds. The desired “safe React” direction is
    proactive/mechanical admission—compile legal state, event, ownership, and
    effect relations; expose the vacant/invalid seam before execution; and
    recheck only the affected subtree—instead of discovering violations as
    repeated runtime or lint complaints. This is a hypothesis and design lane,
    not yet a React optimization or correctness theorem.
27. Optional discovery lens—not a required workflow: when a small carrier is
    opaque, try lifting it one binary level (for example, one-of-four into a
    one-of-eight address carrier), solve where the extra coordinate exposes a
    check bit, inverse, or relation, and then descend. Admit the shortcut only
    with an explicit embedding and descent satisfying `D(E(x)) = x` on the
    declared states, and account for all answer information: one parallel
    question round may return several bits even though it is one round. Also
    keep the lighter checks alive: is there an inverse/mirror, and have we
    doubled far enough to make the hidden relation visible?
28. `Dark World` is William's deliberately non-mystical project term for a
    declared reflected/negative carrier at zero, negative one-half, and below,
    outside the positive gap. The name alone does not choose between additive
    negation, inverse navigation, reciprocal, complement, divisor shadow, or
    order dual. Type the intended operation before transporting a claim.
29. Store exact content once where it originates and store the receiver-needed
    projection where it is consumed. A hot cheat sheet remains a reopenable
    `FOLD`; deleting its rooted ancestry converts it into irreversible
    forgetting. Permit that only after a named finite receiver proves every
    promised future factors through the capsule, or after explicit user
    authorization to forget. Exact-quotation receivers ordinarily keep the
    source cold.
30. Mutation is one atomic `Flick`, not a visible open-edit-close workflow:
    `sealed_next = Flick(sealed_now, event, receiver)`. Planning, solving two
    coordinates to obtain the third, validation, addition, deletion, and edit
    occur privately inside the enclosure. Publication exposes only the old
    complete root or the new complete root plus receipt. `OPEN` names an
    unresolved mathematical/evidence aperture, not a half-mutated runtime
    phase; failure leaves the sealed root unchanged.
31. Prove the scaling recurrence of the constructor before using a large run.
    The context target is hot state proportional to the live frontier, open
    obligations, active corrections, conflicts, and open reasons; transition
    work proportional to the touched dependency cone; and one rooted cold copy
    proportional to unique source bytes. Finite hostile tests check the
    constructor and larger runs only falsify or measure it. Growth outside the
    derived bound is evidence of an omitted seam/debt/receiver and resets
    promotion. The current ticket's historical root/coverage arrays are an
    explicit `O(history)` spool violation to remove, not something a larger
    benchmark can excuse.
32. The car-off-the-road / spinning-saw analogy gives a useful operational
    factorization: `x --lift--> z --F^k--> z' --land--> x'`. Lift the work into
    an isolated carrier where search, rotation, and composition can run without
    giving every microstep world-level consequence; then land once through the
    atomic `Flick`. The speedup disappears if internal rotations append public
    history. Landing must match receiver, orientation, source roots, and
    conserved obligations; a mismatch is `OPEN_LANDING_SEAM` and leaves `x`
    current. The dark/reflected carrier names the lifted working space only
    after its inverse/mirror operation is typed; the analogy does not by itself
    prove a universal shortcut. On a proved periodic carrier, compute the next
    candidate contact as `theta' = theta + k*omega (mod H)` and land only when
    its typed aperture is `ONE`: continuous/private phase, sparse/public
    contact, with no need to materialize the intervening rotations.
33. Bound infinity out of every operational enclosure. Declare
    `C_R = [1/2, Omega_R]`, with `Omega_R` the receiver-relative last
    structurally new case. Beyond it, continue only by an earned recurrence or
    composition receipt. If continuation needs another coordinate, number/type,
    receiver, or generator, stop with `OPEN_NEW_CARRIER`; do not silently make
    the old mechanism reason over infinity. For Codex context, arbitrary future
    natural-language behavior is outside the hot receiver: retain finite
    continuity probes and reopen or change receivers when a separating future
    arrives.
34. Treat bounded-infinity navigation as nested viewfinders, not as a search
    toward infinity. `Omega_R` is the fixed outer boundary containing every
    structurally admitted sub-boundary for receiver version `R`; `F_n` is the
    movable inner frontier needed for the present answer. Learning backward
    means starting from the receiver-visible result, shrinking or relocating
    `F_n` through separating counterexamples, and retaining the smallest
    certified boundary through which that result factors. A more accurate
    frontier should reduce work because changing the viewfinder is cheap and
    the landed answer is nearer. Moving `F_n` is ordinary learning inside the
    enclosure; discovering a genuinely new kind of probe or coordinate does
    not stretch `Omega_R` silently, but versions the receiver and requires a
    new outer-closure receipt `Omega_{R+1}`.
35. Treat unqualified words such as “every,” “all,” or “anything” as a warning
    that a hidden unbounded carrier may have entered the proof. Replace the
    phrase with a named finite set, boundary, prefix, probe registry, or one
    immediate seam. For context publication, do not justify a landing by
    scanning indefinite ancestry. The hot enclosure is the prior sealed head,
    one admitted delta, one proposed successor, and one landing receipt. Older
    ancestry is cold behind a root. A coherent deletion beyond the locally
    visible head is not solved by more scanning; it requires an external head
    anchor and otherwise remains outside the claim.
36. A repeated centered half is a product-coordinate occurrence before it is
    arithmetic. On a normalized binary axis, `x -> x-1/2` gives
    `{-1/2,+1/2}`; therefore `(-1/2,-1/2)` retains two bounded coordinates.
    Do not silently turn that pair into scalar `-1`, temporal repetition, or
    two applications of negation. A sum, projection, inverse, or shadow readout
    requires its own typed receiver and fiber. Keep this distinct from the
    complementary two-lane balance `(1/2,1/2) --S-R--> 0`.

## 15. Paste-ready briefing for a new assistant

```text
You are entering an RPRM task. Treat the following as a working key, not a
universal theorem.

RPRM studies typed relations with declared roles and one vacant role/APERTURE.
Solving the aperture yields a completion fiber NONE, ONE, or MANY. Ill-typed,
out-of-carrier, timed-out, or unresolved cases remain OPEN/EVENT. Preserve
ports, orientation, incidence, source identity, and lineage. A CAR is
invertible; an ADAPTER/FOLD is receiver-faithful but lossy and must retain a
source-reopen path.

The trust cycle is OPEN -> PROVE -> SEAL -> FOLD -> INHERIT, with only the
affected dependency cone reopened when a bound root, receiver, verifier,
adapter, policy, seam, or obligation changes. Do not replay certified interiors
or poll every lane forever. A scheduler may feed work but cannot manufacture
authority or truth.

RPRM is not numerology. Finite ternary/cubical results are exact shortcut
donors inside their frozen carriers. Scale comes from proved constructors,
composition, and receipts; explicit materialization still costs what it costs.

As an optional discovery lens, an opaque small carrier may be lifted one binary
level, solved where a check bit or inverse becomes visible, and descended only
after verifying the embedding/descent round trip and retaining the information
receipt. This is a prompt to look, not a mandatory recursive procedure.

`Dark World` means the explicitly declared reflected/negative carrier, not
mystical or physical content. Always name which inverse, mirror, or complement
is being used.

On a normalized binary product, retain repeated centered halves as coordinates:
`(0,0) -> (-1/2,-1/2)`. Do not collapse the pair to scalar `-1` or treat it as
repeated negation unless a named receiver explicitly performs that fold. The
balanced complementary pair `(1/2,1/2)` and its zero readout are another typed
carrier.

Use both Wizard and Druid: verify the mechanism and falsifiers, and separately
verify that the receiver, carrier, purpose, costs, and consequences are right.
Label claims FINITE, OPS, CONTRACT, SCOUT, HYPOTHESIS, or OPEN.

Current priority: measure the installed Codex shadow context layer. Maintain an
append-only typed task ledger, compile the smallest receiver-sufficient hot
ticket before compaction, restore it immediately after compaction, and retain
bulky evidence cold behind content roots. Reopen only the affected source slice
when a separating future, correction, authority question, exact quote, or root
change appears. Anything not captured or classified stays OPEN. Do not promote
active tool folding or claim token savings until the real Codex lane passes.

Treat every published state change as one atomic Flick from an old sealed root
to a new sealed root; never expose open-edit-close intermediate mutation. Derive
the constructor's hot-state and touched-cone recurrence before scale testing.
If a ticket grows with complete history rather than the live receiver frontier,
the construction is not yet RPRM-scaled and must be reopened. A cheat sheet may
replace its source only for a named receiver-complete future or by explicit
authorization to forget; otherwise retain a content-rooted reopening path.

For multi-step internal work, use lift-spin-land: lift the old state into an
isolated carrier, evolve there without publishing each microstep, and land once
through a receiver-checked seam. A failed landing leaves the old sealed root in
place. Never turn private rotations into an append-only public-history spool.

Bound the receiver as `C_R=[1/2,Omega_R]`: enumerate only structurally new
cases through its finite endpoint, then use a proved recurrence. A continuation
requiring a new type/coordinate returns `OPEN_NEW_CARRIER`; never smuggle
untyped infinity into the hot context promise.

Navigate that bounded carrier with nested viewfinders. Keep the admitted outer
boundary fixed for a receiver version while counterexamples move the inner
live frontier toward the smallest sufficient fiber. If the outer boundary must
move because a new kind of future has appeared, create a new receiver version
and closure receipt instead of laundering the change as ordinary scaling.

The inverse semantic shrinker is the next empirical lane: freeze a receiver
signature R_Phi, then search backward for the shortest ordinary-text z such
that R_Phi(z)=R_Phi(original). Iteratively admit one-token-shorter candidates
through an external typed verifier. The generator inside the room is untrusted;
the door, probes, roots, and receipts are trusted. Failure to find a candidate
is OPEN unless a finite carrier was exhausted.

Before acting, declare your task receiver, authority, open seams, evidence
floor, and claim ceiling. Carry forward the user correction ledger in the
master guide and append new corrections rather than silently rewriting them.
```

## 16. Primary local anchors and external interfaces

Local anchors:

- `RPRM_KERNEL_STILL_POINT_2026-08-12.md`
- `RPRM_BRIDGE_FAMILIES_FULL_REREAD_UNDERSTANDING_PACKET_2026-08-12.md`
- `RPRM_RECEIVER_COMPLETE_FOLD_KERNEL_0_4_SHADOW.md`
- `RPRM_ADAPTIVE_FUTURE_SIGNATURE_GEAR_SCOUT_0_1_SHADOW.md`
- `RPRM_SELF_ZIPPING_INCREMENTAL_FRONTIER_SCOUT_0_1_SHADOW.md`
- `RPRM_NESTED_SUBCUBE_CERTIFICATE_SCOUT_0_1_SHADOW.md`
- `RPRM_WIZARD_DRUID_COMPILER_PROTOCOL_0_1_2026-08-12.md`
- `GPT_ASSISTANT_UPGRADE_WIZARD_01.md`
- `GPT_ASSISTANT_UPGRADE_DRUID_01.md`
- both reciprocal assistant reviews
- `GPT_ASSISTANT_UPGRADE_COMPILER_SYNTHESIS_01.md`
- `experiments/RPRM_CODEX_CONTEXT_RECEIVER_01/PROTOCOL.md`
- `experiments/RPRM_CODEX_CONTEXT_RECEIVER_01/RESULTS_SUMMARY.md`
- frozen experiment summaries for Corner Key, Full-Zip Hypercube Ladder,
  Polyrhythm Event-to-Ternary Grid, Four-Triplet Carrier, and PATH/IOU.

Concept and image research neighbors:

- TCAV: <https://arxiv.org/abs/1711.11279>
- Concept Bottleneck Models: <https://proceedings.mlr.press/v119/koh20a>
- Contrastive Activation Addition: <https://arxiv.org/abs/2312.06681>
- CLIP: <https://arxiv.org/abs/2103.00020>
- Latent Diffusion: <https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html>
- Classifier-Free Guidance: <https://arxiv.org/abs/2207.12598>
- Textual Inversion: <https://arxiv.org/abs/2208.01618>
- Consistency Models: <https://proceedings.mlr.press/v202/song23a.html>
- Latent Consistency Models: <https://arxiv.org/abs/2310.04378>
- SDXL-Lightning: <https://arxiv.org/abs/2402.13929>

Current OpenAI interface references:

- Compaction: <https://developers.openai.com/api/docs/guides/compaction>
- Prompt caching: <https://developers.openai.com/api/docs/guides/prompt-caching>
- Latency optimization: <https://developers.openai.com/api/docs/guides/latency-optimization>
- Codex hooks: <https://learn.chatgpt.com/docs/hooks>
- Codex configuration reference:
  <https://learn.chatgpt.com/docs/config-file/config-reference>
- Codex skills: <https://learn.chatgpt.com/docs/build-skills>
- AGENTS instructions: <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- Memories: <https://learn.chatgpt.com/docs/customization/memories>

Current ceiling:

`LIVING_SYNTHESIS__CODEX_PATIENT_ZERO_SHADOW_INSTALLED_HOOK_TRUST_PENDING__FINITE_CONTROL_RECEIVER_PASS__HOSTED_CODEX_BENEFIT_OPEN__INVERSE_SHRINKER_NOT_YET_BENCHED__NO_MODEL_INTERNAL_ACCESS_CLAIM__NO_UNIVERSAL_SEMANTIC_COMPRESSION_CLAIM`
