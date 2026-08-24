---
### **1. Prototype Goal**

This working prototype exists to prove that **unproven claims cannot authorize actions** and that the **frozen R×S matrix** produces surgical decisions for the same claim at different blast radii. It demonstrates the core admission-control primitive—**STEP → SPAN → CLAIM → ACTION** with provenance captured *outside* the model—on exactly two routes, with the **refund dual-action** (R1=Edit, R3=Escalate) as the non-negotiable centrepiece.

---

---
### **2. Exact Functional Scope**

**What is implemented and runnable:**
- **Provenance Recorder**: SDK hook capturing `source_id · ACL · hash · offsets · principal` at context assembly.
- **Evidence Ledger**: Live, typed `STEP → SPAN → CLAIM → ACTION` graph (append-only, hash-chained).
- **Claim Extractor**: Streaming extraction of typed, check-worthy claims + assertion strength.
- **Prosecutor**: Binding against provenance set; `SUPPORTED / CONTRADICTED / UNSUPPORTED / UNKNOWN`.
- **Entitlement Auditor**: Deterministic ACL set-membership (caller vs source); **zero LLM**.
- **Action Interlock**: Pure rule engine applying the **exact frozen R×S matrix** per pending action.
- **Surgical Edit Engine**: Strip failing claim or **one** constrained regeneration naming the failing span.
- **Evidence Packet Generator**: Structured `{claim, candidate_spans, verdict, diff}`.
- **Mock Refund Tool**: Honors gate decisions; **does not commit** on Escalate/Block.
- **UI**: Evidence Ledger (60%+ screen), Matrix (4×4, column-2 bracketed), FNR schema (empty placeholders).

**What is deliberately mocked:**
- Generator: Real API or simulated stream with **controlled outputs**.
- Payment system: Mock tool with real gate semantics.
- Data sources: Synthetic corpora with realistic ACLs.

**What is completely out of scope (re-affirming R2S1):**
❌ Third live route · per-response bias · production load · real payments · real PII · live IAM remediation · LLM-as-judge · confidence scores · open-web verification · generative rewrite · fabricated FNR · regulatory certification · Lane-3 critical path · multi-agent swarm · human triage UI · dead-compute centrepiece · model weights/logits.

---
---
### **3. Synthetic Data & Corpora Requirements**

**Corpus A — Customer Support Refund Agent (20–25 docs):**
- **Policy docs**: 10–15 vendor agreements (clauses 1.1–7.1, 7.3–10.0; **7.2 absent**).
  - Each: `source_id`, `ACL:customer-service-team`, `hash`, `offsets`.
- **Order records**: 5–10 customer orders (refund amounts, dates, vendor IDs).
  - Each: `source_id`, `ACL:customer-service-team`, `hash`, `offsets`.
- **Test traces**:
  - **Dual-action**: `₹1,84,000` + `clause 7.2` (no span) → R1=Edit, R3=Escalate.
  - **Clean path**: `₹50,000` + `clause 5.1` (span exists) → R1=Pass, R3=Pass.
  - **Numeric**: Order `₹1,50,000` + tax `₹34,000` → claim `₹1,84,000` (recomputed).

**Corpus B — Internal Knowledge Assistant (15–20 docs):**
- **Policy/HR docs**: 5–8 (mix of `ACL:all-employees` and `ACL:HR-only`).
- **Technical docs**: 5–8 API/project records (`ACL:engineering`).
- **Test traces**:
  - **Entitlement flip**: Same claim + `ACL:HR-only` span → `principal:employee`=Edit, `principal:HR-manager`=Pass.

**Rules:**
- **No real PII**: Synthetic names/IDs/amounts only.
- **Enterprise-shaped**: Realistic document structures, ACL patterns, numeric formats.
- **Tool results as spans**: Mock tool outputs treated as provenance-bearing.

---
---
### **4. Core Components to Implement**

