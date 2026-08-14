## 1. Single Sharp Insight

Every other system inspects AI outputs as text after generation and asks whether they look acceptable; ControlPlane treats every response as an unprivileged execution claim that cannot act until it proves its entitlement against the exact evidence captured at context-assembly time. The burden of proof is inverted and held by the response, not the operator.

---

## 2. What the Market Currently Does (and Why Each Fails)

**LLM-as-judge.** Replaces one unverified generative process with another. Circular trust with no grounding in actual provenance; the judge hallucinates exactly when the original model does.

**Static guardrails and regex blocklists.** Decay immediately in production. They block safe utterances that match a pattern and miss dangerous ones that do not, because they have no concept of what the response is about to *do*.

**Post-hoc observability dashboards.** Discover harm after the user has already acted on it. You cannot un-send a biased loan decision, un-leak PII, or un-burn compute. Observation without execution control is an audit trail, not architecture.

**Confidence thresholding.** Confidence is not correlated with correctness. Models are confidently wrong precisely when they appear most certain; thresholding on confidence selects for the most dangerous failures.

**Simple RAG checkers.** Verify that retrieval happened, not that the response is entitled to act on what was retrieved. Retrieval is not permission.

**Composite risk scores.** Collapse multi-dimensional, incommensurable risks into a single scalar. A cost anomaly and a data-leakage event become indistinguishable numerically, destroying the signal required for surgical intervention.

---

## 3. Positioning Statement

ControlPlane.ai is an execution-boundary layer that sits between any AI model and the outside world, treating every generated response as an unprivileged claim that must prove its entitlement before it acts. Unlike monitoring tools that observe after the fact or guardrails that pattern-match on text, ControlPlane captures provenance at context-assembly time—with ACL and hash, outside the model—binds each claim to the exact evidence the model was given, and enforces an inverted burden of proof: default unsupported. It matters now because enterprises are moving from AI experimentation to AI execution, and the difference between finding out that a model failed and finding it before it acts is the difference between a dashboard and a control plane.

---

## 4. Differentiation Table

| Common Approach | How ControlPlane is Fundamentally Different |
|---|---|
| **LLM-as-judge** scores outputs for quality after generation | No model judges another model. Claims are verified against captured provenance with deterministic entitlement checks. |
| **Static guardrails** and regex blocklists | No static lists. Verification budget is spent in proportion to blast radius; an R0–R3 × Severity matrix governs every intervention. |
| **Post-hoc observability** dashboards | Observation is not separate from control. The same graph that detects deviation gates execution before the user acts. |
| **Composite risk scores** and thresholding | Risk is never collapsed to a scalar. Unsupported, Uncertain, and Supported are verdicts on individual claims, not aggregate numbers. |
| **Confidence-based** filtering | Confidence is not evidence. Default state is UNSUPPORTED; a claim must positively prove its entitlement against the actual context it received. |

---

## 5. Narrative Spine — 3-Minute Video

**0:00–0:30 | Opening Hook**  
"Six weeks. That is how long a production AI system leaked sensitive customer data before a post-hoc audit found it. The dashboard was green. The logs were complete. The harm was already done. This is not a tooling failure. It is an architectural category error: we built observation layers for systems that need execution boundaries."

**0:30–1:15 | Problem + Reframe**  
"Every current approach treats the model's output as text to be scored after generation. LLM-as-judge, static guardrails, composite risk scores—they inspect the response and ask, 'Does this look okay?' That is the wrong question. The right question is: 'What is this response claiming it is entitled to do, and can it prove it against the evidence it was actually given?' ControlPlane.ai is not a monitor. It is an execution boundary that treats every AI response as an unprivileged claim requesting permission to act."

**1:15–2:15 | Core Mechanism + Three-Axis Demo**  
"Here is how it works. At context assembly—before the model ever sees the prompt—we capture provenance with ACL and hash, outside the model. The model responds. We decompose that response into claims against the evidence graph: Step, Span, Claim, Action.

Performance: Is this claim supported by the graph, or unsupported? Inverted burden of proof—default is UNSUPPORTED.

Cost: We walk the graph backward and measure dead compute exactly. Does this response trigger rework, redundant API calls, wasted tokens?

Responsibility: Deterministic entitlement check. Does this claim access data outside its ACL? Is there leakage?

Three reads of one graph. Not three separate tools. One control plane."

**2:15–2:45 | Decision Logic / Why It Does Not Over-Block**  
"We do not over-block because we do not use composite scores. We use a Blast Radius R0 to R3 crossed with Verdict Severity matrix. Low blast radius, uncertain claim? Surgical edit. High blast radius, unsupported action? Hard gate, and we ship a structured evidence packet to a human. For text, optimistic streaming with short hold-back—fast where safe, gated where dangerous. And the plane publishes its own per-route false-negative rate, so you know exactly what it misses instead of pretending it sees everything."

**2:45–3:00 | Closing Line**  
"Monitoring tells you the plane crashed. ControlPlane is the air traffic control. Build the boundary, or remain a passenger."

---

## 6. What We Deliberately Refuse to Claim

- **"We eliminate all AI risk."** We publish our own false-negative rates precisely because we know the plane misses things; claiming perfection would signal naivety.
- **"Zero latency overhead."** We use optimistic streaming with short hold-back; we spend verification budget proportionally. Claiming zero overhead is dishonest and destroys credibility.
- **"Fully autonomous with no human in the loop."** We explicitly escalate with structured evidence packets; humans are a designed component of the architecture, not a failure mode.
- **"Powered by a proprietary safety-trained foundation model."** We sit on top of any model. Claiming a proprietary model contradicts our model-agnostic position and smells like vaporware.

---

## 7. Strongest Narrative Risk + Exact Correction

**Risk:** A judge hears "bias, safety, leakage" and pattern-matches to yet another AI safety/guardrail tool. The architecture collapses into the same category as a dozen other teams, and the systems depth is lost.

**Exact Correction:** Lead every sentence with *execution* and *entitlement*, never with *safety*. If the first fifteen seconds mention ethics, trust, or responsible AI, the narrative is dead. The opening hook must be about a leaked loan decision or burned compute budget—an execution failure, not a moral one. Frame the three axes as reads on a permission graph, not as ethical guardrails. The word "safety" should appear only after "deterministic entitlement check" and "ACL violation," never as a standalone virtue.