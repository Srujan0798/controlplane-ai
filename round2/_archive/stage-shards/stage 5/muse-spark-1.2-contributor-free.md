# Stage 5: Pitch Architecture — ControlPlane.ai

> Accenture Innovation Challenge 2026 · Round 2 · Stage 5 — Pitch Architecture
> Model: **muse-spark-1.2-contributor-free**
> Sources of truth (eternally frozen): `docs/ARCHITECTURE.md` · `docs/NARRATIVE.md` · `docs/QA.md` · `round 2/_archive/stage-locks/R2S1.md` · `R2S2.md` · `R2S3.md` · `R2S4.md` · `round 2/CONTROLPLANE_R2_FINAL.md` · `docs/ps.md`
> Stage 5 does not reopen any technical, scope, or value decision from Stages 1–4. It is the structural spine of the live/recorded pitch.
> Total target: **10:00** (hard ceiling 11:00). Dense hybrid. Demo is the pitch.

---

### 1. Pitch Thesis (one sharp paragraph)

An AI response is not text to be scored — it is a set of **claims requesting permission to act** (`docs/ARCHITECTURE.md:13`, `docs/NARRATIVE.md:13`). The only record that can prove or refuse that request is the evidence assembled **before the model ran** — `source_id · ACL · hash · offsets` plus calling principal — and the entire industry throws that record away the moment generation starts (`docs/NARRATIVE.md:10`). ControlPlane keeps the receipts and turns verification from an opinion into a **set-membership test** (`CALLER → CLAIM → SPAN → SOURCE ACL`), inverts the burden of proof (`default = UNSUPPORTED`), and prices proof by **blast radius** on one `STEP → SPAN → CLAIM → ACTION` graph. Text may stream; actions do not proceed without proof.

---

### 2. Overall Pitch Structure — 10:00 spine

Tight, not comprehensive. Business case earns its time *after* the mechanism earns respect. No consulting deck.

| Beat | Time | What happens | On screen |
|---|---|---|---|
| **1. Opening — held transaction** | 0:00–1:15 | Category change, not AI risk. Cold open on gate. | Action Gate: `refund.execute HELD — ESCALATE executed:false` |
| **2. Thesis + reframe** | 1:15–2:15 | Admission control, not text scoring. One graph. | `STEP → SPAN → CLAIM → ACTION` single line |
| **3. Architecture primer (30s)** | 2:15–3:00 | Default UNSUPPORTED, claim-type routing, set-membership entitlement | Ledger skeleton with 3 claims born red |
| **4. Prototype centrepiece — DUAL-ACTION** | 3:00–6:30 | **Emotional + intellectual centre. ~35% of pitch.** Backward from gate. Both actuators live. | Ledger ≥60% + Matrix + Packet + Executor |
| **5. Principal-flip** | 6:30–7:30 | Same claim, different principal → different outcome. Zero LLM in path. | Same graph, `analyst_01 → Edit` → `hr_partner_01 → Pass` |
| **6. Business case integration** | 7:30–9:00 | Value levers + buyer logic + earn-out roadmap as earned consequences | Exposure = freq × P(unproven) × loss; per-route FNR format (empty) |
| **7. Differentiation & refusal** | 9:00–9:30 | Three contrasts + publish-misses closer. No score. | Vs table: provenance / UNSUPPORTED / entitlement / one graph / matrix / FNR |
| **8. Closing — resolution** | 9:30–10:00 | Opening negated and resolved. Hold. | First and last line pair on black |

**Rule:** If Beat 4 is cut or collapsed, the pitch has failed regardless of polish elsewhere.

---

### 3. Opening Beat (first 60–90 seconds) — held transaction, never risk

**Exact approach:** No title slide. No "AI is powerful but risky." No person. No confidence number. Projector already shows the Action Gate frozen on failure.

**Visual cold open (0:00):**
```
Action: refund.execute
Args: { amount: 184000, reason: "clause 7.2", order_id: "ORD-1023" }
R: R3 — irreversible payment
Status: HELD — ESCALATE
Executed: false
```

