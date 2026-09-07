"""Clean raw synthetic examples; no recorded audio or observer data."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("music_model",HERE/"model.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path);args=parser.parse_args()
    if args.output and not args.output.is_absolute():parser.error("--output must be absolute")
    left=(0,4,7);right=(2,5,9);w=(0,1,0,-1);hostile=(4,0,-2,0,-2,0)
    a=(0,1,3,7);b=(0,1,4,6);events=(1,0,1,0)
    result={"status":"EXPERIMENTAL","schema":"symbolic-music-example/v1", "pitch_class_matching":{"left":left,"right":right,**m.matching(left,right)},
        "multiset_fold":{"value":[0,0,7],"labelled_fiber":m.labelled_fiber((0,0,7))},
        "histogram_counterexample":{"left":a,"right":b,"left_histogram":m.interval_histogram(a),"right_histogram":m.interval_histogram(b),"same_dihedral_orbit":m.multiset(b) in m.orbit(a)},
        "wave":{"samples":w,"negation":m.negate(w),"shift_two":m.shift(w,2),"sum":m.sum_waves(w,m.negate(w))},
        "wave_hostile":{"samples":hostile,"negation":m.negate(hostile),"shifts_equal_to_negation":[k for k in range(len(hostile)) if m.shift(hostile,k)==m.negate(hostile)]},
        "event_model":{"mask":events,"q":6,"cycles":m.event_cycles(events,6),"operation":"(f,h) -> (f+1 mod P,h+event[f] mod q)"}}
    payload=json.dumps(result,indent=2)+"\n"
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(payload,encoding="utf-8")
    print(payload)

if __name__=="__main__":main()
