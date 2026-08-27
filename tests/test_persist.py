from __future__ import annotations

import threading

from fastapi.testclient import TestClient

from controlplane.persist import AuditStore
from controlplane.server.app import create_app


def test_persist_roundtrip(tmp_path):
    store = AuditStore(tmp_path / "controlplane.db")
    payload = {
        "request_id": "req-1",
        "use_case": "decision-support",
        "mode": "enforce",
        "chain_valid": True,
        "decisions": {"show_text": {"actuator": "Edit"}},
    }
    store.save(payload)
    assert store.count() == 1
    assert store.ok() is True
    got = store.get("req-1")
    assert got is not None
    assert got["use_case"] == "decision-support"
    assert got["chain_valid"] is True
    listed = store.list(limit=10, offset=0)
    assert len(listed) == 1
    assert listed[0]["request_id"] == "req-1"
    assert store.get("missing") is None
    store.save({**payload, "request_id": "req-2", "mode": "shadow"})
    assert store.count() == 2
    page = store.list(limit=1, offset=0)
    assert page[0]["request_id"] == "req-2"
    page2 = store.list(limit=1, offset=1)
    assert page2[0]["request_id"] == "req-1"
    store.close()


def test_persist_thread_safe(tmp_path):
    store = AuditStore(tmp_path / "cp.db")

    def worker(i: int) -> None:
        store.save({"request_id": f"r-{i}", "n": i})

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(24)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert store.count() == 24
    assert store.get("r-0")["n"] == 0
    store.close()


def test_server_prefers_sqlite_and_ledger_verify(tmp_path, monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_DB", str(tmp_path / "cp.db"))
    app = create_app()
    client = TestClient(app)

    health = client.get("/healthz").json()
    assert health["ok"] is True
    assert health["db_ok"] is True
    assert health["policies_count"] >= 3
    assert health["lane1"] == "deterministic_only"

    demo = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert demo.status_code == 200
    body = demo.json()
    assert body["decisions"]["show_text"]["actuator"] == "Edit"
    assert body["decisions"]["issue_refund"]["actuator"] == "Escalate"
    assert body["response_overlay"]["action_allowed"] is False
    rid = body["request_id"]

    listed = client.get("/v1/controlplane/requests").json()["requests"]
    assert any(row["request_id"] == rid for row in listed)
    got = client.get(f"/v1/controlplane/requests/{rid}")
    assert got.status_code == 200
    assert got.json()["request_id"] == rid

    ver = client.get(f"/v1/controlplane/ledger/{rid}/verify")
    assert ver.status_code == 200
    assert ver.json() == {"request_id": rid, "chain_valid": True}

    missing = client.get("/v1/controlplane/ledger/no-such-id/verify")
    assert missing.status_code == 404
