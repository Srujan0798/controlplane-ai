# Contributing

1. Work on `main` (or a short-lived branch off `main`); never `.worktrees/` for prize elevation.
2. Read `AGENTS.md` invariants before coding.
3. Prefer a task from `work/wave-*/` over ad-hoc edits.
4. Run `pytest -q` before commit; after code changes run `graphify update .`.
5. No secrets in git. Use `.env.example` as the env catalog.
6. Refund copy: held/escalated — never "blocked."
7. Lane 1 (claims/decisions) is deterministic — no LLM on the critical path.
8. Tag policy: only a human creates `v0.2.0-round2` after green suite + sign-off. Do not self-tag or force-push.
9. Reports: every `work/wave-N/<id>.md` task gets a sibling `work/reports/wave-N/<id>.report.md` with the test/command evidence.
