## 1. Round 2 Core Thesis

ControlPlane.ai expands the frozen admission-control mechanism into a route-aware enterprise control plane: one `STEP → SPAN → CLAIM → ACTION` graph governs customer support, internal knowledge, and decision-support flows without requiring model weights, logits, or fine-tuning. Provenance is captured outside the model, every claim starts `UNSUPPORTED`, entitlement is checked against the caller and source ACL, and verification effort is priced by blast radius rather than by a global score. The result is not another output monitor: it is an execution boundary where proof scales with consequence. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYE7FAO6F6Q&Signature=97lv6x7dJnN%2FtwuRveCLwFTzM3E%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAsaCXVzLWVhc3QtMSJHMEUCIQCqS0VZZGGEAylYHe8y01nZuXEw3mcqiv6U1wMHeMnf%2BAIgb3G3nfawtsJSreRDi%2FS28qCL1MTQnl0uLrsd8dld3l8q%2FAQI0%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDLodnJyAJCn74IPd3SrQBLEnXwYUom91S07MnmxFLKJ2sNbvEXLW0vUD7eYEvkVP8ZyTDapZ3%2F442vNqmX0nGgs104TP7qWVY6EWw3B1JbjnfPbQmCvL4j2Ty09LCb18%2BUh%2Fz92SXW%2Fa002x23PWFX04YG%2F7hnUo1%2Bj3rldm0Bd1D87ibMaxeYdoFcf0ZoLxxvzIczBHL5M0Le8CRR18KEpzMgwclkIaweqp7UGFpoq9UUIS5gqI7JBEA3gcLLp7Yp8hi%2Bf%2BUe0svdI%2Bc8qrLK7beRnNiFTjaX9Mw7nNgABOLi4XRYTs34s8GEk%2FeyjgAgPpuRgBJWNb9RnRxkT8qBKY1WuVYh4Lz4e6%2FXnqTWSA5yHgEIHgMNMQiXQjKB8sCKpnwYKrSDvQECF2WDlc%2FG07HW2P9eHzZKJliasFGH3QIhJZdtBqYQ03D2n4Y42s1tGlXy%2FZM3ZOSJUtD2xDQAMLTqpx8rCs2lqgWURBXmMql4qqbQ7DYICEb22Rrh7rQK4TGhjk8SDuZt4ROWHMiAf3AcAJoFydoNjhoOeOG2GscuNNFY32UBZYv2%2BokZ817JWBG1qgWKqCZmz4VjOI4ukOEKJXNZB7mQL46RSFcMivK1t88Rn%2F3UpMimAwrV3WoIhGFn%2F%2FDHp0NdOFMRzXPH2pNHKAkubyYLoZwVlTXqqD8j7GD5xk%2FAPgBpmEhhJ%2BR6WJr%2FjLIFyehTzbjxs0xs8uMiyQBiOnBxq9cBRbf%2Be5gsFi25oucixZVUxN7IolSfVeAjKYieJlWI6J1%2FIedJXGvdOpjhmrUEMChwRTwfYwxo%2Br1AY6mAFQHkFyMYFb6V%2FpA558o2DndTX4qniKA6Cnh78unj%2FlmbHnxSh7%2BtXca0fducaeuQUbjMeiiTsiHseiw5ZyO4aM%2BT44%2BNI1%2FKvRWPyxg8mtJgh85MSDxPxLPDJM6DiAOn0WIC1KbaFdykjmauRh3umCCa7OX%2F9Z0z5Jj1eQFktsmrMOj1kDCY1R0eUoFdEfv5G4F%2B9PxSsUMw%3D%3D&Expires=1787483545)

## 2. Use-Case Selection for the Prototype

Select exactly **two** use cases. Two provide stronger depth than three shallow adapters and let the demo expose both read-path leakage and write-path authorization.

### Use case A: Internal knowledge assistant

**Concrete description:** An employee asks questions over mixed enterprise sources: approved policy documents, HR records, and loosely governed shared files. The assistant returns an answer with citations derived from retrieved chunks.

