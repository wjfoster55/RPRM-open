"""Replay E34 from source in a new directory, retaining every stage's output.

Python standard library only. No old receipt is copied into the new run.
This orchestrates computations, not a formal verifier of the written proofs.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='A new directory; existing destinations are refused')
    args = parser.parse_args()
    destination = args.output.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    work = destination / 'work'
    evidence = destination / 'evidence'
    work.mkdir()
    evidence.mkdir()
    source_paths = sorted((ROOT / 'work').glob('*.py')) + [ROOT / 'work/BUDGET.json']
    for path in source_paths:
        shutil.copyfile(path, work / path.name)
    run = {'started_utc': datetime.now(timezone.utc).isoformat(),
           'python': sys.version, 'executable': sys.executable,
           'copied_inputs': {p.name: digest(p) for p in source_paths},
           'copied_saved_receipts': False, 'stages': [],
           'status': 'RUNNING', 'evidence_scope':
           'Fresh computations and dependency consistency; written proofs remain required'}
    record = destination / 'RUN.json'

    def save():
        record.write_text(json.dumps(run, indent=2) + '\n', encoding='utf-8')

    save()
    stages = ['arithmetic', 'local_inputs', 'generator', 'interval',
              'interval_audit', 'midpoint', 'factor_frontier']
    for name in stages:
        command = [sys.executable, '-I', '-B', str(work / (name + '.py'))]
        if name != 'interval_audit':
            command += ['--output', str(evidence / (name + '.json'))]
        if name == 'local_inputs':
            command += ['--limit', '1000']
        started = time.monotonic()
        result = subprocess.run(command, cwd=destination, capture_output=True,
                                text=True, encoding='utf-8', errors='replace')
        log = evidence / (name + '_execution.log')
        log.write_text(result.stdout + '\nSTDERR:\n' + result.stderr, encoding='utf-8')
        row = {'stage': name, 'command': command, 'exit_code': result.returncode,
               'elapsed_seconds': time.monotonic() - started,
               'source_sha256': digest(work / (name + '.py')),
               'log_sha256': digest(log)}
        receipt = evidence / (name + '.json')
        if receipt.exists():
            row['receipt_sha256'] = digest(receipt)
        run['stages'].append(row)
        save()
        print(f'{name}: exit {result.returncode}; {row["elapsed_seconds"]:.2f}s', flush=True)
        if result.returncode != 0:
            run['status'] = 'FAILED_STAGE_PRESERVED'
            save()
            raise SystemExit(f'{name} failed; inspect {log}')

    receipts = {name: json.loads((evidence / (name + '.json')).read_text(encoding='utf-8'))
                for name in stages}
    try:
        a, g, i, f = (receipts[name] for name in
                      ('arithmetic', 'generator', 'interval', 'factor_frontier'))
        assert a['status'] == g['status'] == receipts['midpoint']['status'] == 'PASS'
        assert a['conclusions']['rank'] == 2
        assert a['conclusions']['selmer_2_order'] == 16
        assert a['conclusions']['sha_2_primary'] == 'ZERO'
        assert a['conclusions']['rational_torsion_order'] == f['torsion_order'] == 4
        assert g['conclusion']['free_index'] == 1
        assert i['status'] == 'CERTIFIED_COEFFICIENT_INTERVAL'
        assert i['selected_cutoff'] == 160
        assert [r['status'] for r in i['attempts']] == [
            'OPEN_WITH_THIS_TAIL_BOUND', 'OPEN_WITH_THIS_TAIL_BOUND', 'ENCLOSURE_SUCCEEDED']
        assert F(i['lambda2_interval'][0]) > 0
        assert i['general_BSD'] == 'OPEN'
        assert f['status'] == 'RIGOROUS_FACTOR_COMPARISON_ONLY'
        assert f['sha_order'] == f['full_BSD_identity'] == 'NOT_ESTABLISHED'
        assert F(f['bsd_quotient'][0]) < 1 < F(f['bsd_quotient'][1])
        assert receipts['interval_audit']['second_derivative_matches']
        assert receipts['interval_audit']['fourth_derivative_matches']
        step = receipts['midpoint']['directed_step_correction']
        assert F(step['full_gap']) == F(-1, 5)
        assert F(step['half_gap']) == F(-1, 10)
        assert F(step['half_step_endpoint']) == F(1, 2)
        for name, receipt in receipts.items():
            if 'source_sha256' in receipt:
                assert receipt['source_sha256'] == digest(work / (name + '.py'))
        for name, expected in run['copied_inputs'].items():
            assert digest(work / name) == expected
        run['consistency_checks'] = {
            'rank': 2, 'basis_index': 1, 'sha_2_primary': 'ZERO',
            'analytic_rank': '2, using cited low-rank theorem plus positive second coefficient',
            'full_sha': 'NOT_ESTABLISHED', 'full_BSD_identity': 'NOT_ESTABLISHED',
            'midpoint_full_and_half_gap': ['-1/5', '-1/10'],
            'failed_tail_attempts_preserved': [40, 80]}
        run['status'] = 'FRESH_REPLAY_AND_CONSISTENCY_CHECKS_COMPLETED'
    except Exception as exc:
        run['status'] = 'FAILED_CONSISTENCY_CHECK_PRESERVED'
        run['exception'] = repr(exc)
        save()
        raise
    run['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save()
    print(json.dumps({'status': run['status'], 'record': str(record),
                      'full_BSD_identity': 'NOT_ESTABLISHED'}, indent=2))


if __name__ == '__main__':
    main()
