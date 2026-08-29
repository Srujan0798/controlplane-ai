# Round 2 Submission Protocol — five deliverables, two tracks, seven days

**Date:** 2026-08-29 · Team ControlPlane · Accenture Innovation Challenge 2026 · PS #1
**Companion:** [`2026-08-29-round2-100-design.md`](2026-08-29-round2-100-design.md) — the code plan
**Baseline:** `main` @ `7a631c8`, tag `v0.2.0-round2` · 135 tests green · **no git remote**

---

## 1. What the portal actually asks for

Unstop form, five required fields. **Three do not exist.**

| # | Field | Constraint | Status |
|---|---|---|---|
| 1 | Public GitHub link | ≤500 chars | ❌ **no remote configured**; `gh` token invalid |
| 2 | Prototype video | `.mp4` / `.mov` | ❌ **does not exist** |
| 3 | README document | `.pdf`, ≤20 MB | ❌ **does not exist** (only `README.md`) |
| 4 | Detailed Business Proposal | `.pdf` | ✅ `submission/ControlPlane_Round2_Proposal.pdf` — must be rebuilt against real numbers |
| 5 | Detailed Business Proposal | `.pptx` | ✅ `submission/ControlPlane_Round2_Pitch.pptx` — must be rebuilt against real numbers |

### Three consequences that reshape the plan

**C1 — The repository is a judged artifact.** A public link means judges can clone, read, and
grep. `fixture_map = {"amount": (amount_span,), "clause_72": None}` at `pipeline.py:326` stops
being an internal risk and becomes a public one. Findings F1–F3 move from *should fix* to
*must fix before the link is submitted*.

**C2 — There is no live presentation.** The form is upload-only. The **video is the demo**, and
the form says *Prototype* video, not pitch video — the PPTX carries the pitch. The video must
show the system running on screen, not slides narrated. This replaces the "live console for the
room" framing in the code plan.

**C3 — Strict ordering.** The video and the README PDF both display the prototype's real
behavior. Producing either before the code lands means filming the fixtures. Track B therefore
cannot start until Track A has closed Phase 4.

---

## 2. Two tracks

**Track A — Code.** The nine phases in the companion design doc. This is what the GitHub link
exposes and what the video films.

**Track B — Artifacts.** The four uploads. Depends on Track A: the numbers in the proposal, the
deck, the README PDF and the video must all be the numbers `make eval` actually prints.

The only Track B item that is independent — and the only true blocker — is the repository
itself. It goes first.

---

## 3. Day protocol

Seven working days, `D0` through `D6`. Every day ends with a green tree and a stated gate.

### D0 — Clear the blocker, freeze the laws *(~3h)*

**B0.1 — Repository live.** This needs a human; `gh auth login` is interactive.

```bash
gh auth login -h github.com            # you run this — device flow, browser
gh repo create controlplane-ai --public --source=. --remote=origin --push
git push origin --tags
```

Then verify, in this order:
- GitHub Actions CI goes green on the pushed `main` (the workflow already exists and is correct)
- `.env.example` holds placeholders only — no real values
- No secret matches across tracked files
- `README.md` renders correctly on the GitHub landing page, because that is the first thing a
  judge sees after clicking the link

**Push now rather than at the end.** A repository that only appears on submission day is a
single point of catastrophic failure; and a visible engineering arc — `fix: replace
fixture-driven binding with real numeric recomputation` — reads as judgment, not as an
admission. Judges read `HEAD`, not archaeology.

**B0.2 — Content laws into CI** (companion Phase 0). Nine laws as executable tests across code,
docs, and the extracted text of the PDF and PPTX, landed *before* any behavior changes.

> **Gate D0:** public URL resolves · CI badge green · content-law suite green.

### D1 — Claim extraction *(Phase 1)*

Arbitrary text → typed claims. Pure Python, offline, no LLM on Lane 1. The LLM extractor ships
as a switchable adapter behind `CONTROLPLANE_EXTRACTOR=llm`.

> **Gate D1:** the refund response text alone yields its six claims with correct kinds and
> hedging; no `Claim(...)` literal remains in the demo path.

### D2 — Binder v2 *(Phase 2 — the pivotal day)*

