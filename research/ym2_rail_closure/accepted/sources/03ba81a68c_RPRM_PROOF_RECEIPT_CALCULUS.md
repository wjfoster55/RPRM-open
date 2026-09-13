# RPRM proof-receipt calculus 0.1

## Status

This note formalizes two small results needed by `RPRM-MATH-KERNEL-0.1`:

1. finite-word preservation from a successor-congruent quotient;
2. associative composition of exactly scoped receipts with one-count
   obligations.

Both are elementary structural theorems, not novelty claims. The value here is
the explicit typing and failure boundary. A receipt is not proposed as a new
truth value; it is the reusable interface needed when downstream work observes
assumptions, scope, seams, obligations, or witnesses.

Lean 4 was not found locally, so the ticket's no-Lean fallback was used. The
finite definitions and countermodels are executable in the standard-library
[model finder](countermodels/finite_model_finder.py), checked by the
[focused tests](countermodels/test_finite_model_finder.py), and frozen in the
[exact JSON result](countermodels/results/countermodels_frozen.json). Source
and artifact hashes are in the [pre-source
receipt](countermodels/receipts/PRE_SOURCE_RECEIPT.json) and [post-artifact
receipt](countermodels/receipts/POST_ARTIFACT_RECEIPT.json).

## 1. Predictive system

Fix a declared context with:

```text
S       states
A       primitive action alphabet
T_a     deterministic transition S -> S for every a in A
Y       observation carrier
O       observation map S -> Y
Q       proposed quotient-key carrier
K       key map S -> Q
```

The theorem does not require `S`, `A`, or `Q` to be finite. Totality is assumed
only to keep the notation small. For partial moves, add the condition that
states with equal keys have equal definedness under each admitted action, then
apply the proof on the common defined domain.

For finite words `w in A*`, define execution by

```text
T_empty(s) = s
T_(w a)(s) = T_a(T_w(s)).
```

The empty word is the typed no-move identity. Word concatenation supplies
transition composition; no untyped global identity is introduced.

### Definition 1 - present observation consistency

`K` is observation-consistent when

```text
K(s) = K(t)  implies  O(s) = O(t).
```

The equality on `Q` and equality on `Y` are typed judgments. They need not be
literal state identity.

### Definition 2 - primitive successor congruence

`K` is successor-congruent when, for every `a in A`,

```text
K(s) = K(t)  implies  K(T_a(s)) = K(T_a(t)).
```

Present observation consistency alone is not enough. The frozen three-state
countermodel merges states `0` and `2` with equal present observations, but one
`a` step sends them to different quotient keys.

## 2. Finite-word successor-congruence theorem

**Theorem FWSC.** Assume deterministic transitions, present observation
consistency, and primitive successor congruence as declared above. Then for all
states `s,t` with `K(s)=K(t)` and every finite word `w in A*`,

```text
K(T_w(s)) = K(T_w(t))
and
O(T_w(s)) = O(T_w(t)).
```

### Proof

Induct on the length of `w`.

- **Base:** `w=empty`. The key equality is the hypothesis `K(s)=K(t)`. The
  observation equality follows from present observation consistency.
- **Step:** suppose the key equality holds after a word `w`. For any primitive
  `a`, successor congruence applied to `T_w(s)` and `T_w(t)` gives

  ```text
  K(T_a(T_w(s))) = K(T_a(T_w(t))).
  ```

  By the definition of word execution this is the key equality after `w a`.
  Present observation consistency applied to that equal key gives equality of
  final observations.

Thus both conclusions hold for every finite word. QED.

### Corollary - quotient action is well-defined

For each primitive action define

```text
bar_T_a(K(s)) = K(T_a(s)).
```

Successor congruence makes the right side independent of the representative
`s`. Hence primitive quotient actions are well-defined, and their finite
compositions compute `K(T_w(s))`. This is the exact condition under which a
proved word may be Flattened on the declared quotient domain.

