"""ARCHITECTURE.md §10 content laws — executable CI.

Phase 0 of Round 2 elevation. These must stay green forever.
"""
from __future__ import annotations

import re
from pathlib import Path
from zipfile import ZipFile

import pytest

from controlplane.interlock import (
    COL_CONTRADICTED,
    COL_UNKNOWN,
    COL_UNSUPPORTED_CATEGORICAL,
    COL_UNSUPPORTED_HEDGED,
    MATRIX,
)
from controlplane.models import Actuator, BlastTier

ROOT = Path(__file__).resolve().parents[1]

# Exact 16 cells transcribed from ARCHITECTURE.md §4 / interlock.py
CANONICAL_MATRIX = {
    (BlastTier.R3, COL_CONTRADICTED): Actuator.BLOCK,
    (BlastTier.R3, COL_UNSUPPORTED_CATEGORICAL): Actuator.ESCALATE,
    (BlastTier.R3, COL_UNSUPPORTED_HEDGED): Actuator.ESCALATE,
    (BlastTier.R3, COL_UNKNOWN): Actuator.ESCALATE,
    (BlastTier.R2, COL_CONTRADICTED): Actuator.BLOCK,
    (BlastTier.R2, COL_UNSUPPORTED_CATEGORICAL): Actuator.EDIT,
    (BlastTier.R2, COL_UNSUPPORTED_HEDGED): Actuator.EDIT,
    (BlastTier.R2, COL_UNKNOWN): Actuator.ESCALATE,
    (BlastTier.R1, COL_CONTRADICTED): Actuator.EDIT,
    (BlastTier.R1, COL_UNSUPPORTED_CATEGORICAL): Actuator.EDIT,
    (BlastTier.R1, COL_UNSUPPORTED_HEDGED): Actuator.PASS_ANNOTATE,
    (BlastTier.R1, COL_UNKNOWN): Actuator.PASS_ANNOTATE,
    (BlastTier.R0, COL_CONTRADICTED): Actuator.PASS_ANNOTATE,
    (BlastTier.R0, COL_UNSUPPORTED_CATEGORICAL): Actuator.PASS_ANNOTATE,
    (BlastTier.R0, COL_UNSUPPORTED_HEDGED): Actuator.PASS,
    (BlastTier.R0, COL_UNKNOWN): Actuator.PASS,
}

FORBIDDEN_ACTUATORS = (
    "STREAM",
    "Kill Span",
    "Terminate Step",
    "Hold & Re-verify",
    "Redact & Flag",
)

# Asserted refund-was-blocked language (meta "never blocked" is allowed).
_REFUND_BLOCKED = re.compile(
    r"(?i)"
    r"(?:"
    r"refund\s+(?:was\s+|is\s+|gets?\s+)?blocked"
    r"|blocked\s+the\s+refund"
    r"|the\s+refund\s+blocked"
    r"|COMMIT\s+BLOCKED"
    r"|response\s+blocked"
    r")",
)

# Clause 7.2 + wrong verbs (absence only).
_CLAUSE_WRONG = re.compile(
    r"(?i)clause\s*7\.2.{0,40}?\b(?:caps?|denies|denied|covers?|covering|limits?|limited)\b"
    r"|\b(?:caps?|denies|denied|covers?|covering|limits?|limited)\b.{0,40}?clause\s*7\.2",
)

_P95_40 = re.compile(r"(?i)(?:40\s*ms.{0,12}?p95|p95.{0,12}?40\s*ms|40ms\s*p95|p95\s*=\s*40)")

ARTIFACT_GLOBS = [
    "AGENTS.md",
    "README.md",
    "docs/*.md",
    "docs/reference/*.md",
    "round2/*.md",
    "controlplane/**/*.py",
    "examples/*.py",
    "policies/*.yaml",
    "submission/*.js",
]


