from __future__ import annotations

import time

from controlplane.holdback import HoldBackBuffer, admit_for_decisions
from controlplane.models import Actuator, Decision
from controlplane.pipeline import ControlPlaneGate
from controlplane.shadow import MetricsStore


def test_admit_ok_releases_without_sleep():
    buf = HoldBackBuffer(delay_ms=200)
    t0 = time.perf_counter()
    out = buf.admit("hello", True)
    elapsed = time.perf_counter() - t0
    assert elapsed < 0.05
    assert out["released"] is True
    assert out["held"] is False
    assert out["delay_ms"] == 200
    assert buf.intended_release_at is not None
    assert buf.intended_release_at > time.time() - 1


def test_failure_inside_buffer_never_releases():
    buf = HoldBackBuffer(delay_ms=200)
    out = buf.admit("bad token", False)
    assert out["released"] is False
    assert out["held"] is True
    assert out["delay_ms"] == 200


def test_irreversible_actuators_held_even_when_ok():
    for act in ("Edit", "Escalate", "Block"):
        out = HoldBackBuffer().admit("x", True, actuator=act)
        assert out["held"] is True
        assert out["released"] is False
        assert out["actuator"] == act


def test_pass_actuator_releases():
    out = HoldBackBuffer().admit("ok", True, actuator="Pass")
    assert out["released"] is True
    assert out["held"] is False


def test_admit_for_decisions_holds_escalate():
    decisions = {
        "show_text": Decision(
            action_id="show_text",
            actuator=Actuator.EDIT,
            matrix_row="R1",
            matrix_col="unsupported+categorical",
            driving_claim_ids=("c1",),
            packet={},
        ),
        "issue_refund": Decision(
            action_id="issue_refund",
            actuator=Actuator.ESCALATE,
            matrix_row="R3",
            matrix_col="unsupported+categorical",
            driving_claim_ids=("c2",),
            packet={},
        ),
    }
    out = admit_for_decisions("Refund issued.", decisions)
    assert out["held"] is True
    assert out["released"] is False
    assert out["actuator"] == "Escalate"


def test_gate_overlay_includes_holdback():
    gate = ControlPlaneGate(metrics=MetricsStore())
    result = gate.run_refund_demo(mode_override="enforce")
    hb = result.response_overlay["holdback"]
    assert hb["held"] is True
    assert hb["released"] is False
    assert hb["delay_ms"] == 200
    assert hb["actuator"] in {"Edit", "Escalate", "Block"}
    pub = result.public_dict()
    assert pub["response_overlay"]["holdback"]["held"] is True
