# Architecture — elevation deltas

**System of record:** [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) (frozen).

## Unchanged core
`STEP → SPAN → CLAIM → ACTION` · Recorder → Binder → Entitlement → Interlock (frozen MATRIX) · Lane 1 deterministic.

## Elevation deltas (Waves 6–8)
| Area | Change |
|---|---|
| Console | OG meta, print one-pager, louder principal/entitlement, error chrome |
| Edge | CORS allowlist, Idempotency-Key, JSON logs, graceful shutdown |
| Policy | Fail-stance by tier enforced (not YAML-only) |
| Observability | Shadow counterfactual CSV export; coverage in CI |
| Evidence | Acceptance matrix, prize-readiness audit, assumptions register |

## Non-goals
Proof cache, speculative tool-arg verify, policy DAG engine, Lane 2 NLI — see `BACKLOG.md`.
