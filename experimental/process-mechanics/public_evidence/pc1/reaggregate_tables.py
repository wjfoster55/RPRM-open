#!/usr/bin/env python3
"""Recompute paper headline numbers from public saved-row evidence.

Evidence grades:
- SOURCE_REPORTED_EXTRACT: frozen producer fields (e.g. MATCHED_INFO_HEADLINE)
- SAVED_ROW_REAGGREGATION: arithmetic derived here from public CSV.gz / pair rows
- Teaching demos remain illustrations elsewhere and are not used here

This script does not regenerate trajectories, refit learners, or prove upstream
predictors used their claimed inputs. It reaggregates saved rows only.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLIC_ROOT = HERE.parent

EPS_CLIP = 1e-6
HARD_THRESHOLD = 0.5
# Tolerances comparing SAVED_ROW_REAGGREGATION to SOURCE_REPORTED_EXTRACT.
ABS_TOL_MSE = 1e-15
REL_TOL_MSE = 1e-9
ABS_TOL_CURRENT = 5e-17  # reported extract vs observer CSV max differ ~1e-18
ABS_TOL_BRIER = 1e-12


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def close(a: float, b: float, *, abs_tol: float, rel_tol: float = 0.0) -> bool:
    return abs(a - b) <= max(abs_tol, rel_tol * max(abs(a), abs(b)))


def clip_prob(p: float, eps: float = EPS_CLIP) -> float:
    return min(1.0 - eps, max(eps, p))


def read_gzip_csv(path: Path) -> list[dict[str, str]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def recompute_hard_decisions(rows: list[dict[str, str]]) -> dict:
    by: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"n_rows": 0, "hard_error_sum": 0}
    )
    total_errors = 0
    for row in rows:
        panel = row["panel"]
        view = row["view"]
        label = float(row["label"])
        p = float(row["p"])
        if not math.isfinite(p) or not math.isfinite(label):
            raise ValueError(f"nonfinite learner row: {panel}/{view}")
        pred = 1.0 if p >= HARD_THRESHOLD else 0.0
        err = int(pred != label)
        key = (panel, view)
        by[key]["n_rows"] += 1
        by[key]["hard_error_sum"] += err
        total_errors += err
    groups = [
        {
            "panel": panel,
            "view": view,
            "n_rows": vals["n_rows"],
            "hard_error_sum": vals["hard_error_sum"],
        }
        for (panel, view), vals in sorted(by.items())
    ]
    return {
        "n_rows": len(rows),
        "n_panel_view_groups": len(groups),
        "hard_error_total": total_errors,
        "hard_error_counts_by_panel_view": groups,
        "all_hard_errors_zero": total_errors == 0,
        "threshold": HARD_THRESHOLD,
        "operation": "SAVED_ROW_REAGGREGATION",
        "rule": "hard prediction = 1 if p >= 0.5 else 0; error if prediction != label",
    }


def recompute_observer_metrics(rows: list[dict[str, str]]) -> dict:
    noisy = [r for r in rows if r["panel"] == "RC_noisy"]
    rlc = [r for r in rows if r["panel"] == "RLC"]
    if len(noisy) != 660:
        raise ValueError(f"expected 660 RC_noisy observer rows, got {len(noisy)}")
    if len(rlc) != 2391:
        raise ValueError(f"expected 2391 RLC observer rows, got {len(rlc)}")

    ls_vals = []
    raw_vals = []
    past_vals = []
    for r in noisy:
        if r["state_error_kind"] != "voltage_squared_error_V2":
            raise ValueError(f"unexpected noisy state_error_kind: {r['state_error_kind']}")
        ls_vals.append(float(r["state_error_value"]))
        raw_vals.append(float(r["raw_voltage_squared_error"]))
        past_vals.append(float(r["past_mean_squared_error"]))
    curr = []
    for r in rlc:
        if r["state_error_kind"] != "absolute_current_error_A":
            raise ValueError(f"unexpected RLC state_error_kind: {r['state_error_kind']}")
        curr.append(abs(float(r["state_error_value"])))
    return {
        "observer_rows": len(rows),
        "RC_noisy_rows": len(noisy),
        "LS_state_MSE": sum(ls_vals) / len(ls_vals),
        "raw_MSE": sum(raw_vals) / len(raw_vals),
        "past_mean_MSE": sum(past_vals) / len(past_vals),
        "RLC_rows": len(rlc),
        "max_stored_current_error": max(curr),
        "operation": "SAVED_ROW_REAGGREGATION",
    }


def recompute_withheld(pairs_doc: dict) -> dict:
    prior = pairs_doc["prior"]
    p0 = float(prior["0.0"])
    p1 = float(prior["1.0"])
    if abs(p0 - 0.5) > 1e-15 or abs(p1 - 0.5) > 1e-15:
        raise ValueError("withheld-plan reaggregation expects equal prior 1/2")
    eps = float(pairs_doc.get("clipping", {}).get("eps", EPS_CLIP))
    pairs = pairs_doc["pairs"]
    if len(pairs) != int(pairs_doc["n_pairs"]):
        raise ValueError("n_pairs does not match pairs array length")
    conflicts = 0
    losses_unclipped: list[float] = []
    losses_clipped: list[float] = []
    for pair in pairs:
        y0 = int(pair["label_release0"])
        y1 = int(pair["label_release1"])
        conflicting = y0 != y1
        if bool(pair.get("conflicting")) != conflicting:
            raise ValueError("pair conflicting flag inconsistent with labels")
        if conflicting:
            conflicts += 1
        # Realized-branch rows: two labels under equal prior mixture.
        for y in (y0, y1):
            # Mixture predictive probability for the realized branch under equal prior.
            # When plans disagree, p*=0.5; when they agree, p*= that common label.
            p_star = 0.5 if conflicting else float(y0)
            losses_unclipped.append((p_star - y) ** 2)
            p_clip = clip_prob(p_star, eps)
            # For agreeing correct hard labels, clip 0/1; for conflicts keep 0.5.
            if not conflicting:
                p_clip = clip_prob(float(y0), eps)
            losses_clipped.append((p_clip - y) ** 2)
    n = len(losses_unclipped)
    return {
        "n_pairs": len(pairs),
        "n_conflicting_pairs": conflicts,
        "n_branch_rows": n,
        "unclipped_mixture_brier": sum(losses_unclipped) / n,
        "clipped_mixture_brier": sum(losses_clipped) / n,
        "ambiguous_subset_squared_loss": 0.25,
        "operation": "SAVED_ROW_REAGGREGATION",
        "clipping_eps": eps,
    }


def build_claim_table(
    public_root: Path | None = None,
    verify_csv: Path | None = None,
) -> dict:
    root = public_root or PUBLIC_ROOT
    pe = root if root.name == "public_evidence" else root / "public_evidence"
    if not pe.is_dir():
        raise SystemExit(f"public_evidence not found under {root}")

    matched_path = pe / "pc1" / "MATCHED_INFO_HEADLINE.json"
    hard_path = pe / "pc1" / "HARD_DECISION_SUMMARY.json"
    trust_path = pe / "water" / "PR13_TRUST_EXTRACT.json"
    c1_path = pe / "c1" / "MEASUREMENT_STATUS.json"
    learner_gz = pe / "pc1" / "LEARNER_ORIGIN_PREDICTIONS.csv.gz"
    observer_gz = pe / "pc1" / "OBSERVER_ORIGIN_RECORDS.csv.gz"
    pairs_path = pe / "pc1" / "WITHHELD_PLAN_PAIRS.json"

    for required in (matched_path, learner_gz, observer_gz, pairs_path, trust_path, c1_path):
        if not required.is_file():
            raise SystemExit(f"missing required public evidence file: {required}")

    matched = load_json(matched_path)
    trust = load_json(trust_path)
    c1 = load_json(c1_path)
    pairs_doc = load_json(pairs_path)

    learner_rows = read_gzip_csv(learner_gz)
    observer_rows = read_gzip_csv(observer_gz)
    hard = recompute_hard_decisions(learner_rows)
    obs = recompute_observer_metrics(observer_rows)
    withheld = recompute_withheld(pairs_doc)

    # Optional external CSV verify: requested hash must match exported source pin.
    hard_summary_expected_sha = (
        load_json(hard_path)["source"]["sha256"] if hard_path.is_file() else None
    )
    if verify_csv is not None:
        if not verify_csv.is_file():
            raise SystemExit(f"--verify-csv path missing: {verify_csv}")
        got = sha256_file(verify_csv)
        expected = learner_gz  # compare against private source pin recorded at export
        # Prefer HARD_DECISION_SUMMARY source sha if present; else learner meta.
        expected_sha = hard_summary_expected_sha or json.loads(
            (pe / "pc1" / "SAVED_ROW_EXPORT.json").read_text(encoding="utf-8")
        )["learner"]["source_sha256"]
        if got != expected_sha:
            raise SystemExit(
                f"--verify-csv hash mismatch: got {got}, expected {expected_sha}"
            )
        optional_verify = {"path_present": True, "sha256_matches": True, "sha256": got}
    else:
        optional_verify = {
            "path_present": False,
            "note": "pass --verify-csv to fail on hash mismatch against the pinned source",
        }

    # Source-reported extract fields (not treated as independently recomputed).
    rlc_rep = matched["cases"]["RLC_voltage_only_known_plan"]["two_voltage_affine_observer"]
    noisy_rep = matched["cases"]["RC_noisy_known_plan"]
    withheld_rep = matched["cases"]["RC_withheld_future_plan"]

    reported_brier = float(withheld_rep["prior_mixture_metrics"]["brier"])
    derived_brier = withheld["clipped_mixture_brier"]

    checks = {
        "learner_rows_15475": hard["n_rows"] == 15475,
        "hard_errors_zero": hard["hard_error_total"] == 0,
        "observer_rows_3271": obs["observer_rows"] == 3271,
        "rc_noisy_rows_660": obs["RC_noisy_rows"] == 660,
        "rlc_rows_2391": obs["RLC_rows"] == 2391,
        "pairs_60": withheld["n_pairs"] == 60,
        "conflicts_24": withheld["n_conflicting_pairs"] == 24,
        "pair_array_len_matches": len(pairs_doc["pairs"]) == withheld["n_pairs"],
        "unclipped_brier_is_0_1": close(
            withheld["unclipped_mixture_brier"], 0.1, abs_tol=ABS_TOL_BRIER
        ),
        "reported_brier_matches_recomputed_clipped": close(
            reported_brier, derived_brier, abs_tol=ABS_TOL_BRIER
        ),
        "reported_conflicts_match_recomputed": int(withheld_rep["n_conflicting_pairs"])
        == withheld["n_conflicting_pairs"],
        "reported_n_pairs_match_recomputed": int(withheld_rep["n_pairs"])
        == withheld["n_pairs"],
        "reported_ls_mse_matches_recomputed": close(
            float(noisy_rep["state_MSE"]["finite_window_LS"]),
            obs["LS_state_MSE"],
            abs_tol=ABS_TOL_MSE,
            rel_tol=REL_TOL_MSE,
        ),
        "reported_raw_mse_matches_recomputed": close(
            float(noisy_rep["state_MSE"]["raw_measurement"]),
            obs["raw_MSE"],
            abs_tol=ABS_TOL_MSE,
            rel_tol=REL_TOL_MSE,
        ),
        "reported_past_mse_matches_recomputed": close(
            float(noisy_rep["state_MSE"]["plain_past_mean_excl_current"]),
            obs["past_mean_MSE"],
            abs_tol=ABS_TOL_MSE,
            rel_tol=REL_TOL_MSE,
        ),
        "reported_rlc_n_matches": int(rlc_rep["n"]) == obs["RLC_rows"],
        "reported_rlc_max_err_near_recomputed": close(
            float(rlc_rep["max_abs_i_reconstruction_error"]),
            obs["max_stored_current_error"],
            abs_tol=ABS_TOL_CURRENT,
            rel_tol=0.05,
        ),
        "optional_csv_verify_ok": optional_verify.get("sha256_matches", True)
        if verify_csv is not None
        else True,
    }

    counts_out = {
        **hard,
        "learner_gzip": {
            "path": "pc1/LEARNER_ORIGIN_PREDICTIONS.csv.gz",
            "sha256": sha256_file(learner_gz),
            "bytes": learner_gz.stat().st_size,
        },
        "source_csv_sha256_pin": hard_summary_expected_sha,
    }
    counts_path = pe / "pc1" / "hard_decision_counts.json"
    counts_path.write_text(json.dumps(counts_out, indent=2) + "\n", encoding="utf-8")

    # Refresh HARD_DECISION_SUMMARY from recomputation (public).
    hard_summary = {
        "record_type": "REAGGREGATION_OF_SAVED_LEARNER_ORIGIN_PREDICTIONS",
        "evidence_grade": "SAVED_ROW_REAGGREGATION",
        "operation": "SAVED_ROW_REAGGREGATION",
        "note": (
            "Hard-decision counts recomputed from public LEARNER_ORIGIN_PREDICTIONS.csv.gz "
            "using p/label at threshold 0.5. Not a teaching demo."
        ),
        "source": {
            "public_gzip": "pc1/LEARNER_ORIGIN_PREDICTIONS.csv.gz",
            "public_gzip_sha256": sha256_file(learner_gz),
            "sha256": hard_summary_expected_sha
            or "69e19af411e50424e719264f3ef732e11c0517fd89066f598bb4b9452834755d",
            "bytes": 2041659,
            "scientific_source_identifier": "d2e63b56d79d3c620e8aec8121adf18bcb7395bd",
        },
        **{k: hard[k] for k in (
            "n_rows",
            "n_panel_view_groups",
            "hard_error_total",
            "hard_error_counts_by_panel_view",
            "all_hard_errors_zero",
            "threshold",
            "rule",
        )},
    }
    hard_path.write_text(json.dumps(hard_summary, indent=2) + "\n", encoding="utf-8")

    claim_table = {
        "record_type": "CLAIM_TABLE_FROM_PUBLIC_SAVED_ROWS",
        "operations": {
            "SOURCE_REPORTED_EXTRACT": "MATCHED_INFO_HEADLINE / PR13 / C1 status card fields",
            "SAVED_ROW_REAGGREGATION": "derived below from public CSV.gz and pair rows",
            "not_done_here": [
                "model regeneration",
                "learner refitting",
                "source-trajectory resimulation",
                "independent PR14 audit replay",
                "C1 figure redigitization",
            ],
        },
        "inputs": {
            "LEARNER_ORIGIN_PREDICTIONS.csv.gz": {
                "path": "pc1/LEARNER_ORIGIN_PREDICTIONS.csv.gz",
                "sha256": sha256_file(learner_gz),
                "evidence_grade": "SAVED_ROW_EXPORT",
            },
            "OBSERVER_ORIGIN_RECORDS.csv.gz": {
                "path": "pc1/OBSERVER_ORIGIN_RECORDS.csv.gz",
                "sha256": sha256_file(observer_gz),
                "evidence_grade": "SAVED_ROW_EXPORT",
            },
            "WITHHELD_PLAN_PAIRS.json": {
                "path": "pc1/WITHHELD_PLAN_PAIRS.json",
                "sha256": sha256_file(pairs_path),
                "evidence_grade": "SOURCE_REPORTED_EXTRACT",
            },
            "MATCHED_INFO_HEADLINE.json": {
                "path": "pc1/MATCHED_INFO_HEADLINE.json",
                "sha256": sha256_file(matched_path),
                "evidence_grade": "SOURCE_REPORTED_EXTRACT",
                "note": "Compared to recomputation; not copied as the sole arithmetic support",
            },
            "PR13_TRUST_EXTRACT.json": {
                "path": "water/PR13_TRUST_EXTRACT.json",
                "sha256": sha256_file(trust_path),
                "evidence_grade": "SOURCE_REPORTED_EXTRACT",
            },
            "MEASUREMENT_STATUS.json": {
                "path": "c1/MEASUREMENT_STATUS.json",
                "sha256": sha256_file(c1_path),
                "evidence_grade": "SOURCE_REPORTED_EXTRACT",
            },
        },
        "derived": {
            "evidence_grade": "SAVED_ROW_REAGGREGATION",
            "hard_decisions": hard,
            "observer_metrics": obs,
            "withheld_plan": withheld,
        },
        "headline_numbers": {
            "PC-STATE-01_rlc_rows_recomputed": obs["RLC_rows"],
            "PC-STATE-01_max_abs_i_error_recomputed": obs["max_stored_current_error"],
            "PC-STATE-01_max_abs_i_error_source_reported": rlc_rep[
                "max_abs_i_reconstruction_error"
            ],
            "PC-EST-01_finite_window_LS_MSE_recomputed": obs["LS_state_MSE"],
            "PC-EST-01_raw_measurement_MSE_recomputed": obs["raw_MSE"],
            "PC-EST-01_plain_past_mean_MSE_recomputed": obs["past_mean_MSE"],
            "PC-EST-01_finite_window_LS_event_n_source_reported": noisy_rep[
                "finite_window_LS_event"
            ]["n"],
            "PC-INPUT-01_n_pairs_recomputed": withheld["n_pairs"],
            "PC-INPUT-01_n_conflicting_pairs_recomputed": withheld["n_conflicting_pairs"],
            "PC-INPUT-01_unclipped_mixture_brier_recomputed": withheld[
                "unclipped_mixture_brier"
            ],
            "PC-INPUT-01_clipped_mixture_brier_recomputed": withheld[
                "clipped_mixture_brier"
            ],
            "PC-INPUT-01_prior_mixture_brier_source_reported": reported_brier,
            "PC-NULL-01_n_rows_recomputed": hard["n_rows"],
            "PC-NULL-01_hard_error_total_recomputed": hard["hard_error_total"],
            "W-TRUST-01_joined": trust["public_map_frozen_numbers"]["joined"],
            "W-TRUST-01_exact": trust["public_map_frozen_numbers"]["exact"],
            "W-TRUST-01_primary_11_5": trust["public_map_frozen_numbers"]["primary_11_5"],
            "C-MEAS-01_status": c1["status"],
            "C-MEAS-01_primary_doi": c1["primary_citation"]["doi"],
        },
        "consistency_checks": checks,
        "optional_csv_verify": optional_verify,
        "artifacts_written": {
            "hard_decision_counts.json": "pc1/hard_decision_counts.json",
            "HARD_DECISION_SUMMARY.json": "pc1/HARD_DECISION_SUMMARY.json",
        },
        "boundary": (
            "Saved-row reaggregation only. Does not establish that upstream predictors "
            "used their claimed inputs, nor regenerate source trajectories."
        ),
    }
    return claim_table


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--public-root",
        type=Path,
        default=PUBLIC_ROOT,
        help="Path to public_evidence/ or its parent process-mechanics dir",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write CLAIM_TABLE.json here (default: public_evidence/pc1/CLAIM_TABLE.json)",
    )
    parser.add_argument(
        "--verify-csv",
        type=Path,
        help="Path to uncompressed LEARNER_ORIGIN_PREDICTIONS.csv; hash mismatch fails",
    )
    args = parser.parse_args()
    try:
        table = build_claim_table(args.public_root, verify_csv=args.verify_csv)
    except ValueError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        raise SystemExit(1) from exc

    pe = (
        args.public_root
        if args.public_root.name == "public_evidence"
        else args.public_root / "public_evidence"
    )
    out = args.output or (pe / "pc1" / "CLAIM_TABLE.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(table, indent=2) + "\n"
    out.write_text(text, encoding="utf-8")
    print(text, end="")
    print("wrote", out)
    print("sha256", hashlib.sha256(text.encode()).hexdigest())

    failed = [k for k, v in table["consistency_checks"].items() if v is False]
    if failed:
        print(json.dumps({"status": "FAIL", "failed_checks": failed}, indent=2))
        raise SystemExit(1)
    print(json.dumps({"status": "PASS", "failed_checks": []}, indent=2))


if __name__ == "__main__":
    main()
