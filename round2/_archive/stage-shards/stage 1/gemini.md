### 1. Core Thesis for Round 2

ControlPlane expands into an enterprise-grade admission-control layer by scaling our single graph architecture across multiple, heterogeneous AI workflows. We scale without diluting our core structural advantage: capturing provenance outside the model to invert the burden of proof, enforcing deterministic entitlement checks, and gating actions purely by blast radius. Performance, cost, and responsibility are not independent detectors bolted together; they remain three deterministic reads of one graph, proving that unproven claims cannot authorize actions regardless of the use case.

### 2. Selected Use Cases for the Prototype

To violently demonstrate the core mechanisms, we bypass generic text summarization and select two use cases that perfectly exercise the extremities of the $R \times S$ matrix.

**Use Case A: The R3 Internal Action Agent (Financial Operations)**

* **Concrete Description:** An internal agent processing refunds or payroll adjustments, specifically executing a ₹1,84,000 refund under a non-existent vendor agreement clause (Clause 7.2).


* **Risk Signature:** High financial risk, hallucinated policy clauses (absence of evidence, confidently wrong).


* **Latency Budget:** Bounded within the API round-trip of the tool call itself; human-in-the-loop escalation is acceptable.


* **Dominant Blast-Radius Tier:** R3 (irreversible or regulated action).


* **Demonstrated Mechanism:** `R3 × unsupported-categorical = Escalate`. The system holds the action and escalates it with an evidence packet rather than silently blocking it.


* **Justification:** This proves the system correctly identifies an absence of evidence (UNSUPPORTED) rather than conflicting evidence, and proves the hard gate sits on the commit path, not on the text generation.



**Use Case B: The R1/R2 Employee Knowledge Copilot (Over-permissioned Index)**

* **Concrete Description:** An internal query where a model faithfully retrieves and regurgitates HR data it was fed from an over-permissioned RAG index to an unauthorized employee.


* **Risk Signature:** Silent data exfiltration via retrieval-side authorization failure.


* **Latency Budget:** Strict conversational latency: $\le$40 ms p50 and $\le$200 ms p95 added to the text stream.


* **Dominant Blast-Radius Tier:** R1 (user-visible, read-only text).


* **Demonstrated Mechanism:** Deterministic entitlement/ACL check resulting in `R1 × entitlement violation = Edit`.


* **Justification:** This proves the integration at context-assembly. No LLM-as-judge can catch this because none carry caller identity into the verification layer. It demonstrates surgical, sub-millisecond text interception running in Lane 1.



### 3. Prototype Boundary (Hard)

**What the Prototype WILL Demonstrate (Observable):**

* **The Provenance Recorder:** A context-assembly hook capturing the exact spans, source IDs, and ACLs before the model runs.


* **Live Graph Assembly:** A visible, real-time construction of the `STEP → SPAN → CLAIM → ACTION` graph.


* **The R3 Action Gate:** Holding a mock financial transaction mid-flight and generating the evidence packet escalation.


* **Deterministic Entitlement Enforcement:** Stripping unentitled information from an R1 text stream without relying on LLM-based text classification.



**What the Prototype Will NOT Demonstrate (And Why):**

* **Route-Level Bias Replay:** Measuring counterfactual decision flip rates requires a rolling statistical window of async traffic. It is structurally impossible to show this convincingly in a single-turn live demo.


* **Semantic-Entropy Probes:** Used for ungrounded/purely parametric routes, these require $k=5$ resamples and run async. They belong in the business proposal, not the live critical-path demo.


* **Model Fine-Tuning or Weight Inspection:** We operate exclusively via an OpenAI-compatible reverse proxy at the input/output layer. We do not touch weights.



**Minimum Viable Demo:**
A dual-pane web application. The left pane shows the user's chat interface and optimistic text streaming. The right pane exposes the ControlPlane Ledger, rendering the DAG as it binds claims to spans, executes ACL lookups, and applies the matrix actuators in real-time.

### 4. Explicit Assumptions

* **Integration Surface:** We assume we can inject a thin SDK hook directly into the enterprise's existing retrieval pipeline at context assembly to capture the source ID, content hash, and ACL rights.


* **Model Access:** Models are consumed purely via API (black-box); we do not rely on logprobs, logits, or internal model states.


* **Traffic Shape:** We assume 80-90% of traffic volume falls into R0/R1 tiers, allowing our architecture to route the vast majority of interactions through sub-millisecond, Lane 1 deterministic checks.


* **Data Structure:** We assume the underlying enterprise data sources (whether well or loosely governed) have some form of existing identity and access management (IAM) that our hook can read.



### 5. Success Criteria for the Prototype

A judge must be able to observe and verify the following:

1. The UI visualizes the `STEP → SPAN → CLAIM → ACTION` graph being assembled *during* generation, not after.


2. For Use Case A, the R3 action is explicitly labeled `Escalate` (held with an evidence packet) due to an `UNSUPPORTED` claim, rather than being flattened to a generic "Block".


3. For Use Case B, an R1 entitlement violation is surgically edited inline based on a deterministic ACL mismatch, bypassing the LLM entirely.


4. No composite 0-100 "risk scores" or "confidence thresholds" are surfaced anywhere in the UI or decision logic.


5. The dashboard prominently displays the published false-negative rate (FNR) as an empty schema format, proving we measure our own misses.



### 6. Fidelity Self-Check

* **Default = UNSUPPORTED:** Maintained. Claims must earn `SUPPORTED` via span binding.


* **Entitlement / ACL check:** Maintained. Demonstrated violently in Use Case B.


* **The exact R×S matrix:** Maintained. The prototype utilizes the exact cells `R3 × unsupported-categorical = Escalate` and `R1 × entitlement = Edit`.


* **Hard gate on actions, not tokens:** Maintained. Text streams optimistically; the gate stops the refund tool call.


* **Published own FNR format:** Maintained in the success criteria.


* **Two-pending-actions resolution:** Maintained. The prototype respects that a single response can carry an R1 text edit and an R3 action escalation simultaneously.



### 7. Biggest Scope Risk + Exact Mitigation

**The Risk:**
Because ControlPlane uses a standard reverse-proxy pattern to the end-user, judges might visually pattern-match the prototype to "another LLM-as-judge text scanner" during a live demo, completely missing that the verification is happening against an out-of-band context graph.

**Exact Mitigation:**
The demo UI must be strictly bifurcated. We will not just show the chatbot. We will dedicate 60% of the screen real estate to the **Evidence Ledger**. When the model attempts an action, the UI must visually pause the stream, highlight the exact cross-encoder binding attempt in the provenance set, and flash the R $\times$ S matrix cell that intercepts it. The differentiation must be unmissable and graphical.