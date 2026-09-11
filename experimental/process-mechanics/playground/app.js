(function () {
  'use strict';
  const M = globalThis.ProcessMechanicsPlayground;
  const catalogue = [
    { id: 'c1', outcome: 'NO_ENTRY', D: 0.10, k_suppress: 1.0, r_scale: 1.0 },
    { id: 'c3', outcome: 'ENTRY', D: 0.80, k_suppress: 1.0, r_scale: 1.0 },
    { id: 'c5', outcome: 'DELAYED', D: 0.40, k_suppress: 1.0, r_scale: 0.25 },
    { id: 'c6', outcome: 'DELAYED', D: 0.42, k_suppress: 1.2, r_scale: 1.0 }
  ];
  const cached = { sourceId: 'source1', planId: 'planA', interval: '(4,8]' };
  let edited = false;

  function markEdited() {
    edited = true;
    document.getElementById('edit-banner').hidden = false;
    document.getElementById('announcement').textContent = 'Sandbox edit active.';
  }

  function renderContinuation() {
    const seed = Number(document.getElementById('seed').value);
    document.getElementById('seed-value').textContent = String(seed);
    const demo = M.continuationDemo(seed);
    document.getElementById('out-continuation').textContent = JSON.stringify(demo, null, 2);
  }

  function renderJoin() {
    const mix = document.getElementById('mix-false').checked;
    const observations = mix
      ? [{ k_suppress: 1.2 }, { r_scale: 0.25 }]
      : [{ D: 0.10 }];
    const result = M.joinCandidates(catalogue, observations);
    document.getElementById('out-join').textContent = JSON.stringify({ observations, result }, null, 2);
  }

  function renderReuse() {
    const planId = document.getElementById('plan').value;
    const request = { sourceId: 'source1', planId, interval: '(4,8]' };
    const result = M.reuseCheck(cached, request);
    document.getElementById('out-reuse').textContent = JSON.stringify({ cached, request, result }, null, 2);
  }

  function reset() {
    edited = false;
    document.getElementById('edit-banner').hidden = true;
    document.getElementById('seed').value = 10;
    document.getElementById('mix-false').checked = true;
    document.getElementById('plan').value = 'planA';
    document.getElementById('export-box').hidden = true;
    renderContinuation();
    renderJoin();
    renderReuse();
    document.getElementById('announcement').textContent = 'Reset to seeded sandbox.';
  }

  function exportJson() {
    const payload = {
      edited,
      continuation: JSON.parse(document.getElementById('out-continuation').textContent),
      join: JSON.parse(document.getElementById('out-join').textContent),
      reuse: JSON.parse(document.getElementById('out-reuse').textContent)
    };
    const text = M.exportReceipt(payload);
    const box = document.getElementById('export-box');
    box.hidden = false;
    box.textContent = text;
  }

  document.getElementById('seed').addEventListener('input', function () {
    markEdited();
    renderContinuation();
  });
  document.getElementById('mix-false').addEventListener('change', function () {
    markEdited();
    renderJoin();
  });
  document.getElementById('plan').addEventListener('change', function () {
    markEdited();
    renderReuse();
  });
  document.getElementById('run-join').addEventListener('click', function () {
    markEdited();
    renderJoin();
  });
  document.getElementById('run-reuse').addEventListener('click', function () {
    markEdited();
    renderReuse();
  });
  document.getElementById('reset').addEventListener('click', reset);
  document.getElementById('export').addEventListener('click', exportJson);

  document.addEventListener('keydown', function (event) {
    if (event.key === 'r' && (event.ctrlKey || event.metaKey)) {
      event.preventDefault();
      reset();
    }
  });

  reset();
})();
