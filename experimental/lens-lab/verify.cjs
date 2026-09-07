'use strict';

// Fresh node:test execution -> complete TAP summary -> scoped JSON receipt.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');

const SOURCE_FILES = ['model.js', 'model.test.js', 'verify.cjs'];
const PACKAGE_FILES = [...SOURCE_FILES, 'README.md', 'index.html', 'style.css', 'app.js', '.gitignore'];
const EXPECTED_TESTS = 16;

function outputPath(args) {
  if (args.length === 0) return path.join(__dirname, '.artifacts', 'model.json');
  if (args.length !== 2 || args[0] !== '--output' || !path.isAbsolute(args[1])) {
    throw new Error('Use no arguments, or --output ABSOLUTE_JSON_PATH');
  }
  const destination = path.resolve(args[1]);
  if (PACKAGE_FILES.some(file => path.relative(path.join(__dirname, file), destination) === '')) {
    throw new Error('Receipt destination must not overwrite a package source file');
  }
  return destination;
}

function snapshot() {
  return Object.fromEntries(SOURCE_FILES.map(file => [file,
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

function summaryOf(tap) {
  const summary = {};
  for (const field of ['tests', 'pass', 'fail', 'cancelled', 'skipped', 'todo']) {
    const matches = [...tap.matchAll(new RegExp('^# ' + field + ' (\\d+)\\r?$', 'gm'))];
    if (matches.length !== 1) throw new Error('Missing or ambiguous completed test summary: ' + field);
    summary[field] = Number(matches[0][1]);
  }
  if (summary.tests !== EXPECTED_TESTS || summary.pass !== EXPECTED_TESTS ||
      ['fail', 'cancelled', 'skipped', 'todo'].some(field => summary[field] !== 0)) {
    throw new Error('All ' + EXPECTED_TESTS + ' model tests must complete and pass without omissions');
  }
  return summary;
}

function main() {
  let destination;
  try { destination = outputPath(process.argv.slice(2)); }
  catch (error) {
    process.stderr.write('CLI_ERROR: ' + error.message + '\n');
    return 2;
  }
  const receipt = {
    schema: 'lens-lab-model-tests/v1', suite: 'lens_lab_model', status: 'PENDING',
    runId: crypto.randomUUID(), startedUTC: new Date().toISOString(), node: process.version,
    scope: '16 pure model tests over the stated finite transition families and renderer fixtures; not all 360^5 source tuples.',
    uiQA: 'NOT_RUN_UI',
    coverage: { expectedTests: EXPECTED_TESTS, lockedTransitions: 648000,
      duplicateWrapSignatureChecks: 3600, unlockedEdits: 5400 }
  };
  // Replace any prior receipt before executing or reading model/test sources.
  try { publish(destination, receipt); }
  catch (error) {
    process.stderr.write('RECEIPT_ERROR: unable to publish PENDING; no tests ran (' + error.message + ').\n');
    return 1;
  }
  try {
    receipt.sourceHashes = snapshot();
    const command = ['--test', '--test-reporter=tap', path.join(__dirname, 'model.test.js')];
    const run = spawnSync(process.execPath, command, {
      cwd: __dirname, encoding: 'utf8', timeout: 840000, maxBuffer: 4 * 1024 * 1024,
      windowsHide: true
    });
    receipt.execution = { executable: process.execPath, arguments: command,
      exitCode: run.status, signal: run.signal, stdout: run.stdout || '', stderr: run.stderr || '' };
    receipt.sourceUnchanged = JSON.stringify(receipt.sourceHashes) === JSON.stringify(snapshot());
    if (run.error) throw run.error;
    if (run.status !== 0 || run.signal) throw new Error('Model test process did not exit successfully');
    if (!receipt.sourceUnchanged) throw new Error('Model or checker source changed during verification');
    receipt.summary = summaryOf(receipt.execution.stdout);
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

process.exitCode = main();
