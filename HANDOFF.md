# ControlPlane.ai — HANDOFF

Accenture Innovation Challenge 2026 · Round 1 · Team **ControlPlane**
Choda Srujan Sai (Team Leader) · Dhrithika — both IIT Gandhinagar

> This is the only status document. Anything in `archive/legacy/` describing a broken team
> slide, a stale MP4, or a failing official builder is superseded — those are fixed.

---

## 1. UPLOAD THIS

**Primary — official AIC template, 7 slides:**

```text
submission/official/ControlPlane_ControlPlane-ai.pptx    3.84 MB   7 slides
submission/official/ControlPlane_ControlPlane-ai.pdf     3.11 MB   7 pages
submission/official/ControlPlane_ControlPlane-ai.mp4     7.01 MB   2:57
```

Order: **Cover · Team details · Graph · Matrix · Credibility · Video · Thank you.**
The template's "Instructions — remove before submission" slide and both 200-word placeholders are
deleted. No "All fields are mandatory" text remains. Team slide carries real data, CS/DH
monograms, and `TEAM NAME: ControlPlane`. The video slide shows the closing transcript frame.

**Fallback — content slides only**, if the portal rejects the wrapper:

```text
submission/ControlPlane_ControlPlane-ai.pptx             1.53 MB   3 slides
submission/ControlPlane_ControlPlane-ai.pdf              2.07 MB   3 pages
submission/ControlPlane_ControlPlane-ai.mp4              7.01 MB   2:57
```

Identical content slides in both. Everything is far under the 20 MB cap.

---

## 2. GATE — 11/11

```text
official pptx = 7 slides   PASS     posters current      PASS
official pdf  = 7 pages    PASS     decks current        PASS
portal pptx   = 3 slides   PASS     all 6 files < 20 MB  PASS
portal pdf    = 3 pages    PASS     no cruft anywhere    PASS
video 2:57                 PASS     no dead imports      PASS
video matches graph        PASS

python3 verify_content.py  ->  ALL CONTENT CHECKS: PASS
```

**Reproducibility proven:** every poster and frame was deleted and rebuilt from source — the
posters come back byte-identical (`s1 821dbd9d… · s2 72f57b3d… · s3 a52ebfac…`).

---

## 3. REPO

```text
SEBI/
  HANDOFF.md              this file — the only status doc
  build_official.py       -> submission/official/   (7-slide AIC package)
  build_submission.py     -> submission/            (3-slide package)
  build_video.py          -> video/*.mp4
  verify_content.py       content + banned-motif gate
  visuals/
    s1_page.py            slide 1 graph (CSS grid) — deck AND video Beat 3
    pages.py              s2, s3, video-slide poster, all video frames
    tokens.py             colour / font tokens
    render.py             Playwright: HTML -> PNG   posters dpr=3, frames dpr=2
    _html/                intermediate HTML (regenerable)
  posters/                s1 s2 s3 sv .png
  submission/             ★ UPLOAD — 3-slide package + official/ 7-slide package
  video/                  frames/ · vo/ · the encoded mp4
  archive/
    docs/                 FROZEN source content — read it, never write it
    tools/                the official AIC template
    proposals/            stage 2–5 raw model outputs
    legacy/               dead code + superseded plans, kept for history
```

### Build

```bash
cd /Users/srujansai/Desktop/SEBI
python3 -m visuals.render        # posters + video frames
python3 build_video.py           # MP4 — must run AFTER render
python3 build_submission.py      # 3-slide package
python3 build_official.py        # 7-slide official package
python3 verify_content.py        # must print PASS
```

**Order matters.** Encoding before re-rendering leaves the video showing an older graph than the
deck. That failed the gate twice.

---

## 4. WHAT SLIDE 1 IS NOW

**It no longer comes from an SVG renderer.** The old `graph.py` drew s1 as one string with ~200
hand-placed coordinates, so nothing responded to anything else and every edit opened a void or a
collision somewhere new. s2 and s3 used CSS grid and landed at 9/10 immediately. That contrast was
the root cause of twenty passes that never converged. `graph.py` is in `archive/legacy/`.

s1 is **`visuals/s1_page.py`** — same graph, real layout engine. Three defects became
*structurally impossible* rather than repeatedly patched:

| Was | Now |
|---|---|
| bindings drifted out of line with span cards | spans + claims share **one 6-row grid** |
| a connector could point at a span that isn't there | row 6's span slot is an **empty dashed ghost** |
| the ACTION plate opened a 496 px void | flex column carrying all six frozen elements |

