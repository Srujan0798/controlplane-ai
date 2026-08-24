---
### **1. Round 2 Core Thesis**

ControlPlane.ai is an **admission-control layer** that treats every AI action as a set of claims requesting permission to act. It binds each claim to provenance captured *outside the model* at context-assembly time—source, ACL, and hash—then spends verification budget in proportion to blast radius: a draft is checked cheaply, a payment is held until proven. The same graph (**STEP → SPAN → CLAIM → ACTION**) powers performance, cost, and responsibility checks across all use cases, with the **R×S matrix** ensuring surgical decisions that never over-block.

---

---
### **2. Use-Case Selection for the Prototype**

**Use Case 1: Customer Refund Processing**
- **Concrete description**: AI agent approves/refuses customer refunds by referencing policy documents (clause library) and customer records.
- **Risk signature**: Financial (₹1,84,000-class errors), regulatory (payment compliance), privacy (PII in customer data).
- **Latency budget**: ≤200ms p50 / ≤400ms p95 for text streaming; ≤500ms for action gating.
- **Dominant blast-radius tiers**: **R1** (show response to customer), **R3** (execute refund payment).
- **Frozen mechanism demonstrated**: **Entitlement check** (ACL on policy docs), **Blast-radius matrix** (same unproven claim → **Edit** at R1, **Escalate** at R3), **Two-pending-actions resolution**.

**Use Case 2: Internal Knowledge Assistant**
- **Concrete description**: Employees query internal wikis, API docs, and proprietary datasets.
- **Risk signature**: Hallucination (incorrect technical facts), leakage (internal-only data), bias (synthesized recommendations).
- **Latency budget**: ≤100ms p50 / ≤200ms p95 for text streaming; ≤300ms for action gating.
- **Dominant blast-radius tiers**: **R0** (internal draft), **R1** (user-visible read-only).
- **Frozen mechanism demonstrated**: **Performance** (claim-binding), **Cost** (dead compute from re-retrieval), **Responsibility** (ACL on internal docs), **Default UNSUPPORTED**.

**Why this combination is the strongest demonstration**:
- Use Case 1 **proves the matrix** via the two-pending-actions (R1=Edit, R3=Escalate for the same unproven claim).
- Use Case 2 **proves breadth**—same mechanisms work across different blast-radius profiles and latency budgets.
- Both demonstrate **API-only integration** (no model access), **overlapping failure modes** (hallucination, leakage), and the **one-graph** concept.
- The pair shows **surgical decisions** (Edit vs. Escalate vs. Pass) without over-blocking.

---
---
### **3. Prototype Boundary (Hard)**

**What the working prototype WILL demonstrate** *(observable by a judge)*:
1. **Live graph construction**: STEP → SPAN → CLAIM → ACTION built in real-time as a refund response is generated.
2. **Provenance capture**: Spans displayed with **source · ACL · hash** captured at context-assembly (before the model runs).
3. **Claim extraction**: Typed, check-worthy claims extracted from the response stream.
4. **Binding verification**: Claims visibly bind to spans (or fail to bind, staying red).
5. **Three-axis reads**: Performance (unbound claim), Responsibility (ACL violation), Cost (dead compute steps) on the **same graph**.
6. **Matrix application**: R×S matrix appears with **R3 × unsupported-categorical = Escalate** for the refund action.
7. **Surgical edit**: Unproven claim **stripped** from the response (R1 action), not rewritten.
8. **Evidence packet**: Structured packet (claim + candidate spans + verdict) displayed for escalation (R3 action).
9. **Hold-back buffer**: Text streams to user with ~200ms trailing delay; payment action **held** separately.
10. **FNR format**: Per-route gate report schema shown with **empty placeholders** (labelled *illustrative format*).

**What it will deliberately NOT demonstrate** *(and why)*:
- **Bias detection** → Async counterfactual replay requires historical data not available in prototype. *Excluded to keep scope focused on core mechanism.*
- **Circuit breaker / autonomy downgrade** → System-level SRE mechanisms. *Excluded to maintain prototype simplicity.*
- **Proof cache** → Optimization, not core differentiation. *Excluded to avoid clutter.*
- **Shadow mode deployment** → Operational detail. *Excluded to keep demo focused.*
- **Multi-hop claim verification** → Complex NLI case. *Excluded to ensure reliability.*
- **Out-of-band stop-sequence injection** → Requires provider API integration. *Excluded due to integration complexity.*
- **Counterfactual bias replay** → Async mechanism. *Excluded to maintain live demo pace.*

**Minimum viable live demonstration** *(≤90 seconds, still feels advanced)*:
A **single end-to-end run** of the Customer Refund Processing use case:
- User requests refund citing *“clause 7.2”*.
- System shows **context assembly** capturing policy docs as spans (with ACLs).
- Model generates response with **6 claims**; one stays **red** (clause 7.2 does not exist).
- **Three-axis reads** flash on the graph: Performance (unbound), Responsibility (ACL check), Cost (4 of 9 steps grounded nothing).
- **Matrix** appears: R1=Edit, R3=Escalate for the same claim.
- Text streams to user with unproven claim **stripped** (Edit).
- Payment action **held** with evidence packet displayed (Escalate).
- FNR report **format** shown with empty fields.

---
---
### **4. Explicit Assumptions**

