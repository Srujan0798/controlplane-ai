# AGENTS.md — ControlPlane.ai project law

Accenture Innovation Challenge 2026 · Round 2 · Team ControlPlane · PS #1  
Branch: **`main`**. Do not use `.worktrees/` for new work.

## Stack
- Python ≥ 3.11 · FastAPI · uvicorn · pytest · YAML policies · static HTML/CSS/JS console
- `pip install -e ".[dev]"` · `pytest -q`
- Judge: `docker compose up --build` (:8080) or uvicorn on **8787**

## Frozen invariants (never “improve”)
1. Provenance **outside** the model — model output never creates spans.
2. Default claim verdict = `UNSUPPORTED`.
3. Clause **7.2 does not exist** → absence → `UNSUPPORTED` (never “doesn’t cover”).
4. Blast-radius **MATRIX transcribed, never redrawn**.
5. Action Interlock is the **sole decider**.
6. Refund language: **held / escalated with evidence packet** — never “blocked” for the R3 payout.
7. Lane 1 = **deterministic only** (no LLM / NLI on critical path).
8. Fail **closed** toward Escalate/Block — never Pass without proof.

## Evidence
- Prefer `orchestrator/scripts/preflight-lite.sh` before claiming green.
- After code changes: `graphify update .`
- Never invent FNR %, customer logos, or quote **40ms as p95** (targets ≤40ms p50 / ≤200ms p95; cite `submission/latency_bench.json`).

## Canon
- Architecture: `docs/ARCHITECTURE.md`
- Proposal: `round2/CONTROLPLANE_R2_FINAL.md`
- Pitch: `round2/R2S5.md`
- Stand: `docs/JUDGE_RUNBOOK.md`
- Acceptance: `docs/ACCEPTANCE.md`

## graphify
- `graphify query "<question>"` when `graphify-out/graph.json` exists.
- After code changes: `graphify update .`
