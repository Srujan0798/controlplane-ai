#!/usr/bin/env python3
"""Render round2/CONTROLPLANE_R2_FINAL.md → submission/ControlPlane_Round2_Proposal.pdf.

Requires reportlab (`pip install reportlab` or `pip install '.[pdf]'`).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "round2" / "CONTROLPLANE_R2_FINAL.md"
OUT = ROOT / "submission" / "ControlPlane_Round2_Proposal.pdf"


def _require_reportlab():
    try:
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT  # noqa: F401
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            ListFlowable,
            ListItem,
            PageBreak,
            Paragraph,
            Preformatted,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
        from reportlab.lib import colors
    except ImportError as exc:
        print(
            "reportlab required: pip install reportlab  (or pip install '.[pdf]')",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    return {
        "A4": A4,
        "ParagraphStyle": ParagraphStyle,
        "getSampleStyleSheet": getSampleStyleSheet,
        "inch": inch,
        "ListFlowable": ListFlowable,
        "ListItem": ListItem,
        "PageBreak": PageBreak,
        "Paragraph": Paragraph,
        "Preformatted": Preformatted,
        "SimpleDocTemplate": SimpleDocTemplate,
        "Spacer": Spacer,
        "Table": Table,
        "TableStyle": TableStyle,
        "colors": colors,
        "TA_CENTER": TA_CENTER,
        "TA_JUSTIFY": TA_JUSTIFY,
        "TA_LEFT": TA_LEFT,
    }


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _inline_md(text: str) -> str:
    """Very small markdown → reportlab XML subset."""
    t = _escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"`([^`]+)`", r"<font face='Courier' size='9'>\1</font>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<u>\1</u>", t)
    return t


def _split_table_row(line: str) -> list[str]:
    raw = line.strip().strip("|")
    return [c.strip() for c in raw.split("|")]


def build(md_path: Path = SRC, out_path: Path = OUT) -> Path:
    rl = _require_reportlab()
    text = md_path.read_text(encoding="utf-8")
    # Helvetica lacks ₹; use INR so glyphs render
    text = text.replace("₹", "INR ").replace("■", "INR ")
    lines = text.splitlines()

    styles = rl["getSampleStyleSheet"]()
    title = rl["ParagraphStyle"](
        "TitleCP",
        parent=styles["Title"],
        fontSize=22,
        leading=26,
        spaceAfter=10,
        alignment=rl["TA_CENTER"],
        textColor=rl["colors"].HexColor("#1A2A3D"),
        fontName="Helvetica-Bold",
    )
    h1 = rl["ParagraphStyle"](
        "H1CP", parent=styles["Heading1"], fontSize=14, leading=18, spaceBefore=16, spaceAfter=8
    )
    h2 = rl["ParagraphStyle"](
        "H2CP", parent=styles["Heading2"], fontSize=12, leading=15, spaceBefore=12, spaceAfter=6
    )
    h3 = rl["ParagraphStyle"](
        "H3CP", parent=styles["Heading3"], fontSize=11, leading=14, spaceBefore=10, spaceAfter=4
    )
    body = rl["ParagraphStyle"](
        "BodyCP",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=rl["TA_JUSTIFY"],
        spaceAfter=6,
        textColor=rl["colors"].HexColor("#2A2A35"),
        fontName="Helvetica",
    )
    quote = rl["ParagraphStyle"](
        "QuoteCP",
        parent=body,
        leftIndent=12,
        textColor=rl["colors"].HexColor("#333333"),
        fontName="Helvetica-Oblique",
    )
    code = rl["ParagraphStyle"](
        "CodeCP",
        parent=styles["Code"],
        fontSize=8,
        leading=10,
        fontName="Courier",
        backColor=rl["colors"].HexColor("#f4f4f4"),
        leftIndent=6,
        rightIndent=6,
        spaceBefore=4,
        spaceAfter=8,
    )
    meta = rl["ParagraphStyle"](
        "MetaCP", parent=body, alignment=rl["TA_CENTER"], fontSize=9, spaceAfter=4
    )

    story: list = []
    i = 0
    in_code = False
    code_buf: list[str] = []
    list_buf: list[str] = []
    table_buf: list[list[str]] = []

    def flush_list() -> None:
        nonlocal list_buf
        if not list_buf:
            return
        items = [
            rl["ListItem"](rl["Paragraph"](_inline_md(item), body), leftIndent=12, value="bullet")
            for item in list_buf
        ]
        story.append(
            rl["ListFlowable"](items, bulletType="bullet", start="•", leftIndent=18, spaceAfter=6)
        )
        list_buf = []

    def flush_table() -> None:
        nonlocal table_buf
        if not table_buf:
            return
        # Drop markdown separator rows (|---|---|)
        rows = [
            r
            for r in table_buf
            if not all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in r)
        ]
        if not rows:
            table_buf = []
            return
        wrapped = [
            [rl["Paragraph"](_inline_md(c), body) for c in row] for row in rows
        ]
        col_n = max(len(r) for r in wrapped)
        for row in wrapped:
            while len(row) < col_n:
                row.append(rl["Paragraph"]("", body))
        usable = rl["A4"][0] - 1.5 * rl["inch"]
        col_w = usable / col_n
        tbl = rl["Table"](wrapped, colWidths=[col_w] * col_n, repeatRows=1)
        tbl.setStyle(
            rl["TableStyle"](
                [
                    ("BACKGROUND", (0, 0), (-1, 0), rl["colors"].HexColor("#eeeeee")),
                    ("GRID", (0, 0), (-1, -1), 0.4, rl["colors"].grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(tbl)
        story.append(rl["Spacer"](1, 8))
        table_buf = []

    while i < len(lines):
        line = lines[i]
        if in_code:
            if line.strip().startswith("```"):
                story.append(rl["Preformatted"]("\n".join(code_buf) or " ", code))
                code_buf = []
                in_code = False
            else:
                code_buf.append(line)
            i += 1
            continue

        if line.strip().startswith("```"):
            flush_list()
            flush_table()
            in_code = True
            code_buf = []
            i += 1
            continue

        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            flush_list()
            table_buf.append(_split_table_row(line))
            i += 1
            continue
        else:
            flush_table()

        if re.match(r"^[-*] ", line.strip()):
            list_buf.append(re.sub(r"^[-*] ", "", line.strip()))
            i += 1
            continue
        else:
            flush_list()

        if line.startswith("# "):
            story.append(rl["Paragraph"](_inline_md(line[2:].strip()), title))
        elif line.startswith("## "):
            story.append(rl["Paragraph"](_inline_md(line[3:].strip()), h1))
        elif line.startswith("### "):
            story.append(rl["Paragraph"](_inline_md(line[4:].strip()), h2))
        elif line.startswith("#### "):
            story.append(rl["Paragraph"](_inline_md(line[5:].strip()), h3))
        elif line.startswith("> "):
            story.append(rl["Paragraph"](_inline_md(line[2:].strip()), quote))
        elif line.strip() == "---":
            story.append(rl["Spacer"](1, 10))
        elif line.strip() == "":
            story.append(rl["Spacer"](1, 4))
        elif i < 8 and not line.startswith("#"):
            story.append(rl["Paragraph"](_inline_md(line.strip()), meta))
        else:
            story.append(rl["Paragraph"](_inline_md(line.strip()), body))
        i += 1

    flush_list()
    flush_table()
    if in_code and code_buf:
        story.append(rl["Preformatted"]("\n".join(code_buf), code))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = rl["SimpleDocTemplate"](
        str(out_path),
        pagesize=rl["A4"],
        leftMargin=0.75 * rl["inch"],
        rightMargin=0.75 * rl["inch"],
        topMargin=0.7 * rl["inch"],
        bottomMargin=0.7 * rl["inch"],
        title="ControlPlane.ai — Round 2 Detailed Business Proposal",
        author="Team ControlPlane",
    )
    doc.build(story)
    return out_path


def main() -> None:
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
