from __future__ import annotations

import hashlib
import hmac

from controlplane.signing import DEFAULT_SECRET, sign_bytes, verify


def test_sign_verify_roundtrip(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_AUDIT_SECRET", "unit-secret")
    payload = b'{"type":"chain","payload":{"valid":true}}\n'
    sig = sign_bytes(payload)
    assert len(sig) == 64
    assert all(c in "0123456789abcdef" for c in sig)
    assert verify(payload, sig) is True


def test_verify_rejects_tamper_and_wrong_sig(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_AUDIT_SECRET", "unit-secret")
    payload = b"audit-line\n"
    sig = sign_bytes(payload)
    assert verify(payload + b"x", sig) is False
    assert verify(payload, "0" * 64) is False
    assert verify(payload, "") is False
    assert verify(payload, "short") is False


def test_matches_stdlib_hmac(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_AUDIT_SECRET", "unit-secret")
    payload = b"abc"
    expected = hmac.new(b"unit-secret", payload, hashlib.sha256).hexdigest()
    assert sign_bytes(payload) == expected
    assert verify(payload, expected) is True


def test_default_secret_when_env_unset(monkeypatch):
    monkeypatch.delenv("CONTROLPLANE_AUDIT_SECRET", raising=False)
    payload = b"abc"
    expected = hmac.new(
        DEFAULT_SECRET.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()
    assert sign_bytes(payload) == expected
    assert verify(payload, expected) is True


def test_verify_strips_whitespace(monkeypatch):
    monkeypatch.setenv("CONTROLPLANE_AUDIT_SECRET", "unit-secret")
    payload = b"abc"
    sig = sign_bytes(payload)
    assert verify(payload, f" {sig} \n") is True