- **Risk signature:** Entitlement violation, fabricated policy claims, source poisoning, and multi-turn leakage. The key failure is not merely that a statement is wrong; it may be supported by a source the caller is not entitled to read.
- **Latency budget:** ≤40 ms p50 and ≤200 ms p95 added latency for R0/R1 text. Deterministic provenance and ACL checks remain inline; expensive claim binding is reserved for claims that require it.
- **Dominant blast-radius tiers:** R1 for user-visible read-only answers; R0 for drafts or analyst previews.
- **Most powerful frozen mechanism:** External provenance capture plus deterministic entitlement checking. The prototype must show that the same text is acceptable for one principal and unacceptable for another because the source ACL differs.

### Use case B: Customer-support refund agent

**Concrete description:** A support agent retrieves order and vendor-agreement data, generates a customer-facing explanation, and proposes or invokes a refund action.

- **Risk signature:** Unsupported contractual claims, incorrect amounts, PII leakage, multi-turn contamination, and an irreversible or regulated financial action.
- **Latency budget:** ≤40 ms p50 and ≤200 ms p95 for the customer-visible text; action verification is performed while the tool call is in flight, but release never occurs before the interlock decision.
- **Dominant blast-radius tiers:** R1 for customer-visible text; R3 for issuing the refund.
- **Most powerful frozen mechanism:** The exact two-pending-actions resolution. A response may require surgical editing for the R1 text while independently holding and escalating the R3 refund with an evidence packet.

### Why this pair is strongest

Together, these routes force the same graph to operate across two different control problems:

- Internal knowledge proves that retrieval is not permission.
- Refund automation proves that a claim’s consequence changes its required proof.
- The same unsupported claim can pass with annotation at R1, be edited at R2, or be held and escalated at R3.
- The prototype visibly separates claim severity from blast radius instead of collapsing both into a score.
- Both routes expose the one-graph structure: retrieval and tool calls are `STEP`s, their outputs are `SPAN`s, model statements become `CLAIM`s, and proposed side effects become `ACTION`s.

Do not add decision-support as a third live route. Its counterfactual bias measurement is important to the business proposal, but a credible live bias estimate requires route-level samples and confidence intervals; adding it to the core demo would dilute the graph and matrix. Bias remains in scope as an asynchronous measurement lane, not as a third end-to-end demo route. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYE7FAO6F6Q&Signature=97lv6x7dJnN%2FtwuRveCLwFTzM3E%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAsaCXVzLWVhc3QtMSJHMEUCIQCqS0VZZGGEAylYHe8y01nZuXEw3mcqiv6U1wMHeMnf%2BAIgb3G3nfawtsJSreRDi%2FS28qCL1MTQnl0uLrsd8dld3l8q%2FAQI0%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDLodnJyAJCn74IPd3SrQBLEnXwYUom91S07MnmxFLKJ2sNbvEXLW0vUD7eYEvkVP8ZyTDapZ3%2F442vNqmX0nGgs104TP7qWVY6EWw3B1JbjnfPbQmCvL4j2Ty09LCb18%2BUh%2Fz92SXW%2Fa002x23PWFX04YG%2F7hnUo1%2Bj3rldm0Bd1D87ibMaxeYdoFcf0ZoLxxvzIczBHL5M0Le8CRR18KEpzMgwclkIaweqp7UGFpoq9UUIS5gqI7JBEA3gcLLp7Yp8hi%2Bf%2BUe0svdI%2Bc8qrLK7beRnNiFTjaX9Mw7nNgABOLi4XRYTs34s8GEk%2FeyjgAgPpuRgBJWNb9RnRxkT8qBKY1WuVYh4Lz4e6%2FXnqTWSA5yHgEIHgMNMQiXQjKB8sCKpnwYKrSDvQECF2WDlc%2FG07HW2P9eHzZKJliasFGH3QIhJZdtBqYQ03D2n4Y42s1tGlXy%2FZM3ZOSJUtD2xDQAMLTqpx8rCs2lqgWURBXmMql4qqbQ7DYICEb22Rrh7rQK4TGhjk8SDuZt4ROWHMiAf3AcAJoFydoNjhoOeOG2GscuNNFY32UBZYv2%2BokZ817JWBG1qgWKqCZmz4VjOI4ukOEKJXNZB7mQL46RSFcMivK1t88Rn%2F3UpMimAwrV3WoIhGFn%2F%2FDHp0NdOFMRzXPH2pNHKAkubyYLoZwVlTXqqD8j7GD5xk%2FAPgBpmEhhJ%2BR6WJr%2FjLIFyehTzbjxs0xs8uMiyQBiOnBxq9cBRbf%2Be5gsFi25oucixZVUxN7IolSfVeAjKYieJlWI6J1%2FIedJXGvdOpjhmrUEMChwRTwfYwxo%2Br1AY6mAFQHkFyMYFb6V%2FpA558o2DndTX4qniKA6Cnh78unj%2FlmbHnxSh7%2BtXca0fducaeuQUbjMeiiTsiHseiw5ZyO4aM%2BT44%2BNI1%2FKvRWPyxg8mtJgh85MSDxPxLPDJM6DiAOn0WIC1KbaFdykjmauRh3umCCa7OX%2F9Z0z5Jj1eQFktsmrMOj1kDCY1R0eUoFdEfv5G4F%2B9PxSsUMw%3D%3D&Expires=1787483545)

