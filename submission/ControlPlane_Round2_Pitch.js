// ControlPlane.ai — Round 2 pitch
// Accenture Innovation Challenge 2026 · PS #1 · Team ControlPlane
// Rebuild: node submission/ControlPlane_Round2_Pitch.js
// Measured numbers load from evals/last_run.json + submission/latency_bench.json.

const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

function _pct(x, digits) {
  return `${(Number(x) * 100).toFixed(digits)}%`;
}

function loadMeasured() {
  const evalPath = path.join(__dirname, "..", "evals", "last_run.json");
  const benchPath = path.join(__dirname, "latency_bench.json");
  const evRaw = JSON.parse(fs.readFileSync(evalPath, "utf8"));
  const bench = JSON.parse(fs.readFileSync(benchPath, "utf8"));
  const ev = evRaw.summary || evRaw;
  const fnr = ev.ungrounded_fnr_wilson;
  const fpr = ev.passable_fpr_wilson;
  const hn = ev.hard_negative_hold_wilson;
  const ungrounded = (ev.action_level && ev.action_level.ungrounded) || {};
  const caution = (ev.action_level && ev.action_level.hard_negative_caution) || {};
  const g = bench.gate_latency_ms || {};
  if (!fnr || !fpr || !hn || g.p50 == null) {
    throw new Error("eval/bench JSON missing required measured fields");
  }
  const missIds = ungrounded.miss_ids || [];
  return {
    nCases: ev.n_cases,
    fnr: _pct(fnr[0], 1),
    fnrLo: _pct(fnr[1], 1),
    fnrHi: _pct(fnr[2], 1),
    fpr: _pct(fpr[0], 1),
    fprHi: _pct(fpr[2], 1),
    hn: `${Math.round(Number(hn[0]) * 100)}%`,
    hnLo: _pct(hn[1], 1),
    hnHi: _pct(hn[2], 1),
    hnTotal: caution.total,
    hnShare: ev.n_cases ? _pct(caution.total / ev.n_cases, 1) : "n/a",
    nUngrounded: (ungrounded.held || 0) + (ungrounded.missed || 0),
    missIds: missIds.join(", ") || "named in evals/last_run.json",
    nBench: bench.n,
    p50: Number(g.p50).toFixed(2),
    p95: Number(g.p95).toFixed(2),
    p99: Number(g.p99).toFixed(2),
  };
}

const M = loadMeasured();

pres.defineLayout({ name: "BASED_WIDE", width: 20, height: 11.25 });
pres.layout = "BASED_WIDE";
pres.author = "ControlPlane · Choda Srujan Sai · Dhrithika";
pres.company = "IIT Gandhinagar";
pres.title = "ControlPlane.ai — Round 2 Pitch";
pres.subject = "Admission-control layer for AI that acts · Accenture Innovation Challenge 2026 · PS #1";

const C = {
  bgBase: "120806",
  bgBaseAlt: "0A0504",
  bgWarm: "2A120C",
  panel: "1A0D0A",
  border: "3A1E16",
  borderHi: "5A2E20",
  rust: "D9482A",
  cream: "F2E3D5",
  muted: "7A5D4E",
  warm: "C9B5A3",
  amber: "F2C572",
  hiFill: "2A140F",
};

const FONT = "Arial";
const FMONO = "Courier New";
const SW = 20.0;
const SH = 11.25;

function chrome(s, sectionLabel, useDarkBg = false) {
  s.background = { color: useDarkBg ? C.bgBaseAlt : C.bgBase };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: SW, h: SH,
    fill: { color: C.bgWarm, transparency: 70 },
    line: { type: "none" },
  });

  s.addText("◢", {
    x: 0.42, y: 0.44, w: 0.23, h: 0.25,
    fontFace: FONT, fontSize: 12, color: C.rust, margin: 0,
  });
  s.addText("CONTROLPLANE//SYS", {
    x: 0.68, y: 0.42, w: 4.20, h: 0.29,
    fontFace: FONT, fontSize: 15, color: C.cream, charSpacing: 1.5, margin: 0,
  });
  s.addText(sectionLabel, {
    x: 12.6, y: 0.42, w: 6.8, h: 0.29,
    fontFace: FONT, fontSize: 15, color: C.muted, charSpacing: 1.5, margin: 0,
    align: "right",
  });
  s.addText("◣", {
    x: 19.44, y: 0.44, w: 0.23, h: 0.25,
    fontFace: FONT, fontSize: 12, color: C.rust, margin: 0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.42, y: 10.66, w: 0.10, h: 0.10,
    fill: { color: C.rust }, line: { type: "none" },
  });
  s.addText("ADMIT//PROVE", {
    x: 0.62, y: 10.59, w: 2.4, h: 0.29,
    fontFace: FONT, fontSize: 15, color: C.muted, margin: 0,
  });
  s.addText("AIC.2026 · PS #1 · IITGN", {
    x: 14.6, y: 10.59, w: 4.9, h: 0.29,
    fontFace: FONT, fontSize: 15, color: C.muted, charSpacing: 1.5, margin: 0,
    align: "right",
  });
}

function eyebrow(s, text, x, y, w = 18.45, align = "left") {
  s.addText(text, {
    x, y, w, h: 0.29,
    fontFace: FONT, fontSize: 15, color: C.rust, charSpacing: 3, margin: 0,
    align,
  });
}

function headline(s, runs, opts) {
  const arr = runs.map((r) => ({
    text: r.text,
    options: {
      bold: true,
      color: r.accent ? C.rust : C.cream,
      fontFace: FONT,
      fontSize: opts.size || 54,
      charSpacing: -0.75,
    },
  }));
  s.addText(arr, {
    x: opts.x, y: opts.y, w: opts.w, h: opts.h,
    align: opts.align || "left", margin: 0, valign: opts.valign || "top",
  });
}

function card(s, x, y, w, h, fill = C.panel, borderC = C.border, lineW = 0.68) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: fill },
    line: { color: borderC, width: lineW },
  });
}

function divider(s, x, y, w, color = C.border, h = 0.01) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color }, line: { type: "none" },
  });
}

function panel(s, x, y, w, h, leftLabel, rightLabel) {
  card(s, x, y, w, h, C.panel, C.borderHi, 0.68);
  divider(s, x + 0.01, y + 0.48, w - 0.02, C.border, 0.01);
  const leftW = rightLabel ? w * 0.54 - 0.22 : w - 0.36;
  s.addText(leftLabel, {
    x: x + 0.18, y: y + 0.08, w: leftW, h: 0.32,
    fontFace: FONT, fontSize: 13, color: C.muted, charSpacing: 1.2, margin: 0,
  });
  if (rightLabel) {
    s.addText(rightLabel, {
      x: x + w * 0.58, y: y + 0.08, w: w * 0.42 - 0.20, h: 0.32,
      fontFace: FONT, fontSize: 13, color: C.muted, charSpacing: 1.0, margin: 0,
      align: "right",
    });
  }
}

function ascii(s, x, y, w, h, lines, color = C.rust, sz = 12) {
  const arr = lines.map((ln, i) => ({
    text: ln,
    options: {
      fontFace: FMONO, fontSize: sz, color,
      breakLine: i < lines.length - 1,
    },
  }));
  s.addText(arr, { x, y, w, h, margin: 0, valign: "top" });
}

function chip(s, x, y, w, h, text, textColor, lineColor) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { type: "none" },
    line: { color: lineColor, width: 0.68 },
  });
  s.addText(text, {
    x: x + 0.14, y: y + 0.06, w: w - 0.24, h: h - 0.10,
    fontFace: FONT, fontSize: 14, color: textColor, charSpacing: 1.2, margin: 0, valign: "middle",
  });
}

function rustBar(s, x, y, w) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h: 0.045,
    fill: { color: C.rust }, line: { type: "none" },
  });
}

function notes(s, text) {
  s.addNotes(text);
}

