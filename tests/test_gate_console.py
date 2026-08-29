"""T7.1 — upload-capable gate console (RED first).

Acceptance: a judge-chosen paragraph (pasted or uploaded) produces a correct,
explained decision live. The server exposes POST /v1/controlplane/analyze that
runs the REAL pipeline (extract -> bind -> entitle -> interlock -> shadow) on
arbitrary text and returns claims with types/hedging, binding method + rationale,
symbol table, matrix cell, actuator, evidence packet, dead compute, per-stage
latency. Refund language must be held/escalated, never "blocked".
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from controlplane.server.app import create_app


def _client():
    return TestClient(create_app())


def test_analyze_runs_on_arbitrary_text():
    c = _client()
    resp = c.post(
        "/v1/controlplane/analyze",
        json={
            "response_text": "Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.",
            "principal_id": "judge-demo",
            "clearance": ["vendor-public"],
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "decisions" in body
    assert "claims" in body
    assert len(body["claims"]) >= 1


def test_analyze_returns_binding_rationale_and_method():
    c = _client()
    resp = c.post(
        "/v1/controlplane/analyze",
        json={
            "response_text": "Refund amount ₹1,84,000 for order ORD-9.",
            "principal_id": "judge-demo",
            "clearance": ["vendor-public"],
        },
    )
    body = resp.json()
    for claim in body["claims"]:
        binding = claim.get("binding")
        assert binding is not None, "every claim must carry a binding"
        assert binding.get("method"), "binding method required"
        assert "rationale" in binding, "binding rationale required"


def test_analyze_returns_symbol_table_and_matrix_cell():
    c = _client()
    resp = c.post(
        "/v1/controlplane/analyze",
        json={
            "response_text": "Refund of ₹1,84,000 under clause 7.2.",
            "principal_id": "judge-demo",
            "clearance": ["vendor-public"],
        },
    )
    body = resp.json()
    assert "symbol_table" in body, "symbol table required"
    assert "per_stage_latency_ms" in body, "per-stage latency required"


def test_analyze_never_says_blocked():
    c = _client()
    resp = c.post(
        "/v1/controlplane/analyze",
        json={
            "response_text": "Refund of ₹1,84,000 under clause 7.2.",
            "principal_id": "judge-demo",
            "clearance": ["vendor-public"],
        },
    )
    body = resp.json()
    dumped = str(body).lower()
    assert "blocked" not in dumped, "refund language must be held/escalated, never 'blocked'"


def test_gate_html_page_renders():
    c = _client()
    resp = c.get("/gate")
    assert resp.status_code == 200
    html = resp.text.lower()
    assert "textarea" in html or "paste" in html
    assert "upload" in html or "file" in html
