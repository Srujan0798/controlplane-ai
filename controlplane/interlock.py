from __future__ import annotations
from types import MappingProxyType
from typing import Any

from controlplane.entitlement import audit_claim
from controlplane.ledger import EvidenceLedger
from controlplane.models import (
    Action, Actuator, AssertionStrength, Binding, BlastTier, Claim, Decision,
    EntitlementFinding, EvidencePacket, Verdict,
)

# Transcribed from ARCHITECTURE.md §4. Never redraw.
COL_CONTRADICTED = "Contradicted / entitlement violation"
COL_UNSUPPORTED_CATEGORICAL = "Unsupported + categorical"
COL_UNSUPPORTED_HEDGED = "Unsupported + hedged"
COL_UNKNOWN = "Unknown"

MATRIX = MappingProxyType({
    (BlastTier.R3, COL_CONTRADICTED): Actuator.BLOCK,
    (BlastTier.R3, COL_UNSUPPORTED_CATEGORICAL): Actuator.ESCALATE,
    (BlastTier.R3, COL_UNSUPPORTED_HEDGED): Actuator.ESCALATE,
    (BlastTier.R3, COL_UNKNOWN): Actuator.ESCALATE,
    (BlastTier.R2, COL_CONTRADICTED): Actuator.BLOCK,
    (BlastTier.R2, COL_UNSUPPORTED_CATEGORICAL): Actuator.EDIT,
    (BlastTier.R2, COL_UNSUPPORTED_HEDGED): Actuator.EDIT,
    (BlastTier.R2, COL_UNKNOWN): Actuator.ESCALATE,
    (BlastTier.R1, COL_CONTRADICTED): Actuator.EDIT,
    (BlastTier.R1, COL_UNSUPPORTED_CATEGORICAL): Actuator.EDIT,
    (BlastTier.R1, COL_UNSUPPORTED_HEDGED): Actuator.PASS_ANNOTATE,
    (BlastTier.R1, COL_UNKNOWN): Actuator.PASS_ANNOTATE,
    (BlastTier.R0, COL_CONTRADICTED): Actuator.PASS_ANNOTATE,
    (BlastTier.R0, COL_UNSUPPORTED_CATEGORICAL): Actuator.PASS_ANNOTATE,
    (BlastTier.R0, COL_UNSUPPORTED_HEDGED): Actuator.PASS,
    (BlastTier.R0, COL_UNKNOWN): Actuator.PASS,
})

_SEVERITY = {
    Actuator.BLOCK: 4,
    Actuator.ESCALATE: 3,
    Actuator.EDIT: 2,
    Actuator.PASS_ANNOTATE: 1,
    Actuator.PASS: 0,
}

_COL_RANK = {
    COL_CONTRADICTED: 4,
    COL_UNSUPPORTED_CATEGORICAL: 3,
    COL_UNSUPPORTED_HEDGED: 2,
    COL_UNKNOWN: 1,
    "": 0,
}


def _column_for_claim(claim: Claim, binding: Binding, violated: bool) -> str:
    if violated or binding.verdict == Verdict.CONTRADICTED:
        return COL_CONTRADICTED
    if binding.verdict == Verdict.UNSUPPORTED and claim.assertion == AssertionStrength.CATEGORICAL:
        return COL_UNSUPPORTED_CATEGORICAL
    if binding.verdict == Verdict.UNSUPPORTED and claim.assertion == AssertionStrength.HEDGED:
        return COL_UNSUPPORTED_HEDGED
    if binding.verdict == Verdict.UNKNOWN:
        return COL_UNKNOWN
    return ""


def _actuator_for(tier: BlastTier, column: str) -> Actuator:
    if not column:
        return Actuator.PASS
    return MATRIX[(tier, column)]


def _is_fail_closed(stance: str) -> bool:
    """A closed fail-stance may not soft-Pass at irreversible blast tiers.

    Matches `closed` and the pack vocabulary `closed_escalate`. Open stances
    (e.g. `open_annotate`) never flip a matrix verdict.
    """
    return bool(stance) and stance.split("_", 1)[0] == "closed"


