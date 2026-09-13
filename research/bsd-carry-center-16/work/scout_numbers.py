"""Fresh narrow number scouts, reusing only an unchanged byte-bound verifier receipt."""
from pathlib import Path
from hashlib import sha256
import subprocess,sys,json,argparse

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
if args.output.exists():raise FileExistsError('Use a new evidence path')
lex=Path('C:/github/RPRMLexicon/operational_numbers')
receipt=Path('C:/github/RPRM-open/research/bsd-sliding-hook-15/evidence/translator-verification.json')
prior=json.loads(receipt.read_text(encoding='utf-8'))
hashes={name:sha256((lex/name).read_bytes()).hexdigest() for name in prior['sha256_after']}
assert hashes==prior['sha256_after'],'Translator changed: obtain fresh verification before reuse'
reports=[]
for word in ('5','9','01','0/1'):
    cmd=[sys.executable,'-B',str(lex/'translate_number.py'),word,'--scout']
    p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
    try:out=json.loads(p.stdout)
    except json.JSONDecodeError:out=p.stdout
    reports.append({'input':word,'command':cmd,'exit_code':p.returncode,'stdout':out,'stderr':p.stderr})
assert hashes=={name:sha256((lex/name).read_bytes()).hexdigest() for name in hashes}
result={'status':'FOUR_NARROW_SCOUTS_RECORDED','prior_receipt':str(receipt),
 'prior_receipt_sha256':sha256(receipt.read_bytes()).hexdigest(),
 'verified_source_hashes':hashes,'reused_verifier_bytes_unchanged':True,
 'scouts':reports,'claim_ceiling':'Scouts enumerate typed possibilities; they do not select user meaning',
 'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'bytes_unchanged':True,
 'inputs_and_exit_codes':[(r['input'],r['exit_code']) for r in reports]},indent=2))
