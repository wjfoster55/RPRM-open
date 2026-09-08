'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const M = require('./model.js');

// Independent ray/plane intersection: R(t)=L+t(O-L), t=Lz/(Lz-Oz).
// These cross-products are safe integers at the declared bounds; no tolerance
// or model rational/projection helper is used to establish the geometry.
function assertRayProjection(scene, light, targets) {
  assert.equal(light.z.d, 1);
  for (let i = 0; i < scene.exact.cutout.length; i += 1) {
    const vertex = scene.exact.cutout[i], target = targets[i];
    assert.equal(vertex.z.d, 1);
    assert.equal(target.z.n, 0);
    const gap = light.z.n - vertex.z.n;
    assert.ok(gap > 0 && vertex.z.n > 0);
    for (const axis of ['x', 'y']) {
      assert.equal(light[axis].d, 1);
      const origin = light[axis].n, p = vertex[axis], goal = target[axis];
      const numerator = origin * p.d * gap + light.z.n * (p.n - origin * p.d);
      const denominator = p.d * gap;
      const left = numerator * goal.d, right = goal.n * denominator;
      assert.ok(Number.isSafeInteger(left) && Number.isSafeInteger(right));
      assert.equal(left, right, 'ray must meet the exact ground vertex');
    }
  }
}

function deepFrozen(value) {
  if (!value || typeof value !== 'object') return;
  assert.ok(Object.isFrozen(value));
  for (const child of Object.values(value)) deepFrozen(child);
}

function signature(points) { return JSON.stringify(points); }

test('CommonJS and browser script expose the same usable API', () => {
  const context = vm.createContext({});
  vm.runInContext(fs.readFileSync(path.join(__dirname, 'model.js'), 'utf8'), context);
  const browserScene = vm.runInContext('ShadowLens.scene(ShadowLens.defaults())', context);
  assert.equal(JSON.stringify(browserScene), JSON.stringify(M.scene(M.defaults())));
  assert.deepEqual(Object.keys(context.ShadowLens), Object.keys(M));
});

test('defaults, snapshots, and successors are immutable and independent', () => {
  const first = M.defaults(), second = M.defaults();
  assert.notEqual(first, second);
  assert.deepEqual(first, { lightX: -40, lightY: 30, depth: 5, centerX: 0, centerY: 0, size: 80, shape: 0 });
  const patch = { depth: 8, lightX: 70 };
  const next = M.update(first, patch);
  patch.depth = 3;
  assert.equal(next.depth, 8);
  assert.equal(first.depth, 5);
  assert.notEqual(first, next);
  deepFrozen(M);
  deepFrozen(next);
  deepFrozen(M.scene(next));
  assert.throws(() => { next.depth = 2; }, TypeError);
  assert.throws(() => { M.SHAPES[0].vertices[0].x = 0; }, TypeError);
  const before = JSON.stringify(first);
  assert.throws(() => M.update(first, { depth: 9 }), RangeError);
  assert.equal(JSON.stringify(first), before);
});

test('all source fields admit their integer endpoints and reject malformed data', () => {
  for (const [key, { min, max }] of Object.entries(M.BOUNDS)) {
    assert.equal(M.createState({ [key]: min })[key], min);
    assert.equal(M.createState({ [key]: max })[key], max);
    for (const value of [min - 1, max + 1]) {
      assert.throws(() => M.createState({ [key]: value }), RangeError);
      assert.throws(() => M.update(M.defaults(), { [key]: value }), RangeError);
      assert.throws(() => M.scene({ ...M.defaults(), [key]: value }), RangeError);
    }
    for (const value of ['5', true, false, null, undefined, NaN, Infinity, 2.5, 5n, {}, []]) {
      assert.throws(() => M.createState({ [key]: value }), TypeError);
    }
    const missing = { ...M.defaults() };
    delete missing[key];
    assert.throws(() => M.scene(missing), TypeError);
    assert.throws(() => M.update(missing, {}), TypeError);
  }
  for (const input of [null, [], 4, 'scene', true, new Date(), Object.create({ depth: 3 })]) {
    assert.throws(() => M.createState(input), TypeError);
  }
  for (const extra of [{ probeDelta: { x: 0, y: 0 } }, { version: 1 }, { lightZ: 100 }, { [Symbol('extra')]: 1 }]) {
    assert.throws(() => M.createState(extra), TypeError);
    assert.throws(() => M.update(M.defaults(), extra), TypeError);
    assert.throws(() => M.scene({ ...M.defaults(), ...extra }), TypeError);
  }
  assert.throws(() => M.update(M.defaults()), TypeError);
  let getterCalls = 0;
  const getter = Object.defineProperty({}, 'depth', { enumerable: true, get() { getterCalls += 1; return 3; } });
  assert.throws(() => M.createState(getter), TypeError);
  assert.equal(getterCalls, 0);
  assert.throws(() => M.createState(Object.defineProperty({}, 'depth', { value: 3 })), TypeError);
  assert.equal(M.createState(Object.assign(Object.create(null), { depth: 3 })).depth, 3);
  assert.equal(Object.is(M.createState({ centerX: -0 }).centerX, -0), false);
});

