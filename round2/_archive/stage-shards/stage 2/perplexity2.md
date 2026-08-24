## 1. Expanded Core Thesis

ControlPlane.ai becomes a multi-route enterprise admission-control layer by deploying one typed `STEP → SPAN → CLAIM → ACTION` graph across every AI route, while changing only route configuration, proof depth, and latency budget. Provenance remains captured outside the model; every claim begins `UNSUPPORTED`; caller entitlement remains deterministic ACL set-membership; and the frozen R×S matrix prices proof by consequence. The enterprise system is therefore not a collection of safety products per use case: it is one evidence contract, one decision engine, and multiple route profiles. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

## 2. Multi-Route Architecture

### Shared control-plane substrate

Every route—customer support, internal knowledge, future decision support, batch analysis, or agent workflow—uses the same runtime sequence:

```text
Application / Agent
        │
Context-assembly SDK hook
        │
STEP → SPAN → CLAIM → ACTION Evidence Ledger
        │
Claim routing + entitlement + typed action interlock
        │
Frozen R×S matrix
        │
Pass / Edit / Escalate / Block
        │
Text hold-back and/or action commit boundary
```

The shared components are fixed:

| Shared component | Function | Invariant |
|---|---|---|
| Provenance Recorder | Captures each retrieved chunk, DB row, tool result, and system-provided fact as a `SPAN` with `source_id`, `ACL`, `hash`, and offsets | Captured outside the model |
| Evidence Ledger | Append-only, hash-chained typed record of `STEP → SPAN → CLAIM → ACTION` | One graph; no separate privacy, hallucination, and action graphs |
| Claim Extractor | Emits check-worthy atomic claims and assertion form: categorical or hedged | Claims begin `UNSUPPORTED` |
| Prosecutor | Proves numeric claims by recomputation and direct factual claims by binding only against captured spans | No open-web substitution for missing evidence |
| Entitlement Auditor | Compares caller principal against ACL on every bound span | Deterministic; zero LLM in this decision |
| Action Interlock | Computes R tier, applies the exact frozen matrix, and controls action commit | Pure rule engine; no LLM reasoning at decision time |
| Evidence Packet Builder | Produces claim, candidate spans, verdict, diff, policy version, and affected action for edits/escalations | Escalation is evidence, not an alert |
| Append-only decision ledger | Retains policy version, verifier version, principal, source hash, matrix cell, latency, and actuator | Replayable and auditable |

The graph is not reconstructed from output after generation. `SPAN`s exist because the context-assembly hook captured them before the model generated text; claims can only earn support from that bounded evidence set. That is the architectural difference between binding a claim and scoring a response. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

### Route profile, not route-specific product

Each route receives a configuration profile. The graph, entitlement rule, verdict vocabulary, action interlock, and frozen matrix do not change.

| Configuration surface | Customer-support refund route | Internal-knowledge route | Future decision-support route |
|---|---|---|---|
| Primary interaction | Customer-visible answer plus refund proposal | Employee answer over mixed-governance sources | Recommendation or proposed regulated decision |
| Dominant tiers | R1 text + R3 refund action | R0 draft + R1 read-only answer | Usually R2/R3 |
| Evidence sources | Orders, agreements, account state, refund rules | Policies, HR documents, project/ops records, shared-drive content | Case records, approved procedures, structured decision inputs |
| Required proof | Numeric recomputation, contractual claim binding, ACL check | Entailment binding, ACL check, no-span entity detection | Direct evidence binding, derived-claim recomputation, typed action constraints |
| Inline lane | ACL, span membership, arithmetic, action-schema validation | ACL, span membership, PII/secret entity checks | ACL, deterministic decision constraints, action-schema validation |
| Near-line lane | Binding for action-relevant claims | Binding for disputed factual claims | Binding for high-R claims before recommendation/action release |
| Action grammar | Refund amount, account, reason code, approval state | Generally read-only; no side effect | Route-specific proposal or approved write grammar |
| Fail stance | R1 annotate; R3 hold or escalate | R0/R1 open with annotation | R2/R3 closed or escalate |
| Audit sampling | All held/escalated actions plus sampled passes | All entitlement events plus sampled passes | High sampling for action-bearing cases and counterfactual bias evaluation |

