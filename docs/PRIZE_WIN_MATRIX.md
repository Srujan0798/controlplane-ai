# Prize-win matrix — ControlPlane Round 2

Honest inventory. What we have vs what first-prize teams actually need.

**Branch:** `main` (single source of truth). `feature/round2-controlplane` is **merged**.  
**Verified baseline:** 119 passed / 2 skipped (run `make test` on `main` today — see W8-08 refresh).  
**Refreshed:** W8-08 — line items match code/docs on `main` today (post Waves 6–8).  
**Agent prompts:** [`docs/AGENT_PROMPTS.md`](AGENT_PROMPTS.md).

Scoring lens: Accenture Round 2 asks for (1) detailed business proposal (2) working prototype of core mechanism (3) pitch. Judges also score novelty, technical depth, enterprise realism, demo clarity, risk awareness.

Legend: `DONE` · `PARTIAL` · `GAP` · `DEFER` (explicitly later)

---

## A. Core mechanism & architecture (mechanism must be undeniable)

1. STEP→SPAN→CLAIM→ACTION primitive — DONE
2. Provenance outside the model — DONE
3. Default UNSUPPORTED — DONE
4. Entitlement ACL check — DONE
5. Frozen R×S matrix (never redrawn) — DONE
6. Dual-action same ledger (Edit+Escalate) — DONE
7. Clause 7.2 absence semantics — DONE
8. Hash-chained ledger — DONE
9. Context-assembly freeze — DONE
10. Derived claims → UNKNOWN — DONE
11. Shadow vs enforce modes — DONE (API + console mode switch + metrics)
12. Fail stance by tier — PARTIAL (in policy YAML / packs; not separately enforced beyond interlock)
13. Hold-back buffer / streaming gate — DONE (`controlplane/holdback.py`, wired in pipeline + overlay)
14. Proof cache by context hash — GAP
15. Lane 2 NLI (off critical path) — DEFER
16. Lane 3 async FNR audit loop — PARTIAL (shadow counters + bias probe; no human adjudicator loop)
17. Multi-turn compounding risk / session parent ledger — DONE (`controlplane/session.py` + APIs)
18. Speculative verification of tool args — GAP (hold-back forbids speculative *release*; arg verify-in-flight not built)
19. Dead-compute economist view in UI — DONE (Clearance bay + architecture copy)
20. Bias measurement surface (responsibility axis) — DONE (`controlplane/bias.py`, pipeline probe)
21. Architecture interactive diagram for judges — DONE (`/architecture`)
22. Matrix explorer (click cell → example) — DONE (`/matrix`)
23. Versioned policy DAG engine (not just YAML packs) — PARTIAL (versioned YAML packs; not full DAG lifecycle)
24. Shadow dual-emit counterfactual export CSV — GAP (counters + Prometheus; no CSV export)
25. Published latency targets with real bench numbers — DONE (`submission/latency_bench.json`, `make bench` / `make judge`)

## B. Prototype surface (judges must touch it)

26. OpenAI-compatible `/v1/chat/completions` — DONE
27. Demo scenarios API — DONE
28. Judge console UI — DONE (multi-page Operate console)
29. Policies page — DONE (`/policies`)
30. Metrics / FNR cockpit — DONE (`/metrics`)
31. Audit explorer (search past requests) — DONE (`/audit` + list API)
32. Interactive matrix page — DONE (`/matrix`)
33. Architecture story page — DONE (`/architecture`)
34. 60-second judge runbook page — DONE (`/runbook` + `docs/JUDGE_RUNBOOK.md`)
35. Keyboard shortcuts (Admit, scenario switch) — DONE (1/2/3 · A · E/S)
36. Deep-linkable demo URL `?scenario=refund&mode=enforce&autorun=1` — DONE
37. Mobile / projector layout — DONE (projector toggle + responsive tokens)
38. Empty / loading / error states — DONE (loading/error strip chrome + aria-live + err dialog; ev: `work/reports/wave-6/W6-04.report.md`, `controlplane/server/static/index.html`, `controlplane/server/static/css/bay.css`)
39. Accessibility (focus, contrast, reduced motion) — PARTIAL (aria + `prefers-reduced-motion`; no full WCAG audit)
40. Printable one-pager from console — DONE (`/print` route `controlplane/server/app.py:267-269` + `controlplane/server/static/print.html`, held≠blocked verified; ev: `work/reports/wave-6/W6-02.report.md`)
41. Demo “reset room” button — DONE
42. Side-by-side ungated vs gated text — DONE
43. Soundless “flap” polish + microcopy — DONE (flap UI + content-law polish `06d6115`)
44. Brand consistency with pitch deck — DONE (R2S5 ↔ deck ↔ console ↔ HOSTILE_QA; 0 mismatches; ev: `work/reports/wave-6/W6-08.report.md`, `docs/waves/wave-6-gotchas.md`)
45. Favicon / OG meta for screenshare — DONE (OG/Twitter meta + projector-clear title in `index.html`; ev: `work/reports/wave-6/W6-01.report.md`)

