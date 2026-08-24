# ControlPlane.ai — Pitch Architecture (Stage 5)
**Accenture Innovation Challenge 2026 · Round 2 · Pitch Presentation Design**
Sources: `ARCHITECTURE.md` · `NARRATIVE.md` · `QA.md` · `R2S1.md` · `R2S2.md` · `R2S3.md` · `R2S4.md` — all eternally frozen

---

## 1. Pitch Thesis

**An AI response is not text to be scored — it is a set of claims requesting permission to act.** ControlPlane is the admission-control layer that captures provenance outside the model, inverts the burden of proof (default = UNSUPPORTED), carries caller identity into verification as deterministic set-membership, and hard-gates actions on the exact frozen R×S matrix — so the identical unsupported claim annotates a draft and holds a ₹1,84,000 refund. The plane publishes its own per-route false-negative rate. Nothing acts until it can prove it should.

---

## 2. Overall Pitch Structure (10 minutes)

| Beat | Duration | Content | Purpose |
|---|---|---|---|
| **Opening** | 0:00–1:15 | Held transaction indictment + thesis | Frame as authorisation, not safety; land the category change |
| **Mechanism Walk (The Graph)** | 1:15–3:00 | STEP→SPAN→CLAIM→ACTION live on one screen | Prove one graph, three reads; provenance outside model; default UNSUPPORTED |
| **Dual-Action Demo (Centrepiece)** | 3:00–6:00 | Refund R1 Edit + R3 Escalate held + evidence packet | Emotional & intellectual centre — proof scales with consequence |
| **Principal-Flip** | 6:00–7:00 | Same span, same claim, different caller → entitlement flips | Entitlement = set-membership, not text classification; zero LLM |
| **Business Case Integration** | 7:00–8:15 | Levers A–G, buyer split, phased earn-out roadmap | Value without consulting deck; mechanism→consequence logic |
| **Differentiation & Defence** | 8:15–9:15 | vs observability, vs LLM-as-judge, vs groundedness + refuse-to-claim | Named products; publish misses not catches; credibility closer |
| **Closing** | 9:15–10:00 | Resolve opening indictment | "Now nothing acts until it can prove it should" |

Total: **10 minutes** — tight, no fluff, dual-action remains the centre.

---

## 3. Opening Beat (0:00–1:15)

**Exact approach:** Open on the held transaction. Never on "AI risk." Never on a person.

**First visual (cold, ≤3 seconds):**
```
Action Gate Panel
──────────────────
Action:    refund.execute
Args:      { amount: 184000, reason: "clause 7.2", order_id: "ORD-1023" }
Blast R:   R3 — irreversible payment
Status:    HELD — ESCALATE
Executed:  false
```

**Opening lines (verbatim from frozen narrative):**

> "Everyone watches the exit. Nobody records the entrance.
>
> That system — the one that just moved ₹1,84,000 on a clause that does not exist — was never asked to prove anything.
>
> An AI response is not text to be scored. It is a set of claims requesting permission to act.
>
> ControlPlane is the admission-control layer that records the entrance, binds every claim to the evidence the model was actually given, and refuses to let an unproven claim cross into an action. Because the cost of a wrong output changed category: it used to be a bad paragraph. It is now an executed transaction."

**Timing discipline:** 75 seconds max. No context setting. No "AI is powerful but." The held R3 gate *is* the hook.

---

## 4. Prototype Demonstration Spine (3:00–7:00)

**Governing rule:** Build backward from the action gate. The dual-action crisis is the primary success path (R2S1 §5 criteria 6, 7, 4, 15, 19). Everything serves it.

### 4.1 Dual-Action Crisis (3:00–5:15) — ≤135 seconds

