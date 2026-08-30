#!/usr/bin/env python3
"""One-time patch to submission/ControlPlane_Round2_Pitch.js.

Fixes, in one atomic pass:
  1. Chrome renumber (the "09 // ROADMAP" collision; makes 09..14 sequential).
  2. Eyebrow renumber to match new chrome (off-by-one + collision).
  3. Reconcile "~40,000 / week" -> "Tens of thousands / week (directional)"
     in both the on-slide text and the speaker notes (matches proposal §4).
  4. Insert a dedicated Team slide between MATRIX and ROADMAP.
  5. Update the ASK header comment to reflect new slide count.

After this runs the deck has 15 slides numbered 00..14 with consistent
chrome + eyebrow labels and no "~40k/week" drift vs the proposal.

Idempotency: refuses to run if any anchor is missing or non-unique.
"""
from __future__ import annotations

import sys
from pathlib import Path

P = Path("submission/ControlPlane_Round2_Pitch.js")
t = P.read_text(encoding="utf-8")
orig_len = len(t)

TEAM_SLIDE = '''
// =====================================================================
// SLIDE — TEAM (inserted between MATRIX and ROADMAP)
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "10 // TEAM");
  notes(s,
    "Two-person team. Srujan owns architecture, mechanism, the demo build, and the latency and eval numbers. Dhrithika owns narrative, the pitch, and hostile-Q&A defense. Both can draw the matrix from memory and answer B1 and B5 without hesitating. The repo is the proof: 36 modules, 50+ tests, frozen matrix, deterministic rebuild of every portal artifact from measured JSON."
  );

  eyebrow(s, "10 · TEAM", 1.04, 1.00, 8);
  headline(s, [
    { text: "THE TEAM THAT " },
    { text: "BUILT IT", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.34, w: 17.9, h: 0.62, size: 32 });
  s.addText("Two people. One graph. Every portal artifact regenerated from measured JSON.", {
    x: 1.04, y: 1.98, w: 17.9, h: 0.36,
    fontFace: FONT, fontSize: 17, color: C.warm, margin: 0,
  });

  const team = [
    {
      name: "CHODA SRUJAN SAI",
      role: "ARCHITECTURE  ·  MECHANISM  ·  DEMO",
      bio: "Designs the interlock, builds the gate, runs the load bench. Owns the latency and eval numbers and the reproducible rebuild of every portal artifact.",
      tag: "controlplane/interlock.py  ·  scripts/load_bench.py  ·  scripts/build_*_pdf.py",
    },
    {
      name: "DHRITHIKA",
      role: "NARRATIVE  ·  PITCH  ·  HOSTILE Q&A",
      bio: "Owns the story arc and the room defense. Leads the hostile-Q&A drill (B1 and B5 hardest) and keeps the vocabulary disciplined (admit, authorise, hold — never watch, detect, trust).",
      tag: "round2/R2S5.md  ·  docs/JUDGE_RUNBOOK.md  ·  docs/reference/QA.md",
    },
  ];
  team.forEach((m, i) => {
    const x = 1.04 + i * 9.10;
    card(s, x, 2.78, 8.86, 5.20, C.panel, C.rust, 1.1);
    rustBar(s, x, 2.78, 8.86);
    s.addText(m.name, {
      x: x + 0.30, y: 3.00, w: 8.26, h: 0.42,
      fontFace: FONT, fontSize: 22, bold: true, color: C.cream, charSpacing: 1.2, margin: 0,
    });
    s.addText(m.role, {
      x: x + 0.30, y: 3.52, w: 8.26, h: 0.32,
      fontFace: FONT, fontSize: 13, color: C.rust, charSpacing: 1.6, margin: 0,
    });
    s.addText(m.bio, {
      x: x + 0.30, y: 3.98, w: 8.26, h: 1.80,
      fontFace: FONT, fontSize: 15, color: C.warm, margin: 0, valign: "top",
    });
    s.addText(m.tag, {
      x: x + 0.30, y: 6.10, w: 8.26, h: 1.70,
      fontFace: FMONO, fontSize: 12, color: C.muted, margin: 0, valign: "top",
    });
  });

  card(s, 1.04, 8.18, 17.92, 2.18);
  s.addText("IIT GANDHINAGAR  ·  TEAM CONTROLPLANE  ·  ACCENTURE INNOVATION CHALLENGE 2026  ·  PS #1", {
    x: 1.36, y: 8.42, w: 17.3, h: 0.36,
    fontFace: FONT, fontSize: 15, bold: true, color: C.cream, charSpacing: 1.4, margin: 0,
  });
  s.addText("Public GitHub: github.com/Srujan0798/controlplane-ai  ·  branch main  ·  frozen tag v0.2.0-round2.", {
    x: 1.36, y: 8.86, w: 17.3, h: 0.36,
    fontFace: FONT, fontSize: 14, color: C.warm, margin: 0,
  });
  s.addText("Every artifact in /submission regenerates from the live JSON. make verify is the source of truth — if a number is not in submission/latency_bench.json, it does not exist.", {
    x: 1.36, y: 9.28, w: 17.3, h: 0.78,
    fontFace: FONT, fontSize: 14, color: C.muted, margin: 0, valign: "top",
  });
}
'''