**Preferred opening lines — drawn verbatim from frozen narrative (`docs/NARRATIVE.md:202-231`):**

> "**This refund never moved.**"
> "**Clause 7.2 does not exist.** Money moved Tuesday, found Friday. If ungated, the company wrongly pays out ₹1,84,000 — the customer didn't lose money."
> "It used to be a bad paragraph. It is now an executed transaction. (`docs/NARRATIVE.md:204`)"
> "**The system didn't fail. It was never asked to prove anything.** (`docs/NARRATIVE.md:208`)"
> "[beat] **Everyone watches the exit. Nobody records the entrance.** (`docs/NARRATIVE.md:211`) — we do. And we gate the exit."

First sentence about the failure contains the word **"claim"**, not "response" (`docs/NARRATIVE.md:174`). The rupee figure lands in the first 15 seconds. Danger is implied by money, not asserted as generic risk.

---

### 4. Prototype Demonstration Spine — how dual-action lives inside the pitch

**Governing orders from `R2S1.md:185` + `R2S3.md:198`: build backward from the action gate. Ledger majority (≥60%). Live compute, not animation. Core crisis ≤90s inside a ≤8 min session.**

**Sequence (3:00–6:30) — must run live:**

1. **Gate already live (3:00).** As opened. State the invariant: `refund.execute` is **held and escalated with the evidence packet** — never "blocked" (`docs/ARCHITECTURE.md:349`, `R2S1.md:49`). `committed:false` visible.
2. **Expand the ledger (3:20).** Same screen reveals `STEP → SPAN → CLAIM → ACTION`. Spans appear **before** claim verdicts with `source · ACL · hash · offsets` (`R2S1.md:88`). Show:
   - `AGR-VENDOR-v3` (agent-readable, clauses 1–6 only, **no 7.2 anywhere**)
   - `ORD-1023` (amount 184000)
   - `FIN-INTERNAL-NOTE` (ACL `internal_analyst` — excludes `agent_refund_7`)
   Provenance outside model (`docs/ARCHITECTURE.md:46`): model has no write path.
3. **Claims born UNSUPPORTED (3:45).** All three start red. Unsupported = **not low confidence — unproven** (`docs/NARRATIVE.md:217`):
   - **C1** — numeric amount/order → binds `ORD-1023` → **SUPPORTED** (deterministic recomputation)
   - **C2** — categorical "under clause 7.2…" → **zero candidate spans** → stays **UNSUPPORTED** (absence ≠ contradiction; never "caps/denies/doesn't cover" — `docs/ARCHITECTURE.md:346`)
   - **C3** — sentence grounded on `FIN-INTERNAL-NOTE` → **entitlement violation** for `agent_refund_7`
   Live binding/entitlement/interlock shows real latency ~20–80ms (`R2S3.md:39`).
4. **Matrix before actuator (4:15).** Exact frozen 16-cell `R×S` transcribed, never redrawn (`docs/ARCHITECTURE.md:144`, `R2S1.md:104`). Highlight **before** firing:
   - `text.show` (worst = C3) → **R1 × Contradicted/entitlement violation → Edit**
   - `refund.execute` (worst = C2) → **R3 × Unsupported + categorical → Escalate** — held
   Worst-claim-per-pending-action, never an average (`docs/ARCHITECTURE.md:78`, `R2S1.md:42`). Same graph, two actuators simultaneous — proof scales with consequence.