| Step | Visual | Spoken anchor |
|---|---|---|
| 1 | Evidence Ledger expands (≥60% screen). Spans with `source·ACL·hash·offsets` already present **before** claims. | "Provenance captured outside the model — at context assembly. The model has no write path to this." |
| 2 | Three claims born **UNSUPPORTED**: C1 (numeric), C2 (clause 7.2), C3 (internal note). | "Every claim starts UNSUPPORTED. Not low confidence — unproven. It must earn SUPPORTED." |
| 3 | C1 binds to `ORD-1023` → SUPPORTED. C2 finds **zero spans** → stays UNSUPPORTED (absence, not contradiction). C3 binds to `FIN-INTERNAL-NOTE` but ACL excludes `agent_refund_7` → entitlement violation. | "Clause 7.2 does not exist. Absence of evidence, not conflict. That puts it in the Unsupported+categorical column — which is why the actuator is Escalate, not Block." |
| 4 | Matrix highlighted **before** actuators fire: `text.show` (R1) → Edit; `refund.execute` (R3) → Escalate. | "Same response. Two pending actions. Different blast radii. Proof scales with consequence — worst claim weighted by role in *that* action, never an average." |
| 5 | Surgical Edit strips C3 from customer text. Edited text re-enters gate. Refund stays HELD. | "Edit is surgical — strip the failing claim, or one constrained regeneration naming the exact failing span. No free-form rewrite. The refund never commits." |
| 6 | Evidence packet opens: claim, candidate spans `[]`, verdict UNSUPPORTED, diff, proposed Escalate, action `refund.execute`. | "Escalate ships an evidence packet — not a bare alert. Claim, candidate spans, verdict, diff. The reviewer sees exactly why." |
| 7 | Executor log: `refund.execute → committed:false`. Empty FNR schema visible (null placeholders only). | "The company does not wrongly pay out. The gate held. And this — the FNR schema — is empty by design. We publish what we missed. Emptiness is the credibility play." |

**Hard constraints:**
- Never say "blocked" about the refund. Say **held and escalated with the evidence packet**.
- Matrix cells highlighted **before** actuators.
- Ledger ≥60% screen throughout.
- Binding/entitlement/interlock compute visible (~20–80ms) — not pre-baked animation.
- First failure sentence uses **"claim,"** not "response."

### 4.2 Principal-Flip (6:00–7:00) — ≤60 seconds

| Step | Visual | Spoken anchor |
|---|---|---|
| 1 | Knowledge route. Principal `analyst_01` queries L6 compensation. Claim binds to `HR-COMP-L6`. ACL excludes caller. | "Same span, same claim. Caller is not entitled. R1 × entitlement → Edit." |
| 2 | Switch principal to `hr_partner_01`. Same ledger, same claim, same span. Entitlement passes (set-membership). Outcome flips. | "Only the caller changed. Authorization is a set-membership test — `span.acl ⊆ principal.clearance`. Zero LLM in this path. This is the single most differentiated mechanism — no output-only competitor can replicate it because none carry identity into verification." |

---

## 5. Business Case Integration (7:00–8:15)

**Rule:** No consulting deck. Value levers as mechanism→consequence, not ROI slides. Buyer logic from R2S4 §3–§5.

| Segment | Content | Delivery |
|---|---|---|
| **Buyer split** | Economic buyer (pays when it fails) ≠ Technical buyer (integrates) ≠ Actor (types answer) ≠ Operator (runs plane) ≠ Escalation reviewer. The person who pays is not the person who runs it. | One slide, 4 rows. "We sell to the one who pays when it fails." |
| **Lever A (Avoided wrong actions)** | `refund.execute` cannot commit while R3×unsupported-categorical→Escalate. Structural escape, not statistical. Value = held true-positives × buyer's average direct cost. | "Each held refund is a class of cost observability cannot touch — wrong payout, deletion, publication, regulated advice delivered then retracted." |
| **Lever B (Blast-radius pricing)** | Lane 1 always-on (deterministic); Lane 2 bounded; Lane 3 async. R0/R1 majority volume gets cheap checks; R3 gets expensive pipeline. Same verdict annotates draft and holds payment. | "Verification cost concentrated where consequence is high. The one-size-fits-all latency problem — solved by geometry, not compromise." |
| **Lever C (Exact dead compute)** | Walk graph backward: steps grounding zero accepted claims = waste. Exact, no model. "₹5 of ₹8 grounded nothing." No competitor has this number. | "Observability measures spend. ControlPlane measures waste. Same graph that verifies also accounts." |
| **Lever F (Trustworthiness = publishing misses)** | Per-route FNR as typed format; stratified shadow audit; ground truth = human/expensive multi-verifier — never LLM-as-judge. Status vocabulary: `prototype_corpus` / `production_measured`. | "Buyer conversation changes from 'trust our safety score' to 'here is the route, the evaluation population, what we missed, and the uncertainty around that measurement.'" |
| **Roadmap (Earn-out)** | Phase 0 (prototype) → Phase 1 Shadow (1–2 real routes, dual-emit, "would have held N, M true positives") → Phase 2 Canary R0/R1 → Phase 3 R2/R3 earned enforcement → Phase 4 broader envelope. Day one = shadow. Enforcement earned, not switched on. | "No global enable-from-a-slide. At every phase, publication of misses is mandatory. Emptiness is the credibility play." |

