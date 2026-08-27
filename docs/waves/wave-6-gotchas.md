# Brand Check — R2S5 ↔ Console Microcopy (Wave 6)

Accenture Innovation Challenge 2026 · Team ControlPlane · PS #1
Canons: `round2/R2S5.md` (speak-from), `docs/JUDGE_RUNBOOK.md` (never-say), `docs/ACCEPTANCE.md`.
Scope: fix only **factual / language mismatches**. No rewrite of `round2/CONTROLPLANE_R2_FINAL.md`.
No invented pitch claims.

---

## Method

1. Read R2S5 demo spine + JUDGE_RUNBOOK never-say table.
2. Read console first-viewport microcopy (`controlplane/server/static/index.html`) in the Clearance bay (the first visible surface).
3. Read every static console surface (architecture, matrix, metrics, runbook, print) plus the server code and demo scripts for prohibited vocabulary in any live context.
4. Record each finding (match / mismatch / not applicable).
5. Fix microcopy **only** where wrong — list each fix in this report.

---

## Findings

### A. Refund language — held / escalated, not blocked

| File | What it says | Verdict |
|------|--------------|---------|
| `controlplane/server/static/index.html:52-54` | "Clause 7.2 does not exist." + "Refund is **held and escalated with the evidence packet** — never 'blocked.'" | ✅ match |
| `index.html:390` (dynamic strip, first viewport) | "Awaiting clearance. Press Admit — refund proves Edit + Escalate (**held with packet, not blocked**)." | ✅ match |
| `architecture.html:89` | "Never say 'blocked' about the refund — it is **held and escalated with the evidence packet**." | ✅ match |
| `matrix.html:84` | "Clause 7.2 does not exist … Escalate, not Block. Say held and escalated with the evidence packet." | ✅ match |
| `runbook.html:68` | "Do not say 'blocked' about the refund. Say held and escalated with the packet." | ✅ match |
| `print.html:409` | "Action **held and escalated with evidence packet**." | ✅ match |
| `examples/refund_trace_demo.py` / `knowledge_flip_demo.py` / `multi_usecase_demo.py` | no "blocked" / "Blocked" / "BLOCKED" found | ✅ clean |
| `controlplane/server/app.py` + handlers / interlock / ledger | no live "blocked" for refund found | ✅ clean |

**Finding:** No "blocked" for the refund in the Clearance first viewport, in any live surface, or in any demo script. The task's C2 ("no remaining 'blocked' for refund in Clearance first viewport") is satisfied.

### B. Clause 7.2 — absence, not contradiction; never caps / denies / doesn't cover

| File | What it says | Verdict |
|------|--------------|---------|
| `index.html:52` | "Clause 7.2 does not exist." | ✅ match |
| `architecture.html:68` | "Clause 7.2 does not exist." | ✅ match |
| `architecture.html:108` (law 01) | "Clause 7.2 does not exist. Never 'caps,' never 'denies.' Absence, not conflict — that is why Escalate, not Block." | ✅ match |
| `matrix.html:84` | "Clause 7.2 does not exist. The failure is absence of evidence, not conflicting evidence." | ✅ match |
| `runbook.html:75` | "Clause 7.2 does not exist — absence of evidence, not conflicting evidence." | ✅ match |
| C1 → C3 (all demo/static surfaces) | No caps/denies/doesn't-cover phrasing found in any live context | ✅ clean |

**Finding:** All surfaces use "does not exist" + absence framing. No caps/denies/doesn't-cover phrasing in any live material.

### C. Latency — ≤40 ms p50 / ≤200 ms p95; never 40 ms p95

| File | What it says | Verdict |
|------|--------------|---------|
| `index.html:97` (Clearance bay first viewport) | "Targets ≤40ms p50 / ≤200ms p95 · measured gate p50≈0.074 / p95≈0.134" | ✅ match |
| `metrics.html:35,38` | "Latency targets ≤40ms p50 / ≤200ms p95; measured gate p50≈0.074 / p95≈0.134 — never quote 40ms as p95" + claim shape | ✅ match |
| Any "40ms p95" / "40 ms p95" in console or server or demo? | none found | ✅ clean |

