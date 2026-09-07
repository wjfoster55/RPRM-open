# Music Lens

**Experimental playground, 2026-09-07.** An interactive companion to the
[symbolic music experiment](../music/README.md). Move a six-note phrase and
watch a piano roll, pitch-class dial, and rhythm wheel respond. Optional sound
turns the same events into a quiet synthesized loop.

Open [index.html](index.html) directly from local files in a modern browser.
There is no build, installation, account, sample download, tracking, or remote
dependency. It is included in the repository's [experimental packs](../README.md).

## Start with these three moves

1. Press **Play**. A repeating four-beat bar moves through the views. Turn
   **Sound on** if you want to hear it; visual playback works without audio.
2. Press **+ octave**. Every note rises by twelve semitones. The piano roll
   changes, but the pitch-class dial is identical: it cannot distinguish
   C4 from C5. Their actual pitches remain in the source.
3. Move **Rhythm rotation**. Notes pass across the edge of the bar while
   keeping their cyclic spacing. This changes the starting position, not the
   cyclic pattern.

Drag any note up or down while **Pitches linked** is on to move the melody
without changing its signed intervals. Turn the link off to edit just one
note. The A–F buttons and the **Note** range provide a keyboard alternative.
The allowed range reflects the current phrase, so an edit never silently
wraps a high note into a low note.

**Flip pitches** reflects the contour around A. **Reverse rhythm** reflects
onsets around the retained phrase origin. Each operation is its own inverse;
try it twice. The three starting phrases are newly specified synthetic note
patterns, not recordings or quotations from songs. Reset restores Open sky,
the default tempo, and the linked editor, and stops playback. A confirmed
sound preference remains on until toggled off or the page is reloaded.

## One source, distinct views

| View | What it reads | What it forgets |
|---|---|---|
| Piano roll | Every labelled event's absolute pitch and onset in the bar | The separate phase/relative-step decomposition; drawn pixels also round positions |
| Pitch classes | Absolute pitch modulo 12, with a count at occupied classes | Octave/register, onset, and individual occurrence assignment at a class |
| Rhythm wheel | Absolute onset modulo 16, with event labels and pitch-class colors | Absolute pitch register and the separate phase/relative-step decomposition |
| Interval readout | Consecutive signed differences in **label order A–F** | Absolute root; it is not chronological order after a rhythm transform |
| Gap readout | The sorted multiset of six cyclic onset gaps | Onset order, event assignment, and rotation; equal gap multisets need not mean the same rhythm |
| Optional audio | The supplied 12-TET tuning, tempo, and short synth envelope | It is a playback adapter, not an inverse or a perception measurement |

The pitch dial is a **chromatic** circle: adjacent positions differ by one
semitone. It is not the circle of fifths. Colors are a fixed, deliberately
chosen twelve-entry palette indexed by pitch class; they do not assert a
natural equivalence between sounds and colors.

## Exact bounded model

The source retains `{root, phase, steps, offsets}`:

- Six ordered occurrence labels A–F survive even when pitches coincide.
- `root` is an integer MIDI label 48–72, with A's pitch offset zero.
- Six pitch offsets are integers in `[-12,12]`; the first is zero.
- Six **distinct** relative onset steps lie in `Z/16Z`.
- The retained phase lies in `Z/16Z`.
- Actual note labels are consequently in 36–84. Their integer pitches do
  not wrap. Standard note-name spelling uses C4 for MIDI 60 and sharps.

Admission rejects booleans, fractions, nonfinite values, extra fields,
duplicate onset steps, wrong arity, and out-of-carrier states. Successors are
immutable copies. The complete source record, not any single display, is the
receiver-sufficient representation used for subsequent edits.

For event `i`, the forward maps are:

```text
midi[i] = root + offsets[i]
onset[i] = (phase + steps[i]) mod 16
pitchClass[i] = midi[i] mod 12
```

### Pitch transport and its edit aperture

Setting a new root changes every MIDI label by the same integer delta. Thus
every ordered difference `midi[j]-midi[i]` is unchanged. A fixed-delta shift
has inverse `-delta` wherever both source and destination are admitted.
The UI's absolute root setter needs the old root to undo that edit; it is not
an independently invertible state operation with forgotten history.

Moving one selected pitch with the link enabled solves
`newRoot = targetMidi - offsets[selected]`, then admits that root. With the
link disabled, only that absolute pitch is replaced, and the phrase is
re-encoded. Editing A changes root and the other stored offsets while keeping
the other five absolute pitches fixed. If the proposed result exceeds a
root/offset bound, the model rejects it atomically. The UI clamps dragging to
the complete feasible target interval supplied by `pitchMoveBounds`.

Pitch reflection is `offsets[i] -> -offsets[i]`. It negates signed pitch
differences and preserves their absolute values. It does **not** preserve the
signed interval pattern. Applying it twice is the identity on this carrier.

### Rhythm transport and the movable seam

