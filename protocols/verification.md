# Protocol — Verification (Swiss Cheese)

> Load before claiming anything "done." No single layer catches everything; stack them. Per Anthropic Jan 2026.

## The stack (each catches what the prior misses)
| Layer | Catches | Runs |
|---|---|---|
| Type checks (mypy/tsc) | type/shape errors | pre-commit + CI |
| Lint (ruff/eslint) | style + obvious bugs | pre-commit + CI |
| Unit tests | logic in isolation | pre-commit + CI |
| Integration tests | module interaction | CI |
| Acceptance contracts | spec → reality | CI + /review |
| E2E (Playwright) | user-visible flows | CI nightly |
| Eval pass@k | capability present | CI for changed waves |
| Eval pass^k | capability not regressed | every commit |
| Perf budget | latency targets | pre-deploy |
| `verifier` sub-agent | independent code read | /review |
| **Human transcript read** | grader fairness, agent loopholes | weekly |
| Production monitoring | what all the above missed | live |
| OS-Setup validators | the 14 failure modes | preflight before merge/ship |

## Gate ordering & cost cascade (cheapest first, always)

Run gates in cost order. Most failures are deterministic (parsing/schema/permission — not reasoning), so they must die before any model-based check spends a token.

```
0. ROUTE GATE      route_sentinel — is this transition even in the DAG?     ~free   (FM-16)
1. POLICY GATE     oap_security  — is this tool call allowed at all?        ~free   (FM-18)
2. SCHEMA GATE     structured output / type / format / range checks         ~free
3. STATE GATE      vault_mmu hash check — durable state untampered?         ~free   (FM-17)
4. SELF-CHECK      small/cheap model verifies the output                    1x cheap inference
5. CROSS-CHECK     independent verifier agent / second model on escalation  1x+ inference
6. GROUNDING       source/citation check — high-stakes claims only          expensive, rare
```

Cascade rules:
- A blocked action at gate 0–1 never reaches gate 2 — nothing downstream runs, nothing is spent.
- Escalate 4→5 only on low confidence or high stakes; smaller models verify better per dollar than they generate.
- Every gate result is an event (`verify.passed` / `verify.failed` / `route.blocked` / `policy.denied`) — see `protocols/event-sourcing.md`.
- **max_retries = 3.** After 3 failures at any gate: stop, roll back to last checkpoint, escalate to human. Never silently pass a low-score output, never loop forever.
- Gate outcome is ternary: PASS (continue) · FAIL (retry/rollback) · NEEDS_REVIEW (human). A missing or malformed status = FAIL, not PASS (fail-closed).

How deep to stack the gates for a given task: see the risk × complexity matrix in `adaptor/INPUT-TAXONOMY.md`.

## Who runs what
- **Workers**: unit + integration locally before reporting.
- **Orchestrator**: re-runs acceptance + evals + validators; spawns verifier. (Never trusts worker claims — FM-09.)
- **CI**: everything, on every push.
- **Humans**: read transcripts/results; nothing is taken at face value until someone reads the details.

## The evidence rule (kernel law 5)
"Done" / "passes" / "works" must come with: the command run + its output, THIS session. A claim without evidence is a hypothesis, not a status.

## Before /ship
Run `validators/preflight.sh` — it runs all wired validators (state drift, refs, metrics, processes, publish gate, config, disjoint dispatch). Must be green. Then regenerate derived docs (FM-12) so README/report match reality.
