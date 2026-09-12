#!/usr/bin/env python3
"""Independent, bounded RCF01-R1 API review; not a historical donor replay.
Usage: python -B independent_review.py --package PATH --output-dir FRESH_DIR
Source package is read-only; generated cold artifacts live in output-dir.
"""
from __future__ import annotations
import argparse, hashlib, importlib, json, random, sys
from fractions import Fraction
from pathlib import Path

def plain(x):
    if isinstance(x, Fraction): return str(x)
    if isinstance(x, Path): return str(x)
    if isinstance(x, (set, frozenset)): return [plain(v) for v in sorted(x, key=repr)]
    if isinstance(x, (tuple, list)): return [plain(v) for v in x]
    if isinstance(x, dict): return {str(k): plain(v) for k,v in x.items()}
    return x

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--package', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    a=ap.parse_args(); root=a.package.resolve(); out=a.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False); cold=out/'cold'; cold.mkdir()
    sys.path.insert(0,str(root/'experiments/core_recovery_bridge_01_r1'))
    e=importlib.import_module('prestige_envelope')
    report={'scope':'Reviewer-created exposed development checks, not a full-program proof',
            'python':sys.version,'package':str(root),
            'source_sha256':hashlib.sha256(Path(e.__file__).read_bytes()).hexdigest(), 'checks':{}}
    C=report['checks']
    counter=0
    def make(tab, family='rational_cube', contract=None, backed=True):
        nonlocal counter
        counter+=1
        return e.promote_cube(tab,label='one',contract=e.FULL_CUBE_CONTRACT if contract is None else contract,
                              cold_dir=cold if backed else None,name=f's{counter}',family=family)
    def result(r):
        return {'disposition':r.disposition,'status':r.status,'witness':r.witness}
    def expect_hot(env, table):
        r=e.read_admitted(env)
        assert r.status=='EXACT' and tuple(r.value)==tuple(table[:7])
    # Positive chain through production public API, with independent table oracle.
    h=make(tuple(s&1 for s in range(8)))
    x=make(tuple((s>>1)&1 for s in range(8)))
    y=make(tuple((s>>2)&1 for s in range(8)))
    before=e.meter_snapshot()
    hx=e.multiply_units(h,x).value; p=e.multiply_units(hx,y).value
    after=e.meter_snapshot()
    assert p.retained==(Fraction(0),)*7
    assert after['cold_reads']==before['cold_reads']
    assert p.recipe is not None
    f=e.apply_input_map(p,'flip_h')
    assert f.status=='EXACT'
    expect_hot(f.value, tuple(1 if s==6 else 0 for s in range(8)))
    assert e.inspect_omitted(f.value).value==0
    C['composition_positive']={'status':'PASS','hot_reads_delta':after['cold_reads']-before['cold_reads'],
        'recipe_constructions_delta':after['constructions']-before['constructions'],
        'product_degree_bounds':[h.degree_bound,hx.degree_bound,p.degree_bound],
        'flipped_B2':e.read_admitted(f.value).value}
    # No invalid table can be invented when dependency is deleted.
    leaf=Path(h.cold_route); orig=leaf.read_bytes();leaf.write_bytes(orig+b'corrupt')
    bad=e.apply_input_map(p,'flip_h');assert bad.status=='INVALID_DEPENDENCY' and bad.value is None
    leaf.write_bytes(orig);leaf.unlink()
    missing=e.apply_input_map(p,'flip_h');assert missing.status=='UNRESOLVED' and missing.value is None
    leaf.write_bytes(orig)
    C['composed_dependency_mutations']={'status':'PASS','corrupted':result(bad),'deleted':result(missing)}
    # Various composition / input-map sequences. Oracle is direct table arithmetic,
    # not the implementation's coefficient multiplication / pullback routine.
    rng=random.Random(6112026); nodes=[]
    for _ in range(12):
        tab=tuple(Fraction(rng.randint(-5,5),rng.randint(1,5)) for _ in range(8))
        nodes.append((make(tab),tab))
    reads=0
    for i in range(96):
        if i%3:
            aa,ta=rng.choice(nodes);bb,tb=rng.choice(nodes)
            op=e.add_units if i%2 else e.multiply_units
            r=op(aa,bb); assert r.status=='EXACT'
            table=tuple(u+v if i%2 else u*v for u,v in zip(ta,tb))
        else:
            aa,ta=rng.choice(nodes)
            name=rng.choice(list(e.input_maps()))
            if name=='identity':name='clamp_h_0' # identity is not in FULL_CUBE_CONTRACT
            bit={'h':0,'x':1,'y':2}[name.split('_')[1]]
            mapping=[s^(1<<bit) if name.startswith('flip') else
                     (s | (1<<bit)) if name.endswith('_1') else (s & ~(1<<bit)) for s in range(8)]
            r=e.apply_input_map(aa,name); assert r.status=='EXACT'
            table=tuple(ta[s] for s in mapping)
        expect_hot(r.value,table)
        omitted=e.inspect_omitted(r.value)
        assert omitted.status=='EXACT' and omitted.value==table[7]
        reads+=8;nodes.append((r.value,table))
    C['rational_composition_oracle']={'status':'PASS','seed':6112026,'constructed_steps':96,
        'value_comparisons':reads,'reference':'direct Fraction table arithmetic, direct input indexing'}
    # Actual public-API family counterexample: omitted position is 2 under addition.
    hs=e.unit('h',family='boolean_cube',contract=e.FULL_CUBE_CONTRACT,cold_dir=cold,name='bool_h')
    xs=e.unit('x',family='boolean_cube',contract=e.FULL_CUBE_CONTRACT,cold_dir=cold,name='bool_x')
    ys=e.unit('y',family='boolean_cube',contract=e.FULL_CUBE_CONTRACT,cold_dir=cold,name='bool_y')
    spike=e.multiply_units(e.multiply_units(hs,xs).value,ys).value
    doubled=e.add_units(spike,spike)
    actual_omitted=e.inspect_omitted(doubled.value)
    flipped=e.apply_input_map(doubled.value,'flip_h')
    bool_fiber=e.boolean_fiber_for_compact(doubled.value.retained)
    C['hidden_boolean_addition_class_escape']={
        'status':'DEFECT_REPRODUCED' if doubled.value.family=='boolean_cube' and actual_omitted.value==2 else 'NOT_REPRODUCED',
        'input':'p=multiply(multiply(boolean unit h, boolean unit x), boolean unit y); add(p,p)',
        'retained':doubled.value.retained,'declared_family':doubled.value.family,
        'actual_omitted':actual_omitted.value,'expected_family':'rational_cube',
        'after_flip_family':flipped.value.family,'after_flip_readout_011':e.read_admitted(flipped.value).value[6],
        'boolean_helper_claim':{'disposition':bool_fiber.disposition,'members':bool_fiber.members},
        'significance':'numeric summary is correct, but advertised full-output family excludes its actual output'}
    # The raw mapping helper is reachable and bypasses the named operation gate.
    arith=make(tuple(range(8)),contract=e.ARITH_CONTRACT)
    named=e.apply_input_map(arith,'flip_h')
    generic=e.apply_fixed_receiver_map(arith,e.input_maps()['flip_h'])
    C['generic_map_contract_gate']={'status':'INTERFACE_GAP_REPRODUCED' if named.status=='UNSUPPORTED' and generic.status=='EXACT' else 'NOT_REPRODUCED',
        'named':result(named),'generic':result(generic),'map':'flip_h',
        'boundary':'No mathematical wrong answer; helper needs an explicit unchecked-reference or admitted-public role'}
    # Generic, non-coordinate maps can increase degree even when B2 is closed.
    mapping=tuple(1 if s in (3,7) else 0 for s in range(8))
    rh=e.apply_fixed_receiver_map(h,mapping)
    expect_hot(rh.value,tuple(1 if s in (3,7) else 0 for s in range(8)))
    C['generic_map_degree_bound']={'status':'DEFECT_REPRODUCED' if rh.value.degree_bound<2 else 'NOT_REPRODUCED',
        'mapping':mapping,'input_degree':h.degree_bound,'advertised_output_bound':rh.value.degree_bound,
        'actual_output':'hx','actual_degree':2,
        'boundary':'This map is not a coordinate flip/clamp; generic helper permits it and advertises degree_bound=1'}
    # Coherent transport needs only hot data: correctly returns it without backing,
    # but the backed branch spends an avoidable cold read.
    env=make(tuple(range(8))); e.reset_meter()
    tr=e.coherent_transport(env,e.input_maps()['flip_h']);m=e.meter_snapshot()
    C['coherent_transport_cost']={'status':'OBSERVATION','result':result(tr),
        'cold_reads':m['cold_reads'],'correct_values':tr.value,
        'note':'Correct, but reopens available backing before checking that the transported receiver is already hot-sufficient; not a speed improvement claim.'}
    manifest=json.loads((root/'MANIFEST.json').read_text())
    hashes=[]
    for path,pin in manifest['files'].items():
        data=(root/path).read_bytes();hashes.append({'path':path,'ok':len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256']})
    C['manifest']={'status':'PASS' if all(v['ok'] for v in hashes) else 'FAIL','listed':len(hashes),'checks':hashes}
    dest=out/'independent_review.json';dest.write_text(json.dumps(plain(report),indent=2)+'\n')
    print(json.dumps({k:{q:v[q] for q in ['status'] if q in v} for k,v in C.items()},indent=2))
    print(dest)
    return 0
if __name__=='__main__':raise SystemExit(main())
