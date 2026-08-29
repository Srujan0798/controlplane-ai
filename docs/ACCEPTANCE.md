# Acceptance Matrix — ControlPlane.ai Round 2

Accenture Innovation Challenge 2026 · Team ControlPlane · PS #1
`docs/ACCEPTANCE.md` — copy-pasteable commands + expected outputs + current SHA.
Confidence is mechanical; do not write claims you cannot reproduce.

---

## Current SHA (refresh before each judge session)

```
git rev-parse HEAD
# 5960561bd223abed013e4a7c6ba5122fe05dd443   ← refresh after each verify; tag v0.2.0-round2 @ 551de81
```

If the SHA changes, re-run `make test` and re-record the verdict rows below. Do not present
a commit you have not checked green.

---

## 1. Environment check

| Check | Command | Expected |
|-------|---------|----------|
| Python ≥ 3.11 | `python3 --version` | `Python 3.11.x` or higher |
| FastAPI / uvicorn | `uvicorn --version` | installed |
| Package installed | `pip show controlplane 2>/dev/null | head -5` | `Name: controlplane` present |
| Healthy | `curl -s http://127.0.0.1:8787/healthz` | `{"ok": true, ...}` |

Port swap: Docker Compose → `http://localhost:8080` · Local uvicorn → `http://127.0.0.1:8787`.

---

## 2. Deterministic tests (run before every room)

```bash
make test
```

Expected: **135 passed**, 2 skipped. No failures, no `blocked` in refund language.
If anything red → fix, do not present.

**Proves:**
- Matrix fidelity (frozen R×S, no route param)
- Entitlement = set-membership, zero LLM
- Default UNSUPPORTED; UNKNOWN never → SUPPORTED
- Dual-action centrepiece: R1 Edit + R3 Escalate **held** (never "blocked")
- Refund language fidelity (held/escalated, clause 7.2 does not exist)
- Fail-closed bijection (R3 unsupported → escalate)
- Security negatives: model cannot self-declare binding; injection cannot author provenance
- Principal flip: outcome flips with clearance only

```bash
python3 -c "import json; d=json.load(open('submission/latency_bench.json')); print(d['gate_latency_ms'])"
```

Expected: gate p50≈0.073 ms · p95≈0.09 ms (from `submission/latency_bench.json`; never quote 40ms as p95).

---

## 3. Refund demo — cold open + dual action + held

### CLI fixture

```bash
python3 examples/refund_trace_demo.py
```

Expected: dual-action — `text.show` → **Edit** (R1, C3 entitlement); `refund.execute` → **Escalate**
(R3, C2 no span, clause 7.2 does not exist). Refund **held**, `committed: false`, evidence packet
for C2: claim, candidate spans `[]`, verdict `UNSUPPORTED`, diff.

### Live curl (enforce)

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' | python3 -m json.tool
```

Expected:
- `response_overlay.show_text` → Edit
- `response_overlay.issue_refund` → Escalate, `committed: false`
- driving claim C2 stays red for missing clause
- clause 7.2 **does not exist** → UNSUPPORTED, never caps/denies

### Live curl (shadow)

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=shadow' | python3 -m json.tool
```

Expected: shadow envelope only — would-hold counterfactual; no real commit.

---

## 4. Principal flip — entitlement is identity

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01'   | python3 -m json.tool
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=hr_partner_01' | python3 -m json.tool
```

Expected:
- `analyst_01` → Edit (ACL excludes caller)
- `hr_partner_01` → Pass (ACL includes caller)
- **Same span. Same claim. Same graph. Only the caller changed. Zero LLM.**

---

## 5. Full OpenAI-compatible shape (judge convenience)

```bash
curl -s http://127.0.0.1:8787/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"controlplane-demo","messages":[{"role":"user","content":"Issue refund under clause 7.2"}],"scenario":"refund","mode":"enforce"}' \
  | python3 -m json.tool
