"""T5.3 — threshold proposal behind a shadow replay (RED first).

Acceptance: a threshold change is REFUSED unless a replay delta was produced.

We require that ``FeedbackStore.record_shadow_replay`` has been called for the
named threshold with a non-empty sweep, producing a measured FP/FN delta, BEFORE
``propose_threshold`` may return ``ship=True``. Without that evidence the proposal
is refused (ship=False) and records why.
"""
from __future__ import annotations

from controlplane.feedback import FeedbackStore


def test_proposal_refused_without_shadow_replay():
    store = FeedbackStore()
    prop = store.propose_threshold(
        name="bm25_coverage_supported",
        current=0.72,
        proposed=0.68,
        shadow_fp_delta=None,
        shadow_fn_delta=None,
    )
    assert prop["ship"] is False
    assert "refused" in prop["status"].lower() or "shadow" in prop["status"].lower()


def test_proposal_ships_after_recorded_replay():
    store = FeedbackStore()
    # Produce a real replay delta (the harness would supply these numbers).
    store.record_shadow_replay(
        name="bm25_coverage_supported",
        traces=1000,
        fp_delta=0.01,
        fn_delta=-0.02,
    )
    prop = store.propose_threshold(
        name="bm25_coverage_supported",
        current=0.72,
        proposed=0.68,
        shadow_fp_delta=0.01,
        shadow_fn_delta=-0.02,
    )
    assert prop["ship"] is True
    assert prop["replay_traces"] == 1000


def test_replay_delta_must_match_named_threshold():
    store = FeedbackStore()
    store.record_shadow_replay(name="other_threshold", traces=500, fp_delta=0.0, fn_delta=0.0)
    # Replaying a different threshold does NOT unblock this one.
    prop = store.propose_threshold(
        name="bm25_coverage_supported",
        current=0.72,
        proposed=0.68,
        shadow_fp_delta=None,
        shadow_fn_delta=None,
    )
    assert prop["ship"] is False


def test_recorded_replay_stored_on_ledger():
    store = FeedbackStore()
    rec = __import__("controlplane.recorder", fromlist=["ProvenanceRecorder"]).ProvenanceRecorder()
    from controlplane.models import Principal

    led = rec.begin_request("rp-1", Principal(id="r", clearance=frozenset({"public"})), "show")
    rec.finish_context_assembly(led)
    store.record_shadow_replay(
        name="bm25_coverage_supported",
        traces=2000,
        fp_delta=0.005,
        fn_delta=-0.01,
        ledger=led,
    )
    assert len(led.get("shadow_replay")) >= 1
    assert led.verify_chain() is True
