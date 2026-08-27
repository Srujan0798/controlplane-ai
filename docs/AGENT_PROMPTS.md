# Agent prompts — ControlPlane Round 2 (post-merge)

**Repo root:** `/Users/srujansai/Desktop/SEBI`  
**Branch:** `main` (single source of truth — `feature/round2-controlplane` is merged)  
**Verified:** `106 passed, 1 skipped` · CLI demos OK · graphify updated

Agents must work **only on `main`**. Do not open `.worktrees/`. Do not invent FNR %, customer logos, or `p95=40ms`.

---

## Canon (read before coding)

| Role | Path |
|---|---|
| Frozen architecture | `docs/ARCHITECTURE.md` |
| Business proposal truth | `round2/CONTROLPLANE_R2_FINAL.md` |
| Pitch speak-from | `round2/R2S5.md` |
| Judge stand script | `docs/JUDGE_RUNBOOK.md` |
| Gap inventory | `docs/PRIZE_WIN_MATRIX.md` |
| Product surface intent | `PRODUCT.md` |
| How to run | `README.md` |

**Hard invariants (never “improve”):**
1. Provenance outside the model — model output never creates spans.
2. Default claim verdict = `UNSUPPORTED`.
3. Clause 7.2 does **not** exist → absence → `UNSUPPORTED` (never “doesn’t cover”).
4. Matrix transcribed, never redrawn.
5. Action Interlock is the sole decider.
6. Say **held / escalated with evidence packet** — never “blocked”.
7. Lane 1 = deterministic only (no LLM on critical path).

---

## Current tree (do not reorganize again)

```text
controlplane/     core + FastAPI + static console
policies/         YAML packs
examples/         CLI demos (refund, multi-usecase, knowledge-flip)
tests/            106+ tests
scripts/          PDF, bench, SBOM
submission/       Proposal PDF + Pitch PPTX + benches
docs/             architecture, pitch, proposal, runbook, prize matrix
round2/           FINAL + R2S5 (canon)
```

Ignored: `.venv/`, `.data/`, `.worktrees/`, `graphify-out/`, `node_modules/`, `.wave*`, `.impeccable*`.

---

## Done — do not rebuild

Core gate, dual-action refund, fail-closed tests, FastAPI + OpenAI shape, multi-page console, policies/metrics/audit/matrix/architecture/runbook pages, SQLite audits, security headers/API key/rate limits, threat model, sessions + hold-back, upstream + webhook + signed audits, bias probe, Prometheus, Docker Compose, CI, proposal PDF, pitch PPTX, SBOM freeze, latency bench, `make judge`.

---

## Ordered agent tasks

Copy **one** prompt per agent. Finish in order unless marked parallel-safe.

### Agent 0 — Sanity gate (run first, every time)

```
You are verifying ControlPlane on branch main at the repo root.

1. Read README.md and docs/JUDGE_RUNBOOK.md.
2. Run: python -m pytest tests/ -q
3. Run: python examples/refund_trace_demo.py
4. Run: python examples/knowledge_flip_demo.py
5. Start: uvicorn controlplane.server.app:create_app --factory --host 127.0.0.1 --port 8787
6. curl GET /healthz and POST /v1/controlplane/demo/refund?mode=enforce
7. Open http://127.0.0.1:8787 and confirm Clearance shows Edit + Escalate for refund.

Report: pass/fail per step with exact commands and errors. Fix only broken setup (deps, ports). Do not add features.
After code changes: graphify update .
```

### Agent 1 — Refresh prize matrix (truth inventory)

```
Update docs/PRIZE_WIN_MATRIX.md so every item matches the code on main TODAY.

Rules:
- Branch note must say main (feature is merged).
- Mark SHIPPED items DONE (sessions, hold-back, webhook, signing, upstream, bias, prometheus, multi-page UI, SQLite, security negatives, e2e smoke, proposal PDF, SBOM, make judge, CHANGELOG, etc.).
- Leave only real remaining gaps as GAP/PARTIAL/DEFER.
- Add a short “Remaining for prize day” section (max 15 bullets), ordered by room impact.

Do not implement features. Commit message: docs: refresh prize matrix for merged main.
After edits: graphify update .
```

### Agent 2 — Pitch fidelity: R2S5 ↔ deck ↔ console

```
Align the live pitch path. Canon speak-from file is round2/R2S5.md.

1. Diff round2/R2S5.md beats against docs/ROUND2-PITCH.md and submission/ControlPlane_Round2_Pitch.pptx (and .js if that builds the pptx).
2. Fix mismatches in wording: held≠blocked, clause 7.2 absence, dual Edit+Escalate, latency honesty (never quote 40ms as p95).
3. Ensure docs/JUDGE_RUNBOOK.md 60s script matches R2S5 demo spine.
4. If you regenerate the PPTX, update submission/ and note the command used.

Do not change the frozen matrix or ARCHITECTURE content laws. Prefer editing docs/ROUND2-PITCH.md + deck over rewriting R2S5 unless R2S5 has a factual error.
Commit: docs: align pitch deck and runbook to R2S5.
```

