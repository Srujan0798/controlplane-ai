"""Deadline-driven lanes. Interlock remains sole decider.

ARCHITECTURE §5/§6: Lane 1 inline, hard 30–60 ms p95, deterministic only.
Lane 2 near-line (100–400 ms) NLI adapter slot. Lane 3 async (bias,
calibration, shadow). Deadline miss → UNKNOWN, resolved by that tier's
fail stance — never a global default. A slow probabilistic check never
overturns a fast deterministic one.
"""
from __future__ import annotations

import asyncio
import inspect
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from controlplane.interlock import decide
from controlplane.ledger import EvidenceLedger
from controlplane.models import Action, Binding, Decision, Verdict

# Hard Lane-1 ceiling (ARCHITECTURE §5: 30–60 ms p95). Never quote as p95 of 40.
LANE1_DEADLINE_MS = 60.0
# Near-line NLI ceiling (ARCHITECTURE §5: 100–400 ms).
LANE2_DEADLINE_MS = 400.0

Work = Callable[[], Any]


@dataclass(frozen=True)
class LaneOutcome:
    lane: str
    timed_out: bool
    elapsed_ms: float
    payload: Any = None
    verdict: Verdict | None = None  # UNKNOWN on deadline miss

    def as_public(self) -> dict[str, Any]:
        return {
            "lane": self.lane,
            "timed_out": self.timed_out,
            "elapsed_ms": round(self.elapsed_ms, 3),
            "verdict": None if self.verdict is None else self.verdict.value,
        }


@dataclass(frozen=True)
class LaneBundle:
    lane1: LaneOutcome
    lane2: LaneOutcome
    lane3: LaneOutcome
    elapsed_ms: float
    bindings: dict[str, Binding] = field(default_factory=dict)

    def as_public(self) -> dict[str, Any]:
        return {
            "lane1": self.lane1.as_public(),
            "lane2": self.lane2.as_public(),
            "lane3": self.lane3.as_public(),
            "elapsed_ms": round(self.elapsed_ms, 3),
        }


def nli_adapter_stub(
    *,
    delay_ms: float = 0.0,
    verdict: Verdict = Verdict.UNKNOWN,
    claim_ids: tuple[str, ...] = (),
) -> Callable[[], Any]:
    """Near-line NLI slot. Default is instant; tests inject delay_ms."""

    async def _run() -> dict[str, Binding]:
        if delay_ms > 0:
            await asyncio.sleep(delay_ms / 1000.0)
        return {
            cid: Binding(
                cid, (), "nli-stub", verdict, "near-line NLI adapter stub"
            )
            for cid in claim_ids
        }

    return _run


def merge_bindings(
    lane1_bindings: Mapping[str, Binding] | None,
    lane2_bindings: Mapping[str, Binding] | None,
    *,
    lane2_timed_out: bool,
) -> dict[str, Binding]:
    """Lane 1 deterministic verdicts are sticky.

    Lane 2 may fill UNKNOWN when it lands in time. A timeout writes UNKNOWN
    only for claims Lane 1 did not already decide. Never a global default.
    """
    merged: dict[str, Binding] = dict(lane1_bindings or {})
    if lane2_timed_out:
        for cid, _b2 in (lane2_bindings or {}).items():
            existing = merged.get(cid)
            if existing is None:
                merged[cid] = Binding(
                    cid,
                    (),
                    "lane-timeout",
                    Verdict.UNKNOWN,
                    "deadline miss → UNKNOWN",
                )
        return merged
    for cid, b2 in (lane2_bindings or {}).items():
        b1 = merged.get(cid)
        if b1 is None or b1.verdict == Verdict.UNKNOWN:
            merged[cid] = b2
    return merged


def resolve_deadline_miss(
    ledger: EvidenceLedger,
    action: Action,
    *,
    fail_stance: str,
    timed_out_claim_ids: tuple[str, ...],
) -> Decision:
    """Write UNKNOWN for a miss, then the interlock + fail stance decide.

    Does not pick an actuator itself — that would be a global default.
    """
    for cid in timed_out_claim_ids:
        existing = ledger.bindings.get(cid)
        if existing is not None and existing.verdict != Verdict.UNKNOWN:
            continue
        span_ids = existing.span_ids if existing is not None else ()
        ledger.bindings[cid] = Binding(
            cid,
            span_ids,
            "lane-timeout",
            Verdict.UNKNOWN,
            "deadline miss → UNKNOWN",
        )
    return decide(ledger, action, fail_stance=fail_stance)


