# Task: W6-04 — Empty / loading / error chrome

## Goal
Dedicated, accessible empty/loading/error states on Clearance (not silent failure).

## Writes (only)
- `controlplane/server/static/css/bay.css`
- `controlplane/server/static/index.html` (strips/empty/error regions only)
- `controlplane/server/static/js/bay.js` if needed for error handlers

## Forbid
- Server Python except if you must not — prefer client-side fetch error handling only

## Steps
1. Style empty / loading / error strip states with aria-live.
2. On fetch failure show recoverable message pointing to JUDGE_RUNBOOK ports.
3. Respect `prefers-reduced-motion`.
4. `pytest -q tests/test_e2e_console.py`

## Acceptance
- [ ] Error state visible when API fails (simulate by bad URL in dev or mock)
- [ ] e2e green

## Commit message
`feat(ui): clearance empty loading error chrome`

## Report
`work/reports/wave-6/W6-04.report.md`
