#!/usr/bin/env python3
"""Print three Round 2 use cases: same plane, three actuators."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from controlplane.interlock import MATRIX
from controlplane.ledger import EvidenceLedger
from controlplane.models import BlastTier
from controlplane.scenarios.multi_usecase import (
    run_customer_support,
    run_decision_refund,
    run_knowledge_copilot,
)


def _print_case(title: str, action_id: str, led: EvidenceLedger) -> None:
    action = led.actions[action_id]
    decision = led.decisions[action_id]
    key = (BlastTier(decision.matrix_row), decision.matrix_col)
    cell = MATRIX[key]
    claim_id = decision.driving_claim_ids[0]
    claim = led.claims[claim_id]
    binding = led.bindings[claim_id]
    print(title)
    print(f"  request    {led.request_id}")
    print(f"  action     {action_id}  ({action.name}, {action.tier.value})")
    print(f"  claim      {claim_id}: {claim.text!r}")
    print(f"             assertion={claim.assertion.value}  verdict={binding.verdict.value}")
    print(
        f"  cell       {decision.matrix_row} × {decision.matrix_col}"
        f"  →  {cell.value}"
    )
    print(f"  actuator   {decision.actuator.value}")
    print(f"  chain      verify_chain() = {led.verify_chain()}")
    print()


def main() -> None:
    print("ControlPlane.ai — three use-case fixtures")
    print("=" * 64)
    print()
    _print_case(
        "1. Customer support chatbot",
        "show_reply",
        run_customer_support(),
    )
    _print_case(
        "2. Internal knowledge copilot",
        "draft_partner_email",
        run_knowledge_copilot(),
    )
    _print_case(
        "3. Decision-support refund",
        "issue_refund",
        run_decision_refund(),
    )
    print("Same plane, three R-tiers, three actuators:")
    print("  R1 × unsupported+hedged       → Pass + annotate")
    print("  R2 × unsupported+categorical  → Edit")
    print("  R3 × unsupported+categorical  → Escalate")


if __name__ == "__main__":
    main()
