"""HMAC-SHA256 signatures over audit JSONL bytes."""
from __future__ import annotations

import hashlib
import hmac
import os

DEFAULT_SECRET = "dev-only-change-me"
ENV_SECRET = "CONTROLPLANE_AUDIT_SECRET"


def audit_secret() -> bytes:
    raw = os.environ.get(ENV_SECRET, DEFAULT_SECRET)
    if raw is None or raw == "":
        raw = DEFAULT_SECRET
    return raw.encode("utf-8")


def sign_bytes(payload: bytes) -> str:
    """Return hex HMAC-SHA256 of *payload* using CONTROLPLANE_AUDIT_SECRET."""
    return hmac.new(audit_secret(), payload, hashlib.sha256).hexdigest()


def verify(payload: bytes, sig: str) -> bool:
    """Constant-time check that *sig* is the HMAC of *payload*."""
    if not isinstance(sig, str) or not sig.strip():
        return False
    expected = sign_bytes(payload).encode("utf-8")
    presented = sig.strip().encode("utf-8")
    if len(expected) != len(presented):
        return False
    return hmac.compare_digest(expected, presented)
