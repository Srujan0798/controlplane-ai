# Brutal agent prompts — hit 100/100 excellence (not “pytest green”)

**Repo:** https://github.com/Srujan0798/controlplane-ai (`main` only)  
**Local:** `/Users/srujansai/Desktop/SEBI` · prefer commit on `main` after sync; do **not** recreate `feature/round2-elevation` on GitHub  
**Law:** `docs/EXCELLENCE_GATE.md` · Portal: `docs/SUBMIT.md` · Design: `docs/superpowers/specs/2026-08-29-round2-100-design.md`

**Owner expectation:** Face-hitting review. Dummy DONE = reject. Soft language = reject.  
**Score ceiling:** Design says ~99 + honesty. Claiming “100% perfect product” = REJECT.

---

## 0. Paste this header on EVERY agent

```
You are on /Users/srujansai/Desktop/SEBI. Public repo is https://github.com/Srujan0798/controlplane-ai (main ONLY).

Read first:
- docs/EXCELLENCE_GATE.md §0 (DONE definition)
- docs/SUBMIT.md (five portal fields)
- docs/BRUTAL_AGENT_PROMPTS.md (this file) for YOUR role only

Rules:
- DONE forbidden without pasted command output for every acceptance bullet.
- pytest alone ≠ DONE. TestClient/curl for every HTTP route you touch.
- Frozen: docs/ARCHITECTURE.md, controlplane/interlock.py MATRIX, Actuator/BlastTier enums, AGENTS.md.
- Refund language: held / escalated with evidence packet — NEVER "blocked".
- Never quote 40ms as p95. Numbers in PDF/PPTX/README/video must match make eval / make bench.
- Do not push a second branch to GitHub. Work on main (or local elevation then push to main only).
- If partial: reply REJECT-SELF with missing YES rows. Do not claim DONE.
- Report: DONE|REJECT-SELF · SHA · commands+output · concerns.
```

---

## A. BRUTAL REVIEWER (run FIRST — no code edits)

**Give agent this:**

```
ROLE: Hostile Accenture Round-2 judge + submission-form auditor.
NO CODE EDITS. Read-only. Be brutal. Assume the team is lying until proven otherwise.

Read: docs/SUBMIT.md, docs/EXCELLENCE_GATE.md, README.md, submission/*, docs/ARCHITECTURE.md §10,
round2/CONTROLPLANE_R2_FINAL.md (skim), docs/HOSTILE_QA_DRILL.md.

SCORE each portal field 0–20 (sum /100). Sub-scores MUST cite evidence (file path, URL, command).

### Portal scoring rubric (100 points)

1) Public GitHub (20)
- URL opens public? Single branch? README renders five portal fields?
- Clone + pip install -e ".[dev]" + preflight + make run actually works from clean clone notes?
- CI green on main? Secrets absent? .env.example placeholders only?
- Agent shards / TASKS mess / dirty WIP visible to judges? Deduct hard.

2) Prototype video (20)
- File exists, plays, 1080p-ish, length credible (~3–4 min target)?
- Shows LIVE system (gate/demo), NOT slide narration?
- Amount numeric / clause 7.2 absence / Edit+Escalate held visible?
- Says or implies "blocked" for refund? Automatic fail for that beat.
- Silent title-card spam with weak live proof = max 8/20.

3) README PDF (20)
- ≤20MB; separate from proposal; capability ledger (implemented vs designed)?
- Every command in it works from clean clone?
- Numbers match make eval / latency_bench.json (run make verify)?
- Drift / wrong p95 / missing FNR CI = fail.

4) Proposal PDF (20)
- Seven brief asks present and titled (problem, solution, users, business, impact, roadmap, risks)?
- Measured eval table + published FNR with Wilson CI + honesty that corpus is self-authored?
- Content laws on extracted text green?
- Marketing claims without command provenance = fail.

5) Pitch PPTX (20)
- Rebuilt from JS source; same number freeze as PDF?
- Content laws on extracted text?
- Speaks held≠blocked; publishes miss rate; no fake customer logos / invented FNR?

Also score MECHANISM trust (separate 0–100 comment, not portal sum):
- fixture_map in demo path?
- CONTRADICTED / UNKNOWN live?
- override route registered?
- analyze on arbitrary text?
- FNR=0% looks fraudulent without hard-negatives story?

OUTPUT (markdown file work/reports/brutal-review-YYYYMMDD.md):
1. Portal score /100 with 5 sub-scores + evidence
2. Top 10 face-hitting failures ranked by judge damage
3. Exact fix order for implementer agents (R1, R2, …) with Owns files
4. One paragraph: "Would I advance this team?" Yes/No + why
5. Forbidden praise. No "overall looks good".
```

