# Host operating playbook — how the agent must proceed

> Extracted from **how Grok Build actually works well** (plan mode, project rules, sessions, verification) and generalized for **any host** (Grok Build / Claude Code / Cursor / Codex).  
> Adaptoid **embeds this into every generated project** so the environment forces high-level, efficient behavior — not random coding.

This is **not** “reimplement Grok.” It is **Adaptoid law**: how to run the host toolkit on *this* brief.

---

## 0. Mental model (host vs Adaptoid)

```
You
  ↓
Host CLI/TUI (Grok Build, Claude, Cursor, …)
  · plan mode · subagents · skills · hooks · MCP
  · search · multi-file edit · git · terminal · sandbox · CI
  ↓
Adaptoid project files (this repo)
  · AGENTS.md · SHIP-SYSTEM · INTENT · HANDOFF · tasks · preflight
  ↓
Your product code
```

| Layer | Job |
|---|---|
| **Host** | Hands — tools, edits, shell, web |
| **Adaptoid** | Mission — intent lock, stage gates, evidence, environment setup |

---

## 1. Proceeding style (copy Grok’s efficient structure)

When responding to the user, structure work like high-quality Grok Build sessions:

1. **Plain English first** — what we’re doing and why  
2. **Tables** for options / tradeoffs / status  
3. **One clear outcome per turn** — fewer tokens, less thrash  
4. **Bottom line** — 2–4 bullets of decision  
5. **Your move** — only if a real decision blocks progress  

Never dump unstructured code before intent is locked (unless the change is tiny).

---

## 2. Intent lock before code (critical)

From Grok’s brainstorming rule and plan mode:

| Situation | Required behavior |
|---|---|
| New product / ambiguous brief | **Stop. Ask ≤4 options (A/B/C/D).** Write answers into `PROJECT-INTENT.md` |
| Architecture multi-path | Enter **plan mode** (or write `plan/design.md`) → user **approves** → then code |
| Typo / one-button / clear bug | **Skip plan** — implement + verify |

**Never** scaffold full stack while industry, stack, or offline constraints are still open.

### Intent-lock template (agent fills)

```markdown
## Open decisions (must resolve before BUILD)
1. … ?
   - A) … (recommended)
   - B) …
   - C) …
```

Store resolution under PROJECT-INTENT preferences + success criteria.

---

## 3. Plan → approve → implement

| Step | Host | Adaptoid artifact |
|---|---|---|
| Plan | Plan mode / design write-up | `plan/design.md` or session plan |
| Approve | User says “go” / accepts plan | HANDOFF: active task moves to BUILD |
| Implement | Edits + terminal | code under task `writes` |
| Verify | Terminal tests | report with exit code |

---

## 3b. Mid-2026 host reality (adapt or thrash)

### Agent Skills (portable how-to)

