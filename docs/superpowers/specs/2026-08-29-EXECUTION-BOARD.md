# INTERNAL ENGINEERING BOARD — NOT PRODUCT SURFACE

**Not a portal upload. Not part of the product claim.** Agent execution board only.

# Execution board — Round 2 elevation

**Hand this to agents.** Every task below is self-contained: it names the files it
owns, its contract, its acceptance criteria, and the command that proves it done.

**Companions:** [`2026-08-29-round2-100-design.md`](2026-08-29-round2-100-design.md) (why) ·
[`2026-08-29-round2-submission-protocol.md`](2026-08-29-round2-submission-protocol.md) (what ships)

**Branch:** `feature/round2-elevation` · **Fallback tag:** `v0.2.0-round2` (never moved)

---

## 0. Coordination protocol — read before touching anything

Multiple agents share one working directory. On 2026-08-29 two agents wrote the
same Phase-0 file within minutes and one silently overwrote the other. These
rules exist because that already happened.

### 0.1 File ownership is exclusive

Each task lists **Owns**. An agent may create or modify **only** files in its own
`Owns` list. If your task needs a change in a file another task owns, **stop and
open a new task** — do not edit it.

### 0.2 Frozen — no agent writes these

| Path | Why |
|---|---|
| `docs/ARCHITECTURE.md` | System of record. Reopening it re-risks contradictions that took five adversarial merges to remove. |
| `controlplane/interlock.py` — `MATRIX` | Sixteen transcribed cells. Six of seven models corrupted it when asked to redraw it. |
| `controlplane/models.py` — `Actuator`, `BlastTier` | Exactly five actuators, exactly four tiers. |
| `AGENTS.md` | The invariant list. |

Everything new **feeds** the interlock. The interlock stays sole decider.

### 0.3 Before you start a task

```bash
git pull --rebase
git log --oneline -5          # is someone already doing this?
ls <every path in your Owns>  # does it already exist?
pytest -q                     # must be green before you begin
```

If a file in your `Owns` already exists and is non-trivial, **another agent got
there first.** Stop, report, and take a different task.

### 0.4 Before you commit

```bash
pytest -q                     # full suite, never just your file
git pull --rebase
```

Never commit red. Never commit a file outside your `Owns`. Prefix the message
with the task ID: `T2.1: Aho-Corasick PII detector`.

### 0.5 TDD is mandatory

Write the failing test. **Run it and watch it fail for the right reason.** Then
implement. A test that passed the first time proves nothing — if you did not see
it red, delete it and start again. This applies especially to regression guards:
prove the guard catches a violation before trusting it.

### 0.6 Escalate, do not guess

Stop and ask a human when: a frozen file seems to need changing · the acceptance
criteria are ambiguous · a task's contract conflicts with `ARCHITECTURE.md` · a
demo beat gets *weaker* after your change.

---

## 1. Status

| Wave | State |
|---|---|
| W0 · Blocker + content laws | T0.2, T0.3 **done** (`42ac273`, `1670e7e`) · T0.1 **blocked on human** · T0.4 open |
| W1 · Extraction + binding | T1.1 **in flight** · rest open |
| W2–W8 | open |

Suite at time of writing: **214 passed, 2 skipped.** Baseline was 135.

---

## WAVE 0 — Blocker and laws

### T0.1 · Make the repository public — **HUMAN REQUIRED, DO FIRST**
**Owns:** git remote config
**Blocked by:** `gh auth login` is an interactive device flow. No agent can do this.

```bash
gh auth login -h github.com          # human runs this
gh repo create controlplane-ai --public --source=. --remote=origin --push
git push origin --tags
```

**Acceptance:** public URL resolves · Actions CI green on the pushed branch ·
`.env.example` contains placeholders only · `README.md` renders on the landing page.
**Why first:** it is the only deliverable that can fail catastrophically on
submission day with no recovery, and it is seven days early.

### T0.2 · Content laws as CI — **DONE** (`42ac273`)
Nine laws from `ARCHITECTURE.md` §10 executable across code, docs, the built PDF
and the deck.

### T0.3 · CI on the elevation branch — **DONE** (`1670e7e`)

