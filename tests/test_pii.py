"""Phase 3 — PII / entity leakage detectors (TDD)."""
from __future__ import annotations

from controlplane.pii import (
    detect_pii,
    is_valid_aadhaar,
    is_valid_card_luhn,
    is_valid_pan,
    pii_unbound_in_text,
)


def test_pan_checksum_valid_and_invalid():
    # Valid format + structure check (letter pattern AAAAA9999A)
    assert is_valid_pan("ABCDE1234F") is True
    assert is_valid_pan("ABCDE12345") is False
    assert is_valid_pan("abcdE1234F") is False


def test_aadhaar_verhoeff_valid_and_invalid():
    # Well-known Verhoeff-valid test vector style numbers
    assert is_valid_aadhaar("233812706435") is True  # Verhoeff-valid
    assert is_valid_aadhaar("233812706431") is False
    assert is_valid_aadhaar("1234") is False


def test_card_luhn():
    assert is_valid_card_luhn("4111111111111111") is True
    assert is_valid_card_luhn("4111111111111112") is False


def test_detect_pii_finds_email_phone_pan():
    text = "Contact agent at agent@example.com or +91 98765 43210. PAN ABCDE1234F."
    hits = detect_pii(text)
    kinds = {h.kind for h in hits}
    assert "email" in kinds
    assert "phone_in" in kinds
    assert "pan" in kinds


def test_pii_unbound_when_not_in_spans():
    text = "Refund to PAN ABCDE1234F approved."
    span_texts = ["Refund amount for order ORD-9 is 184000 INR."]
    unbound = pii_unbound_in_text(text, span_texts)
    assert any(h.kind == "pan" for h in unbound)


def test_pii_bound_when_present_in_span():
    text = "Refund to PAN ABCDE1234F approved."
    span_texts = ["Customer PAN ABCDE1234F on file for ORD-9."]
    unbound = pii_unbound_in_text(text, span_texts)
    assert not any(h.kind == "pan" for h in unbound)


def test_fabricated_pan_forces_block_at_r3():
    from controlplane.interlock import decide
    from controlplane.models import Action, BlastTier, Principal, StepKind, Actuator
    from controlplane.pii import apply_pii_rule_a
    from controlplane.recorder import ProvenanceRecorder

    rec = ProvenanceRecorder()
    principal = Principal(
        id="cs", roles=frozenset({"cs"}), clearance=frozenset({"vendor-public"})
    )
    led = rec.begin_request("pii-fab", principal, "refund", "matrix-v1")
    step = rec.record_step(led, StepKind.TOOL, "order_lookup")
    rec.record_span(
        led,
        step,
        source_id="db:orders",
        acl=frozenset({"vendor-public"}),
        content="Refund amount for order ORD-9 is 184000 INR.",
    )
    rec.finish_context_assembly(led)
    action = Action("issue_refund", "Issue refund", BlastTier.R3, irreversibility=True)
    led.actions[action.action_id] = action
    apply_pii_rule_a(
        led,
        "Refund issued. Customer PAN ABCDE1234F on file.",
        action_ids=[action.action_id],
    )
    d = decide(led, action)
    assert d.actuator == Actuator.BLOCK
    assert d.matrix_col.startswith("Contradicted")


def test_entitled_pan_in_span_does_not_force_rule_a():
    from controlplane.pii import apply_pii_rule_a
    from controlplane.models import Principal, StepKind
    from controlplane.recorder import ProvenanceRecorder

    rec = ProvenanceRecorder()
    principal = Principal(
        id="cs", roles=frozenset({"cs"}), clearance=frozenset({"vendor-public"})
    )
    led = rec.begin_request("pii-ok", principal, "refund", "matrix-v1")
    step = rec.record_step(led, StepKind.DB, "kyc")
    rec.record_span(
        led,
        step,
        source_id="db:kyc",
        acl=frozenset({"vendor-public"}),
        content="Customer PAN ABCDE1234F verified.",
    )
    rec.finish_context_assembly(led)
    added = apply_pii_rule_a(led, "Refund to PAN ABCDE1234F approved.")
    assert added == []


def test_unentitled_pan_span_takes_entitlement_path():
    from controlplane.binder import bind_claims
    from controlplane.entitlement import audit_claim
    from controlplane.interlock import decide
    from controlplane.models import (
        Action,
        AssertionStrength,
        BlastTier,
        Claim,
        ClaimKind,
        Principal,
        StepKind,
        Actuator,
    )
    from controlplane.recorder import ProvenanceRecorder

    rec = ProvenanceRecorder()
    principal = Principal(
        id="cs", roles=frozenset({"cs"}), clearance=frozenset({"vendor-public"})
    )
    led = rec.begin_request("pii-acl", principal, "refund", "matrix-v1")
    step = rec.record_step(led, StepKind.DB, "kyc")
    rec.record_span(
        led,
        step,
        source_id="db:kyc",
        acl=frozenset({"kyc-confidential"}),
        content="Customer PAN ABCDE1234F verified.",
    )
    rec.finish_context_assembly(led)
    claim = Claim(
        "pan_cite",
        "Customer PAN ABCDE1234F verified.",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        {"issue_refund": 1.0},
    )
    bind_claims(led, [claim])
    finding = audit_claim(led, "pan_cite")
    assert finding.violated is True
    d = decide(led, Action("issue_refund", "Issue refund", BlastTier.R3, irreversibility=True))
    assert d.actuator == Actuator.BLOCK
    assert "entitlement" in d.matrix_col.lower() or d.matrix_col.startswith("Contradicted")