---

## B. VERIFICATION AGENT (run SECOND — prove green or fail)

```
ROLE: Verification executioner. You do not improve features; you prove or kill claims.

Run and PASTE full tails:
1) git status -sb   # must be clean or list every dirty path as FAIL
2) git branch -a; gh api repos/Srujan0798/controlplane-ai/branches --jq '.[].name'
   # remote MUST be only main — if feature/* exists on origin, FAIL
3) pytest -q                    # 0 failed; no --ignore
4) pytest -q tests/test_content_laws.py
5) make eval                    # paste FNR/FPR + Wilson CI
6) make verify                  # must print ALL GREEN
7) Smokes (TestClient or curl):
   - refund: Edit + Escalate; amount method contains numeric not fixture
   - POST /v1/controlplane/analyze on ungated clause 7.2 text
   - POST /v1/controlplane/decisions/issue_refund/override → 200
   - GET /gate → 200
   - python3 examples/multiturn_demo.py
   - python3 examples/refund_trace_demo.py
8) Artifact existence + sizes:
   submission/ControlPlane_Round2_{Prototype.mp4,README.pdf,Proposal.pdf,Pitch.pptx}
9) Number freeze: every number in README PDF / Proposal / PPTX text must appear in
   evals/last_run.json or submission/latency_bench.json — else FAIL with the drift lines.
10) curl -sI https://github.com/Srujan0798/controlplane-ai → 200; visibility PUBLIC

Write work/reports/verify-gate-YYYYMMDD.md with a YES/NO table.
Exit status: VERIFY_PASS or VERIFY_FAIL. No soft middle.
```

---

## C. IMPLEMENTER SWARM (after A+B — one agent per prompt)

### C1 — Video that can win the room (highest judge damage)

```
HEADER from §0.
TASK: Rebuild prototype video to excellence. Current silent title-card capture is NOT enough.

Owns: docs/VIDEO_SCRIPT.md, scripts/record_prototype_video.py,
submission/ControlPlane_Round2_Prototype.mp4 (and recorder helpers only).

Acceptance (all required):
1) 1920×1080 mp4, target 3:30–4:00 (hard floor 3:00).
2) Live /gate: paste ungated refund text, Run gate, show claims/bindings/actuators on screen.
3) On-screen text must show issue_refund → Escalate (held) and show_text → Edit.
4) Show symbol/absence of 7.2 OR binding rationale visible.
5) Show make eval FNR line with CI (terminal or on-screen card with REAL numbers from last_run.json).
6) Never display the word "blocked" for the refund.
7) Prefer voiceover track muxed per VIDEO_SCRIPT (even TTS) — silent-only = REJECT-SELF unless you document portal allows silent AND live proof is overwhelming.
8) Commit on main; do not create remote feature branches.

Verify: ffprobe duration; file size; manual checklist in report with screenshots or frame grabs.
```

### C2 — README PDF that survives clean-clone day

```
HEADER from §0.
TASK: Rebuild submission/ControlPlane_Round2_README.pdf so a stranger can run us in 60 seconds.

Owns: scripts/build_readme_pdf.py, submission/ControlPlane_Round2_README.pdf, docs/SUBMIT.md (only if needed).

Acceptance:
1) Capability ledger: each mechanism marked implemented+tested / prototype / designed-not-built — honest.
2) Commands: venv, pip install -e ".[dev]", preflight, make run, /gate, refund autorun, make eval, make verify.
3) Every number quoted = from make eval / latency_bench.json after regeneration.
4) make verify green after your rebuild.
5) Mentions public URL https://github.com/Srujan0798/controlplane-ai and five portal files.
6) ≤20MB.
```

### C3 — Proposal PDF + pitch PPTX number freeze

