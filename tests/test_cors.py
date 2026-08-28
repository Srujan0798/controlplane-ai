"""CORS allowlist from CONTROLPLANE_CORS_ORIGINS (W7-01).

Fail closed: unset -> judge-port defaults; empty -> no cross-origin allowed.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from controlplane.security import cors_origins_from_env
from controlplane.server.app import create_app

ALLOWED = "http://127.0.0.1:8787"
DENIED = "https://attacker.example"


def test_defaults_cover_judge_ports(monkeypatch):
    monkeypatch.delenv("CONTROLPLANE_CORS_ORIGINS", raising=False)
    origins = cors_origins_from_env()
    assert "http://127.0.0.1:8787" in origins
    assert "http://localhost:8080" in origins


def test_empty_env_denies_every_origin(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_CORS_ORIGINS", "")
    assert cors_origins_from_env() == []


def test_allowed_origin_preflight_returns_allow_header(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_CORS_ORIGINS", ALLOWED)
    client = TestClient(create_app(store=None))
    r = client.options(
        "/v1/controlplane/metrics",
        headers={
            "Origin": ALLOWED,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert r.status_code in (200, 204)
    assert r.headers.get("access-control-allow-origin") == ALLOWED


def test_disallowed_origin_gets_no_allow_header(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_CORS_ORIGINS", ALLOWED)
    client = TestClient(create_app(store=None))
    r = client.options(
        "/v1/controlplane/metrics",
        headers={
            "Origin": DENIED,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert r.headers.get("access-control-allow-origin") != DENIED
    r = client.post(
        "/v1/controlplane/demo/refund?mode=enforce",
        headers={"Origin": DENIED},
    )
    assert r.status_code == 200
    assert "access-control-allow-origin" not in {
        k.lower() for k in r.headers.keys()
    }
