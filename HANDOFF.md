# HANDOFF.md — cold resume (rewrite, never append)

## Focus: ControlPlane prize close
- **Branch:** `main`
- **Verify:** `bash orchestrator/scripts/preflight-lite.sh` · `pytest -q` · console :8787/:8080
- **Stand kit:** `round2/R2S5.md` · `docs/JUDGE_RUNBOOK.md` · `docs/HOSTILE_QA_DRILL.md` · `docs/ACCEPTANCE.md`
- **Waves 6–8:** reports under `work/reports/` — done; do not re-run scaffolding
- **Tag (human when green):** `git tag -a v0.2.0-round2 -m "Round 2 prize-day known-good"`
- **Invariants:** AGENTS.md — held≠blocked · clause 7.2 absent · fail-closed · no LLM on Lane 1

## Out of scope here
Adaptoid OS / Lite copies — closed and removed from this tree. See `~/Desktop/ADAPTOID-CLOSED.md` if needed later.
