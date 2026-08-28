"""HTTP guards: API key, per-IP rate limit, security headers, body cap."""
from __future__ import annotations

import hmac
import os
import threading
import time
from collections.abc import Mapping

MAX_BODY_SIZE = 1_000_000

# Console is static HTML with inline CSS/JS plus Google Fonts (Public Sans).
SECURITY_HEADERS: dict[str, str] = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    ),
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "DENY",
}


def configured_api_key() -> str | None:
    key = os.environ.get("CONTROLPLANE_API_KEY")
    if key is None:
        return None
    key = key.strip()
    return key or None


def path_requires_api_key(path: str, method: str = "GET") -> bool:
    """Key (when configured) applies to /v1/*; /healthz and GET / stay open."""
    if path == "/healthz":
        return False
    if path == "/" and method.upper() == "GET":
        return False
    return path.startswith("/v1/")


def presented_api_key(headers: Mapping[str, str]) -> str | None:
    raw = headers.get("x-api-key")
    if raw:
        return raw.strip()
    auth = headers.get("authorization")
    if auth:
        prefix = "bearer "
        if auth.lower().startswith(prefix):
            return auth[len(prefix) :].strip()
    return None


def _keys_match(presented: str, expected: str) -> bool:
    p = presented.encode("utf-8")
    e = expected.encode("utf-8")
    if len(p) != len(e):
        return False
    return hmac.compare_digest(p, e)


def api_key_authorized(
    headers: Mapping[str, str],
    path: str,
    method: str = "GET",
    expected: str | None = None,
) -> bool:
    if expected is None:
        expected = configured_api_key()
    if not expected:
        return True
    if not path_requires_api_key(path, method):
        return True
    presented = presented_api_key(headers)
    if presented is None:
        return False
    return _keys_match(presented, expected)


def client_ip(headers: Mapping[str, str], client_host: str | None = None) -> str:
    forwarded = headers.get("x-forwarded-for")
    if forwarded:
        first = forwarded.split(",")[0].strip()
        if first:
            return first
    return client_host or "unknown"


def rpm_from_env(default: int = 120) -> int:
    raw = os.environ.get("CONTROLPLANE_RPM")
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


class RateLimiter:
    """Sliding 60s window, in-memory, per key (IP). rpm<=0 disables."""

    def __init__(self, rpm: int | None = None) -> None:
        self.rpm = rpm_from_env() if rpm is None else int(rpm)
        self._hits: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def allow(self, ip: str) -> bool:
        if self.rpm <= 0:
            return True
        now = time.monotonic()
        cutoff = now - 60.0
        with self._lock:
            hits = self._hits.setdefault(ip, [])
            hits[:] = [t for t in hits if t > cutoff]
            if len(hits) >= self.rpm:
                return False
            hits.append(now)
            return True


def content_length_ok(headers: Mapping[str, str], max_bytes: int = MAX_BODY_SIZE) -> bool:
    raw = headers.get("content-length")
    if not raw:
        return True
    try:
        return int(raw) <= max_bytes
    except ValueError:
        return True


# Judge runbook ports: console (8787) + Docker (8080).
DEFAULT_CORS_ORIGINS: tuple[str, ...] = (
    "http://127.0.0.1:8787",
    "http://localhost:8787",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
)


def cors_origins_from_env() -> list[str]:
    """CORS allowlist from CONTROLPLANE_CORS_ORIGINS (comma-separated).

    Unset -> judge-port defaults. Set but empty/whitespace -> [] (deny every
    cross-origin request: fail closed, no wildcard).
    """
    raw = os.environ.get("CONTROLPLANE_CORS_ORIGINS")
    if raw is None:
        return list(DEFAULT_CORS_ORIGINS)
    return [o.strip() for o in raw.split(",") if o.strip()]
