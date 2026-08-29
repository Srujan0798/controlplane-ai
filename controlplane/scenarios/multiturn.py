"""Multi-turn compounding risk — Phase 7.

Turn 1: hedged claim at R1 → Pass + annotate.
Turn 3: R3 action inherits that turn-1 claim via role_in_action → Escalate.
"""
from __future__ import annotations

from controlplane.binder import bind_claims
from controlplane.interlock import decide
from controlplane.ledger import EvidenceLedger
from controlplane.models import (
    Action,
    AssertionStrength,
    BlastTier,
    Claim,
    ClaimKind,
    Principal,
    StepKind,
)
from controlplane.recorder import ProvenanceRecorder
from controlplane.session import SessionStore


def run_multiturn_compounding(
    sessions: SessionStore | None = None,
) -> tuple[EvidenceLedger, EvidenceLedger]:
    """Return (turn1_ledger, turn3_ledger)."""
    sessions = sessions or SessionStore()
    session_id = "multiturn-compound-1"
    principal = Principal(
        id="cs-agent-17",
        roles=frozenset({"customer-support"}),
        clearance=frozenset({"vendor-public"}),
    )
    sessions.begin_session(session_id, principal.id)

    # --- Turn 1: hedged claim, R1 ---
    rec = ProvenanceRecorder()
    led1 = rec.begin_request("turn-1", principal, "support-reply", "matrix-v1")
    step = rec.record_step(led1, StepKind.RETRIEVAL, "faq")
    rec.record_span(
        led1,
        step,
        source_id="doc:faq",
        acl=frozenset({"vendor-public"}),
        content="Shipping typically takes 5-7 business days.",
    )
    rec.finish_context_assembly(led1)
    hedge = Claim(
        "warranty_hedge",
        "this may still be covered under the extended warranty",
        ClaimKind.TEXTUAL,
        AssertionStrength.HEDGED,
        {"show_reply": 1.0},
    )
    bind_claims(led1, [hedge])
    d1 = decide(led1, Action("show_reply", "Show reply", BlastTier.R1))
    sessions.attach_request(
        session_id,
        led1.request_id,
        {
            "request_id": led1.request_id,
            "actuators": {"show_reply": d1.actuator.value},
            "inherited_claim_ids": ["warranty_hedge"],
        },
    )

    # --- Turn 3: R3 refund inherits the hedged claim at full weight ---
    rec3 = ProvenanceRecorder()
    led3 = rec3.begin_request("turn-3", principal, "customer-refund", "matrix-v1")
    step3 = rec3.record_step(led3, StepKind.RETRIEVAL, "vendor")
    rec3.record_span(
        led3,
        step3,
        source_id="doc:vendor",
        acl=frozenset({"vendor-public"}),
        content="Clause 4.1 covers shipping delays.",
    )
    rec3.finish_context_assembly(led3)
    inherited = Claim(
        "warranty_hedge",
        "this may still be covered under the extended warranty",
        ClaimKind.TEXTUAL,
        AssertionStrength.HEDGED,
        # Inherited into the irreversible action — compounding risk.
        {"issue_refund": 1.0},
    )
    bind_claims(led3, [inherited])
    d3 = decide(
        led3,
        Action(
            "issue_refund",
            "Issue the refund",
            BlastTier.R3,
            irreversibility=True,
        ),
        fail_stance="closed_escalate",
    )
    sessions.attach_request(
        session_id,
        led3.request_id,
        {
            "request_id": led3.request_id,
            "actuators": {"issue_refund": d3.actuator.value},
            "inherited_from": "turn-1",
        },
    )
    return led1, led3
