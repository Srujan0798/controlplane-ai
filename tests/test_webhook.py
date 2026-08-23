from __future__ import annotations

import httpx

from controlplane.upstream import (
    UpstreamNotConfigured,
    configured,
    forward_chat,
)
from controlplane.webhook import notify_escalate, should_notify


def test_should_notify_enforce_escalate_only():
    escalate = {
        "mode": "enforce",
        "decisions": {
            "show_text": {"actuator": "Edit"},
            "issue_refund": {"actuator": "Escalate"},
        },
    }
    assert should_notify(escalate) is True
    assert should_notify({**escalate, "mode": "shadow"}) is False
    assert should_notify(
        {
            "mode": "enforce",
            "decisions": {"show_text": {"actuator": "Edit"}},
        }
    ) is False
    assert should_notify(
        {
            "mode": "enforce",
            "decisions": {"deny": {"actuator": "Block"}},
        }
    ) is True


def test_notify_noop_without_url(monkeypatch):
    monkeypatch.delenv("CONTROLPLANE_WEBHOOK_URL", raising=False)
    assert notify_escalate({"request_id": "x"}, url=None) is False
    assert notify_escalate({"request_id": "x"}, url="") is False


def test_notify_posts_json_with_two_second_timeout(monkeypatch):
    posts: list[tuple] = []

    class FakeResp:
        status_code = 204

    def fake_post(url, *, json=None, timeout=None, **kwargs):
        posts.append((url, json, timeout))
        return FakeResp()

    monkeypatch.setattr("controlplane.webhook.httpx.post", fake_post)
    payload = {"request_id": "r1", "mode": "enforce"}
    assert notify_escalate(payload, url="https://hooks.example/escalate") is True
    assert posts == [("https://hooks.example/escalate", payload, 2.0)]


def test_notify_uses_env_url(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_WEBHOOK_URL", "https://hooks.example/from-env")
    seen: list[str] = []

    def fake_post(url, *, json=None, timeout=None, **kwargs):
        seen.append(url)

        class R:
            status_code = 200

        return R()

    monkeypatch.setattr("controlplane.webhook.httpx.post", fake_post)
    assert notify_escalate({"ok": True}) is True
    assert seen == ["https://hooks.example/from-env"]


def test_notify_swallows_httpx_errors(monkeypatch):
    def boom(*_a, **_k):
        raise httpx.ConnectError("nope")

    monkeypatch.setattr("controlplane.webhook.httpx.post", boom)
    assert notify_escalate({"x": 1}, url="https://hooks.example/x") is False


def test_forward_chat_raises_if_unset(monkeypatch):
    monkeypatch.delenv("CONTROLPLANE_UPSTREAM_URL", raising=False)
    monkeypatch.delenv("CONTROLPLANE_UPSTREAM_KEY", raising=False)
    assert configured() is False
    try:
        forward_chat([{"role": "user", "content": "hi"}], "gpt-4")
    except UpstreamNotConfigured as exc:
        assert "CONTROLPLANE_UPSTREAM_URL" in str(exc)
    else:
        raise AssertionError("expected UpstreamNotConfigured")


def test_forward_chat_posts_openai_shape(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_UPSTREAM_URL", "https://api.openai.com/v1")
    monkeypatch.setenv("CONTROLPLANE_UPSTREAM_KEY", "sk-x")
    captured: dict = {}

    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return {"id": "chatcmpl-up", "choices": []}

    def fake_post(url, *, json=None, headers=None, timeout=None, **kwargs):
        captured.update(url=url, json=json, headers=headers, timeout=timeout)
        return FakeResp()

    monkeypatch.setattr("controlplane.upstream.httpx.post", fake_post)
    out = forward_chat([{"role": "user", "content": "hi"}], "gpt-4o-mini")
    assert out["id"] == "chatcmpl-up"
    assert captured["url"] == "https://api.openai.com/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer sk-x"
    assert captured["json"] == {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "hi"}],
    }
    assert captured["timeout"] == 30.0
