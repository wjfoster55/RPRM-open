'use strict';

// Fresh model/transport execution -> completed summary -> scoped JSON receipt.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');

const WRAPPER_FILES = ['verify.cjs', 'verify-audio.cjs'];
const PACKAGE_FILES = [...WRAPPER_FILES, 'model.js', 'model.test.js', 'audio.js',
  'audio.test.cjs', 'README.md', 'REVIEW.md', 'index.html', 'style.css', 'app.js'];
const SUITES = {
  model: {
    files: ['model.js', 'model.test.js', ...WRAPPER_FILES],
    command: ['model.test.js'],
    scope: 'Three representative phrases at all 25 roots and 16 phases, finite pitch-edit admission and inverse/readout fixtures; not the complete source-state product.',
    coverage: { states: 1200, targetChecks: 734400, assertions: 895298 }
  },
  audio: {
    files: ['audio.js', 'audio.test.cjs', ...WRAPPER_FILES],
    command: ['--test', '--test-reporter=tap', 'audio.test.cjs'],
    scope: 'Nine deterministic transport tests with fake clocks and an audio API fixture; no browser acoustic output or subjective listening evaluation.',
    coverage: { expectedTests: 9 }
  }
};

function outputPath(args, kind) {
  if (args.length === 0) return path.join(__dirname, '.artifacts', kind + '.json');
  if (args.length !== 2 || args[0] !== '--output' || !path.isAbsolute(args[1])) {
    throw new Error('Use no arguments, or --output ABSOLUTE_JSON_PATH');
  }
  const destination = path.resolve(args[1]);
  if (PACKAGE_FILES.some(file => path.relative(path.join(__dirname, file), destination) === '')) {
    throw new Error('Receipt destination must not overwrite a package source file');
  }
  return destination;
}

function snapshot(files) {
  return Object.fromEntries(files.map(file => [file,
    crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname, file))).digest('hex')]));
}

function publish(destination, receipt) {
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  const temporary = destination + '.' + crypto.randomUUID() + '.tmp';
  try {
    fs.writeFileSync(temporary, JSON.stringify(receipt, null, 2) + '\n', { encoding: 'utf8', flag: 'wx' });
    fs.renameSync(temporary, destination);
  } catch (error) {
    try { fs.unlinkSync(temporary); } catch (_) { /* Only this run's exact temporary file. */ }
    throw error;
  }
}

function summaryOf(stdout, kind) {
  if (kind === 'model') {
    const summary = JSON.parse(stdout);
    if (summary.status !== 'PASS' || Object.entries(SUITES.model.coverage)
      .some(([field, count]) => summary[field] !== count)) {
      throw new Error('The model replay must complete its full declared state, target and assertion census');
    }
    return summary;
  }
  const summary = {};
  for (const field of ['tests', 'pass', 'fail', 'cancelled', 'skipped', 'todo']) {
    const matches = [...stdout.matchAll(new RegExp('^# ' + field + ' (\\d+)\\r?$', 'gm'))];
    if (matches.length !== 1) throw new Error('Missing or ambiguous completed test summary: ' + field);
    summary[field] = Number(matches[0][1]);
  }
  if (summary.tests !== 9 || summary.pass !== 9 ||
      ['fail', 'cancelled', 'skipped', 'todo'].some(field => summary[field] !== 0)) {
    throw new Error('All nine audio tests must complete and pass without omissions');
  }
  return summary;
}

function run(kind) {
  const suite = SUITES[kind];
  if (!suite) throw new Error('Unknown Music Lens verification suite');
  let destination;
  try { destination = outputPath(process.argv.slice(2), kind); }
  catch (error) {
    process.stderr.write('CLI_ERROR: ' + error.message + '\n');
    return 2;
  }
  const receipt = {
    schema: 'music-lens-' + kind + '-tests/v1', suite: 'music_lens_' + kind, status: 'PENDING',
    runId: crypto.randomUUID(), startedUTC: new Date().toISOString(), node: process.version,
    scope: suite.scope, uiQA: 'NOT_RUN_UI', acousticQA: 'NOT_RUN', coverage: suite.coverage
  };
  // Replace any prior receipt before executing or reading model/test sources.
  try { publish(destination, receipt); }
  catch (error) {
    process.stderr.write('RECEIPT_ERROR: unable to publish PENDING; no tests ran (' + error.message + ').\n');
    return 1;
  }
  try {
    receipt.sourceHashes = snapshot(suite.files);
    const command = suite.command.map(arg => arg.endsWith('.js') || arg.endsWith('.cjs') ? path.join(__dirname, arg) : arg);
    const execution = spawnSync(process.execPath, command, {
      cwd: __dirname, encoding: 'utf8', timeout: 840000, maxBuffer: 4 * 1024 * 1024,
      windowsHide: true
    });
    receipt.execution = { executable: process.execPath, arguments: command,
      exitCode: execution.status, signal: execution.signal, stdout: execution.stdout || '', stderr: execution.stderr || '' };
    receipt.sourceUnchanged = JSON.stringify(receipt.sourceHashes) === JSON.stringify(snapshot(suite.files));
    if (execution.error) throw execution.error;
    if (execution.status !== 0 || execution.signal) throw new Error('Test process did not exit successfully');
    if (!receipt.sourceUnchanged) throw new Error('Model, transport or checker source changed during verification');
    receipt.summary = summaryOf(receipt.execution.stdout, kind);
    receipt.status = 'PASS';
    receipt.finishedUTC = new Date().toISOString();
    publish(destination, receipt);
    process.stdout.write(JSON.stringify(receipt, null, 2) + '\n');
    return 0;
  } catch (error) {
    receipt.status = 'FAIL';
    receipt.error = { name: error.name, message: error.message };
    receipt.finishedUTC = new Date().toISOString();
    try { publish(destination, receipt); }
    catch (writeError) { process.stderr.write('RECEIPT_ERROR: unable to publish FAIL (' + writeError.message + ').\n'); }
    process.stderr.write(JSON.stringify(receipt, null, 2) + '\n');
    return 1;
  }
}

module.exports = { run };
if (require.main === module) process.exitCode = run('model');
