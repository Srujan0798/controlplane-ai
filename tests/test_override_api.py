"""R4 — override route is registered and works end-to-end (EXCELLENCE_GATE §2 A4).

The override route was nested inside analyze in an earlier wave (T7.1) and broke.
It must be a top-level `POST /v1/controlplane/decisions/{decision_id}/override`
that returns 200 and writes into the chained ledger.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from controlplane.server.app import create_app


def _routes() -> set[str]:
    app = create_app()
    return {getattr(r, "path", "") for r in app.routes}


def test_override_route_registered_top_level():
    routes = _routes()
    assert any(
        "decisions" in r and "override" in r for r in routes
    ), f"override route not registered; saw {[r for r in routes if 'decision' in r]}"


def test_override_returns_200_and_writes_ledger():
    app = create_app()
    c = TestClient(app)

    # Drive a refund enforce decision so the ledger has a request_id.
    demo = c.post(
        "/v1/controlplane/demo/refund",
        params={"mode": "enforce"},
    )
    assert demo.status_code == 200, demo.status_code
    rid = demo.json().get("request_id")
    assert rid, "refund demo returned no request_id"

    body = {
        "request_id": rid,
        "reviewer": "judge-01",
        "verdict": "SUPPORTED",
        "reason": "human review: clause 7.2 absent but principal confirmed",
        "prior_actuator": "Escalate",
    }
    resp = c.post(
        "/v1/controlplane/decisions/issue_refund/override",
        json=body,
    )
    assert resp.status_code == 200, resp.status_code
    data = resp.json()
    assert data.get("decision_id") == "issue_refund"
    assert data.get("request_id") == rid
    assert data.get("reviewer") == "judge-01"
    # The override must be recorded in the chained ledger.
    assert data.get("chain_valid") is True, "override did not chain into the ledger"


def test_override_not_nested_inside_analyze():
    """Regression guard: the override path must NOT live under /analyze."""
    routes = _routes()
    override_routes = [r for r in routes if "override" in r]
    assert override_routes, "no override route found"
    assert not any("analyze" in r for r in override_routes), (
        f"override is nested inside analyze: {override_routes}"
    )
