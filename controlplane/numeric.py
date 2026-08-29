"""Quantity extraction, normalisation, and derived recomputation.

Lane 1: pure Python, zero deps. Indian *and* Western digit grouping,
currency symbols, scale words, per-unit tolerance.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

from controlplane.models import Verdict

REL_TOL = 1e-6
ABS_TOL_BY_UNIT = {
    "INR": 0.5,
    "USD": 0.01,
    "EUR": 0.01,
    "PCT": 0.05,
    "DAY": 0.0,
    "": 0.5,
}
_CURRENCY = frozenset({"INR", "USD", "EUR"})
_SCALE_WORDS = {
    "lakh": 1e5,
    "lakhs": 1e5,
    "crore": 1e7,
    "crores": 1e7,
    "thousand": 1e3,
    "thousands": 1e3,
    "million": 1e6,
    "millions": 1e6,
    "billion": 1e9,
    "billions": 1e9,
    "bn": 1e9,
    "k": 1e3,
    "m": 1e6,
}
_CUR_PREFIX = {
    "₹": "INR",
    "rs.": "INR",
    "rs": "INR",
    "inr": "INR",
    "$": "USD",
    "usd": "USD",
    "€": "EUR",
    "eur": "EUR",
}

_INDIAN = r"\d{1,3}(?:,\d{2})+,\d{3}(?:\.\d+)?"
_WESTERN = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?"
_BARE = r"\d+(?:\.\d+)?"
_NUM_RX = re.compile(rf"(?P<indian>{_INDIAN})|(?P<western>{_WESTERN})|(?P<bare>{_BARE})")
_PREFIX_RX = re.compile(r"(₹|Rs\.?|INR|USD|\$|€)\s*$", re.IGNORECASE)
_SUFFIX_CUR_RX = re.compile(r"\s*(INR|Rs\.?|USD|EUR)\b", re.IGNORECASE)
_SCALE_RX = re.compile(
    r"\s*(lakhs?|crores?|thousands?|millions?|billions?|bn|k|m)\b",
    re.IGNORECASE,
)
_PCT_RX = re.compile(r"\s*(%|percent(?:age)?)\b", re.IGNORECASE)
_DAY_RX = re.compile(r"\s*(?:business\s+)?days?\b", re.IGNORECASE)
_STRUCTURAL_LEFT = re.compile(r"(?:clause|section|§)\s*$", re.IGNORECASE)
_SUM_RX = re.compile(r"\b(?:sum of|total of)\b|\+", re.IGNORECASE)
_AVG_RX = re.compile(r"\b(?:average of|avg of|mean of)\b", re.IGNORECASE)
_COUNT_RX = re.compile(r"\b(?:count of|number of)\b", re.IGNORECASE)
_DIFF_RX = re.compile(r"\b(?:difference of|minus)\b", re.IGNORECASE)


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str
    raw: str
    start: int = 0
    end: int = 0


def _norm_unit(unit: str) -> str:
    u = (unit or "").strip().upper().rstrip(".")
    if u in {"RS", "₹"}:
        return "INR"
    return u


def _parse_grouped(num: str) -> float:
    return float(num.replace(",", ""))


def extract_quantities(text: str) -> list[Quantity]:
    """Pull normalised quantities; skip clause/section numbers and ID fragments."""
    if not text:
        return []
    out: list[Quantity] = []
    occupied: list[tuple[int, int]] = []

    def taken(start: int, end: int) -> bool:
        return any(start < hi and end > lo for lo, hi in occupied)

    for m in _NUM_RX.finditer(text):
        start, end = m.start(), m.end()
        if taken(start, end):
            continue
        if start > 0 and text[start - 1] in "-_":
            continue
        if _STRUCTURAL_LEFT.search(text[:start]):
            continue
        raw_num = m.group(0)
        try:
            value = _parse_grouped(raw_num)
        except ValueError:
            continue
        unit = ""
        raw = raw_num
        prefix = _PREFIX_RX.search(text[:start])
        if prefix:
            unit = _CUR_PREFIX.get(prefix.group(1).lower(), _CUR_PREFIX.get(prefix.group(1), ""))
            if not unit:
                unit = _norm_unit(prefix.group(1))
            raw = prefix.group(1) + raw_num
        rest = text[end:]
        pct = _PCT_RX.match(rest)
        scale = _SCALE_RX.match(rest)
        cur = _SUFFIX_CUR_RX.match(rest)
        days = _DAY_RX.match(rest)
        if pct:
            unit = "PCT"
            end += pct.end()
            raw = raw_num + pct.group(0)
        elif scale:
            key = scale.group(1).lower()
            value *= _SCALE_WORDS.get(key, 1.0)
            end += scale.end()
            raw = raw_num + scale.group(0)
        elif cur:
            unit = _norm_unit(cur.group(1))
            end += cur.end()
            raw = raw_num + cur.group(0)
        elif days:
            unit = "DAY"
            end += days.end()
            raw = raw_num + days.group(0)
        occupied.append((start, end))
        out.append(Quantity(value=value, unit=unit, raw=raw.strip(), start=start, end=end))
    return out


def _same_slot(claim_q: Quantity, span_q: Quantity) -> bool:
    cu, su = _norm_unit(claim_q.unit), _norm_unit(span_q.unit)
    if cu and su:
        return cu == su
    if cu in _CURRENCY and not su:
        return True
    if su in _CURRENCY and not cu:
        return True
    if not cu and not su:
        return True
    return False


def quantities_equal(a: Quantity, b: Quantity) -> bool:
    abs_tol = max(
        ABS_TOL_BY_UNIT.get(_norm_unit(a.unit), 0.5),
        ABS_TOL_BY_UNIT.get(_norm_unit(b.unit), 0.5),
    )
    return math.isclose(a.value, b.value, rel_tol=REL_TOL, abs_tol=abs_tol)


def match_numeric(
    claim_text: str,
    spans: dict[str, str],
) -> tuple[Verdict, tuple[str, ...], str]:
    claim_qs = extract_quantities(claim_text)
    if not claim_qs:
        return Verdict.UNSUPPORTED, (), "numeric: no quantity in claim"
    cq = claim_qs[0]
    matches: list[tuple[str, Quantity]] = []
    conflicts: list[tuple[str, Quantity]] = []
    for sid, content in spans.items():
        for sq in extract_quantities(content):
            if not _same_slot(cq, sq):
                continue
            if quantities_equal(cq, sq):
                matches.append((sid, sq))
            elif _norm_unit(cq.unit) and _norm_unit(cq.unit) == _norm_unit(sq.unit):
                conflicts.append((sid, sq))
            elif _norm_unit(cq.unit) in _CURRENCY and _norm_unit(sq.unit) in _CURRENCY:
                conflicts.append((sid, sq))
            elif _norm_unit(cq.unit) in _CURRENCY and not _norm_unit(sq.unit):
                # Empty-unit span number only contradicts when it is amount-scale.
                if sq.value >= 1000:
                    conflicts.append((sid, sq))
    if matches:
        sid, sq = matches[0]
        unique = tuple(dict.fromkeys(s for s, _ in matches))
        return (
            Verdict.SUPPORTED,
            unique,
            f"numeric: {cq.raw} ≡ {sq.raw} on {sid}",
        )
    if conflicts:
        sid, sq = conflicts[0]
        return (
            Verdict.CONTRADICTED,
            (sid,),
            f"numeric: {cq.raw} ≠ {sq.raw} on {sid}",
        )
    return Verdict.UNSUPPORTED, (), "numeric: no compatible quantity in provenance"


def recompute_derived(
    claim_text: str,
    spans: dict[str, str],
) -> tuple[Verdict, tuple[str, ...], str]:
    """Sum/avg/count/diff from span quantities. Not recomputable → UNKNOWN."""
    if _SUM_RX.search(claim_text):
        op = "sum"
    elif _AVG_RX.search(claim_text):
        op = "avg"
    elif _COUNT_RX.search(claim_text):
        op = "count"
    elif _DIFF_RX.search(claim_text):
        op = "diff"
    else:
        return Verdict.UNKNOWN, (), "derived: no recomputation operator"

    claimed = extract_quantities(claim_text)
    operands: list[tuple[str, Quantity]] = []
    for sid, content in spans.items():
        for q in extract_quantities(content):
            if claimed and not _same_slot(claimed[0], q):
                continue
            operands.append((sid, q))
    values = [q.value for _, q in operands]
    sids = tuple(dict.fromkeys(sid for sid, _ in operands))

    if op in {"sum", "avg", "diff"} and len(values) < 2:
        return Verdict.UNKNOWN, (), f"derived: {op} needs ≥2 operands"
    if op == "sum":
        computed = float(sum(values))
    elif op == "avg":
        computed = float(sum(values) / len(values))
    elif op == "diff":
        computed = abs(values[0] - values[1])
    else:
        computed = float(len(values))

    if not claimed:
        return Verdict.UNKNOWN, (), "derived: no claimed quantity"
    target = claimed[0]
    if math.isclose(computed, target.value, rel_tol=REL_TOL, abs_tol=0.5):
        return (
            Verdict.SUPPORTED,
            sids,
            f"derived: {op}={computed:g} ≡ {target.raw}",
        )
    return (
        Verdict.CONTRADICTED,
        sids,
        f"derived: {op}={computed:g} ≠ {target.raw}",
    )