test('rational admission is exact, reduced, and rejects invalid records', () => {
  assert.deepEqual(M.rational(6, -8), { n: -3, d: 4 });
  assert.deepEqual(M.rational(0, -3), { n: 0, d: 1 });
  assert.deepEqual(M.rational(10), { n: 10, d: 1 });
  for (const args of [[1, 0], [1, -0]]) assert.throws(() => M.rational(...args), RangeError);
  for (const args of [[1.5, 2], [1, '2'], [1, NaN], [Infinity, 1], [Number.MAX_SAFE_INTEGER + 1, 2]]) {
    assert.throws(() => M.rational(...args), TypeError);
  }
  for (const displacement of [null, {}, { x: -40, y: 30 }, { x: { n: -40, d: 1 }, y: { n: 30 } },
    { x: { n: -40, d: 1, extra: 0 }, y: { n: 30, d: 1 } },
    { x: { n: -40, d: 1 }, y: { n: 30, d: 1 }, z: 0 }]) {
    assert.throws(() => M.depthFromDisplacement(displacement), TypeError);
  }
  assert.throws(() => M.depthFromDisplacement({ x: { n: 0, d: 0 }, y: { n: 0, d: 1 } }), RangeError);
});

test('every admitted depth has a unique exact two-coordinate probe displacement', () => {
  const displacements = new Set();
  for (let depth = 2; depth <= 8; depth += 1) {
    const scene = M.scene(M.createState({ depth }));
    displacements.add(signature(scene.exact.displacement));
    assert.deepEqual(M.depthFromDisplacement(scene.exact.displacement), { kind: 'ONE', values: [depth], count: 1 });
    assert.equal(scene.displacement.x, -40 * depth / (10 - depth));
    assert.equal(scene.displacement.y, 30 * depth / (10 - depth));
  }
  assert.equal(displacements.size, 7);
  const pair = (x, y) => ({ x: { n: x, d: 1 }, y: { n: y, d: 1 } });
  for (const sample of [pair(0, 0), pair(40, -30), pair(-40, 29), pair(-1000, 750), pair(-12, 9)]) {
    assert.deepEqual(M.depthFromDisplacement(sample), { kind: 'NONE', values: [], count: 0 });
  }
  assert.deepEqual(M.depthFromDisplacement({ x: { n: 80, d: -2 }, y: { n: -90, d: -3 } }),
    { kind: 'ONE', values: [5], count: 1 });
  assert.equal(M.depthFromDisplacement({
    x: { n: -Number.MAX_SAFE_INTEGER, d: Number.MAX_SAFE_INTEGER - 1 },
    y: { n: Number.MAX_SAFE_INTEGER, d: Number.MAX_SAFE_INTEGER - 2 }
  }).kind, 'NONE');
});

test('equal primary shadow does not identify a scene; the probe recovers only depth', () => {
  const source = M.defaults();
  const a = M.scene(source);
  const b = M.scene(M.update(source, { depth: 8, lightX: 80, lightY: -80 }));
  const c = M.scene(M.update(source, { lightX: 80, lightY: -80 }));
  assert.deepEqual(a.exact.shadow, b.exact.shadow);
  assert.notDeepEqual(a.exact.cutout, b.exact.cutout);
  assert.notDeepEqual(a.exact.secondary, b.exact.secondary);
  assert.deepEqual(a.exact.shadow, c.exact.shadow);
  assert.deepEqual(a.exact.secondary, c.exact.secondary);
  assert.notDeepEqual(a.exact.light, c.exact.light);
  assert.notDeepEqual(a.exact.cutout, c.exact.cutout);
  for (const patch of [{ centerX: 1 }, { centerY: 1 }, { size: 81 }, { shape: 1 }]) {
    assert.notDeepEqual(a.exact.shadow, M.scene(M.update(source, patch)).exact.shadow);
  }
});

