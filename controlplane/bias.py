"""Bias measurement — ACL skew stub + counterfactual flip rate (Phase 6c).

ACL skew remains as a distributional surface. The load-bearing number is the
decision-flip rate under protected-attribute perturbation, reported with a
Wilson CI over a rolling window. Lane-3 / async; never a per-response moral
verdict (content law #9).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from controlplane.ledger import EvidenceLedger

# Local Wilson CI — keep controlplane independent of evals package.
import math


def _wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n <= 0:
        return 0.0, 0.0, 0.0
    p = successes / n
    z2 = z * z
    denom = 1.0 + z2 / n
    centre = p + z2 / (2 * n)
    margin = z * math.sqrt((p * (1 - p) + z2 / (4 * n)) / n)
    low = max(0.0, (centre - margin) / denom)
    high = min(1.0, (centre + margin) / denom)
    return p, low, high


def probe_acl_skew(ledger: EvidenceLedger) -> dict[str, Any]:
    """Return `{acl_skew, flag}` for spans vs principal clearance.

    `acl_skew` = fraction of spans whose ACL is not ⊆ principal.clearance.
    `flag` is True when acl_skew > 0 (any unreadable span present).
    """
    spans = list(ledger.spans.values())
    if not spans:
        return {"acl_skew": 0.0, "flag": False}
    clearance = ledger.principal.clearance
    unreadable = sum(1 for sp in spans if not sp.acl.issubset(clearance))
    acl_skew = unreadable / len(spans)
    return {"acl_skew": acl_skew, "flag": acl_skew > 0}


@dataclass
class FlipWindow:
    """Rolling window of counterfactual flip observations."""

    flips: list[bool] = field(default_factory=list)
    max_n: int = 200

    def record(self, flipped: bool) -> None:
        self.flips.append(bool(flipped))
        if len(self.flips) > self.max_n:
            self.flips = self.flips[-self.max_n :]

    def summary(self) -> dict[str, Any]:
        n = len(self.flips)
        k = sum(self.flips)
        rate, lo, hi = _wilson_ci(k, n)
        return {
            "n": n,
            "flips": k,
            "flip_rate": rate,
            "wilson_95": [lo, hi],
            "flag_ci_excludes_zero": bool(n > 0 and lo > 0),
            "note": (
                "Counterfactual flip rate under protected-attribute perturbation. "
                "Measurement only — not a per-response moral verdict."
            ),
        }


_DEFAULT_WINDOW = FlipWindow()


def counterfactual_flip(
    decide_fn: Callable[[str], str],
    *,
    baseline_attr: str,
    perturbed_attrs: list[str],
    window: FlipWindow | None = None,
) -> dict[str, Any]:
    """Run decide_fn(attr) for baseline and perturbations; record flips.

    `decide_fn` returns an actuator string (or any decision token). A flip is
    any perturbation whose token differs from the baseline token.
    """
    win = window or _DEFAULT_WINDOW
    baseline = decide_fn(baseline_attr)
    flipped_any = False
    details = []
    for attr in perturbed_attrs:
        got = decide_fn(attr)
        flipped = got != baseline
        flipped_any = flipped_any or flipped
        details.append({"attr": attr, "decision": got, "flipped": flipped})
    win.record(flipped_any)
    out = win.summary()
    out["baseline"] = {"attr": baseline_attr, "decision": baseline}
    out["perturbations"] = details
    return out
