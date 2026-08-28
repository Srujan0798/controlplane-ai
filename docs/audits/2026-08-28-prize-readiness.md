# Prize-readiness audit — ControlPlane.ai (Accenture Round 2)

**Date:** 2026-08-28
**Current SHA:** `25045330789bf0a6a445d5de4e607197abbb7787`
**Branch of record:** `main`
**Auditor:** Tier-2 Adaptoid worker (docs-only; no code changes)

> Frozen invariants applied: provenance outside model; default `UNSUPPORTED`; Clause 7.2 does not exist; MATRIX transcribed never redrawn; Action Interlock sole decider; refund = held/escalated never "blocked"; Lane 1 deterministic only (no LLM); fail closed. No FNR %, no customer logos, no "40ms as p95" invented anywhere below.

---

## 1. Pass criteria — `docs/ps.md` asks mapped to evidence

`docs/ps.md` (lines 48–52) asks Round 2 to deliver three things. Each is mapped to concrete evidence on `main`.

| ps.md ask | Evidence (file) | Report / proof |
|---|---|---|
| **Detailed Business Proposal** (problem framing, solution design, target users, business case/impact, phased roadmap, key risks + mitigations) | `round2/CONTROLPLANE_R2_FINAL.md`, `round2/R2S5.md`, `docs/ASSUMPTIONS.md`, `docs/ACCEPTANCE.md`, `submission/ControlPlane_Round2_Proposal.pdf` | W8-03 (`docs/ASSUMPTIONS.md`), W8-01 (`docs/ACCEPTANCE.md`); proposal PDF in `submission/` |
| **Working Prototype** (functional core mechanism on illustrative/sample data) | `controlplane/` (STEP→SPAN→CLAIM→ACTION, provenance audit, entitlement ACL, frozen R×S matrix, dual Edit+Escalate, hold-back), `docs/ARCHITECTURE.md` | `docs/PRIZE_WIN_MATRIX.md` A1–A25, B26–B45; W8-01 acceptance matrix |
| **Pitch Presentation** (proposal + prototype for evaluation) | `submission/ControlPlane_Round2_Pitch.pptx`, `docs/JUDGE_RUNBOOK.md`, `docs/HOSTILE_QA_DRILL.md`, `docs/KILL_SHOT.md` | `docs/PRIZE_WIN_MATRIX.md` F93–F105 |

Secondary judge lenses (novelty, technical depth, enterprise realism, demo clarity, risk awareness) are addressed by: `docs/THREAT_MODEL.md` (security), `docs/ACCEPTANCE.md` (determinism + honest FNR empty shape), `docs/ASSUMPTIONS.md` (risk awareness), and the live `/runbook` + `/architecture` + `/matrix` console surfaces.

---

## 2. Findings

Status legend: **DONE** · **PARTIAL** (evidence attached) · **GAP** · **DEFERRED**.

### CRITICAL (must hold for prize day)

| # | Finding | Evidence (path) | Status |
|---|---|---|---|
| C1 | Core primitive STEP→SPAN→CLAIM→ACTION with provenance outside model | `docs/PRIZE_WIN_MATRIX.md:18` (A1–A2); `docs/ARCHITECTURE.md` | DONE |
| C2 | Default verdict `UNSUPPORTED`; Clause 7.2 absence = `UNSUPPORTED` (never "doesn't cover") | `docs/PRIZE_WIN_MATRIX.md:20,24` (A3,A7); `docs/JUDGE_RUNBOOK.md:98` | DONE |
| C3 | Action Interlock is sole decider; frozen R×S MATRIX never redrawn | `docs/PRIZE_WIN_MATRIX.md:22` (A5); `tests/test_interlock.py` (16 cells) | DONE |
| C4 | Dual Edit + Escalate actuators, refund = held/escalated (never "blocked") | `docs/PRIZE_WIN_MATRIX.md:23` (A6); `docs/waves/wave-6-gotchas.md` (W6-08) | DONE |
| C5 | Lane 1 deterministic only — no LLM on critical path | `docs/AGENTS.md` invariant 7; `docs/JUDGE_RUNBOOK.md:82` | DONE |
| C6 | Working prototype runs (`make test` green, demo routes live) | `work/reports/wave-8/W8-01.report.md` (107 passed); `docs/ACCEPTANCE.md` | DONE |

### HIGH (strongly expected by judges)

