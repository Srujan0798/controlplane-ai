"""Override capture → ledger → shadow-replay threshold proposals (Phase 6b).

T5.2 (override capture): reviewer overrides are written into the chained ledger
so they are tamper-evident and become labels feeding the eval corpus.

T5.3 (threshold proposal behind a shadow replay): ARCHITECTURE §4 — no threshold
ships without a shadow replay over the last N traces printing the FP/FN delta.
``propose_threshold`` REFUSES to ship unless ``record_shadow_replay`` has produced
a measured delta for that named threshold.

T5.4 (canary): per-route canary with auto-rollback when the human-override rate
exceeds 3x baseline. Explicit state machine.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from controlplane.ledger import EvidenceLedger


@dataclass
class Canary:
    """Per-route canary with explicit auto-rollback state machine (T5.4).

    States: armed -> rolled_back (override rate > multiplier*baseline) ->
    recovered (rate drops back to/below baseline). While rolled_back, serving is
    refused so the regressed route is taken out of the loop automatically.
    """

    baseline_override_rate: float = 0.02
    multiplier: float = 3.0
    state: str = "armed"  # armed | rolled_back | recovered

    def observe(self, *, rate: float) -> str:
        threshold = self.multiplier * self.baseline_override_rate
        if rate > threshold:
            self.state = "rolled_back"
        elif self.state == "rolled_back" and rate <= self.baseline_override_rate:
            self.state = "recovered"
        elif self.state == "rolled_back":
            # still elevated but not above 3x — stay rolled_back until recovered
            self.state = "rolled_back"
        return self.state

    def serving_allowed(self) -> bool:
        return self.state != "rolled_back"


@dataclass
class OverrideRecord:
    decision_id: str
    reviewer: str
    verdict: str
    reason: str
    prior_actuator: str
    request_id: str


@dataclass
class ShadowReplay:
    name: str
    traces: int
    fp_delta: float
    fn_delta: float


@dataclass
class FeedbackStore:
    overrides: list[OverrideRecord] = field(default_factory=list)
    replays: dict[str, ShadowReplay] = field(default_factory=dict)
    baseline_override_rate: float = 0.02
    canary_multiplier: float = 3.0
    canary: Canary = field(default_factory=Canary)

    def __post_init__(self) -> None:
        self.canary.baseline_override_rate = self.baseline_override_rate
        self.canary.multiplier = self.canary_multiplier

    @property
    def canary_state(self) -> str:
        return self.canary.state

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

    def record_shadow_replay(
        self,
        *,
        name: str,
        traces: int,
        fp_delta: float,
        fn_delta: float,
        ledger: EvidenceLedger | None = None,
    ) -> ShadowReplay:
        """Record a measured shadow replay over N traces for a named threshold.

        This is the ONLY way to unblock ``propose_threshold`` for ``name``.
        """
        replay = ShadowReplay(name=name, traces=traces, fp_delta=fp_delta, fn_delta=fn_delta)
        self.replays[name] = replay
        if ledger is not None:
            ledger.append(
                "shadow_replay",
                {
                    "name": name,
                    "traces": traces,
                    "fp_delta": fp_delta,
                    "fn_delta": fn_delta,
                },
            )
        return replay

    def propose_threshold(
        self,
        *,
        name: str,
        current: float,
        proposed: float,
        shadow_fp_delta: float | None = None,
        shadow_fn_delta: float | None = None,
    ) -> dict[str, Any]:
        """Threshold ships only after a printed shadow-replay delta (T5.3).

        Refuses (ship=False) unless a recorded replay exists for ``name`` and the
        supplied deltas match the recorded measurement.
        """
        replay = self.replays.get(name)
        if replay is None:
            return {
                "name": name,
                "current": current,
                "proposed": proposed,
                "ship": False,
                "status": "refused: no shadow replay recorded for this threshold",
                "canary_state": self.canary_state,
                "note": (
                    "ARCHITECTURE §4 — a threshold change is refused unless a shadow "
                    "replay over the last N traces printed the FP/FN delta first."
                ),
            }
        if shadow_fp_delta != replay.fp_delta or shadow_fn_delta != replay.fn_delta:
            return {
                "name": name,
                "current": current,
                "proposed": proposed,
                "ship": False,
                "status": "refused: supplied delta does not match recorded replay",
                "replay_traces": replay.traces,
                "canary_state": self.canary_state,
                "note": "Supplied FP/FN delta must equal the measured replay delta.",
            }
        return {
            "name": name,
            "current": current,
            "proposed": proposed,
            "shadow_fp_delta": shadow_fp_delta,
            "shadow_fn_delta": shadow_fn_delta,
            "replay_traces": replay.traces,
            "ship": True,
            "status": "approved: shadow replay delta on record",
            "canary_state": self.canary_state,
            "note": "Threshold proposal carries a measured shadow-replay FP/FN delta.",
        }

    def override_rate(self, window: int = 50) -> float:
        recent = self.overrides[-window:]
        if not recent:
            return 0.0
        return len(recent) / float(window)

    def _maybe_canary_rollback(self) -> None:
        rate = self.override_rate()
        self.canary.observe(rate=rate)
