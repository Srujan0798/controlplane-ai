"""PII / sensitive-entity detectors for leakage Rule A (ARCHITECTURE §3).

Pure Python. Gazetteer match via a tiny Aho-Corasick automaton plus
checksum-validated pattern detectors (PAN, Aadhaar/Verhoeff, email,
Indian phone, IFSC, card/Luhn, IBAN).
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PiiHit:
    kind: str
    value: str
    start: int
    end: int


# --- Verhoeff (Aadhaar) -------------------------------------------------

_VERHOEFF_D = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
)
_VERHOEFF_P = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
)


def _verhoeff_ok(num: str) -> bool:
    if not num.isdigit():
        return False
    c = 0
    for i, ch in enumerate(reversed(num)):
        c = _VERHOEFF_D[c][_VERHOEFF_P[i % 8][int(ch)]]
    return c == 0


def is_valid_aadhaar(value: str) -> bool:
    digits = re.sub(r"\s+", "", value)
    if not re.fullmatch(r"[2-9]\d{11}", digits):
        return False
    return _verhoeff_ok(digits)


def is_valid_pan(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]{5}\d{4}[A-Z]", value))


def is_valid_card_luhn(value: str) -> bool:
    digits = re.sub(r"[\s-]", "", value)
    if not digits.isdigit() or not (12 <= len(digits) <= 19):
        return False
    total = 0
    alt = False
    for ch in reversed(digits):
        n = int(ch)
        if alt:
            n *= 2
            if n > 9:
                n -= 9
        total += n
        alt = not alt
    return total % 10 == 0


# --- Tiny Aho-Corasick for gazetteer tokens ------------------------------


class _ACNode:
    __slots__ = ("next", "fail", "out")

    def __init__(self) -> None:
        self.next: dict[str, _ACNode] = {}
        self.fail: _ACNode | None = None
        self.out: list[str] = []


def build_aho(patterns: list[str]) -> _ACNode:
    root = _ACNode()
    for pat in patterns:
        if not pat:
            continue
        node = root
        for ch in pat.lower():
            node = node.next.setdefault(ch, _ACNode())
        node.out.append(pat)
    # failure links
    from collections import deque

    q: deque[_ACNode] = deque()
    for child in root.next.values():
        child.fail = root
        q.append(child)
    while q:
        r = q.popleft()
        for ch, s in r.next.items():
            q.append(s)
            f = r.fail
            while f is not None and ch not in f.next:
                f = f.fail
            s.fail = f.next[ch] if f is not None and ch in f.next else root
            s.out = s.out + s.fail.out
    return root


def _ac_find(root: _ACNode, text: str) -> list[tuple[int, int, str]]:
    hits: list[tuple[int, int, str]] = []
    node = root
    lower = text.lower()
    for i, ch in enumerate(lower):
        while node is not None and node is not root and ch not in node.next:
            node = node.fail  # type: ignore[assignment]
        if node is None:
            node = root
        node = node.next.get(ch, root)
        for pat in node.out:
            start = i - len(pat) + 1
            hits.append((start, i + 1, pat))
    return hits


# --- Pattern detectors ---------------------------------------------------

_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_IN = re.compile(r"(?:\+91[\s-]*)?[6-9]\d{9}\b|\b[6-9]\d{4}\s?\d{5}\b")
_PAN = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")
_AADHAAR = re.compile(r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b")
_IFSC = re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b")
_CARD = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b")

_STATIC_SENSITIVE = (
    "ssn",
    "password",
    "secret key",
    "api_key",
)


def detect_pii(text: str, *, gazetteer: list[str] | None = None) -> list[PiiHit]:
    """Return PII-shaped hits in `text` (deduped by span)."""
    hits: list[PiiHit] = []

    def add(kind: str, m: re.Match[str]) -> None:
        hits.append(PiiHit(kind, m.group(0), m.start(), m.end()))

    for m in _EMAIL.finditer(text):
        add("email", m)
    for m in _PHONE_IN.finditer(text):
        add("phone_in", m)
    for m in _PAN.finditer(text):
        if is_valid_pan(m.group(0)):
            add("pan", m)
    for m in _AADHAAR.finditer(text):
        raw = re.sub(r"\s+", "", m.group(0))
        if is_valid_aadhaar(raw):
            hits.append(PiiHit("aadhaar", m.group(0), m.start(), m.end()))
    for m in _IFSC.finditer(text):
        add("ifsc", m)
    for m in _CARD.finditer(text):
        if is_valid_card_luhn(m.group(0)):
            add("card", m)
    for m in _IBAN.finditer(text):
        add("iban", m)

    patterns = list(_STATIC_SENSITIVE) + list(gazetteer or [])
    if patterns:
        root = build_aho(patterns)
        for start, end, pat in _ac_find(root, text):
            hits.append(PiiHit("gazetteer", text[start:end], start, end))

    # Dedup overlapping identical kind+value
    seen: set[tuple[str, str, int, int]] = set()
    out: list[PiiHit] = []
    for h in hits:
        key = (h.kind, h.value, h.start, h.end)
        if key not in seen:
            seen.add(key)
            out.append(h)
    return out


def pii_unbound_in_text(text: str, span_texts: list[str]) -> list[PiiHit]:
    """Rule A: PII-shaped entities in output that appear in no span."""
    joined = "\n".join(span_texts).lower()
    unbound: list[PiiHit] = []
    for hit in detect_pii(text):
        needle = re.sub(r"\s+", "", hit.value).lower()
        hay = re.sub(r"\s+", "", joined)
        if needle not in hay and hit.value.lower() not in joined:
            unbound.append(hit)
    return unbound


def apply_pii_rule_a(
    ledger: "EvidenceLedger",
    response_text: str,
    *,
    action_ids: list[str] | None = None,
) -> list["Claim"]:
    """Inject CONTRADICTED claims for unbound PII (forces Block at R2/R3).

    Returns the synthetic claims added. Does not invent spans — absence of a
    spanning record is exactly the leak signal.
    """
    from controlplane.models import (  # local import keeps pii import-light
        AssertionStrength,
        Binding,
        Claim,
        ClaimKind,
        Verdict,
    )

    span_texts = [sp.content for sp in ledger.spans.values()]
    unbound = pii_unbound_in_text(response_text, span_texts)
    if not unbound:
        return []

    roles = {aid: 1.0 for aid in (action_ids or list(ledger.actions.keys()) or ["issue_refund"])}
    added: list[Claim] = []
    for i, hit in enumerate(unbound):
        cid = f"pii_leak_{hit.kind}_{i}"
        claim = Claim(
            cid,
            f"output discloses {hit.kind} {hit.value}",
            ClaimKind.TEXTUAL,
            AssertionStrength.CATEGORICAL,
            dict(roles),
        )
        ledger.claims[cid] = claim
        binding = Binding(
            cid,
            (),
            "pii-unbound",
            Verdict.CONTRADICTED,
            (
                f"Rule A: {hit.kind}={hit.value!r} appears in model output but "
                "binds to no provenance span (memory leak or fabrication)"
            ),
        )
        ledger.bindings[cid] = binding
        ledger.append(
            "binding",
            {
                "claim_id": cid,
                "span_ids": [],
                "method": binding.method,
                "verdict": binding.verdict.value,
                "rationale": binding.rationale,
            },
        )
        added.append(claim)
    return added
