"""Frozen refund running example (ARCHITECTURE.md §9)."""
from __future__ import annotations

from controlplane.binder import bind_claims
from controlplane.extract import extract_claims
from controlplane.interlock import decide
from controlplane.ledger import EvidenceLedger
from controlplane.models import (
    Action,
    BlastTier,
    Claim,
    Principal,
    StepKind,
)
from controlplane.recorder import ProvenanceRecorder

UNGATED_RESPONSE = (
    "Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement."
)

# Not in the ungated response; extracted (never Claim literals) so the
# entitlement beat and clause-4.1 support beat stay live while fixtures remain.
DEMO_SUPPLEMENTAL = (
    "Clause 4.1 covers shipping delays. "
    "customer account flagged for goodwill override."
)


def refund_demo_actions() -> list[Action]:
    return [
        Action("show_text", "Show text to the customer", BlastTier.R1),
        Action(
            "issue_refund",
            "Issue the refund",
            BlastTier.R3,
            args={"amount": 184000, "currency": "INR", "order": "ORD-9"},
            irreversibility=True,
        ),
    ]


def extract_demo_claims(actions: list[Action] | None = None) -> list[Claim]:
    actions = actions or refund_demo_actions()
    return extract_claims(
        f"{UNGATED_RESPONSE} {DEMO_SUPPLEMENTAL}",
        actions=actions,
    )


def run_refund_scenario() -> EvidenceLedger:
    rec = ProvenanceRecorder()
    principal = Principal(
        id="cs-agent-17",
        roles=frozenset({"customer-support"}),
        clearance=frozenset({"vendor-public"}),
    )
    led = rec.begin_request(
        request_id="refund-ord-9",
        principal=principal,
        action_intent="customer-refund",
        policy_version="matrix-v1",
    )

    vendor_step = rec.record_step(led, StepKind.RETRIEVAL, "vendor_agreement")
    rec.record_span(
        led,
        vendor_step,
        source_id="doc:vendor-agreement-v3",
        acl=frozenset({"vendor-public"}),
        content=(
            "Clause 4.1 covers shipping delays and restocking. "
            "Approved refunds follow the published vendor schedule."
        ),
    )

    order_step = rec.record_step(led, StepKind.TOOL, "order_lookup")
    amount_span = rec.record_span(
        led,
        order_step,
        source_id="db:orders",
        acl=frozenset({"vendor-public"}),
        content="Refund amount for order ORD-9 is 184000 INR.",
    )

    hr_step = rec.record_step(led, StepKind.RETRIEVAL, "hr_internal_note")
    rec.record_span(
        led,
        hr_step,
        source_id="doc:hr-exception-desk",
        acl=frozenset({"hr-confidential"}),
        content="Internal exception desk: customer account flagged for goodwill override.",
    )

    # Dead-compute steps: spans that ground no accepted claim.
    faq_step = rec.record_step(led, StepKind.RETRIEVAL, "faq_search")
    rec.record_span(
        led,
        faq_step,
        source_id="doc:faq",
        acl=frozenset({"vendor-public"}),
        content="Return window is 30 days for unused goods.",
    )
    crm_step = rec.record_step(led, StepKind.TOOL, "crm_lookup")
    rec.record_span(
        led,
        crm_step,
        source_id="db:crm",
        acl=frozenset({"vendor-public"}),
        content="Ticket T-441 opened Tuesday; no policy citation attached.",
    )

    rec.finish_context_assembly(led)

    actions = refund_demo_actions()
    claims = extract_demo_claims(actions)
    bind_claims(
        led,
        claims,
        fixture_map={
            "amount": (amount_span,),
            "clause_72": None,  # Clause 7.2 does not exist.
        },
    )

    for action in actions:
        decide(led, action)
    return led
