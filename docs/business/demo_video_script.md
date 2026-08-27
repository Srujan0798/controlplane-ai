# ControlPlane.ai — Demo Video Script (≤3 min)

Accenture Innovation Challenge 2026 · Round 2 · Team ControlPlane
Read aloud in 2:45–3:00. Beats map 1:1 to `round2/R2S5.md` §4 demo spine and `docs/JUDGE_RUNBOOK.md`.
Ports: **8080** (Docker) or **8787** (local uvicorn). Health: `GET /healthz`.

---

## Pre-roll (silent, on the recorded build)

Screen is already live on the Clearance / Operate strip. **No title slide.** The first frame is the held refund:

```text
Action:      refund.execute
Args:        { amount: 184000, reason: "clause 7.2", order_id: "ORD-1023" }
R:           R3 — irreversible payment
Status:      HELD — ESCALATE
Executed:    false
```

A two-second beat of silence. Then Beat 1.

---

## Beat 1 — Cold open, held refund (0:00–0:30)

**On-screen:** held-refund panel; ledger collapsed; matrix dim.

**VOICE (A):**

> "₹1,84,000. Refund executed under clause 7.2 of the vendor agreement.
>
> Clause 7.2 does not exist.
>
> Every filter passed it. Confidence read 0.94. The money moved on Tuesday. Found Friday.
>
> **The system didn't fail. It was never asked to prove anything.**
>
> Everyone watches the exit. Nobody records the entrance."

**Action:** none. Static panel.

---

## Beat 2 — Ledger reveal, claims born UNSUPPORTED (0:30–1:15)

**On-screen:** expand the Evidence Ledger. Spans visible before claims.

```
AGR-VENDOR-v3            ACL: agent     clauses 1–6   hash: 9f3c…
ORD-1023                 ACL: agent     amount 184000 hash: 12aa…
FIN-INTERNAL-NOTE        ACL: internal_analyst   excludes agent_refund_7
INJECT-NOTICE            ACL: untrusted (injection cannot author provenance)
```

Three claims appear. **All start `UNSUPPORTED`.** Then they resolve:

| Claim | What it says | Type | Finding |
|-------|--------------|------|---------|
| C1 | Refund ₹1,84,000 / order ORD-1023 | numeric | binds → **SUPPORTED** |
| C2 | "under clause 7.2 …" | categorical | zero candidates → **UNSUPPORTED** |
| C3 | Text grounded on FIN-INTERNAL-NOTE | textual | ACL excludes caller → **entitlement violation** |

**VOICE (A):**

> "Before the model ran, we captured what it was allowed to know — source, ACL, content hash, offsets. The model cannot write these. **Binding is computed by us, not asserted by the model.** Injection has no channel to declare a binding.
>
> Every claim starts unsupported. C1 earns proof: the number matches an order record. C2 finds nothing. **Clause 7.2 has no span.** Absence is not contradiction."

---

## Beat 3 — Dual action, matrix cells before actuators (1:15–1:50)

**On-screen:** 4×4 matrix. Two cells light up before either actuator fires.

| Pending action | Tier | Matrix cell | Actuator |
|----------------|------|-------------|----------|
| `text.show` (worst = C3) | R1 | R1 × entitlement violation | **Edit** |
| `refund.execute` (worst = C2) | R3 | R3 × Unsupported + categorical | **Escalate — held** |

**VOICE (A):**

> "One response. Two pending actions. The system prices them separately.
>
> The text carries a claim grounded on an internal note the refund agent isn't entitled to read — R1, entitlement violation, **Edit**.
>
> The refund carries a claim with no evidence at all — R3, unsupported categorical, **Escalate. Held.**
>
> Same response. Two different consequences. **Severity describes the error. Blast radius describes the consequence. Proof scales with consequence.**"

---

## Beat 4 — Surgical Edit + held refund + evidence packet (1:50–2:25)

**On-screen:** ledger scrolls to show C3 stripped from customer-visible text (no free-form rewrite). Refund executor log shows `committed: false`. Evidence packet panel opens: claim C2, candidate spans `[]`, verdict `UNSUPPORTED`, diff.

```text
commit_refund()
   → COMMIT = FALSE
   → ACTION = HELD
   → ESCALATION PACKET = READY
```

**VOICE (A):**

