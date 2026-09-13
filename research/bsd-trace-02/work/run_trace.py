"""Replay every new trace calculation in a fresh, isolated source snapshot."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    destination = args.output.resolve()
    if destination.exists():
        raise FileExistsError('Use a fresh output directory; prior runs are preserved')
    source = Path(__file__).resolve().parent
    destination.mkdir(parents=True)
    (destination/'work').mkdir()
    (destination/'evidence').mkdir()
    (destination/'logs').mkdir()
    files = {}
    for path in sorted(source.glob('*.py')):
        target = destination/'work'/path.name
        shutil.copyfile(path,target)
        files[path.name] = digest(target)
    jobs = [
        ('cm_action','cm_action.py',['--output','evidence/cm_action.json']),
        ('trace125','trace125.py',['--output','evidence/trace125.json']),
        ('trace25','trace125.py',['--modulus','25','--output','evidence/trace25.json']),
        ('character_orbit','division_orbit.py',[]),
        ('independent_readback','trace_readback.py',[]),
        ('independent_point_reassembly','trace_formula_reassembly.py',[]),
    ]
    # Isolated Python, with only this frozen source directory explicitly
    # admitted for neighboring modules. No shell and no inherited PYTHONPATH.
    bootstrap = ('import runpy,sys; from pathlib import Path; '
                 'p=Path(sys.argv[1]).resolve(); sys.path.insert(0,str(p.parent)); '
                 'sys.argv=sys.argv[1:]; runpy.run_path(str(p),run_name="__main__")')
    started = time.monotonic()
    report = {'created_utc':datetime.now(timezone.utc).isoformat(),
              'python':sys.version,'executable':sys.executable,
              'source_snapshot':files,'jobs':[],
              'saved_numerical_receipts_copied_as_inputs':False,
              'status':'RUNNING', 'full_complex_BSD_identity':'OPEN'}
    for label,name,arguments in jobs:
        command = [sys.executable,'-I','-B','-c',bootstrap,
                   str(destination/'work'/name),*arguments]
        before = time.monotonic()
        process = subprocess.run(command,cwd=destination,text=True,
                                 encoding='utf-8',errors='replace',
                                 stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log = destination/'logs'/f'{label}.log'
        log.write_text(process.stdout,encoding='utf-8')
        report['jobs'].append({'name':label,'exit_code':process.returncode,
                               'elapsed_seconds':time.monotonic()-before,
                               'log':str(log.relative_to(destination)),
                               'log_sha256':digest(log)})
        print(f'{label}: exit {process.returncode}',flush=True)
        if process.returncode:
            report['status'] = 'OPEN_FAILED_PROOF_OBLIGATION_PRESERVED'
            break
    else:
        large = json.loads((destination/'evidence/trace125.json').read_text())
        small = json.loads((destination/'evidence/trace25.json').read_text())
        point_reduces = [[c % 25 for c in row] for row in large['lifted_point']] == small['lifted_point']
        orbit_reduces = all(
            a['gaussian_action'] == b['gaussian_action']
            and [c % 25 for c in a['rho']] == b['rho']
            and [c % 25 for c in a['term']] == b['term']
            for a,b in zip(large['orbit_terms'],small['orbit_terms']))
        trace_reduces = [c % 25 for c in large['trace_unit_multiple']] == small['trace_unit_multiple']
        report['cross_precision_checks'] = {
            'lifted_point':point_reduces,'all_512_orbit_terms':orbit_reduces,
            'trace':trace_reduces}
        report['status'] = ('ALL_NEW_EXACT_CALCULATIONS_VERIFIED'
                            if point_reduces and orbit_reduces and trace_reduces
                            else 'OPEN_CROSS_PRECISION_MISMATCH')
        report['unit_multiple_trace_mod125'] = large['trace_unit_multiple'][0]
        report['v5_exactly_2'] = large['v5_exactly_2']
        report['mathematical_conclusion'] = (
            'Sha(E34/Q)[5^infinity]=0, with the written theorem and inherited rank proofs')
    report['elapsed_seconds'] = time.monotonic()-started
    report['evidence_files'] = {str(p.relative_to(destination)):digest(p)
                                for p in sorted((destination/'evidence').glob('*.json'))}
    (destination/'RUN.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','elapsed_seconds','full_complex_BSD_identity')},indent=2))
    if report['status'] != 'ALL_NEW_EXACT_CALCULATIONS_VERIFIED':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
