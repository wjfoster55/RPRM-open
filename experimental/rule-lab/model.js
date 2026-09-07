/* Pure model for the RPRM Rule Lab rebuild. No DOM, I/O, or randomness. */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.RPRMRuleLab = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const LIMITS = Object.freeze({ maxCells: 16777216, maxSieveLimit: 16777216 });
  const VIEWS = Object.freeze(["A", "B", "XOR", "equality", "AND", "OR", "four-state"]);
  const CONVENTIONS = Object.freeze({
    neighborhoodIndex: "4*left + 2*center + right",
    ruleOutput: "bit neighborhoodIndex of rule; least-significant bit is 000",
    displayedBitOrder: "111,110,101,100,011,010,001,000",
    rowOrder: "row 0 is the supplied seed; rows counts seed plus subsequent rows",
    layout: "row-major: index = row*width + column",
    fourState: "A + 2*B: 0=neither, 1=A only, 2=B only, 3=both",
    boundaries: "zero fixes every outside input to 0 at every step; periodic wraps within the supplied width"
  });

  function integer(value, name, min, max) {
    if (!Number.isSafeInteger(value) || value < min || value > max) {
      throw new RangeError(name + " must be a safe integer in [" + min + ", " + max + "]");
    }
    return value;
  }

  function ruleNumber(rule) { return integer(rule, "rule", 0, 255); }
  function bit(value, name) { return integer(value, name, 0, 1); }

  function arrayLike(value, name) {
    if (!Array.isArray(value) && Object.prototype.toString.call(value) !== "[object Uint8Array]") {
      throw new TypeError(name + " must be an Array or Uint8Array");
    }
    return value;
  }

  function copyBits(values, name) {
    arrayLike(values, name);
    integer(values.length, name + ".length", 0, LIMITS.maxCells);
    const out = new Uint8Array(values.length);
    for (let i = 0; i < values.length; i++) out[i] = bit(values[i], name + "[" + i + "]");
    return out;
  }

  function dimensions(width, rows) {
    integer(width, "width", 0, LIMITS.maxCells);
    integer(rows, "rows", 0, LIMITS.maxCells);
    return integer(width * rows, "cell count", 0, LIMITS.maxCells);
  }

  function boundaryName(boundary) {
    if (boundary !== "zero" && boundary !== "periodic") {
      throw new RangeError("boundary must be explicitly 'zero' or 'periodic'");
    }
    return boundary;
  }

  function outputUnchecked(rule, left, center, right) {
    return (rule >>> (4 * left + 2 * center + right)) & 1;
  }

  function ruleOutput(rule, left, center, right) {
    ruleNumber(rule); bit(left, "left"); bit(center, "center"); bit(right, "right");
    return outputUnchecked(rule, left, center, right);
  }

  function ruleBits(rule) { return ruleNumber(rule).toString(2).padStart(8, "0"); }

  function ruleTable(rule) {
    ruleNumber(rule);
    const table = [];
    for (let index = 7; index >= 0; index--) {
      const left = (index >>> 2) & 1, center = (index >>> 1) & 1, right = index & 1;
      table.push(Object.freeze({ index, left, center, right,
        neighborhood: "" + left + center + right,
        output: outputUnchecked(rule, left, center, right) }));
    }
    return Object.freeze(table);
  }

  function transformedRule(rule, transform) {
    ruleNumber(rule);
    let result = 0;
    for (let index = 0; index < 8; index++) {
      const left = (index >>> 2) & 1, center = (index >>> 1) & 1, right = index & 1;
      result |= transform(rule, left, center, right) << index;
    }
    return result;
  }

  function mirrorRule(rule) {
    return transformedRule(rule, (r, left, center, right) => outputUnchecked(r, right, center, left));
  }

  function outputComplementRule(rule) {
    return transformedRule(rule, (r, left, center, right) => 1 - outputUnchecked(r, left, center, right));
  }

  function conjugateRule(rule) {
    return transformedRule(rule, (r, left, center, right) =>
      1 - outputUnchecked(r, 1 - left, 1 - center, 1 - right));
  }

  function mirrorSeed(seed) { return copyBits(seed, "seed").reverse(); }
  function complementSeed(seed) {
    const out = copyBits(seed, "seed");
    for (let i = 0; i < out.length; i++) out[i] = 1 - out[i];
    return out;
  }

  function generate(options) {
    if (!options || typeof options !== "object") throw new TypeError("generation options required");
    const rule = ruleNumber(options.rule);
    const boundary = boundaryName(options.boundary);
    const seed = copyBits(options.seed, "seed");
    const width = seed.length, rows = options.rows, count = dimensions(width, rows);
    const data = new Uint8Array(count);
    if (rows > 0) data.set(seed);
    // Width zero is a legitimate empty carrier; do not loop over empty rows.
    if (width > 0) {
      for (let row = 1; row < rows; row++) {
        const prev = (row - 1) * width, current = row * width;
        for (let column = 0; column < width; column++) {
          const left = column > 0 ? data[prev + column - 1]
            : boundary === "periodic" ? data[prev + width - 1] : 0;
          const right = column + 1 < width ? data[prev + column + 1]
            : boundary === "periodic" ? data[prev] : 0;
          data[current + column] = outputUnchecked(rule, left, data[prev + column], right);
        }
      }
    }
    const metadata = Object.freeze({ rule, ruleBits: ruleBits(rule), boundary, width, rows,
      seed: Object.freeze(Array.from(seed)), conventions: CONVENTIONS });
    return Object.freeze({ kind: "eca-grid/v1", width, rows, data, metadata });
  }

  function generatePair(options) {
    if (!options || typeof options !== "object") throw new TypeError("pair options required");
    arrayLike(options.seedA, "seedA"); arrayLike(options.seedB, "seedB");
    if (options.seedA.length !== options.seedB.length) throw new RangeError("paired seed widths must match");
    const A = generate({ rule: options.ruleA, seed: options.seedA, rows: options.rows, boundary: options.boundary });
    const B = generate({ rule: options.ruleB, seed: options.seedB, rows: options.rows, boundary: options.boundary });
    return Object.freeze({ kind: "eca-pair/v1", width: A.width, rows: A.rows, A, B,
      metadata: Object.freeze({ alignment: "same row and column", A: A.metadata, B: B.metadata }) });
  }

  function validateGrid(grid, maxValue) {
    if (!grid || typeof grid !== "object") throw new TypeError("grid required");
    const count = dimensions(grid.width, grid.rows);
    arrayLike(grid.data, "grid.data");
    if (grid.data.length !== count) throw new RangeError("grid data length must equal width*rows");
    for (let i = 0; i < count; i++) integer(grid.data[i], "grid cell", 0, maxValue);
    return count;
  }

  function relationView(pair, mode) {
    if (!pair || pair.kind !== "eca-pair/v1") throw new TypeError("generated pair required");
    if (!VIEWS.includes(mode)) throw new RangeError("unknown relation view");
    const count = validateGrid(pair.A, 1);
    validateGrid(pair.B, 1);
    if (pair.width !== pair.A.width || pair.rows !== pair.A.rows ||
        pair.A.width !== pair.B.width || pair.A.rows !== pair.B.rows) {
      throw new RangeError("pair grids must share the same declared coordinates");
    }
    const data = new Uint8Array(count);
    for (let i = 0; i < count; i++) {
      const a = pair.A.data[i], b = pair.B.data[i];
      if (mode === "A") data[i] = a;
      else if (mode === "B") data[i] = b;
      else if (mode === "XOR") data[i] = a ^ b;
      else if (mode === "equality") data[i] = Number(a === b);
      else if (mode === "AND") data[i] = a & b;
      else if (mode === "OR") data[i] = a | b;
      else data[i] = a + 2 * b;
    }
    return Object.freeze({ kind: "eca-view/v1", width: pair.width, rows: pair.rows, data, base: pair,
      metadata: Object.freeze({ mode, source: pair.metadata, fourState: CONVENTIONS.fourState,
        retainedBase: true, direction: "paired bits to selected pointwise readout" }) });
  }

  function sieve(limit) {
    integer(limit, "sieve limit", 0, LIMITS.maxSieveLimit);
    const isPrime = new Uint8Array(limit + 1);
    const smallestFactor = new Uint32Array(limit + 1);
    if (limit >= 2) isPrime.fill(1, 2);
    for (let prime = 2; prime * prime <= limit; prime++) {
      if (isPrime[prime] === 0) continue;
      for (let multiple = prime * prime; multiple <= limit; multiple += prime) {
        isPrime[multiple] = 0;
        if (smallestFactor[multiple] === 0) smallestFactor[multiple] = prime;
      }
    }
    return Object.freeze({ kind: "bounded-sieve/v1", limit, isPrime, smallestFactor,
      metadata: Object.freeze({ inclusive: true, algorithm: "Eratosthenes; mark from p*p in ascending p",
        primeFlag: "1 iff prime; 0 and 1 are nonprime, not composite",
        factorWitness: "smallest prime factor for composites; 0 for primes, 0, and 1",
        proof: "Every composite n has a prime divisor at most sqrt(n); the sieve processes all such divisors." }) });
  }

  function rowMajorAddress(width, rows, row, column, start) {
    dimensions(width, rows);
    integer(start, "address start", 0, LIMITS.maxSieveLimit);
    integer(row, "row", 0, rows - 1);
    integer(column, "column", 0, width - 1);
    return integer(start + row * width + column, "address", 0, LIMITS.maxSieveLimit);
  }

  function ratio(numerator, denominator) { return denominator === 0 ? null : numerator / denominator; }

  function comparePrimes(grid, options) {
    const count = validateGrid(grid, 3);
    if (!options || options.addressMap !== "row-major") {
      throw new RangeError("an explicit addressMap: 'row-major' is required");
    }
    const start = integer(options.start, "address start", 0, LIMITS.maxSieveLimit);
    if (!Array.isArray(options.positiveValues)) throw new TypeError("explicit positiveValues array required");
    const selected = new Set();
    for (const value of options.positiveValues) {
      integer(value, "positive view value", 0, 3);
      if (selected.has(value)) throw new RangeError("positiveValues must not contain duplicates");
      selected.add(value);
    }
    const last = count === 0 ? null : integer(start + count - 1, "last address", 0, LIMITS.maxSieveLimit);
    const certificate = sieve(last === null ? 0 : last);
    const prediction = new Uint8Array(count), truth = new Uint8Array(count), outcomes = new Uint8Array(count);
    let TP = 0, FP = 0, FN = 0, TN = 0;
    for (let i = 0; i < count; i++) {
      const predicted = Number(selected.has(grid.data[i])), actual = certificate.isPrime[start + i];
      prediction[i] = predicted; truth[i] = actual;
      outcomes[i] = predicted + 2 * actual;
      if (predicted && actual) TP++;
      else if (predicted) FP++;
      else if (actual) FN++;
      else TN++;
    }
    const counts = Object.freeze({ TP, FP, FN, TN, total: count });
    const metrics = Object.freeze({ precision: ratio(TP, TP + FP), recall: ratio(TP, TP + FN),
      specificity: ratio(TN, TN + FP), accuracy: ratio(TP + TN, count),
      f1: ratio(2 * TP, 2 * TP + FP + FN), prevalence: ratio(TP + FN, count) });
    return Object.freeze({ kind: "prime-comparison/v1", width: grid.width, rows: grid.rows, source: grid,
      prediction, truth, outcomes, counts, metrics, certificate,
      metadata: Object.freeze({ addressMap: "row-major", formula: "start + row*width + column", start,
        first: count === 0 ? null : start, last, positiveValues: Object.freeze(Array.from(selected)),
        outcomeCodes: "0=TN, 1=FP, 2=FN, 3=TP", undefinedRatio: "null when denominator is zero",
        ceiling: "One declared finite comparison; no inferred prime map or search over maps/rules." }) });
  }

  return Object.freeze({ version: "0.2.0-model", LIMITS, VIEWS, CONVENTIONS, ruleOutput, ruleBits, ruleTable,
    mirrorRule, outputComplementRule, conjugateRule, mirrorSeed, complementSeed, generate, generatePair,
    relationView, sieve, rowMajorAddress, comparePrimes });
});