### T0.4 · Reconcile the duplicate law-checker
**Owns:** `controlplane/lawcheck.py`, `tests/test_lawcheck.py`, `tests/test_content_laws.py`
**Context:** two implementations exist. `tests/test_content_laws.py` (committed,
green) scans the corpus including the built PDF via `pypdf` and the PPTX via
`ZipFile` — that binary coverage is genuinely better. The untracked
`controlplane/lawcheck.py` + `tests/test_lawcheck.py` (60 tests) adds three things
the committed version lacks: **every checker is proven able to fail**, per-law
*correctives* (a line pairing wrong phrasing with right is a correction, not a
breach), and **section scoping** (a `### Boundary — out` heading exempts what it
lists).

**Contract:** keep one module. Merge the corrective + section-scoping + proven-can-fail
machinery into the committed suite, or adopt `lawcheck.py` and port the PDF/PPTX
readers into it. Do not lose either capability.
**Acceptance:** one law-checking module · every checker has a test that feeds it a
violation and asserts it is caught · the corpus scan still covers the built PDF and
PPTX · zero false positives on the current tree.
**Verify:** `pytest -q tests/test_content_laws.py tests/test_lawcheck.py`

---

## WAVE 1 — Extraction and binding · *the pivotal wave*

Closes F1, F2, F3, F4. Moves the score more than every other wave combined.
**Two of four matrix columns currently never fire.** This wave is why.

### T1.1 · Claim extraction — **IN FLIGHT**
**Owns:** `controlplane/extract.py`, `tests/test_extract.py`
**Contract:** arbitrary response text → `list[Claim]`. Pure Python, zero deps,
offline, sub-millisecond. No LLM — this is Lane 1.
- Segmentation surviving `₹1,84,000.`, `Clause 7.2`, `§4.1`, decimals, abbreviations
- Check-worthiness filter (drops greetings, meta, questions — the largest FP lever)
- Typing, precedence **DERIVED > NUMERIC > TEMPORAL > STRUCTURAL > TEXTUAL**.
  A derived claim mistyped as directly checkable breaks the §7 false-assurance boundary.
- Assertion strength from a hedge lexicon with negation scoping
- `role_in_action` **computed** from entity/argument overlap — never hand-typed
- Optional `CONTROLPLANE_EXTRACTOR=llm` adapter, identical signature, never depended on

**Acceptance:** the refund response text *alone* yields its six claims with correct
kinds and hedging · no `Claim(...)` literal remains in any demo path.
**Verify:** `pytest -q tests/test_extract.py && grep -rn "Claim(" controlplane/scenarios/`

### T1.2 · Numeric normalisation and recomputation
**Owns:** `controlplane/numeric.py`, `tests/test_numeric.py`
**Depends:** none (pure library)
**Contract:** extract quantities from text and compare them across notations.
- Currency symbols; **Indian grouping (`1,84,000`) and Western (`184,000`)**
- Scale words: `lakh`, `crore`, `k`, `M`, `bn`; percentages; units
- Compare with per-unit tolerance
- Return `SUPPORTED` on match, **`CONTRADICTED` on a differing value for the same slot**, `UNSUPPORTED` on absence

**This is the task that makes `Block` reachable.** Today nothing in the codebase
emits `Verdict.CONTRADICTED` outside a test fixture, so a quarter of the matrix is
inert. Numeric contradiction is the cleanest producer.
**Acceptance:** `₹1,84,000` ≡ `184000 INR` ≡ `1.84 lakh` · `₹1,84,000` vs `₹1,04,000`
→ CONTRADICTED · `2 crore` ≡ `20000000`.
**Verify:** `pytest -q tests/test_numeric.py`

### T1.3 · Structural symbol table
**Owns:** `controlplane/symbols.py`, `tests/test_symbols.py`
**Contract:** at context-assembly time, index every clause / section / ID / entity
token found in any span → `span_ids`. Claim references are looked up, not searched.
**Acceptance:** the refund span set yields `{4.1, 4.3, 9.1, ORD-9, ...}` and
**`7.2` is absent** · the table is printable as evidence.
**Why it matters:** clause 7.2 then fails *organically and showably* — the console
prints *"the provenance set holds 4.1, 4.3, 9.1 — 7.2 is not among them."* That is
strictly stronger than today's beat, because the judge sees the mechanism.
**Verify:** `pytest -q tests/test_symbols.py`

