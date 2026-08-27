# Hall of Shame — Failure Pattern Archive

> Learning tool, not blame tool.

## Pattern 1: Fail-open admission (unproven action → Pass)

- **Date:** 2026-08-24
- **Test / Component:** `tests/test_fail_closed.py`
- **Severity:** Critical
- **Root cause:** Paths let actions through without proof / entitlement.
- **Impact:** Irreversible action could Pass when it must Escalate/Block.
- **Fix:** Fail-closed regressions; interlock + entitlement gates.
- **Prevention:** Any gate change must extend `test_fail_closed.py`. Never Pass without proof.

## Pattern 2: Saying “blocked” for R3 Escalate

- **Date:** recurring
- **Severity:** High (room / fidelity)
- **Root cause:** Colloquial language collapses Escalate into Block.
- **Impact:** Judges hear the wrong actuator; matrix fidelity breaks.
- **Fix:** Content laws + desk-law microcopy; JUDGE_RUNBOOK never-say table.
- **Prevention:** AGENTS.md invariant #6; pitch/deck lint for “blocked.”

## Pattern 3: Quoting 40ms as p95

- **Date:** recurring
- **Severity:** Medium
- **Root cause:** Marketing latency vs measured bench.
- **Impact:** Credibility kill if a judge checks the bench JSON.
- **Fix:** Targets ≤40ms **p50** / ≤200ms **p95**; cite `submission/latency_bench.json`.
- **Prevention:** AGENTS.md evidence rule; metrics UI copy.