// =====================================================================
// SLIDE 1 — TITLE
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "00 // TITLE");
  notes(s,
    "ControlPlane is an admission-control layer for AI. Enterprises moved from AI that answers to AI that acts. We authorise the action. We do not score the paragraph."
  );

  s.addText("ACCENTURE INNOVATION CHALLENGE 2026  ·  ROUND 2  ·  TRACK 1", {
    x: 1.04, y: 1.85, w: 9.6, h: 0.32,
    fontFace: FONT, fontSize: 14, color: C.rust, charSpacing: 2.2, margin: 0,
  });

  s.addText([
    { text: "CONTROL", options: { bold: true, color: C.cream, fontFace: FONT, fontSize: 72, charSpacing: -2 } },
    { text: "PLANE", options: { bold: true, color: C.rust, fontFace: FONT, fontSize: 72, charSpacing: -2 } },
    { text: ".AI", options: { bold: true, color: C.cream, fontFace: FONT, fontSize: 72, charSpacing: -2 } },
  ], { x: 1.04, y: 2.28, w: 9.7, h: 1.15, margin: 0, valign: "middle" });

  s.addText("Admission-control layer for AI that acts", {
    x: 1.04, y: 3.52, w: 9.6, h: 0.48,
    fontFace: FONT, fontSize: 24, color: C.warm, margin: 0,
  });

  s.addText("We authorise the action. We do not score the paragraph.", {
    x: 1.04, y: 4.08, w: 9.6, h: 0.42,
    fontFace: FONT, fontSize: 18, color: C.muted, margin: 0,
  });

  chip(s, 1.04, 4.78, 2.55, 0.42, "◉  PS #1", C.rust, C.rust);
  chip(s, 3.75, 4.78, 3.15, 0.42, "IIT GANDHINAGAR", C.warm, C.border);
  chip(s, 7.06, 4.78, 3.55, 0.42, "TEAM CONTROLPLANE", C.warm, C.border);

  s.addText("CHODA SRUJAN SAI  ·  DHRITHIKA", {
    x: 1.04, y: 9.55, w: 9.6, h: 0.32,
    fontFace: FONT, fontSize: 16, color: C.cream, charSpacing: 1.5, margin: 0,
  });
  s.addText("IIT GANDHINAGAR  ·  PROBLEM STATEMENT #1", {
    x: 1.04, y: 9.90, w: 9.6, h: 0.28,
    fontFace: FONT, fontSize: 14, color: C.muted, charSpacing: 1.2, margin: 0,
  });

  panel(s, 11.20, 1.70, 7.76, 8.20, "▸ PRIMITIVE // ONE GRAPH", "LANE 1");
  const graphRows = [
    { a: "STEP", v: "produces", b: "SPAN" },
    { a: "SPAN", v: "binds", b: "CLAIM" },
    { a: "CLAIM", v: "authorizes", b: "ACTION" },
  ];
  graphRows.forEach((g, i) => {
    const y = 2.58 + i * 0.62;
    s.addText(g.a, {
      x: 11.52, y, w: 1.55, h: 0.48,
      fontFace: FMONO, fontSize: 15, bold: true, color: C.cream, margin: 0, valign: "middle",
    });
    s.addText("→  " + g.v + "  →", {
      x: 13.10, y, w: 2.90, h: 0.48,
      fontFace: FONT, fontSize: 13, color: C.rust, margin: 0, valign: "middle", align: "center",
    });
    s.addText(g.b, {
      x: 16.05, y, w: 2.10, h: 0.48,
      fontFace: FMONO, fontSize: 15, bold: true, color: C.amber, margin: 0, valign: "middle",
    });
  });

  s.addText("FOUR NODES. THREE READS.", {
    x: 11.48, y: 4.85, w: 7.20, h: 0.32,
    fontFace: FONT, fontSize: 14, color: C.amber, charSpacing: 1.8, margin: 0,
  });

  const reads = [
    { n: "01", t: "PERFORMANCE", d: "Does each claim bind to a span?" },
    { n: "02", t: "COST", d: "Did each step ground an accepted claim?" },
    { n: "03", t: "RESPONSIBILITY", d: "Is the caller entitled to every bound span?" },
  ];
  reads.forEach((r, i) => {
    const y = 5.35 + i * 1.12;
    s.addText(r.n, {
      x: 11.48, y, w: 0.70, h: 0.36,
      fontFace: FONT, fontSize: 16, bold: true, color: C.rust, margin: 0,
    });
    s.addText(r.t, {
      x: 12.22, y, w: 5.9, h: 0.32,
      fontFace: FONT, fontSize: 16, bold: true, color: C.cream, charSpacing: 1.2, margin: 0,
    });
    s.addText(r.d, {
      x: 12.22, y: y + 0.34, w: 5.9, h: 0.36,
      fontFace: FONT, fontSize: 15, color: C.warm, margin: 0,
    });
  });
}

// =====================================================================
// SLIDE 2 — PROBLEM
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "01 // PROBLEM");
  notes(s,
    "A refund agent emitted that sentence. Confidence point-nine-four. Money moved Tuesday, found Friday. Clause 7.2 does not exist. The company wrongly paid one lakh eighty-four thousand rupees. The system didn't fail. It was never asked to prove anything. Oversight is still built for the answering era: score the text, chart the failure, review the log next week. The cost of a wrong output changed category. It used to be a bad paragraph. It is now an executed transaction."
  );

  eyebrow(s, "01 · PROBLEM", 1.04, 1.00, 8.0);
  headline(s, [
    { text: "IT USED TO BE A BAD " },
    { text: "PARAGRAPH", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.36, w: 17.9, h: 0.78, size: 36 });

  s.addText("It is now an executed transaction.", {
    x: 1.04, y: 2.14, w: 17.9, h: 0.40,
    fontFace: FONT, fontSize: 22, color: C.warm, margin: 0,
  });

  panel(s, 1.04, 2.68, 11.15, 5.55, "▸ UNGATED OUTPUT", "CONF 0.94 · ALL FILTERS PASS");
  s.addText("“Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.”", {
    x: 1.38, y: 3.40, w: 10.45, h: 2.15,
    fontFace: FONT, fontSize: 28, italic: true, color: C.cream, margin: 0,
  });
  divider(s, 1.38, 5.70, 10.45);
  s.addText("MONEY MOVED TUESDAY.  FOUND FRIDAY.", {
    x: 1.38, y: 5.90, w: 10.45, h: 0.40,
    fontFace: FONT, fontSize: 18, bold: true, color: C.amber, charSpacing: 1.4, margin: 0,
  });
  s.addText("Every filter passed it. Oversight scored the text. The payout had already cleared.", {
    x: 1.38, y: 6.40, w: 10.45, h: 0.85,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });

  card(s, 12.45, 2.68, 6.51, 5.55, C.panel, C.rust, 1.1);
  rustBar(s, 12.45, 2.68, 6.51);
  s.addText("THE COMPANY PAID", {
    x: 12.75, y: 2.90, w: 5.95, h: 0.32,
    fontFace: FONT, fontSize: 14, color: C.muted, charSpacing: 2, margin: 0,
  });
  s.addText("₹1,84,000", {
    x: 12.75, y: 3.28, w: 5.95, h: 1.05,
    fontFace: FONT, fontSize: 48, bold: true, color: C.cream, margin: 0,
  });
  s.addText("CLAUSE 7.2 DOES NOT EXIST.", {
    x: 12.75, y: 4.42, w: 5.95, h: 0.70,
    fontFace: FONT, fontSize: 20, bold: true, color: C.rust, margin: 0,
  });
  s.addText("Not a cap. Not a denial. Not “doesn’t cover.” The clause is absent from the vendor agreement.", {
    x: 12.75, y: 5.20, w: 5.95, h: 1.35,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });
  s.addText("The customer did not lose it.\nThe company wrongly paid it.", {
    x: 12.75, y: 6.65, w: 5.95, h: 1.05,
    fontFace: FONT, fontSize: 16, color: C.cream, margin: 0,
  });

  card(s, 1.04, 8.52, 17.92, 1.68);
  s.addText("THE SYSTEM DIDN'T FAIL. IT WAS NEVER ASKED TO PROVE ANYTHING.", {
    x: 1.36, y: 8.68, w: 17.3, h: 0.42,
    fontFace: FONT, fontSize: 20, bold: true, color: C.cream, charSpacing: 0.6, margin: 0,
  });
  s.addText("Oversight is still built for the answering era: score the text, chart the failure, review the log next week. The cost of a wrong output changed category.", {
    x: 1.36, y: 9.16, w: 17.3, h: 0.72,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });
}

