"""Assemble this E5 experiment's evidence index; this is not a theorem verifier."""
from __future__ import annotations

from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'supplied/BSD_E5_CODEX_TEST_01'
TASK_IDS = ['R01', 'A01', 'A02', 'B01', 'B02', 'C01', 'D01', 'J01']
CONTROL_IDS = ['K01_OFF_CURVE', 'K02_MODEL_BINDING', 'K03_EULER_RECURRENCE',
               'K04_NO_TAIL', 'K05_LOST_REMAINDER', 'K06_FRAME_TRANSPORT']


def read(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def write(rel, value):
    (ROOT / rel).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def identity(rel):
    data = (ROOT / rel).read_bytes()
    return {'path': rel, 'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data)}


def main():
    plan = read('supplied/BSD_E5_CODEX_TEST_01/TEST_PLAN.json')
    assert [r['id'] for r in plan['required_tasks']] == TASK_IDS
    assert [r['id'] for r in plan['required_controls']] == CONTROL_IDS
    arithmetic = read('evidence/arithmetic.json')
    analytic = read('evidence/analytic.json')
    theory = read('evidence/analytic_theorems.json')
    model = read('evidence/model_binding.json')
    interval = read('DERIVATIVE_INTERVAL.json')
    replay = read('evidence/codex_replay/REPLAY.json')
    portable = read('runs/portable_validation/RUN.json')
    assert replay['status'] == 'REPLAY_PASS'
    assert portable['status'] == 'ALL_COMMANDS_COMPLETED'
    assert arithmetic['status'] == 'PASS' and theory['status'] == 'CONFIRMED'
    assert F(interval['upper'])-F(interval['lower']) == F(interval['width']) <= F(1,100)
    assert F(interval['lower']) > 0 and interval['target_met']
    assert len(interval['attempts']) == 1 and interval['selected_cutoff'] == 40
    assert F(interval['width']) == sum((F(v) for v in interval['error_ledger'].values()), F(0))
    tasks = {row['id']: dict(row) for row in arithmetic['tasks']}
    tasks.update({
        'R01': {'id': 'R01', 'status': 'CONFIRMED',
                'conclusion': 'Both byte-preserved supplied programs were executed freshly; the source replay reproduced its stated outputs.',
                'evidence_kind': 'SAME_IMPLEMENTATION_FRESH_REPLAY',
                'evidence': ['evidence/codex_replay/REPLAY.json', 'runs/portable_validation/RUN.json'],
                'independence': 'Replay is not independent mathematical verification.'},
        'B01': {'id': 'B01', 'status': theory['status'],
                'conclusion': 'Exact E5 identification, N=800, sign=-1, additive factors at 2 and 5, and completed Mellin/central derivative normalization checked.',
                'evidence_kind': theory['audit_kind'],
                'evidence': ['ANALYTIC_THEOREMS.md', 'evidence/analytic_theorems.json']},
        'B02': {'id': 'B02', 'status': analytic['B02']['status'],
                'conclusion': 'Independent coefficients and every bound premise give Lprime > '+analytic['B02']['lower_bound']+' > 13/20.',
                'evidence_kind': analytic['B02']['evidence_kind'],
                'evidence': ['evidence/analytic.json', 'INTERVAL_DERIVATION.md', 'ANALYTIC_THEOREMS.md']},
        'D01': {'id': 'D01', 'status': interval['status'],
                'conclusion': interval['lower']+' < c1 < '+interval['upper'],
                'width': interval['width'], 'cutoff': 40, 'panels_per_band': 32,
                'evidence_kind': interval['evidence_kind'],
                'evidence': ['DERIVATIVE_INTERVAL.json', 'INTERVAL_DERIVATION.md', 'work/INTERVAL_BUDGET.json', 'evidence/interval_peer_review.json']},
        'J01': {'id': 'J01', 'status': 'CONFIRMED',
                'conclusion': 'Arithmetic rank=1 independently equals analytic zero order=1 on E5. Sha[2^n]=0 for every n>=1; full BSD coefficient formula remains unestablished here.',
                'evidence_kind': 'WRITTEN_COMBINATION_OF_INDEPENDENT_THEOREM_BASED_RESULTS',
                'evidence': ['ARITHMETIC_PROOF.md', 'ANALYTIC_THEOREMS.md', 'DERIVATIVE_INTERVAL.json', 'RETURN_TO_WILLIAM.md']}
    })
    assert set(tasks) == set(TASK_IDS) and all(r['status'] == 'CONFIRMED' for r in tasks.values())
    for obligation in plan['required_tasks']:
        tasks[obligation['id']]['required_task'] = obligation['task']
    controls = {r['id']: dict(r) for r in arithmetic['controls']+analytic['controls']}
    controls['K02_MODEL_BINDING'] = {'id': 'K02_MODEL_BINDING', 'status': model['status'],
        'outcome': model['mutation']['disposition'], 'evidence': 'evidence/model_binding.json',
        'original': model['baseline']['source_model'], 'changed': model['mutation']['source_model'],
        'polynomial_witness': model['polynomial_witness'], 'claim_ceiling': model['claim_ceiling']}
    assert set(controls) == set(CONTROL_IDS) and all(r['status'] == 'CONFIRMED' for r in controls.values())
    for obligation in plan['required_controls']:
        controls[obligation['id']]['required_control'] = obligation['task']
    input_identity = {'field': 'Q', 'a_invariants': [0,0,0,-25,0],
        'source_records': [identity('supplied/BSD_E5_CODEX_TEST_01/'+rel) for rel in
            ['CODEX_START_HERE.md','TEST_PLAN.json','inputs/descent/E5_DESCENT_NOTE.md',
             'inputs/analytic/ANALYTIC_NOTE.md','inputs/descent/e5_descent.py',
             'inputs/analytic/certify_e5.py']]}
    independent = {'experiment': 'BSD E5 test 01', 'generated_utc': datetime.now(timezone.utc).isoformat(),
        'input_identity': input_identity, 'required_task_ids': TASK_IDS,
        'tasks': [tasks[key] for key in TASK_IDS],
        'execution_receipts': ['evidence/codex_replay/REPLAY.json', 'evidence/arithmetic_execution_final.log',
            'evidence/analytic-command.log', 'evidence/model_binding.log', 'runs/portable_validation/RUN.json'],
        'independence': 'Three actual bounded workers; independent implementations after reading exposed source mathematics. No supplied checker imports or archived result fields in independent computation. Analytic branch has no arithmetic rank input.',
        'optional_backend_status': portable['optional_backend_probe'],
        'formal_proof_status': 'NOT_RUN',
        'implementation_failure_preserved': {'file': 'evidence/arithmetic_fresh.log',
            'disposition': 'Corrected initial SyntaxError; successful fresh execution follows. Not a failed mathematical obligation.'},
        'mathematical_obligations': {'baseline_failed_obligations': [],
            'deliberately_removed_tail_premise': 'OPEN on mutated claim, preserved by K04; complete baseline and interval keep all-term proof.'}}
    write('INDEPENDENT_CHECKS.json', independent)
    write('CONTROLS.json', {'input_identity': input_identity, 'required_control_ids': CONTROL_IDS,
        'controls': [controls[key] for key in CONTROL_IDS],
        'interpretation': 'CONFIRMED means the control behaved as required. False records are rejected, missing proof remains OPEN, and coherent transport passes. No changed-curve rank is inferred.'})
    claims = []
    for task in tasks.values():
        claims.append({'id': task['id'], 'input_identity': input_identity['field']+': [0,0,0,-25,0]',
            'status': task['status'], 'conclusion': task['conclusion'],
            'evidence_kind': task.get('evidence_kind', arithmetic['evidence_kind']),
            'checked_hypotheses': ['Exact E5 model', 'Stated carriers and level/cutoff bounds',
                'Written proof and cited hypotheses at the linked evidence scope'],
            'source': task['evidence']})
    for source in arithmetic['sources']:
        claims.append({'id': 'THEOREM_'+source['id'], 'input_identity': 'Characteristic-zero split cubic with roots 0,5,-5 over Q',
            'status': 'CONFIRMED', 'conclusion': source['id']+' applies at its cited scope.',
            'evidence_kind': 'THEOREM_CITED', 'checked_hypotheses': source['checked_hypotheses'],
            'source': {'url': source['url'], 'locator': source['locator'], 'audit': 'ARITHMETIC_PROOF.md'}})
    for row in theory['claims']:
        claims.append({'id': row['id'], 'input_identity': 'Q: [0,0,0,-25,0]', 'status': row['status'],
            'conclusion': row.get('conclusion', row.get('conclusions')),
            'evidence_kind': row['evidence_kind'], 'checked_hypotheses': row['hypotheses'],
            'source': {'audit': 'ANALYTIC_THEOREMS.md', 'detail': 'evidence/analytic_theorems.json',
                       'references': row.get('sources', row.get('depends_on', []))}})
    for cid in CONTROL_IDS:
        row = controls[cid]
        claims.append({'id': 'CONTROL_'+cid, 'input_identity': row.get('input', row.get('actual_mutation', cid)),
            'status': 'CONFIRMED', 'conclusion': row.get('outcome', row.get('control_outcome')),
            'evidence_kind': 'EXECUTED_FINITE_CONTROL', 'checked_hypotheses': [row['required_control']],
            'source': 'CONTROLS.json'})
    claims += [
        {'id': 'K03_FALSE_COEFFICIENT', 'input_identity': 'evidence/controls/K03_mutated_a9.json',
         'status': 'REFUTED', 'conclusion': 'a9=0 is false; the independently computed recurrence requires a9=-3.',
         'evidence_kind': 'EXACT_WRONG_VALUE_WITNESS', 'checked_hypotheses': ['Good prime 3; a3=0; a9=a3^2-3.'],
         'source': ['CONTROLS.json', 'evidence/analytic.json']},
        {'id': 'K02_CHANGED_MODEL_REUSE', 'input_identity': 'Q: [0,0,0,-36,0]',
         'status': 'REFUTED', 'conclusion': 'Reuse of the exact-model E5 certificate is inapplicable after the real a4 change.',
         'evidence_kind': 'EXACT_MODEL_AND_POLYNOMIAL_MISMATCH', 'checked_hypotheses': ['The certificate requires a4=-25; the pullback difference is 55u.'],
         'source': ['CONTROLS.json', 'evidence/model_binding.json']},
        {'id': 'K06_STALE_READOUT', 'input_identity': 'Transformed five-bit coordinates with the original indicator retained',
         'status': 'REFUTED', 'conclusion': 'The stale indicator misclassifies delta(P); correctly transported indicator remains valid.',
         'evidence_kind': 'EXACT_WRONG_VALUE_WITNESS', 'checked_hypotheses': ['Invertible frame change; original independent arithmetic admissible subset.'],
         'source': ['CONTROLS.json', 'evidence/arithmetic.json']},
        {'id': 'K04_MUTATED_INFINITE_CLAIM', 'input_identity': 'evidence/controls/K04_missing_all_term_premise.json',
         'status': 'CONDITIONAL', 'conclusion': 'OPEN: this finite head alone does not establish an infinite-sum enclosure.',
         'evidence_kind': 'EXPLICIT_MISSING_PROOF_OBLIGATION', 'checked_hypotheses': ['The all-term coefficient premise was actually removed from the interval claim.'],
         'source': ['CONTROLS.json', 'evidence/controls/K04_missing_all_term_premise.json']},
        {'id': 'FRONTIER', 'input_identity': 'E5 only', 'status': 'NOT_RUN',
         'conclusion': 'Full BSD coefficient formula, odd saturation of P, odd-primary Sha and total Sha order remain unestablished in this experiment.',
         'evidence_kind': 'SCOPE_BOUNDARY', 'checked_hypotheses': ['Not inferred from binary quotients or one-curve rank equality.'],
         'source': ['CODEX_START_HERE.md in supplied bundle', 'BSD_REBRIEF.md']}
    ]
    assert all(row['status'] in {'CONFIRMED','REFUTED','CONDITIONAL','NOT_RUN'} for row in claims)
    write('CLAIM_LEDGER.json', {'input_identity': input_identity, 'claims': claims,
        'primary_source_index': theory['sources'], 'evidence_ceiling': 'Theorems cited, written specializations, and finite exact executions are distinct. No new formal proof or general BSD theorem.',
        'inventory_ceiling': 'Hashes identify source bytes; they do not prove the mathematical content.'})
    print(json.dumps({'tasks': len(tasks), 'controls': len(controls), 'claims': len(claims),
                      'status': 'EVIDENCE_INDEX_ASSEMBLED'}))


if __name__ == '__main__':
    main()
