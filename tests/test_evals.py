"""T3.2 — eval harness tests.

Red/green: these assert the structure the harness MUST emit before `evals/run.py`
exists. Run `pytest tests/test_evals.py` to watch them fail, then implement.

Invariant enforced here: NO single accuracy number anywhere in the report
(ARCHITECTURE §8 / T3.2 contract). Per-route and per-stratum tables only.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from evals.run import build_report, ROOT, _route_for_method


ROUTES = {"numeric", "structural", "textual", "derived", "temporal", "none"}


def _walk(obj, acc):
    """Collect every key path so we can assert no 'accuracy' field exists."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            acc.append(k)
            _walk(v, acc)
    elif isinstance(obj, list):
        for item in obj:
            _walk(item, acc)


def test_report_has_per_route_metrics():
    rep = build_report()
    assert "per_route" in rep
    for route, m in rep["per_route"].items():
        assert route in ROUTES, f"unexpected route {route}"
        # Per-route is a BINDING DISTRIBUTION (never an undefined precision/FPR).
        for stat in ("supported", "unknown", "contradicted", "unsupported", "abstention_rate"):
            assert stat in m, f"{route} missing {stat}"
        assert isinstance(m["abstention_rate"], (int, float))
        assert 0.0 <= m["abstention_rate"] <= 1.0 + 1e-9


def test_no_single_accuracy_number():
    rep = build_report()
    keys: list[str] = []
    _walk(rep, keys)
    banned = {"accuracy", "case_pass_rate", "overall_accuracy"}
    assert not (set(keys) & banned), f"forbidden single-accuracy field present: {set(keys) & banned}"


def test_action_level_fpr_fnr_have_wilson_cis():
    rep = build_report()
    for k in ("ungrounded_fnr_wilson", "passable_fpr_wilson", "hard_negative_hold_wilson"):
        assert k in rep
        triple = rep[k]
        assert len(triple) == 3
        point, lo, hi = triple
        assert 0.0 <= point <= 1.0 + 1e-9


def test_abstention_reported():
    rep = build_report()
    assert "abstention_unknown" in rep
    assert isinstance(rep["abstention_unknown"], int)


def test_threshold_calibration_present():
    rep = build_report()
    assert "threshold_calibration" in rep
    cal = rep["threshold_calibration"]
    assert isinstance(cal, list) and len(cal) > 0
    for row in cal:
        assert "coverage_supported" in row
        assert "abstention_rate" in row


def test_eval_runs_on_real_corpus():
    rep = build_report()
    # The committed corpus has >= 150 labelled cases (T3.1 acceptance).
    assert rep["n_cases"] >= 150
    # last_run.json is written by main(); build_report is a pure compute.
    assert rep["per_stratum"]


def test_last_run_json_emitted_and_readable():
    from evals.run import main

    rc = main()
    assert rc == 0
    path = ROOT / "last_run.json"
    assert path.exists()
    data = json.loads(path.read_text())
    assert "summary" in data
