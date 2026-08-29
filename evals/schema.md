# Eval case schema

Each YAML file under `evals/cases/` is a list of cases:

```yaml
- id: refund-clean-001
  stratum: clean
  use_case: decision-support
  response_text: "..."
  spans:
    - source_id: doc:x
      acl: [vendor-public]
      content: "..."
  principal:
    id: cs-agent-17
    clearance: [vendor-public]
  actions:
    - action_id: issue_refund
      tier: R3
      irreversibility: true
      args: {amount: 184000, currency: INR, order: ORD-9}
  expected_verdicts:
    amount: SUPPORTED
  expected_actuators:
    issue_refund: Escalate
  label: should_hold   # should_hold | should_pass | hard_negative
```
