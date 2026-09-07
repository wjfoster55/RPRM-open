"use strict";
const {runCheck} = require("./test-receipt.cjs");
runCheck({suite: "model", base: __dirname}, () => {
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const M = require("./model.js");

const counts = { localRuleCases: 0, transformCases: 0, generatedGrids: 0,
  evolutionSymmetries: 0, viewCells: 0, sieveIntegers: 0, primeComparisons: 0,
  rejectedInputs: 0 };

// Independent convention: read a textual truth table from 111 down to 000.
// This oracle does not call production helpers or use bit shifts/masks.
function referenceOutput(rule, left, center, right) {
  const neighborhoods = ["111", "110", "101", "100", "011", "010", "001", "000"];
  const word = "" + left + center + right;
  return Number(rule.toString(2).padStart(8, "0")[neighborhoods.indexOf(word)]);
}

function referenceTransform(rule, kind) {
  const neighborhoods = ["111", "110", "101", "100", "011", "010", "001", "000"];
  const transformed = neighborhoods.map(word => {
    let [left, center, right] = Array.from(word, Number);
    if (kind === "mirror") [left, right] = [right, left];
    if (kind === "conjugate") [left, center, right] = [1 - left, 1 - center, 1 - right];
    let out = referenceOutput(rule, left, center, right);
    if (kind === "output" || kind === "conjugate") out = 1 - out;
    return String(out);
  }).join("");
  return parseInt(transformed, 2);
}

// Second generation implementation: nested arrays, explicit padding, and
// string-table local evaluation. No production rule/step/transform calls.
function referenceGenerate(rule, seed, rows, boundary) {
  if (rows === 0) return [];
  const matrix = [Array.from(seed)];
  while (matrix.length < rows) {
    const previous = matrix[matrix.length - 1];
    const padded = boundary === "zero" ? [0, ...previous, 0]
      : [previous[previous.length - 1], ...previous, previous[0]];
    matrix.push(previous.map((_, i) => referenceOutput(rule, padded[i], padded[i + 1], padded[i + 2])));
  }
  return matrix.flat();
}

function binarySeed(width, code) {
  if (width === 0) return [];
  return Array.from(code.toString(2).padStart(width, "0"), Number);
}

function referencePrime(n) {
  if (n < 2) return false;
  for (let divisor = 2; divisor <= Math.floor(Math.sqrt(n)); divisor++) {
    if (n % divisor === 0) return false;
  }
  return true;
}

function referenceView(mode, a, b) {
  if (mode === "A") return a;
  if (mode === "B") return b;
  if (mode === "XOR") return Number(a !== b);
  if (mode === "equality") return Number(a === b);
  if (mode === "AND") return Number(a === 1 && b === 1);
  if (mode === "OR") return Number(a === 1 || b === 1);
  return [[0, 2], [1, 3]][a][b];
}

function rejects(fn) {
  assert.throws(fn);
  counts.rejectedInputs++;
}

for (let rule = 0; rule < 256; rule++) {
  const table = M.ruleTable(rule);
  assert.equal(table.length, 8);
  assert.equal(table.map(row => row.output).join(""), M.ruleBits(rule));
  assert.equal(table.map(row => row.neighborhood).join(","), M.CONVENTIONS.displayedBitOrder);
  for (const left of [0, 1]) for (const center of [0, 1]) for (const right of [0, 1]) {
    assert.equal(M.ruleOutput(rule, left, center, right), referenceOutput(rule, left, center, right));
    assert.equal(M.ruleOutput(M.mirrorRule(rule), left, center, right), referenceOutput(rule, right, center, left));
    assert.equal(M.ruleOutput(M.outputComplementRule(rule), left, center, right), 1 - referenceOutput(rule, left, center, right));
    assert.equal(M.ruleOutput(M.conjugateRule(rule), left, center, right), 1 - referenceOutput(rule, 1 - left, 1 - center, 1 - right));
    counts.localRuleCases++;
  }
  for (const [kind, transform] of [["mirror", M.mirrorRule], ["output", M.outputComplementRule], ["conjugate", M.conjugateRule]]) {
    assert.equal(transform(rule), referenceTransform(rule, kind));
    assert.equal(transform(transform(rule)), rule);
    counts.transformCases++;
  }
  assert.equal(M.mirrorRule(M.conjugateRule(rule)), M.conjugateRule(M.mirrorRule(rule)));
  assert.equal(M.mirrorRule(M.outputComplementRule(rule)), M.outputComplementRule(M.mirrorRule(rule)));
  assert.equal(M.conjugateRule(M.outputComplementRule(rule)), M.outputComplementRule(M.conjugateRule(rule)));
}

// Literal independently inspected bit tables, not only remembered rule numbers.
assert.equal(M.ruleBits(30), "00011110");
assert.equal(M.ruleBits(M.mirrorRule(30)), "01010110");
assert.equal(M.ruleBits(M.outputComplementRule(30)), "11100001");
assert.equal(M.ruleBits(M.conjugateRule(30)), "10000111");
assert.equal(M.mirrorRule(30), 86);
assert.equal(M.outputComplementRule(30), 225);
assert.equal(M.conjugateRule(30), 135);
assert.notEqual(M.mirrorRule(30), 83);

// Complete finite generation census: all rules, all seeds through width five,
// both boundaries, and seed-inclusive row counts {0,1,2,6}.
for (let rule = 0; rule < 256; rule++) {
  for (let width = 0; width <= 5; width++) {
    for (let code = 0; code < 2 ** width; code++) {
      const seed = binarySeed(width, code);
      for (const boundary of ["zero", "periodic"]) {
        for (const rows of [0, 1, 2, 6]) {
          const grid = M.generate({ rule, seed, rows, boundary });
          assert.deepEqual(Array.from(grid.data), referenceGenerate(rule, seed, rows, boundary));
          assert.deepEqual(grid.metadata.seed, seed);
          assert.equal(grid.width, width); assert.equal(grid.rows, rows);
          counts.generatedGrids++;
        }
      }
    }
  }
}

// Evolution symmetries require transformed seeds and compatible boundaries.
for (let rule = 0; rule < 256; rule++) {
  const seed = [1, 0, 1, 1, 0];
  for (const boundary of ["zero", "periodic"]) {
    const base = M.generate({ rule, seed, rows: 7, boundary });
    const reflected = M.generate({ rule: M.mirrorRule(rule), seed: M.mirrorSeed(seed), rows: 7, boundary });
    for (let row = 0; row < 7; row++) for (let col = 0; col < seed.length; col++) {
      assert.equal(reflected.data[row * seed.length + col], base.data[row * seed.length + seed.length - 1 - col]);
    }
    counts.evolutionSymmetries++;
  }
  const base = M.generate({ rule, seed, rows: 7, boundary: "periodic" });
  const conjugated = M.generate({ rule: M.conjugateRule(rule), seed: M.complementSeed(seed), rows: 7, boundary: "periodic" });
  assert.deepEqual(Array.from(conjugated.data), Array.from(base.data, x => 1 - x));
  counts.evolutionSymmetries++;
}
// Holding an outside-zero boundary fixed breaks black/white conjugacy.
const zeroEdge = M.generate({ rule: 170, seed: [0], rows: 2, boundary: "zero" });
const zeroEdgeConjugated = M.generate({ rule: M.conjugateRule(170), seed: [1], rows: 2, boundary: "zero" });
assert.notDeepEqual(Array.from(zeroEdgeConjugated.data), Array.from(zeroEdge.data, x => 1 - x));
// Valid Rule 0 must survive input validation without a fallback substitution.
assert.deepEqual(Array.from(M.generate({ rule: 0, seed: [1, 1, 1], rows: 2, boundary: "zero" }).data), [1, 1, 1, 0, 0, 0]);
assert.deepEqual(Array.from(M.generate({ rule: 255, seed: [0], rows: 3, boundary: "zero" }).data), [0, 1, 1]);

const allStates = M.generatePair({ ruleA: 0, ruleB: 0, seedA: [0, 1, 0, 1], seedB: [0, 0, 1, 1], rows: 1, boundary: "zero" });
const literalViews = { A: [0, 1, 0, 1], B: [0, 0, 1, 1], XOR: [0, 1, 1, 0],
  equality: [1, 0, 0, 1], AND: [0, 0, 0, 1], OR: [0, 1, 1, 1], "four-state": [0, 1, 2, 3] };
for (const mode of M.VIEWS) assert.deepEqual(Array.from(M.relationView(allStates, mode).data), literalViews[mode]);
for (let a = 0; a < 16; a++) for (let b = 0; b < 16; b++) {
  const seedA = binarySeed(4, a), seedB = binarySeed(4, b);
  const pair = M.generatePair({ ruleA: 30, ruleB: 86, seedA, seedB, rows: 4, boundary: "periodic" });
  const oracleA = referenceGenerate(30, seedA, 4, "periodic"), oracleB = referenceGenerate(86, seedB, 4, "periodic");
  for (const mode of M.VIEWS) {
    const view = M.relationView(pair, mode);
    assert.equal(view.base, pair); assert.equal(view.metadata.source, pair.metadata);
    for (let i = 0; i < view.data.length; i++) {
      assert.equal(view.data[i], referenceView(mode, oracleA[i], oracleB[i]));
      counts.viewCells++;
    }
  }
}

for (const limit of [...Array.from({ length: 257 }, (_, i) => i), 341, 561, 997, 1024, 1105, 1729, 4096, 10000]) {
  const certificate = M.sieve(limit);
  assert.equal(certificate.limit, limit);
  for (let n = 0; n <= limit; n++) {
    assert.equal(certificate.isPrime[n], Number(referencePrime(n)));
    const witness = certificate.smallestFactor[n];
    if (n >= 2 && !referencePrime(n)) {
      assert.ok(witness > 1 && witness < n && n % witness === 0 && referencePrime(witness));
      for (let d = 2; d < witness; d++) assert.notEqual(n % d, 0);
    } else assert.equal(witness, 0);
    counts.sieveIntegers++;
  }
}
assert.equal(M.sieve(49).smallestFactor[49], 7);
assert.equal(M.sieve(2).isPrime[2], 1);

function verifyComparison(grid, start, positiveValues) {
  const result = M.comparePrimes(grid, { addressMap: "row-major", start, positiveValues });
  const expected = { TP: 0, FP: 0, FN: 0, TN: 0, total: grid.data.length };
  for (let i = 0; i < grid.data.length; i++) {
    const row = Math.floor(i / grid.width), col = i % grid.width;
    const address = start + i;
    assert.equal(M.rowMajorAddress(grid.width, grid.rows, row, col, start), address);
    const predicted = positiveValues.includes(grid.data[i]), actual = referencePrime(address);
    const outcome = actual ? predicted ? "TP" : "FN" : predicted ? "FP" : "TN";
    expected[outcome]++;
    assert.equal(result.prediction[i], Number(predicted)); assert.equal(result.truth[i], Number(actual));
    assert.equal(result.outcomes[i], { TN: 0, FP: 1, FN: 2, TP: 3 }[outcome]);
  }
  assert.deepEqual(result.counts, expected);
  const fraction = (n, d) => d ? n / d : null;
  assert.deepEqual(result.metrics, {
    precision: fraction(expected.TP, expected.TP + expected.FP),
    recall: fraction(expected.TP, expected.TP + expected.FN),
    specificity: fraction(expected.TN, expected.TN + expected.FP),
    accuracy: fraction(expected.TP + expected.TN, expected.total),
    f1: fraction(2 * expected.TP, 2 * expected.TP + expected.FP + expected.FN),
    prevalence: fraction(expected.TP + expected.FN, expected.total)
  });
  assert.equal(result.source, grid);
  counts.primeComparisons++;
  return result;
}

// Enumeration verifies the declared map implementation; no best-map/rule
// selection or maximization is performed and no scientific comparison is tuned.
for (let code = 0; code < 256; code++) {
  const values = Array.from(code.toString(4).padStart(4, "0"), Number);
  for (let mask = 0; mask < 16; mask++) {
    const selected = [0, 1, 2, 3].filter(value => Math.floor(mask / 2 ** value) % 2 === 1);
    for (const start of [0, 1, 2, 8]) verifyComparison({ width: 2, rows: 2, data: values }, start, selected);
  }
}
const example = verifyComparison({ width: 3, rows: 2, data: [0, 1, 1, 0, 1, 1] }, 0, [1]);
assert.deepEqual(example.counts, { TP: 2, FP: 2, FN: 1, TN: 1, total: 6 });
assert.equal(example.metrics.precision, 0.5);
assert.equal(example.metrics.recall, 2 / 3);
const empty = verifyComparison({ width: 0, rows: 3, data: [] }, 0, []);
assert.ok(Object.values(empty.metrics).every(x => x === null));
assert.equal(empty.metadata.first, null); assert.equal(empty.metadata.last, null);
verifyComparison({ width: 3, rows: 0, data: [] }, M.LIMITS.maxSieveLimit, [1]);
const onlyNonprimes = verifyComparison({ width: 2, rows: 1, data: [0, 0] }, 0, [1]);
assert.equal(onlyNonprimes.metrics.precision, null);
assert.equal(onlyNonprimes.metrics.recall, null);
assert.equal(onlyNonprimes.metrics.accuracy, 1);
const onlyPrime = verifyComparison({ width: 1, rows: 1, data: [0] }, 2, [1]);
assert.equal(onlyPrime.metrics.specificity, null);
assert.equal(onlyPrime.metrics.recall, 0);

// Copy/lineage guarantees: supplied buffers and base grids are not modified.
const supplied = new Uint8Array([1, 0, 1]);
const generated = M.generate({ rule: 30, seed: supplied, rows: 3, boundary: "zero" });
supplied[0] = 0;
assert.equal(generated.data[0], 1); assert.deepEqual(generated.metadata.seed, [1, 0, 1]);
const detachedView = M.relationView(allStates, "A");
detachedView.data[0] = 1;
assert.equal(allStates.A.data[0], 0);
assert.deepEqual(Array.from(M.mirrorSeed([1, 0, 0])), [0, 0, 1]);
assert.deepEqual(Array.from(M.complementSeed([1, 0, 0])), [0, 1, 1]);

for (const bad of [-1, 256, 1.5, NaN, Infinity, "30", true, null, undefined]) {
  for (const fn of [M.ruleBits, M.ruleTable, M.mirrorRule, M.outputComplementRule, M.conjugateRule]) rejects(() => fn(bad));
}
for (const badSeed of [[2], [-1], [true], [NaN], [,], "101", null, new Uint16Array([1])]) {
  rejects(() => M.generate({ rule: 30, seed: badSeed, rows: 2, boundary: "zero" }));
}
for (const badRows of [-1, 1.1, NaN, Infinity, "2", true, M.LIMITS.maxCells + 1]) {
  rejects(() => M.generate({ rule: 30, seed: [1], rows: badRows, boundary: "zero" }));
}
for (const boundary of [undefined, "wrap", "infinite", false]) rejects(() => M.generate({ rule: 30, seed: [1], rows: 2, boundary }));
rejects(() => M.generate({ rule: 30, seed: [1, 0], rows: M.LIMITS.maxCells, boundary: "zero" }));
rejects(() => M.generate()); rejects(() => M.generatePair());
rejects(() => M.generatePair({ ruleA: 30, ruleB: 86, seedA: [1], seedB: [], rows: 1, boundary: "zero" }));
rejects(() => M.relationView(allStates, "agreement"));
rejects(() => M.relationView({}, "A"));
for (const bad of [-1, 0.5, NaN, Infinity, true, "49", M.LIMITS.maxSieveLimit + 1]) rejects(() => M.sieve(bad));
for (const opts of [{}, { addressMap: "row-major", start: 0 }, { addressMap: "guess", start: 0, positiveValues: [1] },
  { addressMap: "row-major", start: -1, positiveValues: [1] }, { addressMap: "row-major", start: 0, positiveValues: [1, 1] },
  { addressMap: "row-major", start: 0, positiveValues: [4] }, { addressMap: "row-major", start: 0, positiveValues: [true] },
  { addressMap: "row-major", start: M.LIMITS.maxSieveLimit, positiveValues: [1] }]) {
  rejects(() => M.comparePrimes({ width: 2, rows: 1, data: [0, 1] }, opts));
}
for (const badGrid of [{ width: 2, rows: 1, data: [0] }, { width: 1, rows: 1, data: [4] },
  { width: 1, rows: 1, data: [true] }, { width: 1, rows: 1, data: [,] },
  { width: -1, rows: 0, data: [] }, { width: M.LIMITS.maxCells, rows: 2, data: [] }]) {
  rejects(() => M.comparePrimes(badGrid, { addressMap: "row-major", start: 0, positiveValues: [1] }));
}
rejects(() => M.rowMajorAddress(0, 0, 0, 0, 0));
rejects(() => M.rowMajorAddress(2, 2, 2, 0, 0));
rejects(() => M.rowMajorAddress(2, 2, 0, 2, 0));
rejects(() => M.ruleOutput(30, 0, true, 1));

// Classic-script global export smoke test in a bare Node VM; NOT_RUN_UI.
const context = vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(__dirname, "model.js"), "utf8"), context);
assert.equal(context.RPRMRuleLab.mirrorRule(30), 86);
assert.equal(context.RPRMRuleLab.conjugateRule(30), 135);
const browserGrid = context.RPRMRuleLab.generate({ rule: 0, seed: [1], rows: 2, boundary: "zero" });
assert.deepEqual(Array.from(browserGrid.data), [1, 0]);

return {counts,
  knownRule30Transforms: {mirror: M.mirrorRule(30), outputComplement: M.outputComplementRule(30), conjugate: M.conjugateRule(30)},
  scope: "Exact local truth-table enumeration and the stated finite model tests; no prime-prediction claim.",
  uiQA: "NOT_RUN_UI"};
});
