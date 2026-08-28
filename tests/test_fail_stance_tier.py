"""Fail-stance by blast tier (PARTIAL #12).

Enforces that a policy's declared fail-stance actually flips matrix Pass
verdicts toward Escalate at irreversible blast tiers (R2/R3). The MATRIX is
never redrawn; enforcement is monotonic (only downgrades, never relaxes).
"""
from __future__ import annotations

import pytest

from controlplane.interlock import decide
from controlplane.mock_refund import execute_refund
from controlplane.models import (
    Action,
    Actuator,
    AssertionStrength,
    BlastTier,
    Binding,
    Claim,
    ClaimKind,
    Principal,
    Span,
    Verdict,
)
from controlplane.policy import _parse_pack


def _led():
    from controlplane.ledger import EvidenceLedger

    return EvidenceLedger.begin(
        "r", Principal(id="u", clearance=frozenset()), "x"
    )


def _supported(led, claim_id, action_id):
    led.claims[claim_id] = Claim(
        claim_id, "ok", ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL, {action_id: 1.0},
    )
    led.bindings[claim_id] = Binding(claim_id, ("s1",), "fixture", Verdict.SUPPORTED)
    led.spans["s1"] = Span("s1", "step", "src", frozenset(), "ok content", "h")


def _unsupported(led, claim_id, action_id):
    led.claims[claim_id] = Claim(
        claim_id, "Clause 7.2 permits refund", ClaimKind.STRUCTURAL,
        AssertionStrength.CATEGORICAL, {action_id: 1.0},
    )
    led.bindings[claim_id] = Binding(claim_id, (), "none", Verdict.UNSUPPORTED)


def test_closed_r3_supported_claim_must_escalate():
    """Requirement 1: closed + R3 + supported claim -> Escalate (was Pass)."""
    led = _led()
    _supported(led, "c", "issue_refund")
    d = decide(
        led,
        Action("issue_refund", "issue_refund", BlastTier.R3, irreversibility=True),
        fail_stance="closed",
    )
    assert d.actuator == Actuator.ESCALATE
    assert d.packet.get("fail_stance_enforced") is True


def test_closed_r3_unsupported_driving_claim_must_escalate_held():
    """Requirement 2: closed + R3 + one UNSUPPORTED driving claim -> Escalate (held)."""
    led = _led()
    _unsupported(led, "c", "issue_refund")
    d = decide(
        led,
        Action("issue_refund", "issue_refund", BlastTier.R3, irreversibility=True),
        fail_stance="closed",
    )
    assert d.actuator == Actuator.ESCALATE
    result = execute_refund(allowed=d.actuator == Actuator.PASS)
    assert result["committed"] is False
    assert result["status"] == "REFUND HELD"


def test_default_closed_when_pack_omits_field():
    """Requirement 3 prep: a pack that omits fail_stance fails closed."""
    pack = _parse_pack({"use_case": "x", "policy_version": "v", "actions": {}})
    assert pack.fail_stance == "closed"


def test_default_closed_r2_supported_claim_must_escalate():
    """Requirement 3: default (closed) + R2 + supported claim -> Escalate."""
    led = _led()
    _supported(led, "c", "draft")
    d = decide(
        led,
        Action("draft", "draft_partner_email", BlastTier.R2),
        fail_stance="closed",
    )
    assert d.actuator == Actuator.ESCALATE
    assert d.packet.get("fail_stance_enforced") is True


def test_closed_r0_r1_supported_may_still_pass():
    """Requirement 4: low blast tiers may still Pass under closed stance."""
    for tier in (BlastTier.R0, BlastTier.R1):
        led = _led()
        _supported(led, "c", "show")
        d = decide(
            led,
            Action("show", "show_text", tier),
            fail_stance="closed",
        )
        assert d.actuator in (Actuator.PASS, Actuator.PASS_ANNOTATE)
        assert d.packet.get("fail_stance_enforced") is not True


def test_open_stance_never_flips_matrix_verdict():
    """Monotonic guard: open stance leaves a clean R3 supported Pass alone."""
    led = _led()
    _supported(led, "c", "issue_refund")
    d = decide(
        led,
        Action("issue_refund", "issue_refund", BlastTier.R3, irreversibility=True),
        fail_stance="open_annotate",
    )
    assert d.actuator == Actuator.PASS


@pytest.mark.parametrize("stance", ["closed", "closed_escalate"])
def test_closed_family_vocabulary_all_escalate(stance):
    led = _led()
    _supported(led, "c", "issue_refund")
    d = decide(
        led,
        Action("issue_refund", "issue_refund", BlastTier.R3, irreversibility=True),
        fail_stance=stance,
    )
    assert d.actuator == Actuator.ESCALATE