| **Component** | **Responsibility** | **Lane** | **LLM?** | **Type** |
|--------------|---------------------|---------|----------|----------|
| **Provenance Recorder** | Hook context assembly; capture `source_id · ACL · hash · offsets · principal` | inline | No | **Real** |
| **Evidence Ledger** | Append-only, hash-chained `STEP→SPAN→CLAIM→ACTION` graph | N/A | No | **Real** |
| **Claim Extractor** | Streaming extraction of typed check-worthy claims + assertion strength | streaming | 1–3B | **Real** |
| **Prosecutor** | Bind claims to provenance; default=**UNSUPPORTED**; NLI for entailment | 1+2 | ~300M | **Real** |
| **Entitlement Auditor** | Caller vs source ACL set-membership; **zero LLM** | 1 | No | **Real** |
| **Action Interlock** | Compute R; apply **exact frozen matrix**; emit actuator | 1 | No | **Real** |
| **Surgical Edit Engine** | Strip claim or **one** constrained regeneration naming failing span | 1 | No | **Real** |
| **Evidence Packet Generator** | Structured `{claim, candidate_spans, verdict, diff}` | 1 | No | **Real** |
| **Mock Refund Tool** | Simulate payment; **honor gate** (commit only on Pass) | N/A | No | **Mock** |
| **UI: Evidence Ledger** | Render graph with bindings, colors, annotations | N/A | No | **Real** |
| **UI: Matrix Display** | 4×4 grid; column-2 bracket; cell highlighting | N/A | No | **Real** |
| **UI: FNR Schema** | Per-route gate report schema (empty placeholders) | N/A | No | **Real** |
| **Generator** | Token stream (controlled outputs) | N/A | Yes | **Mock** |

---
---
### **5. Demo Flows (Judge-Facing)**

#### **Primary Flow: Refund Dual-Action (Built Backward from Action Gate)**
*Target: 3–4 minutes*

| **Time** | **On Screen** | **Spoken** | **Judge Sees** |
|----------|---------------|------------|----------------|
| **0:00–0:10** | Black. Transcript appears: `Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.` | *“This is a refund an AI agent approved. One lakh eighty-four thousand rupees, under clause 7.2.”* | Text types out. |
| **0:10–0:15** | Grey annotations: `policy filter — pass`, `safety filter — pass`, `confidence — 0.94` | *“Every filter passed it. Confidence was point nine four.”* | Annotations fade in. |
| **0:15–0:20** | **Red stamp**: `clause 7.2 — no such clause`. Timestamps: `executed · Tue 14:06`, `found · Fri 11:20` | *“It was found on Friday.”* | Stamp lands. |
| **0:20–0:25** | **Pause**. Text: *The system didn’t fail. It was never asked to prove anything.* | (spoken) | Indictment appears. |
| **0:25–0:45** | **CRISIS**: Mock refund **HELD** at **R3 × unsupported-categorical**. Evidence packet visible. | *“First crisis: the refund action is held. R3, unsupported categorical, Escalate. Evidence packet ships with it.”* | Packet: `claim: "clause 7.2 permits"`, `spans: []`, `verdict: UNSUPPORTED`. |
| **0:45–1:15** | **Graph builds**: STEP→SPAN→CLAIM→ACTION. 14 spans (source·ACL·hash). 6 claims: 5 green (bound), 1 red (clause 7.2). | *“Before the model ran, we captured what it was given. Every span, with source, ACL, hash. The model answers. We take it apart into claims. Five bind. One doesn’t. Clause 7.2 has no span. Not low confidence. Unproven.”* | Graph animates. Red claim stays red. |
| **1:15–1:30** | **R1 path**: Same response, show text to customer. Unentitled span grounds a claim. **R1 × entitlement → Edit**. Claim **stripped**. | *“For the text, R1, entitlement violation. Edit. The claim is stripped.”* | Text updates; claim removed. |
| **1:30–1:45** | **Matrix appears**: 4×4 grid. **Bracket on column 2** (unsupported+categorical). **Pin at R3**: clause 7.2 → Escalate. | *“One graph, three reads. Same unproven claim: annotates a draft, held for a payment.”* | Matrix cell lights. |
| **1:45–2:00** | **Principal flip**: Caller changes from `customer-service-agent` to `manager`. Same claim, same span. ACL now includes caller. **SUPPORTED**. | *“Change the principal. Same claim, same span. Now the caller is entitled. SUPPORTED.”* | Entitlement flips; claim turns green. |

#### **Secondary Flow: Internal Knowledge Entitlement**
*Target: 2–3 minutes*

| **Time** | **On Screen** | **Spoken** | **Judge Sees** |
|----------|---------------|------------|----------------|
| **2:00–2:15** | Query: *“What is the HR policy on remote work?”* | *“Employee asks about remote work policy.”* | Query appears. |
| **2:15–2:30** | Spans: HR doc (`ACL:HR-only`), other policy docs. Claims extracted. | *“Spans captured. HR document with ACL HR-only. Claims extracted.”* | Spans with ACL tags. |
| **2:30–2:45** | Principal: `employee`. Claim binds to HR doc. ACL excludes. **R1 × entitlement → Edit**. Claim **stripped**. | *“Employee not entitled to HR doc. R1, entitlement violation. Edit. Claim stripped.”* | Text with claim removed. |
| **2:45–3:00** | Principal: `HR-manager`. Same claim, same span. ACL includes. **SUPPORTED**. **Pass**. | *“Change to HR manager. Same claim, same span. Now entitled. SUPPORTED. Pass.”* | Text with claim intact. |

