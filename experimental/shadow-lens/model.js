/* Shadow Lens: bounded point-light geometry. See MODEL.md for the contract. */
(function (root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.ShadowLens = api;
})(typeof globalThis === 'object' ? globalThis : this, function () {
  'use strict';

  function freeze(value) {
    if (value && typeof value === 'object' && !Object.isFrozen(value)) {
      for (const child of Object.values(value)) freeze(child);
      Object.freeze(value);
    }
    return value;
  }

  const BOUNDS = freeze({
    lightX: { min: -80, max: 80 }, lightY: { min: -80, max: 80 },
    depth: { min: 2, max: 8 },
    centerX: { min: -50, max: 50 }, centerY: { min: -50, max: 50 },
    size: { min: 40, max: 120 }, shape: { min: 0, max: 2 }
  });
  const KEYS = Object.keys(BOUNDS);
  const LIGHT_HEIGHT = 100;
  const PROBE_DELTA = freeze({ x: 40, y: -30 });
  const SHAPES = freeze([
    { id: 0, name: 'Kite', vertices: [
      { x: -42, y: -34 }, { x: 10, y: -46 }, { x: 48, y: -4 },
      { x: 16, y: 42 }, { x: -38, y: 22 }
    ] },
    { id: 1, name: 'Chevron', vertices: [
      { x: -48, y: -32 }, { x: 0, y: -18 }, { x: 44, y: -42 },
      { x: 30, y: 8 }, { x: 46, y: 38 }, { x: -40, y: 24 }
    ] },
    { id: 2, name: 'Wing', vertices: [
      { x: -48, y: -26 }, { x: -8, y: -44 }, { x: 46, y: -20 },
      { x: 18, y: 0 }, { x: 42, y: 38 }, { x: -8, y: 26 },
      { x: -42, y: 10 }
    ] }
  ]);
  const DEFAULT = freeze({
    lightX: -40, lightY: 30, depth: 5,
    centerX: 0, centerY: 0, size: 80, shape: 0
  });
  const FIBERS = freeze({ primary: 161 * 161 * 7, withProbe: 161 * 161 });

  // Only plain own data fields are admitted. No coercion, getters, or extras.
  function record(value, allowed, required, label) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) {
      throw new TypeError(label + ' must be a plain record');
    }
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== Object.prototype && prototype !== null) {
      throw new TypeError(label + ' must be a plain record');
    }
    const descriptors = Object.getOwnPropertyDescriptors(value);
    const data = {};
    for (const key of Reflect.ownKeys(descriptors)) {
      const descriptor = descriptors[key];
      if (!allowed.includes(key) || !descriptor.enumerable || !('value' in descriptor)) {
        throw new TypeError(label + ' has an unexpected or non-data field');
      }
      data[key] = descriptor.value;
    }
    for (const key of required) {
      if (!Object.prototype.hasOwnProperty.call(descriptors, key)) {
        throw new TypeError(label + ' is missing ' + key);
      }
    }
    return data;
  }

  function admitFields(value, complete) {
    const data = record(value, KEYS, complete ? KEYS : [], 'Source');
    for (const key of Object.keys(data)) {
      if (!Number.isSafeInteger(data[key])) {
        throw new TypeError(key + ' must be an exact integer');
      }
      if (data[key] < BOUNDS[key].min || data[key] > BOUNDS[key].max) {
        throw new RangeError(key + ' is outside the admitted carrier');
      }
      if (data[key] === 0) data[key] = 0; // Canonical integer zero, including -0.
    }
    return data;
  }

  function defaults() { return Object.freeze({ ...DEFAULT }); }

  function createState(partial = {}) {
    return Object.freeze({ ...DEFAULT, ...admitFields(partial, false) });
  }

  function update(state, patch) {
    const prior = admitFields(state, true);
    const replacement = admitFields(patch, false);
    return Object.freeze({ ...prior, ...replacement });
  }

  function rational(n, d = 1) {
    if (!Number.isSafeInteger(n) || !Number.isSafeInteger(d)) {
      throw new TypeError('Rational numerator and denominator must be safe integers');
    }
    if (d === 0) throw new RangeError('A rational denominator cannot be zero');
    let numerator = BigInt(n), denominator = BigInt(d);
    if (denominator < 0n) { numerator = -numerator; denominator = -denominator; }
    let a = numerator < 0n ? -numerator : numerator, b = denominator;
    while (b !== 0n) { const remainder = a % b; a = b; b = remainder; }
    return Object.freeze({ n: Number(numerator / a), d: Number(denominator / a) });
  }

  function admitRational(value) {
    const data = record(value, ['n', 'd'], ['n', 'd'], 'Rational');
    return rational(data.n, data.d);
  }

  function sameRational(a, b) {
    return BigInt(a.n) * BigInt(b.d) === BigInt(b.n) * BigInt(a.d);
  }

  function displacementAt(depth) {
    return {
      x: rational(-depth * PROBE_DELTA.x, 10 - depth),
      y: rational(-depth * PROBE_DELTA.y, 10 - depth)
    };
  }

  // Complete depth fiber for this exact, fixed probe. An unmatched pair is NONE.
  function depthFromDisplacement(displacement) {
    const data = record(displacement, ['x', 'y'], ['x', 'y'], 'Displacement');
    const x = admitRational(data.x), y = admitRational(data.y);
    const values = [];
    for (let depth = BOUNDS.depth.min; depth <= BOUNDS.depth.max; depth += 1) {
      const candidate = displacementAt(depth);
      if (sameRational(x, candidate.x) && sameRational(y, candidate.y)) values.push(depth);
    }
    return freeze({ kind: values.length ? 'ONE' : 'NONE', values, count: values.length });
  }

  function point(x, y, z) { return { x: rational(x), y: rational(y), z: rational(z) }; }
  function numericPoint(p) { return { x: p.x.n / p.x.d, y: p.y.n / p.y.d, z: p.z.n / p.z.d }; }

  function scene(state) {
    const source = Object.freeze({ ...admitFields(state, true) });
    const { lightX, lightY, depth, centerX, centerY, size, shape } = source;
    const shadow = SHAPES[shape].vertices.map(p => ({
      x: rational(100 * centerX + size * p.x, 100),
      y: rational(100 * centerY + size * p.y, 100), z: rational(0)
    }));
    const cutout = shadow.map(p => ({
      x: rational((10 - depth) * p.x.n + depth * lightX * p.x.d, 10 * p.x.d),
      y: rational((10 - depth) * p.y.n + depth * lightY * p.y.d, 10 * p.y.d),
      z: rational(10 * depth)
    }));
    const displacement = displacementAt(depth);
    const secondary = shadow.map(p => ({
      x: rational(p.x.n * displacement.x.d + displacement.x.n * p.x.d, p.x.d * displacement.x.d),
      y: rational(p.y.n * displacement.y.d + displacement.y.n * p.y.d, p.y.d * displacement.y.d),
      z: rational(0)
    }));
    const light = point(lightX, lightY, LIGHT_HEIGHT);
    const probe = point(lightX + PROBE_DELTA.x, lightY + PROBE_DELTA.y, LIGHT_HEIGHT);
    return freeze({
      state: source, shadow: shadow.map(numericPoint), cutout: cutout.map(numericPoint),
      light: numericPoint(light), probe: numericPoint(probe), secondary: secondary.map(numericPoint),
      displacement: { x: displacement.x.n / displacement.x.d, y: displacement.y.n / displacement.y.d },
      exact: { shadow, cutout, light, probe, secondary, displacement }, fibers: FIBERS
    });
  }

  return freeze({
    BOUNDS, SHAPES, PROBE_DELTA, LIGHT_HEIGHT,
    defaults, createState, update, scene, rational, depthFromDisplacement
  });
});
