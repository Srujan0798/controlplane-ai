"""Three Round 2 reference-parameter fixtures: support, copilot, decision-support."""
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


def _run(
    *,
    request_id: str,
    principal: Principal,
    action_intent: str,
    step_name: str,
    source_id: str,
    span_content: str,
    claim: Claim,
    action: Action,
) -> EvidenceLedger:
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        request_id=request_id,
        principal=principal,
        action_intent=action_intent,
        policy_version="matrix-v1",
    )
    step_id = rec.record_step(led, StepKind.RETRIEVAL, step_name)
    rec.record_span(
        led,
        step_id,
        source_id=source_id,
        acl=principal.clearance,
        content=span_content,
    )
    rec.finish_context_assembly(led)
    bind_claims(led, [claim], fixture_map={claim.claim_id: None})
    decide(led, action)
    return led


def run_customer_support() -> EvidenceLedger:
    """R1 show_reply: unsupported + hedged → Pass + annotate."""
    return _run(
        request_id="support-ticket-88",
        principal=Principal(
            id="cs-bot-4",
            roles=frozenset({"customer-support"}),
            clearance=frozenset({"vendor-public"}),
        ),
        action_intent="customer-support-reply",
        step_name="shipping_faq",
        source_id="doc:shipping-faq",
        span_content=(
            "Shipping typically takes 5-7 business days. "
            "Returns are accepted within 30 days for unused goods."
        ),
        claim=Claim(
            "warranty_hedge",
            "this may still be covered under the extended warranty",
            ClaimKind.TEXTUAL,
            AssertionStrength.HEDGED,
            {"show_reply": 1.0},
        ),
        action=Action("show_reply", "Show reply to the customer", BlastTier.R1),
    )


def run_knowledge_copilot() -> EvidenceLedger:
    """R2 draft_partner_email: unsupported + categorical → Edit."""
    return _run(
        request_id="copilot-partner-12",
        principal=Principal(
            id="km-copilot-2",
            roles=frozenset({"internal-knowledge"}),
            clearance=frozenset({"internal"}),
        ),
        action_intent="draft-partner-email",
        step_name="partner_wiki",
        source_id="doc:partner-onboarding",
        span_content=(
            "Partner onboarding checklist: NDA, sandbox credentials, kickoff call."
        ),
        claim=Claim(
            "partner_sla",
            "Partner SLA is two hours for severity-1 tickets",
            ClaimKind.STRUCTURAL,
            AssertionStrength.CATEGORICAL,
            {"draft_partner_email": 1.0},
        ),
        action=Action(
            "draft_partner_email",
            "Draft email to partner (external send)",
            BlastTier.R2,
        ),
    )


def run_decision_refund() -> EvidenceLedger:
    """R3 issue_refund: unsupported + categorical → Escalate."""
    return _run(
        request_id="decision-refund-ord-9",
        principal=Principal(
            id="ds-agent-3",
            roles=frozenset({"decision-support"}),
            clearance=frozenset({"vendor-public"}),
        ),
        action_intent="decision-support-refund",
        step_name="vendor_agreement",
        source_id="doc:vendor-agreement-v3",
        span_content=(
            "Clause 4.1 covers shipping delays and restocking. "
            "Approved refunds follow the published vendor schedule."
        ),
        claim=Claim(
            "clause_72",
            "Clause 7.2 permits this refund",
            ClaimKind.STRUCTURAL,
            AssertionStrength.CATEGORICAL,
            {"issue_refund": 1.0},
        ),
        action=Action(
            "issue_refund",
            "Issue the refund",
            BlastTier.R3,
            args={"amount": 184000, "currency": "INR", "order": "ORD-9"},
            irreversibility=True,
        ),
    )