**Deck and video are one drawing.** Beat 3's 18 frames call `s1_body()` with state flags; hidden
elements use `visibility:hidden`, so the grid holds its shape and the graph builds in place.

**One typographic system.** All three slides use the same serif display (Charter) against
monospace machine records — the typography of an audit exhibit, which is the thesis.

---

## 5. CHANGE MAP

| To change… | Edit | Where |
|---|---|---|
| S1 step names / which are dead | `visuals/s1_page.py` | `STEPS` |
| S1 spans / claims | `visuals/s1_page.py` | `SPANS`, `CLAIMS` |
| S1 column widths | `visuals/s1_page.py` | `COLS` |
| S1 colour / type | `visuals/s1_page.py` | `CSS` `:root` |
| S1 video reveal states | `visuals/s1_page.py` | `s1_body()` flags |
| S2 matrix cells / strip | `visuals/pages.py` | `poster_s2()` |
| S3 refusals / FNR rows / closer | `visuals/pages.py` | `poster_s3()` |
| Team details | `build_official.py` | `TEAM` |
| Official slide order | `build_official.py` | `_reorder(...)` in `build()` |
| Poster sharpness | `visuals/render.py` | `device_scale_factor` |
| PPTX/PDF quality | `build_submission.py`, `build_official.py` | `JPEG_Q` |
| Video bitrate / beats | `build_video.py` | `TARGET`, `BEATS` |

---

## 6. FROZEN — READ, NEVER WRITE

`archive/docs/FINAL-ARCHITECTURE.md` · `STAGE3-NARRATIVE.md` · `STAGE4-DECK.md` ·
`STAGE5-VIDEO.md` · `ELEVATION-FINAL.md` · `SUBMISSION-PACKAGE.md`

They are the drawing specification, not captions. Treating them as captions is the diagnosis every
earlier pass recorded about itself.

### Content law — verified by seven models against each other

- **Never "blocked" about the refund.** R3 × unsupported-categorical = **Escalate**. Say *held and escalated*.
- **The company wrongly pays out ₹1,84,000.** The customer did not lose money.
- Actuators are exactly **Block · Edit · Escalate · Pass**. No `STREAM`, `Kill Span`, `Terminate Step`.
- Latency is **≤40 ms p50 / ≤200 ms p95**. Never `40 ms p95`, never `<5 ms`.
- FNR block keeps `<measured>` placeholders and the `illustrative format` label.
- **No strikethrough on S3** — it breaks across PowerPoint/Keynote/Slides. Opacity + `REFUSED` + correction.
- S3's left column is the **refuse-to-claim** list (claims about us), not rejected approaches.
- No padlock, shield, eye, dashboard. No "first true AI control plane". No "brand debt".

### Visual rules that are advisory, not law

`STAGE4`/`ELEVATION` also carry layout guesses written by text models that never saw a rendered
pixel and were never validated — *"nine steps as untagged ticks"*, *"55–60 % of slide area"*, node
counts, opacity percentages. **Where the render disagrees, the render wins.** The nine STEP rows
are deliberately **labelled** with tool calls; untagged ticks read as nine empty boxes and made the
cost axis unreadable.

---

## 7. FAILURES NEVER TO REINTRODUCE

1. **Deleting template slides before adding new ones.** python-pptx reuses part names
   (`slide6.xml`), recompression collapses the duplicate, and Video + Thank-you vanish silently.
   `build_official.py` appends first, then deletes, then asserts 7 slides.
2. **Letterboxing the posters.** Placed at `(0, 0, 13.333, 7.5)` — full bleed, no chrome.
3. **Encoding the video before re-rendering frames.** Deck and video diverge.
4. **Case-insensitive banned-token checks.** `STREAM` the invented actuator must not match
   `streams` in "text streams with a short hold-back". `verify_content.py` keeps *must_contain*
   case-insensitive and *must_not_contain* case-**sensitive**.
5. **Writing the same artifact to several places.** The mp4 once existed in four copies. `video/`
   is the only build output; `submission/` is the only upload location.

---

## 8. IF SOMETHING LOOKS WRONG

Name the **one** worst element in one phrase — "S1 ACTION plate too airy", "S2 row labels small" —
fix that exact spot via the change map, re-render, and **look at the built PDF**, not the poster.
Every defect found in the last session was visible only in the PDF.