> "Text is surgically edited — only the failing claim removed. The refund stays held. The company does not wrongly pay out ₹1,84,000.
>
> Here is the evidence packet: what was claimed, what evidence existed — nothing — the verdict, the diff. **Not a bare alert. An evidence packet a human reviewer can act on.**
>
> The gate is on the commit, not on tokens. Text streams behind a 150–300 ms hold-back. **Speculative verification is permitted. Speculative release is forbidden.**"

---

## Beat 5 — Principal flip (2:25–2:55)

**On-screen:** knowledge route. Two runs side-by-side.

```
principal = analyst_01      → R1 × entitlement → Edit
principal = hr_partner_01   → same span · same claim · same graph → SUPPORTED → Pass
```

**VOICE (A):**

> "Same span. Same claim. Same graph. I changed one thing: **who is asking**.
>
> The entitlement check is set-membership — does the caller's clearance include the span's ACL? Zero LLM. Deterministic. Sub-millisecond.
>
> **Authorisation is set-membership. Retrieval is not permission.** The size of the model is irrelevant."

---

## Beat 6 — Close (2:55–3:00)

**On-screen:** the Evidence Ledger, the held refund, the surgical Edit, the evidence packet, the empty FNR schema — all on one screen. No logos. No "thank you."

**VOICE (A):**

> "The system you just saw was never asked to prove anything.
>
> Now **nothing acts until it can prove it should.**
>
> Provenance outside the model. Default unsupported. Entitlement is set-membership. Proof scales with consequence. Hard gate on the commit path. And **we publish what we miss**.
>
> Any softer design is a different product."

Hold the empty FNR schema on screen for **5 seconds**. Fade.

---

## On-screen actions, timecoded

| Time | Action | URL / command |
|------|--------|---------------|
| 0:00 | (cold open already on screen) | — |
| 0:30 | reveal ledger (no click) | — |
| 1:15 | show matrix (no click) | — |
| 1:50 | pre-record Edit + held packet (or live `refund · enforce`) | `POST /v1/controlplane/demo/refund?mode=enforce` |
| 2:25 | principal flip, two curls back-to-back | `POST /v1/controlplane/demo/flip?principal=analyst_01` · `?principal=hr_partner_01` |
| 2:55 | final ledger on screen, empty FNR visible | — |

If recording (not live): the dual-action segment is **one unbroken take** and **labelled on screen**: `recorded · build <sha>`.

---

## Never-say list (read with the script)

| ❌ Never | ✅ Say |
|---|---|
| "blocked the refund" | **held** and **escalated** with the evidence packet |
| "40 ms p95" / "forty millisecond p95" | **≤40 ms p50** / **≤200 ms p95 targets**; measured gate p50≈0.074 ms, p95≈0.134 ms |
| "clause 7.2 caps / denies / doesn't cover" | **clause 7.2 does not exist** — absence → `UNSUPPORTED` |
| "customer lost money" | **company wrongly paid out** — customer did not lose money |
| "we eliminate hallucinations" | ungrounded claims **cannot authorise actions**; we publish what we miss |
| monitor · detect · observe · trust score · "AI safety" as virtue | authorise · admit · prove · bind · hold · escalate · gate |
| composite 0–100 score | discrete verdict × blast-radius tier; per-route FNR |

One permitted exception to the vocabulary ban: the indictment line *"Everyone watches the exit. Nobody records the entrance."* — it indicts what everyone else built.

---

## Recording specs (operator notes)

- **Resolution:** 1920×1080. **Frame rate:** 30 fps.
- **Console scale:** ≥150% browser zoom so the ledger is ≥60% of frame.
- **Cursor:** visible on every click. No animated cursors.
- **No transitions, no lower-thirds, no music.** The architecture is the closer.
- **Audio:** -16 LUFS, mono lavalier preferred. Room tone at the held-refund cold open.
- **Build hash:** stamp the build SHA on the bottom-left at 0:00 (e.g. `build 46a1d74`). Update before each take.
- **Pre-flight:** `make test && curl /healthz`. Two dry runs at full speed before the take.

---

## Source pointers

- Speak-from canon (demo spine): `round2/R2S5.md` §3 opening, §4 demo, §7 close
- Stand script: `docs/JUDGE_RUNBOOK.md` — 60-second script + Never-say table
- Kill-shot framing: `docs/KILL_SHOT.md`
- Hostile Q&A (if Q&A follows the video): `docs/HOSTILE_QA_DRILL.md`
