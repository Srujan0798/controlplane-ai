# ControlPlane.ai — HANDOFF

**Accenture Innovation Challenge 2026 · Round 1 · Problem Statement #1**
Team **ControlPlane** — Choda Srujan Sai (Team Leader) · Dhrithika — both IIT Gandhinagar

> Read this file first. Then run `python3 gate.py`. If it prints **30/30**, the package on
> disk is the one that was signed off. If it prints less, something changed — the failing line
> names what.

---

## 1. UPLOAD THIS — nothing else

```text
submission/ControlPlane_ControlPlane-ai.pptx    2.5 MB   3 slides
submission/ControlPlane_ControlPlane-ai.pdf     3.5 MB   3 pages
submission/ControlPlane_ControlPlane-ai.mp4     5.9 MB   2:25
```

**Never upload `submission/official/`.** It is a 7-slide build of the official Accenture
template. The brief says *"Concept Deck: Pitch deck (Max 3 slides) per team"* and the portal form
says *"2-3 slides."* Seven slides scores zero however well it renders. It exists only as a
fallback if the portal turns out to demand the template wrapper — and if it ever does, rebuild it
at three content slides, not seven.

Portal form, verbatim: 2–3 slides PPTX ≤20 MB · same 2–3 slides PDF ≤20 MB ·
2–3 minute video MP4/MOV ≤20 MB.

---

## 2. STATE — ship gate 30/30

```text
frozen copy intact (verify_content)      S2 severity fall monotonic   sat 36 > 29 > 10
BRIEF Q1 detect, three axes              S2 PASS visible on ground    dlum 25
BRIEF Q2 block/edit/escalate             S2 footer text clears AA     6.3:1
BRIEF Q3 latency on-slide                S2 latency out-reads gloss   1538 vs 422 px
BRIEF who it would help                  S3 closer/title >= 1.4x      1.69x
BRIEF why it matters                     S3 dead band < 15%           0.0%
S1 cause outranks effect  321 vs 195     S3 'prove' clears AA large   5.3:1
S1 no false left hotspot  0 px           PDF embeds full 5760 master
S1 red centroid on failure x.70 y.71     3 slides / 3 pages
S1 failure is brightest   L202           video 2:00-3:00              2:25
S1 failure is densest     5.3%           video shows real slide 2/3   MAD 0.2 / 0.1
S1 red on failure chain   85%            video: every held card moves min MAD 1.9
S1 capture label AA       5.5:1          audio: no mid-film dropout   longest 1.0s
no sideways text on s1                   closing hold is silent       7.5s
                                         all 3 uploads < 20 MB
```

All five of the brief's demands are answerable from the slides alone — nothing essential lives
only in the narration.

---

## 3. REPO

```text
SEBI/
  HANDOFF.md            this file
  gate.py               ★ the ship gate — 30 checks, run it before any upload
  verify_content.py     frozen-copy + banned-motif check (gate.py runs it first)
  build_submission.py   -> submission/            3-slide package  ← THE UPLOAD
  build_official.py     -> submission/official/   7-slide fallback ← NEVER UPLOAD
  build_video.py        -> video/*.mp4
  visuals/
    s1_page.py          slide 1 graph, CSS grid — deck AND video Beat 3
    pages.py            slides 2/3, video-slide poster, all 34 video frames
    tokens.py           colour / font tokens
    render.py           Playwright HTML -> PNG   posters dpr=3, frames dpr=2
  posters/              s1 s2 s3 sv .png at 5760x3240
  video/                frames/ · vo/ (NOT regenerable) · the encoded mp4
  archive/
    docs/               FROZEN spec, 1,915 lines — read it, never write it
    tools/              the official AIC template
    proposals/          stage 2-5 raw model outputs (the evidence trail)
    legacy/             dead code + superseded plans
```

### Build, in this order

```bash
cd /Users/srujansai/Desktop/SEBI
python3 -m visuals.render        # posters + video frames
python3 build_video.py           # MP4 — must run AFTER render
python3 build_submission.py      # the upload package
python3 build_official.py        # fallback only
python3 gate.py                  # must print 30/30
```

**Order matters.** Encoding before re-rendering leaves the video showing an older graph than the
deck. That failed the gate twice.

---

## 4. WHAT THE THREE SLIDES ARE

**Slide 1 — the graph.** STEP → SPAN → CLAIM → ACTION. Five claims bind to evidence; `clause 7.2`
does not, so a ₹1,84,000 payment is **held**. Three axes read one graph: cost backward,
responsibility by labels, performance forward. *Answers the brief's Q1 (detection).*

