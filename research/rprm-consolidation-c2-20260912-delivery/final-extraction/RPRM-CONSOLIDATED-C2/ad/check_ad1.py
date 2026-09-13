"""Run frozen AD1 development cases; report and artifacts must be fresh."""
import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

# Isolated Python does not add the script directory to sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scoped_claim import AdmissionError, OrdinaryCache, ScopedStore, encoded


def metric_delta(after, before):
    return {key: after[key] - before[key] for key in after}


def save_new(path, value):
    with path.open("xb") as stream:
        stream.write(encoded(value) + b"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = args.output.resolve()
    artifacts = report.with_name(report.stem + ".artifacts")
    if report.exists() or artifacts.exists():
        parser.error("refusing to overwrite existing report or artifact directory")
    spec_path = Path(__file__).with_name("CASES.json")
    spec_bytes = spec_path.read_bytes()
    spec = json.loads(spec_bytes)
    frozen = json.loads(Path(__file__).with_name("CASE_FREEZE.json").read_text(encoding="utf-8"))
    if sha256(spec_bytes).hexdigest() != frozen["CASES.json"]:
        parser.error("case definitions differ from pre-run freeze")
    report.parent.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir()
    cold = artifacts / "cold"
    cold.mkdir()
    for name, table in spec["fixtures"].items():
        save_new(cold / (name + ".json"), table)
    reference_path = artifacts / "reference.json"
    child = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).with_name("reference_checks.py")),
                            "--output", str(reference_path)], capture_output=True, text=True)
    if child.returncode != 0:
        result = {"status": "FAIL", "stage": "independent reference", "stdout": child.stdout, "stderr": child.stderr}
        save_new(report, result)
        return 1
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    stores = {"scoped": ScopedStore(artifacts), "ordinary": OrdinaryCache(artifacts)}
    records = {arm: {} for arm in stores}
    rows = []
    for case in spec["cases"]:
        action = case["action"]
        if action == "remove_hot":
            (cold / (case["record"] + ".json")).unlink()
        elif action == "tamper_hot":
            (cold / (case["record"] + ".json")).write_bytes(encoded(spec["fixtures"]["changed"]) + b"\n")
        arm_results = {}
        for arm, store in stores.items():
            before = asdict(store.metrics)
            if action in ("promote", "admission"):
                try:
                    record = store.promote("cold/" + case["fixture"] + ".json")
                    records[arm][case["fixture"]] = record
                    answer = store.hot(record)
                except AdmissionError:
                    answer = {"status": "ADMISSION_ERROR"}
            elif action in ("hot", "remove_hot", "tamper_hot"):
                answer = store.hot(records[arm][case["record"]])
            elif action == "conditional":
                answer = store.conditional(records[arm][case["record"]])
            elif action == "lookup":
                answer = store.lookup(records[arm][case["record"]], case["query_id"])
            elif action == "universal":
                answer = store.universal()
            elif action == "unsupported":
                answer = store.unsupported()
            else:
                raise ValueError("unknown frozen action")
            expected_status = "ADMISSION_ERROR" if action == "admission" else case.get("status", "ONE")
            ok = answer["status"] == expected_status
            if "pair" in case:
                ok = ok and answer.get("value") == case["pair"]
                fixture = case.get("fixture", case.get("record", "changed"))
                ok = ok and answer.get("value") == reference["fixtures"][fixture]["sql_pair"]
                if expected_status == "ONE":
                    ok = ok and answer.get("equal") == (case["pair"][0] == case["pair"][1])
            if "value" in case:
                ok = ok and answer.get("value") == case["value"]
            if action == "admission":
                ok = ok and reference["fixtures"][case["fixture"]]["status"] == "ADMISSION_ERROR"
            delta = metric_delta(asdict(store.metrics), before)
            if action in ("hot", "remove_hot", "tamper_hot", "conditional", "unsupported"):
                ok = ok and delta["source_read_attempts"] == 0 and delta["aggregate_recomputations"] == 0
            if case["id"] in ("harmless_reorder", "harmless_relabel"):
                ok = ok and delta["source_reads"] == 1 and delta["aggregate_recomputations"] == 0
            if case["id"] in ("changed_instance", "conditional_source_change"):
                ok = ok and delta["source_reads"] == 1 and delta["aggregate_recomputations"] == 1
            arm_results[arm] = {"answer": answer, "metrics": delta, "ok": ok}
        rows.append({"id": case["id"], "arms": arm_results,
                     "ok": all(r["ok"] for r in arm_results.values())
                           and arm_results["scoped"]["answer"] == arm_results["ordinary"]["answer"]})
    sequence_totals = {arm: asdict(store.metrics) for arm, store in stores.items()}
    for expected in reference["rows"]:
        name = expected["id"]
        table = [[str(i), value] for i, value in enumerate(expected["values"])]
        save_new(cold / (name + ".json"), table)
        arm_results = {}
        for arm, store in stores.items():
            before = asdict(store.metrics)
            record = store.promote("cold/" + name + ".json")
            answer = store.hot(record)
            arm_results[arm] = {"answer": answer, "metrics": metric_delta(asdict(store.metrics), before),
                                "ok": answer["value"] == expected["sql_pair"]
                                      and answer["equal"] == (expected["sql_pair"][0] == expected["sql_pair"][1])}
        rows.append({"id": name, "arms": arm_results, "ok": all(r["ok"] for r in arm_results.values())})
    retained = {}
    for arm, store in stores.items():
        payload = store.retained()
        save_new(artifacts / (arm + "-hot.json"), payload)
        retained[arm] = {"logical_serialized_bytes": len(encoded(payload)),
                         "records": len(payload["records"]), "cache_entries": len(payload["cache"])}
    cold_files = list(cold.glob("*.json"))
    ok = (reference["status"] == "PASS" and len(rows) == len(spec["cases"]) + 126
          and len({r["id"] for r in rows}) == len(rows) and all(r["ok"] for r in rows))
    result = {"status": "PASS" if ok else "FAIL", "evidence_grade": "development",
              "case_sha256": sha256(spec_bytes).hexdigest(), "case_count": len(spec["cases"]),
              "reference_bags": 126, "rows": rows, "sequence_metrics": sequence_totals,
              "total_metrics": {arm: asdict(store.metrics) for arm, store in stores.items()},
              "retained_hot": retained, "retained_cold": {"files": len(cold_files), "bytes": sum(p.stat().st_size for p in cold_files)},
              "reference_report": str(reference_path.relative_to(report.parent)),
              "python": sys.version, "limits": "bounded development; shared I/O and admission; no performance benefit established"}
    save_new(report, result)
    print(f"{result['status']}: {len(spec['cases'])} named cases and 126 aggregate bags; both arms")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