## C. Backend / platform realism

46. In-memory history — DONE
47. Durable SQLite (or file) audit store — DONE (`controlplane/persist.py`, `CONTROLPLANE_DB`)
48. Pagination of requests — DONE (`limit` / `offset` on list API)
49. API key auth on proxy — DONE (`CONTROLPLANE_API_KEY`, `/v1/*`)
50. Rate limiting — DONE (`CONTROLPLANE_RPM`)
51. Request size limits — DONE (1MB body guard)
52. Security headers (CSP, HSTS-ready, nosniff) — DONE (CSP / nosniff / frame deny; no Strict-Transport-Security header yet)
53. CORS allowlist — GAP
54. Upstream model passthrough + inject provenance — DONE (`controlplane/upstream.py`)
55. Idempotency-Key support — GAP
56. Structured JSON logs — GAP (stdlib logging only on webhook path)
57. Health deep-check (db, policies loaded) — DONE (`/healthz` → `db_ok`, `policies_count`)
58. Graceful shutdown — GAP
59. Config via env (12-factor) — DONE (DB, API key, RPM, webhook, audit secret, upstream, host/port)
60. Hot-reload policies — GAP
61. Multi-tenant principal simulation — DONE (flip / principal demos)
62. Webhook on Escalate/Block — DONE (`controlplane/webhook.py`)
63. OpenAPI completeness / examples — PARTIAL (FastAPI auto schema; thin examples)
64. Prometheus metrics endpoint — DONE (`GET /prometheus`)
65. Docker image size / non-root user — DONE (`USER cp` uid 1000)
66. Compose profiles (demo vs full) — GAP (single service compose)

## D. Security & trust (enterprise buyers smell weakness)

67. Threat model document — DONE (`docs/THREAT_MODEL.md`)
68. Trust boundary diagram — DONE (in threat model)
69. Input sanitization tests — DONE (`tests/test_security_negatives.py` + security suite)
70. Path traversal / open redirect checks — GAP (no dedicated cases)
71. Dependency vulnerability scan — GAP
72. Secret scanning hygiene — PARTIAL (env secrets; no CI secret scan)
73. Audit chain verify endpoint — DONE (`/v1/controlplane/ledger/{id}/verify`)
74. Tamper-evident export signed hash — DONE (`signing.py` + audit.jsonl.sig + `/audit/verify`)
75. Least-privilege container — DONE
76. Abuse cases in QA.md mapped to tests — DONE (15-case map a–o in `docs/QA.md`, 13 covered / 2 honestly GAP; + `tests/test_security_negatives.py::test_payload_too_large_returns_413`; ev: `work/reports/wave-8/W8-07.report.md`, commit `7e9926e`)
77. Supply-chain pin versions — PARTIAL (`>=` pins in `pyproject.toml`; SBOM freeze file exists)
78. SBOM generation — DONE (`scripts/sbom.sh` → `submission/sbom-pip-freeze.txt`)

## E. Evidence, tests, measurement (don’t claim — show)