**Slide 2 — the matrix.** Blast radius × verdict severity, R3 at top, worst verdict left. The
Block→Pass fall reads as a saturation gradient. *Answers Q2 (block/edit/escalate) and Q3 (latency,
in the footer's own row).*

**Slide 3 — credibility and close.** Four claims this team refuses to make, a per-route gate
report in terminal format with deliberately empty fields, the beneficiary line, and the closer:
*"Now nothing acts until it can prove it should."* *Answers "who it helps" and "why it matters."*

---

## 5. FROZEN — read `archive/docs/`, never write it

`FINAL-ARCHITECTURE.md` · `STAGE3-NARRATIVE.md` · `STAGE4-DECK.md` · `STAGE5-VIDEO.md` ·
`ELEVATION-FINAL.md` · `SUBMISSION-PACKAGE.md`

These are the drawing specification, not captions. Treating them as captions is the diagnosis
every early pass recorded about itself.

### Content law — seven models tested this against each other

- **Never "blocked" about the refund.** R3 × unsupported-categorical = **Escalate**. Say *held and escalated*.
- **The company wrongly pays out ₹1,84,000.** The customer did not lose money.
- Actuators are exactly **Block · Edit · Escalate · Pass**.
- Latency is **≤40 ms p50 / ≤200 ms p95**.
- The FNR block keeps `<measured>` placeholders and the `illustrative format` label.
  **The emptiness is the credibility play. Never fill it.**
- **No strikethrough on S3** — it renders unreliably across PowerPoint/Keynote/Slides.
- S3's left column is the **refuse-to-claim** list (about *us*), not rejected approaches.
- No padlock, shield, eye, dashboard. No "first true AI control plane."
- **Slide count: 3. Hard cap.**

### Visual rules that are advisory, not law

`STAGE4`/`ELEVATION` also carry layout guesses written by text models that never saw a rendered
pixel — node counts, opacity percentages, "55–60% of slide area." **Where the render disagrees,
the render wins.** Two live examples: the nine STEP rows are deliberately *labelled* (untagged
ticks read as nine empty boxes), and the context-assembly label is *horizontal* (the spec freezes
the dashed boundary, not the label's orientation — sideways it was unreadable at laptop scale).

---

## 6. THE FIVE STANDING REVIEWER REQUESTS I DECLINED, AND WHY

Reviewers will raise these again. Each trades something scored for something cosmetic.

| Request | Why it is declined |
|---|---|
| Delete the Bias/Safety line on s2 | It is the deck's only coverage of two of the brief's three responsibility categories. Round 1 has no Q&A, so anything off-slide is never scored. |
| Cut the four `REFUSED` markers on s3 | STAGE4 specifies them: claim at 40% opacity + a small `refused` marker + correction at full weight. The marker is what makes the pattern parse as refusal rather than quotation. |
| Fill the `<measured>` FNR fields | The emptiness *is* the argument. A Round 1 deck inventing a precision figure is exactly what slide 3 refuses to do. |
| Re-time the video to graph ≤55% / matrix ≥20% | Derived from nearest-poster MAD, which on mostly-dark 16:9 frames is dominated by shared black background. Demonstrated inverted: the matrix at t=110 scores MAD 9.4 against slide 1 while the graph at t=100 scores 26.1. Hitting those numbers means cutting frozen script. |
| Recolour the ESCALATE hero to red | White on `#3350F5` measures 5.82:1 and works. Red would collide with the failure language on s1. |

---

## 7. FAILURES NEVER TO REINTRODUCE

1. **Deleting template slides before adding new ones** (in `build_official.py`). python-pptx
   reuses part names, recompression collapses the duplicate, and the Video + Thank-you slides
   vanish silently. It appends first, then deletes, then asserts 7.
2. **Letterboxing the posters.** They are placed at `(0, 0, 13.333, 7.5)` — full bleed.
3. **Encoding the video before re-rendering frames.** Deck and video diverge.
4. **Case-insensitive banned-token checks.** `STREAM` the invented actuator must not match
   `streams` in "text streams with a short hold-back."
5. **Writing the same artifact to several places.** The mp4 once existed in four copies.
   `video/` is the only build output; `submission/` the only upload location.
6. **`fps=25` must precede `zoompan`** in `build_video.py`. The concat demuxer emits one frame per
   still — without it the whole video collapses to 1.4 seconds.

---

## 8. THE ONE LESSON WORTH CARRYING FORWARD

**A failing check is a hypothesis about a defect, not proof of one.** Three of this project's own
gate checks had to be corrected rather than the design they were testing:

- raw red-pixel count → **saliency** (a dim full-width line out-counts a bright block while losing the glance)
- RGB distance → **saturation** (the frozen requirement is a hot-red-to-cool-grey severity fall; RGB distance scores grey above saturated colour)
- audio dropout → **mid-film dropout** (the closing hold is silent *by frozen direction*)

And three reviewer metrics did not survive verification either — footer contrast measured 5.70:1
not 3.3:1, s1 red was 177 components not 603, and the "s3 dead band" turned out to contain the
refuse list and the gate report.

**Verify the measurement before you act on it.** Check file mtimes too — several reviews scored a
build two commits stale and reported defects that were already closed.

---

## 9. IF SOMETHING LOOKS WRONG

Name the **one** worst element in one phrase — "S1 ACTION plate too airy", "S2 row labels small" —
fix that exact spot, re-render, and **look at the built PDF at 1400px**, not the 5760 poster.
Nearly every defect found late in this project was visible only at laptop scale.

Then run `python3 gate.py`. It is the contract.