### T1.4 · BM25 over the provenance set + entailment gate
**Owns:** `controlplane/bm25.py`, `tests/test_bm25.py`
**Contract:** pure-Python BM25 over span contents **only — never the open web**.
Top-k, then a lexical-entailment gate (content-word coverage + negation/antonym
detection). Three bands: high → SUPPORTED · **middle → UNKNOWN** · low → UNSUPPORTED.
Negation detected → CONTRADICTED.
**The middle band is the abstention the architecture promises and the codebase has
never produced.** Today `UNKNOWN` has exactly one producer that no demo exercises.
**Thresholds are not magic numbers.** Leave them as named constants with a TODO
pointing at T3.2; they get **calibrated on the eval corpus and published with their
FP/FN curve**. Asserting a threshold is the exact move `ARCHITECTURE.md` §8 condemns.
**Acceptance:** all four verdicts reachable · thresholds are named constants, not literals.
**Verify:** `pytest -q tests/test_bm25.py`

### T1.5 · Binder v2 — route dispatch
**Owns:** `controlplane/binder.py`, `tests/test_binder_routes.py`
**Depends:** T1.2, T1.3, T1.4
**Contract:** keep the `bind_claims(ledger, claims, ...)` signature. Dispatch on
`ClaimKind`: NUMERIC → T1.2 · STRUCTURAL → T1.3 · TEXTUAL → T1.4 · DERIVED →
recompute from span quantities, else **`UNKNOWN`, never `SUPPORTED`**.
Every `Binding` gains a **`rationale`** alongside `method`, so the evidence packet
explains *why*.
**Acceptance:** substring matching is gone · all four verdicts produced by real
routes · `UNKNOWN` never collapses to `SUPPORTED` (assert this explicitly).
**Verify:** `pytest -q tests/test_binder_routes.py`

### T1.6 · Fixture lockout
**Owns:** `controlplane/pipeline.py`, `controlplane/scenarios/refund.py`, `controlplane/scenarios/flip.py`
**Depends:** T1.5
**Contract:** `run_prepared` **rejects `fixture_map` when `mode == "enforce"`** unless
an explicit `allow_fixtures=True` is passed (tests only). Remove `fixture_map` from
every demo path.
**Context:** `pipeline.py:326` currently reads
`fixture_map = {"amount": (amount_span,), "clause_72": None}`. The amount's
`SUPPORTED` verdict is asserted, not computed. **The repo is public — a judge can
read that line.**
**Acceptance:** the refund demo reproduces **Edit + Escalate (held)** with
`fixture_map=None` · `grep -rn fixture controlplane/scenarios/ controlplane/pipeline.py`
returns nothing in demo paths.
**Gate:** if the beat gets weaker without fixtures, **the task does not close** — fix
the binder, do not restore the fixture.
**Verify:** `python3 examples/refund_trace_demo.py && pytest -q`

### T1.7 · Matrix coverage
**Owns:** `tests/test_matrix_coverage.py`
**Depends:** T1.5
**Contract:** one test per matrix cell, sixteen total, each reaching its cell through
the **real** pipeline — no hand-built `Binding` objects.
**Acceptance:** all 16 cells covered · a test asserts every `Verdict` member has at
least one production producer.
**Verify:** `pytest -q tests/test_matrix_coverage.py`

---

## WAVE 2 — Leakage

### T2.1 · PII and entity detection
**Owns:** `controlplane/pii.py`, `tests/test_pii.py`
**Contract:** Aho-Corasick automaton (pure Python, ~80 lines) over a gazetteer built
from spans + a static sensitive-token set. Checksum-validated detectors: **PAN**
(`[A-Z]{5}[0-9]{4}[A-Z]`), **Aadhaar** (Verhoeff), email, Indian phone, IFSC,
card (Luhn), IBAN.
**Acceptance:** microsecond-scale · near-zero FP on the eval corpus · checksums
actually reject invalid numbers.
**Verify:** `pytest -q tests/test_pii.py`