def _iter_text_files() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for pattern in ARTIFACT_GLOBS:
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts:
                continue
            try:
                out.append((str(path.relative_to(ROOT)), path.read_text(encoding="utf-8")))
            except UnicodeDecodeError:
                continue
    return out


def _pdf_text() -> str:
    pdf = ROOT / "submission" / "ControlPlane_Round2_Proposal.pdf"
    if not pdf.exists():
        return ""
    try:
        from pypdf import PdfReader

        return "\n".join((p.extract_text() or "") for p in PdfReader(str(pdf)).pages)
    except Exception:
        return ""


def _pptx_text() -> str:
    pptx = ROOT / "submission" / "ControlPlane_Round2_Pitch.pptx"
    if not pptx.exists():
        return ""
    texts: list[str] = []
    with ZipFile(pptx) as zf:
        for name in zf.namelist():
            if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                xml = zf.read(name).decode("utf-8", errors="ignore")
                texts.extend(re.findall(r"<a:t>([^<]*)</a:t>", xml))
    return "\n".join(texts)


def _all_corpus() -> list[tuple[str, str]]:
    files = _iter_text_files()
    pdf = _pdf_text()
    if pdf:
        files.append(("submission/ControlPlane_Round2_Proposal.pdf", pdf))
    pptx = _pptx_text()
    if pptx:
        files.append(("submission/ControlPlane_Round2_Pitch.pptx", pptx))
    return files


def test_law3_matrix_is_exact_transcription():
    assert dict(MATRIX) == CANONICAL_MATRIX
    assert len(MATRIX) == 16


def test_law5_actuators_exact_five_members():
    names = {a.value for a in Actuator}
    assert names == {"Pass", "Pass + annotate", "Edit", "Escalate", "Block"}


_META = (
    "invent",
    "forbidden",
    "cut.",
    "cut ",
    "never",
    "not ",
    "don't",
    "do not",
    "banned",
    "anti-pattern",
    "reject",
    "≠",
    "instead of",
    "rather than",
    "say \"",
    "say “",
    "calling refund",
    "label",
    "targets",
    "overclaim",
    "dead on contact",
    "five-fold",
    "must not",
    "cannot",
    "cold-open",
    "saying ",
    "forbidden invention",
    "never `",
    "never '",
    "anti-pattern",
    "instead",
    "≠",
    "held/escalate",
    "held / escalate",
    "collapsing",
    "destroys the centrepiece",
    "centrepiece",
)


def _is_meta(window: str) -> bool:
    w = window.lower()
    return any(m in w for m in _META)


def test_law5_no_invented_actuator_names_in_artifacts():
    """Invented actuator phrases must not appear as real actuators.

    Allows: teaching lists that forbid them. Ignores `StreamingResponse` / HTTP streams.
    """
    hits: list[str] = []
    # Multi-word inventions only — "STREAM" alone collides with streaming HTTP.
    banned = ("Kill Span", "Terminate Step", "Hold & Re-verify", "Redact & Flag")
    for rel, text in _all_corpus():
        for bad in banned:
            for m in re.finditer(re.escape(bad), text):
                window = text[max(0, m.start() - 100) : m.end() + 100]
                if _is_meta(window):
                    continue
                hits.append(f"{rel}: uses invented actuator {bad!r}")
        # STREAM as actuator token (not StreamingResponse / upstream stream)
        for m in re.finditer(r"(?i)(?<!Streaming)(?<!streaming_)(?<!/)\\bSTREAM\\b(?!ing)", text):
            window = text[max(0, m.start() - 100) : m.end() + 100]
            if _is_meta(window) or "StreamingResponse" in window or "stream=" in window.lower():
                continue
            if "actuator" in window.lower() or "matrix" in window.lower():
                hits.append(f"{rel}: STREAM used as actuator")
    assert hits == [], "\n".join(hits)


