# Task: W7-03 — Structured JSON logs

## Goal
Request lifecycle logs as JSON lines (request_id, scenario, actuators, latency_ms).

## Writes (only)
- `controlplane/logging_setup.py` (new)
- Wire in `controlplane/server/app.py` (and webhook if trivial)
- Tests that logger emits expected keys (caplog) OR a small unit test of formatter

## Forbid
- MATRIX / binder changes

## Steps
1. JSON formatter; configure on app startup.
2. Log admit decisions without PII sprawle.
3. `pytest -q`

## Acceptance
- [ ] JSON log line shape documented in report
- [ ] pytest green

## Commit message
`feat: structured JSON request logs`

## Report
`work/reports/wave-7/W7-03.report.md`