5. **Surgical Edit (4:50).** Strip only C3 or one constrained regen naming failing span; re-gate; refund stays held. No free-form rewrite (`docs/ARCHITECTURE.md:163`).
6. **Evidence packet (5:15).** For C2: claim + candidate spans `[]` + verdict UNSUPPORTED + diff + matrix cell + proposed actuator. For C3: same + ACL result (`R2S1.md:122`). Not a bare alert.
7. **Executor proof (5:40).** Log: `refund.execute → not committed (executed:false)`. Company does **not** wrongly pay out in gated demo. Hard gate on **actions, not tokens**; text hold-back ~150–300ms visible (`docs/ARCHITECTURE.md:202-204`, `R2S3.md:38-39`). Speculative verification permitted; speculative release forbidden.
8. **Empty FNR schema (6:00).** Typed per-route fields visible with **null / empty placeholders only** (`R2S2.md:364`): `route_id · policy_version · window · strata · sampled_count · false_negative_count · FNR_estimate · CI · ground_truth_method · measurement_status · limitations`. Emptiness is the credibility play (`docs/ARCHITECTURE.md:359`). No invented percentage. No `prototype_corpus` fill in live demo.
9. **Text / action separation close (6:20):** customer text remains subject to its own R1 result while R3 stays held — never one collapsed "response blocked."

**Secondary beat — principal-flip (6:30–7:30) — required (`R2S1.md:128`, `R2S3.md:223`):**

Knowledge route. Claim binds `HR-COMP-L6`. `analyst_01` (non-HR) → **R1 × entitlement → Edit**. Change **only** principal → `hr_partner_01` → Pass. Same span, same claim, same graph. Entitlement is `span.acl ⊆ principal.clearance` — set-membership, Lane 1, **zero LLM** (`docs/ARCHITECTURE.md:117`, `R2S2.md:112`). This second beat proves the graph is not RAG groundedness: semantically correct can still be unauthorized.

---

### 5. Business Case Integration — without becoming a consulting deck

Placed **after** the mechanism is felt. No TAM slide. No "AI market is $Xbn." Each lever is `mechanism → consequence` that a sceptic can attack with their own numbers (`R2S4.md:164`).

**Where it sits (7:30–9:00):**

*   **Exposure frame (15s):** `Exposure = freq(consequential actions) × P(unproven/unauthorized) × loss/wrong action` — buyer fills middle terms from their sample (`R2S4.md:168`).
*   **Lever A — avoided wrong actions (primary, 30s):** R3 held structural escape (`executed:false` artifact) × buyer's direct cost per payout/deletion/publication. Residual sized by published per-route FNR.
*   **Lever C — exact dead compute (20s):** Same graph read backward: `₹5 of ₹8 grounded nothing` — exact, no model (`docs/ARCHITECTURE.md:89`, `R2S4.md:193`). Trace products measure spend; this measures waste. Enterprise prices its own traffic — no % saved on slide.
*   **Levers D/E — alert fatigue without lowering gate + auditability (20s):** Matrix prices actuators (R0/R1 hedged → Pass+annotate, not Escalate) + append-only hash-chained ledger pointer: `action → cell → verdict → span → source/hash/ACL → principal → policy_version → latency` (`R2S2.md:281`).
*   **Buyer logic (20s):** Not org chart — architecture-derived roles (`R2S4.md:145`): *who pays when it fails* (Ops/CS/CHRO/CFO/CISO) ≠ *who runs it* (SRE/Risk) ≠ *who types the answer* (support worker). Beachhead = high-consequence routes (refund-class R3 + mixed-governance knowledge), not "all enterprise AI."
*   **Roadmap as earn-out, not feature calendar (25s):** Shadow (dual-emit `would have held N`) → Canary R0/R1 → Limited R2/R3 enforce → Broader envelope. Phase exits are counterfactuals + override thresholds, not dates (`R2S4.md:261`). Determinism works day one; statistics earn thresholds.

Lever G (earned autonomy) is spoken as **secondary, never the lead** (`R2S4.md:247`). No net-savings slide. No waste % invented.

---

### 6. Differentiation & Defence Moments

Weaved where the demo just proved them — not a separate "competitors" slide.

