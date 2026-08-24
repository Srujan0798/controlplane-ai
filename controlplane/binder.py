from __future__ import annotations

from controlplane.ledger import EvidenceLedger
from controlplane.models import Binding, Claim, ClaimKind, Verdict


def bind_claims(
    ledger: EvidenceLedger,
    claims: list[Claim],
    fixture_map: dict[str, tuple[str, ...] | None] | None = None,
) -> list[Binding]:
    """Bind claims to provenance spans. Default verdict is UNSUPPORTED.

    - DERIVED claims without an explicit fixture → UNKNOWN (never SUPPORTED by shallow match)
    - fixture_map[claim_id] = None or () → force UNSUPPORTED
    - fixture_map[claim_id] = span ids → SUPPORTED via fixture
    - else exact/substring against provenance set only; no match → UNSUPPORTED
    """
    fixture_map = fixture_map or {}
    results: list[Binding] = []
    for claim in claims:
        ledger.claims[claim.claim_id] = claim
        if claim.kind == ClaimKind.DERIVED and claim.claim_id not in fixture_map:
            binding = Binding(claim.claim_id, (), "none", Verdict.UNKNOWN)
        elif claim.claim_id in fixture_map:
            span_ids = fixture_map[claim.claim_id]
            if span_ids:
                binding = Binding(
                    claim.claim_id, tuple(span_ids), "fixture", Verdict.SUPPORTED
                )
            else:
                binding = Binding(
                    claim.claim_id, (), "fixture", Verdict.UNSUPPORTED
                )
        else:
            hits = tuple(
                s.span_id
                for s in ledger.spans.values()
                if claim.text.lower() in s.content.lower()
                or s.content.lower() in claim.text.lower()
            )
            if hits:
                binding = Binding(claim.claim_id, hits, "exact", Verdict.SUPPORTED)
            else:
                binding = Binding(claim.claim_id, (), "none", Verdict.UNSUPPORTED)
        ledger.bindings[claim.claim_id] = binding
        ledger.append(
            "binding",
            {
                "claim_id": binding.claim_id,
                "span_ids": list(binding.span_ids),
                "method": binding.method,
                "verdict": binding.verdict.value,
            },
        )
        results.append(binding)
    return results
