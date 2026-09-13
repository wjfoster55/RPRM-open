"""Fresh E34 identity continuation, preserving OPEN mathematical obligations.

Copies executable source into a new directory, reruns the full input
experiment and all new calculations, and records the scoped outcomes.
Standard library only. Existing output directories are refused.
"""
import argparse
from datetime import datetime, timezone
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
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    destination = args.output.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    work, evidence = destination/'work', destination/'evidence'
    work.mkdir()
    evidence.mkdir()
    for path in (ROOT/'work').glob('*.py'):
        shutil.copyfile(path, work/path.name)
    snapshot = destination/'input_source'
    (snapshot/'work').mkdir(parents=True)
    input_paths = list((ROOT/'input_source/work').glob('*.py'))
    input_paths.append(ROOT/'input_source/work/BUDGET.json')
    for path in input_paths:
        shutil.copyfile(path, snapshot/'work'/path.name)
    for path in (ROOT/'input_source').glob('*.md'):
        shutil.copyfile(path, snapshot/path.name)
    record = {
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version, 'executable': sys.executable,
        'source_sha256': {p.name: digest(p) for p in sorted(work.glob('*.py'))},
        'input_source_sha256': {p.name: digest(p) for p in sorted((snapshot/'work').iterdir())},
        'copied_old_receipts': False, 'steps': [], 'status': 'RUNNING',
        'scope': 'Fresh computations; cited and written proof premises remain necessary'}
    record_path = destination/'RUN.json'

    def save():
        record_path.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')

    def execute(name, command):
        begin = time.monotonic()
        completed = subprocess.run(command, cwd=destination, text=True,
                                   capture_output=True, encoding='utf-8', errors='replace')
        log = evidence/(name+'_execution.log')
        log.write_text(completed.stdout+'\nSTDERR:\n'+completed.stderr, encoding='utf-8')
        row = {'name': name, 'command': command, 'exit_code': completed.returncode,
               'seconds': time.monotonic()-begin, 'log_sha256': digest(log)}
        record['steps'].append(row)
        save()
        print(f'{name}: exit {completed.returncode}; {row["seconds"]:.2f}s', flush=True)
        if completed.returncode:
            record['status'] = 'FAILED_EXECUTION_PRESERVED'
            save()
            raise SystemExit(f'Inspect {log}')

    save()
    execute('fresh_input_experiment', [sys.executable, '-I', '-B',
            str(snapshot/'work/run_all.py'), '--output', str(destination/'inputs')])
    for name in ('height_series', 'odd_prime', 'identity_gate'):
        command = [sys.executable, '-I', '-B', str(work/(name+'.py')),
                   '--output', str(evidence/(name+'.json'))]
        if name == 'identity_gate':
            command += ['--run', str(destination/'inputs')]
        execute(name, command)
    try:
        receipts = {name: json.loads((evidence/(name+'.json')).read_text(encoding='utf-8'))
                    for name in ('height_series', 'odd_prime', 'identity_gate')}
        assert receipts['height_series']['status'] == 'PASS'
        assert receipts['odd_prime']['status'] == 'OPEN'
        gate = receipts['identity_gate']
        assert gate['actual_exact_analytic_identity'] == gate['full_BSD'] == 'NOT_ESTABLISHED'
        assert gate['conditional_rational_gate']['premise_for_actual_quotient'] == 'NOT_ESTABLISHED'
        assert gate['separate_five_adic_trace_readout']['actual_trace_mod125'] is None
        for path in work.glob('*.py'):
            assert digest(path) == record['source_sha256'][path.name]
        for path in (snapshot/'work').iterdir():
            assert digest(path) == record['input_source_sha256'][path.name]
        record['receipts_sha256'] = {name: digest(evidence/(name+'.json')) for name in receipts}
        record['input_run_sha256'] = digest(destination/'inputs/RUN.json')
        record['mathematical_outcome'] = {
            'height_series_and_conditional_equality_criteria': 'PROVED_AT_STATED_SCOPE',
            'odd_prime_5_trace': 'NOT_COMPUTED', 'odd_prime_5_Sha': 'NOT_ESTABLISHED',
            'actual_quotient_denominator_bound': 'NOT_ESTABLISHED',
            'exact_complex_BSD_identity': 'NOT_ESTABLISHED', 'general_BSD': 'OPEN'}
        record['status'] = 'FRESH_COMPUTATIONS_COMPLETED_WITH_OPEN_PROOF_OBLIGATIONS'
    except Exception as exc:
        record['status'] = 'FAILED_AGGREGATION_PRESERVED'
        record['exception'] = repr(exc)
        save()
        raise
    record['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save()
    print(json.dumps({'status': record['status'], 'record': str(record_path),
                      'exact_complex_BSD_identity': 'NOT_ESTABLISHED'}, indent=2))


if __name__ == '__main__':
    main()