## 3. Prototype Boundary (Hard)

### What the prototype WILL demonstrate

The working prototype will demonstrate the following observable chain:

1. **Context assembly outside the model**
   - A thin SDK hook records each retrieved chunk or tool result with:
     - `source_id`
     - caller principal
     - source ACL
     - content hash
     - offsets or span boundaries.
   - The model receives ordinary context and has no ability to declare its own provenance.

2. **One append-only Evidence Ledger**
   - Each trace contains:
     - `STEP`s for retrieval, tool calls, and model turns.
     - `SPAN`s with source, ACL, hash, and offsets.
     - typed `CLAIM`s extracted from the output.
     - pending `ACTION`s with arguments and irreversibility.
   - The demo must display the graph, not merely a final verdict.

3. **Inverted burden of proof**
   - Every check-worthy claim initially displays `UNSUPPORTED`.
   - A claim changes to `SUPPORTED` only when a verifier binds it to an entitled span.
   - Unsupported claims are not treated as low-confidence claims.

4. **Deterministic entitlement enforcement**
   - Replay the same internal-knowledge query for two principals.
   - Show that a claim binding to an HR span is accepted for an authorized principal and held or edited for an unauthorized principal.
   - Show the source ACL and principal in the evidence packet.

5. **Claim-type routing**
   - Numeric claims are recomputed deterministically.
   - Direct textual claims are checked against the captured provenance set.
   - Derived or multi-hop claims that cannot be recomputed are returned as `UNKNOWN`, never silently promoted to `SUPPORTED`.

6. **Exact R×S matrix application**
   - The demo must run at least:
     - R1 × entitlement violation → `Edit`.
     - R3 × unsupported categorical claim → `Escalate`.
   - It must also show at least one clean supported path and one R0/R1 pass-with-annotation path.

7. **Surgical edit**
   - Remove only the failed claim or invoke one constrained re-generation naming the exact failing span.
   - Re-enter the edited output into the gate.
   - A second failure escalates rather than triggering free-form rewriting.

8. **Action gate**
   - Customer-facing text can stream behind a hold-back buffer.
   - The refund tool call cannot commit while its R3 claim remains unsupported.
   - The refund is held and escalated with the evidence packet; it is not described as blocked.

9. **Two pending actions resolved independently**
   - `Show text to customer` → R1 → surgical edit.
   - `Issue refund` → R3 → hold and escalate.
   - One failed claim must not collapse both actions into a single verdict.