// =====================================================================
// SLIDE 3 — INSIGHT
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "02 // INSIGHT");
  notes(s,
    "Every oversight tool inspects what the model said. The only thing that can prove it is the evidence assembled before the model ran — and that record is thrown away the moment generation starts. Everyone watches the exit. Nobody records the entrance. ControlPlane keeps the receipts. That turns hallucination checking from a judgment call into a set-membership test, and turns oversight from scoring text into authorising actions."
  );

  eyebrow(s, "02 · INSIGHT", 1.04, 1.00, 8.0);
  headline(s, [
    { text: "EVERYONE WATCHES THE EXIT." },
  ], { x: 1.04, y: 1.36, w: 17.9, h: 0.70, size: 36 });
  s.addText("Nobody records the entrance.", {
    x: 1.04, y: 2.10, w: 17.9, h: 0.42,
    fontFace: FONT, fontSize: 24, color: C.rust, margin: 0,
  });

  const insights = [
    {
      n: "01",
      t: "RECEIPTS, NOT THE MODEL'S MIND",
      d: "We sit at the I/O layer. Evidence is captured at context assembly — source, ACL, hash, offsets — then frozen. The model cannot invent a span after the fact.",
    },
    {
      n: "02",
      t: "SET-MEMBERSHIP, NOT JUDGMENT",
      d: "The verdict is a set-membership test against evidence captured before generation. Not an opinion about finished text. Binding either exists or it does not.",
    },
    {
      n: "03",
      t: "DEFAULT: UNSUPPORTED",
      d: "A claim must earn SUPPORTED. Nothing passes because nobody objected. Absence of evidence is not conflicting evidence — the claim stays unproven.",
    },
  ];
  insights.forEach((c, i) => {
    const x = 1.04 + i * 6.10;
    card(s, x, 2.78, 5.90, 6.00);
    rustBar(s, x, 2.78, 5.90);
    s.addText(c.n, {
      x: x + 0.32, y: 3.05, w: 5.26, h: 0.40,
      fontFace: FONT, fontSize: 18, bold: true, color: C.rust, charSpacing: 2, margin: 0,
    });
    s.addText(c.t, {
      x: x + 0.32, y: 3.55, w: 5.26, h: 1.35,
      fontFace: FONT, fontSize: 22, bold: true, color: C.cream, margin: 0,
    });
    s.addText(c.d, {
      x: x + 0.32, y: 5.05, w: 5.26, h: 3.20,
      fontFace: FONT, fontSize: 16, color: C.warm, margin: 0, valign: "top",
    });
  });

  s.addText("We read the model's receipts, not the model's mind.  ·  Oversight becomes authorising actions.", {
    x: 1.04, y: 9.00, w: 17.92, h: 0.36,
    fontFace: FONT, fontSize: 16, color: C.muted, margin: 0,
  });
}

// =====================================================================
// SLIDE 4 — PRIMITIVE
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "03 // PRIMITIVE");
  notes(s,
    "An AI response is not text to be scored. It is a set of claims requesting permission to act. We capture every span at context assembly — source, ACL, hash, offsets — then freeze. The model cannot invent a span after the fact, and it has no channel to declare a binding. Performance reads the graph forward. Cost reads it backward. Responsibility reads the labels. Everywhere else that's three products. Here it's three questions on one graph."
  );

  eyebrow(s, "03 · PRIMITIVE", 1.04, 1.00, 10);
  headline(s, [
    { text: "AN AI RESPONSE IS A SET OF " },
    { text: "CLAIMS", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.34, w: 17.9, h: 0.62, size: 32 });
  s.addText("Not text to be scored. Claims requesting permission to act.", {
    x: 1.04, y: 1.98, w: 17.9, h: 0.34,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });

  const nodes = [
    { n: "STEP", sub: "produces", d: "Tool call, retrieval, model turn." },
    { n: "SPAN", sub: "binds", d: "Chunk, tool row, DB record — source, ACL, hash, offsets." },
    { n: "CLAIM", sub: "authorizes", d: "Typed atomic proposition from the output stream." },
    { n: "ACTION", sub: "", d: "Pending side effect: tool + args + irreversibility." },
  ];
  nodes.forEach((n, i) => {
    const x = 1.04 + i * 4.68;
    card(s, x, 2.48, 4.42, 2.55, C.panel, i === 3 ? C.rust : C.borderHi, i === 3 ? 1.1 : 0.68);
    s.addText("0" + (i + 1), {
      x: x + 0.22, y: 2.62, w: 1.2, h: 0.30,
      fontFace: FONT, fontSize: 13, color: C.rust, charSpacing: 1.5, margin: 0,
    });
    s.addText(n.n, {
      x: x + 0.22, y: 2.94, w: 3.98, h: 0.48,
      fontFace: FONT, fontSize: 26, bold: true, color: C.cream, margin: 0,
    });
    s.addText(n.d, {
      x: x + 0.22, y: 3.48, w: 3.98, h: 1.20,
      fontFace: FONT, fontSize: 15, color: C.warm, margin: 0, valign: "top",
    });
    if (i < 3) {
      s.addText("▶", {
        x: x + 4.28, y: 3.35, w: 0.38, h: 0.40,
        fontFace: FONT, fontSize: 16, bold: true, color: C.rust, margin: 0,
      });
    }
  });

  const q = [
    { dir: "→", t: "PERFORMANCE", qn: "Does each claim bind to a span?" },
    { dir: "←", t: "COST", qn: "Did each step ground any accepted claim?" },
    { dir: "≡", t: "RESPONSIBILITY", qn: "Is the caller entitled to every span a claim binds to?" },
  ];
  q.forEach((r, i) => {
    const x = 1.04 + i * 6.10;
    card(s, x, 5.24, 5.90, 2.35);
    s.addText(r.dir + "  " + r.t, {
      x: x + 0.28, y: 5.42, w: 5.34, h: 0.36,
      fontFace: FONT, fontSize: 15, bold: true, color: C.rust, charSpacing: 1.4, margin: 0,
    });
    s.addText(r.qn, {
      x: x + 0.28, y: 5.88, w: 5.34, h: 1.30,
      fontFace: FONT, fontSize: 18, color: C.cream, margin: 0, valign: "top",
    });
  });

  card(s, 1.04, 7.78, 17.92, 2.42, C.panel, C.rust, 1.0);
  s.addText("KEYSTONE  ·  PROVENANCE RECORDER", {
    x: 1.36, y: 7.96, w: 17.3, h: 0.32,
    fontFace: FONT, fontSize: 14, color: C.rust, charSpacing: 1.8, margin: 0,
  });
  s.addText("Everywhere else that's three products. Here it's three questions on one graph.", {
    x: 1.36, y: 8.34, w: 17.3, h: 0.48,
    fontFace: FONT, fontSize: 22, bold: true, color: C.cream, margin: 0,
  });
  s.addText("Hooks context assembly, not the model. Spans freeze before generation. The model has no channel to declare a binding. Actuators: Block · Edit · Escalate · Pass.", {
    x: 1.36, y: 8.90, w: 17.3, h: 0.95,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });
}

// =====================================================================
// SLIDE 5 — DEMO: CLAUSE 7.2 UNSUPPORTED
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "04 // DEMO 01");
  notes(s,
    "The Provenance Recorder captured five spans before the model ran. Vendor agreement, order lookup, an HR note, FAQ, CRM. Clause 7.2 is in none of them, because clause 7.2 does not exist. The claim stays UNSUPPORTED. Not contradicted — there is nothing to contradict. Not low confidence. Unproven. The claim carries the burden of proof. Nothing passes because nobody objected."
  );

  eyebrow(s, "04 · DEMO 01 / 03  ·  python3 examples/refund_trace_demo.py", 1.04, 1.00, 17.9);
  headline(s, [
    { text: "NOT LOW CONFIDENCE. " },
    { text: "UNPROVEN", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.34, w: 17.9, h: 0.62, size: 32 });

  panel(s, 1.04, 2.10, 8.55, 3.55, "▸ CLAIM  clause_72", "kind=structural · categorical");
  s.addText("“Clause 7.2 permits this refund”", {
    x: 1.32, y: 2.78, w: 8.05, h: 0.70,
    fontFace: FONT, fontSize: 22, italic: true, color: C.cream, margin: 0,
  });
  s.addText("Roles:  issue_refund,  show_text", {
    x: 1.32, y: 3.52, w: 8.05, h: 0.32,
    fontFace: FONT, fontSize: 15, color: C.muted, margin: 0,
  });
  s.addText("Five spans at context assembly. No span for clause 7.2.", {
    x: 1.32, y: 3.92, w: 8.05, h: 0.55,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });
  s.addText("VERDICT   UNSUPPORTED    spans=(none)", {
    x: 1.32, y: 4.55, w: 8.05, h: 0.70,
    fontFace: FMONO, fontSize: 16, bold: true, color: C.rust, margin: 0,
  });

  panel(s, 9.80, 2.10, 9.16, 3.55, "▸ SPANS AT ASSEMBLY", "n=5");
  const spans = [
    ["span-1", "doc:vendor-agreement-v3", "vendor-public"],
    ["span-2", "db:orders  ·  ORD-9", "vendor-public"],
    ["span-3", "doc:hr-exception-desk", "hr-confidential"],
    ["span-4", "doc:faq", "vendor-public"],
    ["span-5", "db:crm  ·  T-441", "vendor-public"],
  ];
  spans.forEach((row, i) => {
    const y = 2.72 + i * 0.52;
    s.addText(row[0], {
      x: 10.05, y, w: 1.35, h: 0.42,
      fontFace: FMONO, fontSize: 13, color: C.amber, margin: 0, valign: "middle",
    });
    s.addText(row[1], {
      x: 11.45, y, w: 4.55, h: 0.42,
      fontFace: FONT, fontSize: 14, color: C.cream, margin: 0, valign: "middle",
    });
    s.addText(row[2], {
      x: 16.05, y, w: 2.65, h: 0.42,
      fontFace: FONT, fontSize: 13, color: C.muted, margin: 0, valign: "middle",
    });
  });

  const tblRows = [
    [
      { text: "claim_id", options: { fill: { color: C.hiFill }, color: C.muted, bold: true, fontFace: FONT, fontSize: 13, align: "left", valign: "middle", margin: [7, 8, 7, 8] } },
      { text: "verdict", options: { fill: { color: C.hiFill }, color: C.muted, bold: true, fontFace: FONT, fontSize: 13, align: "left", valign: "middle", margin: [7, 8, 7, 8] } },
      { text: "spans", options: { fill: { color: C.hiFill }, color: C.muted, bold: true, fontFace: FONT, fontSize: 13, align: "left", valign: "middle", margin: [7, 8, 7, 8] } },
    ],
    [
      { text: "approval · amount · order · vendor_41 · hr_side", options: { fill: { color: C.panel }, color: C.cream, fontFace: FONT, fontSize: 14, valign: "middle", margin: [8, 8, 8, 8] } },
      { text: "SUPPORTED", options: { fill: { color: C.panel }, color: C.cream, bold: true, fontFace: FONT, fontSize: 14, valign: "middle", margin: [8, 8, 8, 8] } },
      { text: "span-1 / span-2 / span-3", options: { fill: { color: C.panel }, color: C.warm, fontFace: FMONO, fontSize: 13, valign: "middle", margin: [8, 8, 8, 8] } },
    ],
    [
      { text: "clause_72", options: { fill: { color: "2A0C08" }, color: C.cream, bold: true, fontFace: FONT, fontSize: 15, valign: "middle", margin: [8, 8, 8, 8] } },
      { text: "UNSUPPORTED", options: { fill: { color: "2A0C08" }, color: C.rust, bold: true, fontFace: FONT, fontSize: 15, valign: "middle", margin: [8, 8, 8, 8] } },
      { text: "(none)", options: { fill: { color: "2A0C08" }, color: C.rust, bold: true, fontFace: FMONO, fontSize: 15, valign: "middle", margin: [8, 8, 8, 8] } },
    ],
  ];
  s.addTable(tblRows, {
    x: 1.04, y: 5.85, w: 17.92, h: 2.15,
    colW: [8.2, 4.4, 5.32],
    border: [{ pt: 0.5, color: C.border }, { pt: 0.5, color: C.border }, { pt: 0.5, color: C.border }, { pt: 0.5, color: C.border }],
    valign: "middle",
  });

  s.addText("Absence of evidence, not conflicting evidence — the claim stays UNSUPPORTED. Clause 7.2 does not exist.", {
    x: 1.04, y: 8.20, w: 17.92, h: 0.40,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });
  s.addText("The claim carries the burden of proof. Nothing passes because nobody objected.", {
    x: 1.04, y: 8.62, w: 17.92, h: 0.36,
    fontFace: FONT, fontSize: 16, color: C.muted, margin: 0,
  });
}

