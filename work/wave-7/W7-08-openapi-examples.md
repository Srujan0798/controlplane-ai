# Task: W7-08 — OpenAPI examples polish

## Goal
OpenAPI schema shows worked examples for refund demo + chat completions (judge/integrator clarity).

## Writes (only)
- `controlplane/server/app.py` (response examples / Field examples)
- Optionally `docs/api.md` short pointer — only if you create it; prefer OpenAPI alone

## Forbid
- Redesigning routes
- UI overhaul

## Steps
1. Add `openapi_examples` or equivalent on key routes.
2. Verify `/openapi.json` contains examples.
3. `pytest -q tests/test_server_api.py` (or full).

## Acceptance
- [ ] Examples visible in openapi.json
- [ ] pytest green

## Commit message
`docs(api): openapi examples for demo routes`

## Report
`work/reports/wave-7/W7-08.report.md`
