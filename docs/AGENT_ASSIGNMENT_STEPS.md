# Agent assignment steps — portal 100 + prize ~99

**Repo:** https://github.com/Srujan0798/controlplane-ai (`main` only — never push a second branch)  
**Local:** `/Users/srujansai/Desktop/SEBI`  
**Full prompt text:** `docs/BRUTAL_AGENT_PROMPTS.md`  
**Laws:** `docs/EXCELLENCE_GATE.md` · Portal: `docs/SUBMIT.md`

---

## Universal header (paste on EVERY agent)

```
You are in /Users/srujansai/Desktop/SEBI.
Public GitHub is https://github.com/Srujan0798/controlplane-ai — main ONLY. Do not create/push feature branches.
Read docs/EXCELLENCE_GATE.md §0 and docs/SUBMIT.md before anything else.
DONE forbidden without pasted command evidence. pytest alone ≠ DONE.
Frozen: ARCHITECTURE.md, interlock MATRIX, Actuator/BlastTier, AGENTS.md.
Refund language: held/escalated with evidence packet — never "blocked".
Never quote 40ms as p95. PDF/PPTX/README/video numbers must match make eval / make bench.
If partial: REJECT-SELF with missing YES rows.
Report: DONE|REJECT-SELF · SHA · commands+output · concerns.
Push/sync only to origin main when done.
```

---

## STEP 1 — Brutal reviewer (1 agent, no code)

**Paste:**

```
[UNIVERSAL HEADER]

ROLE: Hostile Round-2 judge + portal auditor. NO CODE EDITS.

Read docs/BRUTAL_AGENT_PROMPTS.md section A and execute it fully.

Write: work/reports/brutal-review.md
Score each portal field /20 (GitHub, video, README PDF, proposal PDF, PPTX) = /100.
Top 10 face-hitting failures. Exact fix order. "Would I advance this team?" Yes/No.
No praise. No soft middle.
```

**Wait for:** `work/reports/brutal-review.md`

---

## STEP 2 — Verification executioner (1 agent)

**Paste:**

```
[UNIVERSAL HEADER]

ROLE: Verification executioner. Prove or kill claims. Prefer no feature work.

Read docs/BRUTAL_AGENT_PROMPTS.md section B and execute every check.
Write: work/reports/verify-gate.md
Final line must be exactly: VERIFY_PASS or VERIFY_FAIL
```

**Wait for:** `VERIFY_PASS` (if FAIL, fix with Step 6 first or assign C6 early)

---

## STEP 3 — Parallel fix swarm (3 agents at once)

### Agent 3A — Video (C1) — highest priority

```
[UNIVERSAL HEADER]

Execute docs/BRUTAL_AGENT_PROMPTS.md section C1 (Video that can win the room).
Owns: docs/VIDEO_SCRIPT.md, scripts/record_prototype_video.py, submission/ControlPlane_Round2_Prototype.mp4
Target 3:30–4:00, 1080p, live /gate, Edit+Escalate held, voiceover preferred.
Commit and sync to main only.
```

### Agent 3B — Eval honesty (C4)

```
[UNIVERSAL HEADER]

Execute docs/BRUTAL_AGENT_PROMPTS.md section C4 (Eval honesty).
Owns: evals/**, controlplane/shadow.py (wiring only), tests/test_evals.py, docs/HOSTILE_QA_DRILL.md (new Qs only)
Kill fake-perfect FNR=0 story OR document hard negatives + honesty bound.
make eval + make verify green. Sync to main only.
```

### Agent 3C — GitHub face-lift (C5)

```
[UNIVERSAL HEADER]

Execute docs/BRUTAL_AGENT_PROMPTS.md section C5 (Public repo face-lift).
Owns: README.md, docs/SUBMIT.md, optionally move/label TASKS.md+tasks/ as internal under docs/reference/
Remote branches must stay: main only.
Sync to main only.
```

**Wait for:** all three DONE or REJECT-SELF reports

---

## STEP 4 — Artifacts after number freeze (2 agents, after 3B)

### Agent 4A — README PDF (C2)

```
[UNIVERSAL HEADER]

Execute docs/BRUTAL_AGENT_PROMPTS.md section C2.
Owns: scripts/build_readme_pdf.py, submission/ControlPlane_Round2_README.pdf
Clean-clone 60s path + capability ledger + real numbers. make verify green. Sync main.
```

### Agent 4B — Proposal PDF + PPTX (C3)

```
[UNIVERSAL HEADER]

Execute docs/BRUTAL_AGENT_PROMPTS.md section C3.
Owns: scripts/build_proposal_pdf.py, round2/CONTROLPLANE_R2_FINAL.md (numbers only),
submission/ControlPlane_Round2_Proposal.pdf, submission/ControlPlane_Round2_Pitch.js,
submission/ControlPlane_Round2_Pitch.pptx
Seven rubric sections + FNR CI + honesty. Content laws green. make verify green. Sync main.
```

---

## STEP 5 — Mechanism regression hunter (1 agent)

```
[UNIVERSAL HEADER]

Execute docs/BRUTAL_AGENT_PROMPTS.md section C6.
Prove: no fixture demo path, override route live, amount numeric, multiturn demo, content laws.
Add regression tests. pytest -q green. Sync main.
```

---

## STEP 6 — Final orchestrator (1 agent)

```
[UNIVERSAL HEADER]

Execute docs/BRUTAL_AGENT_PROMPTS.md section D.
Read work/reports/brutal-review.md + verify-gate.md + all C* reports.
Update docs/EXCELLENCE_GATE.md §1–§2 YES/NO to today's truth with commands.
Re-run make verify; paste output.
ONLY if every portal field ≥18/20 AND VERIFY_PASS:
  print SUBMIT and the five upload paths + GitHub URL.
Else: print DO_NOT_SUBMIT and the remaining NO rows.
Never say "100/100 perfect product". Max: "portal-complete + honest prototype".
```

---

## STEP 7 — You (human) only

1. Open https://github.com/Srujan0798/controlplane-ai — confirm one branch, README OK  
2. Play `submission/ControlPlane_Round2_Prototype.mp4` once  
3. Open the three PDFs/PPTX once  
4. If Step 6 said **SUBMIT**, upload:

| Field | File / URL |
|---|---|
| GitHub | https://github.com/Srujan0798/controlplane-ai |
| Video | `submission/ControlPlane_Round2_Prototype.mp4` |
| README PDF | `submission/ControlPlane_Round2_README.pdf` |
| Proposal PDF | `submission/ControlPlane_Round2_Proposal.pdf` |
| Pitch PPTX | `submission/ControlPlane_Round2_Pitch.pptx` |

---

## Quick map

| Step | Agents | Parallel? |
|---|---|---|
| 1 Review | 1 | alone |
| 2 Verify | 1 | alone |
| 3 Fix | 3 (video, eval, GitHub) | **yes** |
| 4 PDFs | 2 (README PDF, proposal+deck) | **yes** after 3B |
| 5 Regression | 1 | alone |
| 6 Final gate | 1 | alone |
| 7 Human submit | you | — |

**Total agent seats:** ~9 turns (or 6 people if 3A/3B/3C run together).