// =====================================================================
// SLIDE 6 — DEMO: R1 EDIT
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "05 // DEMO 02");
  notes(s,
    "One of those five spans did bind. The HR internal note. The claim is true — it is in the evidence. The caller is a customer-support agent with vendor-public clearance. The span is hr-confidential. Deterministic entitlement check: the ACL is not a subset of the caller's clearance. On the customer-visible text path — R1 — the matrix says Edit. Strip the unentitled span. Surgical, never generative. This is the incident output-only checkers cannot see: they never carry who is asking."
  );

  eyebrow(s, "05 · DEMO 02 / 03  ·  ENTITLEMENT", 1.04, 1.00, 17.9);
  headline(s, [
    { text: "RETRIEVAL IS NOT " },
    { text: "PERMISSION", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.34, w: 17.9, h: 0.62, size: 32 });

  panel(s, 1.04, 2.12, 9.05, 4.55, "▸ PENDING ACTION  show_text", "R1  ·  user-visible");
  s.addText("Show text to the customer", {
    x: 1.36, y: 2.78, w: 8.45, h: 0.36,
    fontFace: FONT, fontSize: 18, color: C.cream, margin: 0,
  });
  s.addText("Claim hr_side is SUPPORTED via span-3. The fact is in the evidence. The caller is not entitled to it.", {
    x: 1.36, y: 3.22, w: 8.45, h: 0.85,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });

  const facts = [
    ["CLAIM", "hr_side  ·  “customer account flagged for goodwill override”"],
    ["SOURCE", "doc:hr-exception-desk  ·  ACL {hr-confidential}"],
    ["PRINCIPAL", "cs-agent-17  ·  clearance {vendor-public}"],
    ["CHECK", "span ACL is not a subset of caller clearance"],
  ];
  facts.forEach((f, i) => {
    const y = 4.15 + i * 0.52;
    s.addText(f[0], {
      x: 1.36, y, w: 1.70, h: 0.42,
      fontFace: FONT, fontSize: 13, bold: true, color: C.rust, charSpacing: 1, margin: 0, valign: "middle",
    });
    s.addText(f[1], {
      x: 3.10, y, w: 6.70, h: 0.42,
      fontFace: FONT, fontSize: 14, color: C.cream, margin: 0, valign: "middle",
    });
  });

  card(s, 10.32, 2.12, 8.64, 4.55, C.panel, C.rust, 1.1);
  rustBar(s, 10.32, 2.12, 8.64);
  s.addText("ENTITLEMENT", {
    x: 10.64, y: 2.32, w: 8.05, h: 0.30,
    fontFace: FONT, fontSize: 13, color: C.muted, charSpacing: 2, margin: 0,
  });
  s.addText("VIOLATION", {
    x: 10.64, y: 2.68, w: 8.05, h: 0.70,
    fontFace: FONT, fontSize: 36, bold: true, color: C.rust, margin: 0,
  });
  s.addText("R1  ×  Contradicted / entitlement violation", {
    x: 10.64, y: 3.48, w: 8.05, h: 0.40,
    fontFace: FONT, fontSize: 16, color: C.amber, margin: 0,
  });
  s.addText("ACTUATOR", {
    x: 10.64, y: 4.10, w: 8.05, h: 0.28,
    fontFace: FONT, fontSize: 13, color: C.muted, charSpacing: 2, margin: 0,
  });
  s.addText("Edit", {
    x: 10.64, y: 4.42, w: 8.05, h: 0.58,
    fontFace: FONT, fontSize: 32, bold: true, color: C.cream, margin: 0,
  });
  s.addText("Unentitled span stripped. Surgical, never generative. Driving claims: hr_side, clause_72.", {
    x: 10.64, y: 5.12, w: 8.05, h: 1.15,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0, valign: "top",
  });

  card(s, 1.04, 6.90, 17.92, 3.30);
  s.addText("OUTPUT-ONLY CHECKERS NEVER CARRY WHO IS ASKING.", {
    x: 1.40, y: 7.12, w: 17.2, h: 0.40,
    fontFace: FONT, fontSize: 18, bold: true, color: C.cream, margin: 0,
  });
  s.addText("Deterministic entitlement check — set-membership on ACL ⊆ clearance. We do not fix their IAM. We stop the model silently bypassing the rights the source already carries.", {
    x: 1.40, y: 7.62, w: 17.2, h: 0.85,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });
  s.addText("Same string. Fine for one caller. A breach for another. Identity-blind tools cannot see this incident.", {
    x: 1.40, y: 8.55, w: 17.2, h: 1.15,
    fontFace: FONT, fontSize: 16, color: C.muted, margin: 0, valign: "top",
  });
}

