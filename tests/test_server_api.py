from fastapi.testclient import TestClient

from controlplane.server.app import create_app


def test_health_and_refund_demo_and_chat():
    app = create_app()
    client = TestClient(app)

    assert client.get("/healthz").json()["ok"] is True
    assert client.get("/").status_code == 200
    assert "ControlPlane" in client.get("/").text

    demo = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert demo.status_code == 200
    body = demo.json()
    assert body["decisions"]["show_text"]["actuator"] == "Edit"
    assert body["decisions"]["issue_refund"]["actuator"] == "Escalate"
    assert body["response_overlay"]["action_allowed"] is False

    chat = client.post(
        "/v1/chat/completions",
        json={
            "model": "controlplane-demo",
            "messages": [{"role": "user", "content": "Issue refund under clause 7.2"}],
            "scenario": "refund",
            "mode": "enforce",
        },
    )
    assert chat.status_code == 200
    payload = chat.json()
    assert "controlplane" in payload
    assert "HOLD" in payload["choices"][0]["message"]["content"] or (
        payload["controlplane"]["response_overlay"]["action_allowed"] is False
    )

    metrics = client.get("/v1/controlplane/metrics").json()
    assert metrics["total_decisions"] >= 2
    assert client.get("/v1/controlplane/policies").status_code == 200