This is how the plane handles different risk tolerance and latency budgets without becoming a different product per route:

- **Shared:** every claim carries the same burden of proof; every evidence span carries the same provenance fields; every action is routed through the same frozen matrix.
- **Configured:** route identity, principal resolver, source connectors, source ACL mappings, action grammar, R assignment inputs, proof-depth budget, lane deadlines, audit sampling, and regulatory policy overlay.
- **Not configurable:** `UNSUPPORTED` default, entitlement enforcement, verdict meanings, matrix cells, or the rule that a held R3 action cannot commit.

A low-consequence internal draft does not receive weaker truth semantics. It receives less verification budget and a proportionate actuator. An unsupported hedged R0 claim may pass, while the same verdict tied to a R3 action escalates. The evidence standard stays hostile; the intervention changes with consequence. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

### Multi-turn and agent execution

A multi-turn session is represented as a chain of hash-linked ledgers, not as a conversational memory blob. A prior assistant statement does not become evidence merely because it reappears in later context.

For each subsequent turn:

1. New retrievals, tool results, and state reads enter as new `STEP` and `SPAN` records.
2. Earlier claims may be referenced only through their original bindings; unproven earlier claims remain unproven.
3. New actions carry a dependency closure: the specific claims, spans, and upstream tool steps on which the action depends.
4. The Action Interlock evaluates the worst relevant claim verdict weighted by its role in that pending action.
5. A tool result becomes a provenance span, not an automatic authorization for the next action.

This prevents compounding risk by refusing to let an earlier plausible output harden into an unexamined fact. Agent autonomy is therefore a configured action permission, not a property granted to the model globally. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

### Overlapping failure modes

The system does not force hallucination, privacy, and bias into a single category.

- A fabricated personal detail with no span is both ungrounded and privacy-shaped; deterministic entity logic can identify the no-span condition, while the claim remains unsupported.
- A semantically correct HR fact bound to a span whose ACL excludes the caller is an entitlement violation, regardless of factual accuracy.
- A policy claim with no binding is unsupported; if it attempts to authorize a refund, the matrix routes that finding through the R3 action.
- Bias is not forced into a per-response claim verdict. It remains a route-level asynchronous counterfactual measurement over decision-shaped outputs.

The control plane preserves different mathematics and different owners for each problem, while allowing one pending action to be constrained by all applicable findings. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

## 3. Governance & Policy Layer

### Policy object

Policy is a versioned DAG of typed rules, not nested conditionals and not an LLM prompt. A rule has the frozen shape:

```text
(signal, threshold, action, latency_budget)
```

The policy engine is deterministic. It consumes ledger facts, route configuration, principal attributes, data classification, and declared action metadata. It does not ask a model to reason about policy at decision time. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

A deployable route policy contains:

```text
policy_version
route_id
jurisdiction / industry posture
principal-resolution method
source / ACL mapping
claim types requiring deterministic recomputation
per-claim proof deadline
lane eligibility
action grammar and argument schemas
R-tier derivation inputs
tier-specific fail stance
audit sampling policy
retention and evidence-packet requirements
circuit-breaker thresholds
```

### What policy may change

| Policy dimension | Allowed configuration |
|---|---|
| Use case / route | Source connectors, claim schemas, action grammar, proof depth, lane budgets, audit sample strata |
| Risk appetite | Whether an application route is permitted to propose or execute an action; autonomy can be downgraded from act to propose |
| Geography / industry | Data classification, regional source restrictions, retention period, required escalation owner, action allow-list, evidence packet fields |
| Blast radius | Inputs to R assignment: irreversibility, audience, data class, and autonomy level |
| Latency | Lane-1/2 deadlines, bounded proof depth, cache TTL, and tier-specific timeout behavior |
| Governance | Circuit-breaker budgets, human-review destination, shadow duration, deployment canary group |

