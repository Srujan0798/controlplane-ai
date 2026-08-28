"""Idempotency-Key support for admission endpoints.

Honors the ``Idempotency-Key`` header so retries do not double-commit the
side effects of a demo/chat admission. Responses are cached for a short TTL
(default 300s) keyed by key + canonical body fingerprint.

Deterministic only — no LLM, no network. Thread-safe via a lock.
"""
from __future__ import annotations

import hashlib
import os
import threading
import time
from typing import Any

_DEFAULT_TTL_S = 300


def _ttl_from_env(default: int = _DEFAULT_TTL_S) -> int:
    raw = os.environ.get("CONTROLPLANE_IDEMPOTENCY_TTL_S")
    if not raw or not raw.strip():
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value > 0 else default


def fingerprint(body: Any) -> str:
    """Canonical sha256 of the request's decision inputs.

    For demo calls the body is the (scenario, mode, principal, session_id)
    tuple; for chat calls it is the JSON request body. Stable across retries.
    """
    if isinstance(body, dict):
        canonical = (
            body.get("scenario"),
            body.get("mode"),
            body.get("principal"),
            body.get("session_id"),
            body.get("model"),
            body.get("messages"),
            body.get("use_case"),
        )
    else:
        canonical = body
    blob = repr(canonical).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


class IdempotencyCache:
    """In-memory key+body -> response store with TTL expiry."""

    def __init__(self, ttl_s: int | None = None) -> None:
        self.ttl_s = ttl_s if ttl_s is not None else _ttl_from_env()
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def _key(self, key: str, fp: str) -> str:
        return f"{key}:{fp}"

    def lookup(self, key: str, fp: str) -> Any | None:
        if not key:
            return None
        k = self._key(key, fp)
        with self._lock:
            entry = self._store.get(k)
            if entry is None:
                return None
            stored_at, value = entry
            if time.monotonic() - stored_at > self.ttl_s:
                self._store.pop(k, None)
                return None
            return value

    def store(self, key: str, fp: str, response: Any) -> None:
        if not key:
            return
        k = self._key(key, fp)
        with self._lock:
            self._store[k] = (time.monotonic(), response)

    def conflict(self, key: str, fp: str) -> bool:
        """True if this key is already cached under a DIFFERENT body fingerprint."""
        if not key:
            return False
        prefix = f"{key}:"
        with self._lock:
            for stored in self._store:
                if stored.startswith(prefix) and stored != self._key(key, fp):
                    return True
            return False