### T2.2 · Rule A — fabricated PII is a leak
**Owns:** `controlplane/entitlement.py`, `tests/test_leakage.py`
**Depends:** T2.1, T1.5
**Contract:** a PII-shaped entity binding to **no span** is a model-memory leak or
fabrication → forces the `Contradicted` column → Block at R2/R3. (Rule B, ACL
exclusion, already exists and already fires organically — do not disturb it.)
**Why it matters:** this answers the brief's *"a fabricated detail about a person is
simultaneously a hallucination and a privacy concern"* with **one** mechanism rather
than two classifiers. It is currently 100% absent despite being promised in §3.
**Acceptance:** fabricated PAN → Block at R3 · entitled real PAN → Pass · unentitled
real PAN → entitlement path. Three tests.
**Verify:** `pytest -q tests/test_leakage.py`

### T2.3 · Make ACL violations possible in the reference use cases
**Owns:** `controlplane/scenarios/multi_usecase.py`, `tests/test_multi_usecase.py`
**Contract:** `multi_usecase.py:41` sets `acl=principal.clearance`, so an ACL
violation is **structurally impossible** in all three of the brief's reference use
cases. Give each a genuinely mixed-ACL span set.
**Acceptance:** at least one reference use case fires an entitlement violation.
**Verify:** `pytest -q tests/test_multi_usecase.py`

---

## WAVE 3 — The numbers · *the second pivotal wave*

### T3.1 · Labelled eval corpus
**Owns:** `evals/cases/**`, `evals/README.md`
**Contract:** 150–200 YAML cases:
`{response_text, spans[], principal, actions[], expected_verdicts, expected_actuators, label}`.
Strata: three use cases × {clean, hallucinated-numeric, hallucinated-structural,
unentitled-span, PII-leak, derived-trap, hedged-borderline, multi-turn-inherited,
prompt-injection}.
**Include deliberate hard negatives** — cases that *look* wrong but are correct.
Without them a false-positive number means nothing.
**Acceptance:** ≥150 cases · every stratum populated · ≥20% hard negatives · corpus
committed so a judge can attack it.

### T3.2 · Eval harness with confidence intervals
**Owns:** `evals/run.py`, `tests/test_evals.py`, `Makefile` (eval target only)
**Depends:** T3.1, T1.5
**Contract:** `make eval` prints **per route**: precision, recall, FPR, FNR — each
with a **Wilson score interval** — plus the confusion matrix and the abstention
(UNKNOWN) rate. Also calibrates and prints the T1.4 thresholds with their FP/FN curve.
**This is the deliverable that wins.** `ARCHITECTURE.md` §12: *"the line that wins the
room is the published FNR."* `shadow.published_fnr` currently returns `None` always.
**Acceptance:** real numbers printed · no single accuracy number anywhere · the claim
takes the §7 shape: *"we catch X% of ungrounded claims at Y ms p50 — and here is the
Z% we don't."*
**Verify:** `make eval`

### T3.3 · Dead compute
**Owns:** `controlplane/economist.py`, `tests/test_economist.py`
**Contract:** exact backward walk — accepted claims → bindings → spans → steps. Steps
grounding zero accepted claims are dead. Report count, token estimate, ₹ at a stated
rate, ₹ per 1k requests. Plus near-duplicate tool calls (arg hash), retry loops, and
re-retrieval of spans already in context.
**No model, no estimation** — `ARCHITECTURE.md` §12 calls this "the most defensible
number" precisely because it is computed exactly.
**Acceptance:** the refund trace reports 4 of 9 tool calls grounding nothing.
**Verify:** `pytest -q tests/test_economist.py`

### T3.4 · Bench at claimed scale
**Owns:** `scripts/load_bench.py`, `submission/latency_bench.json`
**Contract:** 10,000 requests, concurrency sweep, **per-stage breakdown** (extract /
bind / entitle / interlock), p50/p95/p99, sustained throughput mapped to "tens of
thousands per week". Emit a `methodology` block so the number is not quotable out of
context.
**Acceptance:** n=10000 · per-stage timings present · **never quote 40ms as p95**
(content law 6 will fail the build).
**Verify:** `make bench`

