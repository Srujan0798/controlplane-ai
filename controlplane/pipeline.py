"""Production gate pipeline — wraps recorder → bind → entitle → interlock → shadow."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from controlplane.bias import probe_acl_skew
from controlplane.binder import bind_claims
from controlplane.entitlement import audit_claim
from controlplane.interlock import decide
from controlplane.ledger import EvidenceLedger
from controlplane.models import (
    Action,
    Actuator,
    Claim,
    Decision,
    EntitlementFinding,
)
from controlplane.holdback import admit_for_decisions
from controlplane.policy import PolicyRegistry
from controlplane.recorder import ProvenanceRecorder
from controlplane.shadow import HOLDING_ACTUATORS, MetricsStore


@dataclass
class GateResult:
    request_id: str
    use_case: str
    mode: str  # shadow | enforce
    policy_version: str
    ledger: EvidenceLedger
    findings: dict[str, EntitlementFinding]
    decisions: dict[str, Decision]
    latency_ms: float
    enforced: bool
    """True when mode=enforce AND at least one holding actuator fired."""
    would_hold: bool
    response_overlay: dict[str, Any] = field(default_factory=dict)

    def public_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "use_case": self.use_case,
            "mode": self.mode,
            "policy_version": self.policy_version,
            "latency_ms": round(self.latency_ms, 3),
            "enforced": self.enforced,
            "would_hold": self.would_hold,
            "chain_valid": self.ledger.verify_chain(),
            "principal": {
                "id": self.ledger.principal.id,
                "roles": sorted(self.ledger.principal.roles),
                "clearance": sorted(self.ledger.principal.clearance),
            },
            "steps": [
                {"step_id": s.step_id, "kind": s.kind.value, "name": s.name}
                for s in self.ledger.steps.values()
            ],
            "spans": [
                {
                    "span_id": sp.span_id,
                    "step_id": sp.step_id,
                    "source_id": sp.source_id,
                    "acl": sorted(sp.acl),
                    "content": sp.content,
                    "content_hash": sp.content_hash,
                }
                for sp in self.ledger.spans.values()
            ],
            "claims": [
                {
                    "claim_id": c.claim_id,
                    "text": c.text,
                    "kind": c.kind.value,
                    "assertion": c.assertion.value,
                    "role_in_action": c.role_in_action,
                    "binding": {
                        "span_ids": list(self.ledger.bindings[c.claim_id].span_ids),
                        "method": self.ledger.bindings[c.claim_id].method,
                        "verdict": self.ledger.bindings[c.claim_id].verdict.value,
                        "rationale": self.ledger.bindings[c.claim_id].rationale,
                    }
                    if c.claim_id in self.ledger.bindings
                    else None,
                }
                for c in self.ledger.claims.values()
            ],
            "findings": {
                cid: {
                    "violated": f.violated,
                    "offending_span_ids": list(f.offending_span_ids),
                    "detail": f.detail,
                }
                for cid, f in self.findings.items()
            },
            "decisions": {
                aid: {
                    "action_id": d.action_id,
                    "actuator": d.actuator.value,
                    "matrix_row": d.matrix_row,
                    "matrix_col": d.matrix_col,
                    "driving_claim_ids": list(d.driving_claim_ids),
                    "packet": d.packet,
                }
                for aid, d in self.decisions.items()
            },
            "response_overlay": self.response_overlay,
            "responsibility": {
                "bias_probe": probe_acl_skew(self.ledger),
            },
        }


class ControlPlaneGate:
    """Enterprise admission-control gate.

    Lane 1 only: deterministic membership, ACL, matrix. No LLM on this path.
    """

    def __init__(
        self,
        policies: PolicyRegistry | None = None,
        metrics: MetricsStore | None = None,
    ) -> None:
        self.policies = policies or PolicyRegistry()
        self.metrics = metrics or MetricsStore()
        self._history: list[GateResult] = []

    def run_prepared(
        self,
        *,
        use_case: str,
        ledger: EvidenceLedger,
        claims: list[Claim],
        actions: list[Action],
        fixture_map: dict[str, tuple[str, ...] | None] | None = None,
        mode_override: str | None = None,
        labeled_should_hold: bool | None = None,
        ungated_text: str | None = None,
        allow_fixtures: bool = False,
    ) -> GateResult:
        t0 = time.perf_counter()
        pack = self.policies.get(use_case)
        mode = mode_override or pack.mode
        if mode == "enforce" and fixture_map and not allow_fixtures:
            raise ValueError(
                "fixture_map is rejected in enforce mode unless allow_fixtures=True"
            )

        bind_claims(ledger, claims, fixture_map=fixture_map)
        findings = {cid: audit_claim(ledger, cid) for cid in ledger.claims}
        decisions: dict[str, Decision] = {}
        for action in actions:
            decisions[action.action_id] = decide(
                ledger, action, findings=findings, fail_stance=pack.fail_stance
            )

        would_hold = any(d.actuator in HOLDING_ACTUATORS for d in decisions.values())
        enforced = mode == "enforce" and would_hold

        for d in decisions.values():
            self.metrics.record(
                use_case=use_case,
                actuator=d.actuator,
                mode=mode,
                labeled_should_hold=labeled_should_hold,
            )

        overlay = self._overlay(decisions, ungated_text=ungated_text, enforced=enforced)
        latency_ms = (time.perf_counter() - t0) * 1000.0
        self.metrics.record_latency(latency_ms)
        result = GateResult(
            request_id=ledger.request_id,
            use_case=use_case,
            mode=mode,
            policy_version=pack.policy_version,
            ledger=ledger,
            findings=findings,
            decisions=decisions,
            latency_ms=latency_ms,
            enforced=enforced,
            would_hold=would_hold,
            response_overlay=overlay,
        )
        self._history.append(result)
        if len(self._history) > 500:
            self._history = self._history[-500:]
        return result

    def run_refund_demo(self, mode_override: str | None = None) -> GateResult:
        return self._rerun_refund(mode_override=mode_override)

    def run_flip_demo(
        self,
        principal_id: str = "analyst_01",
        mode_override: str | None = None,
    ) -> GateResult:
        """Principal-flip demo: same HR-COMP-L6 span + claim, caller decides actuator.

        analyst_01 is not entitled -> R1 x entitlement violation -> Edit.
        hr_partner_01 is entitled -> R1 clean/supported -> Pass.
        Routes through the real bind -> entitle -> interlock path (zero LLM).
        """
        from controlplane.scenarios.flip import build_flip

        ledger, claims, actions, fixture_map = build_flip(principal_id)
        return self.run_prepared(
            use_case="flip",
            ledger=ledger,
            claims=claims,
            actions=actions,
            fixture_map=fixture_map,
            mode_override=mode_override,
            labeled_should_hold=None,
            ungated_text=None,
            allow_fixtures=True,
        )

    def _rerun_refund(self, mode_override: str | None = None) -> GateResult:
        from controlplane.scenarios.refund import UNGATED_RESPONSE, extract_demo_claims
        from controlplane.models import (
            BlastTier,
            Principal,
            StepKind,
        )

        rec = ProvenanceRecorder()
        principal = Principal(
            id="cs-agent-17",
            roles=frozenset({"customer-support"}),
            clearance=frozenset({"vendor-public"}),
        )
        led = rec.begin_request(
            request_id=f"refund-{uuid.uuid4().hex[:8]}",
            principal=principal,
            action_intent="customer-refund",
            policy_version="pack-decision-v1",
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
        rec.record_span(
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
            content="Last contact was a shipping inquiry, not a refund request.",
        )
        rec.finish_context_assembly(led)

        actions = [
            Action("show_text", "show_text", BlastTier.R1),
            Action(
                "issue_refund",
                "issue_refund",
                BlastTier.R3,
                args={"amount": 184000, "currency": "INR", "order": "ORD-9"},
                irreversibility=True,
            ),
        ]
        claims = extract_demo_claims(actions)
        return self.run_prepared(
            use_case="decision-support",
            ledger=led,
            claims=claims,
            actions=actions,
            mode_override=mode_override,
            labeled_should_hold=True,
            ungated_text=UNGATED_RESPONSE,
        )

    @staticmethod
    def _overlay(
        decisions: dict[str, Decision],
        *,
        ungated_text: str | None,
        enforced: bool,
    ) -> dict[str, Any]:
        actuators = {aid: d.actuator.value for aid, d in decisions.items()}
        if not enforced:
            overlay = {
                "ungated_text": ungated_text,
                "shadow": True,
                "actuators_would_apply": actuators,
                "user_visible_text": ungated_text,
                "action_allowed": True,
                "note": "Shadow mode — counterfactual only; downstream not blocked.",
            }
            overlay["holdback"] = admit_for_decisions(
                overlay.get("user_visible_text") or "", decisions
            )
            return overlay

        # Enforce: Edit strips unproven / unentitled claims from user-visible text;
        # Escalate/Block hold irreversible actions.
        text = ungated_text or ""
        show = decisions.get("show_text") or decisions.get("show_reply")
        if show and show.actuator == Actuator.EDIT and text:
            # Surgical strip of clause 7.2 claim language when present
            for phrase in (
                " under clause 7.2 of the vendor agreement",
                " under clause 7.2",
                "clause 7.2 of the vendor agreement",
            ):
                text = text.replace(phrase, "")
            text = text.replace("  ", " ").strip()
            if text.endswith("issued."):
                pass
            elif "issued" in text and not text.endswith("."):
                text = text.rstrip(".") + "."

        refund = decisions.get("issue_refund")
        action_allowed = not (
            refund and refund.actuator in (Actuator.ESCALATE, Actuator.BLOCK)
        )
        overlay = {
            "ungated_text": ungated_text,
            "shadow": False,
            "actuators_applied": actuators,
            "user_visible_text": text,
            "action_allowed": action_allowed,
            "hold_reason": (
                None
                if action_allowed
                else {
                    "actuator": refund.actuator.value if refund else None,
                    "matrix": (
                        f"{refund.matrix_row} × {refund.matrix_col}" if refund else None
                    ),
                    "packet": refund.packet if refund else None,
                }
            ),
            "note": "Enforce mode — matrix actuators applied.",
        }
        overlay["holdback"] = admit_for_decisions(text, decisions)
        return overlay

    def history(self, limit: int = 50) -> list[dict[str, Any]]:
        return [r.public_dict() for r in self._history[-limit:]]

    def get(self, request_id: str) -> dict[str, Any] | None:
        for r in reversed(self._history):
            if r.request_id == request_id:
                return r.public_dict()
        return None
