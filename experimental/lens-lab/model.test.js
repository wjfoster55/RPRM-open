'use strict';

// Run from committed/local source bytes: node --test model.test.js
// Scope: one complete phase carrier and specified transition families.
// This is not an enumeration of all 360^5 constellations.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const M = require('./model.js');
const wrap = (value) => value - 360 * Math.floor(value / 360);
const near = (actual, expected, label) => assert.ok(Math.abs(actual - expected) < 1e-12, label + ': ' + actual + ' vs ' + expected);

test('browser classic-script export and Node export expose the same API', () => {
  const context = vm.createContext({});
  vm.runInContext(fs.readFileSync(path.join(__dirname, 'model.js'), 'utf8'), context);
  assert.deepEqual(Object.keys(context.LensModel), Object.keys(M));
  assert.equal(context.LensModel.colorHex(120, 100, 50), '#00ff00');
  assert.equal(M.SIZE, 360);
  assert.equal(M.ARITY, 5);
  assert.equal(Object.isFrozen(M), true);
});

test('explicit wrapping covers both seams and rejects silent coercion', () => {
  for (let value = -1080; value <= 1080; value += 1) assert.equal(M.mod(value), wrap(value));
  for (const value of [undefined, null, true, false, '1', NaN, Infinity, -Infinity, 1.5, 2 ** 53]) {
    assert.throws(() => M.mod(value));
  }
  assert.equal(Object.is(M.mod(-0), -0), false);
});

test('state creation clones and freezes the complete tuple without mutating input', () => {
  const offsets = [0, 10, 20, 300, 359];
  const state = M.createState(359, offsets);
  offsets[1] = 99;
  assert.deepEqual(state, { anchor: 359, offsets: [0, 10, 20, 300, 359] });
  assert.equal(M.validateState(state), true);
  assert.equal(Object.isFrozen(state), true);
  assert.equal(Object.isFrozen(state.offsets), true);
  assert.throws(() => { state.anchor = 0; }, TypeError);
  assert.throws(() => { state.offsets[1] = 0; }, TypeError);
  const readout = M.phases(state);
  readout[0] = 0;
  assert.equal(state.anchor, 359);
});

test('strict state admission rejects malformed shapes and out-of-carrier values', () => {
  const badNumbers = [true, false, null, undefined, '0', NaN, Infinity, -Infinity, -1, 360, 1.1];
  for (const value of badNumbers) {
    assert.throws(() => M.createState(value, [0, 1, 2, 3, 4]));
    for (let i = 0; i < 5; i += 1) {
      const offsets = [0, 1, 2, 3, 4];
      offsets[i] = value;
      assert.throws(() => M.createState(0, offsets));
    }
  }
  for (const offsets of [null, {}, '01234', new Uint16Array(5), [], [0, 1, 2, 3], [0, 1, 2, 3, 4, 5], [1, 1, 2, 3, 4], Array(5)]) {
    assert.throws(() => M.createState(0, offsets));
  }
  for (const state of [null, false, [], 0, {}, { anchor: 0 }, { offsets: [0, 1, 2, 3, 4] }, { anchor: 0, offsets: [0, 1, 2, 3, 4], hidden: 1 }]) {
    assert.throws(() => M.validateState(state));
    assert.throws(() => M.phases(state));
    assert.throws(() => M.relativeSignature(state));
    assert.throws(() => M.movePoint(state, 0, 0));
  }
});

test('every phase survives tuple encoding and decoding, including duplicate occurrences', () => {
  for (let anchor = 0; anchor < 360; anchor += 1) {
    for (const offsets of [[0, 0, 0, 0, 0], [0, 1, 71, 180, 359], [0, 359, 358, 1, 0]]) {
      const state = M.createState(anchor, offsets);
      const values = M.phases(state);
      assert.deepEqual(values, offsets.map((offset) => wrap(anchor + offset)));
      const recovered = M.createState(values[0], values.map((value) => wrap(value - values[0])));
      assert.deepEqual(recovered, state);
      assert.equal(values.length, 5);
    }
  }
});

