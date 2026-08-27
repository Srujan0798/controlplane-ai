# Task: W7-07 — Shadow counterfactual CSV export

## Goal
Export shadow “would have held” counters / decision rows as CSV for skeptical stakeholders.

## Writes (only)
- Endpoint in `controlplane/server/app.py` (e.g. `/v1/controlplane/metrics.csv`)
- `controlplane/shadow.py` if needed
- `tests/` for CSV header/rows
- Optional one link on `static/metrics.html`

## Forbid
- Lane 2 NLI
- Fake FNR percentages

## Steps
1. Reuse existing metrics counters.
2. CSV with clear columns; no invented rates.
3. `pytest -q`

## Acceptance
- [ ] CSV download works via TestClient
- [ ] pytest green

## Commit message
`feat: shadow metrics CSV export`

## Report
`work/reports/wave-7/W7-07.report.md`
