/* Lens Lab: exact finite coordinates, followed by explicit visual readouts.
 * Source carrier: five ordered phases in Z/360Z, with occurrence identity.
 * Coordinate carrier: anchor plus five offsets, with offsets[0] = 0.
 * The retained tuple is a CAR. Rounded colors and sampled pictures are not.
 * No operation mutates its input. No external dependencies or network calls.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.LensModel = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const SIZE = 360;
  const ARITY = 5;
  const TAU = 2 * Math.PI;

  function finiteNumber(value, name, minimum, maximum) {
    if (typeof value !== 'number' || !Number.isFinite(value)) {
      throw new TypeError(name + ' must be a finite number.');
    }
    if (value < minimum || value > maximum) {
      throw new RangeError(name + ' must be between ' + minimum + ' and ' + maximum + '.');
    }
    return value;
  }

  function phase(value, name) {
    finiteNumber(value, name, 0, SIZE - 1);
    if (!Number.isInteger(value)) throw new TypeError(name + ' must be an integer phase.');
    return value === 0 ? 0 : value;
  }

  // Deliberately explicit wrap; admission elsewhere never silently wraps input.
  function mod(value) {
    if (typeof value !== 'number' || !Number.isSafeInteger(value)) {
      throw new TypeError('The wrapped value must be a safe integer.');
    }
    return ((value % SIZE) + SIZE) % SIZE;
  }

  function validateState(state) {
    if (!state || typeof state !== 'object' || Array.isArray(state)) {
      throw new TypeError('State must be an anchor and offsets record.');
    }
    const keys = Reflect.ownKeys(state);
    if (keys.length !== 2 || !keys.includes('anchor') || !keys.includes('offsets')) {
      throw new TypeError('State must contain exactly anchor and offsets.');
    }
    phase(state.anchor, 'Anchor');
    if (!Array.isArray(state.offsets) || state.offsets.length !== ARITY) {
      throw new TypeError('Offsets must be an array of exactly five phases.');
    }
    for (let i = 0; i < ARITY; i += 1) phase(state.offsets[i], 'Offset ' + i);
    if (state.offsets[0] !== 0) throw new RangeError('The first offset must be zero.');
    return true;
  }

  function createState(anchor, offsets) {
    validateState({ anchor, offsets });
    return Object.freeze({
      anchor: anchor === 0 ? 0 : anchor,
      offsets: Object.freeze(offsets.map((value) => value === 0 ? 0 : value))
    });
  }

  function phases(state) {
    validateState(state);
    return state.offsets.map((offset) => mod(state.anchor + offset));
  }

  function movePoint(state, index, targetPhase, locked = true) {
    validateState(state);
    if (typeof index !== 'number' || !Number.isInteger(index)) {
      throw new TypeError('Point index must be an integer.');
    }
    if (index < 0 || index >= ARITY) throw new RangeError('Point index must be between 0 and 4.');
    phase(targetPhase, 'Target');
    if (typeof locked !== 'boolean') throw new TypeError('Locked must be a boolean.');
    if (locked) {
      // The same delta moves every occurrence. Retain the old phase to undo
      // this absolute-target action; an absolute setter itself is not a CAR.
      return createState(mod(targetPhase - state.offsets[index]), state.offsets);
    }
    const values = phases(state);
    values[index] = targetPhase;
    // Re-anchor after editing A so that every other absolute phase stays put.
    return createState(values[0], values.map((value) => mod(value - values[0])));
  }

  function relativeSignature(state) {
    const values = phases(state);
    // Row i, column j is the directed difference phase[j] - phase[i].
    return values.map((from) => values.map((to) => mod(to - from)));
  }

  function colorHex(value, saturation = 65, lightness = 55) {
    phase(value, 'Hue');
    finiteNumber(saturation, 'Saturation', 0, 100);
    finiteNumber(lightness, 'Lightness', 0, 100);
    const s = saturation / 100;
    const l = lightness / 100;
    const chroma = (1 - Math.abs(2 * l - 1)) * s;
    const sector = value / 60;
    const secondary = chroma * (1 - Math.abs(sector % 2 - 1));
    let rgb;
    if (sector < 1) rgb = [chroma, secondary, 0];
    else if (sector < 2) rgb = [secondary, chroma, 0];
    else if (sector < 3) rgb = [0, chroma, secondary];
    else if (sector < 4) rgb = [0, secondary, chroma];
    else if (sector < 5) rgb = [secondary, 0, chroma];
    else rgb = [chroma, 0, secondary];
    const base = l - chroma / 2;
    return '#' + rgb.map((channel) => Math.round(255 * (channel + base)).toString(16).padStart(2, '0')).join('');
  }

  function wavePoint(value, x, amplitude, cycles) {
    phase(value, 'Wave phase');
    finiteNumber(x, 'Sample coordinate', 0, 1);
    finiteNumber(amplitude, 'Amplitude', 0, 1);
    finiteNumber(cycles, 'Cycles', 1, 4);
    if (!Number.isInteger(cycles)) throw new TypeError('Cycles must be an integer.');
    // Canonical zero makes the total phase collapse exact at amplitude zero.
    if (amplitude === 0) return 0;
    return amplitude * Math.sin(TAU * (cycles * x + value / SIZE));
  }

  function orbitPoint(value, radius, rotation = 0) {
    phase(value, 'Orbit phase');
    finiteNumber(radius, 'Radius', 0, 1);
    phase(rotation, 'Rotation');
    if (radius === 0) return { x: 0, y: 0 };
    const angle = TAU * mod(value + rotation) / SIZE;
    return { x: radius * Math.cos(angle), y: radius * Math.sin(angle) };
  }

  return Object.freeze({
    SIZE, ARITY, mod, validateState, createState, phases, movePoint,
    relativeSignature, colorHex, wavePoint, orbitPoint
  });
});
