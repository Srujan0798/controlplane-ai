# HIERARCHY.md — repo map + ownership

| Path | Owner | Notes |
|---|---|---|
| `controlplane/` | product agents | Core gate + FastAPI + static |
| `controlplane/server/static/` | Wave 6 UI tasks | File-own per task |
| `policies/` | policy agents | YAML packs; no matrix redraw |
| `tests/` | whoever changes code | Must stay green |
| `docs/` | docs/evidence agents | Canon under `round2/` for FINAL/R2S5 |
| `round2/` | pitch canon | Prefer not to rewrite R2S5 unless factual error |
| `submission/` | packaging agents | PDF/PPTX/bench/SBOM |
| `work/` | orchestrator writes tasks; workers write reports only under `work/reports/` |
| `plan/` | orchestrator | PRD / ARCHITECTURE pointer / EXECUTION |
| `.worktrees/` | ignored | Do not use for new prize work |
| `graphify-out/` | regenerable | `graphify update .` |
