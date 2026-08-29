"""T3.2 — published FNR/FPR wired from eval corpus, not None at startup."""
from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from controlplane.server.app import create_app
from controlplane.shadow import MetricsStore


EVAL_JSON = Path(__file__).resolve().parents[1] / "evals" / "last_run.json"


def test_metricsstore_load_eval_fnr():
    """MetricsStore.load_eval_metrics seeds published_fnr from last_run.json."""
    store = MetricsStore()
    # Before loading: no live labels → published_fnr is None
    assert store.counters.published_fnr is None
    store.load_eval_metrics(EVAL_JSON)
    snap = store.snapshot()
    assert snap["published_fnr"] is not None, "FNR must be seeded from eval corpus"
    assert snap["published_fnr_source"] == "eval-corpus"
    assert snap["published_fnr_n"] > 0


def test_metrics_endpoint_publishes_fnr():
    """GET /v1/controlplane/metrics publishes a non-None published_fnr."""
    app = create_app()
    c = TestClient(app)
    resp = c.get("/v1/controlplane/metrics")
    assert resp.status_code == 200
    data = resp.json()
    fnr = data.get("published_fnr")
    assert fnr is not None, "published_fnr must not be None when eval corpus exists"
    assert "published_fnr_ci" in data
    assert data["published_fnr_source"] == "eval-corpus"


def test_prometheus_publishes_fnr():
    """Prometheus text exposition includes controlplane_published_fnr."""
    store = MetricsStore()
    store.load_eval_metrics(EVAL_JSON)
    prom = store.prometheus_text()
    assert "controlplane_published_fnr" in prom
