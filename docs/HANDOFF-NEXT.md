# HANDOFF — craft pass + ship-day state

**Read `HANDOFF.md` first.** This file only records what changed after it, why, and the two
traps that cost the most time today. Submission is **today**.

---

## 0. STOP — read this before you run any build

**Do not run `build_video.py` while another agent/session is running it.** It writes a shared
temp file `video/_raw.mp4`, then muxes audio onto it. A second concurrent run deletes or
overwrites that temp mid-encode, and the mux then fails with `moov atom not found`
(ffmpeg exit 183 / 254). The result is either a build error **or, worse, a corrupt mp4 that
still has a plausible size and duration** — one such file measured 8,663 H.264 decode errors.

**Second trap: never chain render → video in one shell invocation.** The x264 pass gets
truncated when it starts while Chromium's memory from `visuals.render` is still held. Symptom:
ffmpeg reports `speed=107x elapsed=0:00:01.34` for 3,628 4K frames, which is impossible — a
real encode of this film takes **~94 seconds** (`speed≈1.5x`). A fast "success" is a truncated
`_raw.mp4`. Run them as **separate invocations** and check the raw before muxing:

```bash
python3 -m visuals.render          # invocation 1
python3 build_video.py             # invocation 2 — ~95s, do not background-chain it
ffprobe -v error -show_entries format=duration -of csv=p=0 video/_raw.mp4   # must not error
```

### The only acceptable pre-upload proof

```bash
python3 gate.py                     # must print 30/30
ffmpeg -v error -i submission/ControlPlane_ControlPlane-ai.mp4 -f null - 2>&1 | wc -l   # must be 0
ffprobe -v error -show_entries format=duration -of csv=p=0 submission/ControlPlane_ControlPlane-ai.mp4
```

Duration must be **145.2s (2:25)**. The portal floor is 2:00 — a truncated build produced
**1:37**, which is out of spec and would have been rejected. `TARGET = 145.2` in `build_video.py`.

---

## 1. Known-open items (as of this writing)

| Item | Fix |
|---|---|
| `S2 latency row out-reads glossary` failing (~3067 vs ~4038) | `.foot .gloss` has been brightened again. Set it back to `font-size:12.5px; color:#A8A4AE`. That is 6.6:1 (clears AA) **and** keeps the latency row leading, which commit `1862cb9` deliberately established. |
| mp4 may be 1:37 and/or corrupt | Re-encode per §0 and verify duration + decode errors. |

---

## 2. Design decisions — please do not revert these

The brief was "the submission looks vibecoded, make it professional." Every item below is a
fix for that, verified at 1400px (laptop scale), not on the 5760 master.

**Glow is the single biggest tell of AI-generated dark UI. There is now none in the deck.**
Emphasis comes from fill + keyline + scale + a dark isolation moat (`box-shadow:0 0 0 Npx
var(--ground)`), never from a bloom. A `0 28px 110px rgba(red,.88)` halo was removed from the
s1 clause card, and `0 26px 88px` blue + `0 0 70px` red from the s2 hero. Both were re-added
later at lower alpha and removed again. **A moat is structural; a bloom is atmosphere.**

- **s2 hero**: blue fill `#3350F5` + white type + a light `2px` keyline. It previously carried a
  5px **red** border on a saturated **blue** fill — two accent hues fighting on the one object
  the slide exists to deliver. Red belongs on s1, where failure lives. (`HANDOFF.md` §6 is right
  that the hero must not be recoloured red — the fix was removing the border, not the fill.)
- **s1 ✗ deleted**: it was two crossed gradients + a drop-shadow floating in a gutter, and it
  restated what "no span", "UNSUPPORTED" and "HELD — not executed" already say three times.
  Replaced by a **terminated trace** — the gate line runs in from the claim and stops at a
  terminator bar. An open circuit says "does not reach" in the grid's own vocabulary.
- **Violet retired.** Four colours have jobs: red=unproven, blue=escalate, amber=edit,
  grey=bound/pass. Violet had none. The `14` chip is now a neutral outlined badge.
- **s1 capture label** is `#A9AEBA` (8.6:1). It had been set to `#6E657A`, which measures
  **3.5:1 and fails AA** — see §3.
- **EDIT cells** `#2A2013 / #CE9A52`. The old `#2A2410` sat at G/R 0.86 — yellow-green, which
  reads as dirt rather than as a severity step.
- **s2 column-2 bracket** is ONE continuous outline (`.colmark`), outset from the cells. Four
  `inset 3px` edges on four cells split by a 7px grid gap rendered as a **seam**, not a bracket.