test('three templates are simple, nondegenerate polygons with distinct vertex counts', () => {
  const cross = (a, b, c) => (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
  const on = (a, b, p) => cross(a, b, p) === 0 && p.x >= Math.min(a.x, b.x) && p.x <= Math.max(a.x, b.x)
    && p.y >= Math.min(a.y, b.y) && p.y <= Math.max(a.y, b.y);
  const intersects = (a, b, c, d) => {
    const c1 = cross(a, b, c), c2 = cross(a, b, d), c3 = cross(c, d, a), c4 = cross(c, d, b);
    return (Math.sign(c1) * Math.sign(c2) < 0 && Math.sign(c3) * Math.sign(c4) < 0)
      || on(a, b, c) || on(a, b, d) || on(c, d, a) || on(c, d, b);
  };
  assert.deepEqual(M.SHAPES.map(s => s.vertices.length), [5, 6, 7]);
  for (const shape of M.SHAPES) {
    const p = shape.vertices, n = p.length;
    assert.equal(new Set(p.map(v => v.x + ',' + v.y)).size, n);
    let area2 = 0;
    for (let i = 0; i < n; i += 1) {
      const next = (i + 1) % n;
      assert.notEqual(cross(p[i], p[next], p[(i + 2) % n]), 0);
      area2 += p[i].x * p[next].y - p[next].x * p[i].y;
      for (let j = i + 1; j < n; j += 1) {
        if (j === next || (j + 1) % n === i) continue;
        assert.equal(intersects(p[i], p[next], p[j], p[(j + 1) % n]), false);
      }
    }
    assert.ok(area2 > 0);
  }
});

test('all shape/size pairs and each center coordinate recover their source settings', () => {
  // Vertex count identifies the template. Positive scaling and a fixed
  // nonzero first edge recover size; the first vertex then recovers center.
  let checked = 0;
  for (const template of M.SHAPES) {
    for (let size = 40; size <= 120; size += 1) {
      for (let center = -50; center <= 50; center += 1) {
        for (const axis of ['x', 'y']) {
          const source = M.createState({ shape: template.id, size,
            centerX: axis === 'x' ? center : 0, centerY: axis === 'y' ? center : 0 });
          const scene = M.scene(source), points = scene.exact.shadow;
          assert.equal(points.length, template.vertices.length);
          const a = points[0].x, b = points[1].x;
          const deltaN = b.n * a.d - a.n * b.d, deltaD = a.d * b.d;
          const templateDelta = template.vertices[1].x - template.vertices[0].x;
          assert.equal(100 * deltaN, size * deltaD * templateDelta);
          for (const coordinate of ['x', 'y']) {
            const origin = points[0][coordinate];
            const centerValue = source[coordinate === 'x' ? 'centerX' : 'centerY'];
            assert.equal(100 * origin.n - size * template.vertices[0][coordinate] * origin.d,
              centerValue * 100 * origin.d);
          }
          assertRayProjection(scene, scene.exact.light, scene.exact.shadow);
          assertRayProjection(scene, scene.exact.probe, scene.exact.secondary);
          checked += 1;
        }
      }
    }
  }
  assert.equal(checked, 49086);
});

test('all endpoint combinations ray-project correctly and numeric views match exact data', () => {
  for (const shape of [0, 1, 2]) for (const size of [40, 120]) {
    for (const centerX of [-50, 50]) for (const centerY of [-50, 50]) {
      for (const lightX of [-80, 80]) for (const lightY of [-80, 80]) {
        for (let depth = 2; depth <= 8; depth += 1) {
          const scene = M.scene(M.createState({ shape, size, centerX, centerY, lightX, lightY, depth }));
          assertRayProjection(scene, scene.exact.light, scene.exact.shadow);
          assertRayProjection(scene, scene.exact.probe, scene.exact.secondary);
          for (const kind of ['shadow', 'cutout', 'secondary']) {
            scene[kind].forEach((p, i) => {
              for (const axis of ['x', 'y', 'z']) {
                const exact = scene.exact[kind][i][axis];
                assert.ok(Number.isFinite(p[axis]));
                assert.equal(p[axis], exact.n / exact.d);
              }
            });
          }
        }
      }
    }
  }
});

test('complete fixed-shadow census: 181447 scenes, seven probe fibers of 25921', () => {
  const retained = M.scene(M.defaults()).exact.shadow;
  const buckets = new Map();
  let checked = 0;
  for (let lightX = -80; lightX <= 80; lightX += 1) {
    for (let lightY = -80; lightY <= 80; lightY += 1) {
      for (let depth = 2; depth <= 8; depth += 1) {
        const scene = M.scene(M.createState({ lightX, lightY, depth }));
        assert.deepEqual(scene.exact.shadow, retained);
        assertRayProjection(scene, scene.exact.light, retained);
        assertRayProjection(scene, scene.exact.probe, scene.exact.secondary);
        const key = signature(scene.exact.displacement);
        buckets.set(key, (buckets.get(key) || 0) + 1);
        checked += 1;
      }
    }
  }
  assert.equal(checked, 181447);
  assert.equal(buckets.size, 7);
  assert.deepEqual([...buckets.values()], Array(7).fill(25921));
  assert.deepEqual(M.scene(M.defaults()).fibers, { primary: checked, withProbe: 25921 });
});

test('hostile control: repeating the same light cannot distinguish any admitted depth', () => {
  // Delta=(0,0) is intentionally outside the configurable API. Repeating
  // the primary projection supplies the independent degenerate control.
  const retained = M.scene(M.defaults()).exact.shadow;
  for (let depth = 2; depth <= 8; depth += 1) {
    const scene = M.scene(M.createState({ depth }));
    assertRayProjection(scene, scene.exact.light, retained);
  }
  assert.equal(M.depthFromDisplacement({ x: { n: 0, d: 1 }, y: { n: 0, d: 1 } }).kind, 'NONE');
});
