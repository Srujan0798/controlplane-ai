# Task: W6-03 — Entitlement principal loud on Clearance

## Goal
Clearance first viewport shows **who** is calling (principal) and that entitlement is ACL set-membership — flip story visible without reading docs.

## Writes (only)
- `controlplane/server/static/index.html`
- `controlplane/server/static/js/bay.js`

## Forbid
- Backend entitlement algorithm changes
- docs/round2 FINAL

## Steps
1. Surface principal id / clearance on Clearance after admit (and idle hint for flip scenario).
2. Add short copy: entitlement = span.acl ⊆ principal.clearance · zero LLM.
3. Wire flip scenario button/hint if missing.
4. `pytest -q tests/test_e2e_console.py` (+ flip API test if present).

## Acceptance
- [ ] Principal visible on Clearance after refund/flip run
- [ ] Copy matches AGENTS.md language
- [ ] tests green

## Commit message
`feat(ui): surface principal entitlement on clearance`

## Report
`work/reports/wave-6/W6-03.report.md`
