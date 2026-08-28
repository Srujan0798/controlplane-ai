# Kernel — Anti-Hallucination Rules

> Always loaded. These exist because each one maps to a REAL failure observed across past projects (rfq2boq, swa-erp, DRO-FairML). The full root-cause analysis is in `failure-modes/`. These are the always-on guardrails.

## Before you claim anything
- **Ran ≠ guessed.** Before "tests pass," run them and paste the exit code. Before "the file does X," read it. Before "X is done," show the artifact.
- **This session ≠ memory.** Any number, status, or fact you state must be computed/verified THIS session, or explicitly marked "(from earlier, re-verify)".
- **A file you name must exist.** Before referencing `path/to/x`, confirm it exists (`ls`/Read). Linking deleted files is a top recurring failure (FM-03).

## Before you write to a state file
- **Status files are REPLACED, not appended.** `EXECUTION.md`, `HANDOFF.md`, status tables → rewrite to current truth. Appending creates duplicate, contradictory rows (FM-01 — observed live in swa-erp: two wave-3 rows, two "Changelog" headers).
- **One fact, one home.** Before writing a metric/config/status, check it isn't already stated elsewhere. If it is, reference it; don't copy. Two copies drift (FM-05 — observed: 7/9 vs 5/9, 54x vs 37.5x).

## Before you start a long-running job
- **Check for a stale one first.** `ps aux | grep <project>`. A previous run with wrong params silently competing for CPU is a top recurring failure (FM-02 — observed live: a 157-minute run with `k_inner=5` while the verified config is `k_inner=10`).
- **Params come from the config file, asserted at runtime.** Don't hardcode; read from config; assert the value at startup so an editor/linter revert (FM-06) fails loud instead of running 2 hours wrong.

## Before you commit / publish
- **Publish gate.** Scan for embarrassing artifacts: cheat sheets, AI-prompt files, secrets, `Co-Authored-By` if undesired, vendor chat dumps. (FM-07 — observed live: `MEETING_CHEAT_SHEET.md` reappeared.) Run `validators/publish_gate.sh`.
- **No silent failures.** A `try/except` that swallows an error, or a fallback that hides a broken path, is a bug (FM-11). Errors surface or are handled explicitly — never quietly suppressed.

## Before you expand scope
- **The brief is the box.** If you notice a "while I'm here" improvement, STOP. Is it in the task's file list? If not, it's a new task, not a freebie (FM-08).

## When a new session starts
- **Orient first.** Read HANDOFF.md → the kernel → current wave spec → recent `events.jsonl`. Do NOT start acting from a cold guess (FM-14).

---

If you catch yourself about to violate one of these, that's the signal to open the matching `failure-modes/FM-NN.md` and run its validator.
