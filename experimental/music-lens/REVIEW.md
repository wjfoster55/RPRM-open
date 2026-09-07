# Music Lens review — 2026-09-07

The initial local review covered the new Music Lens playground before release
integration. At that point no existing released files had changed, and the
candidate had not been committed or pushed. The adjacent README gives the
model, operations, losses, tuning convention, and replay commands.

## Executed checks

- `node experimental/music-lens/model.test.js`: PASS; 1,200 representative
  states, 734,400 candidate pitch-bound checks, 895,298 assertions.
- `node --test experimental/music-lens/audio.test.cjs`: 9 passed, 0 failed.
- `node --check experimental/music-lens/app.js`: PASS.

An independent integration review found a drag-grab offset bug. The drag
controller now retains the cursor-to-note-center offset rather than snapping
the note center to the cursor. The correction was checked by a real horizontal
drag grabbed above the note center: pitch stayed C4. A subsequent upward drag
moved all six notes by six semitones while preserving the interval readout.

## Browser observations

Manual review in the in-app browser confirmed:

- Default C4-root phrase, all three presets, and Reset.
- + octave changes all piano-roll pitches and doubles the displayed A-note
  frequency while the complete pitch-class dial DOM remains identical.
- Rhythm rotation to 15 crosses the bar seam and preserves the gap readout.
- Two pitch reflections and two rhythm reflections restore the same labelled
  note/onset list, including after a phase change.
- Unlocked A edit C4→F4 leaves the other five pitches and all onsets fixed.
- Selecting B and pressing ArrowRight in the linked pitch range shifts the
  whole phrase by one semitone and preserves the signed interval readout.
- Play advances the highlighted step in visual-only mode. Sound can be enabled
  through the Sound button; the browser reports the soft-synth playback state
  without a warning/error. Pause stops the visual transport and Sound off
  clears the sound selection. This is browser interaction evidence, not a
  recorded acoustic measurement or subjective listening evaluation.
- Desktop and 390×844 layouts were inspected. The narrow page had no horizontal
  overflow; its pitch/rhythm dials were enlarged into a single column. The
  piano roll uses separate horizontal/vertical display scales, with CTM-based
  pointer conversion and full-size event/pitch controls below it.

Temporary viewport overrides were reset. The final preview starts with Open
sky selected, linked pitches, tempo 96, playback stopped, and sound off.

The deterministic audio tests use fake Web Audio and clocks. Manual browser
review does not become an automated UI suite or a cross-browser certification.
The full release verifier was not rerun during that initial isolated review;
no existing release suite or index was modified at that stage.

## Release integration

The release integration adds Music Lens to the root and experimental indexes
and registers separate `music_lens_model` and `music_lens_audio` aggregate
jobs. It preserves the reviewed model, transport and interface behavior.
The wrappers execute the adjacent tests afresh and require their complete
expected summaries before publishing PASS. Both bind their tested source
bytes, report UI/acoustic verification separately, and reject receipt paths
that would overwrite this package's sources.

Run `python -I -B verify.py` from the repository root for the 20-job Python
and Node release replay; its fresh receipts and logs are under `.artifacts/`.
Lean remains a separate optional job requested with `--lean`. The original
browser observations above retain their tested scope after integration.