10. **Graph-backed waste accounting**
    - Walk the graph backward from accepted claims.
    - Identify retrieval or tool steps that grounded zero accepted claims.
    - Display dead compute as an exact trace property, not a predicted percentage.

11. **Evidence packet**
    - For every edit or escalation, show:
      - claim text
      - claim type and assertion strength
      - candidate spans
      - source IDs and hashes
      - ACL result
      - verdict
      - affected action
      - matrix cell
      - output diff.

12. **Per-route error-report format**
    - Show the schema for route-level auditing:
      - route
      - sample count
      - stratification
      - false-negative count
      - false-negative rate
      - confidence interval
      - audit window.
    - Use placeholders or clearly marked prototype measurements; do not invent production accuracy. The architecture requires publishing the plane’s own miss rate by route. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/68738113/fee3dd84-365d-4e0d-8897-4585cba87f45/paste.txt?AWSAccessKeyId=ASIA2F3EMEYE7FAO6F6Q&Signature=97lv6x7dJnN%2FtwuRveCLwFTzM3E%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEAsaCXVzLWVhc3QtMSJHMEUCIQCqS0VZZGGEAylYHe8y01nZuXEw3mcqiv6U1wMHeMnf%2BAIgb3G3nfawtsJSreRDi%2FS28qCL1MTQnl0uLrsd8dld3l8q%2FAQI0%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgw2OTk3NTMzMDk3MDUiDLodnJyAJCn74IPd3SrQBLEnXwYUom91S07MnmxFLKJ2sNbvEXLW0vUD7eYEvkVP8ZyTDapZ3%2F442vNqmX0nGgs104TP7qWVY6EWw3B1JbjnfPbQmCvL4j2Ty09LCb18%2BUh%2Fz92SXW%2Fa002x23PWFX04YG%2F7hnUo1%2Bj3rldm0Bd1D87ibMaxeYdoFcf0ZoLxxvzIczBHL5M0Le8CRR18KEpzMgwclkIaweqp7UGFpoq9UUIS5gqI7JBEA3gcLLp7Yp8hi%2Bf%2BUe0svdI%2Bc8qrLK7beRnNiFTjaX9Mw7nNgABOLi4XRYTs34s8GEk%2FeyjgAgPpuRgBJWNb9RnRxkT8qBKY1WuVYh4Lz4e6%2FXnqTWSA5yHgEIHgMNMQiXQjKB8sCKpnwYKrSDvQECF2WDlc%2FG07HW2P9eHzZKJliasFGH3QIhJZdtBqYQ03D2n4Y42s1tGlXy%2FZM3ZOSJUtD2xDQAMLTqpx8rCs2lqgWURBXmMql4qqbQ7DYICEb22Rrh7rQK4TGhjk8SDuZt4ROWHMiAf3AcAJoFydoNjhoOeOG2GscuNNFY32UBZYv2%2BokZ817JWBG1qgWKqCZmz4VjOI4ukOEKJXNZB7mQL46RSFcMivK1t88Rn%2F3UpMimAwrV3WoIhGFn%2F%2FDHp0NdOFMRzXPH2pNHKAkubyYLoZwVlTXqqD8j7GD5xk%2FAPgBpmEhhJ%2BR6WJr%2FjLIFyehTzbjxs0xs8uMiyQBiOnBxq9cBRbf%2Be5gsFi25oucixZVUxN7IolSfVeAjKYieJlWI6J1%2FIedJXGvdOpjhmrUEMChwRTwfYwxo%2Br1AY6mAFQHkFyMYFb6V%2FpA558o2DndTX4qniKA6Cnh78unj%2FlmbHnxSh7%2BtXca0fducaeuQUbjMeiiTsiHseiw5ZyO4aM%2BT44%2BNI1%2FKvRWPyxg8mtJgh85MSDxPxLPDJM6DiAOn0WIC1KbaFdykjmauRh3umCCa7OX%2F9Z0z5Jj1eQFktsmrMOj1kDCY1R0eUoFdEfv5G4F%2B9PxSsUMw%3D%3D&Expires=1787483545)

