"""Optional OpenAI-compatible chat passthrough (not the Lane-1 demo path)."""
from __future__ import annotations

import os
from typing import Any

import httpx

ENV_URL = "CONTROLPLANE_UPSTREAM_URL"
ENV_KEY = "CONTROLPLANE_UPSTREAM_KEY"
TIMEOUT_S = 30.0


class UpstreamNotConfigured(RuntimeError):
    """CONTROLPLANE_UPSTREAM_URL is missing; passthrough cannot run."""


class UpstreamError(RuntimeError):
    """Transport or HTTP failure talking to the upstream provider."""


def configured() -> bool:
    raw = os.environ.get(ENV_URL)
    return bool(raw and raw.strip())


def _endpoint(base: str) -> str:
    trimmed = base.strip().rstrip("/")
    if trimmed.endswith("/chat/completions"):
        return trimmed
    return f"{trimmed}/chat/completions"


def _message_dicts(messages: list[Any]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for m in messages:
        if isinstance(m, dict):
            out.append(
                {
                    "role": str(m.get("role", "")),
                    "content": str(m.get("content", "")),
                }
            )
        else:
            out.append(
                {
                    "role": str(getattr(m, "role", "")),
                    "content": str(getattr(m, "content", "")),
                }
            )
    return out


def forward_chat(messages: list[Any], model: str) -> dict[str, Any]:
    """POST /chat/completions to CONTROLPLANE_UPSTREAM_URL.

    Raises UpstreamNotConfigured when the env URL is unset.
    """
    raw = os.environ.get(ENV_URL)
    if not raw or not raw.strip():
        raise UpstreamNotConfigured(
            "CONTROLPLANE_UPSTREAM_URL is not set. "
            "Set it to an OpenAI-compatible base "
            "(e.g. https://api.openai.com/v1) to enable passthrough. "
            "Lane-1 demo fixtures do not need this."
        )
    headers = {"Content-Type": "application/json"}
    key = os.environ.get(ENV_KEY)
    if key and key.strip():
        headers["Authorization"] = f"Bearer {key.strip()}"
    payload = {"model": model, "messages": _message_dicts(messages)}
    try:
        response = httpx.post(
            _endpoint(raw),
            json=payload,
            headers=headers,
            timeout=TIMEOUT_S,
        )
        response.raise_for_status()
        data = response.json()
    except UpstreamNotConfigured:
        raise
    except Exception as exc:
        raise UpstreamError(f"upstream request failed: {exc}") from exc
    if not isinstance(data, dict):
        return {"upstream_response": data}
    return data
