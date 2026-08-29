"""Dead-compute accountant — steps that ground zero accepted claims.

ARCHITECTURE §12: the most defensible number. Exact backward walk:
accepted claims → bindings → spans → steps.
"""
from __future__ import annotations

from typing import Any

from controlplane.ledger import EvidenceLedger
from controlplane.models import Verdict


def analyze_dead_compute(
    ledger: EvidenceLedger,
    *,
    inr_per_1k_tokens: float = 0.5,
    requests_normalize: int = 1000,
) -> dict[str, Any]:
    """Report dead vs live steps and a ₹ estimate at a stated rate."""
    accepted_span_ids: set[str] = set()
    for claim_id, binding in ledger.bindings.items():
        if binding.verdict == Verdict.SUPPORTED:
            accepted_span_ids.update(binding.span_ids)

    live_step_ids: set[str] = set()
    for sid in accepted_span_ids:
        span = ledger.spans.get(sid)
        if span is not None:
            live_step_ids.add(span.step_id)

    dead_steps: list[dict[str, Any]] = []
    live_steps: list[dict[str, Any]] = []
    token_dead = 0
    token_live = 0

    for step in ledger.steps.values():
        step_spans = [s for s in ledger.spans.values() if s.step_id == step.step_id]
        tokens = sum(max(1, len(s.content) // 4) for s in step_spans)
        entry = {
            "step_id": step.step_id,
            "name": step.name,
            "kind": step.kind.value,
            "span_count": len(step_spans),
            "token_estimate": tokens,
        }
        if step.step_id in live_step_ids:
            live_steps.append(entry)
            token_live += tokens
        else:
            # Context-assembly steps with spans that never support a claim.
            if step_spans:
                dead_steps.append(entry)
                token_dead += tokens

    inr_dead = (token_dead / 1000.0) * inr_per_1k_tokens
    return {
        "dead_step_count": len(dead_steps),
        "live_step_count": len(live_steps),
        "dead_steps": dead_steps,
        "live_steps": live_steps,
        "token_estimate_dead": token_dead,
        "token_estimate_live": token_live,
        "rate_inr_per_1k_tokens": inr_per_1k_tokens,
        "inr_estimate_dead": round(inr_dead, 6),
        "inr_per_1k_requests": round(inr_dead * requests_normalize, 4),
        "methodology": (
            "Dead steps = retrieval/tool/db steps whose spans ground zero "
            "SUPPORTED claims. Token estimate = len(content)//4. "
            f"₹ rate stated explicitly: {inr_per_1k_tokens} INR / 1k tokens."
        ),
    }
