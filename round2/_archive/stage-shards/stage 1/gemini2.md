Here is the Expanded Solution Architecture for ControlPlane.ai, engineered strictly against the frozen Stage 1 invariants to meet the highest adversarial standard for Round 2.

---

## 1. Expanded Core Thesis

ControlPlane scales from a single verification graph into an enterprise-wide admission-control plane by decoupling the universal evidence lifecycle from route-specific decision policies. Every application—whether a low-latency draft or a high-stakes financial agent—shares the exact same context-assembly provenance hook, inverting the burden of proof so all claims start `UNSUPPORTED`. The identical `STEP → SPAN → CLAIM → ACTION` graph routes through a versioned, deterministic rule engine that prices verification dynamically by blast radius. This architecture enforces localized regulatory and risk compliance without fragmenting the core product, ensuring provenance, entitlement, and action gating remain unbreakable structural invariants.

---

## 2. Multi-Route Architecture

The system avoids becoming a disjointed suite of tools by enforcing a rigid separation between the shared evidence infrastructure and the per-route decision parameters.

**What is Shared (The Invariants):**

* **The Provenance Recorder:** The context-assembly SDK hook capturing `source_id · ACL · hash · offsets` before the model runs.


* **The Streaming Extractor:** The 1–3B model operating at sentence boundaries to extract typed, check-worthy propositions.


* **The Evidence Ledger:** The append-only, hash-chained `STEP → SPAN → CLAIM → ACTION` data structure.


* **The R×S Matrix:** The transcribed routing logic mapping blast radius and verdict severity to exactly four actuators (`Block`, `Edit`, `Escalate`, `Pass`).



**What is Configured per Route:**

* **Action Interlocks & Blast Radius ($R$):** The mapping of application intents to $R$-tiers. For a chatbot, outputting text maps to $R1$; for a refund agent, the payment payload maps to $R3$.


* **Fail Stances:** $R0/R1$ fail open with annotation; $R2/R3$ fail closed or escalate on timeout.


* **Check-Worthiness Thresholds:** Domain-specific filter lists to bypass extraction for known-safe lexical patterns, preventing false positives before compute is spent.



**How the Matrix is Applied:**
Heterogeneous risk is managed not by changing the matrix, but by changing the $R$-tier of the pending action. When a refund agent emits a claim with an unsupported categorical verdict, the exact same matrix reads the text path as $R1 \times unsupported = Edit$, and the payment path as $R3 \times unsupported = Escalate$.

---

## 3. Governance & Policy Layer

The Action Interlock is a pure rule engine. There is strictly zero LLM reasoning at decision time.

* **Configurable Policy Surface:** Policies are encoded as versioned 4-tuples `(signal, threshold, action, latency_budget)` in a Directed Acyclic Graph (DAG).


* *Geography / Regulatory:* Configures the allow-listed action grammar (e.g., masking rules for EU vs. US) and dictionary-based PII targets.
* *Risk Appetite:* Dictates the route's error budget (SRE-style circuit breakers) and shadow-mode evaluation thresholds.




* **Validation & Rollout:** No threshold change affects live traffic without a shadow replay over the last $N$ traces to generate a precise True Positive / False Positive delta.


* **Audit Trail:** Every decision is permanently hashed in the Evidence Ledger, containing the caller principal, source IDs, span hashes, and exact latency spent. If a human override rate in canary exceeds $3\times$ the baseline, the policy auto-rolls back.



---

## 4. Feedback & Learning Loops

We reject the industry default of retraining models on failure logs. Generative mechanics and verification logic remain structurally decoupled.

* **What is Learned:** Human overrides and shadow outcomes calibrate *route thresholds*. Streaming median + 3.5×MAD for cost anomalies, check-worthiness filter heuristics (removing domain-specific safe phrases that cause FP bloat), and per-route precision/FNR are updated continuously.


* **What Remains Rule-Based:** The $R \times S$ matrix, the tier fail stances, the entitlement Aho-Corasick pass, and the deterministic arithmetic recomputation are hardcoded and mathematically immune to feedback loop contamination.


