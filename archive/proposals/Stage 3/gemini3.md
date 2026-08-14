## 1. Single Sharp Insight

An AI response is not text to be evaluated—it is a set of unverified claims requesting permission to execute an action. ControlPlane shifts oversight from probabilistic post-generation output scoring to deterministic execution gating bound directly to context-assembly provenance.

---

## 2. What the Market Currently Does (and Why Each Fails)

* **LLM-as-a-Judge:** Evaluating probabilistic outputs with another probabilistic model doubles latency and cost while running on the exact same failure surface. It creates a loop of hallucinations evaluating hallucinations.
* **Static Guardrails (e.g., NeMo, LlamaGuard):** Regex and token-level classifiers inspect content syntax at the perimeter, completely blind to semantic context, execution intent, or whether the model is authorized to access the underlying data.
* **Post-Hoc Observability Dashboards:** They log outputs and token counts *after* execution has occurred, turning enterprise risk management into an expensive autopsy report.
* **Confidence Thresholding / Logit Probing:** High LLM token probability correlates poorly with factual truth or safety; a model can be 99% confident while actively leaking data or executing hallucinated API parameters.
* **Simple RAG Checkers:** They compute fuzzy semantic similarity between prompt context and output text, ignoring action entitlements, dead-compute loops, and the real-world blast radius of execution.
* **Composite Risk Scores:** Averaging unrelated metrics (safety, cost, factual drift) into a single scalar obscures specific, actionable runtime failures and gives a false sense of security.

---

## 3. Positioning Statement

ControlPlane.ai is the first execution-time control plane that treats AI responses as unverified action requests bound to context provenance. While legacy guardrails passively monitor text or add massive latency with secondary LLM judges, ControlPlane binds claims to input evidence at context assembly, spending verification budget strictly in proportion to the blast radius of the requested action. By walking the `STEP → SPAN → CLAIM → ACTION` execution graph in real time, ControlPlane provides a deterministic, policy-enforced gate for enterprise AI—stopping dead compute, entitlement leakage, and ungrounded actions before impact.

---

## 4. Differentiation Table

| Common Approach | ControlPlane.ai |
| --- | --- |
| **Evaluates Output Text**<br>

<br>Scrapes generated strings post-hoc to infer quality or safety. | **Evaluates Action Requests & Provenance**<br>

<br>Binds claims directly to signed context-assembly hashes (`STEP → SPAN → CLAIM → ACTION`). |
| **Assumes Validity by Default**<br>

<br>Allows streaming until a perimeter rule or guardrail triggers. | **Inverted Burden of Proof**<br>

<br>Every claim defaults to `UNSUPPORTED` until validated against context evidence. |
| **All-or-Nothing Blocking**<br>

<br>Kills entire streams or lets dangerous payloads pass through entirely. | **Surgical Edits & Action Gates**<br>

<br>Hard-gates high-risk actions, redacts ungrounded sub-claims inline, and ships evidence packets on escalation. |
| **Flat Evaluation Compute**<br>

<br>Runs the same static checks regardless of what the AI is doing. | **Blast Radius-Proportional Verification**<br>

<br>Allocates verification budget dynamically using an $R_0–R_3 \times \text{Severity}$ matrix. |
| **Passive Metric Dashboarding**<br>

<br>Displays aggregate token counts and errors after deployment. | **Deterministic Graph-Walk Audit**<br>

<br>Traces dead compute backward to the exact span and publishes per-route false-negative rates live. |

---

## 5. Narrative Spine (3-Minute Video Sequence)

### **0:00–0:30 — Opening Hook**

* **Visual:** Split screen. On the left, a standard AI observability dashboard shows a green "Healthy" status. On the right, an autonomous AI agent uses an ungrounded claim to trigger an unauthorized database drop.
* **Script:** "Every enterprise AI tool today treats model outputs as text to be read and logged. But in production systems, text is an execution request. While your dashboard reads green, your agent just acted on an ungrounded hallucination."

### **0:30–1:15 — Problem + Reframe**

* **Visual:** Architecture diagram showing the flaw of secondary LLM judges (latency stack) vs post-hoc dashboards (autopsy reports).
* **Script:** "Evaluating probabilistic text with probabilistic LLM judges doubles your latency and cost without guaranteeing safety. We don't need another judge; we need an execution control plane. ControlPlane.ai shifts the paradigm: a response isn't text to score—it's a set of claims requesting permission to act."

### **1:15–2:15 — Core Mechanism + The Three-Axis Demo**

* **Visual:** Live execution graph walking down `STEP → SPAN → CLAIM → ACTION`.
* **Script:**
* *Context Assembly:* "At context assembly, we capture input provenance with an ACL hash outside the model."
* *Performance Axis:* "The model claims a policy number exists. ControlPlane's inverted burden of proof checks the hash—finding no match, it surgically redacts the claim while keeping the response intact."
* *Cost Axis:* "An agent loops. ControlPlane walks the graph backward, identifies zero state-change, detects dead compute, and kills the span."
* *Responsibility Axis:* "The model attempts a sensitive tool call. A deterministic entitlement check identifies an ACL mismatch and hard-gates the action before execution."



### **2:15–2:45 — Decision Logic / Why It Doesn't Over-Block**

* **Visual:** The $R_0–R_3 \times \text{Verdict Severity}$ Matrix showing non-blocking text vs hard-gated actions.
* **Script:** "How do we preserve speed? We don't block everything. For low-risk text ($R_0$), we stream optimistically with a short hold-back. For high-impact actions ($R_3$), we hard-gate execution. If a failure occurs, we don't just throw an error—we ship a structured evidence packet directly to human operators."

### **2:45–3:00 — Closing Line**

* **Visual:** ControlPlane terminal publishing its live per-route false-negative rate alongside system latency metrics.
* **Script:** "Stop reading what your AI generated *after* it acts. Start controlling what your AI is permitted to do *before* it executes. ControlPlane.ai."

---

## 6. What We Deliberately Refuse to Claim

1. **"We eliminate 100% of LLM hallucinations."**
* *Why we reject it:* Hallucination is a probabilistic property of auto-regressive generation. We claim to enforce evidence provenance and gate execution, not alter model weights.


2. **"Zero latency overhead across all checks."**
* *Why we reject it:* Verification requires compute. Claiming zero overhead signals a lack of technical depth. We claim *proportional latency* managed via optimistic streaming hold-backs and blast-radius budgeting.


3. **"Universal semantic intent understanding."**
* *Why we reject it:* Claiming perfect intent understanding sounds like marketing fluff. We rely on deterministic ACL matching, hash provenance, and formal claim-vs-proof extraction.


4. **"Autonomous prompt self-healing."**
* *Why we reject it:* Automatically re-prompting models introduces uncalibrated loops. We perform surgical inline redactions or export structured evidence packets for escalation.



---

## 7. Strongest Narrative Risk + Exact Correction

### **The Risk**

Judges mentally bucket ControlPlane as "just another guardrail API" (like NeMo Guardrails or LlamaGuard) sitting in an API gateway.

### **The Exact Correction**

Address this head-on within the first 45 seconds of the presentation:

> *"Guardrails inspect text strings at the network edge using syntax rules; they are completely blind to whether the system actually gave the model the facts it is citing. ControlPlane is integrated at context assembly—it doesn't inspect string syntax, it validates claim entitlement against signed context hashes before an action can fire."*