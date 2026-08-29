"""Pure-Python BM25 over the provenance set + lexical-entailment gate.

Never searches the open web. Thresholds are named constants — calibrated
on the eval corpus in Phase 4 (T3.2), not asserted as magic numbers
(ARCHITECTURE §8).
"""
from __future__ import annotations

import math
import re
from collections import Counter

from controlplane.models import Verdict

# TODO T3.2 / Phase 4: calibrate on eval corpus; publish FP/FN curve.
BM25_K1 = 1.5
BM25_B = 0.75
BM25_TOP_K = 5
COVERAGE_SUPPORTED = 0.72
COVERAGE_UNKNOWN = 0.38

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
        "does",
        "do",
        "did",
        "not",
        "no",
        "never",
        "than",
        "into",
        "over",
        "under",
        "still",
        "may",
        "typically",
    }
)
_NEG_MARKERS = frozenset(
    {"not", "never", "no", "cannot", "without", "n't", "nt"}
)
_ANTONYM_PAIRS = (
    ("permit", "forbid"),
    ("permit", "deny"),
    ("allow", "deny"),
    ("allow", "forbid"),
    ("approve", "reject"),
    ("cover", "exclude"),
    ("accept", "reject"),
    ("include", "exclude"),
    ("issue", "withhold"),
)
_ANTONYM: dict[str, str] = {}
for _a, _b in _ANTONYM_PAIRS:
    _ANTONYM[_a] = _b
    _ANTONYM[_b] = _a

_WORD = re.compile(r"[a-z0-9]+")
_RANK = {
    Verdict.CONTRADICTED: 3,
    Verdict.SUPPORTED: 2,
    Verdict.UNKNOWN: 1,
    Verdict.UNSUPPORTED: 0,
}


def stem(word: str) -> str:
    w = word.lower()
    for suf, repl in (("ies", "y"), ("ing", ""), ("ers", ""), ("er", ""), ("es", ""), ("ed", ""), ("s", "")):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)] + repl
    return w


def tokenize(text: str) -> list[str]:
    return [
        stem(tok)
        for tok in _WORD.findall(text.lower())
        if tok not in _STOP and len(tok) > 1
    ]


def content_words(text: str) -> set[str]:
    return set(tokenize(text))


def _idf(df: int, n_docs: int) -> float:
    return math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))


def rank(
    query: str,
    documents: list[tuple[str, str]],
    k: int = BM25_TOP_K,
) -> list[tuple[str, float]]:
    """BM25 ranking over provenance documents only."""
    tokenized = [(doc_id, tokenize(body)) for doc_id, body in documents]
    n_docs = len(tokenized) or 1
    avgdl = sum(len(toks) for _, toks in tokenized) / n_docs
    df: Counter[str] = Counter()
    for _, toks in tokenized:
        df.update(set(toks))
    qtoks = tokenize(query)
    scored: list[tuple[str, float]] = []
    for doc_id, toks in tokenized:
        tf = Counter(toks)
        dl = len(toks) or 1
        score = 0.0
        for qi in qtoks:
            freq = tf.get(qi, 0)
            if not freq:
                continue
            denom = freq + BM25_K1 * (1.0 - BM25_B + BM25_B * dl / (avgdl or 1.0))
            score += _idf(df[qi], n_docs) * (freq * (BM25_K1 + 1.0)) / denom
        scored.append((doc_id, score))
    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored[:k]


def negated_stems(text: str) -> set[str]:
    words = _WORD.findall(text.lower())
    out: set[str] = set()
    for i, word in enumerate(words):
        marker = word in _NEG_MARKERS or word.endswith("n't")
        if not marker:
            continue
        for nxt in words[i + 1 : i + 4]:
            if nxt not in _STOP and len(nxt) > 1:
                out.add(stem(nxt))
    return out


def lexical_gate(claim_text: str, span_text: str) -> tuple[Verdict, float, str]:
    claim = content_words(claim_text)
    span = content_words(span_text)
    if not claim:
        return Verdict.UNSUPPORTED, 0.0, "textual: no content words in claim"
    coverage = len(claim & span) / len(claim)
    span_neg = negated_stems(span_text)
    claim_neg = negated_stems(claim_text)
    if coverage >= COVERAGE_UNKNOWN:
        if (claim & span_neg) and not (claim & claim_neg):
            return (
                Verdict.CONTRADICTED,
                coverage,
                f"textual: negation (coverage={coverage:.2f})",
            )
        if (span & claim_neg) and not (span & span_neg):
            return (
                Verdict.CONTRADICTED,
                coverage,
                f"textual: claim negated, span affirms (coverage={coverage:.2f})",
            )
        for word in claim:
            anti = _ANTONYM.get(word)
            if anti and anti in span and word not in span:
                return (
                    Verdict.CONTRADICTED,
                    coverage,
                    f"textual: antonym {word}/{anti} (coverage={coverage:.2f})",
                )
    if coverage >= COVERAGE_SUPPORTED:
        return Verdict.SUPPORTED, coverage, f"textual: coverage={coverage:.2f}"
    if coverage >= COVERAGE_UNKNOWN:
        return (
            Verdict.UNKNOWN,
            coverage,
            f"textual: middle band coverage={coverage:.2f}",
        )
    return Verdict.UNSUPPORTED, coverage, f"textual: coverage={coverage:.2f}"


def bind_textual(
    claim_text: str,
    spans: dict[str, str],
) -> tuple[Verdict, tuple[str, ...], str]:
    if not spans:
        return Verdict.UNSUPPORTED, (), "textual: empty provenance"
    ranked = rank(claim_text, list(spans.items()))
    best: tuple[Verdict, tuple[str, ...], str, float] | None = None
    for sid, score in ranked:
        verdict, coverage, why = lexical_gate(claim_text, spans[sid])
        rank_key = (_RANK[verdict], coverage, score)
        if best is None:
            best = (verdict, (sid,), why, rank_key[0] + coverage)
            best_key = rank_key
            continue
        if rank_key > best_key:
            best = (verdict, (sid,), why, rank_key[0] + coverage)
            best_key = rank_key
    if best is None:
        return Verdict.UNSUPPORTED, (), "textual: no ranked span"
    return best[0], best[1], best[2]
