'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const M = require('./model.js');
const F = require('./presentation.js');

function deepFrozen(value) {
  if (!value || typeof value !== 'object') return;
  assert.ok(Object.isFrozen(value));
  for (const child of Object.values(value)) deepFrozen(child);
}

function assertTarget(scene, shared) {
  const template = M.SHAPES[shared.shape].vertices;
  assert.equal(scene.exact.shadow.length, template.length);
  scene.exact.shadow.forEach((point, index) => {
    for (const axis of ['x', 'y']) {
      const center = shared[axis === 'x' ? 'centerX' : 'centerY'];
      // Independent target-coordinate oracle using the declared template.
      assert.equal(point[axis].n * 100,
        (100 * center + shared.size * template[index][axis]) * point[axis].d);
    }
    assert.equal(point.z.n, 0);
  });
}

test('browser and CommonJS expose the same build and observe behavior', () => {
  const context = vm.createContext({});
  for (const file of ['model.js', 'presentation.js']) {
    vm.runInContext(fs.readFileSync(path.join(__dirname, file), 'utf8'), context);
  }
  const actual = vm.runInContext(`(() => {
    const family = ShadowFamily.build(ShadowLens.defaults(), [2, 5, 8]);
    return { family, A: ShadowFamily.observe(family, 'A'), B: ShadowFamily.observe(family, 'B') };
  })()`, context);
  const family = F.build(M.defaults(), [2, 5, 8]);
  const expected = { family, A: F.observe(family, 'A'), B: F.observe(family, 'B') };
  assert.deepEqual(Object.keys(context.ShadowFamily), Object.keys(F));
  assert.equal(JSON.stringify(actual), JSON.stringify(expected));
});

test('all 343 depth triples preserve A and split B exactly by their distinct depths', () => {
  let checked = 0;
  for (let a = 2; a <= 8; a += 1) for (let b = 2; b <= 8; b += 1) {
    for (let c = 2; c <= 8; c += 1) {
      const depths = [a, b, c];
      const family = F.build(M.defaults(), depths);
      const before = JSON.stringify(family);
      const primary = F.observe(family, 'A');
      const secondary = F.observe(family, 'B');
      assert.equal(primary.groups, 1);
      assert.equal(primary.allMatch, true);
      assert.equal(primary.recoveredDepths, null);
      assert.deepEqual(primary.shifts, [{ x: 0, y: 0 }, { x: 0, y: 0 }, { x: 0, y: 0 }]);
      // Independent oracle: -40*d/(10-d) is injective on admitted depths.
      // Duplicates remain duplicates; counts do not assume three differences.
      const distinctDepths = new Set(depths).size;
      assert.equal(secondary.groups, distinctDepths);
      assert.equal(secondary.allMatch, distinctDepths === 1);
      assert.deepEqual(secondary.recoveredDepths, depths);
      depths.forEach((depth, index) => {
        assert.equal(family.scenes[index].state.depth, depth);
        assert.deepEqual(primary.exact[index], family.scenes[0].exact.shadow);
        assert.strictEqual(primary.polygons[index], family.scenes[index].shadow);
        assert.strictEqual(secondary.polygons[index], family.scenes[index].secondary);
        assert.strictEqual(secondary.exact[index], family.scenes[index].exact.secondary);
        assert.equal(secondary.shifts[index].x, -40 * depth / (10 - depth));
        assert.equal(secondary.shifts[index].y, 30 * depth / (10 - depth));
        secondary.exact[index].forEach((point, vertex) => {
          for (const [axis, delta] of [['x', -40], ['y', 30]]) {
            const target = primary.exact[index][vertex][axis], shifted = point[axis];
            assert.equal((shifted.n * target.d - target.n * shifted.d) * (10 - depth),
              delta * depth * shifted.d * target.d);
          }
        });
      });
      assert.deepEqual(F.observe(family, 'A'), primary);
      assert.equal(JSON.stringify(family), before, 'changing observer must not change any source geometry');
      checked += 1;
    }
  }
  assert.equal(checked, 343);
});

