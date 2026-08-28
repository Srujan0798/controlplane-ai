# Route Sentinel — Pre-Execution Wrong-Route Blocking

> FM-16: Wrong route (hallucinated nodes, invalid transitions, destructive actions)

## What it does
Route Sentinel is the **outermost gate** before any tool call or DAG transition executes. It validates the proposed action against a static, human-reviewed `DAG_TRANSITIONS` map.

## When to load
Before executing any wave plan or worker task that involves state transitions.

## The `dag_transitions` map
```yaml
dag_transitions:
  plan:
    allowed_next: [dispatch, review]
    max_retries: 3
  dispatch:
    allowed_next: [review, merge]
    max_retries: 2
  review:
    allowed_next: [merge, dispatch]
    max_retries: 3
  merge:
    allowed_next: [ship]
    max_retries: 1
```

## Blocking rules
1. **Unknown source** → block
2. **Unknown target** → block
3. **Self-loop** → block (unless explicitly whitelisted)
4. **Transition not in map** → block
5. **Retry exhausted** → escalate to `human_escalation`

## Events
On block, emits `WRONG_ROUTE_BLOCKED` to the event log with:
- `source_node`
- `attempted_target`
- `allowed_targets`
- `retry_count`

## Validator
`validators/route_sentinel.sh` checks the config map for validity.