```
HEADER from §0.
TASK: Rebuild proposal PDF and PPTX against measured numbers only.

Owns: scripts/build_proposal_pdf.py, round2/CONTROLPLANE_R2_FINAL.md (numbers sections only — no architecture rewrite),
submission/ControlPlane_Round2_Proposal.pdf,
submission/ControlPlane_Round2_Pitch.js, submission/ControlPlane_Round2_Pitch.pptx.

Acceptance:
1) Seven brief rubric sections present and titled.
2) Eval table + published FNR with Wilson CI + explicit "self-authored corpus" honesty.
3) Dead compute / bench methodology cited; never 40ms as p95.
4) held ≠ blocked everywhere (content laws green on extracted PDF+PPTX text).
5) make verify green (number diff).
6) PPTX built from JS source so deck cannot drift from proposal numbers.
```

### C4 — Eval honesty (kill the fake-perfect FNR)

```
HEADER from §0.
TASK: Make published FNR intellectually honest. FNR=0.0% with no miss story will get us destroyed in Q&A.

Owns: evals/cases/**, evals/run.py or evals/harness.py, evals/README.md, controlplane/shadow.py (wiring only),
tests/test_evals.py.

Acceptance:
1) ≥20% hard negatives labeled and documented in evals/README.md.
2) At least one stratum where we miss or abstain honestly OR a clear written bound: "on this corpus FNR=X (CI); production unknown".
3) Derived-route garbage metrics fixed or explained in README (no silent precision=0).
4) /v1/controlplane/metrics shows published_fnr from last_run after make eval (source=eval-corpus).
5) Hostile one-pager answers added to docs/HOSTILE_QA_DRILL.md: "your corpus is self-authored", "Wilson CI is wide", "BM25 thresholds are magic" — drilled answers.
6) make eval + make verify green.
```

### C5 — Public repo face-lift (judge opens link in 10 seconds)

```
HEADER from §0.
TASK: Make the GitHub landing page look like a finished submission, not an agent scrapyard.

Owns: README.md, docs/SUBMIT.md, .gitignore (only), optionally hide/archive noise via docs/reference only.
FORBIDDEN: deleting architecture canon; do not reopen MATRIX.

Acceptance:
1) Remote branches: ONLY main (gh api branches).
2) README opens with five portal fields + run in 60s + expected Edit/Escalate.
3) No broken links; SUBMIT.md matches README.
4) TASKS.md / tasks/ either clearly labeled "internal engineering board" at top OR moved under docs/reference/ — judges must not think the product is unfinished because of agent prompts.
5) Push to main only.
6) curl GitHub 200; visibility PUBLIC.
```

### C6 — Mechanism regression hunter

```
HEADER from §0.
TASK: Find and fix silent demo lies.

Owns: only files needed for proven regressions (prefer tests + minimal prod fix).
Must re-check:
- grep fixture_map in demo paths (refund/pipeline enforce)
- override route not nested inside analyze
- amount binding method
- content laws
- multiturn demo

Write tests that FAIL if regressions return.
pytest -q green. Push main only.
```

---

## D. FINAL ORCHESTRATOR PROMPT (you run this last)

```
Merge reports from Brutal Reviewer + Verification + C1–C6.
Update docs/EXCELLENCE_GATE.md §1–§2 YES/NO to TODAY's truth with commands.
If any portal field <18/20 or VERIFY_FAIL → do NOT tell the human to submit.
If all portal ≥18/20 and VERIFY_PASS → say SUBMIT with the five upload paths and GitHub URL.
Never say 100/100 product. Max allowed: "portal-complete + honest prototype."
```

---

## E. How you (human) dispatch

1. Agent **A** (brutal review) → read `work/reports/brutal-review-*.md`  
2. Agent **B** (verify) → read `work/reports/verify-gate-*.md`  
3. Parallel implementers **C1–C5** (C1 video + C4 eval honesty first)  
4. Agent **C6** after they land  
5. Agent **D** final gate  

**Parallel-safe:** C1 ∥ C4 ∥ C5 (different Owns).  
**Serial:** C2/C3 after C4 numbers freeze; D last.

---

## F. Instant reject phrases from agents

If an agent says any of these without evidence, send them back:

- “tests pass so we’re done”
- “committed”
- “looks good overall”
- “should be fine for judges”
- “100/100”
- “pytest --ignore=…”
- “blocked the refund”
