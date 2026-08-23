# Changelog

## Round 2 elevation — ControlPlane.ai (0.2.x)

Accenture Innovation Challenge 2026 · branch `feature/round2-controlplane` (not merged to `main`).

### Mechanism (carried from Round 1 → production surface)

- STEP → SPAN → CLAIM → ACTION primitive with provenance **outside** the model
- Default UNSUPPORTED binder; entitlement ACL auditor; frozen R×S interlock
- Dual-action refund fixture: **Edit** (show_text) + **Escalate** (issue_refund) on one ledger
- Hash-chained Evidence Ledger + audit JSONL export

### Round 2 production elevation

- OpenAI-compatible reverse proxy (`POST /v1/chat/completions`) with ControlPlane extension object
- Versioned YAML policy packs (`policies/`) + shadow / enforce modes
- Shadow counters with publishable FNR claim **shape** (no fabricated accuracy %)
- Judge Operate console (`controlplane/server/static/index.html`)
- Docker Compose on **8080**; local uvicorn tip on **8787**
- GitHub Actions CI + `pytest` suite

### Measurement, security, event-day packaging (this pass)

- `scripts/load_bench.py` — N=200 sequential refund demos; gate `latency_ms` + wall p50/p95/p99 → `submission/latency_bench.json`
- `tests/test_determinism.py` — five enforce runs → identical actuators
- `tests/test_security_negatives.py` — healthz, unknown scenario 400, metrics reset, oversized JSON hygiene
- `docs/THREAT_MODEL.md` — STRIDE for proxy + ledger + console; trust boundaries; mitigations → code
- `docs/JUDGE_RUNBOOK.md` — 60s script, failure recovery, never-say list
- `Makefile` — `test`, `bench`, `run`, `judge`

### Explicit non-claims

Latency **targets** remain ≤40 ms **p50** / ≤200 ms **p95**. We do not claim eliminate-hallucinations, zero integration, or zero added latency. Refunds are **held**, not “blocked.”