```

Expected: user-visible text surgically edited; irreversible refund **held** (`Escalate`); `controlplane`
extension carries the evidence ledger. Never `COMMIT BLOCKED`.

---

## 6. Matrix — two live routes only

| Route | Dominant R | What it proves | Live? |
|-------|------------|---------------|-------|
| Refund agent | R1 text + R3 refund | Two-pending-actions, hard gate, Edit + held Escalate | YES |
| Knowledge assistant | R0/R1 | Provenance + entitlement flip (graph ≠ RAG groundedness) | YES |
| Decision-support / bias | — | Async counterfactual | NO — envelope only |

Exactly two Stage 1 live routes. A third live decision-support/bias route is refused by design.
Bias = async route-level counterfactual flip-rate + CI; **never** a per-response matrix cell.

---

## 7. Latency — quote measured, never invented

| Statement | Truth |
|-----------|-------|
| Targets | **≤40 ms p50 / ≤200 ms p95** on R0/R1 text |
| Measured gate (n=200, TestClient) | p50 ≈ **0.074 ms** / p95 ≈ **0.134 ms** |
| Never say | "40 ms p95" / "forty millisecond p95" |
| Never claim | "we eliminate hallucinations" / "zero added latency" / "zero integration" |
| Always | Hard gate on actions; speculative verify OK; **speculative release forbidden** |

Cite bench: `submission/latency_bench.json` — refresh with `make bench` if human asks.

---

## 8. FNR — empty typed schema until earned

**Refund enforce returns an evidence packet for every Escalate:**
- claim, candidate spans, verdict, diff — never a bare alert.
- FNR renders typed null placeholders; em **ptiness is the credibility play**.

```bash
curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
```

Refresh shadow counters:
```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/metrics/reset'
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=shadow'
curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
```

---

## 9. Edit+Escalate expectation (the single most important row)

On the refund fixture there are **two pending actions** on one response. They must both surface:

| Pending action | Tier | Worst claim | Matrix cell | Actuator | Outcome |
|----------------|------|-------------|-------------|----------|---------|
| `text.show` | R1 | C3 (entitlement violation) | R1 × entitlement violation | **Edit** | surgical strip only |
| `refund.execute` | R3 | C2 (no span, clause 7.2 absent) | R3 × Unsupported + categorical | **Escalate** | **held** with evidence packet |

**Both are correct simultaneously.** Never collapse into one response-level verdict. Never say "blocked."
The console Clearance bay first viewport shows `HELD — ESCALATE` / `executed: false` — no bare block.

---

## 10. Deterministic + security regression (every commit)

```bash
make test
```

Determinism: five runs → same Edit+Escalate (run `make test` again if you doubt). Every regression
locks the holes:
- refund language: held/escalated with packet, never blocked
- refund executor log: `committed: false`, never `COMMIT BLOCKED`
- principal flip: only the caller changes outcome
- matrix: 16 cells, never redrawn, no route param
- default UNSUPPORTED: earned via bind/recompute only
- UNKNOWN never → SUPPORTED

```bash
python3 examples/multi_usecase_demo.py   # support / copilot / decision-support
```

---

## 11. Human dry-run checklist

- [ ] `git rev-parse HEAD` matches the SHA in this file
- [ ] `make test` → 107 passed, no failures
- [ ] `refund_trace_demo.py` → Edit + Escalate held, packet visible
- [ ] `knowledge_flip_demo.py` → outcome flips with principal
- [ ] Console cold-open shows `HELD — ESCALATE` / `executed: false`
- [ ] Verify **two** live routes only (refund + knowledge)
- [ ] Verify latency quoted as ≤40 ms **p50** / ≤200 ms **p95**, measured bench cited
- [ ] Verify "blocked" does not appear anywhere for the refund
- [ ] Verify "40 ms p95" does not appear
- [ ] Verify "customer lost money" does not appear

---

## 12. Judge console surfaces

| Surface | URL / command | Use |
|---------|-----------|-----|
| Enterprise console | `http://127.0.0.1:8787` (or `:8080` via Docker) | Walk the ledger; see Edit + Escalate held |
| OpenAI-compatible gate | `POST /v1/chat/completions` | Shape a judge can call |
| Refund demo (enforce) | `POST /v1/controlplane/demo/refund?mode=enforce` | Centrepiece |
| Flip demo | `POST /v1/controlplane/demo/flip?principal=...` | Entitlement = identity |
| Shadow / FNR metrics | `GET /v1/controlplane/metrics` | Empty typed FNR schema |
| Policy packs | `GET /v1/controlplane/policies` | RoutePolicy, one-liner config |
| Audit export | `GET /v1/controlplane/requests/{id}/audit.jsonl` | Reconstructible trail |

Port swap: Docker Compose → `http://localhost:8080` · Local uvicorn → `http://127.0.0.1:8787`.

Pre-flight once per room:
```bash
make test          # includes determinism + security negatives
make bench         # optional; refreshes submission/latency_bench.json
```

---

## Source pointers

- Speak-from canon (demo spine + never-say): `round2/R2S5.md`
- Runbook (stand + one-liners + port swap): `docs/JUDGE_RUNBOOK.md`
- Kill-shot framing: `docs/KILL_SHOT.md · docs/SUBMIT.md`
- Hostile Q&A drill: `docs/HOSTILE_QA_DRILL.md`
- Architecture freezes (truth): `docs/ARCHITECTURE.md`
- Acceptance matrix: **this file** (`docs/ACCEPTANCE.md`)
