# Protocol — SDLC Loop

> **Full ship OS:** always prefer `SHIP-SYSTEM.md` (project root) or `core/SHIP-SYSTEM.md` (kit).  
> This file is the short gate list. GFG-aligned: [SDLC](https://www.geeksforgeeks.org/software-engineering/software-development-life-cycle-sdlc/).

## Gates (do not skip)

| # | Stage | Evidence |
|---|---|---|
| 1 | Planning & feasibility | Intent goal + tier + viability notes |
| 2 | Requirements | Testable success criteria + OUT box |
| 3 | Design | `plan/design.md` + task `writes` |
| 4 | Development | Code only under `writes` |
| 5 | Testing | Acceptance / tests exit 0 in report |
| 6 | Deployment | `preflight.sh` PASS; blast-radius for prod |
| 7 | Maintenance | `HANDOFF.md` rewritten |

## Host tools (required — part of Adaptoid)

Plan mode · Subagents · Skills · Hooks · MCP · AGENTS.md · Memory(HANDOFF) · Search · Multi-file edit · Git · Deep reasoning · Web search · Terminal · Headless CI · Code review · Sandbox · Background tasks  

**When:** see stage×tool matrix in `SHIP-SYSTEM.md`.  
**Law:** host executes; Adaptoid stages + evidence decide done.

## Anti-waste (GFG mistakes → harness)

1. Docs ≠ goal → only intent + design + reports  
2. Test early → `acceptance:` before/with build  
3. NFRs in intent when real  
4. No early overengineering  
5. Feedback = HANDOFF each wave  
6. Security every stage (OAP + publish_gate)

## Default

Agile waves. `conductor init-wave --sdlc` or `engine --sdlc` creates stage tasks.
