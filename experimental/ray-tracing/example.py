"""Run a local update and export its raw clean snapshot and cost receipt."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("ray_model",HERE/"model.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path);args=parser.parse_args()
    if args.output and not args.output.is_absolute():parser.error("--output must be absolute")
    before=m.compile_scene(((1,0),(2,0)))
    transition=m.update(before,"TOGGLE",(1,0))
    result={"status":"EXPERIMENTAL","model":"finite-grid-rays/v1","operation":{"tag":"TOGGLE","at":[1,0]},
        "horizontal_ray":{"ray":[0,0],"before":m.first_hit(before["rows"][0]),"after":m.first_hit(transition["snapshot"]["rows"][0])},**transition}
    payload=json.dumps(result,indent=2)+"\n"
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(payload,encoding="utf-8")
    print(payload)

if __name__=="__main__":main()
