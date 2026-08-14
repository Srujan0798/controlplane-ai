---
### **ControlPlane.ai — Positioning & Narrative Architecture**

---

#### **1. Single Sharp Insight**
AI responses are not text to be scored—they are **claims requesting permission to act**. ControlPlane inverts the burden of proof: every claim is *unsupported* until bound to the evidence the model was *actually* given at context-assembly time.

---

#### **2. What the Market Currently Does (and Why Each Fails)**

| **Approach** | **Failure Against ControlPlane** |
|--------------|-----------------------------------|
| **LLM-as-judge** | Uses another model to score output—subjective, unauditable, and the judge itself has no provenance. |
| **Static guardrails** | Hard-coded rules that can’t adapt to context or evidence; brittle against adversarial prompts. |
| **Post-hoc observability dashboards** | Looks at what happened *after* the damage is done; zero real-time blocking power. |
| **Confidence thresholding** | Trusts model confidence, which is uncorrelated with correctness; overconfident models bypass it. |
| **Simple RAG checkers** | Only verifies *presence* of citations, not semantic alignment; easily gamed. |
| **Composite risk scores** | Blends signals into a single number; loses traceability and actionability. |

---

#### **3. Positioning Statement**
ControlPlane.ai is the first **action-gated verification layer** that treats every AI response as a set of claims requesting permission to act. It binds each claim to the evidence captured at context-assembly time—with ACLs and cryptographic hashes—then spends verification budget in proportion to blast radius. Unlike tools that score text after the fact, ControlPlane inverts the burden of proof, defaults to *unsupported*, and turns oversight from a post-mortem into a real-time gate that doesn’t slow what matters.

---

#### **4. Differentiation Table**

| **Common Approach** | **ControlPlane’s Fundamental Difference** |
|---------------------|--------------------------------------------|
| LLM-as-judge | **Deterministic verification** via provenance graphs; no model judges another. |
| Static guardrails | **Dynamic entitlement checks** derived from actual ACLs captured at context assembly. |
| Post-hoc dashboards | **Hard gate on actions**, not analytics; blocks *before* harm occurs. |
| Confidence thresholding | **Inverted burden of proof**: default = UNSUPPORTED; evidence must be *proven*, not guessed. |
| Composite risk scores | **Blast Radius R0–R3 × Verdict Severity matrix** for surgical, traceable decisions. |

---
---
#### **5. Narrative Spine (3-Minute Video Beat Sequence)**

| **Time** | **Beat** | **Script + Visual** |
|----------|----------|---------------------|
| **0:00–0:30** | **Opening Hook** | *"Every AI deployment today has the same flaw: it treats answers as text to be scored, not as claims requesting permission to act."* (Visual: Red "ACCEPT" button stamped blindly on a stream of AI responses.) |
| **0:30–1:15** | **Problem + Reframe** | Market solutions—LLM judges, static rules, dashboards—all evaluate *after* the model has decided. The real problem: **no provenance, no inverted burden of proof.** (Visual: Three dominant patterns failing in sequence.) |
| **1:15–2:15** | **Core Mechanism + Three-Axis Demo** | Walk the graph: **STEP → SPAN → CLAIM → ACTION**. Show provenance captured at context assembly (ACL + hash), deterministic ACL leakage detection, dead compute measured by walking the graph backward. (Visual: Animated graph with three colored reads—performance, cost, responsibility.) |
| **2:15–2:45** | **Decision Logic** | Hard gate on actions, optimistic text streaming with short hold-back. Surgical edit only; escalate ships **structured evidence packet**. Plane publishes its own **per-route false-negative rate**. (Visual: Decision matrix with Blast Radius × Severity.) |
| **2:45–3:00** | **Closing Line** | *"ControlPlane doesn’t monitor AI. It **grants or denies permission**—with the evidence to prove it was right."* (Visual: Green "PERMISSION GRANTED" or red "PERMISSION DENIED" stamp on the same response stream from the hook.) |

---
#### **6. What We Deliberately Refuse to Claim**

- ❌ **"We make AI safe"** — Too broad; implies absolute guarantees. We **gate actions with auditable evidence**.
- ❌ **"We catch 100% of errors"** — False promise. We **publish our per-route false-negative rate** instead.
- ❌ **"We work with any model out of the box"** — We **require provenance capture at context assembly**; no shortcuts.
- ❌ **"We reduce costs by X%"** — We **measure dead compute exactly** by walking the graph backward, but don’t make generic savings claims.

---
#### **7. Strongest Narrative Risk + Exact Correction**

**Risk**: Judges hear *"AI monitoring"* and mentally file it with every other guardrail/observability tool.

**Correction**: **Replace every instance of "monitor," "observe," or "guardrail" with "gate," "permission," or "verification."**
- ❌ *"ControlPlane monitors AI responses..."*
- ✅ *"ControlPlane **gates AI actions**..."*
- ❌ *"Our observability layer..."*
- ✅ *"Our **permission layer**..."*

The architecture doesn’t *watch* AI—it **controls what AI is allowed to do**. Language must reinforce that we are a **control plane**, not a dashboard.