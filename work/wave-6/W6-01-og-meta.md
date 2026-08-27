# Task: W6-01 — OG meta + screenshare polish

## Goal
Add Open Graph / Twitter meta + solid screenshare title/description so projector shares look intentional.

## Writes (only)
- `controlplane/server/static/index.html` (primarily `<head>`)
- Optionally tiny notes in `architecture.html` head if shared chrome — prefer index only

## Forbid
- Python gate / interlock / matrix
- Pitch FINAL rewrite

## Steps
1. Add `<meta property="og:*">` and twitter card tags: title ControlPlane.ai, description admission-control layer, theme-color already present.
2. Ensure `<title>` is judge-clear.
3. Keep offline-safe (no new CDN).
4. Run `pytest -q tests/test_e2e_console.py`.

## Acceptance
- [ ] OG tags present in index.html
- [ ] e2e console tests pass

## Commit message
`feat(ui): open graph meta for screenshare`

## Report
`work/reports/wave-6/W6-01.report.md`
