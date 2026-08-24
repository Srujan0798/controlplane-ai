#!/usr/bin/env python3
"""Knowledge principal-flip: same spans/claims; flip principal only → Edit vs Pass."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from controlplane.entitlement import audit_claim
from controlplane.scenarios.knowledge import CLAIM_TEXT, run_principal_flip


def _acl(acl: frozenset[str]) -> str:
    return "{" + ", ".join(sorted(acl)) + "}"


def _print_run(label: str, led) -> None:
    print(f"=== {label} ===")
    print(f"Principal: {led.principal.id}")
    print(f"  roles      {_acl(led.principal.roles)}")
    print(f"  clearance  {_acl(led.principal.clearance)}")
    span = next(iter(led.spans.values()))
    print(f"Span source: {span.source_id}  acl={_acl(span.acl)}")
    print(f"Claim: {CLAIM_TEXT}")
    binding = led.bindings["l6_band"]
    print(f"Binding: {binding.verdict.value} via {binding.method} spans={binding.span_ids}")
    finding = audit_claim(led, "l6_band")
    print(
        f"Entitlement: {'VIOLATION' if finding.violated else 'ok'} — {finding.detail}"
    )
    d = led.decisions["show_text"]
    print(
        f"Decision: {d.actuator.value}  "
        f"({d.matrix_row} × {d.matrix_col or 'clean/supported'})"
    )
    print(f"verify_chain() = {led.verify_chain()}")
    print()


def main() -> None:
    unauthorized, entitled = run_principal_flip()
    print("ControlPlane.ai — knowledge principal-flip")
    print("=" * 64)
    print("Same span (HR-COMP-L6), same claim. Only the principal changes.")
    print("Entitlement is set-membership: span.acl ⊆ principal.clearance. Zero LLM.")
    print()
    _print_run("Unauthorized (analyst_01)", unauthorized)
    _print_run("Entitled (hr_partner_01)", entitled)
    print(
        f"Flip: {unauthorized.decisions['show_text'].actuator.value} → "
        f"{entitled.decisions['show_text'].actuator.value}"
    )


if __name__ == "__main__":
    main()
