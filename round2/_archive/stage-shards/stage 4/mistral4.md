---
### **1. Problem Framing**

Enterprises run AI that **acts**—refunds, files, sends, writes to production—while oversight is still built for the answering era. Existing tools score text after the fact, form opinions about correctness, or check surface forms, but **none can prevent a wrong action from executing**. The cost of a wrong output has changed category: **it used to be a bad paragraph. It is now an executed transaction.** This is not a generic “AI risk” problem—it is a **category shift** from observation to admission control, and the gap is structural: current solutions inspect outputs, not the evidence the model was given before it ran.

---
---
### **2. Solution Design Summary**

ControlPlane.ai is an **admission-control layer** that treats every AI action as a set of claims requesting permission to act. It captures provenance *outside the model* at context assembly—`source_id · ACL · hash · offsets`—with the calling principal recorded. Every check-worthy claim starts **UNSUPPORTED** and must earn proof against that provenance. Entitlement is a deterministic set-membership test (caller vs source ACL). The Action Interlock applies the exact frozen R×S matrix per pending action, hard-gating **actions—not tokens**—with verification budget priced by blast radius. Performance, cost, and responsibility are **three reads of one graph**: **STEP → SPAN → CLAIM → ACTION**. The system doesn’t score text; it **gates actions on proof**.

---
---
### **3. Target Users & Buyers**

| **Role** | **Pain** | **Economic Buyer** | **Technical Buyer** | **Day-to-Day User** |
|----------|----------|---------------------|---------------------|---------------------|
| **CFO** | Wrong actions cost money (₹1,84,000-class errors) | ✅ | | |
| **CTO** | Dead compute waste, rework costs, technical debt | ✅ | | |
| **CISO** | Data leakage, unauthorized access, security incidents | ✅ | | |
| **Head of AI/ML** | Model reliability gaps, oversight blind spots | | ✅ | |
| **Platform Engineering** | Integration complexity, latency constraints | | ✅ | |
| **AI Application Owners** | Over-flagging (alert fatigue), under-flagging (liability) | | | ✅ |
| **DevOps** | Deployment, monitoring, operational overhead | | | ✅ |

**Primary targets**: CFO (economic) + Head of AI/ML (technical) + AI Application Owners (day-to-day). **Secondary**: CTO, CISO, Platform Engineering.

---
---
### **4. Business Case & Impact Logic**

**Value creation (directional, defensible):**

| **Impact Vector** | **Logic** | **Concrete Example** |
|-------------------|-----------|----------------------|
| **Avoid wrong actions** | Hard gate on actions prevents executed transactions that shouldn’t happen | ₹1,84,000 refund under non-existent clause 7.2 **held, not paid** |
| **Reduce dead compute** | Exact measurement via graph backward walk enables targeted optimization | “₹5 of ₹8 grounded nothing” — waste identified, not estimated |
| **Reduce alert fatigue** | Matrix ensures surgical decisions (Edit/Escalate/Block) proportional to blast radius | R1 text passes with annotation; R3 payment held — no one-size-fits-all blocking |
| **Auditability** | Evidence Ledger provides tamper-evident trail for every decision | `action → claim → span → principal → matrix cell` fully traceable |

**Why this matters**: The system doesn’t just catch errors—it **prevents harmful actions** while allowing beneficial ones to proceed. This is the category shift from *observability* to *admission control*. **No fabricated ROI percentages**; the logic is defensible and the examples are concrete.

---
---
### **5. Phased Roadmap**

| **Phase** | **Goal** | **Scope** | **Enforcement** | **Success Criteria** | **Duration** |
|-----------|----------|-----------|----------------|----------------------|--------------|
| **0: Prototype** | Prove the admission primitive | Exactly 2 routes (Refund + Knowledge) | None (shadow) | Dual-action resolution (R1 Edit + R3 Escalate) demonstrated | 4–6 weeks |
| **1: Limited Production** | Earn enforcement on high-value routes | Customer Support Refund + 1 other | Shadow → Canary (5%) → **Earned** | Counterfactual: *“would have held N, of which M were true positives”* | 6–8 weeks |
| **2: Multi-Route Deployment** | Scale to all enterprise AI routes | Support + Knowledge + Decision-Support | Full enforcement on **earned** routes | Per-route FNR published with CIs | 3–4 months |
| **3: Enterprise Optimization** | Optimize based on operational data | All routes + cost controls + bias measurement | Full enforcement | Dead compute reduced; override rates minimized | 6–12 months |
| **4: Platform Hardening** | Production-grade reliability | HA/failover, multi-tenant, real IAM | Full enforcement | SLA compliance; zero downtime | 12+ months |

**Key principle**: Enforcement is **earned per route** through shadow evidence, **never switched on globally**. The matrix and entitlement checks remain **invariant** across all phases.

---
---
### **6. Key Risks & Mitigations**

