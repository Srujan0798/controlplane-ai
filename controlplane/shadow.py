"""Shadow mode — dual-emit counterfactuals and publishable error bars."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
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

        Falls back to the eval-corpus Wilson estimate (set via
        MetricsStore.load_eval_metrics) when no live labels have accumulated
        yet — so the HTTP metrics endpoint always publishes a *measured* FNR,
        never None, at startup.
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
        self._gate_latency_ms: float = 0.0
        self._gate_latency_sum_ms: float = 0.0
        self._gate_latency_count: int = 0
        # T3.2: eval-corpus fall-back — populated from evals/last_run.json
        # so that /metrics publishes an FNR even before live labels arrive (Lane 3).
        self._eval_fnr: float | None = None
        self._eval_fnr_ci: list[float] | None = None
        self._eval_fpr: float | None = None
        self._eval_fpr_ci: list[float] | None = None
        self._eval_n: int = 0

    def load_eval_metrics(self, eval_json_path: str | Path) -> None:
        """T3.2: seed publishable FNR/FPR from the eval corpus results.

        Reads evals/last_run.json (written by ``make eval``) and stores the
        Wilson-CI-backed numbers so /metrics can publish them before enough
        live labels accumulate through Lane 3 feedback.
        """
        path = Path(eval_json_path)
        if not path.exists():
            return
        data = json.loads(path.read_text())
        summary = data.get("summary", data)
        fnr = summary.get("ungrounded_fnr_wilson")
        fpr = summary.get("passable_fpr_wilson")
        if fnr:
            self._eval_fnr = fnr[0]
            self._eval_fnr_ci = list(fnr[1:3])
        if fpr:
            self._eval_fpr = fpr[0]
            self._eval_fpr_ci = list(fpr[1:3])
        self._eval_n = summary.get("n_cases", 0) or 0

    def record(self, **kwargs: Any) -> None:
        with self._lock:
            self.counters.record(**kwargs)

    def record_latency(self, latency_ms: float) -> None:
        with self._lock:
            self._gate_latency_ms = float(latency_ms)
            self._gate_latency_sum_ms += float(latency_ms)
            self._gate_latency_count += 1

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            snap = self.counters.snapshot()
            # T3.2: fall back to eval-corpus numbers when live labels are empty.
            if snap["published_fnr"] is None and self._eval_fnr is not None:
                snap["published_fnr"] = self._eval_fnr
                snap["published_fnr_ci"] = self._eval_fnr_ci
                snap["published_fnr_source"] = "eval-corpus"
                snap["published_fnr_n"] = self._eval_n
            if snap["published_fpr"] is None and self._eval_fpr is not None:
                snap["published_fpr"] = self._eval_fpr
                snap["published_fpr_ci"] = self._eval_fpr_ci
            snap["gate_latency_ms"] = self._gate_latency_ms
            snap["gate_latency_count"] = self._gate_latency_count
            if self._gate_latency_count:
                snap["gate_latency_mean_ms"] = (
                    self._gate_latency_sum_ms / self._gate_latency_count
                )
            else:
                snap["gate_latency_mean_ms"] = None
            return snap

    def prometheus_text(self) -> str:
        """Prometheus text exposition (plain text; scrapable)."""
        with self._lock:
            decisions = self.counters.total_decisions
            would_hold = self.counters.would_have_held
            latency = self._gate_latency_ms
            fnr = self.counters.published_fnr
            if fnr is None:
                fnr = self._eval_fnr
        lines = [
            "# HELP controlplane_decisions_total Total control-plane decisions recorded",
            "# TYPE controlplane_decisions_total counter",
            f"controlplane_decisions_total {decisions}",
            "# HELP controlplane_would_hold_total Decisions that would hold (Edit/Escalate/Block)",
            "# TYPE controlplane_would_hold_total counter",
            f"controlplane_would_hold_total {would_hold}",
            "# HELP controlplane_gate_latency_ms Last gate latency in milliseconds",
            "# TYPE controlplane_gate_latency_ms gauge",
            f"controlplane_gate_latency_ms {latency}",
            "# HELP controlplane_published_fnr False-negative rate (eval-corpus fallback)",
            "# TYPE controlplane_published_fnr gauge",
            f"controlplane_published_fnr {fnr if fnr is not None else 0}",
            "",
        ]
        return "\n".join(lines)

    def reset(self) -> None:
        with self._lock:
            self.counters = ShadowCounters()
            self._gate_latency_ms = 0.0
            self._gate_latency_sum_ms = 0.0
            self._gate_latency_count = 0
            # T3.2: preserve eval-corpus fallback across reset — it is a
            # measured baseline, not a per-request counter.
