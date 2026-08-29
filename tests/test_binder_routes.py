"""Binder v2: one happy/sad case per route. Production CONTRADICTED + UNKNOWN."""
from __future__ import annotations

import pytest

from controlplane.binder import bind_claims
from controlplane.models import (
    Action,
    AssertionStrength,
    BlastTier,
    Claim,
    ClaimKind,
    Principal,
    StepKind,
    Verdict,
)
from controlplane.pipeline import ControlPlaneGate
from controlplane.recorder import ProvenanceRecorder


def _led(*contents: str):
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r", Principal(id="u", clearance=frozenset({"public"})), "t"
    )
    step = rec.record_step(led, StepKind.RETRIEVAL, "ctx")
    for i, content in enumerate(contents):
        rec.record_span(
            led,
            step,
            source_id=f"doc:{i}",
            acl=frozenset({"public"}),
            content=content,
        )
    rec.finish_context_assembly(led)
    return led


def test_numeric_happy_rupee_binds_to_inr_span():
    led = _led("Refund amount for order ORD-9 is 184000 INR.")
    claim = Claim(
        "amount",
        "Refund of ₹1,84,000",
        ClaimKind.NUMERIC,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.SUPPORTED
    assert "numeric" in binding.method
    assert "fixture" not in binding.method
    assert binding.span_ids
    assert binding.rationale


def test_numeric_sad_mismatch_contradicted_by_production_binder():
    led = _led("Refund amount for order ORD-9 is 104000 INR.")
    claim = Claim(
        "amount",
        "Refund of ₹1,84,000",
        ClaimKind.NUMERIC,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.CONTRADICTED
    assert "numeric" in binding.method
    assert binding.span_ids


def test_numeric_sad_absence_unsupported():
    led = _led("Clause 4.1 covers shipping delays and restocking.")
    claim = Claim(
        "amount",
        "Refund of ₹1,84,000",
        ClaimKind.NUMERIC,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.UNSUPPORTED
    assert binding.span_ids == ()


def test_structural_happy_clause_41():
    led = _led("Clause 4.1 covers shipping delays and restocking.")
    claim = Claim(
        "clause_41",
        "Clause 4.1 covers shipping delays",
        ClaimKind.STRUCTURAL,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.SUPPORTED
    assert "structural" in binding.method
    assert binding.span_ids


def test_structural_sad_clause_72_miss():
    led = _led("Clause 4.1 covers shipping delays and restocking.")
    claim = Claim(
        "clause_72",
        "issued under clause 7.2 of the vendor agreement",
        ClaimKind.STRUCTURAL,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.UNSUPPORTED
    assert binding.span_ids == ()
    assert "7.2" in binding.rationale or "absent" in binding.rationale.lower()


def test_textual_happy_high_coverage():
    led = _led(
        "Internal exception desk: customer account flagged for goodwill override."
    )
    claim = Claim(
        "hr_side",
        "customer account flagged for goodwill override",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.SUPPORTED
    assert "bm25" in binding.method or "lexical" in binding.method
    assert binding.span_ids


def test_textual_middle_band_unknown_live_path():
    led = _led("Approved refunds follow the published vendor schedule.")
    claim = Claim(
        "mid",
        "the published vendor schedule covers restocking delays",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.UNKNOWN
    assert binding.method != "fixture"


def test_textual_sad_low_unsupported():
    led = _led("Shipping typically takes 5-7 business days.")
    claim = Claim(
        "warranty",
        "this may still be covered under the extended warranty",
        ClaimKind.TEXTUAL,
        AssertionStrength.HEDGED,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.UNSUPPORTED


def test_textual_negation_contradicted():
    led = _led("the policy does not permit this refund")
    claim = Claim(
        "permit",
        "the policy permits this refund",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.CONTRADICTED


def test_derived_happy_sum_recompute():
    led = _led("Line A is 2 INR. Line B is 3 INR.")
    claim = Claim(
        "derived",
        "The sum of line items is 5 INR",
        ClaimKind.DERIVED,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.SUPPORTED
    assert "derived" in binding.method


def test_derived_sad_mismatch_contradicted():
    led = _led("Line A is 2 INR. Line B is 3 INR.")
    claim = Claim(
        "derived",
        "The sum of line items is 9 INR",
        ClaimKind.DERIVED,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.CONTRADICTED


def test_derived_not_recomputable_unknown_never_supported_by_substring():
    led = _led("The sum of line items is 5 INR as written, without operands.")
    claim = Claim(
        "derived",
        "The sum of line items is 5 INR",
        ClaimKind.DERIVED,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.UNKNOWN
    assert "derived" in binding.method or binding.method == "none"


def test_temporal_falls_through_without_crash():
    led = _led("Return window is 30 days for unused goods.")
    claim = Claim(
        "window",
        "Return window is 30 days",
        ClaimKind.TEMPORAL,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict in (
        Verdict.SUPPORTED,
        Verdict.UNKNOWN,
        Verdict.UNSUPPORTED,
    )


def test_enforce_rejects_fixture_map_unless_allowed():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "lockout",
        Principal(id="u", clearance=frozenset({"public"})),
        "t",
    )
    rec.finish_context_assembly(led)
    claim = Claim(
        "c",
        "hello",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        {"show": 1.0},
    )
    action = Action("show", "show", BlastTier.R1)
    gate = ControlPlaneGate()
    with pytest.raises(ValueError, match="fixture_map"):
        gate.run_prepared(
            use_case="decision-support",
            ledger=led,
            claims=[claim],
            actions=[action],
            fixture_map={"c": None},
            mode_override="enforce",
        )

    rec2 = ProvenanceRecorder()
    led2 = rec2.begin_request(
        "lockout-ok",
        Principal(id="u", clearance=frozenset({"public"})),
        "t",
    )
    rec2.finish_context_assembly(led2)
    gate.run_prepared(
        use_case="decision-support",
        ledger=led2,
        claims=[claim],
        actions=[action],
        fixture_map={"c": None},
        mode_override="enforce",
        allow_fixtures=True,
    )


def test_shadow_still_accepts_fixture_map():
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "shadow-fix",
        Principal(id="u", clearance=frozenset({"public"})),
        "t",
    )
    rec.finish_context_assembly(led)
    claim = Claim(
        "c",
        "hello",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        {"show": 1.0},
    )
    gate = ControlPlaneGate()
    result = gate.run_prepared(
        use_case="decision-support",
        ledger=led,
        claims=[claim],
        actions=[Action("show", "show", BlastTier.R1)],
        fixture_map={"c": None},
        mode_override="shadow",
    )
    assert result.mode == "shadow"
    assert led.bindings["c"].method == "fixture"
    assert led.bindings["c"].verdict == Verdict.UNSUPPORTED
