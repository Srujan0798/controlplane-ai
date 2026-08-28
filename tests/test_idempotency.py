"""Idempotency-Key support for admission endpoints (W7-02).

Same key + same body -> same response (cached). Key reused with a
DIFFERENT body -> 409 conflict (no silent re-commit).
"""
from __future__ import annotations

import json

from fastapi.testclient import TestClient

from controlplane.server.app import create_app

HEADERS = {"Idempotency-Key": "k-1"}
HEADERS_DIFF = {"Idempotency-Key": "k-1"}


def _client():
    return TestClient(create_app(store=None))


def test_same_key_same_body_replays_first_response():
    client = _client()
    r1 = client.post("/v1/controlplane/demo/refund?mode=enforce", headers=HEADERS)
    assert r1.status_code == 200
    r1_json = r1.json()
    r2 = client.post("/v1/controlplane/demo/refund?mode=enforce", headers=HEADERS)
    assert r2.status_code == 200
    # Same request_id -> identical gated result, no double-commit.
    assert r2.json()["request_id"] == r1_json["request_id"]


def test_same_key_different_body_is_409():
    client = _client()
    r1 = client.post("/v1/controlplane/demo/refund?mode=enforce", headers=HEADERS_DIFF)
    assert r1.status_code == 200
    r2 = client.post(
        "/v1/controlplane/demo/support?mode=enforce", headers=HEADERS_DIFF
    )
    assert r2.status_code == 409
    assert "different body" in r2.json()["detail"].lower()


def test_different_keys_both_run():
    client = _client()
    r1 = client.post(
        "/v1/controlplane/demo/refund?mode=enforce",
        headers={"Idempotency-Key": "a"},
    )
    r2 = client.post(
        "/v1/controlplane/demo/refund?mode=enforce",
        headers={"Idempotency-Key": "b"},
    )
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["request_id"] != r2.json()["request_id"]


def test_chat_same_key_same_body_replays():
    client = _client()
    payload = {
        "model": "controlplane-demo",
        "messages": [{"role": "user", "content": "refund my order"}],
    }
    h = {"Idempotency-Key": "chat-k", "X-ControlPlane-Scenario": "refund"}
    r1 = client.post("/v1/chat/completions", json=payload, headers=h)
    assert r1.status_code == 200
    r2 = client.post("/v1/chat/completions", json=payload, headers=h)
    assert r2.status_code == 200
    assert r2.json()["controlplane"]["request_id"] == r1.json()["controlplane"]["request_id"]


def test_no_key_runs_normally():
    client = _client()
    r = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert r.status_code == 200
    assert "idempotent_replay" not in r.json()