### What it will deliberately NOT demonstrate

- **Production-scale throughput:** Excluded because the brief permits limited or simulated scope, and throughput claims would distract from the admission mechanism. The prototype will use a small deterministic trace set while stating the intended tens-of-thousands-per-week deployment assumption.
- **A new model or fine-tuning:** Excluded because ControlPlane is an API-layer system. No weights, logits, model training, or proprietary safety model is required.
- **Full counterfactual bias estimation:** Excluded from the live path because bias is a route-level distributional property requiring a rolling sample and confidence interval. It remains specified as an asynchronous shadow lane.
- **Universal regulatory compliance:** Excluded because geography- and industry-specific obligations require policy configuration and legal interpretation. The prototype will demonstrate versioned policy inputs, not claim certification.
- **Complete enterprise IAM remediation:** Excluded because ControlPlane enforces the ACL supplied by the source system; it does not repair an over-permissioned index.
- **Open-web truth verification:** Excluded because the frozen design verifies against the provenance set, not an unbounded web corpus. Claims unsupported by captured evidence remain unsupported.
- **A generic LLM-as-judge:** Excluded from the critical path because it would replace evidence binding with an opinion and contradict the frozen architecture.
- **Composite risk or confidence scores:** Excluded because no action can be derived cleanly from a scalar score. The prototype exposes verdicts, blast-radius tiers, matrix cells, and actuators.
- **Broad dashboarding:** Excluded because dashboards are not the deliverable. The UI exists only to make the graph, evidence packet, matrix decision, and ledger auditable.

### Minimum viable live demonstration

Use one trace with two principals and two pending actions:

1. Retrieve a public order record and an HR-restricted document.
2. Generate: “The customer qualifies for a ₹1,84,000 refund under clause 7.2.”
3. Show that clause 7.2 has no supporting span, so the claim remains `UNSUPPORTED`.
4. Show that an HR-derived entity is bound to a span whose ACL excludes the caller.
5. Route the customer text as R1 and apply `Edit`.
6. Route the refund action as R3 and apply `Escalate`.
7. Display the evidence packet and prove that the refund tool was not committed.
8. Replay with an authorized principal and a real supporting clause:
   - entitlement passes;
   - numeric amount is recomputed;
   - supported R1 text passes;
   - the R3 action is admitted only when its action claims are proven.
9. Walk backward through the same ledger and identify a dead retrieval step.

That is the smallest demo that proves the frozen differentiation rather than merely displaying a safety label.

## 4. Explicit Assumptions

### Data and provenance

- Prototype data is synthetic or sanitized; no real customer, employee, financial, or health data is required.
- The internal-knowledge corpus contains at least:
  - one public document;
  - one restricted HR document;
  - one loosely governed shared document;
  - one intentionally poisoned or stale document whose hash remains traceable.
- Every context-assembly event exposes a source identifier, ACL metadata, content hash, and span offsets.
- ACL metadata is authoritative for the prototype. ControlPlane does not repair upstream identity or access governance.
- Tool results are treated as provenance-bearing spans just like retrieved documents.
- The generator cannot write, alter, or self-report provenance bindings.

### Models and verification

- The foundation model is accessed through an OpenAI-compatible API.
- The prototype has no access to model weights, logits, hidden states, or fine-tuning.
- A small claim extractor may be used to identify typed, check-worthy propositions.
- Deterministic checks handle ACLs, exact identifiers, arithmetic, hashes, and typed action schemas.
- A separate verifier may be used for direct textual entailment, but it cannot decide the action independently.
- Derived claims are recomputed where possible; otherwise they resolve to `UNKNOWN`.
- Prompt injection may alter generated text but cannot alter the externally captured span set, ACL, hash, or principal.
- Corpus poisoning is outside the prototype’s truth guarantee; provenance makes the source and hash traceable but does not prove that the source is factually correct.

### Traffic and routes

