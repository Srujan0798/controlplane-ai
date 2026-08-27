"""Hold-back buffer — trailing delay; failures inside the window never release.

Architecture §5: stream on a ~150–300ms trailing delay. Speculative
verification, never speculative release. Lane 1: record intended release
time; do not sleep.
"""
from __future__ import annotations

import time
from typing import Any

from controlplane.models import Actuator

IRREVERSIBLE_ACTUATORS = frozenset(
    {Actuator.EDIT, Actuator.ESCALATE, Actuator.BLOCK}
)
IRREVERSIBLE_VALUES = frozenset(a.value for a in IRREVERSIBLE_ACTUATORS)


def _actuator_name(actuator: Any) -> str | None:
    if actuator is None:
        return None
    if hasattr(actuator, "value"):
        return str(actuator.value)
    text = str(actuator)
    return text or None


class HoldBackBuffer:
    """In-memory hold-back. Failures never emit; irreversible actuators stay held."""

    def __init__(self, delay_ms: int = 200) -> None:
        self.delay_ms = int(delay_ms)
        self.intended_release_at: float | None = None
        self._last: dict[str, Any] | None = None

    def admit(
        self,
        text: str,
        ok: bool,
        actuator: str | Actuator | None = None,
    ) -> dict[str, Any]:
        now = time.time()
        self.intended_release_at = now + (self.delay_ms / 1000.0)
        name = _actuator_name(actuator)
        irreversible = bool(name) and name in IRREVERSIBLE_VALUES
        held = (not ok) or irreversible
        released = not held
        result: dict[str, Any] = {
            "released": released,
            "held": held,
            "delay_ms": self.delay_ms,
        }
        if name is not None:
            result["actuator"] = name
        result["intended_release_at"] = self.intended_release_at
        result["text_len"] = len(text or "")
        self._last = result
        return result


def admit_for_decisions(
    text: str,
    decisions: dict[str, Any],
    *,
    delay_ms: int = 200,
) -> dict[str, Any]:
    """Hold irreversible path when any decision is Edit / Escalate / Block."""
    rank = {"Edit": 1, "Escalate": 2, "Block": 3}
    worst: str | None = None
    worst_rank = 0
    for item in decisions.values():
        raw = item.actuator if hasattr(item, "actuator") else None
        if raw is None and isinstance(item, dict):
            raw = item.get("actuator")
        name = _actuator_name(raw)
        if name is None:
            continue
        r = rank.get(name, 0)
        if r > worst_rank:
            worst = name
            worst_rank = r
    ok = worst is None
    return HoldBackBuffer(delay_ms=delay_ms).admit(text, ok, actuator=worst)
