# HANDOFF.md — cold resume (rewrite, never append)

## Three works
See `3-WORKS.md`.

1. **SEBI × Adaptoid (Track 1):** `work/wave-6`, `work/wave-7`, `work/wave-8` all **SHIPPED** on `main` (reports in `work/reports/`).
2. **Lite MD (Track 2):** review `…/Adaptoid-OS/improvements/lite-diffs/ADAPTOID-LITE-3.2-PROPOSED.md` — do not replace Desktop 3.1 until approved.
3. **Adaptoid-OS Ultra (Track 3):** review/merge harvest into `…/Adaptoid-OS/improvements/`; Core stays pristine.

## Product
- Branch: `main`
- Invariants: `AGENTS.md` (frozen — never "improve")
- Waves 6/7/8: **SHIPPED**. Wave 6 room impact (OG meta, entitlement UI, error chrome, demo script, brand gotchas). Wave 7 enterprise edges (CORS allowlist, JSON logs, graceful shutdown, idempotency-key, coverage CI, fail-stance enforcement, shadow CSV, OpenAPI examples). Wave 8 evidence close (audit, abuse test map, prize matrix refresh, handoff, tag).
- Tag (human-approved only): `v0.2.0-round2` once `pytest -q` green and a human signs off (see `docs/EVENT_DAY_CHECKLIST.md`).

## Resume checklist
1. `git status` clean; `git log -1` on `main`.
2. `pytest -q` → expect green (135 passed, 2 skipped at close).
3. `graphify update .` if code changed since last run.
4. For the room: `make test && make judge` then `docker compose up --build` (8080) or `make run` (8787).
