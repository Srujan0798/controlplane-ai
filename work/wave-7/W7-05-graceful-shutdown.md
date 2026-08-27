# Task: W7-05 — Graceful shutdown

## Goal
FastAPI lifespan closes DB connections / flushes cleanly on SIGTERM.

## Writes (only)
- `controlplane/server/app.py` lifespan
- `controlplane/persist.py` if close() needed
- Small test or documented manual evidence

## Forbid
- UI
- Policy semantics

## Steps
1. Add lifespan context: startup/shutdown.
2. Ensure SQLite connections close.
3. `pytest -q`

## Acceptance
- [ ] Lifespan present
- [ ] pytest green

## Commit message
`feat: graceful shutdown lifespan for app`

## Report
`work/reports/wave-7/W7-05.report.md`