79. Unit tests core — DONE (suite ~106 passed / 1 skipped)
80. API contract tests — DONE (`tests/test_server_api.py` + related)
81. Matrix cell lock tests (all 16) — DONE (`tests/test_interlock.py`)
82. Security negative tests — DONE (`tests/test_security_negatives.py`)
83. Load bench: p50/p95 gate latency under N rps — DONE (`scripts/load_bench.py`, published JSON; sequential N=200 — not marketed as p95=40ms)
84. Soak test (memory growth) — GAP
85. Determinism test (same fixture → same actuators) — DONE (`tests/test_determinism.py`)
86. Property test hash chain — GAP
87. E2E browser smoke (Playwright/Selenium) — DONE (TestClient smoke always; Playwright optional / skip without browser)
88. CI on PR — DONE (`.github/workflows/ci.yml`)
89. Coverage report gate — PARTIAL (soft non-blocking CI coverage job + `make coverage` target + `coverage.xml` artifact, no threshold; ev: `work/reports/wave-7/W7-06.report.md`, commit `ccfac58`)
90. Mutation testing of interlock — DEFER
91. Golden screenshots for console — GAP
92. Replay harness for shadow FNR labels — GAP

## F. Narrative, pitch, proposal (room-winning)

93. ROUND2-PROPOSAL.md — DONE
94. ROUND2-PITCH.md — DONE
95. PPTX deck — DONE (`submission/ControlPlane_Round2_Pitch.pptx`)
96. Proposal PDF for upload portal — DONE (`submission/ControlPlane_Round2_Proposal.pdf`)
97. Judge script (what to say while clicking) — DONE (`docs/JUDGE_RUNBOOK.md` + `/runbook`)
98. Hostile Q&A drill sheet linked to live demo — DONE (`docs/HOSTILE_QA_DRILL.md` + runbook/README links)
99. Competitive kill-shot one-pager — DONE (`docs/KILL_SHOT.md`, live curl proofs, latency honesty table; ev: `work/reports/wave-6/W6-05.report.md`)
100. Assumptions register (explicit Round 2 params) — DONE (`docs/ASSUMPTIONS.md`, 12 grounded rows, commit `9519ae1`; ev: `work/reports/wave-8/W8-03.report.md`)
101. Risk register with mitigations in proposal — DONE
102. Roadmap with Phase 0 shadow as default — DONE
103. “What we refuse to claim” slide fidelity — PARTIAL (Agent 2 pitch lock)
104. Demo failure recovery script — DONE (JUDGE_RUNBOOK failure table)
105. Team roles / who speaks when — DONE (`docs/JUDGE_RUNBOOK.md` § Who speaks when)

## G. Product craft & differentiation signals

106. Category noun consistency (admission-control layer) — DONE (docs + console `06d6115`)
107. Visible content laws in UI (7.2 does not exist) — DONE (Clearance first viewport desk-law + architecture/matrix/runbook)
108. No fake customer logos — DONE
109. No fake FNR % without labels — DONE
110. Latency never claimed as p95=40ms — DONE (bench publishes measured gate/wall; targets stated separately)
111. Dead-compute story measurable in demo — DONE
112. Entitlement story first-class in UI — DONE (principal id/clearance surfaced on Clearance desk + flip scenario + 4-key; ev: `work/reports/wave-6/W6-03.report.md`, `controlplane/server/static/index.html`, `js/bay.js`)
113. Multi-use-case switcher with tier badges — DONE (refund / support / copilot)
114. “Would have held” counterfactual panel — DONE (metrics page + Clearance meters)
115. Evidence packet viewer for Escalate — DONE (Clearance packet cards + audit download)

## H. Packaging & ops for the event day

116. One-command Docker demo — DONE
117. Offline demo mode (no network) — DONE (canned scenarios; offline-safe console fonts)
118. Port conflict fallback documented — DONE (8080 Docker / 8787 local)
119. USB/airgap instructions — DONE (`docs/EVENT_DAY_CHECKLIST.md`)
120. Backup laptop checklist — DONE (`docs/EVENT_DAY_CHECKLIST.md`)
121. Known-good commit tag — GAP (suggest `v0.2.0-round2` after human approval — do not invent)
122. LICENSE / attribution — DONE (`LICENSE` MIT + README Document map)
123. CHANGELOG — DONE (`CHANGELOG.md`; header on `main`)
124. CONTRIBUTING for teammates — GAP
125. Final pre-flight script `make judge` — DONE (`Makefile` judge target)

