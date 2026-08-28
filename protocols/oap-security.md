# OAP Security — Open Agent Passport

> FM-18: Unauthorized tool call / destructive action without approval

## What it does
OAP is deterministic, fail-closed policy enforcement at the **pre-tool-call hook**. Every tool invocation is checked against a JSON-schema policy pack before execution.

## When to load
Before any tool call in a worker or orchestrator session.

## Policy decision
- `ALLOW` — proceed
- `DENY` — block with `OAP_DENIED` event
- `REQUIRE_APPROVAL` — pause for human confirmation

## Default policy packs
Located in `policies/`:
- `filesystem.yaml` — read/write/delete rules
- `network.yaml` — curl, fetch, API call rules
- `execution.yaml` — bash, script, code-run rules
- `data.yaml` — database, PII, export rules

## Rule precedence
1. Explicit tool match
2. Pattern match (glob/regex)
3. Default pack rule
4. No match → **DENY**

## Validator
`validators/oap_security.sh` checks that every active tool has a matching policy and that packs are valid YAML.
