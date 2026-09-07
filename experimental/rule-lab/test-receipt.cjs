"use strict";
// Shared synchronous runner: admitted CLI -> PENDING -> fresh checks -> PASS/FAIL.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");

const SOURCE_FILES = Object.freeze([
  ".gitignore", "README.md", "model.js", "presentation.js", "app.js", "index.html",
  "style.css", "model.test.cjs", "presentation.test.cjs", "test-receipt.cjs"
]);
function outputPath(args, base, suite) {
  if (args.length === 0) return path.join(base, ".artifacts", suite + ".json");
  if (args.length !== 2 || args[0] !== "--output" || !path.isAbsolute(args[1])) {
    throw new Error("Use no arguments, or --output ABSOLUTE_JSON_PATH");
  }
  const output = path.resolve(args[1]);
  if (SOURCE_FILES.some(file => path.relative(path.resolve(base, file), output) === "")) {
    throw new Error("Receipt destination must not overwrite a package source file");
  }
  return output;
}
function snapshot(base) {
  return Object.fromEntries(SOURCE_FILES.map(file => [file,
    crypto.createHash("sha256").update(fs.readFileSync(path.join(base, file))).digest("hex")]));
}
function writeReceipt(destination, value) {
  fs.mkdirSync(path.dirname(destination), {recursive: true});
  const temporary = destination + "." + crypto.randomUUID() + ".tmp";
  try {
    fs.writeFileSync(temporary, JSON.stringify(value, null, 2) + "\n", {encoding: "utf8", flag: "wx"});
    fs.renameSync(temporary, destination);
  } catch (error) {
    try { fs.unlinkSync(temporary); } catch (_) { /* Only this run's exact temporary name. */ }
    throw error;
  }
}
function runCheck({suite, base}, check) {
  let destination;
  try { destination = outputPath(process.argv.slice(2), base, suite); }
  catch (error) { process.stderr.write("CLI_ERROR: " + error.message + "\n"); process.exitCode = 2; return; }
  const envelope = {schema: "rule-lab-" + suite + "-tests/v2", suite,
    runId: crypto.randomUUID(), startedUTC: new Date().toISOString(), node: process.version};
  // No model/checker import or assertion runs before this output becomes PENDING.
  try { writeReceipt(destination, {...envelope, status: "PENDING"}); }
  catch (error) {
    process.stderr.write("RECEIPT_ERROR: unable to publish PENDING (" + (error.code || error.name) + "). No checks ran.\n");
    process.exitCode = 1; return;
  }
  let before;
  try {
    before = snapshot(base);
    const detail = check();
    if (detail === null || typeof detail !== "object" || typeof detail.then === "function") throw new TypeError("Check must return a synchronous result object");
    if (JSON.stringify(before) !== JSON.stringify(snapshot(base))) throw new Error("Package source changed during verification");
    const receipt = {...detail, ...envelope, status: "PASS", finishedUTC: new Date().toISOString(), sourceUnchanged: true, sourceHashes: before};
    writeReceipt(destination, receipt);
    process.stdout.write(JSON.stringify(receipt, null, 2) + "\n");
  } catch (error) {
    const receipt = {...envelope, status: "FAIL", finishedUTC: new Date().toISOString(),
      error: {name: error.name, message: error.message}, sourceHashes: before || null};
    try { writeReceipt(destination, receipt); }
    catch (receiptError) { process.stderr.write("RECEIPT_ERROR: unable to publish FAIL (" + (receiptError.code || receiptError.name) + ").\n"); }
    process.stderr.write("FAIL: " + error.name + ": " + error.message + "\n");
    process.exitCode = 1;
  }
}
module.exports = Object.freeze({runCheck, outputPath, SOURCE_FILES});