### Executable regression versus proof

The finite finder exhausted 5,898 deterministic systems on state sizes one
through three, with binary alphabet and binary observations. It checked 7,106
merged pairs in observation-consistent congruences for every word through
length 5 and found zero failures. That run verifies the implementation. The
induction above, not the finite panel, discharges the unbounded finite-word
quantifier.

## 3. Why a finite horizon is not a receipt for `A*`

Let `L_h` contain the words of length at most `h`. For every `h >= 0`, define a
unary deterministic system with states `0,...,h+2`, transition

```text
i -> min(i+1,h+2),
```

and observation 1 only at state `h+2`. Starts 0 and 1 have identical
observations for every word in `L_h`; the word of length `h+1` distinguishes
them. Therefore

```text
FutureSame_(L_h)(0,1)
```

does not imply

```text
FutureSame_(A*)(0,1).
```

At `h=1`, exhaustive search proves four states are minimal within the declared
unary/binary-observation signature. The frozen witness and complete census are
in `countermodels_frozen.json`.

A finite-horizon receipt can be promoted to an open-ended one only through a
separate extension theorem - for example FWSC, an induction invariant, or
another valid compactness/closure argument with its assumptions recorded.
Changing the scope label without that proof is not receipt composition.

## 4. Receipt type

The operational record may contain source hashes, checker versions, witness
decoders, and novelty labels. The mathematical composition core uses the
following fields.

```text
Receipt r = (
  input_r,                 typed input judgment
  output_r,                typed result judgment
  scope_r,                 theory, assumptions, state domain,
                           equality/observation, continuation language
  seam_in_r, seam_out_r,   typed interface identities
  proof_r,                 flattened finite derivation-token sequence
  credit_r                 finite partial map:
                           obligation identity -> one typed destination
)
```

`scope` is treated as one structured value. In this minimum calculus, two
scopes compose only by exact equality. A weakening, substitution, base change,
or scope-extension theorem can be represented as its own receipt; it is not a
silent coercion.

`credit` is a partial map rather than a number. An obligation identity appears
at most once, with one destination. A divisible obligation must first be
replaced by explicitly identified parts whose recombination is separately
receipted.

### Definition 3 - receipt compatibility

Receipts `r` and `s` are directly composable, written `r ; s`, exactly when:

1. `output_r = input_s` as typed judgments;
2. `scope_r = scope_s` exactly;
3. `seam_out_r = seam_in_s` as typed seam identities;
4. `dom(credit_r)` and `dom(credit_s)` are disjoint.

The fourth condition is the minimum no-double-credit rule. A shared seam is
matched by condition 3; it is not republished as a second obligation credit.

When compatible, define

```text
r ; s = (
  input_r,
  output_s,
  scope_r,
  seam_in_r, seam_out_s,
  proof_r ++ proof_s,
  credit_r union credit_s
).
```

The concatenated proof sequence is flattened, so syntactic parentheses are
not preserved as semantic distinctions. Source subreceipts may remain linked
in an archive without becoming extra active credits.

## 5. Scoped receipt-composition theorem

**Theorem SRC.** Let

```text
r : A -> B
s : B -> C
t : C -> D
```

be receipts with one identical scope, matching consecutive seams, and pairwise
disjoint credit domains. Then both `(r ; s) ; t` and `r ; (s ; t)` are defined
and are the same canonical receipt.

### Proof

Endpoint matching gives `A -> D` under either parenthesization. Exact scope
equality is transitive, so both composites retain the same scope. Consecutive
seam matching removes the two internal interfaces and leaves `seam_in_r` and
`seam_out_t` in both cases.

Finite-sequence concatenation is associative:

```text
(proof_r ++ proof_s) ++ proof_t
  = proof_r ++ (proof_s ++ proof_t).
```

Pairwise disjointness makes both partial-map unions defined, and union is
associative:

```text
(credit_r union credit_s) union credit_t
  = credit_r union (credit_s union credit_t).
```

