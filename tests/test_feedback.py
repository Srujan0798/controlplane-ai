from controlplane.feedback import FeedbackStore
from controlplane.models import Principal
from controlplane.recorder import ProvenanceRecorder


def test_override_writes_to_chained_ledger():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "ov-1",
        Principal(id="r", clearance=frozenset({"public"})),
        "show",
    )
    rec.finish_context_assembly(led)
    store = FeedbackStore()
    store.record_override(
        led,
        decision_id="issue_refund",
        reviewer="alice",
        verdict="UNSUPPORTED",
        reason="clause absent — keep escalate",
        prior_actuator="Escalate",
    )
    assert len(led.get("override")) >= 1
    assert len(store.overrides) == 1
    assert led.verify_chain() is True


def test_threshold_proposal_prints_shadow_delta():
    store = FeedbackStore()
    prop = store.propose_threshold(
        name="bm25_coverage_supported",
        current=0.72,
        proposed=0.68,
        shadow_fp_delta=0.01,
        shadow_fn_delta=-0.02,
    )
    assert prop["shadow_fp_delta"] == 0.01
    assert prop["shadow_fn_delta"] == -0.02
    assert "shadow" in prop["note"].lower()


def test_canary_rollback_on_override_spike():
    store = FeedbackStore(baseline_override_rate=0.02, canary_multiplier=3.0)
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "ov-spike",
        Principal(id="r", clearance=frozenset({"public"})),
        "show",
    )
    rec.finish_context_assembly(led)
    for i in range(10):
        store.record_override(
            led,
            decision_id=f"d{i}",
            reviewer="bob",
            verdict="X",
            reason="spike",
            prior_actuator="Pass",
        )
    assert store.canary_state == "rolled_back"
