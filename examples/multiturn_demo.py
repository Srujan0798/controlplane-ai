#!/usr/bin/env python3
"""Multi-turn compounding risk demo.

Turn 1: a hedged claim passes at R1 (Pass + annotate).
Turn 3: the same claim is inherited into an irreversible R3 action → Escalate.

This is the same ledger pair returned by run_multiturn_compounding(); the demo
just prints it in the human-readable format judges expect to see on screen.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from controlplane.interlock import MATRIX
from controlplane.models import BlastTier
from controlplane.scenarios.multiturn import run_multiturn_compounding


def _acl(acl: frozenset[str]) -> str:
    return "{" + ", ".join(sorted(acl)) + "}"


def main() -> None:
    led1, led3 = run_multiturn_compounding()
    print("ControlPlane.ai — multi-turn compounding risk")
    print("=" * 64)
    print()
    print("Turn 1  (R1 support reply)  — hedged claim → Pass + annotate")
    print("Turn 3  (R3 irreversible refund) — same claim inherited at R3 → Escalate")
    print()

    for label, led in (("Turn 1", led1), ("Turn 3", led3)):
        print(f"--- {label}: {led.principal.id} clearance={_acl(led.principal.clearance)} ---")
        print()
        for span in led.spans.values():
            print(f"  span {span.span_id:8} acl={_acl(span.acl):22} {span.content[:56]}")
        print()
        for action_id in led.decisions:
            dec = led.decisions[action_id]
            key = (BlastTier(dec.matrix_row), dec.matrix_col)
            cell = MATRIX[key]
            print(f"  {action_id:14} {dec.matrix_row} × {dec.matrix_col} → {cell.value}")
            print(f"    actuator  {dec.actuator.value}")
            print(f"    driving   {', '.join(dec.driving_claim_ids)}")
        print(f"  chain_valid = {led.verify_chain()}")
        print()

    print("Key: hedging is not consent.")
    print("  Turn 1: 'this may be covered' → insufficient grounding for R1 info reply → Pass+annotate")
    print("  Turn 3: same claim inherits full weight into R3 irreversible → Escalate (held, packet)")

    print()
    print("Inherited claim chain:")
    print(f"  Turn 3 driving claims: {led3.decisions['issue_refund'].driving_claim_ids}")
    assert "warranty_hedge" in led3.decisions["issue_refund"].driving_claim_ids


if __name__ == "__main__":
    main()
