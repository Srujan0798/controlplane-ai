# ControlPlane.ai — Architecture

OK, here's the design. I've centered it on one bet: **the differentiator is not what you detect, it's the unit of gating**. Everyone will show you 3 detectors. Nobody will explain why their gating primitive beats LLM-as-judge at production latency. This does.

---

## 1. Core Thesis

**AI responses are unverified claims, and a real control plane gates on evidence coverage, not on a risk score from a judge LLM.** The "control" comes from making evidence a first-class runtime constraint — same status as latency or memory — and using an evidence-gated, latency-aware policy DAG to decide block / edit / escalate / pass per axis. One composite risk score is the failure mode of every demo in this category; we reject it.

---

## 2. Detection Layer — one mechanism per axis

### Performance (confidently wrong)
- **Signals observed:** (a) Evidence Coverage Score (ECS) — fraction of atomic claims in the response that have an attached verifiable source, computed by decomposing the response into claim spans and matching each span to retrieval index / tool outputs / cached references; (b) Claim-Proof Alignment — embedding similarity + NLI entailment between each claim span and its cited proof; (c) Calibration gap — model verbal confidence vs. evidence density.
- **Computed:** Confidently-wrong = high verbal confidence ∧ low ECS ∧ low claim-proof alignment. This is the exact pattern that LLM-as-judge misses because the judge is also a language model with the same blind spots.
- **FP control:** 7-day shadow mode dual-emits gated vs ungated; threshold auto-calibrates to keep false-positive block rate ≤5%. The gating decision is compared against human review on a sampled subset, not against another LLM.

### Cost (waste / rework)
- **Signals observed:** (a) Marginal Cost per Useful Token (MCUT) — tokens that produced a verifiable claim vs. total tokens emitted; (b) Rework Ratio — fraction of user turns within a session that re-ask the same intent within 3 turns; (c) Tool-call redundancy — duplicate retrievals, repeated web calls, retry loops.
- **Computed:** Rolling z-score over a 1-hour baseline. Alert fires when MCUT > 2σ or rework ratio > 1.5σ.
- **FP control:** Anomaly-based, not absolute thresholds. Cost signals never block — they only escalate to ops and downgrade the model in the routing layer. (If cost blocks, the user disables you within a week.)

### Responsibility (bias / safety / leakage)
- **Three sub-detectors, each deliberately small and deterministic where possible:**
  1. **PII / PHI leakage** — regex + DeBERTa-v3-base NER on the token stream, ~8ms. Hard block on exact match.
  2. **Harmful content** — distilled classifier (≤1B params), not the LLM itself. Catches the obvious 80% (CSAM keywords, jailbreak-amplified outputs, raw credentials). Soft-edit on score > threshold.
  3. **Demographic bias** — only fires on outputs that touch people/groups. Parity check against base rates from the source dataset. Async flag — never block on the first turn.
- **FP control:** Tiered response per sub-detector. Hard block is reserved for the deterministic tier only.

---

## 3. Decision Policy Engine

- **Policy = DAG of rules**, not nested if-else. Each rule is a 4-tuple: `(signal, threshold, action, latency_budget)`.
- **Actions:** `Block` (suppress), `Edit` (rewrite via constrained smaller model), `Escalate` (queue human, release response now), `Pass`.
- **Evidence-gated:** a rule only fires if its required evidence is present. If evidence is missing or stale, the rule degrades to "flag for later" — it does not guess. This is the hostile-validation discipline applied to the policy itself.
- **Latency-aware:** each rule declares a budget (e.g., 30ms, 200ms, 2s). If the running check would exceed budget, the rule auto-downgrades: `Block` → `Escalate` → `Flag`. The policy prefers false negatives over latency violations, because latency violations get the layer disabled.
- **Policy is itself versioned, canary-deployed, and auto-rolls back** if human-override rate spikes > 3× the previous baseline. The control plane watches itself.

---

## 4. Latency & Non-Blocking Design

- **Sidecar pattern** — the control plane is a separate process; the model does not await it.
- **Speculative release:** emit the response to the user as soon as Tier-1 checks pass. Deeper checks continue in the background and may trigger Edit-in-place or post-hoc recall. The user sees the model, not the gate.
- **Tier-1 sync (≤50ms, hard ceiling):** regex PII, exact-match safety, token budget cap, policy lookup.
- **Tier-2 async (≤2s post-emit):** evidence coverage, claim-proof alignment, MCUT.
- **Tier-3 offline (≤60s):** bias parity, cross-session consistency, cost analytics, shadow-mode eval.
- **Streaming gate:** only the first 50 tokens are gated synchronously; the rest release while Tier-2 runs.
- **Shadow mode:** 5% of traffic dual-emits gated + ungated. The delta between them measures the layer's actual catch-rate against its real friction cost. Run continuously; you never trust your own metrics on the same path you're gating.
- **Empirical ceiling to defend on the slide:** ≤50ms p50 added, ≤200ms p95 added. Everything above that budget gets re-classified as Tier-2.