| Moment | Where in pitch | Line |
|---|---|---|
| **vs post-hoc trace products** (LangSmith/Arize/Helicone/WhyLabs) | Right after gate hold (3:10) | "Trace products tell you what went wrong *after* a user acted — audit trail, not interlock (`R2S4.md:40`). We record the entrance, not only the exit, and bind the commit path while text uses hold-back. Same graph that proves also accounts — exact dead compute." |
| **vs LLM-as-judge / wrappers** (NeMo Guardrails) | At C2 binding failure (4:00) | "The judge asks *does this look right?* — unfalsifiable, identity-blind, same-family blind spots. We ask *which span proves it?* — query with an answer (`docs/NARRATIVE.md:68`). Binding is computed by us; the model has no channel to declare a binding (`docs/QA.md:82`). Decision is pure rule engine, zero LLM (`docs/ARCHITECTURE.md:176`)." |
| **vs RAG groundedness** | At principal-flip (6:40) | "Closest cousin, still short three ways (`docs/ARCHITECTURE.md:91`): retrieval-only, averages so one wrong figure drowns, action-blind. We bind full provenance, price worst claim per pending action, and the identical unsupported claim → R1 Edit on a draft and R3 Escalate on a payment. **Retrieval is not permission. Proof scales with consequence.**" (`docs/NARRATIVE.md:96`, `docs/ARCHITECTURE.md:338`) |
| **vs composite 0–100 scores** | At matrix (4:15) | "Three owners/costs collapsed into one number that maps to no actuator. You cannot Block · Edit · Escalate on 87 (`docs/NARRATIVE.md:100`, `docs/ARCHITECTURE.md:304`). We have no score field in the decision path." |
| **Refuse-to-claim (about *us*)** | Immediately after FNR empty schema (6:00) — the only place it is credible | Deliver all four, brisk: "We do **not** claim we eliminate hallucinations — we claim ungrounded claims cannot authorise actions and we report what we missed (`docs/NARRATIVE.md:130`). We do **not** claim zero integration — we hook context assembly; that hook is the moat (`docs/NARRATIVE.md:134`). We do **not** claim zero latency — we never make the model feel slow; we make the action wait; quote only ≤40ms p50 / ≤200ms p95, never 40 as p95 (`docs/ARCHITECTURE.md:222`). We do **not** claim one accuracy number — hallucination/leakage/bias have different mathematics (`docs/NARRATIVE.md:144`)." Every deck disclaims rivals; almost none disclaim themselves." |
| **Bias handling** | If asked, or at roadmap tail (8:45) | "Counterfactual flip rate with CI, route-level, async — flag when CI excludes zero (`docs/QA.md:171`). Never `claim → bias verdict → matrix` (`R2S2.md:340`). Do not drop bias — brief requires it — but never as live per-response verdict." |
| **Hard QA (B1/B5)** | Ready for Q&A, seeded in pitch | B1: "We don't claim to verify what we were never given. We claim what we were never given cannot authorise an action." (`docs/QA.md:49`) B5: "We defend the claim-to-evidence link, not the truth of the evidence." (`docs/QA.md:89`) |

**Systems-clean discipline:** authorise · admit · prove · bind · refuse · hold · escalate · gate — never the banned vocabulary in our own voice. One permitted exception: the indictment line above.

---

### 7. Closing Beat — resolve the opening

**Exact closing move (9:30–10:00):** Return to the frozen transaction. Ledger fades, gate returns alone.

> "That system was never asked to prove anything. (`docs/NARRATIVE.md:229`)"
> *[hold 2 beats]*
> "**Now nothing acts until it can prove it should.** (`docs/NARRATIVE.md:231`)"
> "An AI response is a set of claims requesting permission to act (`docs/ARCHITECTURE.md:13`). Provenance outside the model. Default UNSUPPORTED. Entitlement is set-membership. R×S prices proof by consequence. Hard gate on the commit path. And the plane publishes what it missed — per route — not what it caught."

Leave empty FNR schema on screen for 5 seconds. No contact slide over it.

---

