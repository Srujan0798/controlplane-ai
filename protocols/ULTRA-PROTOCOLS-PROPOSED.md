# Ultra protocols — propose for Core `protocols/`

These showed up as load-bearing in ControlPlane parallel elevation. Core already has blast-radius, oap-security, route-sentinel, sdlc-loop, verification.

## P-06 — File ownership / writes-forbid (extends FM-13)
**Problem:** Parallel workers collide (`file 2.md`, silent overwrite).  
**Protocol:** Every task file MUST declare `writes:` and `forbid:` path lists. Orchestrator publishes a **parallel map** (batches). Same file → serialize or worktree.  
**Evidence:** task brief contains both lists; merge rejects commits touching forbid paths (validator proposal).

## P-07 — Master paste + task pointer
**Problem:** Humans re-explain complex OS to every agent → thrash.  
**Protocol:** One `work/WORKER_PROMPT.md` (≤15 laws). Worker paste = that file + **one** task path. No chat history required.  
**Evidence:** report cites task id + commit.

## P-08 — Confidence ≠ completeness (acceptance matrix)
**Problem:** Team feels “1% done” while deliverables are shipped — or reverse.  
**Protocol:** Wave-close requires `docs/ACCEPTANCE.md` (or project equivalent): SHA + exact commands + expected outputs. Feeling is not a status.  
**Evidence:** acceptance checkboxes with pasted command output.

## P-09 — Domain invariants block (AGENTS.md §)
**Problem:** Competition/product laws (content laws, fail-closed, “never say blocked”) get lost across agents.  
**Protocol:** AGENTS.md must have a frozen **Domain invariants** section (project-specific), separate from stack. Workers cannot “improve” invariants.  
**Evidence:** report affirms invariants; CI/doc lint optional.

## P-10 — Report merge / EXECUTION drift gate
**Problem:** Tasks complete but `plan/EXECUTION.md` stays “READY TO DISPATCH”.  
**Protocol:** After each wave, orchestrator-only task updates EXECUTION + HANDOFF rewrite. Validator: no SHIPPED row without commit hash (exists as idea in Lite validate_execution.sh — **wire as real validator**).  
**Evidence:** EXECUTION row hash matches `git log`.

## P-11 — Evidence pack wave (prize/ship close)
**Problem:** Product waves finish without audit/hostile-Q/runbook/tag recipe.  
**Protocol:** Final wave is always evidence: acceptance, audit, assumptions, kill-shot, event checklist, tag recipe (human creates tag).  
**Evidence:** `docs/audits/YYYY-MM-DD-*.md` PASS.

## P-12 — Dupe artifact quarantine
**Problem:** Agents write `foo 2.md` beside `foo.md`.  
**Protocol:** preflight fails on `* [0-9].md` / `* 2.*` in tracked trees; orchestrator deletes or attic’s them before merge.  
**Evidence:** preflight clean.
