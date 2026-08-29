# Round 2 — Assumptions Register

Accenture Innovation Challenge 2026 · Team ControlPlane · PS #1
Source of truth for scope parameters: `docs/ps.md` (prototype params) + `round2/CONTROLPLANE_R2_FINAL.md`
(authoritative text). Modification requires re-checking both. No fabricated enterprise data.

---

## Purpose

Every design decision in Round 2 rests on explicit assumptions. Spell them out now so the reader can
judge which ones carry the proposition and what happens if each is wrong. Directional values are labelled
as such; we do not pretend proprietary enterprise data exists.

---

## Register

| # | Assumption | Why we made it | Impact if wrong |
|---|-----------|----------------|-----------------|
| 1 | **Traffic scale is directional "tens of thousands of interactions per week"** across three use cases (customer support, internal knowledge, decision-support), per `docs/ps.md:40-43`. | We do not have a real company's traffic; the brief says adapt freely and use reasonable assumptions. We state a range, not a number. | If the real buyer runs far higher volume, integration/deployment cadence (not the plane) is the gating factor. If far lower, the beachhead shrinks but the mechanism does not. The prototype is a curated single-node trace; no throughput claim. |
| 2 | **Three use cases: customer support (refund), internal knowledge, decision-support**, per `docs/ps.md:40-43`. For Stage 1 we demonstrate exactly two live routes (refund + knowledge) and refuse the third live (decision-support / bias lives in the envelope). | Brief names three routes and asks to design a complete solution; architecture defines bias as asymptotic / async; two live routes are the smallest complete proof of the dual-action centrepiece. | If judges expected all three as live, the pitch explains the refusal is architectural by design (bias = async-only, per frozen invariants), not scope dodge. |
| 3 | **Foundation model is consumed via API only — no weights, logits, or fine-tuning access**, per `docs/ps.md:27` and FINAL §2. | Brief asks to assume API-only consumption in enterprise; architecture is built around that boundary (hooks context assembly, OpenAI-compatible proxy, no model internals). | If a customer has direct model access, the integration surface still holds (proxy + SDK hook), so the plane still applies; the boundary is a convenience assumption, not a hard dependency. |
| 4 | **Corpi are synthetic, enterprise-shaped, no real PII**, per FINAL §4 corpus table + §4 assumptions line. | Prototype must be runnable and demonstrable without proprietary data; no real person's data should appear in a pitch demo. | If a real deployment needs real corpora, the provenance contract (source_id · ACL · hash · offsets) does not change; synthetic vs real is a data ingress decision, not an architecture decision. |
| 5 | **FNR is null until a trustworthy stratified audit exists** — Round 2 shows the *typed schema*, not a fabricated percentage, per FINAL §5 FNR schema + JUDGE_RUNBOOK never-say table. | The only honest answer to "how many do you miss?" on production traffic today is "we publish the shape, values are null until measured." Emptiness is the credibility play. | If a reviewer insists on a number, we point at the schema and the measurement_status field; the schema, not the number, is the deliverable. |
| 6 | **Bias is async, route-level, counterfactual invariance only — never a per-response matrix cell**, per FINAL §5, §10.9, and frozen invariants in FINAL §2. | Brief requires bias treatment; architecture says bias has different mathematics and owners than hallucination/leakage; per-response bias would be a second classifier on the critical path, which we refuse. | If the room expects a live "bias verdict" button, we show the async mechanism is the correct answer by design, not a missing feature. |
| 7 | **Latency targets are ≤40 ms p50 / ≤200 ms p95 on R0/R1 text**, per FINAL §4, JUDGE_RUNBOOK never-say table, `submission/latency_bench.json` (n=200, measured gate p50≈0.073 ms / p95≈0.09 ms). | Targets come from FINAL §4 and the runbook; measured bench is the source of truth. Never quote 40 ms as p95 (5× overclaim). | If a judge assumes we claim "zero added latency," we correct: we make the *action* wait; text hold-back is ~150–300 ms; speculation is verified, not released. |
| 8 | **Integration cost is real and is the moat** — one SDK hook + OpenAI-compatible proxy, measurable in days on a standard retrieval stack, never "zero integration" or "drop-in", per FINAL §2 refuse-to-claim #2 and §5. | Honesty: integration is the exact reason the design works (we hook context assembly, so we get provenance). A "drop-in" pitch would be false. | If a buyer expects zero integration, we reframe: the cost is the moat, and we are explicit about it. The integration cost does not break the proposition; it is the proposition's honesty boundary. |
| 9 | **The single failure model is authorisation, not quality** — a better model or bigger RAG index still produces a fabricated clause ID or answers the wrong caller, per FINAL §1 and Q3 in JUDGE_RUNBOOK. | R2S5 thesis + FINAL §1: "an AI response is a set of claims requesting permission to act"; the failure is absence of proof for an action, not the model's text quality. | If a judge says "just use a bigger model / better prompts / RAG," we answer the architecturally: the failure is authorisation; size is irrelevant; the plane sits between the model and the action. |
| 10 | **Default = UNSUPPORTED and entitlement = set-membership (zero LLM) are frozen invariants**, per FINAL §2 eternal invariants and R2S5 §1. | These are not aspirational; they are the pitch's frozen core. Every demo, every curl, every static surface reflects them. | If they were not frozen, the whole pitch collapses into a guardrail. They are not up for negotiation — re-checking FINAL §2 confirms them. |
| 11 | **R3 action classes are locked at parse time**: payment / deletion / publication / regulated advice, per FINAL §5 RoutePolicy. | Locking locked R3 classes prevents mis-mapping (e.g. a payment treated as R1). The interlock lives in the executor, not only the UI. | If a new irreversible class appears, the policy packs are extended, not the frozen matrix; the matrix itself is never redrawn. |
| 12 | **The pitch is two presenters, one demo machine, one handoff**, per R2S5 §2 (handoff rule: A drives 0:00–7:00, B drives 7:00–9:00, A returns for defence + close). | R2S5 §2 is frozen; the handoff rule exists so the demo has one voice. | If team composition changes day-of, the roles must still follow the handoff rule; never co-present the demo. |