### 8. Anti-Patterns (Hard Kill List) — pitch dies if any appear

1. **Opening on generic "AI risk" or responsible-AI virtue.** Must open on held ₹1,84,000 transaction + category change.
2. **First sentence about failure says "response" not "claim."** Kills `NARRATIVE:176` discipline.
3. **Collapsing dual-action into one verdict.** "Response blocked/flagged" — forbidden. Show **R1 Edit + R3 Escalate held** simultaneous, worst-claim-per-action (`R2S1.md:40-49`).
4. **Saying "blocked" about the refund.** R3 × unsupported-categorical = **Escalate held with evidence packet**, never Block (`docs/ARCHITECTURE.md:349`, `R2S1.md:49`).
5. **Calling ledger "monitoring/detection/observation."** Banned in our voice (`docs/NARRATIVE.md:167`). Use authorise/admit/prove/bind/refuse/hold/escalate/gate.
6. **Inventing actuators or scores:** `STREAM` / `Kill Span` / `Redact & Flag` / `Hold & Re-verify` / `COMMIT BLOCKED` / composite risk / confidence / trust scores as disposition (`docs/ARCHITECTURE.md:355`, `R2S1.md:112`).
7. **Redrawing the matrix.** Transcribe 4×4 verbatim; axis labels + column vocabulary + cells load-bearing (`docs/ARCHITECTURE.md:156`). No low/medium/high collapse, no route-parameter cells.
8. **Leading with enablement/earned autonomy** before cost avoidance. G is secondary by freeze (`R2S4.md:247`).
9. **Filling the FNR schema with numbers.** Live = **null/empty placeholders only** — emptiness *is* the credibility play (`R2S2.md:382`). No `prototype_corpus` fill to look complete.
10. **Quoting latency as "40ms p95."** Correct is **≤40ms p50 / ≤200ms p95** (`docs/ARCHITECTURE.md:222`). Never relabel p50 as p95.
11. **Adding a third live bias/decision-support route.** Exactly two live routes; decision-support + async bias = enterprise envelope/proposal only (`R2S1.md:18-24`, `R2S2.md:24`).
12. **Showing LLM-as-judge pane, open-web rescue, or generative rewrite.** All rejected (`docs/ARCHITECTURE.md:292`).
13. **Putting chatbot chrome over ledger.** Ledger ≥60% or the governing test fails: "if removing the graph leaves the demo looking the same, scope has failed" (`R2S1.md:182`, `R2S3.md:198`).
14. **Pre-baked animation without visible live compute.** Binding/interlock must show real ~20–80ms work (`R2S3.md:39`).
15. **Saying clause 7.2 "caps/denies/doesn't cover."** It **does not exist** — absence, not conflict (`docs/ARCHITECTURE.md:346`).
16. **Inverting who pays:** customer did not lose money — **company wrongly pays out** (`docs/ARCHITECTURE.md:352`).
17. **Evidence packet missing diff or candidate spans `[]`.** Must show claim + spans + verdict + diff (`R2S1.md:122`).
18. **Universal fail-open, speculative release, or model-authored bindings.** All forbidden load-bearing floors (`docs/ARCHITECTURE.md:181`, `R2S2.md:264`).

---

### 9. Fidelity Self-Check — pitch protects every invariant from Stages 1–4

