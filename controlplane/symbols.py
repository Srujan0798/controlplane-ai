"""Clause/section/ID symbol table. Binding is a lookup, not a search."""
from __future__ import annotations

import re
from collections.abc import Mapping

from controlplane.models import Verdict

_CLAUSE = re.compile(r"\b(?:clause|section)\s+(\d+(?:\.\d+)*)", re.IGNORECASE)
_SECTION_MARK = re.compile(r"§\s*(\d+(?:\.\d+)*)")
_ID = re.compile(r"\b([A-Z]{2,}[-]\d+)\b")


def extract_symbols(text: str) -> list[str]:
    """Normalised symbols: dotted clause numbers and IDs like ORD-9."""
    if not text:
        return []
    found: list[str] = []
    for rx in (_CLAUSE, _SECTION_MARK):
        for m in rx.finditer(text):
            token = m.group(1)
            if token not in found:
                found.append(token)
    for m in _ID.finditer(text):
        token = m.group(1).upper()
        if token not in found:
            found.append(token)
    return found


def build_symbol_table(spans: Mapping[str, str]) -> dict[str, tuple[str, ...]]:
    """Map each symbol in the provenance set to the span_ids that mention it."""
    table: dict[str, list[str]] = {}
    for sid, content in spans.items():
        for sym in extract_symbols(content):
            bucket = table.setdefault(sym, [])
            if sid not in bucket:
                bucket.append(sid)
    return {key: tuple(ids) for key, ids in table.items()}


def lookup_symbols(claim_text: str, table: Mapping[str, tuple[str, ...]]) -> tuple[str, ...]:
    """Fail closed: every referenced symbol must hit, or the lookup is empty."""
    refs = extract_symbols(claim_text)
    if not refs:
        return ()
    hits: list[str] = []
    for ref in refs:
        if ref not in table:
            return ()
        for sid in table[ref]:
            if sid not in hits:
                hits.append(sid)
    return tuple(hits)


def match_structural(
    claim_text: str,
    table: Mapping[str, tuple[str, ...]],
) -> tuple[Verdict, tuple[str, ...], str]:
    refs = extract_symbols(claim_text)
    have = ", ".join(sorted(table)) or "none"
    if not refs:
        return (
            Verdict.UNSUPPORTED,
            (),
            f"structural: no clause/ID in claim (have {have})",
        )
    hits = lookup_symbols(claim_text, table)
    if hits:
        return (
            Verdict.SUPPORTED,
            hits,
            f"structural: {', '.join(refs)} → {', '.join(hits)}",
        )
    missing = ", ".join(r for r in refs if r not in table)
    return (
        Verdict.UNSUPPORTED,
        (),
        f"structural: {missing} absent from symbol table (have {have})",
    )