**No fabricated percentages. No "99% accuracy." No net-savings slide.**

---

## 6. Differentiation & Defence Moments

Placed where a serious engineer or Accenture evaluator expects them — after they've seen the mechanism work.

| Moment | Contrast | Line (from frozen narrative) |
|---|---|---|
| **vs Observability** (post-demo) | LangSmith/Helicone/Arize/WhyLabs = post-hoc traces after harm lands. Measures spend (₹8), not waste (₹5 grounded nothing). | "Observation without execution control is an audit trail, not architecture. Same graph that verifies also accounts." |
| **vs LLM-as-Judge** (post-matrix) | NeMo Guardrails = "does this look right?" — unfalsifiable, identity-blind, same-family blind spots, too slow, cannot state own error rate. | "The judge asks 'does this look right?' — an unfalsifiable question. We ask 'which span proves it?' — a query with an answer." |
| **vs Groundedness Checkers** (post-principal-flip) | RAG groundedness = retrieval-only, averages (one wrong figure drowns), action-blind (0.82 same on draft and wire transfer). | "Retrieval is not permission. We bind against the full provenance set, price the worst claim per pending action, apply exact R×S so identical unsupported claim annotates draft and holds payment. Proof scales with consequence." |
| **Refuse-to-Claim** (closing differentiation) | Every deck disclaims rivals; almost none disclaim themselves. | "We do not claim to eliminate hallucinations. We do not claim zero integration. We do not claim zero latency. We do not claim one accuracy number across three failure modes. We claim: ungrounded claims cannot authorise actions, and we report what we miss." |
| **Credibility Closer** | Competitors publish precision (how often they bother the user). | "They publish precision — the rate at which they bother the user. We publish the rate at which we missed. The plane is audited by the standard it enforces." |

---

## 7. Closing Beat (9:15–10:00)

**Exact resolution of the opening:**

> "That system was never asked to prove anything.
>
> [hold — 2 seconds]
>
> Now nothing acts until it can prove it should."

**Final visual:** Evidence Ledger with the held refund action, the Edit on text, the evidence packet, the empty FNR schema — all on one graph. No logos. No "thank you." The architecture is the closer.

---

## 8. Anti-Patterns (Hard Kill List)

