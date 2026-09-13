#!/usr/bin/env python3
"""Replay two preserved E5 source programs to fresh output paths.

This checks byte bindings and selected reproduced mathematical records. It is
NOT an independent verifier, a theorem prover, or the new interval experiment.
Python 3.10+, standard library. Run from any working directory.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    with path.open(encoding='utf-8') as stream:
        value = json.load(stream)
    require(isinstance(value, dict), f'JSON object required: {path}')
    return value


def check_bindings() -> list[dict]:
    manifest = read_json(ROOT / 'SOURCE_BINDINGS.json')
    seen = set()
    rows = []
    for item in manifest['files']:
        rel = item['path']
        require(isinstance(rel, str) and rel not in seen, 'Invalid or duplicate source binding')
        seen.add(rel)
        path = (ROOT / rel).resolve()
        require(ROOT in path.parents, f'Path escapes package: {rel}')
        require(path.is_file(), f'Missing bound input: {rel}')
        require(path.stat().st_size == item['size'], f'Size mismatch: {rel}')
        require(digest(path) == item['sha256'], f'Hash mismatch: {rel}')
        rows.append({'path': rel, 'sha256': item['sha256'], 'match': True})
    require(len(rows) == 17, 'Expected exactly 17 preserved source files')
    return rows


def run_source(stage: str, script: Path, output: Path, timeout: int) -> tuple[dict, dict]:
    receipt = output / f'{stage}_receipt.json'
    cmd = [sys.executable, '-B', str(script), '--output', str(receipt)]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=output, text=True, capture_output=True,
                          timeout=timeout, encoding='utf-8', errors='replace')
    elapsed = time.perf_counter() - start
    (output / f'{stage}.stdout.txt').write_text(proc.stdout, encoding='utf-8')
    (output / f'{stage}.stderr.txt').write_text(proc.stderr, encoding='utf-8')
    require(proc.returncode == 0, f'{stage} exited {proc.returncode}; inspect logs')
    value = read_json(receipt)
    require(value.get('status') == 'PASS', f'{stage} did not report PASS')
    metadata = {'stage': stage, 'command': cmd, 'exit_code': proc.returncode,
                'elapsed_seconds': elapsed, 'receipt': receipt.name,
                'receipt_sha256': digest(receipt),
                'executed_script_sha256': digest(script)}
    return value, metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'runs' / 'replay')
    parser.add_argument('--timeout', type=int, default=180,
                        help='Per-program timeout in seconds; not a promised run time')
    args = parser.parse_args()
    output = args.output.resolve()
    require(args.timeout > 0, 'Timeout must be positive')
    for protected in (ROOT / 'inputs', ROOT / 'context', ROOT / 'tools'):
        require(output != protected and protected not in output.parents,
                'Output must not be inside preserved inputs/context/tools')
    require(output != ROOT, 'Output must be a separate run directory')
    require(not output.exists() or not any(output.iterdir()),
            'Choose a new output path; earlier receipts are not overwritten')
    output.mkdir(parents=True, exist_ok=True)
    report = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Source replay and selected exact result comparison ONLY',
              'python': platform.python_version(), 'platform': platform.platform(),
              'independent_codex_verification': 'NOT_RUN_BY_THIS_LAUNCHER',
              'new_two_sided_interval': 'NOT_RUN_BY_THIS_LAUNCHER',
              'stages': []}
    try:
        report['source_bindings'] = check_bindings()
        descent, desc_meta = run_source('descent', ROOT / 'inputs/descent/e5_descent.py', output, args.timeout)
        report['stages'].append(desc_meta)
        analytic, ana_meta = run_source('analytic', ROOT / 'inputs/analytic/certify_e5.py', output, args.timeout)
        report['stages'].append(ana_meta)
        old_d = read_json(ROOT / 'inputs/descent/E5_DESCENT_RECEIPT.json')
        old_a = read_json(ROOT / 'inputs/analytic/CERTIFICATE.json')
        dkeys = ['initial_product_square_candidates', 'real_admissible', 'modular_filters',
                 'four_cosets', 'eight_realized_classes', 'coarse_vs_finer_example', 'decoder_tests']
        akeys = ['point_counts', 'nonzero_coefficients_through_20', 'alpha_enclosure',
                 'positive_first_term_lower_bound', 'retained_negative_magnitude_upper_bound',
                 'entire_omitted_tail_magnitude_upper_bound', 'Lprime_lower_bound',
                 'certified_conclusion', 'finite_cube_recoding']
        comparisons = []
        for stage, new, old, keys in [('descent', descent, old_d, dkeys),
                                      ('analytic', analytic, old_a, akeys)]:
            for key in keys:
                require(new[key] == old[key], f'Historical result discrepancy: {stage}.{key}')
                comparisons.append({'stage': stage, 'field': key, 'equal': True})
        report['historical_result_comparisons'] = comparisons
        report['post_run_source_bindings'] = check_bindings()
        report['summary'] = {
            'source_files_unchanged': 17,
            'descent_initial_candidates': descent['real_admissible'],
            'descent_realized_classes': len(descent['eight_realized_classes']),
            'descent_decoder_cases': descent['decoder_tests']['count'],
            'analytic_lower_rational': {
                k: analytic['Lprime_lower_bound'][k] for k in ('numerator', 'denominator')},
            'cube_candidates': analytic['finite_cube_recoding']['candidate_vertices'],
            'optional_decimal_status': (analytic.get('numerical_display') or {}).get('status', 'NOT_RUN')}
        report['status'] = 'REPLAY_PASS'
    except Exception as exc:
        report['status'] = 'REPLAY_FAIL'
        report['error'] = f'{type(exc).__name__}: {exc}'
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (output / 'REPLAY.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'output': str(output),
                      'summary': report.get('summary'), 'error': report.get('error')}, indent=2))
    return 0 if report['status'] == 'REPLAY_PASS' else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError) as exc:
        print(f'{type(exc).__name__}: {exc}', file=sys.stderr)
        raise SystemExit(1)
