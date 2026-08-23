"""Escalate/Block webhook. Failures never raise into the gate."""
from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

ENV_URL = "CONTROLPLANE_WEBHOOK_URL"
TIMEOUT_S = 2.0
_HOLD_ACTUATORS = frozenset({"Escalate", "Block"})


def webhook_url(url: str | None = None) -> str | None:
    if url is not None:
        target = url.strip()
        return target or None
    raw = os.environ.get(ENV_URL)
    if raw is None:
        return None
    target = raw.strip()
    return target or None


def should_notify(decision_public: dict[str, Any]) -> bool:
    """True for enforce-mode public dicts that include Escalate or Block."""
    if (decision_public.get("mode") or "").lower() != "enforce":
        return False
    decisions = decision_public.get("decisions") or {}
    if not isinstance(decisions, dict):
        return False
    for item in decisions.values():
        actuator = item.get("actuator") if isinstance(item, dict) else None
        if actuator in _HOLD_ACTUATORS:
            return True
    return False


def notify_escalate(decision_public: dict[str, Any], url: str | None = None) -> bool:
    """POST *decision_public* JSON to url or CONTROLPLANE_WEBHOOK_URL.

    No-ops when no URL is configured. Swallows all transport errors.
    """
    target = webhook_url(url)
    if not target:
        return False
    try:
        httpx.post(target, json=decision_public, timeout=TIMEOUT_S)
        return True
    except Exception:
        logger.warning("webhook notify_escalate failed", exc_info=True)
        return False
