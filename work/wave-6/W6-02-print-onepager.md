# Task: W6-02 — Printable one-pager

## Goal
Judges can print/save a one-page receipt of the last refund decision (Edit+Escalate story).

## Writes (only)
- `controlplane/server/static/print.html` (new)
- `controlplane/server/static/css/` only if needed for `@media print`
- `controlplane/server/app.py` — **only** a static route mount for `/print` if not already covered by static mount
- Optional nav link in `index.html` **one line** — if you touch index, do not conflict with W6-01/03; prefer linking from runbook.html instead

## Forbid
- Interlock / binder / matrix changes
- Regenerating PPTX

## Steps
1. Create print.html that can load last request via existing audit/API or query params; show dual actuators + clause 7.2 absence + held language.
2. Wire route if needed.
3. Test manually + any existing e2e smoke.
4. `pytest -q`

## Acceptance
- [ ] `/print` (or documented path) renders a printable page
- [ ] Copy never says refund was “blocked”
- [ ] pytest green

## Commit message
`feat(ui): printable clearance one-pager`

## Report
`work/reports/wave-6/W6-02.report.md`
