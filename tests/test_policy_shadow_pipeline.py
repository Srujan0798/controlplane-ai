from controlplane.pipeline import ControlPlaneGate
from controlplane.policy import PolicyRegistry
from controlplane.shadow import MetricsStore, ShadowCounters
from controlplane.models import Actuator


def test_policy_packs_load_from_dir(tmp_path):
    reg = PolicyRegistry()
    # defaults present
    assert reg.get("decision-support").action("issue_refund").tier.value == "R3"
    # load from repo policies if present
    from pathlib import Path
    root = Path(__file__).resolve().parents[1] / "policies"
    if root.exists():
        reg.load_dir(root)
        assert reg.get("customer-support").mode in {"enforce", "shadow"}


def test_shadow_fnr_shape():
    c = ShadowCounters()
    c.record(use_case="decision-support", actuator=Actuator.ESCALATE, mode="shadow", labeled_should_hold=True)
    c.record(use_case="decision-support", actuator=Actuator.PASS, mode="shadow", labeled_should_hold=True)
    assert c.published_fnr == 0.5
    snap = c.snapshot()
    assert "40ms p50" in snap["fnr_claim_shape"]


def test_gate_refund_enforce_dual_action():
    gate = ControlPlaneGate(metrics=MetricsStore())
    result = gate.run_refund_demo(mode_override="enforce")
    assert result.decisions["show_text"].actuator == Actuator.EDIT
    assert result.decisions["issue_refund"].actuator == Actuator.ESCALATE
    assert result.would_hold is True
    assert result.enforced is True
    assert result.ledger.verify_chain() is True
    assert result.response_overlay["action_allowed"] is False
    pub = result.public_dict()
    assert pub["chain_valid"] is True
    assert result.latency_ms >= 0
