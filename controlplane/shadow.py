"""Shadow mode — dual-emit counterfactuals and publishable error bars."""
from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from controlplane.models import Actuator


HOLDING_ACTUATORS = frozenset({Actuator.BLOCK, Actuator.ESCALATE, Actuator.EDIT})


@dataclass
class ShadowCounters:
    """Would-have vs ungated — the skeptical-stakeholder surface."""

    total_decisions: int = 0
    would_have_held: int = 0
    would_have_passed: int = 0
    enforced_holds: int = 0
    enforced_passes: int = 0
    # Ground-truth labels arrive from adjudicator / human override (Lane 3).
    labeled_holds: int = 0
    true_positive_holds: int = 0
    false_positive_holds: int = 0
    labeled_passes: int = 0
    false_negative_passes: int = 0
    by_use_case: dict[str, dict[str, int]] = field(default_factory=dict)
    by_actuator: dict[str, int] = field(default_factory=dict)

    def record(
        self,
        *,
        use_case: str,
        actuator: Actuator,
        mode: str,
        labeled_should_hold: bool | None = None,
    ) -> None:
        self.total_decisions += 1
        hold = actuator in HOLDING_ACTUATORS
        self.by_actuator[actuator.value] = self.by_actuator.get(actuator.value, 0) + 1
        bucket = self.by_use_case.setdefault(
            use_case,
            {"total": 0, "would_hold": 0, "enforced_hold": 0},
        )
        bucket["total"] += 1

        if hold:
            self.would_have_held += 1
            bucket["would_hold"] += 1
        else:
            self.would_have_passed += 1

        if mode == "enforce":
            if hold:
                self.enforced_holds += 1
                bucket["enforced_hold"] += 1
            else:
                self.enforced_passes += 1

        if labeled_should_hold is None:
            return
        if hold:
            self.labeled_holds += 1
            if labeled_should_hold:
                self.true_positive_holds += 1
            else:
                self.false_positive_holds += 1
        else:
            self.labeled_passes += 1
            if labeled_should_hold:
                self.false_negative_passes += 1

    @property
    def published_fnr(self) -> float | None:
        """False-negative rate among labeled passes that should have held.

        Shape of the claim we publish — never a single accuracy number.
        """
        denom = self.true_positive_holds + self.false_negative_passes
        if denom == 0:
            return None
        return self.false_negative_passes / denom

    @property
    def published_fpr(self) -> float | None:
        denom = self.true_positive_holds + self.false_positive_holds
        if denom == 0:
            return None
        return self.false_positive_holds / denom

    def snapshot(self) -> dict[str, Any]:
        return {
            "total_decisions": self.total_decisions,
            "would_have_held": self.would_have_held,
            "would_have_passed": self.would_have_passed,
            "enforced_holds": self.enforced_holds,
            "enforced_passes": self.enforced_passes,
            "labeled_holds": self.labeled_holds,
            "true_positive_holds": self.true_positive_holds,
            "false_positive_holds": self.false_positive_holds,
            "labeled_passes": self.labeled_passes,
            "false_negative_passes": self.false_negative_passes,
            "published_fnr": self.published_fnr,
            "published_fpr": self.published_fpr,
            "fnr_claim_shape": (
                "On this route we catch <measured>% of ungrounded claims at 40ms p50 "
                "— and here is the <measured>% we don't."
            ),
            "by_use_case": self.by_use_case,
            "by_actuator": self.by_actuator,
            "note": (
                "Shadow is the default deployment mode. Numbers without labels are "
                "counterfactuals (would-have), not ground truth."
            ),
        }


class MetricsStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self.counters = ShadowCounters()

    def record(self, **kwargs: Any) -> None:
        with self._lock:
            self.counters.record(**kwargs)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return self.counters.snapshot()

    def reset(self) -> None:
        with self._lock:
            self.counters = ShadowCounters()
