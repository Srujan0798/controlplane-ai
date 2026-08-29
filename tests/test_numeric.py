"""Numeric normalisation: Indian/Western grouping, scale words, units."""
from __future__ import annotations

from controlplane.models import Verdict
from controlplane.numeric import extract_quantities, match_numeric


def test_indian_grouping_equals_184000_inr():
    qs = extract_quantities("Refund of ₹1,84,000")
    assert any(abs(q.value - 184000) < 0.5 and q.unit == "INR" for q in qs), qs


def test_western_grouping_and_inr_suffix():
    qs = extract_quantities("Refund amount is 184,000 INR.")
    assert any(abs(q.value - 184000) < 0.5 and q.unit == "INR" for q in qs), qs


def test_bare_184000_inr():
    qs = extract_quantities("Refund amount for order ORD-9 is 184000 INR.")
    assert any(abs(q.value - 184000) < 0.5 and q.unit == "INR" for q in qs), qs


def test_lakh_and_crore_scale_words():
    lakh = extract_quantities("1.84 lakh")
    assert any(abs(q.value - 184000) < 0.5 for q in lakh), lakh
    crore = extract_quantities("2 crore")
    assert any(abs(q.value - 20_000_000) < 0.5 for q in crore), crore


def test_k_and_m_scale_suffixes():
    assert any(abs(q.value - 50_000) < 0.5 for q in extract_quantities("50k"))
    assert any(abs(q.value - 2_000_000) < 0.5 for q in extract_quantities("2M"))


def test_rupee_claim_matches_184000_inr_span():
    verdict, span_ids, rationale = match_numeric(
        "Refund of ₹1,84,000",
        {"s-amt": "Refund amount for order ORD-9 is 184000 INR."},
    )
    assert verdict == Verdict.SUPPORTED
    assert span_ids == ("s-amt",)
    assert rationale


def test_numeric_mismatch_is_contradicted():
    verdict, span_ids, rationale = match_numeric(
        "Refund of ₹1,84,000",
        {"s-amt": "Refund amount for order ORD-9 is 104000 INR."},
    )
    assert verdict == Verdict.CONTRADICTED
    assert span_ids == ("s-amt",)
    assert rationale


def test_no_quantity_in_provenance_is_unsupported():
    verdict, span_ids, _ = match_numeric(
        "Refund of ₹1,84,000",
        {"s-pol": "Clause 4.1 covers shipping delays and restocking."},
    )
    assert verdict == Verdict.UNSUPPORTED
    assert span_ids == ()


def test_clause_numbers_are_not_quantities():
    qs = extract_quantities("Clause 7.2 of the vendor agreement. Section 4.1.")
    assert qs == [], qs
