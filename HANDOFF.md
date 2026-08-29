# HANDOFF.md — cold resume (rewrite, never append)

## Focus NOW: ControlPlane product only
- **Branch:** `main`
- **Adaptoid:** CLOSED — see Desktop `ADAPTOID-CLOSED.md`. Do not open Adaptoid-OS for SEBI work.
- **Active product work:** finish Wave 7 (enterprise) + Wave 8 (evidence) under `work/`
- **Verify:** `bash orchestrator/scripts/preflight-lite.sh` · `pytest -q` · judge console :8787/:8080
- **Invariants:** AGENTS.md (held≠blocked, clause 7.2 absent, fail-closed, no LLM Lane 1)
- **Tag (human when green):** `git tag -a v0.2.0-round2 -m "Round 2 prize-day known-good"`

## Ignore for product
`Adaptoid-OS/improvements/**`, harvest prompts, Lite 3.2 proposals — already packed for a later promote.
