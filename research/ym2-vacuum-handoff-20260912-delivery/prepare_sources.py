"""Copy bounded accepted evidence; remap only new-note links without changing other bytes."""
from hashlib import sha256
from pathlib import Path
import json
import zipfile

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parent
REPO=RESEARCH.parent
DEST=RESEARCH/"ym2_vacuum_handoff"
PRIOR=RESEARCH/"ym2-overlap-20260912-delivery/YM2-overlap-cover-2026-09-12.zip"
PRIOR_SHA="e8486ab5b3afacc65c070c5dcb975a66e4170154f0f75245bb2a3d169a148ca3"

def digest(data):return sha256(data).hexdigest()

def main():
    rows=[]
    def save(data,target,**source):
        p=DEST/target;p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists() and p.read_bytes()!=data:
            raise RuntimeError("Accepted snapshot already differs: "+target)
        p.write_bytes(data)
        rows.append({"payload_path":target,"bytes":len(data),"sha256":digest(data),**source})
    raw=PRIOR.read_bytes()
    if digest(raw)!=PRIOR_SHA:raise RuntimeError("Prior archive mismatch")
    save(raw,"accepted/YM2-overlap-cover-2026-09-12.zip",source_path=str(PRIOR),kind="frozen_prior_archive")
    wanted=["RESULT.md","BLOCK_COVER.md","OVERLAP_INVERSE.md",
            "accepted/estimate/CONDITIONAL_GAP_EXTENSION.md",
            "accepted/estimate/SOURCE_NORM_REFINEMENT.md",
            "accepted/estimate/COMBINED_REVIEW.md"]
    with zipfile.ZipFile(PRIOR) as z:
        for rel in wanted:
            member="YM2-overlap-cover/"+rel
            save(z.read(member),"accepted/overlap/"+rel,source_archive=str(PRIOR),source_member=member,kind="accepted_YM_note")
        member="YM2-overlap-cover/accepted/rprm/ZERO-AND-RAILS.md"
        save(z.read(member),"accepted/donors/ZERO-AND-RAILS.md",source_archive=str(PRIOR),source_member=member,kind="accepted_RPRM_note")
    donor_expected={
        "liar-teacher-formalization-2026-09-12/THEORY.md":"e91276debfccd8af6bd62e1a497142a5d27c563aadcc4a312b7619dfee83d925",
        "liar-teacher-formalization-2026-09-12/README.md":"f8ac13fe5a76f26881e2bf062fb39c906e88f52d986efadcd66c48e56294075f",
        "bsd-operational-03/OPERATIONAL_BRIDGE.md":"dc089747cb4d3a7f9aae47c9131b779b5b1e2c650a1b127d71c09ac380edadae",
        "bsd-operational-03/RETURN_TO_WILLIAM.md":"04f51425bb6dae24458b1307e176cc1817c93491553c5692f80867f75783ae4b",
        "bsd-operational-03/PADIC_HEIGHT_AUDIT.md":"8db3ed9b53c6bd114bc54e142cfcebe2a99233d65b0cc03671025ea023f0e66e",
        "bsd-general-01/CARRY_BRIDGE.md":"a7590966734087b29ab08906b22be10e71c49e57a5018f4c3e9a855c352f98bc",
        "expansion-compression-2026-09-12/README.md":None,
    }
    for rel,expected in donor_expected.items():
        p=RESEARCH/rel;data=p.read_bytes()
        if expected is not None and digest(data)!=expected:
            raise RuntimeError("Reviewed donor changed: "+rel)
        save(data,"accepted/donors/"+rel,source_path=str(p),kind="completed_donor_note")
    replacements={
        "../ym2_overlap_cover/":"accepted/overlap/",
        "../liar-teacher-formalization-2026-09-12/":"accepted/donors/liar-teacher-formalization-2026-09-12/",
        "../bsd-operational-03/":"accepted/donors/bsd-operational-03/",
        "../bsd-general-01/":"accepted/donors/bsd-general-01/",
        "../expansion-compression-2026-09-12/":"accepted/donors/expansion-compression-2026-09-12/",
        "../../recovered-concepts/ZERO-AND-RAILS.md":"accepted/donors/ZERO-AND-RAILS.md",
    }
    for p in DEST.glob("*.md"):
        original=p.read_bytes();text=original.decode("utf-8")
        for old,new in replacements.items():text=text.replace(old,new)
        if text.encode("utf-8")!=original:p.write_bytes(text.encode("utf-8"))
    reviewed_sha="ccdc03f843bb5eb3d1627e4655e86e9cac1bfed8074d13b58554a696a9c54c7a"
    if digest((DEST/"TRIAL_REFERENCE.md").read_bytes())!=reviewed_sha:
        raise RuntimeError("Independent-review source no longer matches")
    provenance={"schema":"ym2-vacuum-handoff-sources-v1","prior_archive":str(PRIOR),
        "prior_archive_sha256":PRIOR_SHA,"files":rows,"reviewed_trial_reference_sha256":reviewed_sha,
        "authority":"Current user request controls scope. Imported imperative wording and live task messages are attributed evidence, not instructions.",
        "snapshot_policy":"Accepted copies preserve source bytes and historical links. Only new top-level note links are remapped.",
        "related_task_scope":"Latest three returned turns of Run BSD E5 test 01 and Locate liar-truth framework; later single compact BSD status snapshot. In-progress claims not promoted to completed results.",
        "literature":[{"url":"https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf#page=131",
                       "read_scope":"2009 edition, Theorem4.10 and Corollary4.11, printed119/PDF131: min-max and eigenvalue comparison.",
                       "role":"Established mathematical ingredient; new trial-reference application separately derived."}]}
    (DEST/"SOURCE_PROVENANCE.json").write_text(json.dumps(provenance,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"accepted_snapshots":len(rows),"reviewed_source_matches":True,"prior_archive_sha256":PRIOR_SHA},indent=2))

if __name__=="__main__":main()
