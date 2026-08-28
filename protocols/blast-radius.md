# Protocol — Blast Radius (containment)

> Load before any action that isn't a pure local edit. Per Anthropic "How we contain Claude across products."

Every action has a blast radius — the worst case if it goes wrong. Gate by radius.

| Radius | Examples | Gate |
|---|---|---|
| **r0 — Read-only** | read, grep, ls, list | execute freely |
| **r1 — Local repo** | write src/, run tests, lint, local commit | auto-allowed (git protects) |
| **r2 — Local services** | apply migration to dev DB, seed dev data | confirm; must be reversible |
| **r3 — Remote services** | git push, send Slack, call external API, deploy staging | confirm; possibly reversible |
| **r4 — External humans** | email customers, file tickets, post publicly | ALWAYS confirm; hard to reverse |
| **r5 — Money / data loss** | charge a card, drop prod table, delete a bucket, force-push main | BLOCK by default; require explicit, scoped authorization |

## Mapping to governance tiers
- r0/r1 → T0 auto
- r2 → T1 log + proceed
- r3/r4 → T2 await human approval
- r5 → T3 block

## Auto mode (Anthropic Mar 2026)
Auto mode skips prompts for **r0/r1 only**. r2+ still pauses even in auto mode.

## Rules
- Sending content to an external service = publishing (may be cached/indexed even if deleted later). That's r3+ minimum.
- Before deleting/overwriting something you didn't create, inspect it first; if it contradicts how it was described, surface that instead of proceeding.
- Approval in one context does NOT extend to the next. Re-confirm per action.
- Log r3+ actions to events.jsonl with the radius.

## Enforcement
`orchestrator/hooks/pre-tool-use.sh` classifies the call's radius and pauses/blocks per tier. `mcp-security-gate.sh` whitelists MCP calls.
