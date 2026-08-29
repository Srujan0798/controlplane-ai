"""Jurisdiction axis on policy packs (T5.1).

A policy pack carries a `jurisdiction` tag (eu/in/etc) plus `tier_overrides`
and `regulatory_basis`. This module turns those annotations into *behaviour*:
the actuator for an action can change when the caller swaps packs, even if
every other input is identical.

The interlock stays sole decider — jurisdiction.py only feeds the interlock
the right tier for the action under the caller's pack.
"""
from __future__ import annotations

from typing import Any

from controlplane.interlock import decide as _interlock_decide
from controlplane.models import Action, Actuator, BlastTier, Decision, EntitlementFinding
from controlplane.ledger import EvidenceLedger
from controlplane.policy import PolicyPack


def resolve_action_tier(pack: PolicyPack, action_id: str) -> BlastTier:
    """The effective blast tier for an action under this pack.

    `PolicyPack.action()` already applies `tier_overrides`; this is the
    jurisdiction-exposed lookup so callers don't reach into pack internals.
    """
    return pack.action(action_id).tier


def decide_with_jurisdiction(
    ledger: EvidenceLedger,
    action: Action,
    pack: PolicyPack,
    findings: dict[str, EntitlementFinding] | None = None,
) -> Decision:
    """Run the interlock using the pack's fail-stance and tier-overrides.

    The tier used is the pack-overridden tier for `action.action_id`, not the
    tier the caller happens to pass in. This is what makes geography change
    the actuator: an `eu` pack can elevate a show_reply from R1 to R2,
    turning Pass+annotate into Edit.
    """
    ap = pack.action(action.action_id)
    tier = ap.tier
    if tier is not action.tier:
        action = Action(
            action_id=action.action_id,
            name=action.name,
            tier=tier,
            args=action.args,
            irreversibility=ap.irreversibility,
        )
    return _interlock_decide(ledger, action, findings=findings, fail_stance=pack.fail_stance)


def pack_actuator(
    ledger: EvidenceLedger,
    action: Action,
    pack: PolicyPack,
    findings: dict[str, EntitlementFinding] | None = None,
) -> Actuator:
    """Convenience: the single actuator the interlock assigns under this pack."""
    return decide_with_jurisdiction(ledger, action, pack, findings=findings).actuator


def describe_pack(pack: PolicyPack) -> dict[str, Any]:
    """Jurisdiction + regulatory metadata for evidence packets / shadow rows."""
    return {
        "use_case": pack.use_case,
        "jurisdiction": pack.jurisdiction,
        "regulatory_basis": pack.regulatory_basis,
        "retention_days": pack.retention_days,
        "tier_overrides": dict(pack.tier_overrides),
        "fail_stance": pack.fail_stance,
    }