Every field of the canonical receipts is therefore equal. QED.

### Typed identities

For judgment `A`, scope `sigma`, and seam `e`, define

```text
id_(A,sigma,e) = (A,A,sigma,e,e,empty_proof,empty_credit).
```

Choosing `e` to match the adjacent seam gives the corresponding left or right
identity. There is no claim of one context-free global receipt identity.

### Conditional semantic soundness

SRC is a structural theorem about receipt records. If a checker soundly
validates each primitive proof token and its sequential rule, then validating
the flattened composite derives the endpoint conclusion under the retained
scope. The calculus does not derive checker soundness from the record itself;
checker semantics are an explicit assumption.

## 6. Shortest receipt counterexamples

### Scope mismatch

The frozen pair has

```text
r : P -> P under assumption scope alpha
s : P -> P under assumption scope beta
```

Both use observation scope `all_words` and seam `s`. Endpoint-only composition
returns true; Definition 3 returns false at the assumption-scope field. This is
minimal for a binary mismatch: one receipt cannot fail pairwise composition,
two scope values suffice, and only one endpoint is needed.

The example does not say that results under `alpha` and `beta` can never be
related. It says the relation must be an explicit assumption-transport or
scope-change receipt.

### Double credit

Suppose `r` and `s` each publish a credit for obligation identity `c`. Even if
the destinations print the same, composing by numeric addition counts the same
obligation twice; composing by ordinary set union silently erases the fact that
two publications occurred. Definition 3 rejects the overlapping domains.

An intentional split uses fresh child identities, for example `c.left` and
`c.right`, plus a receipt that their exact sum or join discharges `c` once.
The split is data, not an inference from matching units.

The executable negative control gives the same ablation test at the role
level. A lower object already contains the type read by its receiver; adding a
second external `x:T` changes nothing, and removing it changes nothing. The
alleged `+1` is already credited inside the object.

### Finite scope mislabeled open-ended

The chain family above supplies a receipt valid for `L_h` and a shortest word
outside that scope that reopens it. Since `L_h != A*`, exact scope composition
forbids relabeling it as an open-ended receipt. FWSC can provide the missing
extension only after its one-step hypotheses are independently checked.

## 7. Witness and inverse obligations

A decision receipt and a constructive receipt are different types. When the
conclusion claims an existential object, the full operational schema should
add:

```text
witness_type
witness_decoder
decoder_domain
decoder_cost or size bound when complexity matters
checker for the reconstructed witness
```

This matches the SAT calibration: existential bucket elimination retains
reverse choice tables. A final nonempty bit is not by itself a satisfying
assignment, and a compact backward representation is not a polynomial
shortcut if nonemptiness or witness lifting remains hard.

## 8. Programmed-versus-derived boundary

**Definitions/programmed:** the receipt fields, exact-scope policy, seam
matching, disjoint-credit rule, deterministic transition signature, and finite
test carriers.

**Proved/derived:** FWSC; its quotient-action corollary; SRC associativity and
typed identities; the all-horizon reopening family; and the frozen finite
censuses and counterexamples relative to the programmed signatures.

**Conditional:** semantic soundness of composed proof tokens depends on the
declared checker's soundness. Independent authority depends on the receiver's
issuer-checking rule. Complexity claims require explicit representation and
checker cost receipts.

**Not claimed:** proof relevance for every proposition, a universal authority
layer, non-internalizability in every reflective foundation, a new theorem of
category or proof theory, or closure of any Millennium bridge.

## 9. Integration rule

The predictive kernel and receipt extension should remain separable:

```text
predictive closure:
  state + lawful move + observation + continuation language + congruence

receipt/accounting closure:
  assumptions + scope + seam + proof/witness + unique obligation destinations
```

Zero predictive defect does not imply zero receipt remainder, and a balanced
receipt ledger does not imply successor congruence. A result may be Flattened
only after both closures required by its downstream claim are independently
receipted.
