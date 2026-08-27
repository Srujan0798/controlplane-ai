# Prize-win matrix — ControlPlane Round 2

Honest inventory. What we have vs what first-prize teams actually need.
Branch: `feature/round2-controlplane` only. **Do not merge until human says so.**

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
11. Shadow vs enforce modes — PARTIAL (metrics exist; UI thin)
12. Fail stance by tier — PARTIAL (in policy YAML, not enforced in gate)
13. Hold-back buffer / streaming gate — GAP
14. Proof cache by context hash — GAP
15. Lane 2 NLI (off critical path) — DEFER
16. Lane 3 async FNR audit loop — PARTIAL (counters only)
17. Multi-turn compounding risk / session parent ledger — GAP
18. Speculative verification of tool args — GAP
19. Dead-compute economist view in UI — GAP
20. Bias measurement surface (responsibility axis) — GAP
21. Architecture interactive diagram for judges — GAP
22. Matrix explorer (click cell → example) — GAP
23. Versioned policy DAG engine (not just YAML packs) — PARTIAL
24. Shadow dual-emit counterfactual export CSV — GAP
25. Published latency targets with real bench numbers — GAP

## B. Prototype surface (judges must touch it)

26. OpenAI-compatible `/v1/chat/completions` — DONE
27. Demo scenarios API — DONE
28. Judge console UI — PARTIAL (one page; needs multi-view product)
29. Policies page — GAP
30. Metrics / FNR cockpit — GAP
31. Audit explorer (search past requests) — GAP
32. Interactive matrix page — GAP
33. Architecture story page — GAP
34. 60-second judge runbook page — GAP
35. Keyboard shortcuts (Admit, scenario switch) — GAP
36. Deep-linkable demo URL `?scenario=refund&mode=enforce&autorun=1` — GAP
37. Mobile / projector layout — PARTIAL
38. Empty / loading / error states — PARTIAL
39. Accessibility (focus, contrast, reduced motion) — PARTIAL
40. Printable one-pager from console — GAP
41. Demo “reset room” button — GAP
42. Side-by-side ungated vs gated text — GAP
43. Soundless “flap” polish + microcopy — PARTIAL
44. Brand consistency with pitch deck — PARTIAL
45. Favicon / OG meta for screenshare — GAP

## C. Backend / platform realism

46. In-memory history — DONE (volatile)
47. Durable SQLite (or file) audit store — GAP
48. Pagination of requests — GAP
49. API key auth on proxy — GAP
50. Rate limiting — GAP
51. Request size limits — GAP
52. Security headers (CSP, HSTS-ready, nosniff) — GAP
53. CORS allowlist — GAP
54. Upstream model passthrough + inject provenance — GAP
55. Idempotency-Key support — GAP
56. Structured JSON logs — GAP
57. Health deep-check (db, policies loaded) — PARTIAL
58. Graceful shutdown — GAP
59. Config via env (12-factor) — PARTIAL
60. Hot-reload policies — GAP
61. Multi-tenant principal simulation — PARTIAL
62. Webhook on Escalate/Block — GAP
63. OpenAPI completeness / examples — PARTIAL
64. Prometheus metrics endpoint — GAP
65. Docker image size / non-root user — PARTIAL
66. Compose profiles (demo vs full) — GAP

## D. Security & trust (enterprise buyers smell weakness)

67. Threat model document — GAP
68. Trust boundary diagram — GAP
69. Input sanitization tests — GAP
70. Path traversal / open redirect checks — GAP
71. Dependency vulnerability scan — GAP
72. Secret scanning hygiene — PARTIAL
73. Audit chain verify endpoint — GAP
74. Tamper-evident export signed hash — GAP
75. Least-privilege container — GAP
76. Abuse cases in QA.md mapped to tests — PARTIAL
77. Supply-chain pin versions — PARTIAL
78. SBOM generation — GAP

## E. Evidence, tests, measurement (don’t claim — show)

