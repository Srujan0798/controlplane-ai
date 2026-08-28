"""Security / negative-path checks on the HTTP surface."""
from __future__ import annotations

from fastapi.testclient import TestClient

from controlplane.server.app import create_app


def _client() -> TestClient:
    return TestClient(create_app())


def test_healthz_ok():
    r = _client().get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["service"] == "controlplane"
    assert body["lane1"] == "deterministic_only"


def test_unknown_scenario_is_400():
    r = _client().post("/v1/controlplane/demo/not-a-real-scenario?mode=enforce")
    assert r.status_code == 400
    assert "unknown scenario" in r.json()["detail"].lower()


def test_metrics_reset_works():
    client = _client()
    demo = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert demo.status_code == 200
    before = client.get("/v1/controlplane/metrics").json()
    assert before["total_decisions"] >= 1

    reset = client.post("/v1/controlplane/metrics/reset")
    assert reset.status_code == 200
    assert reset.json()["status"] == "reset"

    after = client.get("/v1/controlplane/metrics").json()
    assert after["total_decisions"] == 0
    assert after["would_have_held"] == 0
    assert after["enforced_holds"] == 0


def test_oversized_json_does_not_500():
    """Round-2 surface has no hard body cap yet; assert no server error on large JSON.

    If a future limit returns 413/400/422, that is also acceptable.
    """
    client = _client()
    huge = {
        "model": "controlplane-demo",
        "messages": [{"role": "user", "content": "x" * 1_500_000}],
        "scenario": "refund",
        "mode": "enforce",
    }
    r = client.post("/v1/chat/completions", json=huge)
    assert r.status_code in {200, 400, 413, 422}
    assert r.status_code != 500


def test_payload_too_large_returns_413():
    """MAX_BODY_SIZE guard (enterprise_guards middleware) must reject oversized bodies."""
    client = _client()
    huge = {
        "model": "controlplane-demo",
        "messages": [{"role": "user", "content": "x" * 1_500_000}],
        "scenario": "refund",
        "mode": "enforce",
    }
    r = client.post("/v1/chat/completions", json=huge)
    assert r.status_code == 413
    assert "payload too large" in r.json()["detail"].lower()
