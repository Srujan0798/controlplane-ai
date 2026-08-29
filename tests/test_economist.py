"""Phase 4b — dead compute economist (TDD)."""
from __future__ import annotations

from controlplane.economist import analyze_dead_compute
from controlplane.models import (
    Action,
    AssertionStrength,
    Binding,
    BlastTier,
    Claim,
    ClaimKind,
    Principal,
    StepKind,
    Verdict,
)
from controlplane.recorder import ProvenanceRecorder


def test_dead_steps_are_those_grounding_no_accepted_claim():
    rec = ProvenanceRecorder()
    principal = Principal(id="p", roles=frozenset(), clearance=frozenset({"public"}))
    led = rec.begin_request("req-1", principal, "intent", "v1")
    live = rec.record_step(led, StepKind.TOOL, "order_lookup")
    live_span = rec.record_span(
        led,
        live,
        source_id="db:orders",
        acl=frozenset({"public"}),
        content="amount is 100 INR",
    )
    dead = rec.record_step(led, StepKind.RETRIEVAL, "faq_search")
    rec.record_span(
        led,
        dead,
        source_id="doc:faq",
        acl=frozenset({"public"}),
        content="unused faq text",
    )
    rec.finish_context_assembly(led)

    claim = Claim("c1", "amount is 100 INR", ClaimKind.TEXTUAL, AssertionStrength.CATEGORICAL)
    led.claims[claim.claim_id] = claim
    led.bindings[claim.claim_id] = Binding(
        claim.claim_id, (live_span,), "exact", Verdict.SUPPORTED
    )
    led.actions["a1"] = Action("a1", "show", BlastTier.R1)

    report = analyze_dead_compute(led, inr_per_1k_tokens=0.5)
    assert report["dead_step_count"] >= 1
    assert any(s["name"] == "faq_search" for s in report["dead_steps"])
    assert report["live_step_count"] >= 1
    assert "token_estimate_dead" in report
    assert "inr_estimate_dead" in report
    assert "inr_per_1k_requests" in report
    assert report["rate_inr_per_1k_tokens"] == 0.5
