"""Phase 5 — deadline-driven lanes (TDD).

Lane 1 hard 30–60 ms deterministic; Lane 2 near-line NLI slot; Lane 3 async.
Deadline miss → UNKNOWN, resolved by that tier's fail stance — never a
global default. A slow probabilistic check never overturns a fast
deterministic one.
"""
from __future__ import annotations

import asyncio
import inspect
import statistics
import time

from controlplane.interlock import COL_UNKNOWN
from controlplane.lanes import (
    LANE1_DEADLINE_MS,
    LANE2_DEADLINE_MS,
    gather_lanes,
    merge_bindings,
    nli_adapter_stub,
    resolve_deadline_miss,
    run_lanes,
)
from controlplane.ledger import EvidenceLedger
from controlplane.models import (
    Action,
    Actuator,
    AssertionStrength,
    Binding,
    BlastTier,
    Claim,
    ClaimKind,
    Principal,
    Verdict,
)
from controlplane.pipeline import ControlPlaneGate


def _percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def _ledger_with_unknown_claim(action_id: str, tier: BlastTier) -> tuple[EvidenceLedger, Action]:
    led = EvidenceLedger.begin(
        "lane-timeout",
        Principal(id="u", clearance=frozenset()),
        "x",
    )
    claim = Claim(
        "c1",
        "flagged textual claim awaiting NLI",
        ClaimKind.TEXTUAL,
        AssertionStrength.CATEGORICAL,
        {action_id: 1.0},
    )
    led.claims[claim.claim_id] = claim
    action = Action(action_id, action_id, tier, irreversibility=tier in (BlastTier.R2, BlastTier.R3))
    return led, action


def test_lane1_deadline_is_hard_30_to_60_ms():
    assert 30.0 <= LANE1_DEADLINE_MS <= 60.0
    assert LANE2_DEADLINE_MS >= 100.0
    assert LANE2_DEADLINE_MS <= 400.0


def test_gather_lanes_uses_asyncio_gather():
    source = inspect.getsource(gather_lanes)
    assert "asyncio.gather" in source


def test_slow_lane2_times_out_unknown_inside_budget():
    """Artificially slow Lane 2 must not stall the decision past its deadline."""

    async def lane1():
        return {"ok": True}

    slow = nli_adapter_stub(delay_ms=2000.0, verdict=Verdict.SUPPORTED)
    t0 = time.perf_counter()
    bundle = run_lanes(
        lane1=lane1,
        lane2=slow,
        lane2_deadline_ms=50.0,
        lane1_deadline_ms=LANE1_DEADLINE_MS,
    )
    wall_ms = (time.perf_counter() - t0) * 1000.0

    assert bundle.lane2.timed_out is True
    assert bundle.lane2.verdict == Verdict.UNKNOWN
    assert bundle.elapsed_ms < 400.0
    assert wall_ms < 400.0
    assert bundle.lane1.timed_out is False
    assert bundle.lane1.payload == {"ok": True}


def test_timeout_unknown_resolved_by_tier_fail_stance_not_global_default():
    """Same deadline miss must not collapse to one global actuator."""
    led_r3, a_r3 = _ledger_with_unknown_claim("issue_refund", BlastTier.R3)
    led_r1, a_r1 = _ledger_with_unknown_claim("show_text", BlastTier.R1)
    led_r0, a_r0 = _ledger_with_unknown_claim("draft", BlastTier.R0)

    d_r3 = resolve_deadline_miss(
        led_r3, a_r3, fail_stance="closed_escalate", timed_out_claim_ids=("c1",)
    )
    d_r1 = resolve_deadline_miss(
        led_r1, a_r1, fail_stance="open_annotate", timed_out_claim_ids=("c1",)
    )
    d_r0 = resolve_deadline_miss(
        led_r0, a_r0, fail_stance="open_annotate", timed_out_claim_ids=("c1",)
    )

    assert led_r3.bindings["c1"].verdict == Verdict.UNKNOWN
    assert d_r3.matrix_col == COL_UNKNOWN
    assert d_r3.actuator == Actuator.ESCALATE
    assert d_r1.actuator == Actuator.PASS_ANNOTATE
    assert d_r0.actuator == Actuator.PASS
    # Distinct actuators ⇒ not a global default (Block-everything or Pass-everything).
    assert len({d_r3.actuator, d_r1.actuator, d_r0.actuator}) == 3
    assert Actuator.BLOCK not in {d_r3.actuator, d_r1.actuator, d_r0.actuator}


def test_slow_probabilistic_never_overturns_fast_deterministic_merge():
    lane1 = {
        "amount": Binding(
            "amount", ("s1",), "numeric", Verdict.CONTRADICTED, "unit mismatch"
        )
    }
    lane2 = {
        "amount": Binding(
            "amount", ("s1",), "nli-stub", Verdict.SUPPORTED, "nli agrees"
        )
    }
    merged = merge_bindings(lane1, lane2, lane2_timed_out=False)
    assert merged["amount"].verdict == Verdict.CONTRADICTED
    assert merged["amount"].method == "numeric"

    merged_timeout = merge_bindings(lane1, None, lane2_timed_out=True)
    assert merged_timeout["amount"].verdict == Verdict.CONTRADICTED


