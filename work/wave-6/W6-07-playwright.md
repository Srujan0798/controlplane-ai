# Task: W6-07 — Playwright optional e2e green

## Goal
Make optional Playwright path documented and runnable (`pip install -e ".[e2e]"`), skipping cleanly if browsers missing.

## Writes (only)
- `tests/test_e2e_console.py` (and helpers if any)
- `pyproject.toml` e2e extras only if needed
- `.github/workflows/ci.yml` note or optional job — do not fail CI if browsers absent
- `Makefile` e2e target comment if useful

## Forbid
- Gate logic / matrix

## Steps
1. Read current e2e tests (skip pattern).
2. Ensure skip message is clear; add one smoke that hits Clearance + refund if playwright available.
3. Document in report how to install browsers.
4. `pytest -q` must stay green without browsers.

## Acceptance
- [ ] pytest -q green without playwright browsers
- [ ] With playwright installed, at least one browser smoke can run OR clearly documented blocker

## Commit message
`test: harden optional playwright console e2e`

## Report
`work/reports/wave-6/W6-07.report.md`
