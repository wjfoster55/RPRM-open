'use strict';

// Bounded cold replay: node experimental/music-lens/model.test.js
// No dependencies, browser, audio device, network, or retained receipt needed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const M = require('./model.js');

let assertions = 0;
function same(actual, expected) { assertions += 1; assert.deepEqual(actual, expected); }
function yes(value) { assertions += 1; assert.ok(value); }
function rejects(action) { assertions += 1; assert.throws(action, /./); }
const clone = (value) => JSON.parse(JSON.stringify(value));
const notes = (state) => M.events(state).map((event) => event.midi);
const independentMod = (value, base) => value - base * Math.floor(value / base);

const initial = M.createState();
same(initial, { root: 60, phase: 0, steps: [0, 3, 6, 8, 10, 14], offsets: [0, 4, 7, 12, 7, 4] });
same(M.events(initial), [
  { id: 'A', step: 0, midi: 60, pitchClass: 0 },
  { id: 'B', step: 3, midi: 64, pitchClass: 4 },
  { id: 'C', step: 6, midi: 67, pitchClass: 7 },
  { id: 'D', step: 8, midi: 72, pitchClass: 0 },
  { id: 'E', step: 10, midi: 67, pitchClass: 7 },
  { id: 'F', step: 14, midi: 64, pitchClass: 4 }
]);
same(M.rhythmGaps(initial), [2, 2, 2, 3, 3, 4]);
same(M.pitchClasses(initial), [0, 4, 7]);
same(M.intervalSignature(initial)[0], [0, 4, 7, 12, 7, 4]);

const phrases = [
  { steps: initial.steps, offsets: initial.offsets },
  { steps: [15, 0, 1, 7, 8, 12], offsets: [0, -12, 12, -1, 1, 0] },
  { steps: [5, 2, 14, 0, 9, 11], offsets: [0, 0, 0, 0, 0, 0] }
];
let states = 0;
let targetChecks = 0;
for (const phrase of phrases) {
  for (let root = 48; root <= 72; root += 1) {
    for (let phase = 0; phase < 16; phase += 1) {
      const state = M.createState(root, phase, phrase.steps, phrase.offsets);
      const snapshot = clone(state);
      const sourceNotes = notes(state);
      const sourceEvents = M.events(state);
      const signature = M.intervalSignature(state);
      const gaps = M.rhythmGaps(state);
      states += 1;
      same(sourceEvents.map((event) => event.step), phrase.steps.map((step) => independentMod(step + phase, 16)));
      same(sourceEvents.map((event) => event.id), ['A', 'B', 'C', 'D', 'E', 'F']);
      same(M.invert(M.invert(state)), state);
      same(M.reverse(M.reverse(state)), state);
      same(M.rhythmGaps(M.reverse(state)), gaps);
      same(M.events(M.reverse(state)).map((event) => event.step), phrase.steps.map((step) => independentMod(phase - step, 16)));
      const invertedSignature = M.intervalSignature(M.invert(state));
      same(invertedSignature, signature.map((row) => row.map((value) => value === 0 ? 0 : -value)));
      same(invertedSignature.map((row) => row.map(Math.abs)), signature.map((row) => row.map(Math.abs)));
      for (const nextRoot of [48, 60, 72]) {
        const moved = M.transpose(state, nextRoot);
        same(M.transpose(moved, root), state);
        same(M.intervalSignature(moved), signature);
        same(notes(moved), sourceNotes.map((midi) => midi + nextRoot - root));
      }
      for (let nextPhase = 0; nextPhase < 16; nextPhase += 1) {
        const rotated = M.rotate(state, nextPhase);
        same(M.rotate(rotated, phase), state);
        same(M.rhythmGaps(rotated), gaps);
      }
      for (let index = 0; index < 6; index += 1) {
        const locked = M.movePitch(state, index, 60 + state.offsets[index], true);
        same(M.intervalSignature(locked), signature);
        same(notes(locked), sourceNotes.map((midi) => midi + 60 - root));
        for (const isLocked of [false, true]) {
          const bounds = M.pitchMoveBounds(state, index, isLocked);
          // Independent enabledness oracle: rebuild the proposed absolute
          // pitches and check every resulting root and offset directly.
          for (let target = 35; target <= 85; target += 1) {
            const candidateNotes = sourceNotes.map((midi, occurrence) => isLocked
              ? midi + target - sourceNotes[index]
              : occurrence === index ? target : midi);
            const candidateRoot = candidateNotes[0];
            const admitted = candidateRoot >= 48 && candidateRoot <= 72 &&
              candidateNotes.every((midi) => midi >= 36 && midi <= 84 && Math.abs(midi - candidateRoot) <= 12);
            same(target >= bounds.min && target <= bounds.max, admitted);
            targetChecks += 1;
          }
          for (const target of [bounds.min, bounds.max]) {
            const moved = M.movePitch(state, index, target, isLocked);
            same(notes(moved), sourceNotes.map((midi, occurrence) => isLocked
              ? midi + target - sourceNotes[index]
              : occurrence === index ? target : midi));
            same(M.movePitch(moved, index, sourceNotes[index], isLocked), state);
          }
          rejects(() => M.movePitch(state, index, bounds.min - 1, isLocked));
          rejects(() => M.movePitch(state, index, bounds.max + 1, isLocked));
        }
      }
      same(state, snapshot);
    }
  }
}

