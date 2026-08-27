from fastapi.testclient import TestClient

from controlplane.server.app import create_app
from controlplane.signing import sign_bytes, verify


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
    assert payload["controlplane"].get("upstream") is not True
    assert "HOLD" in payload["choices"][0]["message"]["content"] or (
        payload["controlplane"]["response_overlay"]["action_allowed"] is False
    )
    assert payload["controlplane"]["decisions"]["show_text"]["actuator"] == "Edit"
    assert payload["controlplane"]["decisions"]["issue_refund"]["actuator"] == "Escalate"

    metrics = client.get("/v1/controlplane/metrics").json()
    assert metrics["total_decisions"] >= 2
    assert client.get("/v1/controlplane/policies").status_code == 200


def test_signed_audit_export_and_verify():
    client = TestClient(create_app())
    demo = client.post("/v1/controlplane/demo/refund?mode=enforce")
    rid = demo.json()["request_id"]

    export = client.get(f"/v1/controlplane/requests/{rid}/audit.jsonl")
    assert export.status_code == 200
    body = export.content
    header_sig = export.headers["X-ControlPlane-Signature"]
    assert verify(body, header_sig) is True
    assert header_sig == sign_bytes(body)

    sig_resp = client.get(f"/v1/controlplane/requests/{rid}/audit.jsonl.sig")
    assert sig_resp.status_code == 200
    assert sig_resp.text.strip() == header_sig

    ok = client.post(
        "/v1/controlplane/audit/verify",
        json={"content": body.decode("utf-8"), "signature": header_sig},
    )
    assert ok.status_code == 200
    assert ok.json() == {"valid": True}

    bad = client.post(
        "/v1/controlplane/audit/verify",
        json={"content": body.decode("utf-8") + "tamper", "signature": header_sig},
    )
    assert bad.json() == {"valid": False}


def test_chat_upstream_passthrough_is_honest(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_UPSTREAM_URL", "https://api.openai.com/v1")
    monkeypatch.setenv("CONTROLPLANE_UPSTREAM_KEY", "sk-test")

    def fake_forward(messages, model):
        assert model == "gpt-4o-mini"
        assert messages[0]["content"] == "hello there"
        return {
            "id": "chatcmpl-up",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "from upstream"},
                    "finish_reason": "stop",
                }
            ],
        }

    monkeypatch.setattr("controlplane.upstream.forward_chat", fake_forward)
    client = TestClient(create_app())
    chat = client.post(
        "/v1/chat/completions",
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "hello there"}],
        },
    )
    assert chat.status_code == 200
    payload = chat.json()
    assert payload["choices"][0]["message"]["content"] == "from upstream"
    ext = payload["controlplane"]
    assert ext["upstream"] is True
    assert ext["demo_fixtures_used"] is False
    assert "not used" in ext["note"].lower()
    assert "decisions" not in ext


def test_chat_scenario_wins_over_upstream(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_UPSTREAM_URL", "https://api.openai.com/v1")

    def boom(*_a, **_k):
        raise AssertionError("scenario path must not call upstream")

    monkeypatch.setattr("controlplane.upstream.forward_chat", boom)
    client = TestClient(create_app())
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
    pub = chat.json()["controlplane"]
    assert pub.get("upstream") is not True
    assert pub["decisions"]["show_text"]["actuator"] == "Edit"
    assert pub["decisions"]["issue_refund"]["actuator"] == "Escalate"


def test_chat_without_scenario_or_upstream_is_400():
    client = TestClient(create_app())
    r = client.post(
        "/v1/chat/completions",
        json={
            "model": "controlplane-demo",
            "messages": [{"role": "user", "content": "hello there"}],
        },
    )
    assert r.status_code == 400
    assert "No scenario resolved" in r.json()["detail"]


def test_refund_enforce_posts_webhook(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_WEBHOOK_URL", "https://hooks.test/escalate")
    posts: list[dict] = []

    def fake_post(url, *, json=None, timeout=None, **kwargs):
        posts.append(json)

        class R:
            status_code = 200

        return R()

    monkeypatch.setattr("controlplane.webhook.httpx.post", fake_post)
    client = TestClient(create_app())
    demo = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert demo.status_code == 200
    assert posts
    assert posts[0]["decisions"]["issue_refund"]["actuator"] == "Escalate"

    posts.clear()
    shadow = client.post("/v1/controlplane/demo/refund?mode=shadow")
    assert shadow.status_code == 200
    assert posts == []
