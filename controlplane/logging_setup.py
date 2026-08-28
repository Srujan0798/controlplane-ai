"""Structured JSON request/decision logging for the ControlPlane API.

One JSON object per line. Decision lines carry only gate metadata
(request_id, scenario, actuators, latency_ms) — never claim text, span
content, or message bodies (no PII on the log path).
"""
from __future__ import annotations

import json
import logging
import os
import sys
from typing import Any

LOGGER_NAME = "controlplane"

_configured = False


class JsonFormatter(logging.Formatter):
    """Render each record as one JSON line: ts, level, logger, msg, fields."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        fields = getattr(record, "fields", None)
        if isinstance(fields, dict) and fields:
            payload["fields"] = fields
        return json.dumps(payload, separators=(",", ":"), default=str)


def configure_logging(level: str | None = None) -> logging.Logger:
    """Attach a JSON-line stderr handler to the ``controlplane`` logger.

    Idempotent: safe to call from every ``create_app()`` in tests.
    Level via CONTROLPLANE_LOG_LEVEL (default INFO).
    """
    global _configured
    logger = logging.getLogger(LOGGER_NAME)
    if _configured:
        return logger
    resolved = (level or os.environ.get("CONTROLPLANE_LOG_LEVEL") or "INFO").upper()
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(resolved)
    # Keep lines single-source: no duplicate via root handlers.
    logger.propagate = False
    _configured = True
    return logger


def log_decision(
    logger: logging.Logger,
    public_dict: dict[str, Any],
    *,
    scenario: str | None = None,
) -> None:
    """Emit one ``decision`` line per admitted request.

    Shape: request_id, scenario, mode, latency_ms, actuators, would_hold,
    enforced. Deliberately excludes claim text, span content, and prompt
    bodies.

    ``scenario`` is the operator-facing identifier (URL parameter or
    header) when known; otherwise the policy ``use_case`` is logged.
    """
    decisions = public_dict.get("decisions") or {}
    actuators = {
        action_id: d.get("actuator")
        for action_id, d in decisions.items()
        if isinstance(d, dict)
    }
    logger.info(
        "decision",
        extra={
            "fields": {
                "request_id": public_dict.get("request_id"),
                "scenario": scenario or public_dict.get("use_case"),
                "mode": public_dict.get("mode"),
                "latency_ms": public_dict.get("latency_ms"),
                "actuators": actuators,
                "would_hold": public_dict.get("would_hold"),
                "enforced": public_dict.get("enforced"),
            }
        },
    )
