"use strict";
const {runCheck} = require("./test-receipt.cjs");
runCheck({suite: "presentation", base: __dirname}, () => {
// Pure Node checks only. No DOM, browser, renderer, or model-suite import.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const M = require("./model.js");
const P = require("./presentation.js");
const totals = {seedCases: 0, projectedBlocks: 0, apertureSlots: 0, binaryApertures: 0, cameraCases: 0};

// Explicit seed fixtures independently written from the documented centered offsets.
for (const [width, mode, expected] of [
  [1, "single", "1"], [1, "pair", "1"], [2, "pair", "01"],
  [5, "pair", "00110"], [5, "triplet", "01110"], [2, "triplet", "11"],
  [9, "echo", "000010000"], [15, "echo", "100000010000001"]
]) { assert.equal(P.makeSeed({width, mode}).join(""), expected); totals.seedCases++; }
assert.equal(P.makeSeed({width: 6, mode: "centered", bits: "101"}).join(""), "001010");
assert.equal(P.makeSeed({width: 5, mode: "exact", bits: "00110"}).join(""), "00110");
assert.throws(() => P.makeSeed({width: 2, mode: "centered", bits: "101"}));
assert.throws(() => P.makeSeed({width: 3, mode: "exact", bits: "10"}));
assert.throws(() => P.makeSeed({width: 3, mode: "centered", bits: "1 0"}));
for (const width of [1, 2, 17, 65, 257]) for (const density of [0, 35, 100]) for (const randomKey of [0, 1, 4294967295]) {
  const expected = Array(width).fill(0), center = Math.floor(width / 2), radius = Math.floor(width * 0.38);
  let word = BigInt(randomKey);
  for (let c = center - radius; c <= center + radius; c++) {
    word = (1664525n * word + 1013904223n) % 4294967296n;
    expected[c] = Number(word * 100n < BigInt(density) * 4294967296n);
  }
  assert.deepEqual(Array.from(P.makeSeed({width, mode: "random", density, randomKey})), expected);
  totals.seedCases++;
}

// Direct receiver truth table is separate from helper dispatch.
const truth = {
  A: [0, 1, 0, 1], B: [0, 0, 1, 1], XOR: [0, 1, 1, 0],
  equality: [1, 0, 0, 1], AND: [0, 0, 0, 1], OR: [0, 1, 1, 1], "four-state": [0, 1, 2, 3]
};
function expectedBlock(pair, data, r0, c0, r1, c1) {
  const histogram = [0, 0, 0, 0]; let countA = 0, countB = 0, edgeSum = 0;
  const cells = [];
  for (let r = r0; r < r1; r++) for (let c = c0; c < c1; c++) cells.push([r, c]);
  for (const [r, c] of cells) {
    const i = r * pair.width + c; histogram[data[i]]++; countA += pair.A.data[i]; countB += pair.B.data[i];
    for (const [rr, cc] of [[r - 1, c], [r + 1, c], [r, c - 1], [r, c + 1]])
      if (rr >= 0 && rr < pair.rows && cc >= 0 && cc < pair.width && data[rr * pair.width + cc] !== data[i]) edgeSum++;
  }
  return {area: cells.length, count: cells.length - histogram[0], countA, countB, edgeSum, histogram};
}
function checkBlock(pair, view, mode, block, base) {
  const expected = expectedBlock(pair, view.data, block.row0, block.column0, block.row1, block.column1);
  for (const key of Object.keys(expected)) assert.deepEqual(block[key], expected[key]);
  const counts = mode === "four-state" ? [expected.countA, expected.countB] : [expected.count];
  const get = summary => P.summarize(block, summary, mode === "four-state", base);
  assert.deepEqual(get("density").values, counts.map(n => n / expected.area));
  assert.deepEqual(get("majority").values, counts.map(n => n >= expected.area / 2 ? 1 : 0));
  assert.deepEqual(get("parity").values, counts.map(n => n % 2));
  assert.deepEqual(get("residue").values, counts.map(n => n % base));
  assert.deepEqual(get("pressure").values, [expected.edgeSum / (expected.area * 4)]);
  const presentCodes = expected.histogram.map((n, i) => n ? i : null).filter(n => n !== null);
  assert.equal(get("closure").kind, presentCodes.length === 1 ? "uniform" : "mixed");
  assert.deepEqual(get("closure").values, presentCodes.length === 1 ? presentCodes : []);
  totals.projectedBlocks++;
}
for (const boundary of ["zero", "periodic"]) for (const [width, rows] of [[1, 1], [1, 3], [2, 4], [5, 4], [10, 8], [17, 12]]) {
  const seedA = Array.from({length: width}, (_, i) => Number(i % 3 === 0));
  const seedB = Array.from({length: width}, (_, i) => Number(i % 4 < 2));
  const pair = M.generatePair({ruleA: 30, ruleB: 83, seedA, seedB, rows, boundary});
  const beforeA = Buffer.from(pair.A.data), beforeB = Buffer.from(pair.B.data);
  for (const mode of M.VIEWS) {
    const view = M.relationView(pair, mode), beforeView = Buffer.from(view.data), projection = P.createProjection(pair, view, mode);
    assert.strictEqual(projection.pair, pair); assert.strictEqual(projection.grid, view);
    for (const base of [3, 7, 9]) {
      const max = P.maxLevel(width, rows, base);
      assert.equal(max === 0 || base ** (max - 1) < Math.max(width, rows), true);
      assert.ok(base ** max >= Math.max(width, rows));
      for (let level = 1; level <= max; level++) {
        const projected = projection.level(base, level), visits = Array(width * rows).fill(0);
        assert.strictEqual(projection.level(base, level), projected);
        assert.equal(projected.blocks.length, Math.ceil(width / (base ** level)) * Math.ceil(rows / (base ** level)));
        for (const block of projected.blocks) {
          checkBlock(pair, view, mode, block, base);
          for (let r = block.row0; r < block.row1; r++) for (let c = block.column0; c < block.column1; c++) visits[r * width + c]++;
        }
        assert.ok(visits.every(n => n === 1), "Hierarchy must partition the exact carrier once, including clipped edges");
      }
      checkBlock(pair, view, mode, projection.block(0, 0, 1, 1), base);
    }
    for (let row = 0; row < rows; row++) for (let column = 0; column < width; column++) {
      const aperture = P.inspect(pair, mode, row, column); assert.equal(aperture.cells.length, 9);
      for (const cell of aperture.cells) {
        const r = cell.requestedRow, c = cell.requestedColumn;
        if (r < 0 || r >= rows) { assert.equal(cell.kind, "unretained-time"); assert.equal(cell.value, null); }
        else if ((c < 0 || c >= width) && boundary === "zero") {
          assert.equal(cell.kind, "fixed-exterior"); assert.equal(cell.value, truth[mode][0]); assert.equal(cell.column, null);
        } else {
          const sourceColumn = ((c % width) + width) % width, i = r * width + sourceColumn;
          assert.equal(cell.kind, c === sourceColumn ? "exact" : "periodic");
          assert.equal(cell.column, sourceColumn); assert.equal(cell.row, r);
          assert.equal(cell.value, truth[mode][pair.A.data[i] + 2 * pair.B.data[i]]);
        }
        totals.apertureSlots++;
      }
      if (row === 0 || row === rows - 1) assert.notEqual(aperture.status, "FULL_CHECK_CLOSURE");
    }
    assert.deepEqual(Buffer.from(view.data), beforeView);
  }
  assert.deepEqual(Buffer.from(pair.A.data), beforeA); assert.deepEqual(Buffer.from(pair.B.data), beforeB);
}

// A clipped 1x2 block can tie even though nominal block sides are odd.
const tiePair = M.generatePair({ruleA: 0, ruleB: 0, seedA: [0, 1], seedB: [1, 0], rows: 1, boundary: "periodic"});
const tieView = M.relationView(tiePair, "four-state");
const tie = P.createProjection(tiePair, tieView, "four-state").level(3, 1).blocks[0];
assert.deepEqual(P.summarize(tie, "majority", true, 3).values, [1, 1]);
assert.equal(tie.edgeSum, 2); // Two directed differing incidences; no extra periodic wrap edges.
assert.equal(tie.pressure, 0.25);
const emptyPair = M.generatePair({ruleA: 0, ruleB: 0, seedA: [], seedB: [], rows: 0, boundary: "zero"});
const empty = P.createProjection(emptyPair, M.relationView(emptyPair, "A"), "A").block(0, 0, 0, 0);
for (const mode of P.MODES) assert.equal(P.summarize(empty, mode, false, 3).kind, "empty");
assert.equal(empty.density, null); assert.equal(empty.pressure, null); assert.equal(empty.uniform, null);

// Independent geometric enumeration of all length-three straight lines through a 3x3 board.
const lines = [[0, 0, 1, 1], [0, 2, 1, -1], [0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 0, 1], [2, 0, 0, 1], [0, 0, 1, 0], [0, 2, 1, 0]];
const independentResiduals = values => lines.map(([r, c, dr, dc]) => {
  const triple = [0, 1, 2].map(k => values[(r + k * dr) * 3 + c + k * dc]);
  return triple.includes(null) ? null : triple[0] + triple[2] - (triple[1] + triple[1]);
});
let closedBinary = 0;
for (let mask = 0; mask < 512; mask++) {
  const values = Array.from({length: 9}, (_, i) => (mask >> i) & 1), result = P.residuals(values);
  assert.deepEqual(result.lines.map(x => x.value), independentResiduals(values));
  assert.notEqual(result.status, "COUNTERFEIT_CENTRAL_CLOSURE");
  if (result.status === "FULL_CHECK_CLOSURE") closedBinary++;
  totals.binaryApertures++;
}
assert.equal(closedBinary, 2);
const counterfeit = [0, 1, 0, 1, 1, 1, 2, 1, 2];
assert.deepEqual(P.residuals(counterfeit).lines.map(x => x.value), [0, 0, 0, 0, -2, 2, 0, 0]);
assert.equal(P.residuals(counterfeit).status, "COUNTERFEIT_CENTRAL_CLOSURE");
for (const values of [Array(9).fill(3), [0, 1, 2, 1, 2, 3, 2, 3, 4]]) assert.equal(P.residuals(values).status, "FULL_CHECK_CLOSURE");
assert.equal(P.residuals([null, null, null, 1, 1, 1, 1, 1, 1]).status, "INCOMPLETE");
assert.equal(P.residuals([null, null, null, 0, 1, 0, 1, 1, 1]).status, "OPEN");
assert.throws(() => P.residuals(Array(9)), /nine finite values/);
assert.throws(() => P.residuals([0, 0, 0, 0, NaN, 0, 0, 0, 0]), /nine finite values/);

// Every manual level survives tiny scale; automatic levels use declared threshold and finite ceiling.
for (const base of [3, 7, 9]) for (const scale of [0.002, 0.02, 0.1, 0.3, 0.9, 6, 64]) {
  const max = P.maxLevel(257, 512, base);
  for (let level = 0; level <= max; level++) assert.equal(P.activeLevel(257, 512, base, scale, false, level), level);
  const actual = P.activeLevel(257, 512, base, scale, true, 0);
  assert.ok(actual === max || scale * base ** actual >= 0.9);
  assert.ok(actual === 0 || scale * base ** (actual - 1) < 0.9);
}
for (const [width, height] of [[300, 320], [800, 600]]) for (const factor of [0.000001, 0.5, 1.5, 10000]) for (const [x, y] of [[0, 0], [110, 230], [width, height]]) {
  const camera = P.fitCamera(257, 512, width, height), before = P.worldPoint(camera, x, y, width, height);
  const changed = P.zoomCamera(camera, factor, x, y, width, height), after = P.worldPoint(changed, x, y, width, height);
  assert.ok(Math.abs(before.x - after.x) < 1e-7 && Math.abs(before.y - after.y) < 1e-7, "Pointer anchor survives zoom and clamp");
  assert.ok(changed.scale >= 0.002 && changed.scale <= 64); totals.cameraCases++;
}
assert.throws(() => P.activeLevel(5, 4, 5, 1, true, 0));
assert.throws(() => P.activeLevel(5, 4, 3, 0, true, 0));
assert.throws(() => P.zoomCamera({cx: 0, cy: 0, scale: 1}, -1, 0, 0, 50, 50));

// Static wiring checks: parse JavaScript but do not execute app.js or construct a DOM.
const appSource = fs.readFileSync(path.join(__dirname, "app.js"), "utf8");
const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
for (const name of ["app.js", "presentation.js", "presentation.test.cjs"]) new vm.Script(fs.readFileSync(path.join(__dirname, name), "utf8"), {filename: name});
const elements = new Map();
for (const match of html.matchAll(/<([a-z][a-z0-9-]*)\b([^>]*)>/gi)) {
  const attrs = Object.fromEntries(Array.from(match[2].matchAll(/([a-z-]+)="([^"]*)"/gi), a => [a[1], a[2]]));
  if (attrs.id) { assert.ok(!elements.has(attrs.id), "Duplicate HTML ID"); elements.set(attrs.id, {tag: match[1], ...attrs}); }
}
for (const match of appSource.matchAll(/\$\("([^"\n]+)"\)/g)) assert.ok(elements.has(match[1]), "Missing HTML ID " + match[1]);
for (const match of appSource.matchAll(/number\("([^"\n]+)"\)/g)) {
  const element = elements.get(match[1]);
  assert.equal(element.tag, "input", "valueAsNumber requires an input: " + match[1]);
  assert.equal(element.type, "number", "valueAsNumber requires a numeric input: " + match[1]);
}
for (const element of elements.values()) for (const key of ["for", "aria-labelledby", "aria-describedby"])
  if (element[key]) for (const reference of element[key].split(/\s+/)) assert.ok(elements.has(reference), "Missing accessible reference " + reference);
assert.deepEqual(Array.from(html.matchAll(/<script\s+src="([^"]+)"/g), m => m[1]), ["model.js", "presentation.js", "app.js"]);
const oneView = M.relationView(tiePair, "A");
const metricKeys = Object.keys(M.comparePrimes(oneView, {addressMap: "row-major", start: 0, positiveValues: [1]}).metrics);
for (const match of appSource.matchAll(/\.metrics\.([a-zA-Z0-9_]+)/g)) assert.ok(metricKeys.includes(match[1]), "Unknown model metric " + match[1]);
return {totals,
  staticChecks: {javaScriptParsedOnly: true, htmlIDs: elements.size, numericInputBindings: true, metricNames: true},
  scope: "Pure Node presentation helpers and static UI source checks; no rendered-browser execution.",
  uiQA: "NOT_RUN_UI"};
});
