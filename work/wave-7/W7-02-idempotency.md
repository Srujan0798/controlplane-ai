# Task: W7-02 — Idempotency-Key support

## Goal
Honor `Idempotency-Key` on demo/chat admission endpoints so retries do not double-commit side effects.

## Writes (only)
- New `controlplane/idempotency.py` (preferred) and wire in `controlplane/server/app.py`
- `tests/test_idempotency.py` (new)
- `.env.example` if TTL/config needed

## Forbid
- static UI
- Changing MATRIX cells

## Steps
1. Store key → response for short TTL (memory or SQLite).
2. Same key + same body → same response; conflict policy documented.
3. Tests for replay.
4. `pytest -q`

## Acceptance
- [ ] Header supported on at least refund demo + chat completions
- [ ] Tests green

## Commit message
`feat: Idempotency-Key for admission endpoints`

## Report
`work/reports/wave-7/W7-02.report.md`
