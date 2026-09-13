// Demo wiring: input, simulation loop, HUD, scenario presets, model toggle.

const GRID_W = 240;
const GRID_H = 150;
const SCALE = 4;

const grid = new Grid(GRID_W, GRID_H);
const canvas = document.getElementById('view');
const renderer = new Renderer(canvas, grid, SCALE);

let model = 'C';
let brush = WATER;
let brushSize = 4;
let paused = false;
let stepsPerFrame = 1;

// ---------------- Scenarios (shared with the headless harness) ----------------
function scenarioEmpty() { grid.clear(); scBorder(grid); grid.wakeAll(); }
function scenarioBasin() { scBasin(grid); }
function scenarioUTube() { scUTube(grid); }
function scenarioDamBreak() { scDam(grid); }
function scenarioStress() { scStress(grid); }

// ---------------- Input ----------------
let painting = false;
function cellFromEvent(e) {
  const r = canvas.getBoundingClientRect();
  const x = Math.floor((e.clientX - r.left) / r.width * grid.w);
  const y = Math.floor((e.clientY - r.top) / r.height * grid.h);
  return [x, y];
}
function paintAt(x, y) {
  const s = brushSize;
  for (let dy = -s; dy <= s; dy++)
    for (let dx = -s; dx <= s; dx++) {
      if (dx * dx + dy * dy > s * s) continue;
      const nx = x + dx, ny = y + dy;
      if (nx <= 0 || ny <= 0 || nx >= grid.w - 1 || ny >= grid.h - 1) continue;
      if (brush === EMPTY) grid.set(nx, ny, EMPTY);
      else grid.set(nx, ny, brush);
    }
}
canvas.addEventListener('mousedown', (e) => { painting = true; const [x, y] = cellFromEvent(e); paintAt(x, y); });
canvas.addEventListener('mousemove', (e) => { if (painting) { const [x, y] = cellFromEvent(e); paintAt(x, y); } });
window.addEventListener('mouseup', () => { painting = false; });
canvas.addEventListener('contextmenu', (e) => e.preventDefault());

// ---------------- HUD / controls ----------------
const hud = document.getElementById('hud');
function setModel(m) {
  model = m;
  normalizeForModel(grid, model);
  for (const b of document.querySelectorAll('[data-model]'))
    b.classList.toggle('active', b.dataset.model === m);
  document.getElementById('modelName').textContent = MODEL_NAMES[m];
}
function setBrush(b) {
  brush = b;
  for (const el of document.querySelectorAll('[data-brush]'))
    el.classList.toggle('active', +el.dataset.brush === b);
}

document.querySelectorAll('[data-model]').forEach(b => b.onclick = () => setModel(b.dataset.model));
document.querySelectorAll('[data-brush]').forEach(b => b.onclick = () => setBrush(+b.dataset.brush));
// A wholesale scene rebuild must invalidate D_fast's cross-frame body cache.
function loadScene(fn) { return () => { fn(); resetFastState(grid); }; }
document.getElementById('reset').onclick = loadScene(scenarioEmpty);
document.getElementById('sc-basin').onclick = loadScene(scenarioBasin);
document.getElementById('sc-utube').onclick = loadScene(scenarioUTube);
document.getElementById('sc-dam').onclick = loadScene(scenarioDamBreak);
const stressBtn = document.getElementById('sc-stress');
if (stressBtn) stressBtn.onclick = loadScene(scenarioStress);
document.getElementById('pause').onclick = (e) => { paused = !paused; e.target.textContent = paused ? 'Play' : 'Pause'; };
document.getElementById('speed').oninput = (e) => { stepsPerFrame = +e.target.value; };
const chunkToggle = document.getElementById('chunks');
chunkToggle.onchange = () => { renderer.showChunks = chunkToggle.checked; };

// ---------------- Loop ----------------
let lastT = performance.now();
let fps = 0;
function frame(now) {
  const dt = now - lastT; lastT = now;
  fps = fps * 0.9 + (1000 / Math.max(1, dt)) * 0.1;

  let active = 0, moved = 0;
  if (!paused) {
    for (let s = 0; s < stepsPerFrame; s++) {
      grid.beginFrame();
      grid.stepSand();
      stepWater(grid, model);
      active += grid.activeCells; moved += grid.movedCells;
    }
  }
  renderer.draw();

  const totalCells = grid.w * grid.h;
  hud.innerHTML =
    `FPS <b>${fps.toFixed(0)}</b> &nbsp;|&nbsp; ` +
    `active cells <b>${active}</b> / ${totalCells} (<b>${(100 * active / totalCells / Math.max(1, stepsPerFrame)).toFixed(1)}%</b>) &nbsp;|&nbsp; ` +
    `moved <b>${moved}</b> &nbsp;|&nbsp; ` +
    `water mass <b>${grid.totalWaterMass().toFixed(0)}</b>`;
  requestAnimationFrame(frame);
}

setModel('C');
setBrush(WATER);
scenarioBasin();
requestAnimationFrame(frame);