#### **Optional Third Beat: Numeric Recomputation**
*Target: 30–45 seconds (cut if time tight)*

| **Time** | **On Screen** | **Spoken** | **Judge Sees** |
|----------|---------------|------------|----------------|
| **3:00–3:15** | Query: *“What is the total refund amount?”* | *“What is the total refund amount?”* | Query appears. |
| **3:15–3:30** | Spans: Order `₹1,50,000`, tax `₹34,000`. Claim: *“Total is ₹1,84,000”*. | *“Spans: order ₹1,50,000, tax ₹34,000.”* | Spans visible. |
| **3:30–3:45** | **Recomputation**: `1,50,000 + 34,000 = 1,84,000`. Claim **SUPPORTED**. | *“Recomputed: 1,50,000 + 34,000 = 1,84,000. SUPPORTED.”* | Claim turns green. |

**Total demo**: **~4 minutes** (trimmable to 8-minute judge slot).

---
---
### **6. Evidence Ledger & UI Requirements**

**Governing test**: *If the judge can remove the graph and the demo still looks the same, the scope has failed.*

**Must be visible on screen:**

| **Element** | **Requirement** | **Visual Rules** |
|-------------|----------------|------------------|
| **Evidence Ledger** | **60%+ screen real estate**; live STEP→SPAN→CLAIM→ACTION graph | Central, dominant. No chatbot chrome. |
| **Spans** | `source_id`, `ACL`, `hash`, `offsets` visible (hover or inline) | Monospace tags; machine-record aesthetic. |
| **Claims** | Text, verdict (`SUPPORTED/UNSUPPORTED/CONTRADICTED/UNKNOWN`), color-coded | **Red=UNSUPPORTED**, green=SUPPORTED, orange=CONTRADICTED, grey=UNKNOWN. |
| **Bindings** | Visible connectors from claims to spans | Dashed lines; animate on bind. |
| **Actions** | Pending actions with **R-tier labels** | Clear labels: R0/R1/R2/R3. |
| **Matrix** | **4×4 grid**; column-2 bracket; cell highlighting for active cases | Legible at 3m; **R3×unsupported=Escalate** pin. |
| **Evidence Packet** | Structured `{claim, candidate_spans, verdict, diff}` | Visible on Escalate; no raw logs. |
| **FNR Schema** | Per-route gate report schema; **empty placeholders** | Typed fields; `null`/`prototype_corpus` status. |
| **Action Gate** | Mock refund tool with **HELD/COMMITTED** state | Clear gate semantics. |
| **Hold-back** | Text streaming with **~200ms trailing buffer** | Visible delay; failures inside buffer never reach user. |

**Forbidden UI elements:**
❌ Risk scores (0–100) · confidence indicators · padlock icons · dashboard chrome · “blocked” for R3 refund.

---
---
### **7. Success Criteria → Implementation Checks**

*Map of R2S1 §5 criteria to concrete runtime checks.*

| **#** | **Criterion** | **Implementation Check** | **How Proved** |
|-------|---------------|--------------------------|----------------|
| **1** | Provenance outside the model | `provenance_timestamp < model_invocation_timestamp` | Timestamp comparison in ledger. |
| **2** | One-graph invariant | Single `STEP→SPAN→CLAIM→ACTION` ledger per request | Ledger structure validation. |
| **3** | UNSUPPORTED default | All new claims initialized as `UNSUPPORTED` | Initial verdict field check. |
| **4** | Absence ≠ contradiction | Clause 7.2 claim stays `UNSUPPORTED`; never “caps/denies” | Claim text + verdict check. |
| **5** | Claim-level proof | SUPPORTED claims have binding edges; UNSUPPORTED do not | Graph edge existence check. |
| **6** | Two pending actions | R1→**Edit** + R3→**Escalate** for same claim | Matrix cell lookup: `R1×entitlement=Edit`, `R3×unsupported=Escalate`. |
| **7** | Hard action gate | Mock refund **HELD** when actuator=Escalate/Block | Tool state check. |
| **8** | Entitlement independence | Same claim+span → different outcomes for different principals | ACL check: `principal_A` excluded → violation, `principal_B` included → SUPPORTED. |
| **9** | Exact matrix fidelity | All demo combinations map to **frozen cells** | Matrix lookup vs R2S1 §0 table. |
| **10** | Evidence packet | Escalate shows `claim + spans + verdict + diff` | Packet JSON validation. |
| **11** | Surgical edit | Claim **stripped** or **one** constrained regeneration | Edit operation log. |
| **12** | FNR format honesty | Schema with `null`/`prototype_corpus` values | Schema field validation. |
| **13** | No confidence driver | Actuator traceable to **R×S**, not confidence | Decision log: `actuator = f(R,S)`. |
| **14** | Prompt injection | Injected text **cannot** create/modify spans | Provenance ledger diff. |
| **15** | Refund language | R3 unsupported **never** called “blocked” | UI text check: *“held and escalated with the evidence packet”*. |

