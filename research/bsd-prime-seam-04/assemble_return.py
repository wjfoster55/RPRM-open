"""Assemble a fresh return archive and verify every archived byte.

This delivery utility writes only inside this experiment and to its one
named sibling ZIP. It never replaces an existing archive.
"""
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import zipfile

ROOT=Path(__file__).resolve().parent

def digest(path):return sha256(path.read_bytes()).hexdigest()
def write(path,data):
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def main():
    archive=ROOT.parent/'BSD_PRIME_SEAM_04_RETURN.zip'
    if archive.exists():raise FileExistsError('Return archive already exists')
    dependency_paths={
        'TRACE_FORMULA_AUDIT.md':ROOT.parent/'bsd-trace-02/TRACE_FORMULA_AUDIT.md',
        'PADIC_HEIGHT_AUDIT.md':ROOT.parent/'bsd-operational-03/PADIC_HEIGHT_AUDIT.md',
        'FACTOR_COMPARISON.md':ROOT.parent/'bsd-identity-01/input_source/FACTOR_COMPARISON.md'}
    dependency_records=[]
    for name,source in dependency_paths.items():
        copy=ROOT/'dependencies'/name
        assert copy.read_bytes()==source.read_bytes()
        dependency_records.append({'original':str(source.resolve()),'copy':'dependencies/'+name,
            'sha256':digest(copy),'role':'ADMITTED_PRIOR_WRITTEN_PROOF_NOT_FRESHLY_REPLAYED'})
    write(ROOT/'dependencies/SOURCES.json',dependency_records)
    source_paths=[
        'C:/github/RPRM-foam-development/research/RPRM_OPERATIONAL_LAYER_FOUNDATION_AND_PRIME_PROGRAM_2026-08-28.md',
        'C:/github/RPRM-open/recovered-concepts/PRESTIGE-AND-NUMBER-OPERATIONS.md',
        'C:/github/RPRM-foam-development/experiments/RPRM_RELATION_RESIDUAL_LENS_LOCK_CUT_ROTATION_AUDIT_105/REPORT.md',
        'C:/github/RPRM-foam-development/knowledge/lenses.json',
        'C:/github/RPRM-foam-development/experiments/RPRM_PRIME_ATLAS_FILTER_SHADOW_EXTENSION_AUDIT_103/REPORT.md',
        'C:/github/RPRMLexicon/operational_numbers/README.md',
        'C:/github/RPRMLexicon/operational_numbers/translate_number.py',
        'C:/github/RPRMLexicon/operational_numbers/carrier_lexer.py',
        'C:/github/RPRMLexicon/operational_numbers/verify.py',
        'C:/github/RPRMLexicon/operational_numbers/readings.json']
    write(ROOT/'evidence/source_hashes.json',{
        'scope':'READ_ONLY_ATTRIBUTED_SOURCES; hashes bind bytes, not contents',
        'sources':[{'path':p,'sha256':digest(Path(p)),'bytes':Path(p).stat().st_size} for p in source_paths],
        'primary_web_sources':[
            {'url':'https://kurihara.math.keio.ac.jp/bks4.pdf',
             'used':'§6.1 interpolation and unit-root convention; Proposition6.1; Theorem6.2; Corollary6.7'},
            {'url':'https://www.tandfonline.com/doi/abs/10.1080/19300980.1956.12467445',
             'used':'bibliographic record for the1956 lucky-sieve paper'}]})
    # Proofs and code are archived as supplied; no prose or formula rewriting.
    final=ROOT/'runs/final_validation'
    run=json.loads((final/'RUN.json').read_text())
    assert run['status']=='ALL_THREE_NEW_CALCULATIONS_VERIFIED'
    for file in (ROOT/'work').glob('*.py'):
        assert (final/'work'/file.name).read_bytes()==file.read_bytes()
    for name,h in run['evidence_sha256'].items():assert digest(final/'evidence'/name)==h
    readback=json.loads((final/'evidence/seam_readback.json').read_text())
    assert readback['status']=='PASS' and len(readback['checks'])==166
    assert not readback['failed_checks'] and not readback['errors']
    # Only actual mathematics from the fresh run is used for these summaries.
    primary=json.loads((final/'evidence/prime_seam.json').read_text())
    assert len(primary['joint_valuation_shadows'])==78
    assert all(row['joint_inverse']==[row['alpha_minus_one_v5'],row['beta_minus_one_v5']]
               for row in primary['joint_valuation_shadows'])
    manifest_path=ROOT/'MANIFEST.json'
    files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and p!=manifest_path]
    assert not any('__pycache__' in p.parts for p in files)
    manifest={'created_utc':datetime.now(timezone.utc).isoformat(),
              'claim_ceiling':'EXACT_LOCAL_IDENTITIES_AND_FINITE_SCOUT; GLOBAL_BSD_OPEN',
              'final_run':'runs/final_validation/RUN.json',
              'files':{p.relative_to(ROOT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in files}}
    write(manifest_path,manifest);files.append(manifest_path)
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for file in files:z.write(file,ROOT.name+'/'+file.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.infolist())==len(files)
        for file in files:
            assert z.read(ROOT.name+'/'+file.relative_to(ROOT).as_posix())==file.read_bytes()
    print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,
                      'sha256':digest(archive),'file_count':len(files),
                      'verified':'CRC, every archived byte, final source snapshot and evidence hashes'},indent=2))

if __name__=='__main__':main()
