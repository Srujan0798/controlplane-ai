"""T5.4 — canary with auto-rollback (RED first).

Acceptance: rollback fires at >3x baseline override rate and NOT below it.

We require an explicit canary state machine (armed | rolled_back | recovered)
with a method that, given a measured override rate, transitions correctly and
refuses to serve traffic while rolled_back.
"""
from __future__ import annotations

from controlplane.feedback import Canary, FeedbackStore


def test_canary_rolls_back_above_3x_baseline():
    c = Canary(baseline_override_rate=0.02, multiplier=3.0)
    # 3x baseline == 0.06; strictly above triggers rollback.
    c.observe(rate=0.07)
    assert c.state == "rolled_back"


def test_canary_stays_armed_at_or_below_3x():
    c = Canary(baseline_override_rate=0.02, multiplier=3.0)
    c.observe(rate=0.06)  # exactly 3x -> not above
    assert c.state == "armed"
    c.observe(rate=0.01)
    assert c.state == "armed"


def test_canary_recovers_when_rate_drops():
    c = Canary(baseline_override_rate=0.02, multiplier=3.0)
    c.observe(rate=0.10)
    assert c.state == "rolled_back"
    c.observe(rate=0.01)  # recovered below baseline
    assert c.state == "recovered"


def test_canary_blocks_serving_while_rolled_back():
    c = Canary(baseline_override_rate=0.02, multiplier=3.0)
    c.observe(rate=0.10)
    assert c.serving_allowed() is False


def test_feedback_store_exposes_canary_state_machine():
    store = FeedbackStore()
    store.canary.observe(rate=0.10)
    assert store.canary_state == "rolled_back"
    assert store.canary.serving_allowed() is False


def test_canary_threshold_exactly_3x_not_above():
    c = Canary(baseline_override_rate=0.05, multiplier=3.0)
    c.observe(rate=0.15)  # exactly 3x
    assert c.state == "armed"
