import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rprm_transport.baselines import dual_domain_candidate_gate
from rprm_transport.observer import (
    EvaluatorTruth,
    assert_policy_blind_to_evaluator,
    build_observer_from_outlet,
)
from rprm_transport.paths import BIN, mf6
from rprm_transport.receiver import ReceiverQuestion, classify_from_candidates, evaluate_threshold


def test_mf6_present():
    assert Path(mf6()).exists()
    assert (BIN / "mf6.exe").exists() or (BIN / "mf6").exists()


def test_plan_manifest_hashes():
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    import hashlib

    for name, expected in manifest["sha256"].items():
        data = (ROOT / name).read_bytes()
        got = hashlib.sha256(data).hexdigest()
        assert got == expected, name


def test_receiver_threshold():
    q = ReceiverQuestion(threshold_c=0.05, t0=10, t1=20)
    assert evaluate_threshold([5, 15, 25], [0.01, 0.06, 0.01], q) is True
    assert evaluate_threshold([5, 15, 25], [0.01, 0.04, 0.01], q) is False


def test_classify_many_and_false_one():
    many = classify_from_candidates({"a": True, "b": False})
    assert many.status.value == "MANY"
    false_one = classify_from_candidates({"a": True}, truth=False)
    assert false_one.status.value == "FALSE_ONE"


def test_policy_blindness():
    obs = build_observer_from_outlet([1.0, 2.0], [0.1, 0.2], t_cutoff=1.5)
    truth = EvaluatorTruth(
        immobile_inventory=[1.0],
        mobile_inventory=[2.0],
        hidden_params={"zeta": 0.01},
        future_outlet=[],
        target_exceeds=True,
    )
    payload = obs.as_policy_input()
    assert_policy_blind_to_evaluator(payload, truth)
    with pytest.raises(AssertionError):
        bad = dict(payload)
        bad["immobile_inventory"] = [1.0]
        assert_policy_blind_to_evaluator(bad, truth)


def test_candidate_gate():
    r = dual_domain_candidate_gate({"x": True, "y": True})
    assert r.answer.status.value == "ONE"
    r2 = dual_domain_candidate_gate({"x": True, "y": False})
    assert r2.answer.status.value == "MANY"