| **Risk** | **Impact** | **Mitigation** | **Residual** |
|----------|------------|----------------|--------------|
| **False assurance on derived claims** | High — subtle wrong synthesized claims marked SUPPORTED | Route derived claims to deterministic recomputation; **UNKNOWN never → SUPPORTED**; verifier model family decorrelated from generator; publish FNR stratified by claim type | Low — UNKNOWN boundary is absolute |
| **Over-permissioned source indexes** | Medium — faithfully enforces wrong ACLs | Make violations visible in ledger; entitlement-violation rate per source = detector; quarantine connectors via policy; **honest boundary**: we enforce existing ACLs, don’t fix IAM | Low — detection is deterministic |
| **Cold-start performance** | Medium — new routes lack baselines | Exclude cold-start from cost baselines; default to pass with annotation for R0/R1; shadow mode default; rapid calibration via canary | Low — conservative defaults |
| **Alert fatigue / over-flagging** | High — users bypass the system | Blast-radius pricing (R0/R1 mostly Lane 1); R0/R1 fail open with annotation; matrix ensures proportional response; auto-rollback on override rate > 3× baseline | Low — matrix prevents over-blocking by design |
| **Under-flagging / liability** | High — missed harmful actions | Default = **UNSUPPORTED** (hostile verdict); hard gate on actions (R2/R3 fail closed or escalate); shadow earn-out per route; publish per-route FNR | Low — hostile default + earned enforcement |
| **Integration cost perceived as too high** | Medium — teams expect “drop-in” | Clear communication: **integration cost is the moat**; SDK hook + reverse proxy (days, not quarters); if you have context assembly, you’re 80% there | Low — transparency builds trust |
| **Team switches it off** | High — over-blocking leads to disablement | Hard gate on **actions only** (text streams optimistically); R0/R1 (80–90% of volume) passes with annotation; matrix prevents over-blocking by design | Low — users don’t feel the gate |
| **Regulatory non-compliance** | Medium — evolving regulations outpace updates | Additive policy overlays (geo/industry); versioned DAG policies; **cannot loosen frozen invariants**; audit trail for all decisions | Low — policy flexibility without architectural drift |

---
---
### **7. Differentiation Anchor**

**The 7 sharpest differentiators** (consistent with NARRATIVE.md §4 and QA.md A1–A3):

| **#** | **ControlPlane** | **Everyone Else** | **Why It Matters** |
|-------|------------------|-------------------|-------------------|
| **1** | **Provenance captured outside the model** at context assembly (`source_id · ACL · hash · offsets`) | Inspect output *after* generation | Verification is deterministic and tamper-proof; evidence exists *before* the model runs |
| **2** | **Default = UNSUPPORTED** (inverted burden of proof) | Default allow, flag what looks wrong | Claims must *earn* SUPPORTED; prevents false assurance |
| **3** | **Entitlement check** = deterministic caller-vs-source ACL **set-membership** | Identity-blind (same string fine for one caller, breach for another) | Catches the most common enterprise incident: over-permissioned RAG index leaking HR data |
| **4** | **One graph, three reads** (STEP→SPAN→CLAIM→ACTION) | Three separate tools: hallucination detector + privacy detector + action safety | Unified architecture; performance, cost, responsibility are reads of the *same* structure |
| **5** | **Exact frozen R×S matrix** (transcribed, never redrawn) | Composite risk scores; one threshold for all traffic | Surgical decisions per action; **proof scales with consequence** |
| **6** | **Hard gate on actions, not tokens** | Gate on text output | Users perceive model speed; harm is prevented at the *commit boundary* |
| **7** | **Publish per-route false-negative rate** (format) | Publish precision (rate at which they bother the user) | **The plane is audited by the standard it enforces**; transparency builds credibility |

**Against named competitors**:
- **NeMo Guardrails / LlamaGuard**: Inspect strings at perimeter with syntax rules; **blind to whether the system ever gave the model the fact it is citing, and blind to who is asking**.
- **RAG Groundedness Checkers**: See **retrieval only** (not tool results, DB rows, computed values); **average** (one wrong figure drowns in nine correct sentences); **action-blind** (0.82 means the same on a draft and a wire transfer).
- **LLM-as-Judge Wrappers**: Produces an opinion using the same reasoning that produced the error; **cannot state its own error rate**; too slow to stand in front of an action.
- **Observability Tools (LangSmith, etc.)**: Tell you what went wrong **after** a user acted on it—the precise thing the brief asks to eliminate.

**The unifying move**: We don’t score text—we **gate actions on proof**. The evidence that proves an output existed *before* the model ran, and we capture it.

---
---
### **8. Fidelity Self-Check**

**Explicit confirmation: Nothing in the business proposal softens or weakens frozen invariants.**

| **Frozen Invariant** | **Status** | **Protection Mechanism** |
|----------------------|------------|--------------------------|
| **Default = UNSUPPORTED** | ✅ **Untouched** | All claims must earn SUPPORTED; absence of proof is not low confidence |
| **Entitlement / ACL check** | ✅ **Untouched** | Deterministic set-membership; **zero LLM**; identity in verification layer |
| **Exact R×S matrix** | ✅ **Untouched** | Transcribed exactly from ARCHITECTURE.md; **never redrawn**; no route-specific cells |
| **Hard gate on actions, not tokens** | ✅ **Untouched** | Text streams with hold-back; **actions gated at commit boundary** |
| **Published FNR as format** | ✅ **Untouched** | Empty schema with typed placeholders; **no fabricated production numbers** |
| **Two-pending-actions resolution** | ✅ **Untouched** | R1 **Edit** + R3 **Escalate** for same claim; **never one response-level verdict**; never call the refund “blocked” |
| **No LLM-as-judge on critical path** | ✅ **Untouched** | Action Interlock is a **pure rule engine**; NLI only in Lane 2 |
| **Bias as async/route-level** | ✅ **Untouched** | Counterfactual flip-rate + CI; **never per-response verdict** |

**Additional protections**:
- ❌ No claim that the system **eliminates hallucinations**
- ❌ No claim of **“zero integration”** or **“zero added latency”**
- ❌ No claim of **“99% accuracy across bias/safety/risk”**
- ❌ No **composite risk scores**
- ❌ No **confidence-driven disposition**
- ❌ No **response-level bias verdicts**
- ✅ **Vocabulary discipline**: **authorise · admit · prove · bind · refuse · hold · escalate · gate** only

**Final verification**: Every element in this proposal **preserves or extends** the frozen architecture. Nothing **softens, weakens, or replaces** the core differentiation. The business case is built on **defensible logic**, not fabricated claims.