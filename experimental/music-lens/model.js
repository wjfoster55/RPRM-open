/* Music Lens: a supplied six-event, 16-step symbolic phrase and 12-TET renderer.
 * Event order A..F is identity, independently of chronological onset order.
 * Root 48..72; offsets -12..12 with A=0; unique steps in Z16; phase in Z16.
 * State operations return frozen clones. Absolute root/phase setters require
 * retaining the old coordinate to undo them. Inversion and reversal undo
 * themselves. Pitch-class and gap readouts discard source information.
 * The tuning formula specifies synthesis; it is no physical/perceptual result.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.MusicModel = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const ARITY = 6;
  const PERIOD = 16;
  const DEFAULT_STEPS = [0, 3, 6, 8, 10, 14];
  const DEFAULT_OFFSETS = [0, 4, 7, 12, 7, 4];
  const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

  function integer(value, name, minimum, maximum) {
    if (typeof value !== 'number' || !Number.isSafeInteger(value)) {
      throw new TypeError(name + ' must be a safe integer.');
    }
    if (value < minimum || value > maximum) {
      throw new RangeError(name + ' must be between ' + minimum + ' and ' + maximum + '.');
    }
    return value === 0 ? 0 : value;
  }

  function mod(value, base) {
    integer(value, 'Wrapped value', Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER);
    if (base !== 12 && base !== PERIOD) throw new RangeError('Modulus must be 12 or 16.');
    return ((value % base) + base) % base;
  }

  function sixIntegers(values, name, minimum, maximum) {
    if (!Array.isArray(values) || values.length !== ARITY) {
      throw new TypeError(name + ' must be an array of exactly six integers.');
    }
    // Reject sparse arrays, accessors and extra properties as malformed input.
    if (Reflect.ownKeys(values).length !== ARITY + 1) {
      throw new TypeError(name + ' must contain only six entries.');
    }
    for (let index = 0; index < ARITY; index += 1) {
      const entry = Object.getOwnPropertyDescriptor(values, String(index));
      if (!entry || !Object.hasOwnProperty.call(entry, 'value')) {
        throw new TypeError(name + ' entries must be stored numeric values.');
      }
      integer(entry.value, name + '[' + index + ']', minimum, maximum);
    }
  }

  function validateState(state) {
    const expected = ['root', 'phase', 'steps', 'offsets'];
    if (!state || typeof state !== 'object' || Array.isArray(state)) {
      throw new TypeError('State must be a root, phase, steps and offsets record.');
    }
    const keys = Reflect.ownKeys(state);
    if (keys.length !== expected.length || expected.some((key) => !keys.includes(key))) {
      throw new TypeError('State must contain exactly root, phase, steps and offsets.');
    }
    for (const key of expected) {
      if (!Object.hasOwnProperty.call(Object.getOwnPropertyDescriptor(state, key), 'value')) {
        throw new TypeError('State fields must be stored values.');
      }
    }
    integer(state.root, 'Root', 48, 72);
    integer(state.phase, 'Phase', 0, PERIOD - 1);
    sixIntegers(state.steps, 'Steps', 0, PERIOD - 1);
    sixIntegers(state.offsets, 'Offsets', -12, 12);
    if (new Set(state.steps).size !== ARITY) throw new RangeError('Onset steps must be distinct.');
    if (state.offsets[0] !== 0) throw new RangeError('The first pitch offset must be zero.');
    // These MIDI bounds follow from the root/offset bounds; state them locally.
    state.offsets.forEach((offset) => integer(state.root + offset, 'MIDI note', 36, 84));
    return true;
  }

  // Omitted trailing arguments use the default phrase; explicit bad values fail.
  function createState(root, phase, steps, offsets) {
    if (arguments.length > 4) throw new TypeError('createState accepts at most four arguments.');
    if (arguments.length < 1) root = 60;
    if (arguments.length < 2) phase = 0;
    if (arguments.length < 3) steps = DEFAULT_STEPS;
    if (arguments.length < 4) offsets = DEFAULT_OFFSETS;
    validateState({ root, phase, steps, offsets });
    return Object.freeze({
      root,
      phase: phase === 0 ? 0 : phase,
      steps: Object.freeze(steps.map((value) => value === 0 ? 0 : value)),
      offsets: Object.freeze(offsets.map((value) => value === 0 ? 0 : value))
    });
  }

  function events(state) {
    validateState(state);
    return state.steps.map((step, index) => {
      const midi = state.root + state.offsets[index];
      return { id: String.fromCharCode(65 + index), step: mod(state.phase + step, PERIOD), midi, pitchClass: mod(midi, 12) };
    });
  }

  function transpose(state, newRoot) {
    validateState(state);
    return createState(newRoot, state.phase, state.steps, state.offsets);
  }

  function rotate(state, newPhase) {
    validateState(state);
    return createState(state.root, newPhase, state.steps, state.offsets);
  }

  function invert(state) {
    validateState(state);
    return createState(state.root, state.phase, state.steps, state.offsets.map((offset) => -offset));
  }

  function reverse(state) {
    validateState(state);
    // Reflect each onset about the supplied phase, preserving event identity.
    return createState(state.root, state.phase, state.steps.map((step) => mod(-step, PERIOD)), state.offsets);
  }

  function pitchMoveBounds(state, index, locked) {
    validateState(state);
    integer(index, 'Event index', 0, ARITY - 1);
    if (typeof locked !== 'boolean') throw new TypeError('Locked must be a boolean.');
    if (locked) return { min: 48 + state.offsets[index], max: 72 + state.offsets[index] };
    if (index !== 0) return { min: state.root - 12, max: state.root + 12 };
    // Editing A changes the coordinate root. All other absolute pitches stay
    // fixed, so their new offsets jointly constrain the permissible root.
    const retained = state.offsets.slice(1).map((offset) => state.root + offset);
    return {
      min: Math.max(48, ...retained.map((midi) => midi - 12)),
      max: Math.min(72, ...retained.map((midi) => midi + 12))
    };
  }

  function movePitch(state, index, targetMidi, locked) {
    const bounds = pitchMoveBounds(state, index, locked);
    integer(targetMidi, 'Target MIDI note', bounds.min, bounds.max);
    if (locked) return transpose(state, targetMidi - state.offsets[index]);
    const values = state.offsets.map((offset) => state.root + offset);
    values[index] = targetMidi;
    return createState(values[0], state.phase, state.steps, values.map((value) => value - values[0]));
  }

  function rhythmGaps(state) {
    const onsets = events(state).map((event) => event.step).sort((left, right) => left - right);
    // Sorted gap multiset forgets event identities, order and absolute phase.
    return onsets.map((step, index) => mod(onsets[(index + 1) % ARITY] - step, PERIOD))
      .sort((left, right) => left - right);
  }

  function intervalSignature(state) {
    const notes = events(state).map((event) => event.midi);
    // Row i, column j is the signed interval from occurrence i to j.
    return notes.map((from) => notes.map((to) => to - from));
  }

  function pitchClasses(state) {
    return Array.from(new Set(events(state).map((event) => event.pitchClass)))
      .sort((left, right) => left - right);
  }

  function noteName(midi) {
    integer(midi, 'MIDI note', 0, 127);
    return NOTE_NAMES[mod(midi, 12)] + (Math.floor(midi / 12) - 1);
  }

  function frequency(midi) {
    integer(midi, 'MIDI note', 0, 127);
    return 440 * 2 ** ((midi - 69) / 12);
  }

  return Object.freeze({
    createState, validateState, events, transpose, rotate, invert, reverse,
    movePitch, pitchMoveBounds, rhythmGaps, intervalSignature, pitchClasses,
    noteName, frequency, mod
  });
});
