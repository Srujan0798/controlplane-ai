# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: plain static HTML/CSS/JS served by existing FastAPI (`controlplane/server/static/index.html`) — no SPA framework rewrite this round.

## Users

Primary: Accenture Innovation Challenge Round 2 judges — stand, click once, understand the gate in under a minute.
Secondary: enterprise platform / SRE buyers evaluating whether ControlPlane looks like something they could trust in production next quarter.

## Product Purpose

ControlPlane.ai is an admission-control layer for AI that acts. It captures provenance outside the model (`STEP → SPAN → CLAIM → ACTION`), binds claims to that evidence set, checks entitlement, and decides with a frozen blast-radius matrix. Success for this surface: a judge can run a refund scenario and immediately see Edit + Escalate with receipts — without reading docs first.

## Positioning

We do not score the model's mind. We check whether a claim is a member of the evidence the model was actually given, and whether the caller is entitled to that evidence, before an irreversible action fires.

## Operating Context

Live demo console next to a pitch. Short attention. Projector or laptop. Must work offline with canned scenarios. APIs already exist: `/v1/controlplane/demo/{scenario}`, metrics, audit download, OpenAI-compatible chat completions.

## Capabilities and Constraints

- Must preserve: Edit / Escalate dual-action refund proof; clause 7.2 does not exist; matrix never redrawn; Lane 1 deterministic (no LLM on critical path).
- Scenarios: refund, support, copilot; modes: enforce / shadow.
- Latency shown as measurement, never marketing (≤40ms p50 / ≤200ms p95 — never quote 40ms as p95).
- Surface file: `controlplane/server/static/index.html` (single-page console).

## Brand Commitments

- Name: ControlPlane.ai
- Voice: precise, adversarial-ready, no hype. Prefer "held with evidence packet" over "blocked."
- Team: ControlPlane · Choda Srujan Sai · Dhrithika · IIT Gandhinagar · PS #1

## Evidence on Hand

- Working gate APIs and scenarios on `feature/round2-controlplane`
- Frozen architecture in `docs/ARCHITECTURE.md`
- Pitch narrative in `docs/ROUND2-PITCH.md`

## Product Principles

1. Prove the mechanism in the first viewport — not a dashboard of vanity metrics.
2. Judges first, buyers second: demo clarity outranks feature density.
3. Receipts over rhetoric: every actuator shows its matrix cell and driving claims.
4. Familiar Operate affordances; distinctive only where ControlPlane's mechanism needs to be unforgettable.
5. Never invent commercial claims, customer logos, or measured FNR percentages beyond what the prototype publishes.

## Accessibility & Inclusion

WCAG 2.1 AA target. Keyboard operable. Respect `prefers-reduced-motion`.