// Crossing the cycle seam changes chronology, never the A..F occurrence order.
const seam = M.events(M.rotate(initial, 15));
same(seam.map((event) => event.step), [15, 2, 5, 7, 9, 13]);
same(seam.slice().sort((a, b) => a.step - b.step).map((event) => event.id), ['B', 'C', 'D', 'E', 'F', 'A']);
const octave = M.transpose(initial, 72);
same(M.pitchClasses(octave), M.pitchClasses(initial));
yes(notes(octave)[0] !== notes(initial)[0]);
same([M.noteName(0), M.noteName(60), M.noteName(61), M.noteName(69), M.noteName(72), M.noteName(127)], ['C-1', 'C4', 'C#4', 'A4', 'C5', 'G9']);
same(M.frequency(69), 440);
yes(Math.abs(M.frequency(60) - 261.6255653005986) < 1e-10);
yes(Math.abs(M.frequency(72) / M.frequency(60) - 2) < 1e-12);
same([M.mod(-1, 12), M.mod(-17, 16), M.mod(-0, 12)], [11, 15, 0]);

// No aliases from caller-owned input or returned readouts reach frozen state.
const source = clone(initial);
const frozen = M.createState(source.root, source.phase, source.steps, source.offsets);
source.steps[0] = 15;
source.offsets[1] = -10;
same(frozen, initial);
yes(Object.isFrozen(frozen) && Object.isFrozen(frozen.steps) && Object.isFrozen(frozen.offsets));
rejects(() => { frozen.root = 61; });
rejects(() => { frozen.offsets[0] = 1; });
const readout = M.events(frozen);
readout[0].midi = 999;
same(frozen, initial);

for (const bad of [undefined, null, false, '60', NaN, Infinity, 60.5, 2 ** 54]) {
  rejects(() => M.createState(bad));
  rejects(() => M.frequency(bad));
  rejects(() => M.noteName(bad));
  rejects(() => M.mod(bad, 12));
}
for (const patch of [
  { root: 47 }, { root: 73 }, { phase: -1 }, { phase: 16 }, { phase: true },
  { steps: [0, 0, 2, 3, 4, 5] }, { steps: [0, 1, 2, 3, 4] },
  { steps: [0, 1, 2, 3, 4, 16] }, { offsets: [1, 2, 3, 4, 5, 6] },
  { offsets: [0, -13, 0, 0, 0, 0] }, { offsets: [0, 13, 0, 0, 0, 0] },
  { offsets: [0, '1', 0, 0, 0, 0] }, { extra: 0 }
]) rejects(() => M.validateState(Object.assign(clone(initial), patch)));
for (const bad of [null, [], {}, false]) rejects(() => M.validateState(bad));
const sparse = clone(initial); delete sparse.steps[2];
rejects(() => M.validateState(sparse));
const extraArray = clone(initial); extraArray.offsets.extra = 0;
rejects(() => M.validateState(extraArray));
const extraSymbol = clone(initial); extraSymbol[Symbol('extra')] = 0;
rejects(() => M.validateState(extraSymbol));
const getterState = clone(initial); Object.defineProperty(getterState, 'root', { get() { throw new Error('Getter executed'); } });
assertions += 1; assert.throws(() => M.validateState(getterState), /stored values/);
for (const bad of [-1, 6, 1.5, '1', true]) rejects(() => M.pitchMoveBounds(initial, bad, true));
for (const bad of [0, 1, 'true', null, undefined]) rejects(() => M.movePitch(initial, 0, 60, bad));
for (const bad of [-1, 128, 60.5, '60']) rejects(() => M.noteName(bad));
for (const bad of [0, 7, '12', true, undefined]) rejects(() => M.mod(1, bad));
rejects(() => M.createState(60, 0, initial.steps, initial.offsets, 'extra'));
rejects(() => M.transpose(initial, 73));
rejects(() => M.rotate(initial, 16));
rejects(() => M.movePitch(initial, 1, 60.5, false));
same(initial, M.createState());

// Replay the same file as a classic browser script, with no CommonJS globals.
const browser = vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(__dirname, 'model.js'), 'utf8'), browser);
yes(typeof browser.MusicModel.createState === 'function');
same(JSON.parse(vm.runInContext('JSON.stringify(MusicModel.events(MusicModel.createState()))', browser)), M.events(initial));

console.log(JSON.stringify({ status: 'PASS', states, targetChecks, assertions,
  coverage: 'Three representative phrases; all 25 roots and 16 phases; all 16 destination phases; six locked/unlocked pitch ports; bounds checked against independent absolute-pitch admission on MIDI35..85; UMD and CommonJS.' }, null, 2));
