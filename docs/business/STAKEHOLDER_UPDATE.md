# ControlPlane.ai — Round 2 Stakeholder Update

Accenture Innovation Challenge 2026 · Team ControlPlane · PS #1
One-screen readable. Weekly-style: shipped / next / risks / asks.

---

## What shipped (merged to main)

- **Provenance recorder + binder + entitlement + frozen interlock matrix** — one graph, `STEP → SPAN → CLAIM → ACTION`, default UNSUPPORTED, set-membership entitlement (zero LLM), exact R×S matrix (no route param).
- **Two live demo routes** — refund agent (dual-action: Edit + Escalate held) + knowledge assistant (principal flip; outcome flips with caller only).
- **FastAPI server + static console** — Clearance bay first viewport shows `HELD — ESCALATE` / `executed: false`; matrix cells light up before actuators; evidence packet on every Escalate; empty typed FNR schema.
- **Deterministic tests green** — `make test` → 107 passed, no failures, no "blocked" in refund language, no p95=40 ms anywhere.
- **Measured latency bench** — `submission/latency_bench.json` (n=200): gate p50≈0.074 ms / p95≈0.134 ms. Targets: ≤40 ms p50 / ≤200 ms p95 (never quote 40 as p95).
- **Pitch docs frozen** — `round2/CONTROLPLANE_R2_FINAL.md` (proposal) + `round2/R2S5.md` (Stage 5 pitch spine) + `docs/JUDGE_RUNBOOK.md` + `docs/HOSTILE_QA_DRILL.md`.
- **Competitive framing written** — `docs/KILL_SHOT.md` (one-pager, scannable in 60s); `docs/ACCEPTANCE.md` (copy-pasteable acceptance matrix with SHA + commands).

---

## What is next (Waves 6–8, this batch)

- **W6-05** — `docs/KILL_SHOT.md` (competitive one-pager vs RAG-only / confidence-threshold / LLM-judge). Done.
- **W6-06** — `docs/business/demo_video_script.md` (≤3 min, timed beats, never-say list, port/URL pointers). Done.
- **W6-08** — `docs/waves/wave-6-gotchas.md` (brand check R2S5 ↔ console; no mismatches found; held/escalated language clean everywhere). Done.
- **W8-01** — `docs/ACCEPTANCE.md` (exact commands + expected outputs + SHA). Done.
- **W8-03** — `docs/ASSUMPTIONS.md` (Round 2 params register: traffic scale, three use cases, API-only, synthetic corpora, FNR null, bias async-only, latency truth, integration cost = moat, 12 assumptions). Done.
- **W8-04** — this file (`docs/business/STAKEHOLDER_UPDATE.md`). Done.

---

## Honest risks (no sugar)

| Risk | Honest state | Mitigation / note |
|------|--------------|-------------------|
| **Lane 2 / Lane 3 deferred** | Deterministic Lane 1 is the full core of the prototype. Lane 2 (NLI/binding) and Lane 3 (bias replay, shadow audit, calibration) are indicated in architecture but not the live centrepiece. The pitch says so. | Earn-out is the roadmap: shadow → canary → enforce. Lane depth is earned, not faked. |
| **FNR is null** | We publish the typed schema with nulls until a stratified shadow audit + human adjudication produces a defensible number. Emptiness is the credibility play. | We do not invent a catch rate. The claim shape is on the schema once measured. |
| **Two live routes only** | A third live decision-support / bias route is refused by design (bias = async, per frozen invariants). Stage 1 is not an enterprise envelope demo. | Pitch frames it as architectural by design, not scope dodge. |
| **Synthetic corpora only** | No real PII, no proprietary enterprise data. Prototype uses curated single-node traces. | Honesty boundary: we do not claim we have real enterprise data. The provenance contract does not change when real corpora arrive. |
| **Integration cost is real** | One SDK hook + OpenAI-compatible proxy. Not "zero integration." Not "drop-in." Integration cost is the moat. | Pitch states it explicitly. Falls on the honesty boundary, not the product. |
| **No fabricated metrics** | No fake users, no fake revenue, no fabricated FNR %, no fabricated ROI. | We refuse-to-claim about ourselves. Any slide without a measured source is a lie and we cut it. |

---

## Asks

- **Tag approval** — when tests are green and a human approves: `git tag -a v0.2.0-round2 -m "Round 2 prize-day known-good"`. Not automatic. Do not push the tag until approved.
- **Pitch dry-run time** — two presenters, one demo machine, one handoff. Dry run the dual-action centrepiece + principal-flip cold at least once at full speed before pitch morning. Pre-flight: `make test && curl /healthz`.
- **Judge-readiness sign-off** — one person confirms the console cold-open shows `HELD — ESCALATE` / `executed: false` and the matrix cells light up before actuators, with no "blocked" for the refund anywhere in the first viewport. No second person re-renders.
- **Latency honesty check** — verify nobody on the team says "40 ms p95" or "forty millisecond p95" anywhere. Targets: ≤40 ms p50 / ≤200 ms p95. Measured gate: p50≈0.074 ms / p95≈0.134 ms.

---

## Source pointers

- Pitch spine (verbatim speak-from, handoff rule): `round2/R2S5.md`
- Stand script + never-say + port swap: `docs/JUDGE_RUNBOOK.md`
- Hostile Q&A drill (one-liners + live curls): `docs/HOSTILE_QA_DRILL.md`
- Competitive framing: `docs/KILL_SHOT.md`
- Acceptance matrix (commands + SHA): `docs/ACCEPTANCE.md`
- Assumptions register: `docs/ASSUMPTIONS.md`
- Brand-check gotchas (clean pass): `docs/waves/wave-6-gotchas.md`
- Demo video script: `docs/business/demo_video_script.md`
