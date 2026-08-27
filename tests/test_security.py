from __future__ import annotations

from fastapi.testclient import TestClient

from controlplane.security import (
    MAX_BODY_SIZE,
    SECURITY_HEADERS,
    RateLimiter,
    api_key_authorized,
)
from controlplane.server.app import create_app


def test_max_body_size_constant():
    assert MAX_BODY_SIZE == 1_000_000


def test_security_headers_allow_console_fonts():
    csp = SECURITY_HEADERS["Content-Security-Policy"]
    assert "fonts.googleapis.com" in csp
    assert "fonts.gstatic.com" in csp
    assert SECURITY_HEADERS["X-Content-Type-Options"] == "nosniff"
    assert SECURITY_HEADERS["X-Frame-Options"] == "DENY"
    assert "Referrer-Policy" in SECURITY_HEADERS


def test_api_key_helper_rejects_missing_and_wrong():
    expected = "s3cret"
    headers = {"x-api-key": "s3cret"}
    assert api_key_authorized(headers, "/v1/controlplane/policies", expected=expected)
    assert not api_key_authorized({}, "/v1/controlplane/policies", expected=expected)
    assert not api_key_authorized(
        {"x-api-key": "nope"}, "/v1/controlplane/policies", expected=expected
    )
    assert api_key_authorized({}, "/healthz", expected=expected)
    assert api_key_authorized({}, "/", "GET", expected=expected)


def test_api_key_rejects_401(monkeypatch, tmp_path):
    monkeypatch.setenv("CONTROLPLANE_API_KEY", "s3cret")
    monkeypatch.setenv("CONTROLPLANE_DB", str(tmp_path / "cp.db"))
    client = TestClient(create_app())

    assert client.get("/healthz").status_code == 200
    assert client.get("/").status_code == 200

    denied = client.get("/v1/controlplane/policies")
    assert denied.status_code == 401
    assert denied.json()["detail"] == "unauthorized"

    wrong = client.get("/v1/controlplane/policies", headers={"X-API-Key": "nope"})
    assert wrong.status_code == 401

    ok_header = client.get("/v1/controlplane/policies", headers={"X-API-Key": "s3cret"})
    assert ok_header.status_code == 200

    ok_bearer = client.get(
        "/v1/controlplane/policies",
        headers={"Authorization": "Bearer s3cret"},
    )
    assert ok_bearer.status_code == 200


def test_security_headers_present_on_healthz(tmp_path, monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_DB", str(tmp_path / "cp.db"))
    r = TestClient(create_app()).get("/healthz")
    assert r.status_code == 200
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert "fonts.googleapis.com" in r.headers["Content-Security-Policy"]
    assert r.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"


def test_rate_limit_eventually_429(monkeypatch, tmp_path):
    monkeypatch.setenv("CONTROLPLANE_RPM", "5")
    monkeypatch.setenv("CONTROLPLANE_DB", str(tmp_path / "cp.db"))
    client = TestClient(create_app())
    codes = [client.get("/v1/models").status_code for _ in range(8)]
    assert 200 in codes
    assert 429 in codes
    health = client.get("/healthz")
    assert health.status_code == 200


def test_rate_limiter_unit():
    limiter = RateLimiter(rpm=3)
    assert limiter.allow("1.1.1.1")
    assert limiter.allow("1.1.1.1")
    assert limiter.allow("1.1.1.1")
    assert limiter.allow("1.1.1.1") is False
    assert limiter.allow("8.8.8.8") is True