// =====================================================================
// SLIDE 7 — DEMO: R3 ESCALATE
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "06 // DEMO 03");
  notes(s,
    "Same response. Second pending action: issue the refund. R3, irreversible, one lakh eighty-four thousand rupees. The driving claim is still clause 7.2, still unproven, still categorical. The matrix says Escalate. Held and escalated with the evidence packet — the claim, the empty span list, the verdict. Not an alert. The hash chain verifies. The customer-visible line is edited. The payout is held. Both are correct at the same time. Proof scales with consequence."
  );

  eyebrow(s, "06 · DEMO 03 / 03  ·  INTERLOCK  ·  RESOLUTION OF SLIDE 02", 1.04, 1.00, 17.9);
  headline(s, [
    { text: "PROOF SCALES WITH " },
    { text: "CONSEQUENCE", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.34, w: 17.9, h: 0.62, size: 32 });

  panel(s, 1.04, 2.12, 9.05, 5.55, "▸ PENDING ACTION  issue_refund", "R3  ·  irreversible");
  s.addText("Issue the refund  ·  ₹1,84,000  ·  ORD-9", {
    x: 1.36, y: 2.78, w: 8.45, h: 0.40,
    fontFace: FONT, fontSize: 18, color: C.cream, margin: 0,
  });
  const r3 = [
    ["DRIVING", "clause_72  ·  UNSUPPORTED  ·  categorical"],
    ["CELL", "R3 × Unsupported + categorical"],
    ["ACTUATOR", "Escalate  ·  held with the evidence packet"],
    ["PACKET", "unproven clause + empty span list + verdict"],
    ["LEDGER", "verify_chain() = True"],
  ];
  r3.forEach((f, i) => {
    const y = 3.32 + i * 0.72;
    s.addText(f[0], {
      x: 1.36, y, w: 1.85, h: 0.55,
      fontFace: FONT, fontSize: 13, bold: true, color: C.rust, charSpacing: 1, margin: 0, valign: "middle",
    });
    s.addText(f[1], {
      x: 3.28, y, w: 6.50, h: 0.55,
      fontFace: FONT, fontSize: 15, color: C.cream, margin: 0, valign: "middle",
    });
  });

  card(s, 10.32, 2.12, 8.64, 5.55, C.panel, C.amber, 1.1);
  rustBar(s, 10.32, 2.12, 8.64);
  s.addText("HELD AND ESCALATED", {
    x: 10.64, y: 2.36, w: 8.05, h: 0.30,
    fontFace: FONT, fontSize: 13, color: C.muted, charSpacing: 2, margin: 0,
  });
  s.addText("Escalate", {
    x: 10.64, y: 2.72, w: 8.05, h: 0.72,
    fontFace: FONT, fontSize: 40, bold: true, color: C.amber, margin: 0,
  });
  s.addText("with the evidence packet.\nNot an alert.", {
    x: 10.64, y: 3.50, w: 8.05, h: 0.95,
    fontFace: FONT, fontSize: 18, color: C.cream, margin: 0,
  });

  s.addText("SAME RESPONSE. TWO ACTUATORS.", {
    x: 10.64, y: 4.62, w: 8.05, h: 0.32,
    fontFace: FONT, fontSize: 13, color: C.muted, charSpacing: 1.6, margin: 0,
  });
  s.addText("show_text  →  Edit", {
    x: 10.64, y: 5.02, w: 8.05, h: 0.40,
    fontFace: FONT, fontSize: 20, bold: true, color: C.cream, margin: 0,
  });
  s.addText("issue_refund  →  Escalate", {
    x: 10.64, y: 5.46, w: 8.05, h: 0.40,
    fontFace: FONT, fontSize: 20, bold: true, color: C.amber, margin: 0,
  });
  s.addText("Text edited. Money held. Both correct at the same time.", {
    x: 10.64, y: 6.00, w: 8.05, h: 1.15,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });

  card(s, 1.04, 7.90, 17.92, 2.20);
  s.addText("The customer-visible line is edited. The payout is held. Hash chain verifies.", {
    x: 1.40, y: 8.12, w: 17.2, h: 0.42,
    fontFace: FONT, fontSize: 18, color: C.cream, margin: 0,
  });
  s.addText("R3 × unsupported-categorical routes to Escalate. Spoken word and grid agree: held and escalated with the evidence packet.", {
    x: 1.40, y: 8.62, w: 17.2, h: 1.05,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0, valign: "top",
  });
}

// =====================================================================
// SLIDE 8 — DEMO: PRINCIPAL FLIP
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "07 // DEMO 04");
  notes(s,
    "Same span. Same claim. Same hash. Only the caller changed. analyst_01 is not entitled to the HR-comp span — the matrix says Edit. hr_partner_01 is — Pass. Zero LLM in this path. The claim did not change. The evidence did not change. The access right did. This is the incident output-only checkers cannot see, and it is the argument against RAG groundedness made concrete: groundedness sees the retrieval and says supported; it never carries who is asking, so it cannot flip on identity."
  );

  eyebrow(s, "07 · DEMO 04 / 04  ·  ENTITLEMENT FLIP  ·  python3 examples/knowledge_flip_demo.py", 1.04, 1.00, 17.9);
  headline(s, [
    { text: "SAME SPAN. SAME CLAIM. SAME HASH." },
    { text: " ONLY THE CALLER CHANGED.", accent: true },
  ], { x: 1.04, y: 1.34, w: 17.9, h: 0.62, size: 26 });

  // Left pane: analyst_01 -> Edit
  card(s, 1.04, 2.30, 8.85, 6.70, C.panel, C.rust, 1.1);
  rustBar(s, 1.04, 2.30, 8.85);
  s.addText("analyst_01", {
    x: 1.36, y: 2.52, w: 8.20, h: 0.40,
    fontFace: FONT, fontSize: 20, bold: true, color: C.cream, margin: 0,
  });
  s.addText("clearance {analyst}  ·  span ACL {hr-comp-l6}", {
    x: 1.36, y: 2.96, w: 8.20, h: 0.34,
    fontFace: FONT, fontSize: 14, color: C.muted, margin: 0,
  });
  s.addText("content_hash  60d00e…f8603d", {
    x: 1.36, y: 3.46, w: 8.20, h: 0.34,
    fontFace: FMONO, fontSize: 14, color: C.amber, margin: 0,
  });
  s.addText("“L6 base range is confidential HR-partner material.”", {
    x: 1.36, y: 3.96, w: 8.20, h: 0.70,
    fontFace: FONT, fontSize: 16, italic: true, color: C.cream, margin: 0, valign: "top",
  });
  s.addText("span ACL ⊄ principal clearance  →  VIOLATION", {
    x: 1.36, y: 4.84, w: 8.20, h: 0.40,
    fontFace: FONT, fontSize: 15, color: C.rust, bold: true, margin: 0,
  });
  s.addText("CELL   R1 × Contradicted / entitlement violation", {
    x: 1.36, y: 5.34, w: 8.20, h: 0.32,
    fontFace: FONT, fontSize: 14, color: C.warm, margin: 0,
  });
  s.addText("ACTUATOR", {
    x: 1.36, y: 5.84, w: 8.20, h: 0.28,
    fontFace: FONT, fontSize: 13, color: C.muted, charSpacing: 2, margin: 0,
  });
  s.addText("Edit", {
    x: 1.36, y: 6.16, w: 8.20, h: 0.90,
    fontFace: FONT, fontSize: 40, bold: true, color: C.cream, margin: 0,
  });

  // Right pane: hr_partner_01 -> Pass
  card(s, 10.11, 2.30, 8.85, 6.70, C.panel, C.amber, 1.1);
  rustBar(s, 10.11, 2.30, 8.85);
  s.addText("hr_partner_01", {
    x: 10.43, y: 2.52, w: 8.20, h: 0.40,
    fontFace: FONT, fontSize: 20, bold: true, color: C.cream, margin: 0,
  });
  s.addText("clearance {hr-partner, hr-comp-l6}  ·  span ACL {hr-comp-l6}", {
    x: 10.43, y: 2.96, w: 8.20, h: 0.34,
    fontFace: FONT, fontSize: 14, color: C.muted, margin: 0,
  });
  s.addText("content_hash  60d00e…f8603d", {
    x: 10.43, y: 3.46, w: 8.20, h: 0.34,
    fontFace: FMONO, fontSize: 14, color: C.amber, margin: 0,
  });
  s.addText("“L6 base range is confidential HR-partner material.”", {
    x: 10.43, y: 3.96, w: 8.20, h: 0.70,
    fontFace: FONT, fontSize: 16, italic: true, color: C.cream, margin: 0, valign: "top",
  });
  s.addText("span ACL ⊆ principal clearance  →  OK", {
    x: 10.43, y: 4.84, w: 8.20, h: 0.40,
    fontFace: FONT, fontSize: 15, color: C.amber, bold: true, margin: 0,
  });
  s.addText("CELL   R1 × clean / supported", {
    x: 10.43, y: 5.34, w: 8.20, h: 0.32,
    fontFace: FONT, fontSize: 14, color: C.warm, margin: 0,
  });
  s.addText("ACTUATOR", {
    x: 10.43, y: 5.84, w: 8.20, h: 0.28,
    fontFace: FONT, fontSize: 13, color: C.muted, charSpacing: 2, margin: 0,
  });
  s.addText("Pass", {
    x: 10.43, y: 6.16, w: 8.20, h: 0.90,
    fontFace: FONT, fontSize: 40, bold: true, color: C.amber, margin: 0,
  });

  card(s, 1.04, 9.14, 17.92, 1.72);
  s.addText("ZERO LLM IN THIS PATH. Set-membership on ACL ⊆ clearance.", {
    x: 1.36, y: 9.30, w: 17.3, h: 0.40,
    fontFace: FONT, fontSize: 18, bold: true, color: C.cream, margin: 0,
  });
  s.addText("The claim is the same. The evidence is the same. Only the caller changed — and the actuator flips. Groundedness sees the retrieval and says supported; it never carries who is asking, so it cannot see this.", {
    x: 1.36, y: 9.74, w: 17.3, h: 0.90,
    fontFace: FONT, fontSize: 15, color: C.warm, margin: 0, valign: "top",
  });
}

