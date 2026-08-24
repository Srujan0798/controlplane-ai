"""Fail-closed regressions.

Each test here pins a hole that once let an action through without proof.
The plane may only ever fail toward Escalate/Block, never toward Pass.
"""
from __future__ import annotations

import pytest

from controlplane.binder import bind_claims
from controlplane.interlock import decide
from controlplane.mock_refund import execute_refund
from controlplane.models import (
    Action,
    Actuator,
    AssertionStrength,
    BlastTier,
    Claim,
    ClaimKind,
    EntitlementFinding,
    Principal,
    StepKind,
    Verdict,
)
from controlplane.recorder import ProvenanceRecorder

R3 = Action("issue_refund", "Issue the refund", BlastTier.R3, irreversibility=True)


def _ledger_with_unentitled_span():
    """Caller is refund_agent; the recorded span is internal_analyst only."""
    rec = ProvenanceRecorder()
    principal = Principal(
        id="agent_refund_7",
        roles=frozenset({"refund_agent"}),
        clearance=frozenset({"refund_agent"}),
    )
    led = rec.begin_request("probe", principal, "refund")
    step = rec.record_step(led, StepKind.RETRIEVAL, "finance_internal")
    span_id = rec.record_span(
        led,
        step,
        source_id="FIN-INTERNAL-NOTE",
        acl=frozenset({"internal_analyst"}),
        content="goodwill override approved",
    )
    rec.finish_context_assembly(led)
    return led, span_id


def _claim(claim_id: str, action_id: str = "issue_refund") -> Claim:
    return Claim(
        claim_id,
        "the refund is authorised",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        {action_id: 1.0},
    )


def test_fixture_citing_absent_span_cannot_earn_supported():
    """A binding may only cite spans the ledger recorded. Asserted != computed."""
    led, _ = _ledger_with_unentitled_span()
    binding = bind_claims(
        led, [_claim("c1")], fixture_map={"c1": ("span-does-not-exist",)}
    )[0]
    assert binding.verdict == Verdict.UNSUPPORTED
    assert binding.span_ids == ()
    assert binding.method == "fixture-unresolved"


def test_unresolvable_span_escalates_instead_of_passing():
    led, _ = _ledger_with_unentitled_span()
    bind_claims(led, [_claim("c1")], fixture_map={"c1": ("span-does-not-exist",)})
    decision = decide(led, R3)
    assert decision.actuator is not Actuator.PASS
    assert decision.actuator == Actuator.ESCALATE


def test_supplied_findings_cannot_clear_a_computed_violation():
    """Entitlement is always on: a caller may raise a verdict, never clear one."""
    led, span_id = _ledger_with_unentitled_span()
    bind_claims(led, [_claim("c1")], fixture_map={"c1": (span_id,)})

    computed = decide(led, R3)
    assert computed.actuator == Actuator.BLOCK

    led2, span_id2 = _ledger_with_unentitled_span()
    bind_claims(led2, [_claim("c1")], fixture_map={"c1": (span_id2,)})
    bypass = decide(
        led2,
        R3,
        findings={
            "c1": EntitlementFinding("c1", False, (), "caller says it is fine")
        },
    )
    assert bypass.actuator == Actuator.BLOCK


def test_empty_findings_dict_does_not_disable_entitlement():
    led, span_id = _ledger_with_unentitled_span()
    bind_claims(led, [_claim("c1")], fixture_map={"c1": (span_id,)})
    assert decide(led, R3, findings={}).actuator == Actuator.BLOCK


@pytest.mark.parametrize(
    ("tier", "expected"),
    [
        (BlastTier.R0, Actuator.PASS),
        (BlastTier.R1, Actuator.PASS_ANNOTATE),
        (BlastTier.R2, Actuator.ESCALATE),
        (BlastTier.R3, Actuator.ESCALATE),
    ],
)
def test_action_with_no_routed_claims_uses_the_unknown_column(tier, expected):
    """Nothing proven for this action is UNKNOWN, routed through the frozen matrix."""
    led, _ = _ledger_with_unentitled_span()
    bind_claims(led, [_claim("c1", action_id="some_other_action")], fixture_map={"c1": None})
    decision = decide(led, Action("act", "act", tier))
    assert decision.actuator == expected
    assert decision.matrix_col == "Unknown"


def test_typo_in_action_id_cannot_commit_the_refund():
    """The demo's exact failure case: a detached gate must not pay out."""
    led, _ = _ledger_with_unentitled_span()
    bind_claims(
        led,
        [_claim("clause_72", action_id="issue_refnud")],  # typo detaches the claim
        fixture_map={"clause_72": None},
    )
    decision = decide(led, R3)
    assert decision.actuator == Actuator.ESCALATE
    result = execute_refund(allowed=decision.actuator == Actuator.PASS)
    assert result["committed"] is False
    assert result["status"] == "REFUND HELD"