### What policy may not change

Policy cannot:

- Mark an unproven claim as `SUPPORTED`.
- Bypass the caller-versus-source-ACL comparison.
- Convert an entitlement violation into a lower severity verdict.
- Redraw the R×S matrix.
- Replace an R3 escalation with a pass.
- Change an action disposition through a confidence score.
- Release an action because verification was slow.

Regulatory posture is therefore expressed as constraint and routing, not as a second decision framework. A financial-services policy may classify a customer-facing recommendation as R3, add retention requirements, and require a named escalation group. It still passes the same evidence facts through the same matrix. Regulation can raise required control; it cannot relax evidence into trust. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

### Policy change lifecycle

A policy change cannot move directly from an administrator edit into live enforcement.

1. **Author:** A policy change is created as a versioned DAG diff with route, jurisdiction, owner, rationale, and effective scope.
2. **Static validation:** The compiler rejects invalid action schemas, missing fail stances, ambiguous R assignment, broken source/ACL references, and any rule that conflicts with the frozen matrix.
3. **Shadow replay:** The candidate policy replays the last N ledger traces for the affected route. The output shows changed matrix cells, actuator deltas, estimated latency impact, override delta, and expected false-positive/false-negative movement where adjudicated data exists.
4. **Approval:** The route owner and policy owner approve the diff; regulated routes can require a designated compliance approver.
5. **Canary:** The candidate policy runs in shadow or on a bounded route slice. Enforcement is earned route by route, not switched on enterprise-wide.
6. **Auto-rollback:** If human-override rate exceeds 3× the route baseline, or if declared latency/error budgets are breached, the policy rolls back to the prior signed version.
7. **Forensic retention:** Every decision retains the exact policy and verifier version that produced it.

This is the mechanism for evolving regulation without hard-coding rules into application logic or allowing opaque policy drift. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

## 4. Feedback & Learning Loops

ControlPlane learns operational evidence, calibration, and policy quality. It does not learn a new opaque disposition model from outcomes.

### Inputs that improve the system

| Signal | What is recorded | What may change |
|---|---|---|
| Human escalation resolution | Whether the escalation packet was upheld, corrected, or insufficient | Policy thresholds, source-quality remediation, action grammar, escalation routing |
| Human override | Override type, reason, actor, action, route, original ledger, later outcome | Override-rate baseline, policy review trigger, route autonomy review |
| Shadow outcome | Gated vs ungated disposition and later adjudicated result | Per-route calibration, enforcement readiness, FNR/FP estimates |
| Binding failure pattern | Claim type, source family, verdict, evidence coverage, verifier latency | Claim typing rules, proof-depth allocation, source connector quality |
| Entitlement event | Principal, source, ACL mismatch, route, downstream action | Source-system/IAM remediation ticket, route policy review |
| Dead-compute trace | Steps producing zero accepted-claim support, retries, duplicate calls | Agent prompt/workflow optimization and retrieval planning |
| Circuit-breaker event | Gate failures, timeout rate, override rate, route mode | Temporary autonomy downgrade and recovery criteria |

### What remains rule-based

The following remain deterministic or explicitly versioned:

- ACL membership decisions.
- Action-schema validation.
- R-tier derivation.
- Matrix lookup.
- Tier-specific fail stance.
- Action commit or hold.
- Evidence-packet structure.
- Circuit-breaker activation.
- The rule that `UNKNOWN` cannot become `SUPPORTED`.
- The rule that derived claims must be recomputed or remain `UNKNOWN`.

A feedback loop may recommend a rule change; it cannot silently alter live enforcement. Every change remains a policy version, replayed and canaried before it becomes active.

### What is never learned from

The plane must not treat these as automatic truth labels:

- A model’s self-reported citation or confidence.
- A user’s acceptance of an answer.
- An action that completed without an immediately visible complaint.
- A human override without its recorded rationale and subsequent review.
- A poisoned source merely because it appears repeatedly in retrieval.
- A previously generated assistant response copied into future context.

