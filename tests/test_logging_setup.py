"""Structured JSON request logs (W7-03).

Formatter emits one JSON object per line; demo/chat admission endpoints
log a decision record carrying request_id, scenario, actuators, latency_ms.
"""
from __future__ import annotations

import io
import json
import logging

import pytest
from fastapi.testclient import TestClient

from controlplane.logging_setup import (
    LOGGER_NAME,
    JsonFormatter,
    configure_logging,
)
from controlplane.server.app import create_app


def _record(fields: dict) -> logging.LogRecord:
    rec = logging.LogRecord(
        LOGGER_NAME, logging.INFO, __file__, 10, "decision", (), None
    )
    rec.fields = fields
    return rec


def test_formatter_emits_json_with_required_keys():
    line = JsonFormatter().format(
        _record(
            {
                "request_id": "r-1",
                "scenario": "refund",
                "latency_ms": 0.5,
                "actuators": {"show_text": "Edit"},
            }
        )
    )
    payload = json.loads(line)
    assert payload["msg"] == "decision"
    assert payload["level"] == "INFO"
    assert payload["logger"] == LOGGER_NAME
    assert payload["ts"]
    assert payload["fields"]["request_id"] == "r-1"
    assert payload["fields"]["latency_ms"] == 0.5
    assert payload["fields"]["actuators"] == {"show_text": "Edit"}


def test_formatter_plain_record_has_no_fields_key():
    rec = logging.LogRecord(
        LOGGER_NAME, logging.INFO, __file__, 10, "plain", (), None
    )
    payload = json.loads(JsonFormatter().format(rec))
    assert payload["msg"] == "plain"
    assert "fields" not in payload


def test_configure_logging_idempotent():
    logger = configure_logging()
    handlers_before = list(logger.handlers)
    again = configure_logging()
    assert again is logger
    assert logger.handlers == handlers_before


@pytest.fixture
def capture_controlplane_log():
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger(LOGGER_NAME)
    logger.addHandler(handler)
    try:
        yield buf
    finally:
        logger.removeHandler(handler)


def test_demo_endpoint_emits_decision_log_line(capture_controlplane_log):
    client = TestClient(create_app(store=None))
    r = client.post("/v1/controlplane/demo/refund?mode=enforce")
    assert r.status_code == 200
    lines = [
        json.loads(raw)
        for raw in capture_controlplane_log.getvalue().splitlines()
        if raw.strip()
    ]
    decisions = [line for line in lines if line.get("msg") == "decision"]
    assert decisions, "expected a decision log line for the demo admit"
    fields = decisions[-1]["fields"]
    # scenario is the operator-facing URL parameter, not the policy use_case
    assert fields["scenario"] == "refund"
    assert fields["request_id"]
    assert isinstance(fields["latency_ms"], (int, float))
    assert fields["actuators"]["show_text"] == "Edit"
    assert fields["actuators"]["issue_refund"] == "Escalate"
    # No PII sprawl on the log path.
    assert "text" not in fields
    assert "content" not in fields


def test_chat_endpoint_emits_decision_log_line(capture_controlplane_log):
    client = TestClient(create_app(store=None))
    r = client.post(
        "/v1/chat/completions",
        json={
            "model": "controlplane-demo",
            "messages": [{"role": "user", "content": "refund my order"}],
        },
        headers={"X-ControlPlane-Scenario": "refund"},
    )
    assert r.status_code == 200
    lines = [
        json.loads(raw)
        for raw in capture_controlplane_log.getvalue().splitlines()
        if raw.strip()
    ]
    decisions = [line for line in lines if line.get("msg") == "decision"]
    assert decisions, "expected a decision log line for chat completions"
    assert decisions[-1]["fields"]["scenario"] == "refund"