- Format: `.agents/skills/<name>/SKILL.md` ([agentskills.io](https://agentskills.io))
- Generated projects include: `intent-lock`, `verify-before-done`, `blast-radius-check`, `handoff-rewrite`, `worktree-parallel`
- **AGENTS.md = short always-on law.** Skills = procedures loaded when relevant (progressive disclosure / FM-04)

### Soft rules vs hard gates

| Host | Soft | Hard |
|---|---|---|
| Cursor | `.mdc` / AGENTS | **preflight only** — model may ignore rules |
| Claude / Grok | CLAUDE/AGENTS | Hooks + permissions + preflight |
| Codex | AGENTS | Shell sandbox + preflight; **MCP not shell-sandboxed** |

### Parallel agents → worktrees

Same-checkout multi-agent → FM-13 collisions. Prefer **one worktree per overlapping writer**. Orchestrator merges after tests. Single HANDOFF writer on primary tree.

### MCP policy

Default: host **CLI** (`git`, `gh`, tests) over MCP. MCP only for authenticated SaaS/DB/browser. Network/write MCP → blast-radius confirm. Allowlist in `adaptoid.config.yaml`; no silent marketplace installs.

### Spec-driven development interop (Spec Kit / Kiro / OpenSpec era)

Adaptoid already **is** spec-driven: `PROJECT-INTENT.md` + intent-lock = the spec; SDLC gates = the executable workflow.
- Team uses GitHub Spec Kit / AWS Kiro / OpenSpec → point their constitution/spec file at `PROJECT-INTENT.md` (one intent source; never two specs — FM-01/FM-05).
- Keep `AGENTS.md` AAIF-plain (thin, no frontmatter dependence) so every SDD tool can read it.
- Their spec workflow may drive *planning*; Adaptoid still owns *proof of done* (acceptance + preflight).

### Single strong agent default

One orchestrator + sparse subagents (explore / test / review). Full multi-agent crews only when debate is required — not greenfield scaffolding.

**Phases:** prefer one SDLC stage (or one wave slice) per focused session when possible.  
Use host **session reset** (`/new` or equivalent) between unrelated jobs to save context and cost.

---

## 4. Efficiency rules (token + thrash)

| Rule | Why |
|---|---|
| **One outcome per turn** | “Create files, then smoke test” beats 10 mixed asks |
| **Point at files** when known (`@path` / explicit path) | Don’t full-repo search for a known file |
| **Compact / new session** when context bloated | Long chats = cost + confusion |
| **Subagents only for large exploration** | Empty or tiny repos: one agent is enough |
| **AGENTS.md once** | Stack, style, secrets, test/commit rules — never re-explain every session |
| **Verify, don’t just write** | Closing lines: run tests · show diff · no “done” until command passes |

---

## 5. When to use which host capability

| Capability | Use when | Skip when |
|---|---|---|
| **Plan mode** | Ambiguous feature, multi-file design, new architecture | Typo, single obvious button, known 5-line fix |
| **Subagents** | Large repo explore / parallel tests | Greenfield tiny MVP |
| **Skills** | Repeated workflows (review, deploy checklist) | One-off |
| **Hooks** | Session orient, format, preflight nudge | N/A for manual Lite paste |
| **MCP** | Linear/Sentry/DB needed and configured | No external systems |
| **Code search** | Unfamiliar code / rename impact | You already named the file |
| **Multi-file edit** | Coordinated refactor in `writes` | Single file |
| **Git** | After tests green | Mid-broken WIP (unless WIP commit agreed) |
| **Web search** | Live API/docs/versions | Pure local logic |
| **Terminal** | Every build/test/preflight | Never skip for “done” |
| **Headless/CI** | Merge/ship automation | Local spike only |
| **Code review** | Before PR/ship | Pure spike throwaway |
| **Sandbox** | Untrusted / agent-generated risky code | Trusted local scripts |
| **Background tasks** | Long builds — **wait for exit** | Don’t claim done while running |
| **Theming** | UX only | Never blocks ship |

---

## 6. Safety (permissions)

| Mode | When |
|---|---|
| Careful / ask | Secrets, prod deploy, money, external humans |
| Always-approve | Local personal sandbox **you** own and accept risk |

Adaptoid: `policies/default.yaml` + blast-radius. **Never commit secrets.**

---

## 7. Environment Adaptoid must create (from user intent)

Given brief → analysis (archetype, tier, stack hints) → project **must** include:

| Artifact | Purpose |
|---|---|
| `AGENTS.md` / host files | Project rules forever (Grok-style project rules) |
| `SHIP-SYSTEM.md` | SDLC × toolkit |
| **This playbook** | How to proceed |
| `PROJECT-INTENT.md` | Intent lock + falsification |
| `HANDOFF.md` | Cross-session memory |
| `work/wave-1/tasks/*` | Stage tasks with host tools required |
| `policies/` | Tool allow/deny |
| `preflight` validators | Evidence gate |

Adapt **depth** to intent:

| Intent signal | Environment shape |
|---|---|
| Hackathon / 48h | Thin design; fast vertical slice; fewer subagents |
| Job take-home | Clean structure, tests, README quality |
| Internship | Report-friendly docs, metrics if research |
| SaaS / production | Stronger NFRs, preflight, blast-radius |
| Ambiguous industry/stack | **Intent-lock questions first** — no full scaffold until A/B/C |

---

## 8. Closing checklist every wave

1. Intent still true?  
2. Stage evidence present?  
3. Tests/preflight command output pasted?  
4. Diff explained?  
5. HANDOFF rewritten for cold start?  
6. Secrets out of tree?  

If any fail → not done.
