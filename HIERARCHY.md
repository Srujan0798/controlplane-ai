# HIERARCHY.md — ownership

| Path | Owner | Notes |
|---|---|---|
| `controlplane/` | product | Gate + server + static |
| `policies/` | product | YAML packs |
| `tests/` | whoever changes code | Must stay green |
| `docs/` | docs | Runbook, acceptance, architecture |
| `round2/` | pitch canon | FINAL + R2S5 — prefer not to rewrite |
| `submission/` | packaging | PDF / PPTX / bench / SBOM |
| `work/` | evidence archive | Wave tasks + reports (shipped) |
| `plan/` | status | EXECUTION.md |
| `orchestrator/` | verify | ROLE + preflight-lite |
| `protocols/` | reference | Ship spine copies (small) |
| `.worktrees/` | ignored | Do not use for new work |
| `graphify-out/` | regenerable | `graphify update .` |
