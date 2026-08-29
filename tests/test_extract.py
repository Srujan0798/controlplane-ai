"""Phase 1: arbitrary response text → typed Claim list.

Assert by kind + substring, not brittle hand ids, except where the
extractor publishes a documented readable slug (amount, clause_72).
"""
from __future__ import annotations

import ast
from pathlib import Path

from controlplane.extract import extract_claims, segment
from controlplane.models import (
    Action,
    AssertionStrength,
    BlastTier,
    ClaimKind,
)
from controlplane.scenarios.refund import UNGATED_RESPONSE

ROOT = Path(__file__).resolve().parents[1]

_REFUND_ACTIONS = [
    Action("show_text", "Show text to the customer", BlastTier.R1),
    Action(
        "issue_refund",
        "Issue the refund",
        BlastTier.R3,
        args={"amount": 184000, "currency": "INR", "order": "ORD-9"},
        irreversibility=True,
    ),
]


def test_segment_survives_indian_amount_and_clause():
    text = (
        "Refund of ₹1,84,000. Clause 7.2 applies. "
        "See §4.1 and Dr. Rao (e.g. 3.14)."
    )
    sents = segment(text)
    blob = " ".join(sents)
    assert "₹1,84,000" in blob
    assert any("₹1,84,000" in s for s in sents)
    assert not any(s.strip() in {"1", "84", "000", "7", "2"} for s in sents)
    assert any("Clause 7.2" in s for s in sents)
    assert any("§4.1" in s for s in sents)
    assert any("Dr. Rao" in s for s in sents)
    assert any("e.g." in s for s in sents)
    assert any("3.14" in s for s in sents)
    # Trailing period after the Indian amount is a sentence boundary, not a split
    # inside the amount itself.
    first = next(s for s in sents if "₹1,84,000" in s)
    assert "Clause 7.2" not in first


def test_filter_drops_greeting_keeps_quantity():
    claims = extract_claims("Hello! The refund is ₹1,84,000.")
    assert not any("hello" in c.text.lower() for c in claims)
    assert any(
        "1,84,000" in c.text or "₹" in c.text for c in claims
    ), [c.text for c in claims]


def test_typing_precedence_numeric_over_textual():
    claims = extract_claims("Refund of ₹1,84,000 was processed.")
    numeric = [c for c in claims if c.kind == ClaimKind.NUMERIC]
    assert numeric
    assert any("1,84,000" in c.text or "₹" in c.text for c in numeric)


def test_typing_structural_clause():
    claims = extract_claims("Clause 7.2 of the vendor agreement.")
    assert any(
        c.kind == ClaimKind.STRUCTURAL and "7.2" in c.text for c in claims
    ), [c.text for c in claims]


def test_hedge_detection():
    hedged = extract_claims("The policy may permit this refund.")
    categorical = extract_claims("The policy permits this refund.")
    assert any(c.assertion == AssertionStrength.HEDGED for c in hedged), [
        (c.text, c.assertion) for c in hedged
    ]
    assert categorical
    assert all(c.assertion == AssertionStrength.CATEGORICAL for c in categorical)


def test_derived_not_mistyped_as_numeric():
    claims = extract_claims("The total of the above is ₹1,84,000.")
    assert any(c.kind == ClaimKind.DERIVED for c in claims), [
        (c.text, c.kind) for c in claims
    ]
    assert not any(c.kind == ClaimKind.NUMERIC for c in claims)

    summed = extract_claims("The sum of line items is ₹500.")
    assert any(c.kind == ClaimKind.DERIVED for c in summed)
    assert not any(c.kind == ClaimKind.NUMERIC for c in summed)


def test_role_in_action_from_action_args():
    action = Action(
        "issue_refund",
        "Issue the refund",
        BlastTier.R3,
        args={"amount": 184000, "currency": "INR", "order": "ORD-9"},
        irreversibility=True,
    )
    claims = extract_claims("Refund of ₹1,84,000 issued.", actions=[action])
    amount_claims = [c for c in claims if c.kind == ClaimKind.NUMERIC]
    assert amount_claims
    assert any(c.role_in_action.get("issue_refund", 0) > 0 for c in amount_claims), [
        (c.text, c.role_in_action) for c in amount_claims
    ]


def test_refund_ungated_extraction_exit_gate():
    claims = extract_claims(UNGATED_RESPONSE, actions=_REFUND_ACTIONS)
    assert any(
        c.kind == ClaimKind.NUMERIC
        and ("1,84,000" in c.text or "184000" in c.text or "₹" in c.text)
        for c in claims
    ), [(c.kind, c.text) for c in claims]
    clause = [
        c
        for c in claims
        if c.kind == ClaimKind.STRUCTURAL and "7.2" in c.text
    ]
    assert clause, [(c.kind, c.text) for c in claims]
    assert any(
        c.kind in (ClaimKind.TEXTUAL, ClaimKind.STRUCTURAL)
        and any(token in c.text.lower() for token in ("approv", "issued"))
        for c in claims
    ), [(c.kind, c.text) for c in claims]
    amount = next(c for c in claims if c.kind == ClaimKind.NUMERIC)
    assert amount.role_in_action.get("issue_refund", 0) > 0, amount.role_in_action
    assert any(c.role_in_action.get("issue_refund", 0) > 0 for c in clause), [
        c.role_in_action for c in clause
    ]


def _claim_calls(path: Path, *, func_name: str | None = None) -> list[str]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    hits: list[str] = []

    func_ranges: list[tuple[int, int]] = []
    if func_name is not None:
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                end = getattr(node, "end_lineno", node.lineno) or node.lineno
                func_ranges.append((node.lineno, end))
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == func_name:
                        end = getattr(item, "end_lineno", item.lineno) or item.lineno
                        func_ranges.append((item.lineno, end))

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = None
        if isinstance(func, ast.Name):
            name = func.id
        elif isinstance(func, ast.Attribute):
            name = func.attr
        if name != "Claim":
            continue
        if func_ranges and not any(lo <= node.lineno <= hi for lo, hi in func_ranges):
            continue
        snippet = lines[node.lineno - 1].strip() if 0 < node.lineno <= len(lines) else ""
        hits.append(f"{path.name}:{node.lineno}:{snippet}")
    return hits


def test_demo_path_has_no_claim_literals():
    refund = ROOT / "controlplane" / "scenarios" / "refund.py"
    pipeline = ROOT / "controlplane" / "pipeline.py"
    hits = _claim_calls(refund) + _claim_calls(pipeline, func_name="_rerun_refund")
    assert hits == [], "Claim() literals remain in the refund demo path:\n" + "\n".join(
        hits
    )