| # | Finding | Evidence (path) | Status |
|---|---|---|---|
| H1 | OpenAI-compatible `/v1/chat/completions` proxy | `docs/PRIZE_WIN_MATRIX.md:46` (B26) | DONE |
| H2 | Judge console UI (Operate, Audit, Matrix, Architecture, Metrics, Runbook, Policies) | `docs/PRIZE_WIN_MATRIX.md:48–54` (B27–B34) | DONE |
| H3 | Hash-chained + tamper-evident signed audit ledger | `docs/PRIZE_WIN_MATRIX.md:25,73,100` (A8,A73,A74) | DONE |
| H4 | Multi-turn / session parent ledger (compounding risk) | `docs/PRIZE_WIN_MATRIX.md:34` (A17); `controlplane/session.py` | DONE |
| H5 | Latency bench published with real measured numbers (honest) | `submission/latency_bench.json`; `docs/PRIZE_WIN_MATRIX.md:42` (A25) | DONE |
| H6 | Pitch deck + proposal PDF + runbook + hostile-QA drill | `docs/PRIZE_WIN_MATRIX.md:93–98` (F93–F98) | DONE |
| H7 | Acceptance matrix (W8-01) proving Edit+Escalate expectation + FNR empty shape | `docs/ACCEPTANCE.md`; `work/reports/wave-8/W8-01.report.md` | DONE |
| H8 | Assumptions register grounding directional params | `docs/ASSUMPTIONS.md`; `work/reports/wave-8/W8-03.report.md` | DONE |

### MEDIUM (polish / enterprise depth; not stand-blocking)

| # | Finding | Evidence (path) | Status |
|---|---|---|---|
| M1 | Fail-stance by tier — in policy YAML/packs, not separately enforced beyond interlock | `docs/PRIZE_WIN_MATRIX.md:29` (A12) | PARTIAL |
| M2 | Empty / loading / error console states | `work/reports/wave-6/W6-04.report.md`; `docs/PRIZE_WIN_MATRIX.md:38` (B38) | PARTIAL |
| M3 | Accessibility (aria + reduced-motion; no full WCAG audit) | `docs/PRIZE_WIN_MATRIX.md:39` (B39); `controlplane/server/static/` | PARTIAL |
| M4 | Brand consistency console ↔ pitch | `docs/PRIZE_WIN_MATRIX.md:44` (B44); `work/reports/wave-6/W6-08.report.md` | PARTIAL |
| M5 | Favicon / OG meta (no Open Graph tags verified) | `docs/PRIZE_WIN_MATRIX.md:45` (B45); W6-01 | PARTIAL |
| M6 | Versioned policy packs (not full DAG lifecycle engine) | `docs/PRIZE_WIN_MATRIX.md:40` (A23) | PARTIAL |
| M7 | Lane 3 async FNR audit loop (shadow counters + bias probe; no human adjudicator) | `docs/PRIZE_WIN_MATRIX.md:33` (A16) | PARTIAL |
| M8 | OpenAPI examples thin (auto schema present) | `docs/PRIZE_WIN_MATRIX.md:63` (C63) | PARTIAL |
| M9 | CORS allowlist | `docs/PRIZE_WIN_MATRIX.md:53` (C53) | GAP |
| M10 | Idempotency-Key support | `docs/PRIZE_WIN_MATRIX.md:55` (C55) | GAP |
| M11 | Proof cache by context hash | `docs/PRIZE_WIN_MATRIX.md:31` (A14) | GAP |
| M12 | Shadow dual-emit CSV export | `docs/PRIZE_WIN_MATRIX.md:24` (A24) | GAP |
| M13 | Known-good annotated tag `v0.2.0-round2` | `docs/PRIZE_WIN_MATRIX.md:159` (G121) — human approval required | DEFERRED |

### LOW (nice-to-have; explicitly deferred/optional)

| # | Finding | Evidence (path) | Status |
|---|---|---|---|
| L1 | Lane 2 NLI off critical path | `docs/PRIZE_WIN_MATRIX.md:32` (A15) | DEFERRED |
| L2 | Speculative tool-arg verification in-flight | `docs/PRIZE_WIN_MATRIX.md:35` (A18) | GAP |
| L3 | Printable one-pager from console | `docs/PRIZE_WIN_MATRIX.md:40` (B40) — pre-existing `/print` | DONE |
| L4 | Dead-compute economist view in UI | `docs/PRIZE_WIN_MATRIX.md:36` (A19) | DONE |
| L5 | Soak / coverage gate | `docs/PRIZE_WIN_MATRIX.md:83,113` (E83,E113) | GAP |
| L6 | Compose profiles / hot-reload / graceful shutdown | `docs/PRIZE_WIN_MATRIX.md:58,60,66` (C58,C60,C66) | GAP |
| L7 | SBOM / dependency scan | `docs/PRIZE_WIN_MATRIX.md:78,104` (D78,D104) | DONE (SBOM); GAP (dep-scan) |
| L8 | Golden screenshots / replay harness for FNR labels | `docs/PRIZE_WIN_MATRIX.md:91,92,122` | GAP |