def decide(
    ledger: EvidenceLedger,
    action: Action,
    findings: dict[str, EntitlementFinding] | None = None,
    fail_stance: str = "closed",
) -> Decision:
    """Run the Action Interlock for one action.

    `fail_stance` is the policy pack's declared stance (default "closed" so a
    caller that omits it fails closed). A closed stance flips any pass-level
    matrix verdict (Pass / Pass+annotate) to Escalate at irreversible blast
    tiers R2/R3 — never the reverse. The MATRIX itself is never redrawn.
    """
    computed: dict[str, EntitlementFinding] = {}
    for claim_id, binding in ledger.bindings.items():
        unresolved = tuple(sid for sid in binding.span_ids if sid not in ledger.spans)
        if unresolved:
            # An ACL we cannot evaluate is not an ACL we may ignore. Skipping the
            # audit here would read as "not violated" and fail open.
            computed[claim_id] = EntitlementFinding(
                claim_id=claim_id,
                violated=True,
                offending_span_ids=unresolved,
                detail="UNRESOLVABLE_SPAN: binding cites spans absent from the ledger",
            )
        else:
            computed[claim_id] = audit_claim(ledger, claim_id)

    # Callers may supply findings, but entitlement is always on: a supplied
    # finding may raise a verdict, never clear one the plane computed itself.
    supplied = findings or {}
    findings = {}
    for claim_id, computed_finding in computed.items():
        override = supplied.get(claim_id)
        if override is not None and (override.violated or not computed_finding.violated):
            findings[claim_id] = override
        else:
            findings[claim_id] = computed_finding

    scored: list[tuple[Claim, str, Actuator]] = []
    for claim in ledger.claims.values():
        if claim.role_in_action.get(action.action_id, 0) <= 0:
            continue
        binding = ledger.bindings[claim.claim_id]
        finding = findings.get(claim.claim_id)
        violated = bool(finding and finding.violated)
        column = _column_for_claim(claim, binding, violated)
        scored.append((claim, column, _actuator_for(action.tier, column)))

    if not scored:
        # No claim carries role_in_action for this action, so nothing was proven
        # for it. Default is UNSUPPORTED, so route the absence through the frozen
        # UNKNOWN column rather than passing: R0 Pass, R1 annotate, R2/R3 Escalate.
        driving_ids: tuple[str, ...] = ()
        matrix_col = COL_UNKNOWN
        actuator = MATRIX[(action.tier, COL_UNKNOWN)]
        if actuator in (Actuator.ESCALATE, Actuator.BLOCK):
            packet: EvidencePacket | dict[str, Any] = EvidencePacket(
                claim_id="",
                claim_text="",
                verdict=Verdict.UNKNOWN.value,
                candidate_span_ids=(),
                diff=None,
                proposed_actuator=actuator.value,
                action_id=action.action_id,
                extra={"reason": "no claim carries role_in_action for this action", "claims": []},
            )
        else:
            packet: EvidencePacket | dict[str, Any] = {"claims": [], "candidate_spans": [], "diff": None}
    else:
        worst = max(_SEVERITY[a] for _, _, a in scored)
        driving = [(c, col, a) for c, col, a in scored if _SEVERITY[a] == worst]
        driving.sort(key=lambda item: (-_COL_RANK.get(item[1], 0), item[0].claim_id))
        matrix_col = driving[0][1]
        actuator = driving[0][2]
        driving_ids = tuple(c.claim_id for c, _, _ in driving)
        packet = {
            "claims": [
                {
                    "claim_id": c.claim_id,
                    "text": c.text,
                    "kind": c.kind.value,
                    "assertion": c.assertion.value,
                    "verdict": ledger.bindings[c.claim_id].verdict.value,
                    "span_ids": list(ledger.bindings[c.claim_id].span_ids),
                }
                for c, _, _ in driving
            ],
            "candidate_spans": [
                sid
                for c, _, _ in driving
                for sid in ledger.bindings[c.claim_id].span_ids
            ],
            "diff": None,
        }

    # --- Fail-stance enforcement (frozen invariant #8: fail closed) ---
    # A closed fail-stance may not soft-Pass at irreversible blast tiers. The
    # MATRIX is never redrawn; this only downgrades a pass-level verdict toward
    # Escalate (monotonic — it never relaxes a stricter matrix verdict).
    if _is_fail_closed(fail_stance) and actuator in (
        Actuator.PASS,
        Actuator.PASS_ANNOTATE,
    ):
        if action.tier in (BlastTier.R2, BlastTier.R3):
            actuator = Actuator.ESCALATE
            if isinstance(packet, dict):
                packet = {
                    **packet,
                    "fail_stance_enforced": True,
                    "fail_stance": fail_stance,
                    "reason": (
                        "closed fail-stance: irreversible blast tier "
                        "cannot soft-Pass without proof"
                    ),
                }

    decision = Decision(
        action_id=action.action_id,
        actuator=actuator,
        matrix_row=action.tier.value,
        matrix_col=matrix_col,
        driving_claim_ids=driving_ids,
        packet=packet,
    )
    ledger.actions[action.action_id] = action
    ledger.decisions[action.action_id] = decision
    ledger.append("decision", {
        "action_id": decision.action_id,
        "actuator": decision.actuator.value,
        "matrix_row": decision.matrix_row,
        "matrix_col": decision.matrix_col,
        "driving_claim_ids": list(decision.driving_claim_ids),
    })
    return decision
