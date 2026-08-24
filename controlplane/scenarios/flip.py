"""Principal-flip running example: same HR-COMP-L6 span, same claim, only the caller changes.

analyst_01 is NOT entitled to the HR-COMP-L6 span -> entitlement violation ->
R1 x Contradicted / entitlement violation -> Edit.

hr_partner_01 IS entitled (clearance carries hr-comp-l6) -> claim is clean /
supported -> R1 x empty column -> Pass.

Zero LLM. Routes through the EXISTING matrix cells only (no new cell). The
admission gate's real decide()/audit_claim() does the work; nothing is mocked.
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
from controlplane.pipeline import ControlPlaneGate
from controlplane.recorder import ProvenanceRecorder

# The single HR-COMP-L6 span both principals share.
SPAN_ACL = frozenset({"hr-comp-l6"})
CLAIM_TEXT = "L6 base range is confidential HR-partner material."

# Entitlement is pure set-membership: a principal is entitled iff its clearance
# is a superset of the span ACL. analyst_01 is not; hr_partner_01 is.
_PRINCIPALS: dict[str, Principal] = {
    "analyst_01": Principal(
        id="analyst_01",
        roles=frozenset({"analyst"}),
        clearance=frozenset({"analyst"}),  # hr-comp-l6 NOT present -> violation
    ),
    "hr_partner_01": Principal(
        id="hr_partner_01",
        roles=frozenset({"hr-partner"}),
        clearance=frozenset({"hr-partner", "hr-comp-l6"}),  # entitled -> clean
    ),
}


def get_principal(principal_id: str) -> Principal:
    if principal_id not in _PRINCIPALS:
        raise KeyError(f"unknown principal for flip demo: {principal_id}")
    return _PRINCIPALS[principal_id]


def build_flip(
    principal_id: str = "analyst_01",
) -> tuple[EvidenceLedger, list[Claim], list[Action], dict[str, tuple[str, ...] | None]]:
    """Build the HR-COMP-L6 ledger + claim for a given principal.

    Returns (ledger, claims, actions, fixture_map) ready for
    ``ControlPlaneGate.run_prepared`` so the REAL interlock runs end to end.
    """
    principal = get_principal(principal_id)
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        request_id="flip-hr-comp-l6",
        principal=principal,
        action_intent="show-text",
        policy_version="pack-flip-v1",
    )
    step = rec.record_step(led, StepKind.RETRIEVAL, "hr_comp_l6_sheet")
    span = rec.record_span(
        led,
        step,
        source_id="doc:hr-comp-l6",
        acl=SPAN_ACL,
        content="L6 base salary range band: 42L-61L INR (band confidential to HR partner).",
    )
    rec.finish_context_assembly(led)

    claim = Claim(
        "l6_confidential",
        CLAIM_TEXT,
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        {"show_text": 1.0},
    )
    actions = [Action("show_text", "Show text to the caller", BlastTier.R1)]
    fixture_map: dict[str, tuple[str, ...] | None] = {"l6_confidential": (span,)}
    return led, [claim], actions, fixture_map


def run_flip_scenario(principal_id: str = "analyst_01") -> EvidenceLedger:
    """Exercise the real gate end to end (bind -> entitle -> interlock)."""
    led, claims, actions, fixture_map = build_flip(principal_id)
    gate = ControlPlaneGate()
    gate.run_prepared(
        use_case="flip",
        ledger=led,
        claims=claims,
        actions=actions,
        fixture_map=fixture_map,
    )
    return led