// =====================================================================
// SLIDE 9 — WHY NOT
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "08 // NOT THESE");
  notes(s,
    "Guardrails match banned surface forms. Clause 7.2 is a well-formed sentence, so they admit it. Groundedness checkers average and cannot see who is asking, so they miss both the missing clause and the HR span. Confidence fails by definition: the failure mode is confidently wrong. The judge asks, does this look right? We ask, which span proves it? You cannot block, edit or escalate on eighty-seven."
  );

  eyebrow(s, "07 · WHY NOT", 1.04, 1.00, 10);
  headline(s, [
    { text: "THEY INSPECT THE OUTPUT. WE QUERY THE " },
    { text: "EVIDENCE", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.34, w: 17.9, h: 0.62, size: 28 });

  const why = [
    {
      name: "STATIC GUARDRAILS",
      sub: "LlamaGuard, regex, deny-lists",
      fail: "A fabricated clause is lexically clean. Identity-blind: the same string is fine for one caller and a breach for another.",
    },
    {
      name: "RAG GROUNDEDNESS",
      sub: "retrieval-only checkers",
      fail: "Sees retrieval, not tool rows or system context. Averages, so one wrong figure drowns. Action-blind: 0.82 means the same on a draft and a wire.",
    },
    {
      name: "CONFIDENCE / LOGPROBS",
      sub: "calibration as detector",
      fail: "The named failure is confidently wrong. You cannot detect a calibration failure with the calibration.",
    },
    {
      name: "LLM-AS-JUDGE",
      sub: "NeMo Guardrails and wrappers",
      fail: "Asks “does this look right?” — unfalsifiable. We ask “which span proves it?”",
    },
    {
      name: "COMPOSITE SCORE",
      sub: "Azure / Bedrock “trust”",
      fail: "“Trust: 87/100.” You cannot block, edit or escalate on 87.",
    },
  ];

  divider(s, 1.04, 2.12, 17.92);
  s.addText("COMMON APPROACH", {
    x: 1.16, y: 2.20, w: 5.4, h: 0.32,
    fontFace: FONT, fontSize: 12, color: C.muted, charSpacing: 1.6, margin: 0,
  });
  s.addText("WHY IT FAILS THIS REFUND", {
    x: 7.00, y: 2.20, w: 11.7, h: 0.32,
    fontFace: FONT, fontSize: 12, color: C.muted, charSpacing: 1.6, margin: 0,
  });
  divider(s, 1.04, 2.56, 17.92);

  why.forEach((r, i) => {
    const y = 2.64 + i * 1.08;
    s.addText(r.name, {
      x: 1.16, y, w: 5.55, h: 0.38,
      fontFace: FONT, fontSize: 15, bold: true, color: C.cream, margin: 0,
    });
    s.addText(r.sub, {
      x: 1.16, y: y + 0.36, w: 5.55, h: 0.32,
      fontFace: FONT, fontSize: 13, color: C.muted, margin: 0,
    });
    s.addText(r.fail, {
      x: 7.00, y, w: 11.70, h: 0.88,
      fontFace: FONT, fontSize: 15, color: C.warm, margin: 0,
    });
    divider(s, 1.04, y + 0.96, 17.92);
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 1.04, y: 8.28, w: 17.92, h: 0.92,
    fill: { color: C.rust, transparency: 85 }, line: { type: "none" },
  });
  s.addText("CONTROLPLANE", {
    x: 1.16, y: 8.42, w: 5.55, h: 0.64,
    fontFace: FONT, fontSize: 18, bold: true, color: C.rust, margin: 0, valign: "middle",
  });
  s.addText("Query the evidence.  Set-membership.  Block · Edit · Escalate · Pass on the same graph.  We publish our own miss rate.", {
    x: 7.00, y: 8.42, w: 11.70, h: 0.64,
    fontFace: FONT, fontSize: 15, color: C.cream, margin: 0, valign: "middle",
  });
}

// =====================================================================
// SLIDE 10 — MATRIX
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "09 // MATRIX");
  notes(s,
    "A hedged warranty guess on a support reply is not the same object as an ungrounded clause authorising a payment. Treat them as one score and you either over-flag the first — the plane gets switched off — or under-flag the second. Same plane. Support streams with an annotation. The copilot's partner email is edited. The refund is held and escalated. Proof still scales with consequence."
  );

  eyebrow(s, "08 · MULTI-USE-CASE", 1.04, 1.00, 12);
  headline(s, [
    { text: "TRANSCRIBED. NEVER " },
    { text: "REDRAWN", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.32, w: 17.9, h: 0.52, size: 28 });

  const hdrOpt = {
    fill: { color: C.hiFill }, color: C.muted, bold: true, fontFace: FONT, fontSize: 11,
    align: "center", valign: "middle", margin: [6, 5, 6, 5],
  };
  const rowLab = {
    fill: { color: C.panel }, color: C.cream, bold: true, fontFace: FONT, fontSize: 13,
    align: "center", valign: "middle", margin: [6, 5, 6, 5],
  };
  function mcell(text, hi) {
    const isBlock = text === "Block";
    const isEsc = text === "Escalate";
    const isEdit = text === "Edit";
    return {
      text,
      options: {
        fill: { color: hi ? "2A0C08" : C.panel },
        color: isBlock ? C.rust : isEsc ? C.amber : isEdit ? C.cream : C.warm,
        bold: isBlock || isEsc || isEdit || hi,
        fontFace: FONT,
        fontSize: 13,
        align: "center",
        valign: "middle",
        margin: [6, 4, 6, 4],
      },
    };
  }

  const matrix = [
    [
      { text: "", options: { ...hdrOpt } },
      { text: "Contradicted /\nentitlement violation", options: { ...hdrOpt } },
      { text: "Unsupported +\ncategorical", options: { ...hdrOpt } },
      { text: "Unsupported +\nhedged", options: { ...hdrOpt } },
      { text: "Unknown", options: { ...hdrOpt } },
    ],
    [
      { text: "R3", options: { ...rowLab } },
      mcell("Block", false),
      mcell("Escalate", true),
      mcell("Escalate", false),
      mcell("Escalate", false),
    ],
    [
      { text: "R2", options: { ...rowLab } },
      mcell("Block", false),
      mcell("Edit", true),
      mcell("Edit", false),
      mcell("Escalate", false),
    ],
    [
      { text: "R1", options: { ...rowLab } },
      mcell("Edit", true),
      mcell("Edit", false),
      mcell("Pass + annotate", true),
      mcell("Pass + annotate", false),
    ],
    [
      { text: "R0", options: { ...rowLab } },
      mcell("Pass + annotate", false),
      mcell("Pass + annotate", false),
      mcell("Pass", false),
      mcell("Pass", false),
    ],
  ];
  s.addTable(matrix, {
    x: 1.04, y: 1.96, w: 17.92, h: 4.05,
    colW: [1.55, 4.20, 4.20, 4.20, 3.77],
    rowH: [0.70, 0.80, 0.80, 0.80, 0.80],
    border: [
      { pt: 0.6, color: C.border },
      { pt: 0.6, color: C.border },
      { pt: 0.6, color: C.border },
      { pt: 0.6, color: C.border },
    ],
    valign: "middle",
  });

  const uc = [
    { k: "01  SUPPORT CHATBOT", a: "show_reply  ·  R1", cell: "R1 × Unsupported + hedged", act: "Pass + annotate" },
    { k: "02  KNOWLEDGE COPILOT", a: "draft_partner_email  ·  R2", cell: "R2 × Unsupported + categorical", act: "Edit" },
    { k: "03  DECISION-SUPPORT REFUND", a: "issue_refund  ·  R3", cell: "R3 × Unsupported + categorical", act: "Escalate" },
  ];
  uc.forEach((u, i) => {
    const x = 1.04 + i * 6.10;
    card(s, x, 6.20, 5.90, 2.55);
    s.addText(u.k, {
      x: x + 0.22, y: 6.34, w: 5.46, h: 0.32,
      fontFace: FONT, fontSize: 12, color: C.rust, charSpacing: 1.1, margin: 0,
    });
    s.addText(u.a, {
      x: x + 0.22, y: 6.70, w: 5.46, h: 0.34,
      fontFace: FONT, fontSize: 15, color: C.cream, margin: 0,
    });
    s.addText(u.cell, {
      x: x + 0.22, y: 7.08, w: 5.46, h: 0.40,
      fontFace: FONT, fontSize: 14, color: C.warm, margin: 0, valign: "top",
    });
    s.addText(u.act, {
      x: x + 0.22, y: 7.55, w: 5.46, h: 0.70,
      fontFace: FONT, fontSize: 22, bold: true, color: i === 2 ? C.amber : C.cream, margin: 0,
    });
  });

  s.addText("Same plane. Three Round 2 use cases. Three actuators. The verdict is hostile. The action is proportionate.", {
    x: 1.04, y: 8.90, w: 17.92, h: 0.36,
    fontFace: FONT, fontSize: 15, color: C.muted, margin: 0,
  });
}

