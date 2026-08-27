"""Regression test for the live principal-flip demo endpoint.

Proves entitlement is set-membership (zero LLM) by running the REAL admission
gate, not a hardcoded string. Same span/claim/hash, different principal -> different
actuator. Mirrors examples/knowledge_flip_demo.py.
"""
import pytest
from fastapi.testclient import TestClient

from controlplane.server.app import create_app


@pytest.fixture
def client():
    with TestClient(create_app()) as c:
        yield c


def _decision(client, principal):
    r = client.post("/v1/controlplane/demo/flip", params={"principal": principal})
    assert r.status_code == 200, r.text
    body = r.json()
    actuator = body["decisions"]["show_text"]["actuator"]
    return actuator, body


def test_flip_endpoints_run_real_interlock(client):
    edit_actuator, edit_body = _decision(client, "analyst_01")
    pass_actuator, pass_body = _decision(client, "hr_partner_01")

    # Same claim, same span, same hash — only the caller differs.
    assert edit_body["spans"][0]["content_hash"] == pass_body["spans"][0]["content_hash"]
    assert edit_body["claims"][0]["text"] == pass_body["claims"][0]["text"]

    # Different principal -> different actuator, via the real interlock.
    assert edit_actuator == "Edit"
    assert pass_actuator == "Pass"

    # analyst_01 violated (entitlement), hr_partner_01 not — real finding, not a string match.
    assert edit_body["findings"]["l6_confidential"]["violated"] is True
    assert pass_body["findings"]["l6_confidential"]["violated"] is False

    # No new matrix cell: both route through existing R1 rows.
    assert edit_body["decisions"]["show_text"]["matrix_row"] == "R1"
    assert pass_body["decisions"]["show_text"]["matrix_row"] == "R1"
