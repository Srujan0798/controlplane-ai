from __future__ import annotations

from fastapi.testclient import TestClient

from controlplane.server.app import create_app
from controlplane.session import SessionStore


def test_begin_and_parent_chain():
    store = SessionStore()
    begun = store.begin_session("sess-1", "cs-agent-17")
    assert begun["session_id"] == "sess-1"
    assert begun["principal_id"] == "cs-agent-17"
    assert begun["parent_chain"] == []

    first = store.attach_request(
        "sess-1",
        "req-a",
        {"would_hold": False, "actuators": {"show_text": "Pass"}},
    )
    second = store.attach_request(
        "sess-1",
        "req-b",
        {"would_hold": True, "actuators": {"issue_refund": "Escalate"}},
    )
    assert first["parent_request_id"] is None
    assert first["seq"] == 0
    assert second["parent_request_id"] == "req-a"
    assert second["seq"] == 1

    got = store.get("sess-1")
    assert got is not None
    assert got["parent_chain"] == ["req-a", "req-b"]


def test_compounding_risk_flags_prior_escalate():
    store = SessionStore()
    store.begin_session("s", "p")
    store.attach_request(
        "s", "r1", {"would_hold": False, "actuators": {"show_text": "Pass"}}
    )
    risk = store.compounding_risk("s")
    assert risk["compounded"] is False
    assert risk["prior_holds"] == 0
    assert risk["prior_escalations"] == 0
    assert risk["request_count"] == 1

    store.attach_request(
        "s",
        "r2",
        {"would_hold": True, "actuators": {"issue_refund": "Escalate"}},
    )
    risk = store.compounding_risk("s")
    assert risk["prior_holds"] == 1
    assert risk["prior_escalations"] == 1
    assert risk["compounded"] is True


def test_begin_is_idempotent():
    store = SessionStore()
    store.begin_session("s", "alice")
    again = store.begin_session("s", "bob")
    assert again["principal_id"] == "alice"


def test_sqlite_roundtrip(tmp_path):
    path = tmp_path / "controlplane.db"
    store = SessionStore(path)
    store.begin_session("s", "p")
    store.attach_request(
        "s",
        "r1",
        {"would_hold": True, "actuators": {"issue_refund": "Escalate"}},
    )
    store.close()

    restored = SessionStore(path)
    got = restored.get("s")
    assert got is not None
    assert got["principal_id"] == "p"
    assert got["requests"][0]["request_id"] == "r1"
    assert restored.compounding_risk("s")["compounded"] is True
    restored.close()


def test_missing_session_get_is_none():
    store = SessionStore()
    assert store.get("nope") is None
    risk = store.compounding_risk("nope")
    assert risk["compounded"] is False
    assert risk["request_count"] == 0


def test_http_sessions_and_demo_attach(tmp_path, monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_DB", str(tmp_path / "cp.db"))
    client = TestClient(create_app())

    started = client.post(
        "/v1/controlplane/sessions",
        json={"session_id": "judge-1", "principal_id": "cs-agent-17"},
    )
    assert started.status_code == 200
    assert started.json()["session_id"] == "judge-1"

    demo = client.post("/v1/controlplane/demo/refund?mode=enforce&session_id=judge-1")
    assert demo.status_code == 200
    body = demo.json()
    assert body["session_id"] == "judge-1"
    assert body["compounding_risk"]["compounded"] is True
    assert body["response_overlay"]["holdback"]["held"] is True
    rid = body["request_id"]

    demo2 = client.post("/v1/controlplane/demo/refund?mode=enforce&session_id=judge-1")
    assert demo2.status_code == 200
    assert demo2.json()["compounding_risk"]["request_count"] == 2

    got = client.get("/v1/controlplane/sessions/judge-1")
    assert got.status_code == 200
    data = got.json()
    assert len(data["requests"]) == 2
    assert data["requests"][0]["request_id"] == rid
    assert data["requests"][0]["parent_request_id"] is None
    assert data["requests"][1]["parent_request_id"] == rid
    assert data["compounding_risk"]["compounded"] is True
    assert data["compounding_risk"]["prior_escalations"] >= 1

    missing = client.get("/v1/controlplane/sessions/no-such")
    assert missing.status_code == 404
