# Kernel — Two-Tier Architecture (Brain / Hands / Session)

> Always loaded. The shape of every project built with Adaptoid OS.

## The two tiers

```
TIER 1 — ORCHESTRATOR  (any host: Grok Build / Claude Code / Cursor / Codex / …)
  Plans. Dispatches. Reviews. Merges. Owns project state.
  ONE active orchestrator session at a time (or one primary + isolated subagents).
        │  writes task brief → work/<wave>/tasks/*.md
        ▼
TIER 2 — WORKERS / HANDS  (host subagents, worktrees, or secondary agent sessions)
  Each takes ONE self-contained brief. Executes. Writes code. Writes a report.
  Prefer isolation: git worktree or separate sandbox when writes may collide.
        │  writes report → work/reports/<wave>/*.report.md
        ▼
  Back to orchestrator: review → merge → rewrite HANDOFF.
```

**Hard rule:** workers never own product intent or HANDOFF truth. The bridge is the `work/` folder + reports. Models and hosts are **swappable**; files are the contract.

**Single-host path (common):** one Agent session *is* both Brain and Hands under SHIP gates — still write tasks/reports/evidence so a cold session can resume.

## Brain / Hands / Session

| Primitive | Our equivalent | Why it matters |
|---|---|---|
| **Brain** (model + harness) | Orchestrator host session + Adaptoid law | can crash and resume |
| **Hands** (tools, sandboxes) | Host tools, worktrees, MCP, terminal | disposable; replace freely |
| **Session** (durable log) | `HANDOFF.md` + optional `orchestrator/memory/session/*.events.jsonl` | the ONE thing that must survive |

Three failure modes, three recoveries:
- **Brain crash** → reopen host → reads HANDOFF.md (+ events if any) → resumes.
- **Hand crash** → that worktree/subagent dies → open a new one with the same brief.
- **Session lost** → fatal if only chat held state. State lives in **files**, never only in chat.

## Why hosts are interchangeable

- `AGENTS.md` is the portable law ([agents.md](https://agents.md/) standard).
- `CLAUDE.md` / `.cursor/rules` / host skills are **projections** of the same truth.
- Switching mid-project = open same repo; no migration of proprietary memory.

## Why workers are stateless

Workers forget between tasks BY DESIGN. Every task brief must be self-contained (writes, forbid, acceptance). A brief that needs "remember what we discussed" is broken. See `protocols/sdlc-loop.md` + `SHIP-SYSTEM.md`.
