"""Verify immutable F2 export against this review's separate fresh replay."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "input" / "fluid_dynamic_frontier_02"
TIMINGS = {"cand_fallback_wall_s", "ref_wall_s", "t_graph_s", "t_prepare_s", "t_ref_s"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def without_timing(row):
    return {k: v for k, v in row.items() if k not in TIMINGS}


def costs(rs):
    candidate = sum(r["t_prepare_s"] + r["cand_fallback_wall_s"] for r in rs)
    reference = sum(r["t_ref_s"] for r in rs)
    return {
        "candidate_prepare_plus_fallback_s": candidate,
        "reference_wrapper_s": reference,
        "candidate_over_reference": candidate / reference,
        "candidate_graph_evaluations_in_exact_fallback": sum(r["cand_graph_evals"] for r in rs),
        "note": "t_graph_s is nested in t_prepare_s and is not added twice. These wrapper timings include process costs but do not measure standalone scene construction/storage.",
    }


def main():
    hashes = []
    for line in (PAYLOAD / "HASHES.txt").read_text().splitlines():
        digest, size, name = line.split(maxsplit=2)
        p = PAYLOAD / name
        hashes.append({"path": name, "match": sha(p) == digest and p.stat().st_size == int(size)})
    saved = rows(PAYLOAD / "results" / "rows.jsonl")
    science = rows(PAYLOAD / "results" / "rows_scientific.jsonl")
    replay = rows(ROOT / "replay" / "rows.jsonl")
    saved_summary = json.loads((PAYLOAD / "results" / "summary.json").read_text())
    replay_summary = json.loads((ROOT / "replay" / "summary.json").read_text())
    summary_difference = [k for k in saved_summary if k != "elapsed_s" and saved_summary[k] != replay_summary.get(k)]
    differences = [a["id"] for a, b in zip(saved, replay) if without_timing(a) != without_timing(b)]
    receipt = {
        "date": "2026-09-12",
        "source_zip_sha256": "45cac52b845b641838a11031f245a2c0a4342a3e69cec42fc17fe0b1320ba5e9",
        "source_zip_bytes": 70475,
        "hashed_payload_files": len(hashes),
        "all_payload_hashes_match": all(x["match"] for x in hashes),
        "row_counts": {"saved": len(saved), "scientific": len(science), "replay": len(replay)},
        "saved_scientific_sha256": sha(PAYLOAD / "results" / "rows_scientific.jsonl"),
        "saved_scientific_matches_saved_rows_after_removing_timings": [without_timing(r) for r in saved] == science,
        "fresh_replay_matches_all_scientific_fields": len(saved) == len(replay) and not differences,
        "different_scene_ids": differences,
        "different_summary_fields_except_elapsed": summary_difference,
        "rows_markdown_matches_after_line_ending_normalization": (PAYLOAD / "results" / "rows.md").read_text() == (ROOT / "replay" / "rows.md").read_text(),
        "saved_costs": costs(saved),
        "fresh_replay_costs": costs(replay),
        "source_hash_checks": hashes,
        "evidence_grade": "Finite replay and source integrity; not a universal certificate soundness proof.",
        "export_limit": "run_f2.py does not regenerate rows_scientific.jsonl; this reviewer compares parsed scientific fields explicitly.",
    }
    (ROOT / "REPLAY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in receipt.items() if k != "source_hash_checks"}, indent=2))
    assert receipt["all_payload_hashes_match"]
    assert receipt["fresh_replay_matches_all_scientific_fields"]
    assert not summary_difference
    assert receipt["saved_scientific_matches_saved_rows_after_removing_timings"]


if __name__ == "__main__":
    main()