Setting a new phase translates every onset by the same element of Z16,
preserving all directed cyclic differences. Notes can cross the visual bar
cut and change chronological list order. Their labelled source identity and
relative cyclic placement remain retained. A fixed phase translation is
inverted by its negative; an absolute phase setter needs its old value to undo.

Rhythm reflection is `steps[i] -> -steps[i] mod 16`, retaining the phase.
Equivalently, it sends each absolute onset to `2*phase-onset mod 16`.
It reverses directed cyclic differences, preserves the sorted gap multiset,
and is self-inverse. It is not merely a rotation.

### Complete fibers and limits

Retaining the full source returns `ONE` reconstruction of that record. A
readout that keeps all labelled pitches and absolute onsets still forgets
the phase/relative-step split. For any admitted event list, each of the 16
possible phases determines exactly one relative-step tuple by subtraction:
its complete source fiber is **MANY(16)**. No condition forces `steps[0]=0`
in the model, though the three UI starting phrases happen to use it.

For one fixed event onset and pitch class, the complete admissible MIDI fiber
within the note-label carrier 36–84 is `{n in 36..84 : n mod 12 = class}`.
For class C it is `{36,48,60,72,84}`. Additional phrase/root/offset constraints
can narrow that fiber; the class label alone does not supply them.

The full model has finitely many states, but its complete state product was
not exhaustively enumerated. The identities above are elementary written
arguments; the executable coverage below is a separate finite result. New
event counts, collisions, lengths, pitch ranges, tuning systems, or required
observations require a new contract. No musical preference, compositional
quality, physical measurement, or psychological claim follows.

## Sound and timing

The explicit tuning map is `frequency(n) = 440 * 2^((n-69)/12)` Hz. It defines
twelve-tone equal temperament with A4=440 Hz. One bar has 16 sixteenth-note
steps; tempo is 48–160 quarter notes per minute. One step lasts `60/BPM/4`
seconds. Six short, shaped oscillator tones play at the supplied onsets.

There is no autoplay. AudioContext creation/resumption occurs only through
the Sound/Play gesture paths. Visual-only playback has a separate clock and
works when Web Audio is unavailable. Sound failure leaves the visual tool
available and reports the error.

Playback uses a short lookahead to schedule oscillator starts against the
audio clock. Source edits and tempo changes restart the bar and cancel queued
tones. Pause and Reset cancel tones and return to step zero. Sound off cancels
tones immediately while leaving visual playback running. Leaving/hiding the
page stops the loop; returning does not resume automatically. There is no
audio export, recording, live microphone input, or persistent browser state.

The implementation follows the user-gesture and scheduling patterns in
[MDN's Web Audio best practices](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices)
and [sequencing guide](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Advanced_techniques).
These API references support the implementation, not a musical-effect claim.

## Replay

From the RPRM-open repository root, with Node.js 18 or newer:

```sh
node experimental/music-lens/model.test.js
node --test experimental/music-lens/audio.test.cjs
node --check experimental/music-lens/app.js
node experimental/music-lens/verify.cjs
node experimental/music-lens/verify-audio.cjs
python -I -B verify.py
```

The model suite checks 1,200 states (three representative phrases × 25 roots
× 16 phases), 734,400 candidate pitch targets against an independently
expressed admission oracle, and 895,298 assertions. It covers translation,
rotation, both reflections, exact inverse returns, interval/gap preservation
at the stated scope, octave loss, strict admission, immutable successors,
note names, frequency values, and browser/CommonJS compatibility.

Nine deterministic transport tests use fake clocks and an audio API fixture.
They cover validation and cloning, visual fallback, loop timing, source-edit
and mute cancellation, pending activation races, permission failure, page
visibility stopping, and recovery from a stalled scheduler. They do not
establish browser acoustic output or subjective listening quality.

The tests run from adjacent local source bytes; no historical artifact,
database, network service, cached receipt, or installed package is needed.
The aggregate verifier registers `music_lens_model` and `music_lens_audio`
as separate jobs. The wrappers require fresh successful child processes and
complete expected summaries, compare source hashes, and publish scoped JSON
receipts under `.artifacts/`. Standalone wrapper receipts are written to this
directory's `.artifacts/`; the root run records its own unique run directory.

The [dated review](REVIEW.md) records manual browser interactions and narrow/
wide layout observations. These remain separate from the automatic model and
transport coverage; the wrappers explicitly report `NOT_RUN_UI` and no
acoustic verification.

## Files

`model.js` and `model.test.js` implement and check the declared finite model.
`audio.js` and `audio.test.cjs` implement and check optional transport.
`verify.cjs` and `verify-audio.cjs` connect the tests to the aggregate verifier.
`index.html`, `style.css`, and `app.js` provide the interface. Original software
uses the repository's [0BSD license](../../LICENSE); original prose and
diagrams use [CC0](../../LICENSES/CC0-1.0.txt).
