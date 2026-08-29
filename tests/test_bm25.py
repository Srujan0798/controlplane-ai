"""Pure-Python BM25 over the provenance set + lexical-entailment gate."""
from __future__ import annotations

from controlplane.bm25 import (
    COVERAGE_SUPPORTED,
    COVERAGE_UNKNOWN,
    bind_textual,
    lexical_gate,
    rank,
)
from controlplane.models import Verdict

DOCS = [
    ("s-faq", "Return window is 30 days for unused goods."),
    (
        "s-hr",
        "Internal exception desk: customer account flagged for goodwill override.",
    ),
    (
        "s-va",
        "Clause 4.1 covers shipping delays and restocking. "
        "Approved refunds follow the published vendor schedule.",
    ),
]


def test_thresholds_are_named_constants():
    assert isinstance(COVERAGE_SUPPORTED, float)
    assert isinstance(COVERAGE_UNKNOWN, float)
    assert 0 < COVERAGE_UNKNOWN < COVERAGE_SUPPORTED <= 1


def test_ranks_goodwill_span_first():
    ranked = rank("customer account flagged for goodwill override", DOCS)
    assert ranked
    assert ranked[0][0] == "s-hr"


def test_high_coverage_supported():
    verdict, coverage, _ = lexical_gate(
        "customer account flagged for goodwill override",
        "Internal exception desk: customer account flagged for goodwill override.",
    )
    assert verdict == Verdict.SUPPORTED
    assert coverage >= COVERAGE_SUPPORTED


def test_middle_band_unknown():
    verdict, coverage, _ = lexical_gate(
        "the published vendor schedule covers restocking delays",
        "Approved refunds follow the published vendor schedule.",
    )
    assert COVERAGE_UNKNOWN <= coverage < COVERAGE_SUPPORTED, coverage
    assert verdict == Verdict.UNKNOWN


def test_low_coverage_unsupported():
    verdict, coverage, _ = lexical_gate(
        "this may still be covered under the extended warranty",
        "Shipping typically takes 5-7 business days.",
    )
    assert coverage < COVERAGE_UNKNOWN, coverage
    assert verdict == Verdict.UNSUPPORTED


def test_negation_contradicted():
    verdict, _, _ = lexical_gate(
        "the policy permits this refund",
        "the policy does not permit this refund",
    )
    assert verdict == Verdict.CONTRADICTED


def test_bind_textual_three_bands_and_negation():
    supported, hits, _ = bind_textual(
        "customer account flagged for goodwill override",
        {d[0]: d[1] for d in DOCS},
    )
    assert supported == Verdict.SUPPORTED
    assert hits[0] == "s-hr"

    unknown, _, _ = bind_textual(
        "the published vendor schedule covers restocking delays",
        {"s-va": "Approved refunds follow the published vendor schedule."},
    )
    assert unknown == Verdict.UNKNOWN

    contradicted, _, _ = bind_textual(
        "the policy permits this refund",
        {"s-neg": "the policy does not permit this refund"},
    )
    assert contradicted == Verdict.CONTRADICTED
