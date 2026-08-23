"""Same refund fixture must yield the same actuators across runs."""
from __future__ import annotations

from fastapi.testclient import TestClient

from controlplane.server.app import create_app


def test_refund_enforce_actuators_stable_across_five_runs():
    client = TestClient(create_app())
    actuators = []
    for _ in range(5):
        r = client.post("/v1/controlplane/demo/refund?mode=enforce")
        assert r.status_code == 200
        body = r.json()
        decisions = body["decisions"]
        actuators.append(
            {
                aid: {
                    "actuator": d["actuator"],
                    "matrix_row": d["matrix_row"],
                    "matrix_col": d["matrix_col"],
                }
                for aid, d in decisions.items()
            }
        )

    first = actuators[0]
    assert first["show_text"]["actuator"] == "Edit"
    assert first["issue_refund"]["actuator"] == "Escalate"
    for run in actuators[1:]:
        assert run == first
