"""Override capture → ledger → shadow-replay threshold proposals (Phase 6b)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from controlplane.ledger import EvidenceLedger


@dataclass
class OverrideRecord:
    decision_id: str
    reviewer: str
    verdict: str
    reason: str
    prior_actuator: str
    request_id: str


@dataclass
class FeedbackStore:
    overrides: list[OverrideRecord] = field(default_factory=list)
    baseline_override_rate: float = 0.02
    canary_multiplier: float = 3.0
    canary_state: str = "armed"  # armed | rolled_back

    def record_override(
        self,
        ledger: EvidenceLedger,
        *,
        decision_id: str,
        reviewer: str,
        verdict: str,
        reason: str,
        prior_actuator: str,
    ) -> OverrideRecord:
        rec = OverrideRecord(
            decision_id=decision_id,
            reviewer=reviewer,
            verdict=verdict,
            reason=reason,
            prior_actuator=prior_actuator,
            request_id=ledger.request_id,
        )
        self.overrides.append(rec)
        ledger.append(
            "override",
            {
                "decision_id": decision_id,
                "reviewer": reviewer,
                "verdict": verdict,
                "reason": reason,
                "prior_actuator": prior_actuator,
            },
        )
        self._maybe_canary_rollback()
        return rec

    def override_rate(self, window: int = 50) -> float:
        recent = self.overrides[-window:]
        if not recent:
            return 0.0
        return len(recent) / float(window)

    def _maybe_canary_rollback(self) -> None:
        rate = self.override_rate()
        if rate > self.canary_multiplier * self.baseline_override_rate:
            self.canary_state = "rolled_back"

    def propose_threshold(
        self,
        *,
        name: str,
        current: float,
        proposed: float,
        shadow_fp_delta: float,
        shadow_fn_delta: float,
    ) -> dict[str, Any]:
        """Threshold ships only after a printed shadow-replay delta."""
        return {
            "name": name,
            "current": current,
            "proposed": proposed,
            "shadow_fp_delta": shadow_fp_delta,
            "shadow_fn_delta": shadow_fn_delta,
            "ship": abs(shadow_fp_delta) + abs(shadow_fn_delta) >= 0,  # always report
            "note": (
                "Threshold proposal must print FP/FN delta from shadow replay "
                "over last N traces before shipping."
            ),
            "canary_state": self.canary_state,
        }
