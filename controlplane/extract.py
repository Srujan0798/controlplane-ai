"""Lane-1 claim extraction: response text → typed Claim list.

Pure Python, zero deps, offline. Optional CONTROLPLANE_EXTRACTOR=llm
dispatches to an identical-signature stub; the demo never depends on it.
"""
from __future__ import annotations

import os
import re
from typing import Iterable

from controlplane.models import (
    Action,
    AssertionStrength,
    BlastTier,
    Claim,
    ClaimKind,
)

# Placeholders must not collide with source text.
_PH = "\x00{n}\x00"

# Indian grouping (1,84,000): first 1–3 digits, optional 2-digit groups, last 3.
# Western grouping (1,840,000) next, then bare decimals.
_PROTECT_PATTERNS: tuple[str, ...] = (
    r"₹\s*\d{1,3}(?:,\d{2})*,\d{3}(?:\.\d+)?",
    r"\b\d{1,3}(?:,\d{2})*,\d{3}(?:\.\d+)?\b",
    r"₹\s*\d{1,3}(?:,\d{3})+(?:\.\d+)?",
    r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b",
    r"§\s*\d+(?:\.\d+)*",
    r"\b(?:e\.g\.|i\.e\.|vs\.|etc\.|Dr\.|Mr\.|Mrs\.|Ms\.|Prof\.|Ltd\.|Inc\.|Jr\.|Sr\.|No\.)",
    r"\b\d+\.\d+\b",
)

