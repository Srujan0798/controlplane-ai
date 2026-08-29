"""Phase 6a — jurisdiction axis changes actuators (T5.1).

The acceptance test: the same request under an `eu` pack and an `in` pack
produces DIFFERENT actuators.  An annotation-only implementation fails here.
"""
from __future__ import annotations

from controlplane.binder import bind_claims
from controlplane.models import (
    Action,
    AssertionStrength,
    BlastTier,
    Claim,
    ClaimKind,
    Principal,
    StepKind,
)
from controlplane.policy import PolicyRegistry
from controlplane.recorder import ProvenanceRecorder


def _registry() -> PolicyRegistry:
    reg = PolicyRegistry()
    reg.load_dir("policies")
    return reg


def _ledger_with_unsupported_hedged():
    """One unsupported + hedged claim on show_reply — looks benign."""
    rec = ProvenanceRecorder()
    principal = Principal(
        id="cs", roles=frozenset({"cs"}), clearance=frozenset({"vendor-public"})
    )
    led = rec.begin_request("jur-1", principal, "reply", "matrix-v1")
    step = rec.record_step(led, StepKind.RETRIEVAL, "faq")
    rec.record_span(
        led,
        step,
        source_id="doc:faq",
        acl=frozenset({"vendor-public"}),
        content="Shipping typically takes 5-7 business days.",
    )
    rec.finish_context_assembly(led)
    claim = Claim(
        "hedge",
        "this may still be covered under the extended warranty",
        ClaimKind.TEXTUAL,
        AssertionStrength.HEDGED,
        {"show_reply": 1.0},
    )
    bind_claims(led, [claim])
    return led


def test_eu_vs_in_pack_diverges_on_actuator():
    """Same ledger, same claim: EU pack → Edit, IN pack → Pass + annotate.

    EU elevates show_reply to R2 (tier_overrides) + closed_escalate fail stance.
    IN keeps R1 + open_annotate.  Geography changes the actuator.
    """
    reg = _registry()
    eu = reg.get("decision-support-eu")
    inn = reg.get("decision-support-in")
    assert eu.jurisdiction == "eu"
    assert inn.jurisdiction == "in"
    assert "GDPR" in eu.regulatory_basis or "AI Act" in eu.regulatory_basis
    assert "DPDP" in inn.regulatory_basis

    # The packs genuinely disagree on the tier for show_reply.
    eu_ap = eu.action("show_reply")
    in_ap = inn.action("show_reply")
    assert eu_ap.tier != in_ap.tier

    from controlplane.jurisdiction import decide_with_jurisdiction

    led_eu = _ledger_with_unsupported_hedged()
    d_eu = decide_with_jurisdiction(
        led_eu,
        Action("show_reply", "reply", in_ap.tier),
        eu,
    )

    led_in = _ledger_with_unsupported_hedged()
    d_in = decide_with_jurisdiction(
        led_in,
        Action("show_reply", "reply", in_ap.tier),
        inn,
    )

    assert d_eu.actuator != d_in.actuator, (
        f"expected divergent actuators, both {d_eu.actuator}"
    )
    # EU: R2 x unsupported+hedged → Edit
    assert d_eu.actuator.value == "Edit"
    # IN: R1 x unsupported+hedged → Pass + annotate
    assert d_in.actuator.value == "Pass + annotate"


def test_describe_pack_carries_jurisdiction():
    from controlplane.jurisdiction import describe_pack

    reg = _registry()
    eu = describe_pack(reg.get("decision-support-eu"))
    assert eu["jurisdiction"] == "eu"
    assert "GDPR" in eu["regulatory_basis"]
    assert eu["tier_overrides"]["show_reply"] == "R2"


def test_resolve_action_tier_applies_overrides():
    from controlplane.jurisdiction import resolve_action_tier

    reg = _registry()
    eu = reg.get("decision-support-eu")
    # show_reply is overridden to R2 in the EU pack even though default is R2
    assert resolve_action_tier(eu, "show_reply") == BlastTier.R2
    # show_text stays R1
    assert resolve_action_tier(eu, "show_text") == BlastTier.R1
