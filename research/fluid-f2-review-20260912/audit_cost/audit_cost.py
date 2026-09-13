"""Read-only F2 evidence aggregation plus six bounded oracle controls."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / 'input' / 'fluid_dynamic_frontier_02'
sys.path.insert(0, str(SOURCE / 'src'))
from scenes import build_panel, scene_to_oracle_spec
from bound import evaluate_layers, official_static_verdict
from run_f2 import run_oracle

rows = [json.loads(line) for line in (SOURCE/'results/rows.jsonl').read_text().splitlines()]
scenes = build_panel()
totals = {key: sum(r[key] for r in rows) for key in (
    't_prepare_s', 't_graph_s', 'cand_fallback_wall_s', 't_ref_s', 'ref_wall_s',
    'cand_steps', 'ref_steps', 'reach_steps', 'cand_graph_evals',
    'cand_sum_active', 'ref_sum_active')}
totals['candidate_timed_pipeline_s'] = totals['t_prepare_s'] + totals['cand_fallback_wall_s']
totals['candidate_over_reference_timed_pipeline'] = totals['candidate_timed_pipeline_s']/totals['t_ref_s']

identities = collections.defaultdict(list)
for scene in scenes:
    encoded = json.dumps(scene_to_oracle_spec(scene, 'yes_exit'), sort_keys=True).encode()
    identities[hashlib.sha256(encoded).hexdigest()].append(scene['id'])
duplicates = [v for v in identities.values() if len(v)>1]
coverage = {
    'named_scenes': len(scenes), 'unique_simulation_inputs': len(identities),
    'duplicate_groups': duplicates,
    'V180_named_but_not_V180': [{'id':s['id'],'actual_V':s['V']} for s in scenes if 'V180' in s['id'] and s['V']!=180],
    'raw_mass_values': sorted({m for s in scenes for m in s['mass']}),
    'geometry_count': len({(s['W'],s['H'],tuple(s['walls']),tuple(s['monitor'])) for s in scenes}),
}

# Only the five Layer-B-only scenes need extra rollouts to reconstruct the
# panel's dynamic-Layer-A step comparator. All other paths are already recorded.
b_only = [r['id'] for r in rows if r['layer_A']['verdict']=='UNRESOLVED' and r['layer_B']['verdict']=='CERTIFIED_NO']
controls = []
for scene_id in b_only:
    scene = next(s for s in scenes if s['id']==scene_id)
    out = run_oracle(scene, 'cut_exit', BASE)
    controls.append({'id':scene_id, **out})

# Initial fractional mass is normalized to one in model B. The static wrapper
# must either share that admission map or reject such source inputs explicitly.
fractional = copy.deepcopy(next(s for s in scenes if s['id']=='C_right_one'))
fractional['id'] = 'audit_fractional_right_one'
fractional['mass'] = [0.25 if m else 0.0 for m in fractional['mass']]
layers = evaluate_layers(fractional['walls'],fractional['mass'],fractional['monitor'],
                         fractional['W'],fractional['H'],fractional['thresh'],
                         dx=fractional['dx'],crest_y=fractional['crest_y'])
fractional_out = run_oracle(fractional,'yes_exit',BASE)

result = {
    'source':str(SOURCE), 'stored_row_cost_totals':totals, 'coverage':coverage,
    'dynamic_A_B_only_controls':controls,
    'reconstructed_dynamic_A_panel_steps':totals['cand_steps']+sum(c['stepsRun'] for c in controls),
    'normalization_control': {'static':official_static_verdict(layers),'layers':layers,'oracle':fractional_out},
    'scope':'Stored-row aggregation, five dynamic-A controls, and one normalization control; no broad benchmark or input edits.',
}
(BASE/'audit_cost_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('dynamic_A_B_only_controls','normalization_control')},indent=2))
print('B-only dynamic A steps:', [(c['id'],c['stepsRun'],c['stop']) for c in controls])
print('Normalization control:',official_static_verdict(layers),fractional_out['Qdyn'],fractional_out['firstBreach'])
