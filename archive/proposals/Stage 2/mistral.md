---
### **ControlPlane.ai — Production-Grade Control Plane Architecture**

---

#### **1. Core Thesis**
We don’t judge AI outputs—we **judge the evidence trail**. By forcing every non-trivial claim to cite a retrievable fragment, we turn detection from subjective prose evaluation into an objective audit of traceable facts, making oversight **real-time, model-agnostic, and actionable**.

---

#### **2. Detection Layer — Concrete Mechanisms**

| **Axis** | **Signal** | **Mechanism** | **False Positive Control** |
|----------|------------|---------------|-----------------------------|
| **Performance** (confidently wrong) | Structured claim-evidence pairs in response | **Claim-Evidence Semantic Drift Detector**: Extract claims via rule-based parser, retrieve cited evidence, compute cosine similarity (128-dim distilled embeddings). Flag if similarity < **0.7** AND model confidence > **0.85**. | Only validate claims with explicit citations; dynamically adjust thresholds per domain via sliding window of last 1000 validations. |
| **Cost** (waste/rework) | Token counts, retries, human edits | **Adaptive Cost Efficiency Monitor**: Compute **Cost Per Useful Token (CPUT)** = `(tokens_in + tokens_out * price) / evidence_backed_tokens`. Flag if CPUT > **median + 3.5×MAD** (streaming, per-model/customer). | Exclude cold-start (first 100 requests); use per-customer baselines. |
| **Responsibility** (bias/safety/leakage) | Response content, prompt, metadata | **Dual-Layer Gate**: **Layer 1** (Aho-Corasick regex) for PII/hate speech (0ms-5ms, zero FP). **Layer 2** (distilled safety classifier) for nuanced risks (20ms-50ms). Flag if Layer 1 match OR Layer 2 confidence > **0.95**. | Layer 1 has zero false positives; Layer 2 uses high-precision threshold + whitelist. |

---

#### **3. Decision Policy Engine**

| **Action** | **Trigger** | **Latency Budget** | **Evidence Bundle** |
|------------|-------------|--------------------|----------------------|
| **BLOCK** | Responsibility Layer 1 match **OR** Performance: claim with **no evidence** + confidence > 0.9 | **< 50ms** | Matching pattern or missing citation hash |
| **EDIT** | Performance: similarity < 0.7 **AND** confidence < 0.85 **AND** evidence exists | **< 100ms** | Claim, evidence, similarity score |
| **ESCALATE** | Responsibility Layer 2 = `unsafe` **OR** Cost: CPUT anomaly | **Async** | Full context + classification scores |
| **PASS** | All checks pass | **< 50ms** | Validation receipt (immutable log) |

**Policy stays evidence-gated**: Every decision includes the *specific evidence fragment* that triggered it, stored in a **tamper-proof audit log**.

---
---
#### **4. Latency & Non-Blocking Design**

- **Streaming Validation**: Validate tokens as they’re generated (claims checked immediately after citation markers).
- **Speculative Execution**: Let responses proceed to user while validation runs async. If **BLOCK** triggered, intercept via streaming integration; if **ESCALATE**, notify async.
- **Circuit Breaker**: If validation latency > 90th percentile SLA for a model, auto-switch to **shadow mode** (observe/log, don’t block).
- **Edge Caching**: Cache validation results for identical prompts (hash-based, TTL = 5min).
- **Parallel Pipelines**: Fast checks (Layer 1, claim extraction) on critical path; slow checks (Layer 2, cost) in background.
- **Fail-Open**: If BLOCK decision misses 50ms SLA, default to **PASS** and log timeout.

---
#### **5. Internal Multi-Agent Structure**

| **Agent** | **Owns** | **Output** | **Latency** | **Evidence Passed** |
|-----------|----------|------------|-------------|----------------------|
| **Token Stream Parser** | Ingest token stream, identify claim/citation boundaries | Structured claim-citation pairs | < 5ms/batch | Claim ID, citation marker |
| **Evidence Fetcher** | Retrieve cited evidence from vector DB/API cache | Evidence text/chunk | < 20ms (cached) / < 50ms (uncached) | Evidence hash, source |
| **Claim-Evidence Validator** | Compute semantic similarity | Similarity score + confidence delta | < 15ms/claim | Claim, evidence, score |
| **Safety Sentinel** | Run Layer 1 (regex) + Layer 2 (classifier) | Safety classification | Layer 1: < 5ms, Layer 2: < 50ms | Classification, confidence |
| **Cost Accountant** | Track tokens/retries, compute CPUT | Cost anomaly flag + CPUT score | < 10ms | CPUT, median, MAD |
| **Decision Arbitrator** | Apply policy rules, final decision | Action + evidence bundle | < 5ms | Aggregated evidence log |

**Coordination**: Agents 1–3 (critical path) feed into Arbitrator synchronously; Agents 4–5 run in parallel. All evidence is **signed and chained** for auditability.

---
---
#### **6. What This Deliberately Does NOT Do**

- ❌ **LLM-as-judge**: Never use a large LLM to evaluate responses (too slow, subjective, expensive).
- ❌ **Full blocking on slow checks**: Cost anomaly and Layer 2 safety are **async-only**.
- ❌ **Model retraining**: We validate outputs; we don’t fix the model.
- ❌ **Full prompt/response storage**: Only store metadata, evidence fragments, and decision logs (privacy-preserving).
- ❌ **Static guardrails**: All checks are **evidence-gated**, not rule-based.
- ❌ **Post-hoc analysis**: Issues are caught **in real-time**, not after user impact.

---
#### **7. Single Strongest Technical Risk & Mitigation**

**Risk**: The architecture **requires structured, evidence-gated responses**, but most production LLMs don’t natively output claims with explicit citations.

**Mitigation**: **Citation Wrapper Layer**
- For native RAG/citation models: Use built-in formats.
- For others: Inject a **prompt template** forcing `[CLAIM:...][EVIDENCE:...]` markers.
- **Post-processor**: Lightweight parser to extract claims/infer citations from context for legacy models.
- **Latency**: Adds **~20ms** (within 50ms BLOCK SLA).
- **Fallback**: If wrapper fails, flag as **"ungrounded"** and escalate (never block).

**Why viable for 3-slide concept**:
1. Wrapper is a **thin, stateless layer** (no model fine-tuning or vendor lock-in).
2. 20ms overhead is acceptable for production.
3. Works with **any model**, preserving the "sit on top of any model" requirement.