This matters because no reliable real-time ground truth exists on many routes. The system does not manufacture certainty from silence. It separates what can be proven now from what requires later adjudication. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

### Bias feedback loop

Bias remains a separate asynchronous measurement program for decision-shaped routes:

1. Sample comparable route inputs over a rolling window.
2. Perturb protected attributes while preserving non-protected decision inputs.
3. Replay the route under controlled conditions.
4. Measure decision flip rate and a confidence interval.
5. Flag the route when the interval excludes zero.
6. Feed results into route policy review, source-data review, and autonomy posture—not into a per-response matrix verdict.

This satisfies the bias requirement without pretending that a single response can be classified as biased with operationally meaningful certainty. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

## 5. Metrics, Monitoring & Trustworthiness Reporting

The measurement surface is ledger-backed. Metrics are computed from trace facts, policy versions, action dispositions, and audited outcomes—not from a generic “AI safety score.”

### Per-route false-negative reporting

A false negative is a claim or action that passed or was insufficiently constrained despite later ground truth showing it should have received a stricter disposition under the declared route policy.

Each route report contains:

```text
route_id
policy_version
audit window
traffic volume
audit strata
sampled passes
all blocks and escalations audited
adjudicated unsafe / ungrounded / unentitled outcomes
false-negative numerator
false-negative denominator
false-negative rate
confidence interval
unresolved / unavailable ground-truth count
measurement status
```

The audit design is stratified:

- Audit 100% of blocks and escalations to determine whether holds are justified and to measure over-control.
- Audit a random sample of passes to find misses.
- Oversample high-R actions, entitlement-related routes, and recently changed policies.
- Report `unavailable` rather than fabricate an FNR where adjudicated ground truth does not exist.

The published FNR is therefore a reporting contract, not a decorative accuracy claim: “On this route, in this audit window, against this sample definition, this is what the plane missed.” No production number is invented before the evidence exists. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

### Core operational metrics

| Metric | Definition | Why it matters |
|---|---|---|
| False-negative rate | Audited misses divided by audited cases with a known control-relevant failure | Measures liability exposure the plane failed to stop |
| False-positive rate | Audited control actions later found unnecessary, segmented by route and matrix cell | Measures avoidable friction |
| Override rate | Human overrides divided by eligible holds/edits/escalations, with reason code | Detects policies likely to be bypassed |
| Override reason distribution | Evidence insufficient, policy too strict, source ACL wrong, action schema exception, adjudication error | Separates policy failure from source-system failure |
| Entitlement violations | ACL-excluded binding attempts, no-span sensitive entity events, source system, principal class, route | Identifies actual authorization failures rather than vague privacy risk |
| Dead compute | Steps that ground zero accepted claims, found by graph backward-walk | Exact waste measure, not estimated spend |
| Rework / non-convergence | Duplicate calls, retries, repeated retrieval, declining evidence yield with stalled plan state | Detects agent loops and avoidable spend |
| Lane latency | p50/p95 by Lane 1, Lane 2, Lane 3; segmented by route and cache hit | Shows whether verification stays within declared budgets |
| Gate latency | Time from action intent to interlock decision | Measures action-gate impact separately from text generation |
| Action disposition | Pass/Edit/Escalate/Block count by R tier, severity, route, and policy version | Makes the matrix operationally visible |
| Evidence coverage | Share of check-worthy claims with direct support, recomputation, unknown, or no-span status | Detects degraded retrieval/source quality |
| Circuit-breaker state | Gate-fail rate, timeout rate, current autonomy tier, recovery progress | Prevents silent route degradation |

### Trustworthiness reporting surface

A skeptical stakeholder should be able to inspect any material decision in this order:

```text
Action
  → matrix cell
  → claim verdict
  → claim type and assertion form
  → bound or missing span
  → source ID / hash / ACL
  → principal entitlement result
  → policy and verifier version
  → latency and lane
  → human adjudication, if later available
```