- The production design targets tens of thousands of interactions per week across multiple routes.
- Prototype traffic is replayed from a small, curated trace set.
- R0/R1 traffic is assumed to be the majority of volume and receives primarily deterministic inline checking.
- R2/R3 routes receive stricter action interlocks and may use the near-line verification lane.
- The latency target is ≤40 ms p50 and ≤200 ms p95 added latency for R0/R1 text; no claim is made that every expensive verifier completes within the inline budget.
- The prototype runs in shadow mode before enforcement, except for the explicitly simulated R3 action gate.

### Regulatory posture

- The initial deployment is assumed to be an internal enterprise pilot spanning general knowledge assistance and customer support.
- No jurisdiction-specific compliance certification is claimed.
- Policy is versioned by route, geography, industry, and data class so regulatory changes do not require redesigning the graph.
- For decision-support routes, bias is measured asynchronously through counterfactual replay and reported at route level, not asserted per response.
- Human review is available for escalations and receives an evidence packet rather than an unstructured alert.

### Integration surface

- Integration consists of:
  - one context-assembly SDK hook;
  - one OpenAI-compatible reverse proxy;
  - action adapters for the refund tool.
- The application does not need to be rewritten.
- The prototype does not require model-provider cooperation beyond ordinary API access.
- The action executor honors ControlPlane’s interlock result and cannot bypass it through the demo UI.
- Failure stance is tier-specific:
  - R0/R1 fail open with annotation;
  - R2/R3 fail closed or escalate.
- Verification timeouts produce `UNKNOWN` and are routed through the existing matrix; timeout is not treated as implicit support.

### Evaluation

- The prototype evaluation set contains labeled cases for:
  - supported claim;
  - unsupported categorical claim;
  - unsupported hedged claim;
  - contradicted claim;
  - entitlement violation;
  - numeric mismatch;
  - unknown derived claim;
  - clean action;
  - unsafe or schema-invalid action.
- Ground truth for the prototype is created by manual adjudication of the synthetic corpus and action contracts.
- Prototype metrics are not presented as enterprise performance guarantees.
- The per-route FNR report is shown as a reporting format and populated only with measurements from the declared evaluation set.
- The prototype does not claim to eliminate hallucination, bias, privacy leakage, or regulatory risk.
- The system reports what it misses through stratified shadow audit: all holds and escalations plus a random sample of passes.

## 5. Success Criteria for the Prototype

A judge must be able to answer “yes” or “no” to every item below:

1. **External provenance:** For every displayed claim, the demo shows whether its evidence span was captured before generation and identifies the span’s source and hash.
2. **One graph:** The trace visibly contains `STEP → SPAN → CLAIM → ACTION`; the final decision is traceable through those edges.
3. **Default state:** Every check-worthy claim first appears as `UNSUPPORTED` before verification.
4. **Entitlement separation:** The same source-derived claim receives different treatment for authorized and unauthorized principals.
5. **No model-declared proof:** Changing or removing a model-emitted citation does not change the externally recorded provenance or ACL result.
6. **Numeric integrity:** A mismatched refund amount is rejected by deterministic recomputation against the captured spans.
7. **Derived-claim discipline:** A non-recomputable multi-hop claim becomes `UNKNOWN`, not `SUPPORTED`.
8. **Exact matrix fidelity:** The displayed matrix contains the frozen columns and produces the correct actuator for each demonstrated cell.
9. **R1 action:** An entitlement violation affecting customer-visible text produces `Edit`, not `Block` or `Escalate`.
10. **R3 action:** An unsupported categorical refund claim produces `Escalate`, not `Block`.
11. **Action non-commit:** The simulated refund tool cannot commit while the R3 action is held or escalated.
12. **Text/action separation:** The customer-facing text and refund action receive independent decisions even when generated in the same response.
13. **Surgical correction:** The edit removes or corrects only the failing claim and the edited output is re-gated.
14. **Evidence packet:** Every escalation contains the claim, candidate spans, verdict, matrix cell, affected action, and output diff.
15. **Dead compute:** The system identifies at least one step that produced no accepted claim support by walking backward through the same graph.
16. **Route-aware policy:** The demo applies different latency or enforcement treatment to the internal-knowledge route and refund route.
17. **No composite score:** The user interface exposes verdicts and actuators, not a single 0–100 risk or confidence number.
18. **FNR reporting:** The system produces a per-route false-negative report with sample definition and confidence interval fields; no unsupported production accuracy claim is presented.
19. **Failure stance:** A simulated verifier timeout routes R1 and R3 differently according to their tier-specific fail stance.
20. **Replayability:** A recorded trace can be replayed and produce the same ledger, matrix cell, and actuator under the same policy and verifier versions.

