"""Re-elaborate the two Lean sources with an explicitly supplied Lean 4.22.0.

This checks declaration inventories and axiom dependencies through separate
generated probes. It trusts the selected compiler and its standard library;
recording its hash is not authentication of an entire toolchain distribution.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
INVENTORIES = {
    "Relations": ("RPRM.Relations.", (
        "identity_left", "identity_right", "compose_assoc", "converse_involutive",
        "converse_compose", "graph_identity", "graph_compose", "graph_converse_inverse",
        "retraction_section_injective", "aperture_backward_forward", "aperture_forward_backward")),
    "Carrier": ("RPRM.", (
        "factorization_iff", "decoder_unique", "toReachable_onto", "option_map_eq_iff",
        "operational_fold_iff", "run_commutes", "run_defined_iff", "future_preserved",
        "fiber_conditions_preserve_all_futures")),
}
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(compiler):
    found = shutil.which(compiler)
    require(found is not None, "Lean executable not found")
    environment = {k: v for k, v in os.environ.items() if not k.upper().startswith("LEAN_")}
    # A PATH entry may be an elan shim. Resolve the selected installed prefix
    # while still in the repository, then execute its actual binary directly.
    prefix = subprocess.run([found, "--print-prefix"], cwd=ROOT, env=environment,
                            capture_output=True, text=True, encoding="utf-8", check=True, timeout=30)
    installed = Path(prefix.stdout.strip())
    require(installed.is_absolute(), "Lean did not report an absolute installation prefix")
    executable = (installed / "bin" / ("lean.exe" if os.name == "nt" else "lean")).resolve()
    require(executable.is_file() and (installed / "lib/lean/Init.olean").is_file(),
            "A complete installed Lean toolchain is required")
    version = subprocess.run([str(executable), "--version"], env=environment,
                             capture_output=True, text=True, encoding="utf-8", check=True, timeout=30)
    require(re.search(r"\bversion 4\.22\.0(?:,|\))", version.stdout), "Lean 4.22.0 is required")
    paths = [ROOT / "checks/formal.py"] + [ROOT / "lean" / (m + ".lean") for m in INVENTORIES]
    snapshots = {p: p.read_bytes() for p in paths}
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(data).hexdigest()
              for p, data in snapshots.items()}
    compiler_hash = digest(executable)
    modules = {}
    with tempfile.TemporaryDirectory(prefix="rprm-lean-") as scratch:
        work = Path(scratch)
        for module, (prefix, names) in INVENTORIES.items():
            source = ROOT / "lean" / (module + ".lean")
            # Each source imports only Init. The scratch directory contains no
            # precompiled project modules; compile the copied source bytes anew.
            # Validate and compile the same captured bytes, even if a source
            # changes and changes back while another process is editing it.
            text = snapshots[source].decode("utf-8")
            require(re.findall(r"^[ \t]*import[ \t]+([^\r\n]+?)[ \t]*\r?$", text, re.M) == ["Init"],
                    "Unexpected imports")
            copied = work / source.name
            copied.write_bytes(snapshots[source])
            command = [str(executable), "-DwarningAsError=true", "-o", module + ".olean", copied.name]
            built = subprocess.run(command, cwd=work, env=environment, capture_output=True,
                                   text=True, encoding="utf-8", check=False, timeout=240)
            source_transcript = built.stdout + built.stderr
            require(built.returncode == 0, "Lean compilation failed: " + source_transcript)
            # The source can print arbitrary messages while being elaborated.
            # Do not infer declaration existence or axioms from those messages.
            # Import the new object in an independently generated probe and ask
            # Lean to resolve every qualified declaration there.
            probe = work / (module + "Audit.lean")
            probe_text = "import " + module + "\n\n" + "\n".join(
                "#print axioms " + prefix + name for name in names) + "\n"
            probe.write_text(probe_text, encoding="utf-8", newline="\n")
            probe_environment = dict(environment)
            probe_environment["LEAN_PATH"] = str(work)
            queried = subprocess.run([str(executable), "-DwarningAsError=true", probe.name],
                                     cwd=work, env=probe_environment, capture_output=True,
                                     text=True, encoding="utf-8", check=False, timeout=240)
            transcript = queried.stdout + queried.stderr
            require(queried.returncode == 0, "Lean declaration probe failed: " + transcript)
            reports = re.findall(r"'([^']+)' (?:depends on axioms:|does not depend)", transcript)
            expected = {prefix + name for name in names}
            require(len(reports) == len(expected) and set(reports) == expected, "Axiom inventory mismatch")
            dependencies = {}
            for name in sorted(expected):
                match = re.search(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", transcript)
                independent = f"'{name}' does not depend on any axioms" in transcript
                require(bool(match) != independent, "Ambiguous or missing axiom report: " + name)
                axioms = [] if independent else [x.strip() for x in match.group(1).split(",") if x.strip()]
                require(set(axioms) <= ALLOWED, "Unadmitted axiom dependency: " + name)
                dependencies[name] = axioms
            modules[module] = {"declarations": len(names), "axiom_dependencies": dependencies,
                               "transcript": transcript, "source_transcript": source_transcript,
                               "probe_sha256": digest(probe),
                               "module_sha256": digest(work / (module + ".olean"))}
    require(hashes == {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}, "Source changed during check")
    require(compiler_hash == digest(executable), "Compiler changed during check")
    return {"schema": "rprm-formal-replay/v1", "status": "PASS", "source_hashes": hashes,
            "compiler_version": version.stdout.strip(), "compiler_sha256": compiler_hash,
            "toolchain_authenticated": False, "modules": modules, "declarations": 20,
            "scope": "20 listed declarations; source re-elaboration and independent generated axiom probes with warnings as errors. "
                     "The compiler and Init library are trusted dependencies. Not the whole manuscript."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    def publish(result):
        temporary = args.output.with_name(args.output.name + "." + run_id + ".tmp")
        temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, args.output)
    publish({"status": "PENDING", "run_id": run_id})
    try:
        result = verify(args.lean)
    except Exception as error:
        result = {"status": "FAIL", "error": type(error).__name__ + ": " + str(error)}
    result["run_id"] = run_id
    publish(result)
    print(json.dumps({"status": result["status"], "declarations": result.get("declarations", 0),
                      "error": result.get("error")}))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