The plane does not ask a buyer to trust a dashboard aggregate. It provides replayable evidence for a single action, then aggregates the same ledger facts into route reports. A buyer can therefore challenge a held refund, an edited employee answer, an ACL violation, or a claimed miss rate without relying on model self-explanation. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

## 6. Complete Enterprise Solution vs Prototype

| Scope | Contains | Does not claim |
|---|---|---|
| **Complete enterprise solution** | Context-assembly SDK, OpenAI-compatible proxy, source/ACL connectors, hash-chained Evidence Ledger, per-route policy DAGs, Lane 1/2/3 execution, action adapters, shadow deployment, audit workflow, route reports, dead-compute accounting, circuit breakers, and async bias measurement for decision-shaped routes | Universal truth verification, IAM replacement, zero integration, zero latency, or one cross-domain accuracy number |
| **Stage 1 live prototype** | Customer-support refund route and internal-knowledge route; live provenance capture; claim binding; ACL principal flip; frozen matrix; R1 Edit and R3 Escalate on two pending actions; action non-commit; surgical edit; evidence packet; FNR report schema | Production throughput, real financial execution, regulatory certification, full triage operations, or a live bias route |
| **Proposal-only / phased capability** | Decision-support route templates; rolling counterfactual bias measurement; multi-region policy packs; source-integrity governance; enterprise IAM connectors; large-scale shadow rollout; human-review operations; non-convergence breaker rollout; full cost-optimization program | A claim that any of these should be placed on the prototype critical path before the graph and action gate are proven |

Bias belongs in the complete solution as asynchronous route-level counterfactual measurement. It is explicitly not a third live prototype route and never a per-response decision layer. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

## 7. Residual Risks & Explicit Mitigations

| Residual risk | Why it remains | Exact mitigation |
|---|---|---|
| **Poisoned or factually wrong source evidence** | ControlPlane proves that the model used a captured source; it cannot prove that the source itself is true. A poisoned document can validly support a wrong claim. | Bind every accepted claim to immutable `source_id` and content hash; maintain source ownership and quality metadata; flag anomalous source-level failure concentration in audits; quarantine or de-rank source connectors through policy; retain provenance for forensic rollback. The plane defends the claim-to-evidence link, not the truth of the evidence. |
| **False assurance on derived or synthesized claims** | Shallow entailment can make a synthesized conclusion look supported when it is not directly proven. This is most dangerous on high-R routes. | Derived, multi-hop, and aggregative claims are recomputed from spans where possible. If not recomputable and not directly entailed, they remain `UNKNOWN`; `UNKNOWN` never becomes `SUPPORTED`. R2/R3 unknowns route through the frozen matrix to escalation, and audited high-R passes estimate residual misses. |
| **Control-plane timeout, bypass, or operational pressure to disable enforcement** | A universal fail-open stance is bypassable under load; aggressive blocking creates override pressure and eventual disablement. | Tier-specific fail stance: R0/R1 fail open with annotation; R2/R3 fail closed or escalate. Put the hard interlock in the action executor, not the UI. Use shadow rollout, per-route enforcement readiness, circuit breakers, override-rate monitoring, and automatic rollback when overrides exceed 3× baseline. |

These mitigations preserve an explicit boundary: ControlPlane reduces the set of unproven claims that can authorize action; it does not claim to eliminate falsehood, repair upstream IAM, or certify a corpus as true. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)

## 8. Fidelity Self-Check