---

## How these were sourced

- `docs/ps.md:40-43` → traffic scale + three use cases.
- `docs/ps.md:27` + FINAL §2 → API-only foundation model.
- FINAL §4 corpus table + §4 assumptions line → synthetic corpora, no real PII.
- FINAL §5 FNR schema + §2 eternal invariants → FNR null, UNSUPPORTED default, set-membership entitlement.
- FINAL §1, §5, §10.9 + JUDGE_RUNBOOK §5 (Q3, Q6) → bias async-only.
- JUDGE_RUNBOOK never-say table + `submission/latency_bench.json` → latency targets.
- FINAL §2 refuse-to-claim #2 + §5 → integration cost = moat.
- R2S5 §1, §2 → thesis, dual-action centrepiece, two presenters, handoff rule.

---

## Live corroboration commands

```bash
git rev-parse HEAD                    # 46a1d749ba5bbd9843768e8f6c209fb6dab17cf4 (last verified)
make test                              # 107 passed — no failures, no "blocked" in refund language
python3 -c "import json; print(json.load(open('submission/latency_bench.json'))['gate_latency_ms'])"
# {'n': 200, 'min': 0.068, 'mean': 0.118, 'p50': 0.073, 'p95': 0.09, 'p99': 0.832, 'max': 4.045}
```

---

## Source pointers

- Prototype params (traffic + use cases + API-only + synthetic + FNR + bias): `docs/ps.md`
- Authoritative text (assumptions line, FNR schema, refuse-to-claim, R3 lock, latency): `round2/CONTROLPLANE_R2_FINAL.md`
- Runbook (latency ethics, FNR honesty, bias stance, principal flip): `docs/JUDGE_RUNBOOK.md`
- Kill-shot (differentiation assumptions): `docs/KILL_SHOT.md`
- Acceptance matrix (corroboration commands): `docs/ACCEPTANCE.md`