---

## 5. Internal Multi-Agent Structure

Five roles. Pipeline, not debate. Each emits a **typed evidence packet**, not free text.

| Agent | Owns | Latency class |
|---|---|---|
| **Director (Policy Resolver)** | Decision DAG; chooses action per rule firing | Sync, Tier-1 |
| **Evidence Builder** | Decomposes response into claim spans, attaches proof from retrieval / tool cache / KG | Async, Tier-2 |
| **Performance Watcher** | Emits ECS, claim-proof alignment, calibration gap | Async, Tier-2 |
| **Cost Watcher** | Emits MCUT, rework ratio, tool-call redundancy | Async, Tier-3 |
| **Responsibility Watcher** | Emits three sub-scores (PII / harm / bias) with tier-appropriate action | Mixed (PII sync, harm sync, bias async) |

- **Coordination under time pressure:** when Tier-2 evidence is not yet available, downstream agents short-circuit to "insufficient evidence → flag" rather than hallucinating a verdict. This is the evidence-gated discipline again.
- **Halt-and-continue:** fast agents can issue a `Block` mid-stream; slow agents can only append to the response's audit trail or trigger a post-hoc `Edit`. The asymmetry is intentional — slow checks should never invalidate a fast decision.

---

## 6. What this deliberately does NOT do

- ❌ **LLM-as-judge.** Circular (same blind spots as the model), slow (300ms–2s), expensive. It also disagrees with humans on the hard cases, which is the only case that matters.
- ❌ **One big safety model at the end.** Single point of failure, single point of latency.
- ❌ **A single composite risk score.** Collapses a 3-axis tradeoff into one number. The user can't act on it, and the policy can't decompose it. The whole point of a *control plane* is per-axis control.
- ❌ **Static blocklists / regex-only safety.** Brittle, always one prompt-injection behind.
- ❌ **Training a new model.** We are a layer *on top*, not a new model. The value is in the policy and the evidence primitive, not in another 7B.
- ❌ **Blocking every flagged response.** Trains users to disable the layer. Block is reserved for deterministic evidence (PII match, ECS=0, policy violation). Soft flags are the default.
- ❌ **Debate / multi-agent voting on safety.** Debate is great for reasoning, terrible for real-time gating. Discussion agents run in Tier-3, never Tier-1.

---

## 7. Single strongest technical risk + mitigation

**Risk:** the control plane becomes a single point of latency failure, making the AI feel slower than it is — and product teams disable it within a quarter, regardless of how well it catches things.

**Mitigation (3-slide-defensible):**
1. **Tiered gating** — only cheap deterministic checks (regex, exact match, cached policy lookup) sit on the critical path. Empirical ceiling: ≤50ms p50, ≤200ms p95.
2. **Speculative release** — the user sees the model, not the gate. The gate runs in shadow, then in async, then in post-hoc edit. The model is never slowed down to gate itself.
3. **Shadow-mode self-measurement** — 5% dual-emit continuously measures the layer's real catch-rate against its real friction cost. The control plane instruments itself; we never trust the layer's own telemetry on the same code path it's gating.

This is the only bet on the slide that, if it fails, kills the whole concept. Everything else (ECS, MCUT, parity check) is a feature. The tiered release is the product.

---

## Recommended 3-slide layout

- **Slide 1 — Thesis + 3 axes.** The claim-vs-proof framing on top; one small icon per axis (Evidence Coverage, Marginal Cost per Useful Token, PII/Harm/Bias tier). Lead with the thesis, not the diagram.
- **Slide 2 — The control flow.** Input → claim decomposition → evidence builder → policy DAG → action. Annotate each arrow with its latency tier (50ms / 2s / 60s). The slide should make a non-technical viewer feel the speed decision.
- **Slide 3 — What we don't do + the latency bet.** Left half: the rejection list (this is what differentiates you from every other team). Right half: the tiered-release diagram with the ≤50ms p50 / ≤200ms p95 number. End on the self-measurement (shadow mode) — it's the line that says "production-grade" without saying it.

---

If you want, I can stress-test this against a team of three adversarial reviewers (one playing devil's advocate on the evidence primitive, one on the latency math, one on the FP rate at production traffic) before you commit it to slides. That would take ~10 min and is the cheapest insurance you can buy before Round 2. Say the word.