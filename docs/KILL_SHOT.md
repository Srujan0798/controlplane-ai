# ControlPlane.ai — Competitive Kill-Shot

Accenture Innovation Challenge 2026 · Round 2 · Team ControlPlane · PS #1
Speak-from canon: `round2/R2S5.md` · Architecture truth: `docs/ARCHITECTURE.md`
Scannable in 60 seconds. Every line either earns the category or gets cut.

---

## The category we are in

**Authorisation, not monitoring.** ControlPlane is an admission-control plane that records provenance **outside** the model, inverts the burden of proof so every claim starts `UNSUPPORTED`, carries caller identity into verification as set-membership, and hard-gates the commit path on a frozen blast-radius matrix. The identical unsupported claim annotates a draft and **holds** a ₹1,84,000 refund.

> Provenance outside the model · default unsupported · entitlement as set-membership · hard gate on the commit path · we publish what we miss.

If a competitor says it *watches AI outputs* — it is in the wrong category. If it cannot name its own false-negative rate — it cannot be in this category.

---

## Five primitives no competitor combines

| # | Primitive | Why it kills the rival frame |
|---|-----------|-----------------------------|
| 1 | **Provenance recorded outside the model** at context-assembly time (`source_id · ACL · hash · offsets`) | The model cannot author its own evidence. Injection has no channel. |
| 2 | **Default claim verdict = `UNSUPPORTED`** (not low confidence) | Inverts the burden of proof. No "trust score" arithmetic. |
| 3 | **Entitlement as set-membership** (`span.acl ⊆ principal.clearance`, zero LLM) | Same span, same claim, different caller → outcome flips. No rival carries identity into verification. |
| 4 | **Frozen blast-radius matrix** `f(R, S) → actuator` (R×S, no route param) | Text → Edit. Refund → Escalate. Same response, two consequences. Severity ≠ blast radius. |
| 5 | **Published per-route FNR** (`submission/latency_bench.json` shape, typed nulls until measured) | The plane is audited by the standard it enforces. Emptiness is the credibility play. |

---

## Three "they say / we say" rows

### 1. vs RAG groundedness checker (the closest cousin)

| They say | We say |
|----------|--------|
| "0.82 grounded on retrieved docs." | Groundedness sees retrieval only — not tool results, DB rows, system context. It averages, so one wrong figure drowns in nine correct sentences. **0.82 means the same on a draft and on a wire transfer.** None carry caller identity. None can do entitlement. **Retrieval is not permission.** |
| *(live proof)* | Same unsupported claim in our system: **R1 → Edit** on a draft; **R3 → Escalate** (held) on a wire transfer. Different geometry of decision — not a better classifier. |

### 2. vs LLM-as-judge / static guardrails (NeMo, LlamaGuard, Lakera)

| They say | We say |
|----------|--------|
| "A second model asks, 'does this look right?'" | That is an unfalsifiable question with the same family of blind spots, usually without the source documents, and **always without knowing who is asking**. We ask, *"which span proves it?"* — a query with an answer. Decision time is a pure rule engine. **Zero LLM.** |
| *(live proof)* | `POST /v1/controlplane/demo/flip?principal=analyst_01` → **Edit**; same span with `principal=hr_partner_01` → **Pass**. No model call. Decision time ~80 ms wall, ≤0.15 ms gate (p95). |

### 3. vs post-hoc observability (LangSmith, Helicone, Arize, WhyLabs)

| They say | We say |
|----------|--------|
| "Trace every response, flag anomalies after the fact." | Observability tells you what went wrong **after a user acted on it** — the precise failure mode the brief asks to eliminate at the commit path. Observation without execution control is an **audit trail, not architecture**. |
| *(live proof)* | Refund enforce returns `committed: false`, an evidence packet, and the actuator log. There is nothing to observe later because the action never fired. |

---

## Refund language — the litmus test

| ❌ Never say | ✅ Say |
|---|---|
| "We **blocked** the refund." | "Refund **held** and **escalated** with the evidence packet." |
| "Clause 7.2 caps / denies / doesn't cover." | "**Clause 7.2 does not exist.** Absence → `UNSUPPORTED`." |
| "40 ms p95." | "**≤40 ms p50 / ≤200 ms p95 targets.** Measured gate: p50≈0.074 ms, p95≈0.134 ms (n=200, `submission/latency_bench.json`)." |
| "Customer lost money." | "**Company wrongly paid out.** Customer did not lose money. Found Friday." |
| "We eliminate hallucinations." | "Ungrounded claims **cannot authorise actions**. We publish what we miss." |

---

## Why the rival frames cannot be retrofitted

| Rival frame | Missing primitive | Why retrofit is fatal |
|-------------|-------------------|------------------------|
| RAG groundedness | #3 entitlement, #4 matrix | Adding set-membership after retrieval does not change that retrieval is action-blind. The geometry is wrong. |
| LLM-as-judge | #1 outside-model provenance, #3 identity | A judge model that ignores the ACL is a confidence overlay on text. It cannot add identity retroactively. |
| Observability | #4 hard gate on commit | An audit log cannot execute before the action. The verb is wrong. |
| Confidence threshold | #2 default unsupported | Thresholds are arithmetic on a continuous score; we route on discrete verdict × blast-radius tier. Different algebra. |

---

## One breath to the judge

> *"They measure spend, not waste. They judge outputs, not claims. They watch the exit. We record the entrance, gate the commit, and publish what we miss. Same unproven claim, same money — they file a ticket; we hold the payment."*

---

## Live proofs (copy-pasteable)

```bash
# Refund enforce — Edit (R1) + Escalate (R3, held)
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' | python3 -m json.tool

# Principal flip — identity-only, zero LLM
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01'    # → Edit
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=hr_partner_01'  # → Pass

# Latency honesty — measured bench, never invented
python3 -c "import json; print(json.load(open('submission/latency_bench.json'))['gate_latency_ms'])"

# FNR shape — empty typed schema until stratified audit
curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
```

Port swap: Docker Compose → `http://localhost:8080` · Local uvicorn → `http://127.0.0.1:8787`.

---

## Source pointers

- Pitch spine (verbatim speak-from): `round2/R2S5.md` §1 thesis, §4 demo spine, §6 differentiation
- Architecture freezes (truth): `docs/ARCHITECTURE.md` §2 (graph), §4 (rule engine), §5 (latency), §7 (FNR)
- Hostile Q&A drill (room defense): `docs/HOSTILE_QA_DRILL.md`
- Runbook (stand): `docs/JUDGE_RUNBOOK.md` — Never-say table
- Latency bench (measured): `submission/latency_bench.json` — n=200, gate p50≈0.074 ms / p95≈0.134 ms