---

## 3. Latency honesty

Sourced **only** from `submission/latency_bench.json` (n=200, TestClient, endpoint `/v1/controlplane/demo/refund?mode=enforce`).

| Metric | Value (measured) |
|---|---|
| Gate latency p50 | **0.074 ms** |
| Gate latency p95 | **0.134 ms** |
| Gate latency p99 / max | 0.832 ms / 4.045 ms |
| Wall (HTTP round-trip) p50 / p95 | 1.247 ms / 1.739 ms |

**Targets** (stated separately, never as measured results): **≤40 ms p50 / ≤200 ms p95** on R0/R1.

> We **never** quote "40 ms as p95." The 40 ms figure is a target ceiling; the measured gate p95 is 0.134 ms — over 1,000× under target. The bench is sequential N=200 and is explicitly not marketed as a p95=40ms claim (`submission/latency_bench.json` note line). No invented latency numbers appear in this audit.

---

## 4. Risks (honest)

- **Lane 2 NLI deferred (L1):** semantic contradiction detection lives off the critical path by design. Lane 1 stays deterministic; no LLM on the gate. Acceptable per AGENTS.md invariant 7, but a judge probing "do you catch subtle contradictions?" gets a "we publish what we miss" answer, not a hidden LLM.
- **Lane 3 async FNR loop partial (M7):** shadow counters + bias probe exist; there is **no human adjudicator loop and no labelled FNR %**. The FNR schema is intentionally empty — the empty shape *is* the credibility play. We do not invent an FNR %.
- **FNR empty shape is the honest position:** per `docs/ACCEPTANCE.md` and `docs/JUDGE_RUNBOOK.md`, falsification-rate numbers are published only when labels exist. Today the typed schema is null. This is disclosed, not concealed.
- **Only two live routes demonstrated deeply (refund + flip/principal):** support/copilot/decision scenarios exist but the dual-action centrepiece is refund-centric. Judge narrative (R2S5 beat 4) owns this; acceptable but worth rehearsing.
- **Synthetic corpora only:** no real enterprise data — by design per ps.md ("illustrative or sample data is expected and encouraged"). Integration-cost realism is argued as the moat, not faked with a customer logo.
- **Known-good tag not created (M13):** `v0.2.0-round2` recommended after human approval; not auto-created (per AGENTS.md / JUDGE_RUNBOOK "do not run unless human asks").
- **GAP items (M9/M10/M11/M12, several LOW):** CORS, idempotency, proof cache, shadow CSV, soak/coverage — enterprise polish with low stand impact; none block the core demonstration.
- **No "blocked" for refund anywhere:** verified across Clearance first viewport, `/print`, proposal, and runbook (W6-08). Language is consistently "held and escalated with evidence packet."

---

## 5. Sign-off

- **Orchestrator verification:** `docs/PRIZE_WIN_MATRIX.md` line-item inventory reviewed against `main` at SHA `25045330789bf0a6a445d5de4e607197abbb7787`; W8-01 acceptance matrix, W8-03 assumptions, W8-04 stakeholder one-pager cross-checked.
- **Tests:** `make test` → 107 passed / 0 failures (per W8-01 report). No code changed in this audit task.
- **Human verification required (do not self-approve):**
  - [ ] Run `make test` and `make judge` on the prize-day machine.
  - [ ] Approve and create annotated tag `v0.2.0-round2` (or explicitly waive).
  - [ ] Confirm refund live demo shows Edit + Escalate simultaneously, `executed:false`, no "blocked".
  - [ ] Confirm latency numbers cited only as measured (p50≈0.074 / p95≈0.134 ms) vs target (≤40 / ≤200 ms).

---

## 6. Recommendation

**PASS (conditional on human sign-off above).**

ControlPlane.ai on `main` (SHA `25045330789bf0a6a445d5de4e607197abbb7787`) satisfies all three Round 2 asks from `docs/ps.md` — a detailed business proposal, a deterministic working prototype of the core admission-control mechanism, and a pitch package — with every frozen invariant intact, honest latency reporting, and no invented FNR %, logos, or "40ms p95"; remaining GAP/DEFERRED items are enterprise-polish and explicitly deferred by design, not stand-blocking.
