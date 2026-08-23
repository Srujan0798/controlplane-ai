"""Counterfactual bias probe — ACL skew on ledger spans (responsibility axis).

Stub measurement only: fraction of spans the principal cannot read.
Not a per-response moral verdict; distributional surface for judges.
"""
from __future__ import annotations

from typing import Any

from controlplane.ledger import EvidenceLedger


def probe_acl_skew(ledger: EvidenceLedger) -> dict[str, Any]:
    """Return `{acl_skew, flag}` for spans vs principal clearance.

    `acl_skew` = fraction of spans whose ACL is not ⊆ principal.clearance.
    `flag` is True when acl_skew > 0 (any unreadable span present).
    """
    spans = list(ledger.spans.values())
    if not spans:
        return {"acl_skew": 0.0, "flag": False}
    clearance = ledger.principal.clearance
    unreadable = sum(1 for sp in spans if not sp.acl.issubset(clearance))
    acl_skew = unreadable / len(spans)
    return {"acl_skew": acl_skew, "flag": acl_skew > 0}