- **Default = UNSUPPORTED:** Preserved. Route configuration changes verification depth and intervention budget, never the burden of proof. No absence of evidence becomes implicit support.
- **Entitlement / ACL check:** Preserved. ACL enforcement remains a deterministic comparison between caller principal and the ACL attached to an externally captured span.
- **Exact R×S matrix:** Preserved. The matrix is not redrawn, relabeled, or made route-specific. Routes supply R inputs; the frozen matrix supplies the actuator.
- **Hard gate on actions, not tokens:** Preserved. Text uses a hold-back buffer; side effects remain gated at the tool/action commit boundary.
- **No LLM-as-judge on the critical path:** Preserved. Claim extraction and textual entailment may be model-assisted, but the Action Interlock is a pure rule engine operating on typed ledger facts. No model opinion decides disposition.
- **Two-pending-actions resolution:** Preserved. The refund trace remains two simultaneous action decisions: R1 customer text is edited for the entitlement violation; R3 refund is held and escalated for unsupported categorical clause 7.2.
- **Bias is not a per-response verdict:** Preserved. Bias is asynchronous, route-level counterfactual flip-rate measurement with a confidence interval.
- **No composite score or confidence disposition:** Preserved. The plane uses typed verdicts, evidence bindings, R tier, and matrix cells; no scalar risk score decides an action.
- **API-only deployment:** Preserved. The architecture requires an SDK context hook, reverse proxy, and action adapters; it requires no weights, logits, hidden states, or fine-tuning. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYEYRI6AZPS&Signature=eNDtddxF0QruqF9Wfxfnlnlz8sU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAwaCXVzLWVhc3QtMSJHMEUCIFZFkW6y3TOnH45YCB2p%2BbruG4XQAg5PU0qf0f%2BM9dy5AiEA4p6Tak6Dq6A6Jd%2FozaYKswLVau5V%2BXhRZNV6Xgyw3l4q%2FAQI1P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDOTfDMhw9ZPu34dMmirQBGCB1Gv7X42hJYS2aijguyHhaDbsG5fBqul3R1Nchw%2BHJ8ipS%2Bopvxuok8PMfFP6O1R60SRQFs2sEI0KhQhRxCuXzF%2B34pgu9Q1rH%2B2ycZkkP54Aim9JqmunD%2Fl2YpXFfUWNsW6kRU4ohOi5EsPsjydeqNaeHiN%2F8hxN3OFIue0wSNuVTlOfVbwY49CGZ23mdOxcEF3yvUw%2B0AYaWbuKvEhjZ6GqeJENdeDPyHFxpWjY%2BBUNQW06KZdoF77GRs9qMaBoFTbtp5yKRxq9A4kr8Kb2hdZwqCQ1DeRfGBskk72Iv%2B5SvYLi1sKFNMcrP5mG44%2F3LbBqnsQaLMpzKixe9gbs5eyZwjoptqeiJQfDFiNx1e5MxtSeMKB%2BgjoiTc2bC1CXPAjP1puByE6ICMLZhyLPbreWgOkDmN03rd44DYTqwfvtuS%2Bt1HwKG3hVlQd%2B%2FgQB7Y0qvZZw75udEQs%2FfFj1J94xQ%2By6Jq3HE5dQ6b%2BUwn48Rm2r3%2B7nJFxNNavoDftBa8pclBcnVRaiCBlr65V4bVT8jZsZZEkU9wXDoZG5yV4sDuCj3Efs%2BE7bJzn6Apd2lhf9RqfJq2EbV%2F3yxVwpDa%2BUVEFaVGhm3miMFrVuKpTqyn%2B%2BS1zkJz4Ka7dTd%2FYatuRxaXtgi2pI2o1kT9uf0WvZs6HVUapsoPJkJrpPpZwVZo%2BxhNqJn3Vq7xMlx1FjP1E8QYqefj0qFHmoTfdBy0Mn5za2mcm0AUa%2BPW1naIsu%2FPYzh1OQQR9k5BymYkZ0Hnhs%2BNB5wmL8XplHmhgwhaur1AY6mAHJFT2kQwNKElV6x%2BMTRqm7rCKC4fuvnybI5FxMItOaw9ce1fSwCkBnv9gJ%2BkTMH%2BacirPR8quy8uDGTK1JjdrkpfJU9mYvq41lBvmuepgwGOFZ3nb6%2F7pBAzlfb5oBUaXsJoO26aneyISeVlsB68aKeoBx%2BpzXzwqia7UqETOQ9LTc3FhFTGoK5nNVmZU4KAPRCEEQtBRC6A%3D%3D&Expires=1787487064)