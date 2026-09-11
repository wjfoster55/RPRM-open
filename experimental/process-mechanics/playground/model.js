/* Process-mechanics playground model — pure functions, no network.
   Not a generic authentication service: reuseCheck only compares declared
   source/plan/interval bindings for the teaching demo. */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.ProcessMechanicsPlayground = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const VIEWS = Object.freeze({
    color: (state) => state.value,
    rank: (state) => Math.floor(state.value / 10),
    parity: (state) => state.value % 2
  });

  const OPS = Object.freeze({
    inc: (v) => v + 1,
    dbl: (v) => v * 2,
    clamp: (v) => Math.min(20, Math.max(0, v))
  });

  function finiteInt(value, name) {
    if (typeof value !== 'number' || !Number.isSafeInteger(value)) {
      throw new TypeError(name + ' must be a safe integer');
    }
    return value;
  }

  function finiteNumber(value, name) {
    if (typeof value !== 'number' || !Number.isFinite(value)) {
      throw new TypeError(name + ' must be a finite number');
    }
    return value;
  }

  function createState(value, planId, sourceId) {
    return Object.freeze({
      value: finiteInt(value, 'value'),
      planId: String(planId || 'planA'),
      sourceId: String(sourceId || 'source1'),
      edited: false
    });
  }

  function display(state, viewName) {
    if (!Object.prototype.hasOwnProperty.call(VIEWS, viewName)) {
      throw new RangeError('unknown view');
    }
    return VIEWS[viewName](state);
  }

  function applyOp(state, opName) {
    if (!Object.prototype.hasOwnProperty.call(OPS, opName)) {
      throw new RangeError('unknown op');
    }
    return Object.freeze({
      ...state,
      value: OPS[opName](state.value)
    });
  }

  // Same displayed rank can hide different next values under `inc`.
  // Pair values at a decade boundary so successors cross ranks.
  function continuationDemo(seedValue) {
    const base = finiteInt(seedValue, 'seed');
    const high = base - (base % 10) + 9; // e.g. 10 -> 19
    const low = high - 1; // 18
    const a = createState(low, 'planA', 'source1');
    const b = createState(high, 'planA', 'source1');
    const view = 'rank';
    return {
      view,
      displayA: display(a, view),
      displayB: display(b, view),
      sameDisplay: display(a, view) === display(b, view),
      nextA: display(applyOp(a, 'inc'), view),
      nextB: display(applyOp(b, 'inc'), view),
      sufficientView: 'color',
      sufficientNextA: display(applyOp(a, 'inc'), 'color'),
      sufficientNextB: display(applyOp(b, 'inc'), 'color'),
      note: 'Rank can coincide while successor ranks diverge; color retains the exact value.'
    };
  }

  function joinCandidates(catalogue, observations) {
    if (!Array.isArray(catalogue) || !Array.isArray(observations)) {
      throw new TypeError('catalogue and observations must be arrays');
    }
    if (observations.some((o) => o == null)) {
      return { status: 'OPEN_INCOMPLETE', survivors: [], outcomes: [] };
    }
    const seenIds = new Set();
    for (const row of catalogue) {
      if (!row || typeof row !== 'object') {
        return { status: 'ADMISSION_ERROR', survivors: [], outcomes: [], note: 'catalogue row must be an object' };
      }
      if (typeof row.id !== 'string' || !row.id) {
        return { status: 'ADMISSION_ERROR', survivors: [], outcomes: [], note: 'candidate id must be a nonempty string' };
      }
      if (seenIds.has(row.id)) {
        return { status: 'ADMISSION_ERROR', survivors: [], outcomes: [], note: 'duplicate candidate id: ' + row.id };
      }
      seenIds.add(row.id);
      if (typeof row.outcome !== 'string' || !row.outcome) {
        return { status: 'ADMISSION_ERROR', survivors: [], outcomes: [], note: 'outcome must be a nonempty string' };
      }
    }
    const knownFields = new Set();
    for (const row of catalogue) {
      Object.keys(row).forEach((k) => knownFields.add(k));
    }
    for (const obs of observations) {
      if (!obs || typeof obs !== 'object') {
        return { status: 'ADMISSION_ERROR', survivors: [], outcomes: [], note: 'observation must be an object' };
      }
      for (const key of Object.keys(obs)) {
        if (!knownFields.has(key)) {
          return { status: 'ADMISSION_ERROR', survivors: [], outcomes: [], note: 'unknown observation field: ' + key };
        }
        try {
          finiteNumber(obs[key], key);
        } catch (e) {
          return { status: 'ADMISSION_ERROR', survivors: [], outcomes: [], note: String(e.message || e) };
        }
      }
    }
    const survivors = catalogue.filter((row) =>
      observations.every((obs) =>
        Object.keys(obs).every((key) => {
          if (!(key in row)) {
            return false;
          }
          return Math.abs(finiteNumber(row[key], key) - obs[key]) <= 0.01;
        })
      )
    );
    if (!survivors.length) {
      return {
        status: 'EMPTY_FAMILY',
        survivors: [],
        outcomes: [],
        note: 'EMPTY_FAMILY is not a NO_EVENT claim'
      };
    }
    const outcomes = Array.from(new Set(survivors.map((s) => s.outcome))).sort();
    return {
      status: outcomes.length === 1 ? 'RESOLVED' : 'AMBIGUOUS',
      survivors: survivors.map((s) => s.id),
      outcomes
    };
  }

  function requireBinding(obj, key) {
    if (obj == null || typeof obj !== 'object') {
      throw new TypeError('reuse context must be an object');
    }
    if (!Object.prototype.hasOwnProperty.call(obj, key)) {
      throw new TypeError('missing required reuse binding: ' + key);
    }
    const value = obj[key];
    if (value == null || value === '') {
      throw new TypeError('reuse binding ' + key + ' must be nonempty');
    }
    return value;
  }

  function reuseCheck(cached, request) {
    const keys = ['sourceId', 'planId', 'interval'];
    try {
      for (const key of keys) {
        requireBinding(cached, key);
        requireBinding(request, key);
      }
    } catch (e) {
      return {
        status: 'ADMISSION_ERROR',
        note: String(e.message || e)
      };
    }
    for (const key of keys) {
      if (cached[key] !== request[key]) {
        return {
          status: 'REJECT_CONTEXT_MISMATCH',
          mismatched: key,
          note: 'Structural cache hit is invalid when request context changes'
        };
      }
    }
    return {
      status: 'REUSE_OK',
      note: 'Reuse agrees only under matching source/plan/interval; it does not prove child truth'
    };
  }

  function exportReceipt(payload) {
    return JSON.stringify(
      {
        evidence_grade: 'NEW_ILLUSTRATIVE_DEMO',
        sandbox_edit: Boolean(payload && payload.edited),
        not_paper_revalidation: true,
        payload
      },
      null,
      2
    );
  }

  return {
    VIEWS,
    OPS,
    createState,
    display,
    applyOp,
    continuationDemo,
    joinCandidates,
    reuseCheck,
    exportReceipt
  };
});