// =====================================================================
// SLIDE 10 — BUSINESS + ROADMAP
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "09 // ROADMAP");
  notes(s,
    "At forty thousand interactions a week, uniform deep checking is how planes get disabled. Budget follows blast radius. We will not put a savings percentage on this slide — that number is knowable only on your traffic. What is knowable now: a missing clause cannot authorise a payout; an HR span cannot ride along to the wrong caller; dead compute is a walk backward on the same graph, not an estimate. Shadow first. Enforce R3 next. We hook context assembly — that is real integration, and it is why the design works."
  );

  eyebrow(s, "10 · BUSINESS CASE + ROADMAP", 1.04, 1.00, 14);
  headline(s, [
    { text: "BUDGET FOLLOWS " },
    { text: "BLAST RADIUS", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.32, w: 12.2, h: 0.52, size: 28 });

  s.addText("~40,000 / week", {
    x: 13.40, y: 1.28, w: 5.56, h: 0.48,
    fontFace: FONT, fontSize: 24, bold: true, color: C.cream, align: "right", margin: 0,
  });
  s.addText("DIRECTIONAL  ·  R0/R1 ≈ 80–90%  →  LANE 1", {
    x: 13.40, y: 1.76, w: 5.56, h: 0.28,
    fontFace: FONT, fontSize: 11, color: C.muted, align: "right", charSpacing: 0.6, margin: 0,
  });

  const qty = [
    { t: "HELD IRREVERSIBLE ACTIONS", d: "R3 × unsupported-categorical → held packet, not a Tuesday payout." },
    { t: "ENTITLEMENT INCIDENTS PREVENTED", d: "Over-permissioned index × wrong caller → Edit/Block, microseconds." },
    { t: "DEAD COMPUTE, NAMED", d: "Walk the graph backward: steps that grounded zero accepted claims." },
  ];
  qty.forEach((q, i) => {
    const x = 1.04 + i * 6.10;
    card(s, x, 2.16, 5.90, 2.20);
    rustBar(s, x, 2.16, 5.90);
    s.addText("0" + (i + 1), {
      x: x + 0.22, y: 2.30, w: 5.46, h: 0.28,
      fontFace: FONT, fontSize: 12, color: C.rust, charSpacing: 1.4, margin: 0,
    });
    s.addText(q.t, {
      x: x + 0.22, y: 2.60, w: 5.46, h: 0.70,
      fontFace: FONT, fontSize: 15, bold: true, color: C.cream, margin: 0,
    });
    s.addText(q.d, {
      x: x + 0.22, y: 3.32, w: 5.46, h: 0.80,
      fontFace: FONT, fontSize: 14, color: C.warm, margin: 0, valign: "top",
    });
  });

  const phases = [
    { n: "0", t: "SHADOW", w: "weeks 0–6", d: "Proxy + SDK hook; dual-emit. Would have held N, of which M were true positives." },
    { n: "1", t: "ENFORCE R3", w: "weeks 6–12", d: "Payments, deletion, publication, regulated advice. Fail closed or escalate." },
    { n: "2", t: "ENFORCE R2", w: "weeks 12–20", d: "Reversible writes / external sends. Autonomy downgrade." },
    { n: "3", t: "FNR + LOOPS", w: "from week 16", d: "Per-route FNR with CI; override capture; geographic packs as DAG content." },
  ];
  phases.forEach((p, i) => {
    const x = 1.04 + i * 4.68;
    card(s, x, 4.54, 4.50, 2.85);
    s.addText("PHASE " + p.n, {
      x: x + 0.20, y: 4.68, w: 4.10, h: 0.26,
      fontFace: FONT, fontSize: 12, color: C.rust, charSpacing: 1.4, margin: 0,
    });
    s.addText(p.t, {
      x: x + 0.20, y: 4.96, w: 4.10, h: 0.38,
      fontFace: FONT, fontSize: 16, bold: true, color: C.cream, margin: 0,
    });
    s.addText(p.w, {
      x: x + 0.20, y: 5.36, w: 4.10, h: 0.28,
      fontFace: FONT, fontSize: 13, color: C.amber, margin: 0,
    });
    s.addText(p.d, {
      x: x + 0.20, y: 5.72, w: 4.10, h: 1.40,
      fontFace: FONT, fontSize: 13, color: C.warm, margin: 0, valign: "top",
    });
  });

  card(s, 1.04, 7.58, 17.92, 2.52);
  s.addText("LATENCY TARGETS    ≤40 ms p50  /  ≤200 ms p95 added on R0/R1 text.  Never quote 40 as p95.", {
    x: 1.36, y: 7.74, w: 17.3, h: 0.36,
    fontFace: FONT, fontSize: 15, bold: true, color: C.cream, margin: 0,
  });
  s.addText(`Measured gate (submission/latency_bench.json, n=${M.nBench}): p50=${M.p50} ms · p95=${M.p95} ms — under target; quote measured vs targets separately.`, {
    x: 1.36, y: 8.12, w: 17.3, h: 0.36,
    fontFace: FONT, fontSize: 14, color: C.amber, margin: 0,
  });
  s.addText("We do not eliminate hallucinations. We do not claim drop-in. We do not claim zero added latency: we never make the model feel slow; we make the action wait. The integration cost is the moat — we hook context assembly.", {
    x: 1.36, y: 8.50, w: 17.3, h: 1.35,
    fontFace: FONT, fontSize: 15, color: C.warm, margin: 0, valign: "top",
  });
}

// =====================================================================
// SLIDE 11 — FNR
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "10 // FNR");
  notes(s,
    "We do not claim to eliminate hallucinations. The honest claim has a shape: on this route we catch a measured percent of ungrounded claims at forty milliseconds p50 — and here is the measured percent we don't. Every team will claim detection. Publishing our own false-negative rate is the move none of them will make. The blanks stay blank until we measure. Derived claims are the residual risk we will say out loud. UNKNOWN never becomes SUPPORTED. That one rule is the boundary between a control plane and false assurance."
  );

  eyebrow(s, "11 · RISKS WE PUBLISH", 1.04, 1.00, 12);
  headline(s, [
    { text: "WE PUBLISH OUR OWN " },
    { text: "MISS RATE", accent: true },
    { text: "." },
  ], { x: 1.04, y: 1.32, w: 17.9, h: 0.52, size: 28 });
  s.addText(`Per route. Not what we caught — what we missed. Schema empty until earned. This build: ${M.fnr} FNR (${M.fnrLo}–${M.fnrHi}) on a self-authored corpus — next slide.`, {
    x: 1.04, y: 1.88, w: 17.9, h: 0.32,
    fontFace: FONT, fontSize: 15, color: C.warm, margin: 0,
  });

  panel(s, 1.04, 2.32, 10.15, 7.70, "▸ GATE REPORT", "EMPTY UNTIL MEASURED");
  ascii(s, 1.32, 2.98, 9.60, 6.70, [
    "route                     <id>",
    "window                    <start>-<end>",
    "volume                    <n>",
    "holds                     <n>",
    "escalations               <n>",
    "edits                     <n>",
    "blocks                    <n>",
    "shadow_would_have_held    <n>",
    "true_positives_in_holds   <n>  (sampled)",
    "false_negatives           <n>  (sampled)",
    "FNR                       <measured>%  +/- <CI>  per route",
    "dead_compute_share        <measured>%",
    "override_rate             <measured> vs baseline",
    "p50_added_ms              <=40 (target)",
    "p95_added_ms              <=200 (target)",
    "policy_version            <id>",
  ], C.warm, 14);

  card(s, 11.42, 2.32, 7.54, 3.65, C.panel, C.rust, 1.0);
  rustBar(s, 11.42, 2.32, 7.54);
  s.addText("STRONGEST RESIDUAL RISK", {
    x: 11.72, y: 2.52, w: 7.00, h: 0.30,
    fontFace: FONT, fontSize: 12, color: C.muted, charSpacing: 1.4, margin: 0,
  });
  s.addText("False assurance on derived / multi-hop claims.", {
    x: 11.72, y: 2.92, w: 7.00, h: 0.85,
    fontFace: FONT, fontSize: 18, bold: true, color: C.cream, margin: 0,
  });
  s.addText("Derived → recompute, or UNKNOWN. UNKNOWN never collapses into SUPPORTED.", {
    x: 11.72, y: 3.88, w: 7.00, h: 1.55,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0, valign: "top",
  });

  card(s, 11.42, 6.17, 7.54, 3.85);
  s.addText("BIAS  ·  KEPT, IN MEASUREMENT TERMS", {
    x: 11.72, y: 6.37, w: 7.00, h: 0.32,
    fontFace: FONT, fontSize: 12, color: C.rust, charSpacing: 1.2, margin: 0,
  });
  s.addText("Counterfactual flip rate with a confidence interval, route-level, async.", {
    x: 11.72, y: 6.80, w: 7.00, h: 1.15,
    fontFace: FONT, fontSize: 18, bold: true, color: C.cream, margin: 0,
  });
  s.addText("Not a per-response verdict. Specified, not coded in this slice. If asked: that sentence is the whole answer.", {
    x: 11.72, y: 8.05, w: 7.00, h: 1.45,
    fontFace: FONT, fontSize: 15, color: C.warm, margin: 0, valign: "top",
  });
}

