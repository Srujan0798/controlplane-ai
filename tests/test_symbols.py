"""Structural symbol table: clause/section/ID lookup, not search."""
from __future__ import annotations

from controlplane.models import (
    AssertionStrength,
    Claim,
    ClaimKind,
    Principal,
    StepKind,
    Verdict,
)
from controlplane.recorder import ProvenanceRecorder
from controlplane.symbols import build_symbol_table, extract_symbols, lookup_symbols


def test_extract_clause_section_and_order_id():
    text = (
        "Clause 4.1 covers shipping. Section 4.3 and §9.1 apply. "
        "Refund amount for order ORD-9 is 184000 INR."
    )
    symbols = set(extract_symbols(text))
    assert "4.1" in symbols
    assert "4.3" in symbols
    assert "9.1" in symbols
    assert "ORD-9" in symbols
    assert "7.2" not in symbols


def test_refund_like_table_lists_41_not_72():
    table = build_symbol_table(
        {
            "s-va": (
                "Clause 4.1 covers shipping delays and restocking. "
                "Section 4.3 and §9.1 apply. Approved refunds follow the "
                "published vendor schedule."
            ),
            "s-ord": "Refund amount for order ORD-9 is 184000 INR.",
        }
    )
    keys = set(table)
    assert "4.1" in keys
    assert "4.3" in keys
    assert "9.1" in keys
    assert "ORD-9" in keys
    assert "7.2" not in keys
    assert table["4.1"] == ("s-va",)


def test_lookup_hit_and_miss():
    table = build_symbol_table(
        {"s-va": "Clause 4.1 covers shipping delays and restocking."}
    )
    assert lookup_symbols("Clause 4.1 covers shipping delays", table) == ("s-va",)
    assert lookup_symbols("Clause 7.2 permits this refund", table) == ()


def test_structural_bind_miss_is_unsupported():
    from controlplane.binder import bind_claims

    rec = ProvenanceRecorder()
    led = rec.begin_request(
        "r", Principal(id="u", clearance=frozenset({"public"})), "t"
    )
    sid = rec.record_step(led, StepKind.RETRIEVAL, "va")
    rec.record_span(
        led,
        sid,
        source_id="doc:va",
        acl=frozenset({"public"}),
        content="Clause 4.1 covers shipping delays and restocking.",
    )
    rec.finish_context_assembly(led)
    claim = Claim(
        "clause_72",
        "Clause 7.2 permits this refund",
        ClaimKind.STRUCTURAL,
        AssertionStrength.CATEGORICAL,
    )
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == Verdict.UNSUPPORTED
    assert binding.span_ids == ()
    assert "fixture" not in binding.method
