#!/usr/bin/env python3
"""Fault-injection check of the ACTUAL portable runner, not a math-suite replay.
Copies the package and replaces expensive mathematical subjobs with explicitly
labelled fixtures. Tests aggregation/error handling in run_portable.py unchanged.
Use alongside, not instead of, the separate unmodified full replay.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

ENVELOPE_FIXTURE='''import argparse,json,sys\nfrom pathlib import Path\np=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--work');p.add_argument('--control',default='none');a=p.parse_args()\nfail=a.control in ('omit','duplicate','unexpected')\nstatus='FAIL' if fail else 'PASS'\nPath(a.output).write_text(json.dumps({'status':status,'control':a.control,'scope':'AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION'}))\nprint(json.dumps({'status':status,'scope':'AGGREGATOR FIXTURE'}))\nsys.exit(2 if fail else 0)\n'''
CRASH_FIXTURE='''import argparse,json,sys\nfrom pathlib import Path\np=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--work');p.add_argument('--control',default='none');a=p.parse_args()\nif a.control in ('omit','duplicate','unexpected'): raise RuntimeError('INJECTED UNRELATED CHILD CRASH; not a coverage rejection')\nPath(a.output).write_text(json.dumps({'status':'PASS','scope':'AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION'}))\nprint('fixture successful')\n'''
STARTER_SUCCESS='''import argparse,json\nfrom pathlib import Path\np=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args()\nPath(a.output).write_text(json.dumps({'status':'PASS','scope':'AGGREGATOR FIXTURE; NOT MATHEMATICAL EXECUTION'}))\n'''

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--package',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    report={'scope':'Actual unmodified run_portable.py exercised in disposable copies with explicitly substituted fast mathematical subjobs; NOT a rerun of mathematical cases. Unmodified full replay is separate.','cases':[]}
    for case in ('starter_failure','export_failure','negative_control_unrelated_crash'):
        root=out/case/'package';shutil.copytree(a.package,root)
        (root/'experiments/core_recovery_bridge_01_r1/check_envelope.py').write_text(CRASH_FIXTURE if case=='negative_control_unrelated_crash' else ENVELOPE_FIXTURE)
        (root/'RPRM-CORE-FORMALIZATION-01/check_bridge.py').write_text("raise SystemExit(7)\n" if case=='starter_failure' else STARTER_SUCCESS)
        if case=='export_failure':
            (root/'experiments/core_recovery_bridge_01/runs/cursor_rcf01_envelope_02.json').unlink()
        command=[sys.executable,'-B',str(root/'run_portable.py'),'--output-dir',str(root.parent/'run')]
        r=subprocess.run(command,cwd=out,env=env,capture_output=True,text=True,timeout=20)
        (root.parent/'stdout.txt').write_text(r.stdout);(root.parent/'stderr.txt').write_text(r.stderr)
        summary=json.loads((root.parent/'run/portable_summary.json').read_text())
        report['cases'].append({'case':case,'command':command,'exit_code':r.returncode,'reported_status':summary['status'],
            'job_exit_codes':[x['exit_code'] for x in summary['jobs']],
            'finding':{'starter_failure':'Starter exit 7 is absent from aggregate ok; PASS / exit 0.',
                       'export_failure':'Export validator correctly exits 2 and aggregate exits 2, but reported summary status remains PASS.',
                       'negative_control_unrelated_crash':'Negative child crashes exit 1, and no coverage-rejection report is emitted, yet any nonzero exit satisfies the aggregate.'}[case]})
    (out/'runner_controls.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return 0
if __name__=='__main__':raise SystemExit(main())
