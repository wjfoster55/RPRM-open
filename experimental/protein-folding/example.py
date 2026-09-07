"""Print the complete small worked example and a contact-map loss witness."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("hp_model", HERE / "model.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and not args.output.is_absolute():
        parser.error("--output must be absolute")
    straight = ((0, 0), (1, 0), (2, 0))
    bent = ((0, 0), (1, 0), (1, 1))
    result = {
        "status": "EXPERIMENTAL_NEWLY_PROPOSED",
        "schema": "hp-square-oriented-example/v1",
        "scope": "2D square-lattice H/P toy; 1..8 residues; no biological prediction",
        "worked_example": {"sequence": "HPPH", "enumerated_paths": 36,
                           **model.minimizers("HPPH")},
        "none_completion": model.completions("HPPH", target_energy=1),
        "one_completion": model.completions("H", target_energy=0),
        "loss_witness": {
            "sequence": "PPP", "straight": straight, "bent": bent,
            "same_contact_map": model.contact_map(straight),
            "same_energy": model.energy("PPP", straight),
            "action": "append W, with a supplied P occurrence",
            "straight_successor": model.extend(straight, "W"),
            "bent_successor": model.extend(bent, "W"),
            "conclusion": "contact map preserves this energy but loses extension enabledness"
        }
    }
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
