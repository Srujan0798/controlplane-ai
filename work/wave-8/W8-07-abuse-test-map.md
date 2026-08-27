# Task: W8-07 — Abuse cases → tests map

## Goal
Map hostile/abuse cases in QA to concrete tests; add only missing **small** regression tests if clearly absent.

## Writes (only)
- `docs/QA.md` (map section)
- `tests/` only for clearly missing fail-closed/security negatives (keep minimal)

## Forbid
- Matrix redraw
- Broad refactors

## Steps
1. Read QA.md + test_security* + test_fail_closed.
2. Table: abuse case → test file::name → gap?
3. Add ≤3 tests if gaps are real; else docs-only.

## Acceptance
- [ ] Map section exists
- [ ] pytest -q green

## Commit message
`docs: map abuse cases to tests`

## Report
`work/reports/wave-8/W8-07.report.md`