def test_slow_probabilistic_never_overturns_fast_deterministic_runtime():
    async def lane1():
        return {
            "amount": Binding(
                "amount", ("s1",), "numeric", Verdict.CONTRADICTED, "mismatch"
            )
        }

    slow_supported = nli_adapter_stub(delay_ms=1500.0, verdict=Verdict.SUPPORTED)
    bundle = run_lanes(
        lane1=lane1,
        lane2=slow_supported,
        lane2_deadline_ms=40.0,
    )
    assert bundle.lane2.timed_out is True
    merged = merge_bindings(
        bundle.lane1.payload, bundle.lane2.payload, lane2_timed_out=True
    )
    assert merged["amount"].verdict == Verdict.CONTRADICTED
    assert merged["amount"].method == "numeric"


def test_nli_may_fill_lane1_unknown_only_when_it_lands():
    lane1 = {
        "hedge": Binding("hedge", (), "bm25+lexical", Verdict.UNKNOWN, "middle band")
    }
    lane2 = {
        "hedge": Binding("hedge", ("s1",), "nli-stub", Verdict.SUPPORTED, "nli")
    }
    filled = merge_bindings(lane1, lane2, lane2_timed_out=False)
    assert filled["hedge"].verdict == Verdict.SUPPORTED
    assert filled["hedge"].method == "nli-stub"

    stayed = merge_bindings(lane1, None, lane2_timed_out=True)
    assert stayed["hedge"].verdict == Verdict.UNKNOWN


def test_lanes_run_in_parallel():
    async def pause():
        await asyncio.sleep(0.10)
        return True

    bundle = run_lanes(
        lane1=pause,
        lane2=pause,
        lane1_deadline_ms=500.0,
        lane2_deadline_ms=500.0,
    )
    # Sequential would be ≥ 200 ms; gather must overlap.
    assert bundle.elapsed_ms < 170.0
    assert bundle.lane1.timed_out is False
    assert bundle.lane2.timed_out is False


def test_lane3_async_does_not_block_critical_path():
    started = {"lane3": False}

    async def hanging():
        started["lane3"] = True
        await asyncio.sleep(2.0)
        return "shadow"

    t0 = time.perf_counter()
    bundle = run_lanes(
        lane1=lambda: 1,
        lane2=lambda: 2,
        lane3=hanging,
    )
    wall_ms = (time.perf_counter() - t0) * 1000.0
    assert started["lane3"] is True
    assert bundle.lane3.timed_out is False
    assert wall_ms < 500.0
    assert bundle.elapsed_ms < 500.0


def test_nli_adapter_slot_is_injectable():
    fast = nli_adapter_stub(delay_ms=0.0, verdict=Verdict.UNKNOWN)
    slow = nli_adapter_stub(delay_ms=2000.0, verdict=Verdict.SUPPORTED)
    quick = run_lanes(lane1=lambda: True, lane2=fast, lane2_deadline_ms=200.0)
    assert quick.lane2.timed_out is False
    delayed = run_lanes(lane1=lambda: True, lane2=slow, lane2_deadline_ms=40.0)
    assert delayed.lane2.timed_out is True
    assert delayed.lane2.verdict == Verdict.UNKNOWN


def test_lane1_p95_inside_declared_budget():
    async def cheap():
        return True

    run_lanes(lane1=cheap, lane2=lambda: None)  # warm
    samples: list[float] = []
    for _ in range(40):
        bundle = run_lanes(lane1=cheap, lane2=lambda: None)
        samples.append(bundle.lane1.elapsed_ms)
    p95 = _percentile(sorted(samples), 95)
    assert p95 <= LANE1_DEADLINE_MS


def test_pipeline_refund_unchanged_with_lanes():
    gate = ControlPlaneGate()
    result = gate.run_refund_demo(mode_override="enforce")
    assert result.decisions["show_text"].actuator == Actuator.EDIT
    assert result.decisions["issue_refund"].actuator == Actuator.ESCALATE
    assert result.would_hold is True
    pub = result.public_dict()
    assert pub["lanes"]["lane1"]["timed_out"] is False
    assert result.latency_ms < 200.0


def test_pipeline_slow_lane2_decision_still_via_unknown():
    """Injected slow NLI cannot stall or overturn the refund dual-action."""
    slow = nli_adapter_stub(delay_ms=2000.0, verdict=Verdict.SUPPORTED)
    gate = ControlPlaneGate(nli_adapter=slow, lane2_deadline_ms=40.0)
    t0 = time.perf_counter()
    result = gate.run_refund_demo(mode_override="enforce")
    wall_ms = (time.perf_counter() - t0) * 1000.0
    assert result.decisions["show_text"].actuator == Actuator.EDIT
    assert result.decisions["issue_refund"].actuator == Actuator.ESCALATE
    assert result.decisions["issue_refund"].actuator != Actuator.BLOCK
    assert wall_ms < 400.0
    assert result.lanes is not None
    assert result.lanes["lane2"]["timed_out"] is True
    assert result.lanes["lane2"]["verdict"] == "UNKNOWN"
    # Clause 7.2 stays UNSUPPORTED (Lane 1 deterministic), not flipped by NLI.
    assert result.ledger.bindings["clause_72"].verdict == Verdict.UNSUPPORTED
    assert "nli" not in result.ledger.bindings["clause_72"].method
    assert result.ledger.bindings["amount"].verdict == Verdict.SUPPORTED
    assert "numeric" in result.ledger.bindings["amount"].method
