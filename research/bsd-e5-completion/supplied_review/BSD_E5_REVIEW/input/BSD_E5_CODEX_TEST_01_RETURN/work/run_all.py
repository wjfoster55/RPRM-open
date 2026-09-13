"""Replay this single E5 experiment into a new directory (standard library only)."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='New output directory; existing paths are rejected.')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise ValueError('Choose a new output directory; delivered evidence is preserved.')
    for protected in (ROOT / 'supplied', ROOT / 'work', ROOT / 'evidence'):
        if output == protected or protected in output.parents:
            raise ValueError(f'Output lies in a protected delivery directory: {protected}')
    output.mkdir(parents=True)
    commands = [
        ('supplied_replay', ROOT / 'supplied/BSD_E5_CODEX_TEST_01/tools/replay_inputs.py',
         ['--output', str(output / 'supplied_replay')]),
        ('arithmetic', ROOT / 'work/arithmetic_check.py',
         ['--output', str(output / 'arithmetic.json')]),
        ('model_binding', ROOT / 'work/model_binding_check.py',
         ['--output', str(output / 'model_binding.json')]),
        ('analytic', ROOT / 'work/analytic_check.py',
         ['--output-dir', str(output / 'analytic')]),
        ('interval_peer', ROOT / 'work/interval_peer_check.py',
         ['--input-dir', str(output / 'analytic'),
          '--output', str(output / 'interval_peer_review.json')]),
    ]
    report = {'experiment': 'BSD E5 test 01',
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'python': sys.version, 'platform': platform.platform(), 'commands': [],
              'optional_backend_probe': {
                  'modules_present': {name: importlib.util.find_spec(name) is not None
                                      for name in ('sage', 'cypari2', 'sympy', 'flint', 'mpmath')},
                  'executables': {name: shutil.which(name) for name in ('sage', 'gp')},
                  'independent_backend_comparison': 'NOT_RUN'},
              'scope': 'Fresh source replay and finite exact computations. '
                       'Cited theorem applicability is audited in the written reports.'}
    failed = False
    for name, script, arguments in commands:
        command = [sys.executable, '-B', str(script), *arguments]
        start = time.perf_counter()
        process = subprocess.run(command, cwd=ROOT, capture_output=True,
                                 encoding='utf-8', errors='replace')
        (output / f'{name}.stdout.txt').write_text(process.stdout, encoding='utf-8')
        (output / f'{name}.stderr.txt').write_text(process.stderr, encoding='utf-8')
        report['commands'].append({
            'stage': name, 'command': command, 'exit_code': process.returncode,
            'elapsed_seconds': time.perf_counter() - start,
            'script': script.relative_to(ROOT).as_posix(),
            'script_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
            'stdout': f'{name}.stdout.txt', 'stderr': f'{name}.stderr.txt'})
        print(f'{name}: exit {process.returncode}', flush=True)
        failed |= process.returncode != 0
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    report['status'] = 'EXECUTION_FAILURE' if failed else 'ALL_COMMANDS_COMPLETED'
    (output / 'RUN.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