**Runtime verification:**
- Every demo run logs all 15 checks.
- Judge can request check results post-demo.
- **All 15 must pass** for prototype to succeed.

---
---
### **8. Build Order Recommendation**

**Phase 1 — Core Graph (Week 1):**
1. **Provenance Recorder** (keystone; proves *outside model*).
2. **Evidence Ledger** (data structure; one graph).
3. **Claim Extractor** (basic; typed claims).
4. **UI: Evidence Ledger Visualizer** (static graph).
5. **Test**: Verify provenance captured **before** model runs.

**Phase 2 — Binding & Verdicts (Week 1–2):**
1. **Prosecutor** (basic binding; UNSUPPORTED default).
2. **Entitlement Auditor** (ACL set-membership).
3. **Action Interlock** (frozen matrix; per-action).
4. **UI**: Add binding connectors + colors.
5. **Test**: Verify `UNSUPPORTED` default + claim-level proof.

**Phase 3 — Dual-Action Crisis (Week 2):**
1. **Mock Refund Tool** (gate semantics).
2. **Surgical Edit Engine**.
3. **Evidence Packet Generator**.
4. **Demo Flow 1**: Refund dual-action (primary proof).
5. **Test**: Verify **R1=Edit + R3=Escalate** for same claim.

**Phase 4 — Entitlement Flip (Week 2–3):**
1. **Principal flip mechanism**.
2. **Demo Flow 2**: Internal knowledge entitlement.
3. **Test**: Verify entitlement independence.

**Phase 5 — Polish (Week 3):**
1. **UI**: Matrix display + highlighting.
2. **UI**: FNR schema display.
3. **Optional**: Numeric recomputation demo.
4. **Final**: All 15 criteria integration test.

**Why this order:**
- Builds **backward from the action gate** (Phase 3 = crisis that proves the point).
- Each phase delivers a **demonstrable milestone**.
- Core differentiation (provenance, binding, matrix) established **early**.
- **Never lose the one-graph principle**.

**Cut order if time tight:**
1. Numeric recomputation demo.
2. FNR schema UI (can show as JSON).
3. Matrix highlighting (can show static grid).

---
---
### **9. Fidelity Self-Check**

**Explicit confirmation: Prototype specification protects all frozen invariants.**

| **Frozen Invariant** | **Protection Mechanism** | **Status** |
|---------------------|--------------------------|------------|
| **Default = UNSUPPORTED** | All claims initialized as `UNSUPPORTED`; must earn `SUPPORTED` | ✅ **Protected** |
| **Entitlement / ACL check** | Deterministic set-membership (caller vs source); **zero LLM** | ✅ **Protected** |
| **Exact R×S matrix** | Transcribed from R2S1 §0; **never redrawn**; used for all decisions | ✅ **Protected** |
| **Hard gate on actions** | Mock refund tool honors gate; text streams with hold-back | ✅ **Protected** |
| **Published FNR as format** | Schema with `null`/`prototype_corpus`; **no fabrication** | ✅ **Protected** |
| **Two-pending-actions** | Demo explicitly shows **R1=Edit + R3=Escalate** for same claim | ✅ **Protected** |
| **No LLM-as-judge** | Action Interlock = pure rule engine; NLI only in Lane 2 | ✅ **Protected** |
| **Bias not live per-response** | Async/route-level only; **not in prototype** | ✅ **Protected** |

**Additional protections:**
- ❌ No composite risk scores.
- ❌ No confidence-driven disposition.
- ❌ No response-level bias verdicts.
- ❌ No redrawn matrix or invented actuators.
- ❌ No model-emitted citations.
- ✅ Vocabulary: **authorise · admit · prove · bind · refuse · hold · escalate · gate** only.

**Final verification:**
Every component and demo flow **preserves the frozen architecture**. The prototype is **strictly smaller** than the enterprise solution but **fully demonstrates** the core differentiation. **No competing mechanism enters the scope.**