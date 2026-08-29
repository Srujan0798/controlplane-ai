"""All 16 MATRIX cells reachable. CONTRADICTED/UNKNOWN from the production binder."""
from __future__ import annotations

import pytest

from controlplane.binder import bind_claims
from controlplane.interlock import (
    COL_CONTRADICTED,
    COL_UNKNOWN,
    COL_UNSUPPORTED_CATEGORICAL,
    COL_UNSUPPORTED_HEDGED,
    MATRIX,
    decide,
)
from controlplane.models import (
    Action,
    Actuator,
    AssertionStrength,
    BlastTier,
    Claim,
    ClaimKind,
    Principal,
    StepKind,
    Verdict,
)
from controlplane.recorder import ProvenanceRecorder

CELLS = [
    (BlastTier.R3, COL_CONTRADICTED, Actuator.BLOCK),
    (BlastTier.R3, COL_UNSUPPORTED_CATEGORICAL, Actuator.ESCALATE),
    (BlastTier.R3, COL_UNSUPPORTED_HEDGED, Actuator.ESCALATE),
    (BlastTier.R3, COL_UNKNOWN, Actuator.ESCALATE),
    (BlastTier.R2, COL_CONTRADICTED, Actuator.BLOCK),
    (BlastTier.R2, COL_UNSUPPORTED_CATEGORICAL, Actuator.EDIT),
    (BlastTier.R2, COL_UNSUPPORTED_HEDGED, Actuator.EDIT),
    (BlastTier.R2, COL_UNKNOWN, Actuator.ESCALATE),
    (BlastTier.R1, COL_CONTRADICTED, Actuator.EDIT),
    (BlastTier.R1, COL_UNSUPPORTED_CATEGORICAL, Actuator.EDIT),
    (BlastTier.R1, COL_UNSUPPORTED_HEDGED, Actuator.PASS_ANNOTATE),
    (BlastTier.R1, COL_UNKNOWN, Actuator.PASS_ANNOTATE),
    (BlastTier.R0, COL_CONTRADICTED, Actuator.PASS_ANNOTATE),
    (BlastTier.R0, COL_UNSUPPORTED_CATEGORICAL, Actuator.PASS_ANNOTATE),
    (BlastTier.R0, COL_UNSUPPORTED_HEDGED, Actuator.PASS),
    (BlastTier.R0, COL_UNKNOWN, Actuator.PASS),
]


def _fresh(request_id: str):
    rec = ProvenanceRecorder()
    led = rec.begin_request(
        request_id,
        Principal(id="u", clearance=frozenset({"public"})),
        "t",
    )
    step = rec.record_step(led, StepKind.RETRIEVAL, "ctx")
    return rec, led, step


def _bind_column(col: str, action_id: str):
    """Production binder produces the column's driving verdict."""
    rec, led, step = _fresh(f"mx-{col[:8]}")
    if col == COL_CONTRADICTED:
        rec.record_span(
            led,
            step,
            source_id="db:orders",
            acl=frozenset({"public"}),
            content="Refund amount for order ORD-9 is 104000 INR.",
        )
        rec.finish_context_assembly(led)
        claim = Claim(
            "amount",
            "Refund of ₹1,84,000",
            ClaimKind.NUMERIC,
            AssertionStrength.CATEGORICAL,
            {action_id: 1.0},
        )
        expected_verdict = Verdict.CONTRADICTED
    elif col == COL_UNSUPPORTED_CATEGORICAL:
        rec.record_span(
            led,
            step,
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
            {action_id: 1.0},
        )
        expected_verdict = Verdict.UNSUPPORTED
    elif col == COL_UNSUPPORTED_HEDGED:
        rec.record_span(
            led,
            step,
            source_id="doc:faq",
            acl=frozenset({"public"}),
            content="Shipping typically takes 5-7 business days.",
        )
        rec.finish_context_assembly(led)
        claim = Claim(
            "warranty",
            "this may still be covered under the extended warranty",
            ClaimKind.TEXTUAL,
            AssertionStrength.HEDGED,
            {action_id: 1.0},
        )
        expected_verdict = Verdict.UNSUPPORTED
    else:
        rec.record_span(
            led,
            step,
            source_id="doc:va",
            acl=frozenset({"public"}),
            content="Clause 4.1 covers shipping delays and restocking.",
        )
        rec.finish_context_assembly(led)
        claim = Claim(
            "derived",
            "The total of line items is derived from the above",
            ClaimKind.DERIVED,
            AssertionStrength.CATEGORICAL,
            {action_id: 1.0},
        )
        expected_verdict = Verdict.UNKNOWN
    binding = bind_claims(led, [claim])[0]
    assert binding.verdict == expected_verdict, (
        f"{col}: binder produced {binding.verdict} via {binding.method}"
    )
    assert "fixture" not in binding.method
    return led