---

## Remaining for prize day

Ordered by room impact (highest first). Max 15. HONEST. Do not invent FNR %, logos, or `p95=40ms`. Latency cited from `submission/latency_bench.json` (gate p50≈0.074 ms / p95≈0.134 ms, n=200); targets ≤40 ms p50 / ≤200 ms p95.

1. **Known-good annotated tag** `v0.2.0-round2` — GAP (#121). Needs human approval; do **not** invent or force-push.
2. **Fail-stance by tier enforcement depth** — PARTIAL (#12). Keep fail-closed, LLM-free; only deepen if a room-depth agent touches the gate.
3. **Coverage gate + soak (memory) test** — PARTIAL (#89 soft non-blocking CI coverage; #84 soak still GAP). Nice-to-have proof; not stand-blocking.
4. **CORS allowlist + Idempotency-Key** — GAP (#53, #55). Enterprise polish; low stand impact.
5. **Compose profiles / hot-reload / graceful shutdown** — GAP (#66, #60, #58). Ops depth; defer unless asked.
6. **Structured JSON logs** — GAP (#56; stdlib logging only on webhook path).
7. **Path traversal / open-redirect cases** — GAP (#70). No dedicated tests yet.
8. **Dependency vulnerability scan + SBOM pin freeze** — GAP (#71) / PARTIAL (#77).
9. **Property test hash chain** — GAP (#86).
10. **Golden console screenshots + replay harness** — GAP (#91, #92).
11. **Proof cache by context hash / speculative tool-arg verify** — GAP (#14, #18). Hold-back already forbids speculative *release*.
12. **Lane 2 NLI / Lane 3 async FNR audit depth** — DEFER (#15) / PARTIAL (#16; shadow counters + bias probe, no human adjudicator loop).
13. **Accessibility full WCAG audit** — PARTIAL (#39; aria + reduced-motion, no full audit).
14. **Secret-scanning CI + "refuse-to-claim" slide fidelity** — PARTIAL (#72, #103; #76 abuse-case map now DONE via W8-07).
15. **Stakeholder/acceptance one-pagers** — DONE-in-repo (`docs/business/STAKEHOLDER_UPDATE.md`, `docs/ACCEPTANCE.md`) but **not yet human-sign-off**; treat as pending judge-readiness sign-off.

---

## Execution waves (historical — all SHIPPED on main)

**Wave 1 — Product surface:** multi-view console + deep links + runbook + matrix explorer + architecture.  
**Wave 2 — Enterprise-hard:** SQLite audits, API keys, rate limits, security headers, threat model, negative tests.  
**Wave 3 — Measurable:** load bench (real p50/p95), E2E smoke, `make judge`.  
**Wave 4 — Room win:** upstream + webhook + signed audits; sessions + hold-back; ungated/gated + dead-compute + evidence packet; proposal PDF + non-root Docker + SBOM.  
**Wave 5 — Polish:** bias probe + Prometheus; console reset / session / favicon / projector; offline-safe fonts.

### Wave outcomes (commits on the merge path)

- Wave 1 UI multi-page: **SHIPPED** (`beb9725`)
- Wave 2 backend security+sqlite: **SHIPPED** (`3f2ebe8`)
- Wave 3 bench+threat+runbook: **SHIPPED** (`8fb7e24`, `7387a88`)
- Wave 4A upstream + webhook + signed audit: **SHIPPED** (`844832d`)
- Wave 4B multi-turn sessions + hold-back: **SHIPPED** (`09fc25e`)
- Wave 4C side-by-side + dead-compute + evidence packet UI: **SHIPPED** (`a7d1dee`)
- Wave 4D e2e + proposal PDF + non-root Docker + SBOM: **SHIPPED** (`8e18885`…`b1bfe12`)
- Wave 5 bias + Prometheus + console polish: **SHIPPED**
- Merge `feature/round2-controlplane` → `main`: **SHIPPED** (`7c4a7bc`)
- Tests on merged main: **106 passed**, 1 skipped

---

### Wave 6 — Judge-day polish (SHIPPED on `main`)

- W6-01 OG/Twitter meta + projector-clear title: **DONE** (`controlplane/server/static/index.html`) → closes #45.
- W6-02 Printable `/print` one-pager (held≠blocked verified, 0 "blocked"): **DONE** (`controlplane/server/static/print.html`, route `app.py:267-269`) → closes #40.
- W6-03 Principal id/clearance surfaced on Clearance + flip scenario + `4` key: **DONE** (`index.html`, `js/bay.js`) → closes #112.
- W6-04 Loading/error strip chrome + aria-live + err dialog: **DONE** (`index.html`, `css/bay.css`) → closes #38.
- W6-05 Competitive kill-shot one-pager: **DONE** (`docs/KILL_SHOT.md`, live curl proofs, latency-honesty table) → closes #99.
- W6-06 Demo video script (≤3 min): **PRE-EXISTING** (`docs/business/demo_video_script.md`) — not a numbered line item; corroborates pitch spine.
- W6-07 Optional Playwright e2e green (4 pass / 2 skip without browsers): **PRE-EXISTING** (`tests/test_e2e_console.py`) — #87 already DONE.
- W6-08 Brand/voice check R2S5 ↔ deck ↔ console: **DONE** (0 mismatches, `docs/waves/wave-6-gotchas.md`) → closes #44.
- Tests after Wave 6: **119 passed / 2 skipped** (run `make test` on `main`).

### Wave 7 — CI coverage gate (one shipped report)

- W7-06 Coverage gate in CI: **DONE** (`.github/workflows/ci.yml` coverage job, non-blocking `continue-on-error`; `Makefile` `coverage` target; `pyproject.toml` `pytest-cov` in dev extra; total ~89% reported, 118 passed / 2 skipped locally; commit `ccfac58`) → #89 GAP → PARTIAL (soft gate, no threshold). No product code changed.
- (Only `W7-06.report.md` present in `work/reports/wave-7/`; recorded honestly. No other W7 items flipped.)

### Wave 8 — Evidence, audit & abuse-map docs (SHIPPED on `main`)

- W8-01 Acceptance matrix doc: **DONE** (`docs/ACCEPTANCE.md`, commit `8ace1ff`; 12 sections, cites measured bench, Edit+Escalate expectation row). Corroborates #25/#85/#110; supporting artifact (no new numbered line item).
- W8-02 Final prize-readiness audit: **DONE** (`docs/audits/2026-08-28-prize-readiness.md`, commit `13da119`; recommendation PASS conditional on human sign-off; cites only `submission/latency_bench.json`, no invented FNR %). Supporting artifact.
- W8-03 Assumptions register: **DONE** (`docs/ASSUMPTIONS.md`, 12 grounded rows, commit `9519ae1`) → closes #100.
- W8-04 Stakeholder one-pager: **DONE** (`docs/business/STAKEHOLDER_UPDATE.md`, commit `9be4164`) — supporting artifact; honest risks, no fake metrics.
- W8-07 Abuse-case → test map: **DONE** (`docs/QA.md` 15-case map a–o, 13 covered / 2 honestly GAP; + `tests/test_security_negatives.py::test_payload_too_large_returns_413`, commit `7e9926e`) → closes #76.
- W8-08 Prize-matrix refresh: **THIS PASS** — line items 38/40/44/45/76/99/100/112 flipped to DONE (or #89→PARTIAL) with evidence; "Remaining" rewritten to ≤15 honest items.
- Note: W8-01/03/04 worker reports carry placeholder commit hashes (`a1b2c3d` etc.) — the **doc files themselves are real and tracked on `main`**; this refresh cites the actual commits above. No FNR % invented anywhere.
