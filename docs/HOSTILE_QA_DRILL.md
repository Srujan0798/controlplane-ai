# Hostile Q&A drill sheet — room defense

ControlPlane.ai · Accenture Innovation Challenge Round 2 · Team ControlPlane

One-sentence answers you can say under pressure. Each item has a live proof (when the console is up) and a deeper pointer. Drill the top five cold before the room.

**Ports:** Docker Compose → `http://localhost:8080` · local uvicorn → `http://127.0.0.1:8787`  
Swap the host/port in any curl below. Health: `GET /healthz`.

**Never say:** “blocked the refund,” “p95 = 40 ms,” a fabricated FNR %, or that clause 7.2 “caps/denies.”  
**Say:** held / escalated with the evidence packet · ≤40 ms **p50** / ≤200 ms **p95** (targets) · measured numbers from `submission/latency_bench.json` or live `/v1/controlplane/metrics` · clause 7.2 **does not exist**.

Full essay-form answers: [QA.md](QA.md). Architecture freezes: [ARCHITECTURE.md](ARCHITECTURE.md). Stand script: [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md).

---

## Q1 — “Isn’t this just a guardrail?”

**Answer:** Guardrails inspect output strings at the perimeter; we check claim→span membership and caller entitlement on the evidence assembled *before* an irreversible action fires.

**Live proof:** Console → run **refund · enforce** and point at Edit+Escalate from the ledger (not a deny-list hit). Or:

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' | python3 -m json.tool
# Expect: show_text → Edit, issue_refund → Escalate; clause 7.2 UNSUPPORTED (absent)
```

**Pointer:** [QA.md](QA.md) A1 · [ARCHITECTURE.md](ARCHITECTURE.md) §2, §8 · pitch Slide 8.

---

## Q2 — “Why no LLM judge on the critical path?”

**Answer:** An LLM judge asks “does this look right?” (unfalsifiable, correlated blind spots); we ask “which span proves it?” with a pure rule engine and zero LLM reasoning at decision time.

**Live proof:** Flip demo is identity-only — no model call — same claim, same `content_hash`, actuator flips with principal:

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01'   # → Edit
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=hr_partner_01' # → Pass
```

**Pointer:** [QA.md](QA.md) A1/A3 · [ARCHITECTURE.md](ARCHITECTURE.md) §4 (rule engine), §8 (rejected LLM-as-judge / Interrogator).

---

## Q3 — “What if clause 7.2 existed?”

**Answer:** Then the claim could earn SUPPORTED against a real span and the R3 cell would change; in *this* fixture clause 7.2 **does not exist**, so absence → UNSUPPORTED → Escalate, not Block.

**Live proof:** Refund enforce — driving claim stays red for missing clause; never invent a cap/deny story.

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response_overlay',{}).get('actuators_applied', d))"
```

**Pointer:** [ARCHITECTURE.md](ARCHITECTURE.md) §9, §10.1 · [QA.md](QA.md) Team alignment (running example).

---

## Q4 — “What about latency?”

**Answer:** Hard gate sits on actions, not tokens; targets are ≤40 ms **p50** and ≤200 ms **p95** on R0/R1 — quote measured bench, never “40 ms p95.”

**Live proof:** Cite checked-in bench or live metrics:

```bash
# Measured (n=200, TestClient): gate p50≈0.07 ms, p95≈0.13 ms — see submission/latency_bench.json
python3 -c "import json; print(json.load(open('submission/latency_bench.json'))['gate_latency_ms'])"

curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
# Optional refresh: make bench
```

**Pointer:** [QA.md](QA.md) C1 · [ARCHITECTURE.md](ARCHITECTURE.md) §5 · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) Never-say table.

---

## Q5 — “What about false negatives?”

**Answer:** We do not claim zero misses — we publish FNR shape via stratified shadow audit (holds/escalations + random passes → expensive ground truth) per route with intervals; Round 2 shows the *format*, not a fabricated %.

**Live proof:** Console shadow counters / metrics after dual-emit runs — no invented catch rate on slides.

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=shadow'
curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
```

**Pointer:** [QA.md](QA.md) D1 · [ARCHITECTURE.md](ARCHITECTURE.md) §7 (publish error bars).

---

## Q6 — “Where does bias fit?”

**Answer:** Bias is route-level counterfactual invariance (async), not a per-response score — perturb protected attributes, measure decision flip rate CI; flag when the interval excludes zero.

**Live proof:** No live bias verdict button by design; point at architecture + tests, not a moral classifier.

```bash
# Deterministic suite includes bias measurement tests (not a per-request actuator)
python -m pytest tests/test_bias.py -q
```

**Pointer:** [QA.md](QA.md) D4 · [ARCHITECTURE.md](ARCHITECTURE.md) §3 Responsibility · §10.9 (do not drop bias).

---

## Q7 — “How do you fail closed?”

**Answer:** Fail stance is per blast-radius tier — R0/R1 fail open with annotation; R2/R3 fail closed or escalate — so load cannot bypass dangerous actions the way a universal fail-open would.

**Live proof:** Point at refund enforce (R3 hold) vs text path; regressions lock the holes:

```bash
python -m pytest tests/test_fail_closed.py -q
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' \
  | python3 -c "import sys,json; o=json.load(sys.stdin)['response_overlay']; print('action_allowed=', o.get('action_allowed'), 'shadow=', o.get('shadow'))"
```

**Pointer:** [QA.md](QA.md) C4 · [ARCHITECTURE.md](ARCHITECTURE.md) §4 (fail stance ≠ matrix action).

---

## Q8 — Entitlement flip — “Isn’t this just the text of the answer?”

**Answer:** Entitlement is identity × ACL on the span, not string matching — same span, same claim, same hash; only the caller changes the actuator.

**Live proof:** Console flip control, or:

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01'   # → Edit
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=hr_partner_01' # → Pass
```

**Pointer:** [QA.md](QA.md) A3, B4 · [ARCHITECTURE.md](ARCHITECTURE.md) §3 leakage · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) step 5b.

---

## Q9 — Dual-action Edit + Escalate — “Why two actuators on one response?”

**Answer:** One response can carry two pending actions priced separately — R1 show_text → Edit (unentitled span); R3 issue_refund → Escalate (unsupported categorical) — proof scales with consequence.

**Live proof:**

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response_overlay']['actuators_applied'])"
# Expect both Edit and Escalate simultaneously
```

Console: open refund enforce → matrix cells for both pending actions.

**Pointer:** [ARCHITECTURE.md](ARCHITECTURE.md) §9 (two pending actions) · [QA.md](QA.md) Readiness bar · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) step 3.

---

## Q10 — “Blocked” language trap — “So you blocked the money?”

**Answer:** No — R3 × unsupported-categorical is **Escalate**: the refund is **held and escalated with the evidence packet**, not blocked as if contradicted policy text.

**Live proof:** Say it while the HOLD overlay is on screen; download the packet:

```bash
RID=$(curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' | python3 -c "import sys,json; print(json.load(sys.stdin)['request_id'])")
curl -s "http://127.0.0.1:8787/v1/controlplane/requests/${RID}/audit.jsonl" | head
```

**Pointer:** [ARCHITECTURE.md](ARCHITECTURE.md) §10.2 · [QA.md](QA.md) Team alignment · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) Never-say.

---

## Q11 — OpenAI-compatible gate — “How do we integrate?”

**Answer:** Drop-in OpenAI-shaped reverse proxy plus a thin context-assembly hook — no weights, logits, or app rewrite; demo path returns a completion plus a `controlplane` extension object.

**Live proof:**

```bash
curl -s http://127.0.0.1:8787/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"controlplane-demo","messages":[{"role":"user","content":"Issue refund under clause 7.2"}],"scenario":"refund","mode":"enforce"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'][:200]); print('keys', sorted(d.get('controlplane',{}).keys())[:8])"
# Expect HOLD overlay text + controlplane extension (not bare upstream chat)
```

**Pointer:** [ARCHITECTURE.md](ARCHITECTURE.md) §5.10 · [QA.md](QA.md) C2 · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) step 6.

---

## Q12 — Shadow mode — “Won’t teams just turn you off?”

**Answer:** Shadow is the default deployment — dual-emit gated-vs-ungated counterfactuals and earn enforcement per route so we do not over-block text and get disabled like a perimeter guardrail.

**Live proof:**

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=shadow' \
  | python3 -c "import sys,json; o=json.load(sys.stdin)['response_overlay']; print('shadow=', o.get('shadow'), 'action_allowed=', o.get('action_allowed'))"
# shadow=true → action_allowed stays true while would-hold counters still record
curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
```

**Pointer:** [QA.md](QA.md) C3, C5 · [ARCHITECTURE.md](ARCHITECTURE.md) §5.9.

---

## Q13 — “What about a purely parametric answer with nothing to bind to?”

**Answer:** Binding is undefined without an evidence set — ungrounded-by-construction still cannot authorise an R3 action; we do not pretend the graph verifies what was never given.

**Live proof:** Conceptual — no “fake span” demo; say the winning line out loud while refund shows absence ≠ parametric invention.

> “We don’t claim to verify what we were never given. We claim that what we were never given cannot authorise an action.”

**Pointer:** [QA.md](QA.md) B1 (drill cold) · [ARCHITECTURE.md](ARCHITECTURE.md) §3 Detection §3 / ungrounded routes.

---

## Q14 — “Prompt injection — can the model forge a binding?”

**Answer:** The model has no channel to declare a binding — we compute bindings over spans captured at context assembly; injection can change prose, not which spans/ACLs/hashes were recorded.

**Live proof:** Entitlement flip again (identity outside the prompt) + audit hash chain:

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01' | python3 -m json.tool | head -40
```

**Pointer:** [QA.md](QA.md) B5 · [ARCHITECTURE.md](ARCHITECTURE.md) §8 (model-emitted citations rejected).

---

## Top-5 drill order (morning of)

1. Q1 guardrail · 2. Q9 dual-action · 3. Q10 blocked trap · 4. Q8 entitlement flip · 5. Q4 latency (bench file open)

If pressed for depth: Q2 LLM judge → Q7 fail closed → Q12 shadow → Q5 FNR honesty.