79. Unit tests core — DONE (~42)
80. API contract tests — PARTIAL
81. Matrix cell lock tests (all 16) — DONE-ish (interlock tests)
82. Security negative tests — GAP
83. Load bench: p50/p95 gate latency under N rps — GAP
84. Soak test (memory growth) — GAP
85. Determinism test (same fixture → same actuators) — PARTIAL
86. Property test hash chain — GAP
87. E2E browser smoke (Playwright/Selenium) — GAP
88. CI on PR — DONE (workflow file)
89. Coverage report gate — GAP
90. Mutation testing of interlock — DEFER
91. Golden screenshots for console — GAP
92. Replay harness for shadow FNR labels — GAP

## F. Narrative, pitch, proposal (room-winning)

93. ROUND2-PROPOSAL.md — DONE
94. ROUND2-PITCH.md — DONE
95. PPTX deck — DONE
96. Proposal PDF for upload portal — GAP
97. Judge script (what to say while clicking) — GAP
98. Hostile Q&A drill sheet linked to live demo — PARTIAL (QA.md exists)
99. Competitive kill-shot one-pager — GAP
100. Assumptions register (explicit Round 2 params) — PARTIAL
101. Risk register with mitigations in proposal — DONE-ish
102. Roadmap with Phase 0 shadow as default — DONE
103. “What we refuse to claim” slide fidelity — PARTIAL
104. Demo failure recovery script — GAP
105. Team roles / who speaks when — GAP

## G. Product craft & differentiation signals

106. Category noun consistency (admission-control layer) — PARTIAL
107. Visible content laws in UI (7.2 does not exist) — PARTIAL
108. No fake customer logos — DONE
109. No fake FNR % without labels — DONE
110. Latency never claimed as p95=40ms — PARTIAL (need bench)
111. Dead-compute story measurable in demo — GAP
112. Entitlement story first-class in UI — PARTIAL
113. Multi-use-case switcher with tier badges — PARTIAL
114. “Would have held” counterfactual panel — GAP
115. Evidence packet viewer for Escalate — GAP

## H. Packaging & ops for the event day

116. One-command Docker demo — DONE
117. Offline demo mode (no network) — DONE
118. Port conflict fallback documented — DONE
119. USB/airgap instructions — GAP
120. Backup laptop checklist — GAP
121. Known-good commit tag — GAP
122. LICENSE / attribution — GAP
123. CHANGELOG — GAP
124. CONTRIBUTING for teammates — GAP
125. Final pre-flight script `make judge` — GAP

---

## Execution waves (this session)

**Wave 1 — Make it a product, not a page:** multi-view console + deep links + runbook + matrix explorer + architecture view.  
**Wave 2 — Make it enterprise-hard:** SQLite audits, API keys, rate limits, security headers, threat model, negative tests.  
**Wave 3 — Make claims measurable:** load bench publishing real p50/p95, E2E smoke, coverage, `make judge`.  
**Wave 4 — Make the room win:** judge script, side-by-side ungated/gated, evidence packet UI, proposal PDF, tag release.

Anything not in Wave 1–3 stays listed so we never pretend it shipped.

## Session progress (auto)

Wave 1 UI multi-page: **SHIPPED** (`beb9725`) — Clearance/Policies/Metrics/Audit/Matrix/Architecture/Runbook.  
Wave 2 backend security+sqlite: **SHIPPED** (`3f2ebe8`).  
Wave 3 bench+threat+runbook: **SHIPPED** (`8fb7e24`, `7387a88`) — gate p50≈0.05ms p95≈0.17ms on N=200.  
Pretty routes + nav: **this commit**.

Still open from the 125: upstream passthrough, multi-turn ledger, hold-back buffer, Playwright E2E, proposal PDF, SBOM, webhook escalations, Lane 2 NLI.

## Wave 4 (SHIPPED — parallel agents)

- 4A upstream + webhook + signed audit
- 4B multi-turn session + hold-back
- 4C side-by-side ungated/gated + dead-compute + evidence packet UI
- 4D e2e smoke + proposal PDF + non-root docker + SBOM
- Monitor: healthz + pytest every 3 min

### Wave 4 outcomes
- Upstream hook + escalate webhook + signed audits (`844832d`)
- Multi-turn sessions + hold-back (`09fc25e`)
- Side-by-side ungated/gated + dead-compute + evidence packet UI (`a7d1dee`)
- E2E smoke + proposal PDF + non-root Docker + SBOM (`8e18885`…`b1bfe12`)
- Tests: **89 passed**, 1 skipped (Playwright optional)