Four routes: numeric recomputation with Indian and Western digit normalization; a structural
symbol table; BM25 over the provenance set with a three-band entailment gate; derived claims
that recompute or return `UNKNOWN`. `CONTRADICTED` and `UNKNOWN` both become reachable, which
brings `Block` and the entire Unknown column alive. Fixtures locked out of enforce mode.

> **Gate D2:** refund reproduces Edit + Escalate (held) with **zero fixtures**; all sixteen
> matrix cells have a reaching test; `grep fixture` over the demo path is empty.

### D3 — Leakage and the corpus *(Phase 3 + Phase 4a)*

Aho-Corasick PII with checksum detectors (PAN, Aadhaar/Verhoeff, Luhn, IFSC, email, phone).
Rule A — a PII-shaped entity binding to no span forces the contradicted column. Fix the three
reference use cases so an ACL violation is possible in them at all. Then build the 150–200 case
labeled corpus, hard negatives included.

> **Gate D3:** fabricated PAN → Block at R3; entitled real PAN → Pass; unentitled real PAN →
> entitlement path. Corpus loads and runs.

### D4 — The numbers and the lanes *(Phase 4b/c + Phase 5)*

`make eval` prints per-route precision, recall, FPR and FNR each with a Wilson interval, plus
the confusion matrix and abstention rate. Dead compute by exact backward walk, priced. A
10,000-request bench with per-stage breakdown. Then real per-lane deadlines, where a miss
returns `UNKNOWN` resolved by that tier's fail stance.

> **Gate D4:** real numbers printed. **From this moment, no artifact may quote any number these
> commands did not produce.** This is the freeze line for Track B.

### D5 — Governance, feedback, bias, multi-turn *(Phase 6 + Phase 7)*

Jurisdiction axis that changes behavior (EU AI Act Art. 14 · DPDP Act 2023 · GDPR Art. 22).
Override capture into the chained ledger, feeding labels; thresholds move only behind a printed
shadow-replay delta; canary auto-rollback past 3× baseline. Bias as counterfactual flip rate
with a confidence interval. The multi-turn beat: a turn-one hedged claim inherited by a
turn-three irreversible action, escalated.

> **Gate D5:** jurisdiction divergence proven by test; bias reports a flip rate with its
> interval; multi-turn scenario runs end to end.

### D6 — Track B sprint *(all four artifacts)*

Everything in §4 below, produced in one day against frozen numbers, with D7 held in reserve for
a video re-record.

> **Gate D6:** all five deliverables exist and `make verify` is green.

### D7 *(reserve)* — Verify, dry run, submit

`make verify` runs preflight, tests, content laws, eval and bench, then diffs every number
printed against every number quoted in the PDF and the deck. Any drift fails. Then a security
review, a high-effort code review, and a determinism check. Then the submission dry run in §5.

---

## 4. Track B — the four artifacts

### 4a. Prototype video

**Format:** `.mp4`, 1920×1080, screen capture with voiceover. Target **3:30–4:00**.
*The portal does not state a length limit — check the brief and the portal before recording;
if a limit exists it governs.*

**It is a prototype video, not a pitch video.** No slides. The screen shows the system running.

| Time | Beat | On screen |
|---|---|---|
| 0:00–0:20 | **The failure** | The ungated response, plain: *"Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement."* Confidence 0.94. Every filter passed it. Money moved Tuesday, found Friday. **Clause 7.2 does not exist.** |
| 0:20–0:40 | **The reframe** | `STEP → SPAN → CLAIM → ACTION`. "An AI response is not text to be scored — it is a set of claims requesting permission to act." |
| 0:40–2:00 | **Mechanism, live** | Paste the response *fresh*. Six claims extract themselves, typed. The symbol table prints — 4.1, 4.3, 9.1; **no 7.2**. The amount recomputes: `₹1,84,000 ≡ 184000 INR`. The HR span's ACL excludes the caller. Two pending actions priced separately: `show_text` R1 → **Edit**; `issue_refund` R3 → **Escalate, held**. Sub-millisecond. Zero LLM. |
| 2:00–2:30 | **The flip** | Same span. Same claim. Same graph. Change only the caller. `analyst_01` → Edit. `hr_partner_01` → Pass. "No output-only checker can do this, because none of them carry identity into the verification layer." |
| 2:30–3:10 | **The numbers** | `make eval` → per-route precision, recall, FPR, **FNR with its confidence interval**. Dead compute: of nine tool calls, four grounded nothing. "Every team will claim detection. We publish what we miss." |
| 3:10–3:30 | **Close** | *"That system was never asked to prove anything. Now nothing acts until it can prove it should."* |