- **s1 axis rules** span the full width of the column they measure. As orphan 12px ticks the row
  read as unfinished; ACTION carrying no rule now parses as deliberate (it is the outcome, not
  an axis).
- **s1 graph edges** are `#5A6070` at full opacity. At `opacity:.5` they resolved to ~`#414650`
  and vanished at laptop scale — the slide claims "one graph" and the bindings must be visible.
- **s1 HELD box** is deliberately *quieter* than the clause card (2px border, `#4A1014`). The
  frozen law is **cause outranks effect**; brightening HELD to `#62161E`/3px inverted it
  (236 vs 248 red px) and failed the gate.
- **s1 headline stays grey.** This is load-bearing, not a defect: `S1 failure is brightest`
  requires the failure to out-luminance the headline. Do not "fix" it to white.

### Frozen content that was deleted and has been restored

Both were explicitly declined in `HANDOFF.md` §6 and were removed anyway:

1. **Bias/Safety line on s2** — the deck's only coverage of two of the brief's three
   responsibility categories. Round 1 has no Q&A, so anything off-slide is never scored.
   `verify_content.py` now asserts `counterfactual flip rate` and `typed interlocks`; it had
   no guard, which is why it vanished silently.
2. **The four `REFUSED` markers on s3** — removed as "stamp spam". Without the marker each row
   parses as quote-then-remark; only the headline says they are refusals, and four items get
   four separate reads.

---

## 3. Five gate checks were measuring nothing. They are fixed.

`HANDOFF.md` §8 says a failing check is a hypothesis about a defect. The converse bit us harder:
**a passing check can be a hypothesis about nothing.** Each of these was green while measuring a
colour that was not on the slide, or a band containing no content.

| Check | What was wrong |
|---|---|
| `S1 capture label clears AA` | Hardcoded `#9A78D8` and reported 5.5:1 while the slide had drifted to `#6E657A` — **an actual 3.5:1 AA failure, hidden by a green light.** |
| `S2 footer text clears AA` | Hardcoded `#20242E`, then `#C4C0CA`; both stopped matching the CSS. |
| `S1 failure is brightest` | The "rupee" reference band sampled `y .34–.46`, which went empty when the ACTION plate moved to `space-between`. Reported `L0` and passed **against nothing**. |
| `S2 severity fall monotonic` | Row bands were hardcoded pixel offsets. Changing the header row 74→96px left them averaging dark plate into a cell, reading a monotonic 37 > 27 > 14 fall as *inverted*. **Now detected from the render.** |
| `S1 red is on the failure chain` | Credited only the 12 largest connected components. With a bloom, red merged into two giant blobs → 85%. Without it the same red sits in more, smaller pieces → 71%, while actually being **more** concentrated (93%). The metric rewarded glow. **Now measured by location**, which is what its name claims. |

Two assertions were added so a band that misses its row **fails loudly instead of passing on
emptiness** (`s2 footer bands missed their rows`, `expected 4 matrix rows`). Thresholds were
never lowered.

**Rule going forward:** if you recolour an element whose hex is hardcoded in `gate.py`, change
it in the same commit. If you move layout, prefer detecting the band over re-hardcoding it.

---

## 4. Video encoding

- `-b:v 4200k` (was 1500k). At 1500k over 3840×2160 (~0.007 bpp) x264 skips static macroblocks
  outright: the slow zoom push was quantised away and **40→100s decoded pixel-identical**. The
  film genuinely looked frozen. Headroom was never the constraint — 20 MB cap, ~7–9 MB used.
- `noise=all_seed=20260815` — seeded. Unseeded grain made `video: every held card moves` bounce
  **1.9 / 1.6 / 0.0 across three runs on identical frames**; the check was reading dither.
- Whole-film motion should read median ≈3.4 MAD over 6s windows, with no window below ~0.5.

---

## 5. Files touched

`visuals/s1_page.py` · `visuals/pages.py` · `gate.py` · `verify_content.py` · `build_video.py`
· `build_submission.py` (`JPEG_Q` 96→97)

All uncommitted. A snapshot of the pre-existing uncommitted work is in this session's scratchpad
as `backup-1518/uncommitted.patch`.

Stray untracked `s1.png` `s2.png` `s3.png` in the repo root are 1400px review renders that
leaked out of a review script — no build reads them (builds read `posters/`). Safe to delete.

`submission/official/` is still **never uploaded** (7 slides; the brief caps at 3). Note its
`sv.png` reads "VIDEO · 2:58" while the film is 2:25 — latent, harmless while unused.
