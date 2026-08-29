"""Claim → span binding. Four routes; default verdict UNSUPPORTED.

`bind_claims(ledger, claims, fixture_map=...)` signature is unchanged.
fixture_map remains a test hook; production demo paths omit it.
"""
from __future__ import annotations

from controlplane.bm25 import bind_textual
from controlplane.ledger import EvidenceLedger
from controlplane.models import Binding, Claim, ClaimKind, Verdict
from controlplane.numeric import match_numeric, recompute_derived
from controlplane.symbols import build_symbol_table, match_structural


def _fixture_binding(claim: Claim, span_ids: tuple[str, ...] | None, ledger: EvidenceLedger) -> Binding:
    if span_ids:
        unresolved = tuple(sid for sid in span_ids if sid not in ledger.spans)
        if unresolved:
            return Binding(
                claim.claim_id,
                (),
                "fixture-unresolved",
                Verdict.UNSUPPORTED,
                "fixture cites spans absent from the ledger",
            )
        return Binding(
            claim.claim_id,
            tuple(span_ids),
            "fixture",
            Verdict.SUPPORTED,
            "fixture override (tests only)",
        )
    return Binding(
        claim.claim_id,
        (),
        "fixture",
        Verdict.UNSUPPORTED,
        "fixture asserted absence",
    )


def _route(
    claim: Claim,
    span_texts: dict[str, str],
    table: dict[str, tuple[str, ...]],
) -> Binding:
    if claim.kind == ClaimKind.NUMERIC:
        verdict, span_ids, rationale = match_numeric(claim.text, span_texts)
        return Binding(claim.claim_id, span_ids, "numeric", verdict, rationale)
    if claim.kind == ClaimKind.STRUCTURAL:
        verdict, span_ids, rationale = match_structural(claim.text, table)
        return Binding(claim.claim_id, span_ids, "structural", verdict, rationale)
    if claim.kind == ClaimKind.DERIVED:
        verdict, span_ids, rationale = recompute_derived(claim.text, span_texts)
        return Binding(claim.claim_id, span_ids, "derived", verdict, rationale)
    if claim.kind == ClaimKind.TEMPORAL:
        verdict, span_ids, rationale = bind_textual(claim.text, span_texts)
        return Binding(
            claim.claim_id,
            span_ids,
            "temporal/textual",
            verdict,
            rationale or "temporal: fell through to textual",
        )
    verdict, span_ids, rationale = bind_textual(claim.text, span_texts)
    return Binding(claim.claim_id, span_ids, "bm25+lexical", verdict, rationale)


def bind_claims(
    ledger: EvidenceLedger,
    claims: list[Claim],
    fixture_map: dict[str, tuple[str, ...] | None] | None = None,
) -> list[Binding]:
    fixture_map = fixture_map or {}
    span_texts = {sid: sp.content for sid, sp in ledger.spans.items()}
    table = build_symbol_table(span_texts)
    results: list[Binding] = []
    for claim in claims:
        ledger.claims[claim.claim_id] = claim
        if claim.claim_id in fixture_map:
            binding = _fixture_binding(claim, fixture_map[claim.claim_id], ledger)
        else:
            binding = _route(claim, span_texts, table)
        ledger.bindings[claim.claim_id] = binding
        ledger.append(
            "binding",
            {
                "claim_id": binding.claim_id,
                "span_ids": list(binding.span_ids),
                "method": binding.method,
                "verdict": binding.verdict.value,
                "rationale": binding.rationale,
            },
        )
        results.append(binding)
    return results
