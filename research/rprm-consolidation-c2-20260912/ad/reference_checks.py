"""Independent SQL/direct-arithmetic oracle; imports no specimen decisions."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sqlite3


def reference(values):
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE rows (occurrence_id TEXT PRIMARY KEY, value INTEGER NOT NULL)")
        db.executemany("INSERT INTO rows VALUES (?,?)", [(str(i), v) for i, v in enumerate(values)])
        pair = list(db.execute("SELECT COALESCE(SUM(value),0), COALESCE(SUM(DISTINCT value),0) FROM rows").fetchone())
    direct = [sum(values), sum(set(values))]
    excess = sum((count - 1) * value for value, count in Counter(values).items())
    return {"values": list(values), "sql_pair": pair, "direct_pair": direct,
            "multiplicity_difference": excess,
            "ok": pair == direct and pair[0] - pair[1] == excess}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("refusing to overwrite existing output")
    case_file = Path(__file__).with_name("CASES.json")
    spec = json.loads(case_file.read_text(encoding="utf-8"))
    rows = []
    for size in range(spec["max_rows"] + 1):
        for bag in combinations_with_replacement(spec["domain"], size):
            row = reference(bag)
            row["id"] = f"bag-{len(rows):03d}"
            rows.append(row)
    fixtures = {}
    for name, table in spec["fixtures"].items():
        # This independent admission predicate does not call specimen.validate.
        valid = (isinstance(table, list) and len(table) <= spec["max_rows"]
                 and all(isinstance(r, list) and len(r) == 2 for r in table))
        if valid:
            ids = [r[0] for r in table]
            valid = (all(isinstance(i, str) and bool(i) for i in ids)
                     and len(ids) == len(set(ids))
                     and all(type(r[1]) is int and r[1] in spec["domain"] for r in table))
        fixtures[name] = reference([r[1] for r in table]) if valid else {"status": "ADMISSION_ERROR"}
    with sqlite3.connect(":memory:") as db:
        native_empty = list(db.execute("SELECT SUM(v),SUM(DISTINCT v) FROM (SELECT 1 AS v WHERE 0)").fetchone())
    ok = (len(rows) == 126 and all(r["ok"] for r in rows)
          and all(r.get("ok", True) for r in fixtures.values()) and native_empty == [None, None])
    result = {"status": "PASS" if ok else "FAIL", "evidence_grade": "development",
              "case_sha256": sha256(case_file.read_bytes()).hexdigest(),
              "sqlite_version": sqlite3.sqlite_version, "native_sql_empty": native_empty,
              "rows": rows, "fixtures": fixtures,
              "counts": {"bags": len(rows), "equal_bags": sum(r["sql_pair"][0] == r["sql_pair"][1] for r in rows)}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(f"{result['status']}: independent reference; {len(rows)} bags")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
