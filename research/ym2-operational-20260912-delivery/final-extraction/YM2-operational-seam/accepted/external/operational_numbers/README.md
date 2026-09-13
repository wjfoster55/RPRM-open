# RPRM Operational Number Translator

This directory turns a numeral or digit string into a **bundle of typed,
concurrent affordances**. It does not assign a single hidden meaning to a
number. It keeps arithmetic facts, declared transforms, dependent shadows,
RPRM readings, and abductive proposals in separate lanes so they can be used
together without being confused.

The declared decimal maps include the nines-flip `M(d)=9-d`. Before applying
any gap filter, every adjacent ordered digit pair now receives a signed-pair
receipt. It retains `signed_gap=B-A`, `centered_sum=A+B-9`, the source, swap,
coordinatewise `M`, and `O after M` words, the complete four-operation orbit,
the full base-10 signed-gap fiber, and exact recovery from the two coordinates.
The receipt is an exact declared-map result derived from the supplied source;
it is not an independent stream.

For the decimal four-state cell:

| operation | word | `(centered_sum, signed_gap)` |
| --- | --- | --- |
| source `I` | `35` | `(-1,+2)` |
| swap `O` | `53` | `(-1,-2)` |
| coordinatewise `M` | `64` | `(+1,-2)` |
| fold `O after M` | `46` | `(+1,+2)` |

The negative signed gap alone has eight decimal words, so it is `MANY(8)`,
not `ONE(64)`. Adding `centered_sum=+1` recovers `ONE(64)`. The name
`signed_gap` is reserved for `B-A`; it must not silently replace `gcd`, for
which `gcd(3,5)=1` and `gcd(4,6)=2` even though both `35` and `46` have signed
gap `+2`.

The pre-existing ascending gap-two receiver remains separate and unchanged.
It types qualifying pairs into the eight-rung decimal tower with coordinatewise
`M`, the ascending fold `O after M`, chart visibility, and carry state. Thus
`35` reports `M(35)=64` and `O(M(35))=46` without treating the two orientations
as rival answers. Input `64` still receives its signed-pair receipt even though
it is rejected by that ascending-only filter.

Every report now attaches a lexical-carrier receipt before punctuation is
removed. Context-free syntax returns a candidate fiber rather than a forced
meaning: `3.5`, `3/5`, `3+5`, `3,5`, timestamps, versions, dates, and UUIDs
may share the normalized digit view `35` (or contain it) without becoming the
same source object. Exact plain digit strings remain backward-compatible.

The first use case is the Pi eleven-digit window and the questions around
"anti-Pi", fake six/eight, `1234679`, and the `9|1` carry brink. The machinery
is generic over decimal digit strings; Pi-specific facts are opt-in through
`--profile pi-window`.

## Evidence lanes

| Lane | Meaning |
| --- | --- |
| `EXACT_ARITHMETIC` | Recomputed ordinary arithmetic. |
| `EXACT_DECLARED_MAP` | Recomputed under an explicitly named finite map. |
| `DERIVED_DEPENDENT` | Exact output derived from the supplied source; not independent evidence. |
| `RPRM_READING` | A preserved operational lens with a stated scope and missing receiver. |
| `OPEN_HYPOTHESIS` | A testable candidate, not yet a reusable rule. |
| `SCOUT_PROPOSAL` | Bounded vibe-generation output; never authority or evidence. |

## Run it

```powershell
python -B operational_numbers\translate_number.py 31415926535 --profile pi-window --scout
python -B operational_numbers\translate_number.py 64 --scout
python -B operational_numbers\translate_number.py 1234679 --scout
python -B operational_numbers\translate_number.py 8 --scout
python -B operational_numbers\verify.py
```

The output is deterministic JSON. `--scout` adds a few colloquial prompts of
the form "this may be acting like..." and records which exact receipt inspired
each prompt. The scout cannot edit registries, select experiments, promote
claims, or impersonate a human receiver. The bounded `64` anti-mirror prompt
explicitly retains its `M` lineage and never calls the derived word an
independent anti-Pi source.

## Interpretation rule

Numeral equality permits multiple lenses to be inspected. It does **not** make
their construction histories interchangeable. Thus an `8` may concurrently
admit `2^3`, `2x4`, an image under `P`, and William's paired-four reading; a
claim that needs one of those histories must still name and verify its adapter.

The attached Fable legend remains unmodified under `lexicon/`. Its claim audit
is [PI_CLOSURE_LEGEND_AUDIT.md](PI_CLOSURE_LEGEND_AUDIT.md), and exact source
identities are pinned in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json).