replacements = [
    # 1. Chrome renumber — fixes the "09 // ROADMAP" collision (slide 11).
    # After Team insert, the sequence is 00..14; we shift slides 11..14 by +1
    # (ROADMAP 09->10, FNR 10->11, MEASURED 11->12, ASK 12->13) and the Team
    # slide will take chrome "10 // TEAM", pushing ROADMAP/FNR/MEASURED/ASK to
    # 11..14. See the TEAM_SLIDE insert below for the order.
    ('chrome(s, "09 // ROADMAP");',          'chrome(s, "11 // ROADMAP");'),
    ('chrome(s, "10 // FNR");',              'chrome(s, "12 // FNR");'),
    ('chrome(s, "11 // MEASURED");',         'chrome(s, "13 // MEASURED");'),
    ('chrome(s, "12 // ASK", true);',        'chrome(s, "14 // ASK", true);'),
    # 2. Eyebrow renumber to match the new chrome sequence.
    ('eyebrow(s, "07 · WHY NOT", 1.04, 1.00, 10);',
     'eyebrow(s, "08 · WHY NOT", 1.04, 1.00, 10);'),
    ('eyebrow(s, "08 · MULTI-USE-CASE", 1.04, 1.00, 12);',
     'eyebrow(s, "09 · MULTI-USE-CASE", 1.04, 1.00, 12);'),
    ('eyebrow(s, "10 · BUSINESS CASE + ROADMAP", 1.04, 1.00, 14);',
     'eyebrow(s, "11 · BUSINESS CASE + ROADMAP", 1.04, 1.00, 14);'),
    ('eyebrow(s, "11 · RISKS WE PUBLISH", 1.04, 1.00, 12);',
     'eyebrow(s, "12 · RISKS WE PUBLISH", 1.04, 1.00, 12);'),
    ('eyebrow(s, "12 · WHAT WE MEASURED  ·  AND WHAT WE REFUSE TO CLAIM", 1.04, 1.00, 14);',
     'eyebrow(s, "13 · WHAT WE MEASURED  ·  AND WHAT WE REFUSE TO CLAIM", 1.04, 1.00, 14);'),
    ('eyebrow(s, "12 · ASK", 1.04, 1.15, 8);',
     'eyebrow(s, "14 · ASK", 1.04, 1.15, 8);'),
    # 3. Reconcile ~40,000 / week with proposal's "tens of thousands/week (directional)".
    ('s.addText("~40,000 / week", {',
     's.addText("Tens of thousands / week  (directional)", {'),
    ('forty thousand interactions a week',
     'tens of thousands of interactions a week (directional)'),
    # 5. Update the ASK header comment to reflect the new (post-insert) count.
    ('// SLIDE 13 — ASK / CLOSE',
     '// SLIDE 15 — ASK / CLOSE'),
]

applied = 0
for old, new in replacements:
    if old not in t:
        sys.exit(f"ANCHOR NOT FOUND:\n{old[:140]}")
    if t.count(old) != 1:
        sys.exit(f"ANCHOR NOT UNIQUE ({t.count(old)} occurrences):\n{old[:140]}")
    t = t.replace(old, new, 1)
    applied += 1

# 4. Insert the Team slide immediately before the (now-renumbered) ASK block.
ask_anchor = '// SLIDE 15 — ASK / CLOSE'
if ask_anchor not in t:
    sys.exit("ASK anchor not found for Team insertion")
if t.count(ask_anchor) != 1:
    sys.exit(f"ASK anchor not unique ({t.count(ask_anchor)})")
# Insert: put TEAM_SLIDE + a blank line, then keep the separator comment line
# that immediately precedes the ASK block intact.
t = t.replace(ask_anchor, TEAM_SLIDE + ask_anchor, 1)
applied += 1

P.write_text(t, encoding="utf-8")
print(f"applied {applied} patches; {orig_len} -> {len(t)} bytes ({len(t)-orig_len:+d})")