---

## WAVE 4 — Lanes

### T4.1 · Real per-lane deadlines
**Owns:** `controlplane/lanes.py`, `tests/test_lanes.py`
**Depends:** T1.5
**Contract:** `asyncio.gather` with per-lane deadlines. Lane 1 hard 30–60 ms,
deterministic only. Lane 2 near-line (the NLI adapter slot). Lane 3 async.
**A deadline miss returns `UNKNOWN`, resolved by that tier's fail stance — never a
global default.** A universal fail-open makes the plane bypassable by anyone who can
induce load.
**Acceptance:** an artificially slow Lane 2 still lands the decision inside budget via
`UNKNOWN` · a test proves **a slow probabilistic check never overturns a fast
deterministic one** · Lane 1 p95 inside its declared budget in the bench.
**Verify:** `pytest -q tests/test_lanes.py`

---

## WAVE 5 — Governance, feedback, bias

### T5.1 · Jurisdiction axis
**Owns:** `controlplane/jurisdiction.py`, `policies/*.yaml`, `tests/test_jurisdiction.py`
**Contract:** packs gain `jurisdiction`, `regulatory_basis`
(**EU AI Act Art. 14** · **DPDP Act 2023** · **GDPR Art. 22**), `retention_days`,
`tier_overrides`. It must **change behaviour**, not just annotate.
**Acceptance:** a test proves the same request under an `eu` pack and an `in` pack
produces **different actuators**.
**Why:** the brief asks for behaviour varying by use case, **geography**, or risk
appetite. All four packs are currently identical on every axis but tier and stance.
**Verify:** `pytest -q tests/test_jurisdiction.py`

### T5.2 · Override capture → labels
**Owns:** `controlplane/feedback.py`, `tests/test_feedback.py`
**Contract:** `POST /v1/controlplane/decisions/{id}/override` → reviewer, verdict,
reason, written **into the chained ledger** so overrides are tamper-evident too.
Overrides become labels feeding the T3.1 corpus.
**Acceptance:** an override is chained and verifiable · it appears as a label in the
next eval run.
**Verify:** `pytest -q tests/test_feedback.py`

### T5.3 · Threshold proposal behind a shadow replay
**Owns:** `controlplane/feedback.py` (with T5.2), `tests/test_threshold_shadow.py`
**Contract:** **no threshold ships without a shadow replay over the last N traces
printing the FP/FN delta.** This is `ARCHITECTURE.md` §4, and it is what keeps the
T1.4 thresholds from being magic numbers.
**Acceptance:** a threshold change is refused unless a replay delta was produced.
**Verify:** `pytest -q tests/test_threshold_shadow.py`

### T5.4 · Canary with auto-rollback
**Owns:** `controlplane/feedback.py` (with T5.2/T5.3), `tests/test_canary.py`
**Contract:** canary by route; **auto-roll back when human-override rate exceeds 3×
baseline.** State machine with explicit states.
**Verify:** `pytest -q tests/test_canary.py`

