"""Snapshot earlier written proof dependencies; never computational inputs."""
from pathlib import Path
import hashlib
import json
import shutil

root=Path(__file__).resolve().parents[1]
repo=root.parents[1]
names={
 "ARITHMETIC_PROOF.md":"research/bsd-coefficient-05/dependencies/ARITHMETIC_PROOF.md",
 "GENERATOR_PROOF.md":"research/bsd-identity-01/input_source/GENERATOR_PROOF.md",
 "TRACE_CALCULATION.md":"research/bsd-trace-02/TRACE_CALCULATION.md",
 "PADIC_HEIGHT_AUDIT.md":"research/bsd-coefficient-05/dependencies/PADIC_HEIGHT_AUDIT.md",
 "COEFFICIENT_PROOF.md":"research/bsd-coefficient-05/COEFFICIENT_PROOF.md",
 "EXACT_IDENTITY_THEOREMS.md":"research/bsd-identity-01/EXACT_IDENTITY_THEOREMS.md",
 "EXPLICIT_IDENTITY_TARGET.md":"research/bsd-identity-01/EXPLICIT_IDENTITY_TARGET.md",
}
target=root/"dependencies"
target.mkdir(exist_ok=True)
rows=[]
for name,relative in names.items():
    source=repo/relative; data=source.read_bytes(); dest=target/name
    if dest.exists():
        if dest.read_bytes()!=data: raise ValueError("Changed dependency: "+name)
    else: shutil.copyfile(source,dest)
    rows.append({"snapshot":name,"original_source":str(source),"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)})
report={"scope":"Earlier written proofs, not fresh results and not read by the computation",
        "links":"Relative links within snapshots refer to their original source directories; use original_source to resolve them.",
        "files":rows}
payload=json.dumps(report,indent=2)+"\n"
binding=target/"SOURCES.json"
if binding.exists() and binding.read_text(encoding="utf-8")!=payload: raise ValueError("Changed source bindings")
if not binding.exists(): binding.write_text(payload,encoding="utf-8")
print(json.dumps({"dependency_snapshots":len(rows),"unchanged_bytes":True},indent=2))