### Agent 3 — Proposal pack consistency

```
Ensure submission proposal matches round2/CONTROLPLANE_R2_FINAL.md Stage Check + invariants.

1. Read Stage Check at top of round2/CONTROLPLANE_R2_FINAL.md.
2. Compare to docs/ROUND2-PROPOSAL.md and submission/ControlPlane_Round2_Proposal.pdf.
3. Fix doc drift (missing invariants, wrong actuators language, outdated branch refs).
4. If PDF must regenerate: python scripts/build_proposal_pdf.py (or make pdf) and refresh submission/.

No new product claims. Commit: docs: sync proposal pack to FINAL.
```

### Agent 4 — Hostile Q&A drill sheet (room defense)

```
Create docs/HOSTILE_QA_DRILL.md — 12–15 hostile judge questions with:
- One-sentence answer
- Live demo click / curl that proves it (if any)
- Pointer into docs/QA.md or ARCHITECTURE.md section

Must cover: “isn’t this just a guardrail?”, “why no LLM judge?”, “what if clause 7.2 existed?”, “latency?”, “false negatives?”, “bias?”, “how do you fail closed?”, entitlement flip.

Link it from README Document map and JUDGE_RUNBOOK.
Commit: docs: add hostile Q&A drill sheet.
```

### Agent 5 — Event-day packaging (parallel-safe with 4)

```
Event readiness only — no new product features.

1. Add docs/EVENT_DAY_CHECKLIST.md: backup laptop, port 8080/8787, USB/airgap offline, known-good commit hash, make test / make judge, docker compose, panic recovery.
2. git tag recommendation text (do not force-push): suggest annotated tag v0.2.0-round2 after human approval.
3. Confirm Makefile targets: test, bench, run, judge, e2e, pdf, sbom — document in README if missing.
4. Ensure .gitignore still excludes .data, node_modules, graphify-out, .worktrees.

Commit: docs: event-day checklist and packaging.
```

### Agent 6 — Console microcopy & content laws (UI polish)

```
Polish judge-facing copy in controlplane/server/static/ only.

Requirements from PRODUCT.md + ARCHITECTURE §10:
- Visible “Clause 7.2 does not exist”
- Never say blocked — use held / escalated with evidence packet
- Category noun: admission-control layer
- Latency shown as measured numbers from /metrics or bench — not marketing
- Keyboard / projector mode still work
- prefers-reduced-motion respected

Verify in browser at 1280px and 375px. Run tests/test_e2e_console.py.
Commit: feat(ui): content-law microcopy polish for judges.
After: graphify update .
```

### Agent 7 — Coverage of remaining GAP tops from refreshed matrix

```
ONLY after Agent 1 refreshes the matrix. Implement the top 3 remaining GAP items marked “room impact” — nothing else.

Constraints:
- No LLM on critical path
- No matrix redraw
- Fail closed only
- Add/adjust tests for each change
- Run pytest -q before claiming done

Commit per item or one commit with a clear list. After: graphify update .
```

### Agent 8 — Final pre-flight (human + agent)

```
Final prize-day verification on main:

1. pytest -q → all green
2. make judge (or documented equivalent)
3. docker compose up --build → console on :8080
4. Walk JUDGE_RUNBOOK 60s script end-to-end
5. Walk HOSTILE_QA_DRILL top 5 answers with live proof
6. Confirm submission/ has Proposal.pdf + Pitch.pptx + latency_bench.json + sbom
7. Print known-good commit SHA and tag status

Output a single PASS/FAIL report. Fix only blockers. Do not start new features.
```

---

## Parallel map

```text
Agent 0 ──► Agent 1 ──► Agent 7
              │
              ├── Agent 2 ──► Agent 3
              ├── Agent 4 ──┐
              └── Agent 5 ──┴── Agent 6 ──► Agent 8
```

- **Serial:** 0 → 1 → 7; 2 → 3; then 8 last.
- **Parallel-safe after 0:** 2, 4, 5, 6 (6 may touch static UI; avoid simultaneous edits to same HTML/JS).

---

## Definition of done for the competition

1. `pytest -q` green on `main`
2. Judge can finish refund demo in ≤60s without reading docs
3. Proposal PDF + Pitch PPTX match FINAL + R2S5 language
4. Hostile Q&A + event checklist exist
5. No fake metrics; fail-closed preserved
```

---

## Superseded by Adaptoid waves (2026-08-28)

**New dispatch path:** `HOW_TO_RUN.md` + `work/wave-6|7|8/*.md`  
Agents 0–8 above completed the post-merge polish. Elevation continues via Waves 6–8 task files (Adaptoid Lite hybrid plan).
