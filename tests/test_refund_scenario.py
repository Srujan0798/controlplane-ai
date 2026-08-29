import ast
from pathlib import Path

from controlplane.models import Actuator, Verdict
from controlplane.scenarios.refund import run_refund_scenario

ROOT = Path(__file__).resolve().parents[1]


def test_dual_action_edit_and_escalate():
    led = run_refund_scenario()
    assert led.decisions["show_text"].actuator == Actuator.EDIT
    assert led.decisions["issue_refund"].actuator == Actuator.ESCALATE
    assert led.verify_chain() is True


def test_clause_72_is_absence_not_contradiction():
    led = run_refund_scenario()
    binding = led.bindings["clause_72"]
    assert binding.verdict == Verdict.UNSUPPORTED
    assert binding.span_ids == ()
    assert all("7.2" not in span.content for span in led.spans.values())


def test_show_text_driven_by_entitlement():
    led = run_refund_scenario()
    d = led.decisions["show_text"]
    assert d.actuator == Actuator.EDIT
    assert d.matrix_row == "R1"
    assert d.matrix_col == "Contradicted / entitlement violation"
    assert "hr_side" in d.driving_claim_ids


def test_refund_held_not_blocked():
    led = run_refund_scenario()
    d = led.decisions["issue_refund"]
    assert d.actuator == Actuator.ESCALATE
    assert d.actuator != Actuator.BLOCK
    assert d.matrix_row == "R3"
    assert d.matrix_col == "Unsupported + categorical"
    assert d.driving_claim_ids == ("clause_72",)


def test_principal_excludes_hr_and_hr_span_is_present():
    led = run_refund_scenario()
    assert led.principal.clearance == frozenset({"vendor-public"})
    assert "hr-confidential" not in led.principal.clearance
    hr_spans = [s for s in led.spans.values() if "hr-confidential" in s.acl]
    assert len(hr_spans) == 1
    assert led.bindings["hr_side"].span_ids == (hr_spans[0].span_id,)
    assert led.bindings["amount"].verdict == Verdict.SUPPORTED


def test_refund_demo_zero_fixtures():
    led = run_refund_scenario()
    assert led.decisions["show_text"].actuator == Actuator.EDIT
    assert led.decisions["issue_refund"].actuator == Actuator.ESCALATE
    amount = led.bindings["amount"]
    assert amount.verdict == Verdict.SUPPORTED
    assert "fixture" not in amount.method
    assert "numeric" in amount.method
    assert amount.span_ids
    clause = led.bindings["clause_72"]
    assert clause.verdict == Verdict.UNSUPPORTED
    assert "fixture" not in clause.method


def _fixture_map_kw_in(path: Path, func_name: str | None = None) -> list[str]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    hits: list[str] = []
    func_ranges: list[tuple[int, int]] = []
    if func_name is not None:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                end = getattr(node, "end_lineno", node.lineno) or node.lineno
                func_ranges.append((node.lineno, end))

    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "fixture_map":
            if func_ranges and not any(
                lo <= node.lineno <= hi for lo, hi in func_ranges
            ):
                continue
            snippet = lines[node.lineno - 1].strip()
            hits.append(f"{path.name}:{node.lineno}:{snippet}")
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "fixture_map":
                if func_ranges and not any(
                    lo <= node.lineno <= hi for lo, hi in func_ranges
                ):
                    continue
                snippet = lines[node.lineno - 1].strip()
                hits.append(f"{path.name}:{node.lineno}:{snippet}")
    return hits


def test_demo_path_has_no_amount_clause_fixture_map():
    refund = ROOT / "controlplane" / "scenarios" / "refund.py"
    pipeline = ROOT / "controlplane" / "pipeline.py"
    hits = _fixture_map_kw_in(refund) + _fixture_map_kw_in(
        pipeline, func_name="_rerun_refund"
    )
    assert hits == [], "fixture_map remains on the refund demo path:\n" + "\n".join(
        hits
    )