test('locked moves cover every anchor, selected occurrence and target for a nonuniform constellation', () => {
  const offsets = [0, 19, 71, 180, 359];
  let cases = 0;
  for (let anchor = 0; anchor < 360; anchor += 1) {
    const state = M.createState(anchor, offsets);
    const before = M.phases(state);
    for (let index = 0; index < 5; index += 1) {
      for (let target = 0; target < 360; target += 1) {
        const moved = M.movePoint(state, index, target, true);
        const after = M.phases(moved);
        const delta = wrap(target - before[index]);
        assert.equal(after[index], target);
        for (let point = 0; point < 5; point += 1) assert.equal(wrap(after[point] - before[point]), delta);
        assert.deepEqual(moved.offsets, offsets);
        // The old selected phase is retained explicitly for the return move.
        assert.deepEqual(M.movePoint(moved, index, before[index], true), state);
        cases += 1;
      }
    }
  }
  assert.equal(cases, 648000);
});

test('locked changes preserve all 25 ordered differences under duplicates and wrap', () => {
  for (const state of [M.createState(359, [0, 0, 1, 1, 359]), M.createState(1, [0, 359, 0, 180, 180])]) {
    const signature = M.relativeSignature(state);
    assert.equal(signature.length, 5);
    for (let i = 0; i < 5; i += 1) {
      assert.equal(signature[i].length, 5);
      for (let j = 0; j < 5; j += 1) assert.equal(signature[i][j], wrap(state.offsets[j] - state.offsets[i]));
      for (let target = 0; target < 360; target += 1) assert.deepEqual(M.relativeSignature(M.movePoint(state, i, target)), signature);
    }
  }
});

test('unlocked moves edit only the selected occurrence, including re-anchoring A', () => {
  for (const state of [M.createState(359, [0, 0, 1, 1, 359]), M.createState(1, [0, 359, 0, 180, 180]), M.createState(180, [0, 1, 71, 180, 359])]) {
    const before = M.phases(state);
    for (let index = 0; index < 5; index += 1) {
      for (let target = 0; target < 360; target += 1) {
        const moved = M.movePoint(state, index, target, false);
        const expected = before.slice();
        expected[index] = target;
        assert.deepEqual(M.phases(moved), expected);
        assert.equal(moved.offsets[0], 0);
        assert.deepEqual(M.movePoint(moved, index, before[index], false), state);
      }
    }
    assert.deepEqual(M.phases(state), before);
  }
});

test('moving a duplicate occurrence does not merge identities', () => {
  const state = M.createState(0, [0, 0, 0, 0, 0]);
  assert.deepEqual(M.phases(M.movePoint(state, 2, 90, false)), [0, 0, 90, 0, 0]);
  assert.deepEqual(M.phases(M.movePoint(state, 2, 90, true)), [90, 90, 90, 90, 90]);
  assert.notDeepEqual(M.relativeSignature(M.movePoint(state, 2, 90, false)), M.relativeSignature(state));
});

test('absolute-target setters require saved history for reversal', () => {
  const first = M.createState(0, [0, 1, 2, 3, 4]);
  const second = M.createState(90, [0, 1, 2, 3, 4]);
  assert.notDeepEqual(first, second);
  assert.deepEqual(M.movePoint(first, 2, 180), M.movePoint(second, 2, 180));
});

test('move admission rejects invalid occurrence, target and lock flag', () => {
  const state = M.createState(0, [0, 1, 2, 3, 4]);
  for (const index of [true, false, '0', null, NaN, Infinity, -1, 5, 0.5]) assert.throws(() => M.movePoint(state, index, 0));
  for (const target of [true, '0', null, NaN, Infinity, -1, 360, 0.5]) assert.throws(() => M.movePoint(state, 0, target));
  for (const locked of [null, 0, 1, 'true', {}, []]) assert.throws(() => M.movePoint(state, 0, 0, locked));
});