**Production rules.** Rehearse the exact command sequence until it runs clean — a fumble on
camera cannot be edited around convincingly. Large terminal font. Nothing personal on screen:
no other tabs, no notifications, no home-directory paths in frame. Record voiceover separately
so a stumble costs one take, not the whole run. No music, or barely any. Export well under any
upload cap.

**Never say "blocked" about the refund.** Say *held and escalated with the evidence packet.*
This is content law #2 and it is the single most likely on-camera slip.

### 4b. README PDF

A distinct document from the business proposal. This is what a judge reads to understand the
repository, and it is where the honesty move lives.

1. **What this is** — one paragraph.
2. **The mechanism** — the `STEP → SPAN → CLAIM → ACTION` diagram and the frozen matrix.
3. **Run it in sixty seconds** — copy-pasteable commands with their expected output.
4. **What to look at** — the three demos, each with its expected verdict.
5. **Capability ledger — proven vs. designed.** Every mechanism in the architecture, marked
   *implemented and tested* / *implemented, prototype-grade* / *designed, not built*. This
   preempts every "is any of this real?" question by answering it before it is asked, and it is
   the same move as publishing the false-negative rate.
6. **Evidence** — test count, eval table, latency table, all reproducible by named command.
7. **Repository map.**

Built by a script so it regenerates from source and cannot drift.

### 4c. Business Proposal PDF — rebuild

`scripts/build_proposal_pdf.py` already exists and renders from
`round2/CONTROLPLANE_R2_FINAL.md`. The rebuild carries: the real eval table, the published FNR
with its interval, dead compute priced, the jurisdiction packs, and the honest
proven-vs-designed line. The brief asks for problem framing, solution design, target users,
business case and impact, a phased roadmap, and key risks with mitigations — audit that all
seven are present and titled as such, because that list is the rubric.

Fix the known cosmetic defect: some Unicode arrows render as `■` in the current build.

### 4d. Pitch PPTX — rebuild

Rebuild from `submission/ControlPlane_Round2_Pitch.js` so deck and proposal cannot diverge.
Same number freeze. Content laws run over the deck's extracted text in CI.

---

## 5. Submission-day dry run

Run this once end-to-end before touching the portal.

1. `make verify` — green, no drift between printed and quoted numbers.
2. Clone the public repo **into a fresh directory**, follow the README PDF's sixty-second path
   verbatim, and confirm the three demos produce their stated verdicts. If a clean clone does
   not run, nothing else matters.
3. Confirm CI is green on the exact commit the link points at.
4. Play the video start to finish. Listen for the word "blocked."
5. Open both PDFs and the PPTX; confirm every number matches `make verify`'s output.
6. Check each file against the portal's type and size limits.
7. Upload. Screenshot the confirmation.

---

## 6. Risk register — submission-specific

| Risk | Mitigation |
|---|---|
| `gh auth` stays broken and the repo never goes public | D0 task, seven days early, and it needs a human — do it first, today |
| Video records the fixtures | Track B cannot start before Gate D4; the ordering is the control |
| A number in the deck drifts from a number in the code | `make verify` diffs quoted against printed and fails the build |
| Saying "blocked" on camera | Content law #2 in CI for text; for the video, a rehearsed script and a listen-back pass in the dry run |
| A clean clone does not run | Step 2 of the dry run tests exactly this, from a fresh directory |
| Repo history exposes the fixture commit | Judges read `HEAD`. The arc reads as engineering judgment; the alternative — a one-commit repo — reads worse |
| Video exceeds an unstated length or size cap | Confirm the cap from the portal before recording, not after |
| A week is not a year | Phases are ordered by score per hour. Stopping after D4 still lands ~90 with all five deliverables present |