async def _call(work: Work | None) -> Any:
    if work is None:
        return None
    result = work()
    if inspect.isawaitable(result):
        return await result
    return result


async def _run_with_deadline(
    name: str, work: Work | None, deadline_ms: float
) -> LaneOutcome:
    t0 = time.perf_counter()
    if work is None:
        return LaneOutcome(name, False, 0.0, None, None)
    try:
        payload = await asyncio.wait_for(
            _call(work), timeout=max(deadline_ms, 0.0) / 1000.0
        )
        elapsed = (time.perf_counter() - t0) * 1000.0
        return LaneOutcome(name, False, elapsed, payload, None)
    except asyncio.TimeoutError:
        elapsed = (time.perf_counter() - t0) * 1000.0
        return LaneOutcome(name, True, elapsed, None, Verdict.UNKNOWN)


def _as_binding_map(payload: Any) -> dict[str, Binding]:
    if not isinstance(payload, dict) or not payload:
        return {}
    if all(isinstance(v, Binding) for v in payload.values()):
        return dict(payload)
    inner = payload.get("bindings")
    if isinstance(inner, dict) and all(isinstance(v, Binding) for v in inner.values()):
        return dict(inner)
    return {}


def _lane3_outcome(
    work: Work | None,
    task: asyncio.Task[Any] | None,
    elapsed_ms: float,
) -> LaneOutcome:
    if work is None or task is None:
        return LaneOutcome("lane3", False, 0.0, None, None)
    if task.done() and not task.cancelled():
        try:
            return LaneOutcome("lane3", False, elapsed_ms, task.result(), None)
        except Exception:
            return LaneOutcome("lane3", False, elapsed_ms, None, None)
    return LaneOutcome("lane3", False, elapsed_ms, None, None)


async def gather_lanes(
    *,
    lane1: Work,
    lane2: Work | None = None,
    lane3: Work | None = None,
    lane1_deadline_ms: float = LANE1_DEADLINE_MS,
    lane2_deadline_ms: float = LANE2_DEADLINE_MS,
) -> LaneBundle:
    """Run lanes concurrently. Per-lane wait_for; Lane 3 is not on the path."""
    t0 = time.perf_counter()
    lane3_task: asyncio.Task[Any] | None = None
    if lane3 is not None:
        lane3_task = asyncio.create_task(_call(lane3))
        await asyncio.sleep(0)
    try:
        lane1_out, lane2_out = await asyncio.gather(
            _run_with_deadline("lane1", lane1, lane1_deadline_ms),
            _run_with_deadline("lane2", lane2, lane2_deadline_ms),
        )
    finally:
        if lane3_task is not None and not lane3_task.done():
            lane3_task.cancel()
            try:
                await lane3_task
            except asyncio.CancelledError:
                pass
            except Exception:
                pass

    elapsed = (time.perf_counter() - t0) * 1000.0
    bindings = merge_bindings(
        _as_binding_map(lane1_out.payload),
        _as_binding_map(lane2_out.payload),
        lane2_timed_out=lane2_out.timed_out,
    )
    return LaneBundle(
        lane1=lane1_out,
        lane2=lane2_out,
        lane3=_lane3_outcome(lane3, lane3_task, elapsed),
        elapsed_ms=elapsed,
        bindings=bindings,
    )


def run_lanes(
    *,
    lane1: Work,
    lane2: Work | None = None,
    lane3: Work | None = None,
    lane1_deadline_ms: float = LANE1_DEADLINE_MS,
    lane2_deadline_ms: float = LANE2_DEADLINE_MS,
) -> LaneBundle:
    """Sync wrapper. Safe from pytest and from a running FastAPI loop."""

    def _in_thread() -> LaneBundle:
        return asyncio.run(
            gather_lanes(
                lane1=lane1,
                lane2=lane2,
                lane3=lane3,
                lane1_deadline_ms=lane1_deadline_ms,
                lane2_deadline_ms=lane2_deadline_ms,
            )
        )

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return _in_thread()

    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(_in_thread).result()