| Frozen invariant / content law | Where pitch holds it | How |
|---|---|---|
| **Default = UNSUPPORTED** (`ARCHITECTURE:70`, `R2S1:93`) | Beat 3 + Beat 4 | All claims born red; SUPPORTED only via bind/recompute; `UNKNOWN` never → `SUPPORTED` spoken at 3:45 |
| **Entitlement = set-membership, zero LLM, always on** (`ARCHITECTURE:109`, `R2S1:68`) | Beat 4 C3 + Beat 5 flip | `span.acl ⊆ principal.clearance` visible; Lane 1 deterministic; zero LLM in ACL path; flip proves identity, not classification |
| **Exact R×S matrix, no route parameter** (`ARCHITECTURE:144`, `R2S2:141`) | Beat 4 matrix highlight | 16 cells transcribed; cells highlighted *before* actuators; same `Unsupported+categorical` → R1 Edit vs R3 Escalate proves matrix ≠ renamed severity |
| **One graph `STEP→SPAN→CLAIM→ACTION`, three reads** (`ARCHITECTURE:29`) | Entire pitch backbone | Single ledger on screen from 3:20; performance/binding, cost/dead-compute, responsibility/ACL as three reads of that one object |
| **Hard gate on actions, not tokens; hold-back ~150–300ms; speculative release forbidden** (`ARCHITECTURE:202`, `R2S3:37`) | Beat 4 steps 7–9 | Text streams optimistically behind hold-back; `refund.execute committed:false` while escalated; interlock in executor, not UI |
| **Two-pending-actions resolution, held never blocked** (`ARCHITECTURE:328`, `R2S1:40`) | Centrepiece heart (4:15) | R1 Edit + R3 Escalate simultaneous, worst-claim-per-action, never collapsed; language "held and escalated with the evidence packet" |
| **Published FNR as typed format, empty until earned** (`ARCHITECTURE:277`, `R2S2:364`) | Beat 4 end + Beat 7 closer | Empty schema visible; `measurement_status` vocabulary; line "we publish misses per route" with CI; no invented % |
| **`UNKNOWN` never → `SUPPORTED`** (`ARCHITECTURE:265`) | Beat 3 routing rule | Derived/multi-hop → recompute or UNKNOWN → matrix + tier fail stance spoken |
| **Zero LLM at decision time; no composite score; no LLM-as-judge primary** (`ARCHITECTURE:176`, `R2S2:112`) | Architecture primer + defence | Action Interlock = pure rule engine; NLI is binder, not judge; no score field drives disposition |
| **Bias = async route-level counterfactual, never live matrix cell, never dropped** (`ARCHITECTURE:118`, `R2S1:18`) | Beat 7 tail | Spoken exactly as counterfactual flip rate + CI; no per-response bias verdict; not a third live route |
| **Exactly two live routes; third is enterprise template** (`R2S1:17`) | Scope framing (Beat 2) | Refund + Knowledge only; decision-support shown only in roadmap Phase 4 template |
| **Latency ≤40ms p50 / ≤200ms p95; never 40 as p95** (`ARCHITECTURE:222`) | Refusal + business case | Quoted once, correctly; Lane 1 majority-volume logic explains why it stays fast |
| **Surgical Edit only; evidence packet not alert** (`ARCHITECTURE:163`, `R2S1:121`) | Beat 4 steps 5–6 | Strip/one constrained regen + re-gate; second fail → Escalate; packet = claim + spans + verdict + diff |
| **Refuse-to-claim list (about *us*)** (`NARRATIVE:129`) | Beat 7 refusal | All four refusals delivered where FNR emptiness makes them credible |
| **Content laws: 7.2 does not exist (absence); company wrongly pays out; customer did not lose** (`ARCHITECTURE:346`) | Opening + Beat 4 | Never "caps/denies"; never inverted payout; confidence 0.94 mentioned only as foil |
| **Vocabulary: admission-control layer; authorise/bind/refuse** (`NARRATIVE:55`, `R2S4:375`) | All beats | Category noun correct; banned vocabulary never in our voice (one permitted indictment line) |

**Final spine, once you accept the thesis, is forced (`R2S4.md:377`):** *AI can act → unproven claim must not authorise → provenance outside model → Default UNSUPPORTED → entitlement set-membership → R×S prices by consequence → hard gate on commit → publish misses.*

Any softer design is a different product.

---
*End of Stage 5 Pitch Architecture — muse-spark-1.2-contributor-free.*
*Stages 1–4 are rendered, not reopened. A judge can stress the logic on this spine and attack the design on the architecture — no benchmark needs to be trusted.*
