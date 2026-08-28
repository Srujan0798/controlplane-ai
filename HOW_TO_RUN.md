# See also: [MASTER-FLOW.md](MASTER-FLOW.md) (Core-shaped spine)

# HOW_TO_RUN.md — dual-tier parallel agents

## Product (judge)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787
# or: docker compose up --build  → http://localhost:8080
```

## Agents (Adaptoid)

1. Read `AGENTS.md` once.
2. Open one agent window per task.
3. Paste **all** of `work/WORKER_PROMPT.md`, then paste **one** file from `work/wave-N/`.
4. Worker commits + writes `work/reports/wave-N/<task>.report.md`.
5. Orchestrator merges, runs `pytest -q`, updates `plan/EXECUTION.md`.

### Recommended parallel batches

**Batch A (start now — no shared writes):**
- `work/wave-6/W6-05-kill-shot.md`
- `work/wave-6/W6-06-demo-video-script.md`
- `work/wave-6/W6-08-brand-check.md`
- `work/wave-8/W8-01-acceptance.md`
- `work/wave-8/W8-03-assumptions.md`
- `work/wave-8/W8-04-stakeholder.md`

**Batch B (UI — serialize if same file):**
- First: `W6-01-og-meta.md`
- Then parallel: `W6-03-entitlement-ui.md` + `W6-04-error-chrome.md` (coordinate on index.html)
- Alone: `W6-02-print-onepager.md`

**Batch C (enterprise — mostly parallel):**
- `W7-01-cors.md`, `W7-03-json-logs.md`, `W7-05-graceful-shutdown.md`, `W7-06-coverage-ci.md`, `W7-08-openapi-examples.md`
- Alone: `W7-02-idempotency.md`, `W7-04-fail-stance.md`, `W7-07-shadow-csv.md`

**Batch D (evidence close):**
- `W8-02-final-audit.md`, `W8-07-abuse-test-map.md`, `W8-08-prize-matrix-refresh.md`
- Serialize: `W8-05-handoff-execution.md` then `W8-06-tag-contributing.md`

### Worker prompt location
`work/WORKER_PROMPT.md`
