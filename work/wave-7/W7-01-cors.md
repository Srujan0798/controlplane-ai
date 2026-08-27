# Task: W7-01 — CORS allowlist

## Goal
Configurable CORS allowlist via env (default localhost judge ports).

## Writes (only)
- `controlplane/security.py` and/or `controlplane/server/app.py`
- `tests/` new or extended security tests
- `.env.example` (`CONTROLPLANE_CORS_ORIGINS`)

## Forbid
- static UI redesign
- matrix changes

## Steps
1. Read existing security middleware.
2. Add CORSMiddleware or equivalent from allowlist env (comma-separated).
3. Tests: allowed origin OK; disallowed behaves safely.
4. `pytest -q`

## Acceptance
- [ ] Env-documented
- [ ] Tests cover allow/deny
- [ ] pytest green

## Commit message
`feat(security): CORS allowlist from env`

## Report
`work/reports/wave-7/W7-01.report.md`