test('HSL rendering agrees with independent canonical color values', () => {
  const anchors = ['#ff0000', '#ffff00', '#00ff00', '#00ffff', '#0000ff', '#ff00ff'];
  for (let i = 0; i < 6; i += 1) assert.equal(M.colorHex(i * 60, 100, 50), anchors[i]);
  assert.equal(M.colorHex(0), '#d74242');
  assert.equal(M.colorHex(210, 50, 40), '#336699');
  for (let value = 0; value < 360; value += 1) {
    assert.match(M.colorHex(value), /^#[0-9a-f]{6}$/);
    assert.equal(M.colorHex(value, 0, 50), '#808080');
    assert.equal(M.colorHex(value, 100, 0), '#000000');
    assert.equal(M.colorHex(value, 100, 100), '#ffffff');
  }
});

test('wave readouts match quarter-period samples and amplitude bounds', () => {
  for (let cycles = 1; cycles <= 4; cycles += 1) {
    near(M.wavePoint(0, 0, 1, cycles), 0, 'origin');
    near(M.wavePoint(0, 1 / (4 * cycles), 0.75, cycles), 0.75, 'positive peak');
    near(M.wavePoint(0, 3 / (4 * cycles), 0.75, cycles), -0.75, 'negative peak');
    near(M.wavePoint(90, 0, 0.5, cycles), 0.5, 'quarter-turn phase');
    near(M.wavePoint(270, 0, 0.5, cycles), -0.5, 'three-quarter phase');
    for (let value = 0; value < 360; value += 1) {
      assert.ok(Math.abs(M.wavePoint(value, 0.317, 0.6, cycles)) <= 0.6);
      near(M.wavePoint(value, 0, 0.6, cycles), M.wavePoint(value, 1, 0.6, cycles), 'cycle endpoint');
    }
  }
});

test('orbit readouts obey axes, radius and explicit rotation', () => {
  for (const [value, x, y] of [[0, 1, 0], [90, 0, 1], [180, -1, 0], [270, 0, -1]]) {
    const point = M.orbitPoint(value, 1);
    near(point.x, x, 'axis x');
    near(point.y, y, 'axis y');
  }
  for (let value = 0; value < 360; value += 1) {
    const point = M.orbitPoint(value, 0.37, 91);
    const unrotated = M.orbitPoint(wrap(value + 91), 0.37);
    near(Math.hypot(point.x, point.y), 0.37, 'radius');
    near(point.x, unrotated.x, 'rotation x');
    near(point.y, unrotated.y, 'rotation y');
  }
});

test('zero amplitude and zero radius collapse every phase while source stays distinct', () => {
  for (let value = 0; value < 360; value += 1) {
    assert.equal(M.wavePoint(value, 0.217, 0, 3), 0);
    assert.deepEqual(M.orbitPoint(value, 0, 137), { x: 0, y: 0 });
  }
  assert.notDeepEqual(M.createState(0, [0, 1, 2, 3, 4]), M.createState(1, [0, 1, 2, 3, 4]));
  // Even a nonzero-amplitude single sample can lose phase.
  near(M.wavePoint(30, 0, 1, 1), M.wavePoint(150, 0, 1, 1), 'single sample collision');
});

test('projection admission rejects invalid parameters even at collapsed settings', () => {
  for (const value of [true, false, '0', null, NaN, Infinity, -1, 360, 0.25]) {
    assert.throws(() => M.colorHex(value));
    assert.throws(() => M.wavePoint(value, 0, 0, 1));
    assert.throws(() => M.orbitPoint(value, 0));
    assert.throws(() => M.orbitPoint(0, 0, value));
  }
  for (const value of [true, null, '0', NaN, Infinity, -0.01, 1.01]) {
    assert.throws(() => M.wavePoint(0, value, 0, 1));
    assert.throws(() => M.wavePoint(0, 0, value, 1));
    assert.throws(() => M.orbitPoint(0, value));
  }
  for (const cycles of [true, '1', null, NaN, Infinity, 0, 5, 1.5]) assert.throws(() => M.wavePoint(0, 0, 0, cycles));
  for (const value of [true, null, '0', NaN, Infinity, -1, 101]) {
    assert.throws(() => M.colorHex(0, value, 50));
    assert.throws(() => M.colorHex(0, 50, value));
  }
});
