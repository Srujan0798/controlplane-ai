"""Knowledge principal-flip: same span/claim, flip only the principal."""
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

HR_COMP_L6 = (
    "HR-COMP-L6 compensation band: L6 base range is confidential HR-partner material. "
    "Published band midpoint for L6 is internal-only."
)

CLAIM_TEXT = "L6 base range is confidential HR-partner material."


def analyst_01() -> Principal:
    return Principal(
        id="analyst_01",
        roles=frozenset({"employee"}),
        clearance=frozenset({"employee"}),
    )


def hr_partner_01() -> Principal:
    return Principal(
        id="hr_partner_01",
        roles=frozenset({"hr_partner"}),
        clearance=frozenset({"hr_partner", "employee"}),
    )


def run_knowledge_scenario(principal: Principal) -> EvidenceLedger:
    """Same spans and claims; only the calling principal differs."""
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        request_id=f"knowledge-{principal.id}",
        principal=principal,
        action_intent="knowledge-query",
        policy_version="matrix-v1",
    )

    step = rec.record_step(led, StepKind.RETRIEVAL, "hr_comp_lookup")
    span_id = rec.record_span(
        led,
        step,
        source_id="HR-COMP-L6",
        acl=frozenset({"hr_partner"}),
        content=HR_COMP_L6,
        offsets=(0, len(HR_COMP_L6)),
    )
    rec.finish_context_assembly(led)

    claim = Claim(
        "l6_band",
        CLAIM_TEXT,
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        {"show_text": 1.0},
    )
    bind_claims(led, [claim], fixture_map={"l6_band": (span_id,)})
    decide(led, Action("show_text", "Show knowledge answer", BlastTier.R1))
    return led


def run_principal_flip() -> tuple[EvidenceLedger, EvidenceLedger]:
    """Unauthorized analyst → Edit; entitled HR partner → Pass."""
    unauthorized = run_knowledge_scenario(analyst_01())
    entitled = run_knowledge_scenario(hr_partner_01())
    return unauthorized, entitled