## 6. Fidelity Self-Check

- **Default = `UNSUPPORTED`:** Preserved. Claims must earn `SUPPORTED`; absence of proof is never converted into low confidence or implicit approval.
- **Entitlement / ACL check:** Preserved. The caller principal is compared against the ACL attached to each provenance span. A source ACL violation is an entitlement violation and routes as such.
- **Exact R×S matrix:** Preserved without modification:

|  | Contradicted / entitlement violation | Unsupported + categorical | Unsupported + hedged | Unknown |
|---|---|---|---|---|
| **R3** | **Block** | **Escalate** | **Escalate** | **Escalate** |
| **R2** | **Block** | **Edit** | **Edit** | **Escalate** |
| **R1** | **Edit** | **Edit** | **Pass + annotate** | **Pass + annotate** |
| **R0** | **Pass + annotate** | **Pass + annotate** | **Pass** | **Pass** |

- **Hard gate on actions, not tokens:** Preserved. Text uses hold-back and optimistic streaming; the action executor is the hard gate. The refund is held and escalated, never described as blocked.
- **Published own FNR as a format:** Preserved. The prototype reports the schema and measured prototype values only; it does not invent enterprise accuracy.
- **Two-pending-actions resolution:** Preserved. R1 customer text is edited independently of the R3 refund, which is held and escalated.
- **No competing mechanism introduced:** Preserved. No composite score, generic LLM-as-judge, global threshold, post-hoc recall, model introspection, or replacement graph has been added.
- **Bias retained correctly:** Preserved as asynchronous, route-level counterfactual flip-rate measurement with a confidence interval. It is not incorrectly turned into a per-response matrix verdict.
- **Timeout behavior:** Preserved. Timeout yields `UNKNOWN`; the tier’s fail stance handles unavailable evidence. It does not alter the frozen matrix.

There is one deliberate scope tension: the live prototype will use a small adjudicated set, while the architecture describes continuous route-level auditing. This is resolved by demonstrating the ledger and reporting format now, while reserving production calibration and statistically meaningful FNR estimation for the business proposal and shadow deployment.

## 7. Biggest Scope Risk + Exact Mitigation

### Risk

The prototype becomes a generic “AI response checker” with a final label, a few canned examples, and an attractive dashboard. Judges then never see that provenance was captured outside the model, that entitlement is a set-membership decision, or that one response can produce two different action outcomes.

### Exact mitigation

Build the demo around **one replayable refund trace**, not a feature tour, and enforce the following implementation gates:

1. The first screen shows the externally captured spans, source ACLs, hashes, and caller principal before showing the model output.
2. The output is decomposed into claims, each visibly starting `UNSUPPORTED`.
3. The same response creates two pending actions: R1 customer text and R3 refund.
4. The demo runs the exact frozen matrix and displays the matrix cell before the actuator.
5. The customer text is surgically edited; the refund is held and escalated with its evidence packet.
6. A principal replay changes only the entitlement result and demonstrates why identity belongs in the provenance record.
7. The final screen walks backward through the same graph to show dead compute and displays the per-route FNR reporting format.

If any feature cannot strengthen that trace, it is removed from the prototype. The prototype succeeds only if a judge can point from an action to its claim, from that claim to its externally captured span, and from that span to the principal’s entitlement decision.