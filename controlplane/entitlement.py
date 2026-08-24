from __future__ import annotations

from controlplane.ledger import EvidenceLedger
from controlplane.models import EntitlementFinding


def audit_claim(ledger: EvidenceLedger, claim_id: str) -> EntitlementFinding:
    """Set-membership entitlement: span.acl ⊆ principal.clearance. Zero LLM."""
    binding = ledger.bindings[claim_id]
    offending: list[str] = []
    for span_id in binding.span_ids:
        span = ledger.spans[span_id]
        if not span.acl.issubset(ledger.principal.clearance):
            offending.append(span_id)
    return EntitlementFinding(
        claim_id=claim_id,
        violated=bool(offending),
        offending_span_ids=tuple(offending),
        detail=(
            "ENTITLEMENT_VIOLATION: span ACL not subset of principal clearance"
            if offending
            else "ok"
        ),
    )