### T5.5 · Bias v2 — counterfactual replay
**Owns:** `controlplane/bias.py`, `tests/test_bias.py`
**Contract:** replace the ACL fraction (currently 12 lines self-labelled *"Stub
measurement only"*) with counterfactual replay: perturb protected attributes on
decision-shaped routes, measure **decision-flip rate with a Wilson CI over a rolling
window**, flag when the CI excludes zero.
**Async / Lane-3 only. Per route, never per response** — a per-response bias verdict
is statistically illiterate. State it in **measurement terms, never moral ones**
(content law 9).
**Acceptance:** flip rate reported with an interval · no per-response bias verdict
anywhere · bias never becomes a matrix cell.
**Verify:** `pytest -q tests/test_bias.py`

---

## WAVE 6 — Multi-turn compounding risk

### T6.1 · Claim inheritance across turns
**Owns:** `controlplane/session.py`, `tests/test_multiturn.py`
**Contract:** a claim accepted at turn 1 is inheritable by a later turn's action.
Turn 1: hedged claim passes at R1 (`Pass + annotate`). Turn 3: an R3 action's
`role_in_action` inherits it; the gate re-evaluates **at R3 severity** → Escalate.
**Acceptance:** turn-1 verdict unchanged · turn-3 actuator escalates *because of* the
inherited claim.
**Why:** the brief names multi-turn compounding risk explicitly and **no other team
will demonstrate it.**
**Verify:** `pytest -q tests/test_multiturn.py`

### T6.2 · Multi-turn demo
**Owns:** `examples/multiturn_demo.py`, `controlplane/scenarios/multiturn.py`
**Depends:** T6.1
**Acceptance:** runs end to end and prints the inheritance chain.

---

## WAVE 7 — Track B · the four uploads

> **Hard ordering rule: nothing in Wave 7 starts before T3.2 and T3.4 have printed
> real numbers.** The video and README both display live prototype behaviour.
> Producing either earlier means filming the fixtures.

### T7.1 · The "paste your own text" console screen
**Owns:** `controlplane/server/static/gate.html`, `controlplane/server/app.py` (route only)
**Depends:** T1.5, T3.3
**Contract:** one page — textarea for response text, editable span set, principal
picker, action picker → live graph, extracted claims with types and hedging, binding
method **and rationale**, the symbol table, matrix cell, actuator, evidence packet,
dead compute, per-stage latency.
**This is the answer to "run it on my text."** Today there is no such path.
**Acceptance:** a judge-chosen paragraph produces a correct, explained decision live.

### T7.2 · README PDF
**Owns:** `scripts/build_readme_pdf.py`, `submission/ControlPlane_Round2_README.pdf`
**Depends:** T3.2
**Contract:** a **separate document from the business proposal** — this is what a
judge reads to understand the repository. Generated by script so it cannot drift.
Sections: what this is · the mechanism · **run it in sixty seconds** (copy-pasteable,
tested from a fresh clone) · what to look at · **capability ledger** · evidence ·
repo map.
**The capability ledger is the point.** Every mechanism in the architecture marked
*implemented and tested* / *implemented, prototype-grade* / *designed, not built*.
It preempts every "is any of this real?" question by answering it first — the same
move as publishing the FNR.
**Acceptance:** ≤20 MB · every command in it runs from a clean clone.

### T7.3 · Rebuild the proposal PDF
**Owns:** `scripts/build_proposal_pdf.py`, `round2/CONTROLPLANE_R2_FINAL.md`, `submission/ControlPlane_Round2_Proposal.pdf`
**Depends:** T3.2, T3.3, T5.1
**Contract:** carry the real eval table, the published FNR with its interval, dead
compute priced, the jurisdiction packs, and the honest proven-vs-designed line.
**Audit that all seven of the brief's asks are present and titled as such** — problem
framing, solution design, target users, business case, impact, phased roadmap, risks
with mitigations. **That list is the rubric.**
Fix the known defect: some Unicode arrows render as `■`.
**Acceptance:** content laws green over the PDF's extracted text · all seven sections present.

### T7.4 · Rebuild the deck
**Owns:** `submission/ControlPlane_Round2_Pitch.js`, `submission/ControlPlane_Round2_Pitch.pptx`
**Depends:** T7.3
**Contract:** rebuild from the JS source so deck and proposal cannot diverge. Same
number freeze.
**Acceptance:** content laws green over the deck's extracted text.

### T7.5 · Prototype video
**Owns:** `docs/VIDEO_SCRIPT.md`, the recording
**Depends:** T7.1
**Contract:** `.mp4`, 1920×1080, screen capture + voiceover, target **3:30–4:00**.
**Confirm the portal's length and size caps before recording.**
**It is a *prototype* video, not a pitch video** — the PPTX carries the pitch. Show
the system running; no narrated slides.

| Time | Beat |
|---|---|
| 0:00–0:20 | **The failure.** *"Approved. Refund of ₹1,84,000 issued under clause 7.2."* Confidence 0.94. Money moved Tuesday, found Friday. **Clause 7.2 does not exist.** |
| 0:20–0:40 | **The reframe.** `STEP → SPAN → CLAIM → ACTION`. "Not text to be scored — claims requesting permission to act." |
| 0:40–2:00 | **Mechanism, live.** Paste fresh. Six claims extract themselves. Symbol table prints 4.1, 4.3, 9.1 — **no 7.2**. Amount recomputes. HR span ACL excludes the caller. Two pending actions: `show_text` R1 → **Edit**; `issue_refund` R3 → **Escalate, held**. Zero LLM. |
| 2:00–2:30 | **The flip.** Same span, same claim, same graph — change only the caller. Edit → Pass. |
| 2:30–3:10 | **The numbers.** `make eval` → FNR with its interval. Dead compute. "Every team will claim detection. We publish what we miss." |
| 3:10–3:30 | **Close.** *"That system was never asked to prove anything. Now nothing acts until it can prove it should."* |

**Production rules:** rehearse the command sequence until it runs clean — a fumble
cannot be edited around. Large terminal font. Nothing personal in frame, no
notifications, no home paths. Record voiceover separately so a stumble costs one take.
**Never say "blocked" about the refund** — say *held and escalated with the evidence
packet*. Content law 2, and the single most likely on-camera slip.

### T7.6 · Hostile Q&A v2
**Owns:** `docs/HOSTILE_QA_DRILL.md`
**Depends:** T3.2
**Contract:** the new capabilities invite ~12 new attacks. Draft and drill answers to
at least: *"your BM25 threshold is a magic number"* · *"a Wilson CI on 150 cases is
wide"* · *"your corpus is self-authored"* · *"you wrote the labels you're graded on"* ·
*"what happens when the extractor misses a claim entirely?"*

---

## WAVE 8 — Verification

### T8.1 · `make verify`
**Owns:** `Makefile`, `scripts/verify.py`
**Depends:** all of Wave 7
**Contract:** one command — preflight → tests → content laws → eval → bench → then
**diff every number printed against every number quoted in the PDF and the deck.**
Any drift fails the build.
**Verify:** `make verify`

### T8.2 · Determinism
**Owns:** `tests/test_determinism.py`
**Contract:** the same input yields a **byte-identical ledger hash** across runs and
across processes.

### T8.3 · Reviews
Run `/security-review`, then `/code-review high`. Fix findings, re-run.

### T8.4 · Submission dry run — **HUMAN**
1. `make verify` — green, no drift.
2. **Clone the public repo into a fresh directory**, follow the README PDF's
   sixty-second path verbatim, confirm the three demos. *If a clean clone does not
   run, nothing else matters.*
3. CI green on the exact commit the link points at.
4. Play the video start to finish. **Listen for the word "blocked."**
5. Open both PDFs and the PPTX; confirm every number matches `make verify`.
6. Check each file against the portal's type and size limits.
7. Upload. Screenshot the confirmation.

---

## 2. Parallelisation

Tasks with disjoint `Owns` and satisfied dependencies run concurrently.

```
NOW      T0.1 (human)   T0.4   T1.1(in flight)   T1.2   T1.3   T1.4   T2.1   T3.1
then     T1.5 ──▶ T1.6 ──▶ T1.7        T2.2   T2.3
then     T3.2   T3.3   T3.4   T4.1
then     T5.1   T5.2 ──▶ T5.3 ──▶ T5.4     T5.5   T6.1 ──▶ T6.2
then     T7.1 ──▶ T7.5      T7.2   T7.3 ──▶ T7.4   T7.6      ← gated on T3.2 + T3.4
finally  T8.1   T8.2   T8.3 ──▶ T8.4
```

**Critical path:** T1.2/1.3/1.4 → T1.5 → T1.6 → T3.2 → T7.x → T8.4.
Everything else has slack. If a day is lost, lose it off Wave 5, not Wave 1 or 3.

## 3. Stopping rule

If the week runs out, ship from wherever you are — **every wave ends green and
submittable**, and `git checkout v0.2.0-round2` is always a valid fallback.
Stopping after Wave 3 still lands ~91 with all five deliverables present.
Stopping mid-Wave-1 is the only genuinely bad outcome, because the fixtures would
be half-removed. **Finish Wave 1 or do not start it.**