// =====================================================================
// SLIDE 12 — MEASURED / REFUSE TO CLAIM
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "11 // MEASURED");
  notes(s,
    `This is the honesty slide. Every number here is measured by make eval and make bench on a ${M.nCases}-case self-authored corpus — no production traffic. Ungrounded FNR is ${M.fnr} with a Wilson interval of ${M.fnrLo} to ${M.fnrHi}. Passable-action FPR is ${M.fpr} with a ${M.fprHi} upper bound. The hard-negative hold rate is ${M.hn} — we over-flag, and we name that as the next milestone rather than hide it. Gate latency over ${M.nBench} runs is p50 ${M.p50}ms, p95 ${M.p95}ms, p99 ${M.p99}ms. Published miss: ${M.missIds}. Then the refusals, about us and never about competitors: we do not claim eliminated hallucinations, zero integration, zero added latency, one accuracy number, or production-scale proof. In the demo the refund was held and escalated with the evidence packet.`
  );

  eyebrow(s, "12 · WHAT WE MEASURED  ·  AND WHAT WE REFUSE TO CLAIM", 1.04, 1.00, 14);
  headline(s, [
    { text: `${M.nCases} CASES. ` },
    { text: "SELF-AUTHORED", accent: true },
    { text: ". NO PRODUCTION TRAFFIC." },
  ], { x: 1.04, y: 1.32, w: 17.9, h: 0.52, size: 28 });
  s.addText("Every number below regenerates from `make eval` and `make bench`. Intervals, not point estimates. The miss is published, not smoothed.", {
    x: 1.04, y: 1.88, w: 17.9, h: 0.32,
    fontFace: FONT, fontSize: 15, color: C.warm, margin: 0,
  });

  panel(s, 1.04, 2.32, 10.15, 5.32, "▸ MEASURED — evals/last_run.json", `${M.nCases} CASES · SELF-AUTHORED`);
  ascii(s, 1.32, 2.98, 9.60, 4.40, [
    `corpus                    ${M.nCases} cases, self-authored`,
    "production traffic        none",
    `ungrounded FNR            ${M.fnr}   95% CI ${M.fnrLo} - ${M.fnrHi}`,
    `passable-action FPR       ${M.fpr}   95% upper bound ${M.fprHi}`,
    `hard-negative hold rate   ${M.hn}    95% CI ${M.hnLo} - ${M.hnHi}`,
    `gate latency  n=${M.nBench}     p50 ${M.p50}ms`,
    `                          p95 ${M.p95}ms`,
    `                          p99 ${M.p99}ms`,
  ], C.warm, 14);

  card(s, 1.04, 7.86, 10.15, 2.16, C.hiFill, C.rust, 1.0);
  rustBar(s, 1.04, 7.86, 10.15);
  s.addText("THE MISS  ·  NAMED, NOT SMOOTHED", {
    x: 1.34, y: 8.06, w: 9.55, h: 0.30,
    fontFace: FONT, fontSize: 12, color: C.muted, charSpacing: 1.4, margin: 0,
  });
  s.addText(`Hard-negative hold rate ${M.hn} — we over-flag.`, {
    x: 1.34, y: 8.44, w: 9.55, h: 0.42,
    fontFace: FONT, fontSize: 20, bold: true, color: C.cream, margin: 0,
  });
  s.addText(`Measured, published, and named as the next milestone. ${M.hnTotal}/${M.nCases} cases are hard negatives (${M.hnShare}). Published miss: ${M.missIds}.`, {
    x: 1.34, y: 8.94, w: 9.55, h: 0.95,
    fontFace: FONT, fontSize: 15, color: C.warm, margin: 0, valign: "top",
  });

  card(s, 11.42, 2.32, 7.54, 7.70, C.panel, C.rust, 1.0);
  rustBar(s, 11.42, 2.32, 7.54);
  s.addText("WE REFUSE TO CLAIM  ·  ABOUT US, NOT COMPETITORS", {
    x: 11.72, y: 2.52, w: 7.00, h: 0.30,
    fontFace: FONT, fontSize: 12, color: C.muted, charSpacing: 1.2, margin: 0,
  });
  s.addText("We do not claim:", {
    x: 11.72, y: 2.94, w: 7.00, h: 0.40,
    fontFace: FONT, fontSize: 20, bold: true, color: C.cream, margin: 0,
  });
  ascii(s, 11.72, 3.52, 7.00, 3.10, [
    "-  eliminated hallucinations",
    "-  zero integration",
    "-  zero added latency",
    "-  one accuracy number across",
    "   three failure modes",
    "-  production-scale proof",
  ], C.warm, 15);

  divider(s, 11.72, 6.72, 7.00);
  s.addText(`What we do claim is bounded: ${M.nCases} self-authored cases, every rate published with its Wilson interval. Production is unknown until shadow replay.`, {
    x: 11.72, y: 6.98, w: 7.00, h: 1.30,
    fontFace: FONT, fontSize: 15, color: C.warm, margin: 0, valign: "top",
  });
  s.addText("In the demo, the refund was held and escalated with the evidence packet.", {
    x: 11.72, y: 8.42, w: 7.00, h: 1.10,
    fontFace: FONT, fontSize: 17, bold: true, color: C.amber, margin: 0, valign: "top",
  });
}

// =====================================================================
// SLIDE 13 — ASK / CLOSE
// =====================================================================
{
  const s = pres.addSlide();
  chrome(s, "12 // ASK", true);
  notes(s,
    "We are asking to take this into shadow on one support route and one acting route. Enforcement is earned per route. The first artefact you get is the counterfactual — would have held N, of which M were true positives — not a block. That system was never asked to prove anything. Now nothing acts until it can prove it should."
  );

  eyebrow(s, "12 · ASK", 1.04, 1.15, 8);
  s.addText("CONTROLPLANE.AI", {
    x: 1.04, y: 1.55, w: 17.9, h: 0.40,
    fontFace: FONT, fontSize: 16, color: C.muted, charSpacing: 3, margin: 0,
  });
  s.addText("Admission-control layer  ·  STEP → SPAN → CLAIM → ACTION", {
    x: 1.04, y: 1.98, w: 17.9, h: 0.36,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0,
  });

  headline(s, [
    { text: "THAT SYSTEM WAS NEVER ASKED\nTO PROVE ANYTHING." },
  ], { x: 1.04, y: 2.50, w: 17.9, h: 1.85, size: 36 });

  s.addText("Now nothing acts until it can prove it should.", {
    x: 1.04, y: 4.42, w: 17.9, h: 0.55,
    fontFace: FONT, fontSize: 26, color: C.rust, margin: 0,
  });

  card(s, 1.04, 5.20, 17.92, 2.55, C.panel, C.rust, 1.0);
  s.addText("ASK  ·  ROUND 2 ADVANCE", {
    x: 1.40, y: 5.40, w: 17.2, h: 0.32,
    fontFace: FONT, fontSize: 14, color: C.rust, charSpacing: 1.8, margin: 0,
  });
  s.addText("Phase 0 shadow on one support route and one acting route.", {
    x: 1.40, y: 5.80, w: 17.2, h: 0.48,
    fontFace: FONT, fontSize: 22, bold: true, color: C.cream, margin: 0,
  });
  s.addText("The counterfactual, not a global switch. Would have held N, of which M were true positives — not a block. Enforcement is earned per route.", {
    x: 1.40, y: 6.38, w: 17.2, h: 1.00,
    fontFace: FONT, fontSize: 16, color: C.warm, margin: 0, valign: "top",
  });

  s.addText("That refund was ₹1,84,000 on a clause that does not exist.", {
    x: 1.04, y: 8.00, w: 17.92, h: 0.42,
    fontFace: FONT, fontSize: 18, color: C.cream, margin: 0,
  });
  s.addText("CHODA SRUJAN SAI  ·  DHRITHIKA  ·  IIT GANDHINAGAR  ·  TEAM CONTROLPLANE  ·  PS #1", {
    x: 1.04, y: 8.55, w: 17.92, h: 0.32,
    fontFace: FONT, fontSize: 14, color: C.muted, charSpacing: 1.2, margin: 0,
  });
}

pres.writeFile({
  fileName: path.join(__dirname, "ControlPlane_Round2_Pitch.pptx"),
}).then(() => {
  console.log("wrote submission/ControlPlane_Round2_Pitch.pptx");
}).catch((err) => {
  console.error(err);
  process.exit(1);
});