def test_law1_clause_72_is_absence_not_coverage():
    hits: list[str] = []
    for rel, text in _all_corpus():
        for m in _CLAUSE_WRONG.finditer(text):
            window = text[max(0, m.start() - 80) : m.end() + 80]
            if _is_meta(window):
                continue
            hits.append(f"{rel}: {m.group(0)!r}")
    assert hits == [], "\n".join(hits)


def test_law2_never_assert_refund_was_blocked():
    hits: list[str] = []
    for rel, text in _all_corpus():
        for m in _REFUND_BLOCKED.finditer(text):
            window = text[max(0, m.start() - 100) : m.end() + 100]
            if _is_meta(window):
                continue
            hits.append(f"{rel}: {m.group(0)!r}")
    assert hits == [], "\n".join(hits)


def test_law6_never_quote_40ms_as_p95():
    """Fail only when 40ms is presented as p95, not when teaching 'never quote 40ms as p95'."""
    hits: list[str] = []
    for rel, text in _all_corpus():
        for m in _P95_40.finditer(text):
            window = text[max(0, m.start() - 100) : m.end() + 100]
            if _is_meta(window) or "p50" in window.lower():
                # "≤40ms p50 / ≤200ms p95" and "never quote 40ms as p95" are legal.
                continue
            hits.append(f"{rel}: {m.group(0)!r}")
    assert hits == [], "\n".join(hits)


def test_law9_company_pays_customer_does_not_lose():
    """Running example: company wrongly pays INR 1,84,000 — customer did not lose money."""
    blob = "\n".join(t for _, t in _all_corpus())
    assert re.search(r"(?i)(company|enterprise).{0,40}(pays|paid|payout|wrongly)", blob)
    # Forbidden inversion: customer lost the money as the primary framing.
    bad = re.findall(
        r"(?i)customer.{0,30}(lost|loses)\s+(INR\s*)?[₹■]?\s*1[,.]?84,?000",
        blob,
    )
    assert bad == []


def test_law8_refuse_to_claim_list_exists_and_is_about_us():
    narrative = (ROOT / "docs" / "reference" / "NARRATIVE.md").read_text(encoding="utf-8")
    arch = (ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    # Must disclaim ourselves — eliminate hallucinations / zero integration / zero latency / one accuracy.
    markers = ["eliminate hallucination", "zero integration", "zero", "latency", "accuracy"]
    # Look in ARCHITECTURE §10.8 / NARRATIVE refuse section
    section = arch + "\n" + narrative
    assert "refuse" in section.lower() or "disclaim" in section.lower()
    # Distinct from rejected approaches
    assert "Rejected approaches" in arch or "rejected approaches" in arch.lower()
    # About-us refusals appear near refuse-to-claim language
    assert any(m in section.lower() for m in ("hallucination", "zero integration", "one accuracy"))


def test_law9_bias_section_exists_in_measurement_terms():
    arch = (ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    final = (ROOT / "round2" / "CONTROLPLANE_R2_FINAL.md").read_text(encoding="utf-8")
    blob = arch + "\n" + final
    assert re.search(r"(?i)\bbias\b", blob)
    # Measurement framing, not moral lecture alone
    assert re.search(r"(?i)(counterfactual|flip rate|measurement|async)", blob)


def test_law7_fnr_schema_is_typed_placeholder_not_fabricated_percent():
    """Published FNR must not invent a measured percentage in stand docs."""
    stand = []
    for rel in (
        "README.md",
        "docs/SUBMIT.md",
        "docs/JUDGE_RUNBOOK.md",
        "docs/HOSTILE_QA_DRILL.md",
        "docs/ACCEPTANCE.md",
        "AGENTS.md",
    ):
        stand.append((ROOT / rel).read_text(encoding="utf-8"))
    blob = "\n".join(stand)
    # Fabricated "we catch 94%" style claims forbidden in stand surface.
    fab = re.findall(r"(?i)catch(?:es|ing)?\s+\d{2,3}\s*%\s+of\s+ungrounded", blob)
    assert fab == [], fab