test('shared target and lamp edits reach all three sources at representative bounds', () => {
  let checked = 0;
  for (const shape of [0, 1, 2]) for (const size of [40, 120]) {
    for (const centerX of [-50, 50]) for (const centerY of [-50, 50]) {
      for (const lightX of [-80, 80]) for (const lightY of [-80, 80]) {
        const shared = M.update(M.defaults(), { shape, size, centerX, centerY, lightX, lightY });
        const family = F.build(shared, [2, 5, 8]);
        assert.strictEqual(family.target, family.scenes[0].shadow);
        family.scenes.forEach((scene, index) => {
          assert.deepEqual(scene.state, { ...shared, depth: [2, 5, 8][index] });
          assertTarget(scene, shared);
          assert.deepEqual(scene.exact.shadow, family.scenes[0].exact.shadow);
          assert.deepEqual(scene.light, { x: lightX, y: lightY, z: 100 });
        });
        assert.equal(F.observe(family, 'A').groups, 1);
        assert.equal(F.observe(family, 'B').groups, 3);
        checked += 1;
      }
    }
  }
  assert.equal(checked, 96);
});

test('families and observations retain immutable snapshots, independent of inputs', () => {
  const shared = { ...M.defaults() }, depths = [2, 5, 8];
  const family = F.build(shared, depths);
  const before = JSON.stringify(family);
  shared.shape = 2;
  shared.centerX = 50;
  depths[0] = 8;
  assert.equal(JSON.stringify(family), before);
  deepFrozen(F);
  deepFrozen(family);
  deepFrozen(F.observe(family, 'A'));
  deepFrozen(F.observe(family, 'B'));
  assert.throws(() => { family.scenes[0].state.depth = 8; }, TypeError);
  assert.throws(() => { family.target[0].x = 0; }, TypeError);
});

test('build rejects invalid prior sources, malformed depths, holes, and accessor entries', () => {
  for (const source of [null, {}, [], { ...M.defaults(), depth: 9 }, { ...M.defaults(), size: '80' }]) {
    assert.throws(() => F.build(source, [2, 5, 8]));
  }
  for (const depths of [undefined, null, {}, '258', new Uint8Array([2, 5, 8]), [], [2, 5], [2, 5, 8, 2],
    [2, , 8], [2, undefined, 8], [2, '5', 8], [2, 5.5, 8], [2, NaN, 8], [2, Infinity, 8],
    [2, true, 8], [2, 5n, 8], Object.assign([2, 5, 8], { extra: 1 })]) {
    assert.throws(() => F.build(M.defaults(), depths), TypeError);
  }
  for (const depth of [-1, 0, 1, 9, 100]) {
    assert.throws(() => F.build(M.defaults(), [2, depth, 8]), RangeError);
  }
  let getterCalls = 0;
  const getter = Object.defineProperty([2, 5, 8], '1', {
    enumerable: true, get() { getterCalls += 1; return 5; }
  });
  assert.throws(() => F.build(M.defaults(), getter), TypeError);
  assert.equal(getterCalls, 0);
  const inherited = [2, , 8];
  Object.setPrototypeOf(inherited, { 1: 5 });
  assert.throws(() => F.build(M.defaults(), inherited), TypeError);
  assert.throws(() => F.build(M.defaults(), Object.defineProperty([2, 5, 8], '1', { enumerable: false })), TypeError);
});

test('observe rejects forged families and unknown observers without changing retained sources', () => {
  const family = F.build(M.defaults(), [2, 5, 8]);
  const before = JSON.stringify(family);
  for (const observer of [undefined, null, 'a', 'b', 'C', 0, true, {}, new String('A')]) {
    assert.throws(() => F.observe(family, observer), TypeError);
  }
  for (const forged of [undefined, null, 0, [], {}, { ...family }, JSON.parse(before), Object.create(family)]) {
    assert.throws(() => F.observe(forged, 'A'), TypeError);
  }
  assert.equal(JSON.stringify(family), before);
});