**Finding:** Latency phrasing matches the runbook. No p95=40 ms anywhere in live material.

### D. Money / who pays

| File | What it says | Verdict |
|------|--------------|---------|
| `index.html` / `architecture.html` | "The **company wrongly paid**. … Clause 7.2 does not exist." | ✅ match |
| "Customer lost money?" | No "customer lost money" phrasing found in any live surface | ✅ clean |

**Finding:** Who-pays language matches R2S5 ("company wrongly paid out"). Customer-loss phrasing absent.

### E. Vocabulary — monitor/detect/observe/trust score/AI safety as virtue

One permitted exception: the indictment line *"Everyone watches the exit. Nobody records the entrance."* is allowed to indict what everyone else built. Beyond that line:

| File | Findings | Verdict |
|------|----------|---------|
| `index.html` / `architecture.html` / `matrix.html` / `runbook.html` / `metrics.html` | No stand-alone "monitor / detect / observe / trust score / AI safety as virtue" found in our own voice (aside from the single permitted indictment line) | ✅ clean |

**Finding:** Vocabulary matches the speak-from table.

### F. FNR / dead compute

| File | Findings | Verdict |
|------|----------|---------|
| `metrics.html` | Empty typed FNR shape; claim shape: "*On this route we catch <measured>% of ungrounded claims at ≤40ms p50 — and here is the <measured>% we don't.*" Emptiness = credibility. | ✅ match |
| `architecture.html:68,108` (dead compute line) | "Cost never blocks a user's answer; it kills a runaway loop." | ✅ match |

### G. Composite score / confidence-as-decider

| File | Findings | Verdict |
|------|----------|---------|
| All live surfaces | No single 0–100 composite risk/confidence/trust score as decision mechanism found | ✅ clean |

**Finding:** No competitor-aping composite score as the decision primitive.

### H. Dual-action collapse

| File | Findings | Verdict |
|------|----------|---------|
| `index.html` / `architecture.html` / `matrix.html` | Both pending actions (Edit + Escalate held) shown simultaneously — never collapsed into one "response blocked" | ✅ clean |

---

## Mismatches found

**None requiring fixes.** The console microcopy already tracks R2S5 speak-from + JUDGE_RUNBOOK never-say.

Past microcopy polish from `commit 06d6115` + `commit dee3513` held: held/escalated language, absence framing, latency truth, and who-pays language all present in the Clearance first viewport and across every static surface. The console/server/demo-script grep for prohibited vocabulary returned clean.

---

## Items verified, not fixed

| Check | Status |
|-------|--------|
| No "blocked" for refund in Clearance first viewport (C2) | ✅ satisfied |
| No caps/denies/doesn't-cover for clause 7.2 | ✅ satisfied |
| No 40 ms p95 anywhere | ✅ satisfied |
| No "customer lost money" | ✅ satisfied |
| No composite 0–100 score as decision primitive | ✅ satisfied |
| Dual-action not collapsed | ✅ satisfied |
| FNR empty typed shape until earned | ✅ satisfied |
| Dead compute phrasing present | ✅ satisfied |

No console microcopy file was touched in this pass — no fix was required and the task forbids touching canon pitch docs. The gotchas file is a record of a clean pass.

---

## What would trigger a fix next time

- A console surface that says "blocked" / "COMMIT BLOCKED" / "response blocked" for the refund without the "held/escalated with packet" framing.
- A surface that says "40ms p95" / "forty millisecond p95" anywhere.
- A surface that says "caps / denies / doesn't cover" for clause 7.2.
- Any composite score (0–100) presented as the decision mechanism.
- Any "customer lost money" / "refund denied" phrasing.

---

## Source pointers

- Speak-from canon (demo spine + never-say): `round2/R2S5.md`
- Runbook (stand + never-say table): `docs/JUDGE_RUNBOOK.md`
- Console microcopy (Clearance bay first viewport + all static surfaces): `controlplane/server/static/*.html`
- Server / handlers / interlock: `controlplane/server/`
- Demo scripts: `examples/`
- Acceptance matrix (companion verification): `docs/ACCEPTANCE.md`
