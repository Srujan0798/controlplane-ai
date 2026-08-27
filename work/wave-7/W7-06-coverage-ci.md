# Task: W7-06 — Coverage gate in CI

## Goal
CI publishes coverage; optional soft gate (do not brick prize demo if coverage tool missing).

## Writes (only)
- `.github/workflows/ci.yml`
- `Makefile` (`coverage` target)
- `pyproject.toml` dev extra for pytest-cov if needed

## Forbid
- Product behavior changes

## Steps
1. Add `pytest --cov=controlplane` job or step.
2. Makefile target `make coverage`.
3. Keep default `make test` fast.
4. Ensure CI still passes locally runnable.

## Acceptance
- [ ] `make coverage` documented
- [ ] CI workflow updated
- [ ] `pytest -q` still green

## Commit message
`ci: add coverage report target`

## Report
`work/reports/wave-7/W7-06.report.md`