@pytest.mark.parametrize("tier,col,expected", CELLS)
def test_matrix_cell_reachable_via_binder(tier, col, expected):
    action_id = f"act_{tier.value}_{abs(hash(col)) % 10_000}"
    led = _bind_column(col, action_id)
    action = Action(action_id, action_id, tier)
    decision = decide(led, action, fail_stance="open_annotate")
    assert decision.matrix_row == tier.value
    assert decision.matrix_col == col
    assert decision.actuator == expected
    assert MATRIX[(tier, col)] == expected


def test_contradicted_producer_is_numeric_binder():
    led = _bind_column(COL_CONTRADICTED, "issue")
    binding = led.bindings["amount"]
    assert binding.verdict == Verdict.CONTRADICTED
    assert "numeric" in binding.method


def test_unknown_producer_is_derived_live_bind():
    led = _bind_column(COL_UNKNOWN, "issue")
    binding = led.bindings["derived"]
    assert binding.verdict == Verdict.UNKNOWN
    assert "derived" in binding.method or binding.method == "none"


def test_every_verdict_has_a_production_producer():
    producers = {
        Verdict.SUPPORTED: None,
        Verdict.CONTRADICTED: None,
        Verdict.UNSUPPORTED: None,
        Verdict.UNKNOWN: None,
    }
    rec, led, step = _fresh("all-verdicts")
    rec.record_span(
        led,
        step,
        source_id="db:orders",
        acl=frozenset({"public"}),
        content="Refund amount for order ORD-9 is 184000 INR.",
    )
    rec.record_span(
        led,
        step,
        source_id="db:orders-wrong",
        acl=frozenset({"public"}),
        content="Other order refund is 104000 INR.",
    )
    rec.record_span(
        led,
        step,
        source_id="doc:va",
        acl=frozenset({"public"}),
        content="Clause 4.1 covers shipping delays.",
    )
    rec.finish_context_assembly(led)
    claims = [
        Claim(
            "amount",
            "Refund of ₹1,84,000",
            ClaimKind.NUMERIC,
            AssertionStrength.CATEGORICAL,
        ),
        Claim(
            "wrong",
            "Refund of ₹1,04,000",
            ClaimKind.NUMERIC,
            AssertionStrength.CATEGORICAL,
        ),
        Claim(
            "clause_72",
            "Clause 7.2 permits this refund",
            ClaimKind.STRUCTURAL,
            AssertionStrength.CATEGORICAL,
        ),
        Claim(
            "derived",
            "The total of line items is derived from the above",
            ClaimKind.DERIVED,
            AssertionStrength.CATEGORICAL,
        ),
    ]
    # Isolate CONTRADICTED: bind the 104000 claim against a 184000-only ledger.
    rec2, led2, step2 = _fresh("c-only")
    rec2.record_span(
        led2,
        step2,
        source_id="db:orders",
        acl=frozenset({"public"}),
        content="Refund amount for order ORD-9 is 184000 INR.",
    )
    rec2.finish_context_assembly(led2)
    contradicted = bind_claims(
        led2,
        [
            Claim(
                "wrong",
                "Refund of ₹2,84,000",
                ClaimKind.NUMERIC,
                AssertionStrength.CATEGORICAL,
            )
        ],
    )[0]
    producers[Verdict.CONTRADICTED] = contradicted.method

    bindings = bind_claims(led, claims)
    by_id = {b.claim_id: b for b in bindings}
    producers[Verdict.SUPPORTED] = by_id["amount"].method
    producers[Verdict.UNSUPPORTED] = by_id["clause_72"].method
    producers[Verdict.UNKNOWN] = by_id["derived"].method
    assert by_id["amount"].verdict == Verdict.SUPPORTED
    assert contradicted.verdict == Verdict.CONTRADICTED
    assert by_id["clause_72"].verdict == Verdict.UNSUPPORTED
    assert by_id["derived"].verdict == Verdict.UNKNOWN
    for verdict, method in producers.items():
        assert method and "fixture" not in method, (verdict, method)