* **What is Never Learned From:** The generator LLM is never fine-tuned on the evidence packets. The system never trains a secondary LLM-as-judge on human triage data.



---

## 5. Metrics, Monitoring & Trustworthiness Reporting

Observation without execution control is merely an audit trail. ControlPlane reports architectural realities, not generalized risk scores.

* **Per-Route False-Negative Rate:** The credibility move. We publish our own miss rate via a stratified shadow audit (100% of blocks/escalations + random slice of passes sampled to expensive ground truth). The format ships as an empty schema (e.g., `{"route": "A", "metric": "FNR", "value": null, "ci": null}`) to definitively prove we do not fabricate production accuracy.


* **False-Positive / Override Rates:** Tracked per route. An escalation without a subsequent human modification counts as an FP and flags the route for threshold tuning.
* **Dead Compute:** Billed waste is computed exactly. The engine walks the graph backward; any generation step grounding zero accepted claims is categorized and priced as dead compute.


* **Latency by Lane:** Measured strictly as added p50 and p95 per route (e.g., $\le 40$ ms p50, $\le 200$ ms p95 for $R0/R1$ text).


* **Entitlement Violations:** Logged deterministically against a named principal and a named source ID, highlighting retrieval-side authorization failures rather than vague "safety" flags.



---

## 6. Complete Enterprise Solution vs Prototype

* **What the Full Solution Contains:** The enterprise deployment scales across thousands of routes via the OpenAI-compatible reverse proxy, managing jurisdiction-specific policy packs, live shadow replays, CI/CD policy rollbacks, and active synchronization with enterprise IAM.


* **What the Stage 1 Prototype Deliberately Shows:** The non-negotiable core. A single interactive session displaying the context-assembly hook, the strict `UNSUPPORTED` default, the exact matrix logic, the deterministic ACL flip for the knowledge route, and the dual-action resolution ($R1$ Edit / $R3$ Escalate) for the refund agent.


* **What Remains Proposal-Only (Including Bias):** Production-scale load testing, full IAM remediation, and bias measurement. Bias remains distributional and async—measured via counterfactual flip-rate with a confidence interval over a rolling window. It is explicitly refused as a per-response verdict.



---

## 7. Residual Risks & Explicit Mitigations

| Residual Risk | Exact Mitigation |
| --- | --- |
| **False assurance on derived/synthesized claims** (NLI entailment is weakest on multi-hop reasoning)

 | Route away from NLI entirely. Arithmetic or aggregative claims are deterministically recomputed from spans. Claims that are neither recomputable nor directly entailed return `UNKNOWN`, which never collapses into `SUPPORTED`.

 |
| **Over-permissioned source index** (ControlPlane flawlessly enforces a flawed ACL)

 | Visibility via logging. Every entitlement decision is recorded against a named principal and source ID. The plane transforms a silent model-memory leak into an observable identity configuration error.

 |
| **Parametric Hallucinations** (The model fabricates an answer with zero retrieval context)

 | Routes lacking provenance are declared ungrounded by construction. They are bound strictly by blast radius: they can annotate a draft ($R0$) but structurally cannot authorize a payment ($R3$). Async semantic-entropy probes measure dispersion for route calibration.

 |

---

## 8. Fidelity Self-Check

This expansion strictly preserves the Stage 1 Scope Lock invariants:

* **Softens Default = UNSUPPORTED:** Untouched. Every newly extracted claim begins as `UNSUPPORTED` and must earn proof.


* **Weakens or removes the entitlement check:** Untouched. It remains a deterministic set-membership test using caller principal vs. source ACL.


* **Redraws the R×S matrix:** Untouched. The matrix retains exactly four actuators, driven purely by verdict severity and blast radius.


* **Moves the hard gate from actions to tokens:** Untouched. Text streams optimistically behind a hold-back buffer; tool commits face the hard interlock.


* **Introduces LLM-as-judge on the critical path:** Untouched. Decision policy is governed purely by a rule engine.


* **Collapses the two-pending-actions resolution:** Untouched. The system independently edits the $R1$ text while escalating the $R3$ tool call on the same graph.


* **Turns bias into a per-response verdict:** Untouched. Bias remains solely an async, route-level counterfactual measurement.