| Anti-pattern | Why it kills | Frozen source |
|---|---|---|
| Opening on "AI risk" / "AI is powerful but" | Pattern-matches every guardrail deck; frame set before thesis | NARRATIVE §6 |
| Saying "blocked" about the refund | R3×unsupported-categorical = Escalate. Matrix cell is load-bearing. | ARCHITECTURE §10 Law 2, NARRATIVE §8 Trap 2 |
| Collapsing dual-action into one "response blocked" | Destroys "proof scales with consequence" — the centrepiece | R2S1 §3, R2S3 §5 |
| Leading with enablement / "safe AI" / "responsible AI" | Sells virtue, not infrastructure. Category error. | NARRATIVE §6 Correction 4 |
| Showing composite risk/confidence/trust score | "You cannot block, edit or escalate on 87." | ARCHITECTURE §8, NARRATIVE §3 |
| Calling entitlement a "classifier" or "privacy check" | Entitlement = deterministic set-membership, zero LLM. Different mathematics. | ARCHITECTURE §3.1, R2S2 §2 |
| Fabricating FNR numbers in demo | Empty schema *is* the credibility play. | R2S1 §3.11, R2S2 §5, R2S3 §3.41 |
| Showing bias as live per-response verdict | Bias = async route-level counterfactual flip-rate + CI. Never a matrix cell. | R2S1 §2, R2S2 §4, R2S4 §2 |
| Quoting 40ms as p95 | Architecture: ≤40ms p50 / ≤200ms p95. Five-fold overclaim. | ARCHITECTURE §5, QA §C1 |
| LLM-as-judge on critical path | Rejected category. Destroys provenance/entitlement differentiation. | ARCHITECTURE §8, R2S1 §3 |
| Post-hoc recall / speculative release | Liability gap by construction. Hold-back closes it. | ARCHITECTURE §5.2 |
| Demo without live binding compute visible | Hostile judge dismisses as recording. | R2S1 §3.17, R2S3 §5 |
| Chatbot-majority UI | Ledger must be ≥60%. If removing graph leaves demo same → fail. | R2S1 §3, R2S3 §6 |
| "Monitor" / "detect" / "observe" / "watch" / "guard" / "trust score" / "risk score" / "responsible AI" | Vocabulary ban. Authorise / admit / prove / bind / refuse / hold / escalate / gate. | NARRATIVE §6.2, QA §Team alignment |

---

## 9. Fidelity Self-Check

| Frozen Invariant | Pitch Protection |
|---|---|
| **Default = UNSUPPORTED** | Opening thesis, mechanism walk, demo claims born UNSUPPORTED, C2 stays UNSUPPORTED |
| **Entitlement / ACL = deterministic set-membership, zero LLM** | Principal-flip beat; spoken "zero LLM in this path"; ACL check shown as clearance ⊆ membership |
| **Exact R×S matrix (4×4, 16 cells, transcribed never redrawn)** | Matrix highlighted before actuators for both R1 and R3; all 16 cells visible; no invented tiers/actuators |
| **Hard gate on actions, not tokens** | Text hold-back ~150–300ms; refund executor `committed:false`; speculative verification permitted, speculative release forbidden |
| **Two-pending-actions resolution (R1 Edit + R3 Escalate simultaneously)** | Centrepiece of demo; worst-claim weighting per action; never one response-level verdict |
| **Published FNR as empty typed schema (format, not numbers)** | Visible in demo as null placeholders; business case: "emptiness is the credibility play"; status vocabulary includes `prototype_corpus` / `production_measured` |
| **`UNKNOWN` never → `SUPPORTED`** | Mechanism walk: derived/timeout paths return UNKNOWN → matrix routes; never silent allow |
| **No LLM-as-judge on critical path** | Action Interlock = pure rule engine; NLI is binder not judge; FNR ground truth never LLM-as-judge |
| **Bias = async route-level only, never live verdict** | Not in demo; business case states measurement terms; "never claim → bias verdict → matrix" |
| **Refuse-to-claim list (about us)** | Explicit slide: eliminate hallucinations / zero integration / zero latency / one accuracy number — all refused |
| **Content laws** | Clause 7.2 does not exist (absence ≠ contradiction); company wrongly pays out; customer did not lose money; latency ≤40ms p50 / ≤200ms p95 |
| **Prototype boundary (exactly two live routes)** | Demo shows only refund + knowledge; decision-support acknowledged as enterprise/proposal template only |
| **One graph, three reads** | Opening: "Performance reads it forward. Cost reads it backward. Responsibility reads its labels." Ledger = single structure |
| **Vocabulary discipline** | Every spoken line uses: authorise, admit, prove, bind, refuse, hold, escalate, gate. Zero banned terms. |
| **Integration cost = moat (stated out loud)** | Business case: "The integration cost is the moat — say it out loud." One SDK hook + reverse proxy. |

**All invariants protected. No Stage 1–4 decision reopened. Pitch architecture is frozen.**