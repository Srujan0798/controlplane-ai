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
    summary = data["summary"]
    assert summary.get("published_fnr_source") == "eval-corpus"
    assert summary.get("production_fnr") == "unknown"


def test_hard_negative_share_at_least_20_percent():
    rep = build_report()
    assert rep["n_cases"] >= 150
    share = rep["hard_negative_share"]
    assert share >= 0.20, f"hard-negative share {share:.1%} below 20% floor"
    assert rep["hard_negative_n"] == sum(
        s["hard_negative"] for s in rep["per_stratum"].values()
    )


def test_fnr_has_honest_miss_or_written_bound():
    """Kill fake-perfect FNR=0 with no miss story."""
    rep = build_report()
    fnr = rep["ungrounded_fnr"]
    ci = rep["ungrounded_fnr_wilson"]
    assert len(ci) == 3
    assert ci[1] <= ci[0] <= ci[2]
    assert rep["production_fnr"] == "unknown"
    assert rep["corpus"]["self_authored"] is True
    misses = rep["action_level"]["ungrounded"]["miss_ids"]
    if fnr == 0:
        # Allowed only with an explicit production-unknown bound, never as "perfect".
        assert "production" in rep["note"].lower()
        assert "unknown" in rep["note"].lower()
    else:
        assert misses, "FNR>0 must name the miss case"
        assert "struct-miss-000" in misses


def test_derived_route_not_silent_precision_zero():
    rep = build_report()
    derived = rep["per_route"]["derived"]
    assert derived.get("precision") is None
    assert "note" in derived
    assert "precision" in derived["note"].lower()
    assert "distribution" in derived["note"].lower()
    counted = (
        derived["supported"]
        + derived["contradicted"]
        + derived["unsupported"]
        + derived["unknown"]
    )
    assert derived["n"] == counted


def test_readme_states_honesty_contract():
    text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "self-authored" in text
    assert "production fnr" in text and "unknown" in text
    assert "wilson" in text
    assert "hard negative" in text
    assert "20%" in text or "20 %" in text


def test_metrics_endpoint_source_eval_corpus():
    """GET /v1/controlplane/metrics publishes eval-corpus FNR after last_run exists."""
    from fastapi.testclient import TestClient

    from controlplane.server.app import create_app

    app = create_app()
    c = TestClient(app)
    resp = c.get("/v1/controlplane/metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("published_fnr") is not None
    assert data.get("published_fnr_source") == "eval-corpus"
    assert "published_fnr_ci" in data
    assert data.get("production_fnr") == "unknown"


def test_threshold_calibration_is_a_real_sweep():
    rep = build_report()
    cal = rep["threshold_calibration"]
    assert len(cal) >= 2
    for row in cal:
        assert row["abstention_rate"] is not None
        assert row["supported_count"] is not None
        assert 0.0 <= row["abstention_rate"] <= 1.0 + 1e-9
