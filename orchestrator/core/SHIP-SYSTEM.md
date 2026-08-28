# Adaptoid SHIP SYSTEM — SDLC × Host capabilities (one OS)

> **This is the product.** Adaptoid is not “docs next to Grok.”  
> It is the **operating system** that forces **plan → build → test → deploy → maintain**  
> using the host’s full toolkit (Grok Build / Claude Code / Cursor / Codex).  
> SDLC ref: [GFG Software Development Life Cycle](https://www.geeksforgeeks.org/software-engineering/software-development-life-cycle-sdlc/).

---

## One sentence

**Ship = SDLC gates + host tools + evidence.** Skip a gate or a tool when required → not done.

### Loop engineering (mid-2026 language)

Elite practice is **not** one-shot prompts. It is **loops**: plan → act → verify → write state → next.  
Harness = environment one agent runs in. **Loop** = system that prompts agents (automations, `/goal`, worktrees, skills, subagents) while **maker ≠ checker**.  
Adaptoid SHIP SYSTEM is the **mission / factory layer** on top of host harnesses — portable across Claude / Cursor / Codex / Grok.  
Research corpus (incomplete ocean): `docs/research/era-ocean/elite/ELITE-10-PERCENT.md`.

---

## A. Host toolkit (must use — Adaptoid activates these)

Every coding host (especially Grok Build) already has these.  
**Adaptoid requires them at the right SDLC stage.** Do not ignore them. Do not rebuild them.

| # | Capability | What it is | Adaptoid activation rule |
|---|---|---|---|
| 1 | **Plan mode** | Structured approach before code | **Mandatory** in stages 1–3. No BUILD until plan exists in intent/tasks. |
| 2 | **Subagents** | Parallel agents for test/research | Stage 2 research, stage 5 testing, parallel `writes`-disjoint tasks. Orchestrator reviews. |
| 3 | **Skills** | Reusable slash/workflows | Encode repeated stage moves as skills; project law still AGENTS.md. |
| 4 | **Hooks** | Scripts on edit/tool | Session start → orient HANDOFF; pre-ship → run preflight. |
| 5 | **MCP servers** | Linear, Sentry, Grafana, DB, … | Declare in `adaptoid.config.yaml` `mcp_servers`; OAP policy before write/network. |
| 6 | **AGENTS.md** | Conventions per project | **Generated** cold-start; always load first. |
| 7 | **Memory** | Persist across sessions | **HANDOFF.md** (replace-not-append) + session events if present. |
| 8 | **Code search** | Grep / navigate | Before edit: search; stay in task `writes`/`forbid`. |
| 9 | **Multi-file edits** | Cross-file refactor | Only paths in `writes`; FM-13 disjoint for parallel work. |
| 10 | **Git integration** | Stage/commit/PR | After TEST green; never commit secrets (publish_gate). |
| 11 | **Deep reasoning** | Hard problems step-by-step | Allowed anytime; still need command evidence after. |
| 12 | **Web search** | Docs/packages | Prefer live docs over memory for APIs/versions. |
| 13 | **Terminal** | Builds/tests streaming | Every acceptance + preflight runs here. |
| 14 | **Headless / CI** | Script in pipelines | `preflight.sh` / `make ship-check` in CI. |
| 15 | **Code review** | Line feedback pre-PR | After BUILD, before merge/ship; status claims need evidence. |
| 16 | **Sandbox** | Untrusted code isolated | Untrusted/generated code → sandbox; OAP deny-by-default secrets. |
| 17 | **Background tasks** | Long builds/monitors | Wait for exit code; never claim done while running. |
| 18 | **Theming** | UI chrome only | Optional; zero effect on ship gates. |
| 19 | **Git worktrees** | Isolated checkouts for parallel agents | **Required** when ≥2 writers risk path collision (FM-13); else optional. Host: Claude `--worktree`, Grok/Codex worktrees. |
| 20 | **Agent Skills (open)** | Portable `SKILL.md` procedures ([agentskills.io](https://agentskills.io)) | Prefer over bloating AGENTS. Engine emits `.agents/skills/*` (+ Claude mirror). |
| 21 | **Permissions / sandbox profiles** | Host hard gates (deny/ask/allow, shell sandbox) | Map OAP tiers → host profile. **Codex: shell sandboxed, MCP often not** → MCP write = high blast-radius. |
| 22 | **Nested project instructions** | Per-package AGENTS / rules in monorepos | Closest instruction file wins for files touched. |
| 23 | **Context budget** | Tokens per turn are finite; decide where they go | Thin always-on law (AGENTS) + skills on demand + session reset between phases. Ask "where do this turn's tokens go?" before big reads (FM-04/FM-15). |

### Soft vs hard enforcement

| Soft (guidance) | Hard (truth) |
|---|---|
| AGENTS.md prose, Cursor `.mdc` | Hooks (Claude/Codex/Grok), permissions, **preflight validators** |

Rules without validators are theater. Ship = hard gates green.

### Efficiency law

| Layer | Owns |
|---|---|
| **Host toolkit** (rows above) | Hands — execute, search, edit, test, git, MCP, worktrees |
| **Portable skills** | How-to on demand (`.agents/skills`) |
| **Adaptoid SHIP SYSTEM** | Brain rules — which stage, which tools, what evidence, when stop |

---

## B. Full SDLC (7 stages) — GFG-aligned, Adaptoid-enforced

Default model: **Agile waves** (each wave can run a thin slice through stages).  
Waterfall only if tier T3+ compliance needs hard phase freezes.

### Stage 1 — Planning & Feasibility
| | |
|---|---|
| **GFG** | Scope, cost, schedule, viability |
| **Adaptoid artifacts** | `PROJECT-INTENT.md` (goal, IN/OUT, tier), `adaptoid.config.yaml` |
| **Host tools** | Plan mode, deep reasoning, web search (feasibility of stack) |
| **Evidence** | Intent written; falsification listed; no code yet |
| **Anti-mistake** | Don’t skip planning and jump to coding |

### Stage 2 — Requirements (SRS-lite)
| | |
|---|---|
| **GFG** | Functional + non-functional requirements |
| **Adaptoid artifacts** | Intent `success_criteria`, stakeholders, NFRs (security/perf if real) |
| **Host tools** | Plan mode, subagents (research), web search, MCP (tickets if any) |
| **Evidence** | Testable bullets; OUT box explicit |
| **Anti-mistake** | Docs are not the goal — criteria must be checkable |

### Stage 3 — System Design (HLD/LLD-light)
| | |
|---|---|
| **GFG** | Architecture, data, APIs, UI structure |
| **Adaptoid artifacts** | `plan/design.md` or design task; task `writes` lists |
| **Host tools** | Plan mode, code search (existing code), multi-file read |
| **Evidence** | Modules + interfaces named; smallest vertical slice for this wave |
| **Anti-mistake** | No overengineering before core slice works |

### Stage 4 — Development (Coding)
| | |
|---|---|
| **GFG** | Implement, VCS, unit tests as you go |
| **Adaptoid artifacts** | Code under `writes` only; reports |
| **Host tools** | Terminal, multi-file edits, code search, git, skills, sandbox if untrusted |
| **Evidence** | Diff in box; local tests if any |
| **Anti-mistake** | No scope freebies (FM-08) |

### Stage 5 — Testing
| | |
|---|---|
| **GFG** | Unit, integration, system, UAT as needed |
| **Adaptoid artifacts** | `tests/`, task `acceptance:`, reports with exit codes |
| **Host tools** | Terminal, subagents (parallel test), background tasks (wait for finish) |
| **Evidence** | Commands + exit 0 pasted in report |
| **Anti-mistake** | Never ship with late/skipped tests. Benchmark/proxy green ≠ done (FM-21) — acceptance must be able to fail |

### Stage 6 — Deployment
| | |
|---|---|
| **GFG** | Release, smoke, CI/CD |
| **Adaptoid artifacts** | `preflight.sh` green; deploy notes if any |
| **Host tools** | Terminal, headless/CI, git (tag/PR), hooks, MCP (observability) |
| **Evidence** | Preflight PASS; blast-radius check for prod |
| **Anti-mistake** | Security continuous — publish_gate / OAP, not “later” |

### Stage 7 — Maintenance
| | |
|---|---|
| **GFG** | Fixes, patches, enhancements |
| **Adaptoid artifacts** | **Rewrite** `HANDOFF.md`; new wave tasks |
| **Host tools** | Memory=HANDOFF, code search, plan mode for next slice |
| **Evidence** | Cold session can resume from HANDOFF alone |
| **Anti-mistake** | Don’t silent-scope “while I’m here” |

---

## C. Per-wave execution order (default)

```
1 PLAN+REQ  → intent (plan mode)
2 DESIGN    → plan/design.md + task writes (plan mode)
3 BUILD     → code (terminal, edits, search, git)
4 TEST      → acceptance + optional subagents
5 DEPLOY    → preflight / CI headless
6 MAINT     → rewrite HANDOFF → next wave
```

**Never BUILD without PLAN/REQ evidence.**  
**Never DEPLOY without TEST evidence.**

---

## D. Methodologies (when to pick)

| Context | Model | How Adaptoid runs it |
|---|---|---|
| Default | **Agile** | Short waves; each wave thin SDLC slice |
| Fixed contract T3+ | Waterfall-ish | Harder gates; design before any build |
| Ops/release heavy | DevOps | Headless preflight on every merge |
| Spike T0 | RAD/prototype | Compress design; still test + handoff |

---

## E. Security in every stage (DevSecOps)

- Intent: security NFRs when relevant  
- Design: threat notes if networked/auth  
- Build: no secrets in tree (`publish_gate`)  
- Test: include security checks when applicable  
- Deploy: OAP + blast-radius for prod  
- Maintain: patch as new wave, not silent edit  

---

## F. Failure if you “follow SDLC on paper”

GFG lists: unclear requirements, weak stakeholders, rigid checklist, underestimated complexity, no ownership.  
Adaptoid counter: **falsification**, **evidence**, **IN/OUT box**, **HANDOFF ownership**, **smallest slice first**.

---

## G. Session operating playbook (from Grok Build practice)

Full detail: **`HOST-OPERATING-PLAYBOOK.md`** (copied into every Core project).

Mandatory behavior:

| Practice | Rule |
|---|---|
| **Intent lock** | Ambiguous brief → ≤4 A/B/C options **before** BUILD |
| **Plan → approve → implement** | Big/ambiguous → plan mode / `plan/design.md` → user “go” → code |
| **One outcome per turn** | Don’t mix 10 unrelated jobs |
| **Point at files** | Use explicit paths when known |
| **Session hygiene** | Compact/new session between phases when context bloated |
| **Subagents** | Large explore/tests only — not empty greenfield |
| **AGENTS.md** | Stack + secrets + test rules once; never re-explain every chat |
| **Verify before done** | Run tests · show diff · exit code required |
| **Safety** | Careful on secrets/prod; never commit secrets |

---

## H. Generated projects must ship with

- `SHIP-SYSTEM.md` (this file)  
- `HOST-OPERATING-PLAYBOOK.md` (how to proceed like an efficient host agent)  
- `protocols/sdlc-loop.md`  
- AGENTS.md that requires stages + host tools + playbook  
- SDLC tasks (engine default `--sdlc`)  
- Intent-lock section in PROJECT-INTENT or `plan/intent-lock.md` when brief is thin  

**If the agent is not intent-locking, planning big work, running tests, and rewriting HANDOFF — Adaptoid is not running.**
