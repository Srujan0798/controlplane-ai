#!/usr/bin/env python3
"""Print the frozen refund running example: same ledger, two actuators."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from controlplane.entitlement import audit_claim
from controlplane.interlock import MATRIX
from controlplane.models import BlastTier
from controlplane.scenarios.refund import UNGATED_RESPONSE, run_refund_scenario


def _acl(acl: frozenset[str]) -> str:
    return "{" + ", ".join(sorted(acl)) + "}"


def main() -> None:
    led = run_refund_scenario()
    print("ControlPlane.ai — refund running example")
    print("=" * 64)
    print()
    print("Ungated response:")
    print(f"  {UNGATED_RESPONSE}")
    print()
    print(f"Principal: {led.principal.id}")
    print(f"  roles      {_acl(led.principal.roles)}")
    print(f"  clearance  {_acl(led.principal.clearance)}")
    print(f"  policy     {led.policy_version}")
    print()

    print("--- Spans (context assembly) ---")
    for span in led.spans.values():
        step = led.steps[span.step_id]
        print(
            f"  {span.span_id:8}  {step.kind.value:9} {step.name:20} "
            f"acl={_acl(span.acl):22}  {span.source_id}"
        )
        print(f"            {span.content}")
    print()

    print("--- Claims / bindings ---")
    for claim in led.claims.values():
        binding = led.bindings[claim.claim_id]
        spans = ",".join(binding.span_ids) if binding.span_ids else "(none)"
        roles = ", ".join(
            f"{k}={v:g}" for k, v in sorted(claim.role_in_action.items())
        )
        print(
            f"  {claim.claim_id:12}  {binding.verdict.value:12}  "
            f"via {binding.method:7}  spans={spans}"
        )
        print(f"               {claim.text}")
        print(f"               kind={claim.kind.value}  assertion={claim.assertion.value}  role={roles}")
    print()

    print("--- Entitlement findings ---")
    for claim_id in led.claims:
        finding = audit_claim(led, claim_id)
        flag = "VIOLATION" if finding.violated else "ok"
        extra = (
            f"  offending={','.join(finding.offending_span_ids)}"
            if finding.offending_span_ids
            else ""
        )
        print(f"  {claim_id:12}  {flag:10}  {finding.detail}{extra}")
    print()

    print("--- Matrix cells (transcribed, never redrawn) ---")
    show = led.decisions["show_text"]
    refund = led.decisions["issue_refund"]
    for decision in (show, refund):
        key = (BlastTier(decision.matrix_row), decision.matrix_col)
        cell = MATRIX[key]
        print(
            f"  {decision.action_id:14}  {decision.matrix_row} × {decision.matrix_col}"
            f"  →  {cell.value}  (MATRIX[{decision.matrix_row!r}, {decision.matrix_col!r}])"
        )
    print()

    print("--- Decisions ---")
    for action_id in ("show_text", "issue_refund"):
        action = led.actions[action_id]
        decision = led.decisions[action_id]
        irr = " irreversible" if action.irreversibility else ""
        print(f"  {action_id}  ({action.name}, {action.tier.value}{irr})")
        print(f"    actuator   {decision.actuator.value}")
        print(f"    cell       {decision.matrix_row} × {decision.matrix_col}")
        print(f"    driving    {', '.join(decision.driving_claim_ids)}")
        packet_claims = decision.packet.get("claims") or []
        if packet_claims:
            print("    packet")
            for item in packet_claims:
                print(
                    f"      {item['claim_id']}: {item['text']!r}  "
                    f"verdict={item['verdict']}"
                )
        print()

    print("Clause 7.2 does not exist.")
    print("  Absence of evidence, not conflicting evidence — the claim stays UNSUPPORTED.")
    print("  Show text (R1 × entitlement) → Edit: the unentitled span is stripped.")
    print("  Issue refund (R3 × unsupported-categorical) → Escalate:")
    print("  held and escalated with the evidence packet.")
    print(f"  Hash chain verify_chain() = {led.verify_chain()}")


if __name__ == "__main__":
    main()