| **Category** | **Assumption** | **Justification** |
|--------------|---------------|-------------------|
| **Data Sources** | Policy documents and customer records include **source_id, ACL, hash** metadata at query time. | Standard in enterprise RAG/agent stacks; required for entitlement check. |
| **Data Sources** | Context assembly is a **distinct step before model invocation**. | True for all RAG/agent frameworks; the hook point for Provenance Recorder. |
| **Model Access** | Models accessed **only via API** (OpenAI-compatible). No weights, logits, or fine-tuning. | Matches enterprise reality; enables reverse-proxy deployment. |
| **Model Access** | Model outputs are **plain text** (no structured citations from the model). | Required for provenance captured *outside* the model. |
| **Traffic Shape** | Tens of thousands of interactions/week; **<10% are action-taking**. | Justifies budgeting verification by blast radius. |
| **Traffic Shape** | Mix of short (1–2 turn) and multi-turn conversations. | Prototype focuses on single-turn for clarity. |
| **Regulatory Posture** | **No real-time ground truth** available; audit trails must be tamper-evident. | Aligns with frozen architecture (shadow replay, hash-chained ledger). |
| **Regulatory Posture** | Compliance requirements vary by geography/industry. | Prototype assumes generic enterprise posture. |
| **Integration Surface** | Integration via **OpenAI-compatible reverse proxy + thin SDK hook**. | Matches frozen deployment shape (ARCHITECTURE.md §5.10). |
| **Integration Surface** | **No application rewrite** required. | SDK hook at context assembly only. |
| **Evaluation Data** | Prototype uses **simulated policy docs and customer data** (no real PII). | Enables live demo without compliance risk. |
| **Evaluation Data** | Ground truth for demo is **manually constructed**. | Acceptable for prototype; Round 2 will use real data. |
| **Technical** | Provenance capture adds **<10ms overhead**. | Validated in ARCHITECTURE.md §5.1. |
| **Technical** | Claim extraction (1–3B model) runs in **<50ms**. | Validated in ARCHITECTURE.md §3.1. |
| **Technical** | NLI cross-encoder (~300M) runs in **<15ms batched**. | Validated in ARCHITECTURE.md §3.1. |
| **Technical** | ACL checks are **sub-millisecond**. | Validated in ARCHITECTURE.md §3.3.1. |
| **Technical** | Deterministic recomputation is **sub-millisecond**. | Validated in ARCHITECTURE.md §3.1.2. |

---
---
### **5. Success Criteria for the Prototype**

A judge must be able to verify **all 10** criteria in a live or recorded demo. Each is **binary** (✅ PASS / ❌ FAIL).

| **#** | **Criterion** | **✅ PASS Condition** | **❌ FAIL Condition** |
|-------|---------------|----------------------|----------------------|
| 1 | **Graph Construction** | STEP → SPAN → CLAIM → ACTION graph built **in real-time** as response is generated. | Graph is static, pre-built, or not visible. |
| 2 | **Provenance Capture** | ≥3 spans visible with **source · ACL · hash** captured **before model runs**. | Provenance captured after generation or lacks metadata. |
| 3 | **Inverted Burden of Proof** | Claims start as **UNSUPPORTED (red)** and must earn SUPPORTED (green). | Default is allow, or unsupported is not the starting state. |
| 4 | **Three-Axis Reads** | Performance, Cost, Responsibility reads demonstrated on the **same graph**. | Any axis missing or shown separately. |
| 5 | **Matrix Application** | R×S matrix appears with **R3 × unsupported-categorical = Escalate**. | Matrix redrawn or cell values incorrect. |
| 6 | **Two-Pending-Actions** | Same unproven claim routes to **Edit (R1)** and **Escalate (R3)**. | Same claim routes to same action for both tiers. |
| 7 | **Surgical Edit** | Unproven claim **stripped or re-grounded**, not generatively rewritten. | Free-form LLM rewrite occurs. |
| 8 | **Evidence Packet** | Escalation shows **claim + candidate spans + verdict** in structured format. | Packet missing any of the three elements. |
| 9 | **Hard Gate on Actions** | Payment action **held** while text streams to user. | Action not gated or gated with text. |
| 10 | **FNR Format** | Per-route gate report **schema** visible with **empty placeholders** and *“illustrative format”* label. | Format missing, has fabricated numbers, or lacks label. |

---
---
### **6. Fidelity Self-Check**

| **Frozen Element** | **Status** | **Resolution** |
|---------------------|------------|----------------|
| **Default = UNSUPPORTED** | ✅ **Protected** | Prototype shows claims starting as red/UNSUPPORTED. |
| **Entitlement / ACL check** | ✅ **Protected** | Responsibility axis demonstrates ACL violation detection. |
| **Exact R×S matrix** | ✅ **Protected** | Matrix transcribed exactly from ARCHITECTURE.md §4. |
| **Hard gate on actions, not tokens** | ✅ **Protected** | Payment action held separately from text streaming. |
| **Published own FNR as a format** | ✅ **Protected** | Gate report schema shown with empty placeholders. |
| **Two-pending-actions resolution** | ✅ **Protected** | Same unproven claim routes to Edit (R1) and Escalate (R3). |

**Tension check**: **No tensions identified.** All prototype elements are fully aligned with the frozen Round 1 architecture.

---
---
### **7. Biggest Scope Risk + Exact Mitigation**

**Biggest Scope Risk**:  
The prototype attempts to demonstrate **too many mechanisms** and ends up showing *none* well. The most likely failure is diluting the core graph + matrix demonstration with async mechanisms (bias, circuit breaker) or optimizations (proof cache) that cannot be shown live or clutter the demo.

**Exact Mitigation**:  
- **Hard limit**: Prototype demonstrates **only** the core graph mechanism and matrix decision logic on the **Customer Refund** use case.
- **Time limit**: Demo must complete in **≤90 seconds**.
- **Mechanism limit**: Only mechanisms that can be **shown live and visually** are included.
- **Fallback rule**: If any mechanism cannot be demonstrated **reliably live**, it is **cut from the prototype** and moved to the business proposal or Q&A.

This ensures the prototype remains **focused, reliable, and differentiated**—exactly what Round 2 judges reward.