_AMOUNT = re.compile(
    r"₹\s*\d{1,3}(?:,\d{2})*,\d{3}(?:\.\d+)?"
    r"|₹\s*\d{1,3}(?:,\d{3})+(?:\.\d+)?"
    r"|₹\s*\d+(?:\.\d+)?"
    r"|\b\d{1,3}(?:,\d{2})*,\d{3}(?:\.\d+)?\b"
    r"|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b"
    r"|\b(?:INR|Rs\.?)\s*\d[\d,]*"
    r"|\b\d[\d,]*\s*(?:INR|Rs\.?)\b"
    r"|\b\d+(?:\.\d+)?\s*%"
    r"|\b\d+(?:\.\d+)?\s*(?:lakh|lakhs|crore|crores)\b",
    re.IGNORECASE,
)
_CLAUSE = re.compile(r"\bclause\s+\d+(?:\.\d+)*\b", re.IGNORECASE)
_SECTION = re.compile(r"§\s*\d+(?:\.\d+)*|\bsection\s+\d+(?:\.\d+)*\b", re.IGNORECASE)
_ORDER_ID = re.compile(r"\bORD[- ]?\d+\b", re.IGNORECASE)
_DERIVED = re.compile(
    r"\b(?:sum of|total of|average of|avg of|mean of|computed(?:-|\s+)from|"
    r"aggregate of|difference of|count of|derived)\b",
    re.IGNORECASE,
)
_DATE = re.compile(
    r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|\d{1,2}\s+(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
    r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|"
    r"nov(?:ember)?|dec(?:ember)?)\s+\d{2,4}"
    r"|\d+\s+(?:day|days|week|weeks|month|months|year|years))\b",
    re.IGNORECASE,
)
_MODAL = re.compile(
    r"\b(?:must|shall|permits?|covers?|issued under)\b",
    re.IGNORECASE,
)
_CAUSAL = re.compile(
    r"\b(?:because|therefore|hence|due to|so that|as a result)\b",
    re.IGNORECASE,
)
_DECISION = re.compile(
    r"\b(?:approved|approves|approval|authorised|authorized|issued|denied|rejected)\b",
    re.IGNORECASE,
)
_ENTITY = re.compile(
    r"\b(?:[A-Z]{2,}[-_]?\d+"
    r"|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+"
    r"|customer account|goodwill)\b"
)
_HEDGE = re.compile(
    r"\b(?:may|might|typically|approximately|appears|should|i believe|"
    r"around|likely|possibly|probably|seems|roughly)\b",
    re.IGNORECASE,
)
_GREETING = re.compile(
    r"^(?:hello|hi|hey|thanks|thank you|good (?:morning|afternoon|evening)|"
    r"ok|okay|please)[!.,\s]*$",
    re.IGNORECASE,
)
_HEDGE_ALONE = re.compile(
    r"^(?:maybe|perhaps|probably|possibly|i think so|not sure|appears so)"
    r"[!.,\s]*$",
    re.IGNORECASE,
)
_META = re.compile(
    r"\b(?:as an ai|i am a language|let me know if|hope this helps|"
    r"here is what i|as requested)\b",
    re.IGNORECASE,
)
_STOP = frozenset(
    {
        "the",
        "a",
        "an",
        "of",
        "to",
        "for",
        "and",
        "or",
        "in",
        "on",
        "at",
        "is",
        "this",
        "that",
        "it",
        "be",
        "as",
        "by",
        "from",
        "with",
        "was",
        "are",
    }
)
_SHOWISH = re.compile(r"show|text|reply|display", re.IGNORECASE)
_REFUNDISH = re.compile(r"refund|issue", re.IGNORECASE)


def segment(text: str) -> list[str]:
    """Split into sentences without breaking amounts, clauses, or abbreviations."""
    if not text or not text.strip():
        return []
    held: list[str] = []

    def _stash(pattern: str, blob: str) -> str:
        def repl(m: re.Match[str]) -> str:
            held.append(m.group(0))
            return _PH.format(n=len(held) - 1)

        return re.sub(pattern, repl, blob)

    protected = text
    for pattern in _PROTECT_PATTERNS:
        protected = _stash(pattern, protected)

    parts = re.split(r"(?<=[.!?])\s+", protected)
    out: list[str] = []
    for part in parts:
        restored = re.sub(
            r"\x00(\d+)\x00",
            lambda m: held[int(m.group(1))],
            part,
        ).strip()
        if restored:
            out.append(restored)
    return out


def _has_payload(text: str) -> bool:
    return bool(
        _AMOUNT.search(text)
        or _CLAUSE.search(text)
        or _SECTION.search(text)
        or _ORDER_ID.search(text)
        or _DATE.search(text)
        or _MODAL.search(text)
        or _CAUSAL.search(text)
        or _DECISION.search(text)
        or _DERIVED.search(text)
        or _ENTITY.search(text)
    )


def _is_check_worthy(sentence: str) -> bool:
    s = sentence.strip()
    if not s:
        return False
    if _GREETING.match(s) or _HEDGE_ALONE.match(s) or _META.search(s):
        return False
    if s.endswith("?") and not _has_payload(s):
        return False
    return _has_payload(s)


def _kind_of(text: str) -> ClaimKind:
    # Strict precedence: DERIVED > NUMERIC > TEMPORAL > STRUCTURAL > TEXTUAL
    if _DERIVED.search(text):
        return ClaimKind.DERIVED
    if _AMOUNT.search(text):
        return ClaimKind.NUMERIC
    if _DATE.search(text):
        return ClaimKind.TEMPORAL
    if _CLAUSE.search(text) or _SECTION.search(text) or _ORDER_ID.search(text):
        return ClaimKind.STRUCTURAL
    return ClaimKind.TEXTUAL


def _assertion_of(text: str) -> AssertionStrength:
    """Hedge lexicon with light negation scoping.

    `may not` / `not likely` stay HEDGED. Bare `cannot` / `will not` without
    another hedge stay CATEGORICAL.
    """
    if not _HEDGE.search(text):
        return AssertionStrength.CATEGORICAL
    return AssertionStrength.HEDGED


def _left_words(text: str, start: int, n: int) -> str:
    return " ".join(text[:start].split()[-n:])


def _right_tail(text: str, end: int, n_words: int = 6) -> str:
    rest = text[end:]
    m = re.match(r"(?:\s+of(?:\s+the)?(?:\s+\w+){0,4})?", rest)
    if m and m.group(0).strip():
        return m.group(0)
    words = rest.split()
    if not words:
        return ""
    # Keep a short right context only when it is a prepositional tail.
    return ""


def _fragments(sentence: str) -> list[tuple[str, ClaimKind]]:
    """Split a check-worthy sentence into typed clause fragments."""
    kind = _kind_of(sentence)
    if kind == ClaimKind.DERIVED:
        return [(sentence.strip(), ClaimKind.DERIVED)]

    pieces: list[tuple[int, int, str, ClaimKind]] = []

    for m in _AMOUNT.finditer(sentence):
        left = _left_words(sentence, m.start(), 3)
        chunk = f"{left} {m.group(0)}".strip() if left else m.group(0)
        start = sentence.find(chunk) if chunk in sentence else m.start()
        pieces.append((start, start + len(chunk), chunk, ClaimKind.NUMERIC))

    for m in _CLAUSE.finditer(sentence):
        left = _left_words(sentence, m.start(), 2)
        tail = _right_tail(sentence, m.end())
        chunk = f"{left} {m.group(0)}{tail}".strip()
        start = sentence.find(chunk) if chunk in sentence else m.start()
        pieces.append((start, start + len(chunk), chunk, ClaimKind.STRUCTURAL))

    for m in _SECTION.finditer(sentence):
        pieces.append((m.start(), m.end(), m.group(0).strip(), ClaimKind.STRUCTURAL))

    for m in _ORDER_ID.finditer(sentence):
        left = _left_words(sentence, m.start(), 1)
        chunk = f"{left} {m.group(0)}".strip() if left.lower() == "order" else m.group(0)
        start = sentence.find(chunk) if chunk in sentence else m.start()
        pieces.append((start, start + len(chunk), chunk, ClaimKind.STRUCTURAL))

    for m in _DATE.finditer(sentence):
        if _AMOUNT.search(m.group(0)):
            continue
        pieces.append((m.start(), m.end(), m.group(0).strip(), ClaimKind.TEMPORAL))

    if not pieces:
        return [(sentence.strip(), kind)]

    # Drop fully contained duplicates (same kind, inner span).
    pieces.sort(key=lambda p: (p[0], -(p[1] - p[0])))
    kept: list[tuple[int, int, str, ClaimKind]] = []
    for piece in pieces:
        if any(
            piece[3] == k and piece[0] >= s and piece[1] <= e for s, e, _, k in kept
        ):
            continue
        kept.append(piece)

    covered = sentence
    for _, _, chunk, _ in kept:
        covered = covered.replace(chunk, " ", 1)
    residual = re.sub(r"\s+", " ", covered).strip(" .,;:")
    frags = [(chunk, k) for _, _, chunk, k in sorted(kept, key=lambda p: p[0])]
    if residual and _is_check_worthy(residual):
        frags.append((residual, _kind_of(residual)))
    return frags


def _tokens(text: str) -> set[str]:
    return {
        t
        for t in re.findall(r"[a-z0-9]+", text.lower())
        if t not in _STOP and len(t) > 1
    }


def _digits(text: str) -> set[str]:
    found: set[str] = set()
    for m in _AMOUNT.finditer(text):
        raw = re.sub(r"[^\d]", "", m.group(0).split("%")[0])
        if raw:
            found.add(raw.lstrip("0") or "0")
    for m in re.finditer(r"\b\d+\b", text):
        found.add(m.group(0).lstrip("0") or "0")
    return found


def _arg_norm(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def _roles(text: str, kind: ClaimKind, actions: Iterable[Action] | None) -> dict[str, float]:
    if not actions:
        return {}
    claim_toks = _tokens(text)
    claim_nums = _digits(text)
    roles: dict[str, float] = {}
    for action in actions:
        score = 0.0
        args = action.args or {}
        arg_toks: set[str] = set()
        for key, value in args.items():
            nv = _arg_norm(value)
            arg_toks |= _tokens(str(key)) | _tokens(str(value))
            compact = re.sub(r"[,\s₹]", "", nv).lower()
            if compact and (compact in {n.lower() for n in claim_nums} or compact in re.sub(r"[,\s₹]", "", text).lower()):
                score += 1.0
            if nv and nv.lower() in text.lower():
                score += 1.0
        name_toks = _tokens(action.name) | _tokens(action.action_id.replace("_", " "))
        overlap = claim_toks & (name_toks | arg_toks)
        if overlap:
            score += 0.4 * len(overlap)
        aid = action.action_id
        if action.tier == BlastTier.R1 or _SHOWISH.search(aid) or _SHOWISH.search(action.name):
            score = max(score, 0.5)
        if kind == ClaimKind.STRUCTURAL and (
            _CLAUSE.search(text) or _SECTION.search(text) or _ORDER_ID.search(text)
        ):
            if _REFUNDISH.search(aid) or _REFUNDISH.search(action.name):
                score = max(score, 0.9)
        if kind == ClaimKind.NUMERIC and (
            "amount" in args or _REFUNDISH.search(aid) or _REFUNDISH.search(action.name)
        ):
            score = max(score, 0.9)
        if score > 0:
            roles[aid] = min(1.0, score)
    return roles


def _stable_id(text: str, kind: ClaimKind, used: set[str]) -> str:
    lower = text.lower()
    clause = re.search(r"clause\s+(\d+)\.(\d+)", lower)
    section = re.search(r"§\s*(\d+(?:\.\d+)*)", text)
    if kind == ClaimKind.NUMERIC or (_AMOUNT.search(text) and kind != ClaimKind.DERIVED):
        base = "amount"
    elif clause:
        base = f"clause_{clause.group(1)}{clause.group(2)}"
    elif "goodwill" in lower or re.search(r"flagged for", lower):
        base = "hr_side"
    elif kind == ClaimKind.TEXTUAL and re.search(r"\bapprov", lower):
        base = "approval"
    elif _ORDER_ID.search(text) or re.search(r"\border\b", lower):
        base = "order"
    elif section:
        base = "section_" + section.group(1).replace(".", "")
    elif kind == ClaimKind.DERIVED:
        base = "derived"
    else:
        slug = re.sub(r"[^a-z0-9]+", "_", lower).strip("_")[:40]
        base = slug or "claim"
    cid = base
    n = 2
    while cid in used:
        cid = f"{base}_{n}"
        n += 1
    used.add(cid)
    return cid


def _seed_from_actions(
    text: str,
    actions: list[Action],
    existing: list[Claim],
    used: set[str],
) -> list[Claim]:
    """Promote action-arg entities that are only implicit in the response."""
    surface = " ".join([text, *(c.text for c in existing)]).lower()
    surface_compact = re.sub(r"[,\s₹]", "", surface)
    seeded: list[Claim] = []
    for action in actions:
        args = action.args or {}
        order = args.get("order")
        if order:
            token = str(order)
            if token.lower() not in surface:
                frag = f"order {token}"
                cid = _stable_id(frag, ClaimKind.STRUCTURAL, used)
                seeded.append(
                    Claim(
                        cid,
                        frag,
                        ClaimKind.STRUCTURAL,
                        AssertionStrength.CATEGORICAL,
                        _roles(frag, ClaimKind.STRUCTURAL, actions),
                    )
                )
                surface += " " + frag.lower()
        amount = args.get("amount")
        if amount is not None and not any(c.kind == ClaimKind.NUMERIC for c in existing + seeded):
            compact = re.sub(r"[,\s₹]", "", _arg_norm(amount))
            if compact and compact not in surface_compact:
                frag = f"amount {amount}"
                cid = _stable_id(frag, ClaimKind.NUMERIC, used)
                seeded.append(
                    Claim(
                        cid,
                        frag,
                        ClaimKind.NUMERIC,
                        AssertionStrength.CATEGORICAL,
                        _roles(frag, ClaimKind.NUMERIC, actions),
                    )
                )
    return seeded


def _extract_claims(
    text: str,
    *,
    actions: list[Action] | None = None,
) -> list[Claim]:
    used: set[str] = set()
    claims: list[Claim] = []
    seen_text: set[str] = set()
    for sentence in segment(text):
        if not _is_check_worthy(sentence):
            continue
        for frag, kind in _fragments(sentence):
            frag = frag.strip().strip(".,;:")
            key = frag.lower()
            if not frag or key in seen_text:
                continue
            seen_text.add(key)
            cid = _stable_id(frag, kind, used)
            claims.append(
                Claim(
                    cid,
                    frag,
                    kind,
                    _assertion_of(frag),
                    _roles(frag, kind, actions),
                )
            )
    if actions:
        claims.extend(_seed_from_actions(text, actions, claims, used))
    return claims


def extract_claims_llm(
    text: str,
    *,
    actions: list[Action] | None = None,
) -> list[Claim]:
    """Optional small-model adapter. Demo never depends on this path."""
    return _extract_claims(text, actions=actions)


def extract_claims(
    text: str,
    *,
    actions: list[Action] | None = None,
) -> list[Claim]:
    """Segment, filter, type, hedge-detect, and assign role_in_action."""
    if os.environ.get("CONTROLPLANE_EXTRACTOR") == "llm":
        return extract_claims_llm(text, actions=actions)
    return _extract_claims(text, actions=actions)
