"""Slide 1 — the graph, built on a CSS grid instead of hand-placed SVG coordinates.

Why this exists
---------------
`graph.py` draws s1 as one SVG string with ~200 hardcoded coordinates. Nothing responds
to anything else, so every edit opens a void or lands on top of something — which is why
s1 never converged while s2/s3 (CSS grid, in pages.py) landed at 9/10 immediately.

Structure that makes the defects impossible rather than fixed:
  * spans and claims share ONE 6-row grid, so bindings cannot drift out of alignment
  * row 6's span slot is an empty dashed ghost — the missing binding is structural,
    you cannot draw a connector to a span that does not exist
  * the ACTION plate is a flex column carrying all six frozen elements, so it cannot void
  * the three axis reads are labels with short vertical leaders — lines, never panels
"""

from .tokens import DISPLAY, MONO

# 4 dead of 9 — search_clauses ran and found nothing, which is why clause 7.2 has no span.
STEPS = [
    ("search_policy", False), ("fetch_tickets", False), ("read_contract", False),
    ("read_ledger", False), ("query_billing", False),
    ("fetch_notes", True), ("list_invoices", True),
    ("recompute_total", True), ("search_clauses", True),
]
SPANS = ["policy.db", "tickets", "contract", "ledger"]
CLAIMS = ["vendor id", "order date", "amount paid", "return window", "account"]

COLS = "236px 62px 470px 96px 428px 86px 1fr"

CSS = f"""
:root{{
  /* Slightly lifted ground so failure red survives thumbnail (review fix 2). */
  --ground:#14161A; --panel:#1C1E24; --rule:#2A2D34; --rule-soft:#212429;
  --ink:#F5F4F0; --muted:#9A9690; --bound:#C4C2CA; --dim:#6E6A72;
  --red:#E82028; --red-ink:#FF5A61; --red-wash:#2A0F13; --red-rule:#5A1319;
  --serif:Charter,'Iowan Old Style',Georgia,serif;
  --sans:{DISPLAY}; --mono:{MONO};
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1920px;height:1080px;overflow:hidden;background:var(--ground);
  color:var(--ink);-webkit-font-smoothing:antialiased}}
.slide{{width:1920px;height:1080px;padding:50px 62px 38px;display:flex;flex-direction:column}}

.kicker{{font-family:var(--mono);font-size:14px;letter-spacing:.15em;color:var(--muted);
  text-transform:uppercase;margin-bottom:16px}}
/* Cool headline — failure card owns glance (densest/brightest checks). */
h1{{font-family:var(--serif);font-size:42px;line-height:1.05;font-weight:700;
  letter-spacing:-.02em;white-space:nowrap;color:#9AA0A8}}

.heads{{display:grid;grid-template-columns:{COLS};align-items:end;margin-top:34px;
  padding-bottom:11px;border-bottom:1px solid var(--rule)}}
.hd{{font-family:var(--sans);font-size:15px;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--ink)}}
.hd small{{display:block;font-family:var(--mono);font-size:13px;letter-spacing:.02em;
  text-transform:none;font-weight:400;color:var(--muted);margin-top:5px}}
.model{{display:block;font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;
  color:var(--dim);font-weight:400;margin-bottom:6px;text-transform:uppercase}}
/* A count badge carries no verdict, so it gets no hue. Four colours have jobs on this deck —
   red=unproven, blue=escalate, amber=edit, grey=bound/pass. Violet had none. */
.chip{{display:inline-block;font-family:var(--mono);font-size:12px;font-weight:700;
  background:#2E323B;color:#C8CCD6;border:1px solid #3E434E;
  padding:2px 7px;margin-left:8px;vertical-align:2px}}

.body{{flex:1;min-height:0;display:grid;grid-template-columns:{COLS};padding-top:16px}}
.col{{display:grid;min-height:0}}
.steps{{grid-template-rows:repeat(9,1fr) auto}}
.spans,.links,.claims,.gates{{grid-template-rows:repeat(6,1fr);gap:10px}}
.capture{{position:relative}}

.step{{display:flex;align-items:center;gap:11px;font-family:var(--mono);font-size:16px;
  color:#787D88}}
.step i{{flex:0 0 24px;height:2px;background:var(--dim);font-style:normal}}
.step.dead{{color:#4A4F58}}
.step.dead i{{background:#2E3138}}
.step.dead span{{position:relative;opacity:.85}}
/* No strikethrough — grey mute is enough; lines read as noise at thumbnail. */
.step.dead span::after{{display:none}}
.costnote{{font-family:var(--sans);font-size:15px;color:var(--muted);display:flex;
  align-items:center;gap:9px;padding-top:12px}}
.costnote b{{color:var(--ink);font-weight:600}}
.aback{{width:32px;height:1px;background:var(--muted);position:relative}}
.aback::before{{content:"";position:absolute;left:0;top:-3px;border:3.5px solid transparent;
  border-right-color:var(--muted)}}

/* Capture note lives in the Span header only — no vertical pillar stealing mid-graph focus. */
.capture::before{{display:none}}
.capture span{{display:none}}
/* Structural annotation — a dimension line's label, not a third accent colour.
   #6E657A measured 3.5:1 on the ground and failed AA; this is 8.6:1. */
.cap-h{{display:block;font-family:var(--mono);font-size:12.5px;letter-spacing:.04em;
  color:#A9AEBA;font-weight:400;text-transform:none;margin-top:5px}}

.span{{background:#161A20;border:1px solid #252A32;padding:12px 18px;
  display:flex;flex-direction:column;justify-content:center;gap:9px}}
.span .name{{font-family:var(--mono);font-size:23px;color:#A8ADB8}}
.span .tags{{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}}
.span .tag{{font-family:var(--mono);font-size:15px;color:#6E737E;background:#1B1E24;
  border:1px solid var(--rule-soft);padding:4px 0;text-align:center}}
/* Billing mismatch is secondary evidence — keep cool, not failure-red. */
.span.breach{{background:#15171D;border-color:#3A3D45}}
.span.breach .name{{color:#A8ADB8}}
.span.breach .tags{{grid-template-columns:1fr auto 1fr}}
.span.breach .tag{{background:transparent;border-color:#2E3138;color:#8E93A0;
  font-size:15px;padding:5px 10px}}
.span.breach .neq{{border:none;color:#8A909A;font-size:18px;font-weight:700;background:none}}
.ghost{{border:1px dashed #3A3D45;display:flex;align-items:center;justify-content:center;
  font-family:var(--mono);font-size:14px;color:#5A5F6B;letter-spacing:.02em}}

.link{{display:flex;align-items:center}}
/* The slide's whole claim is "one graph". At opacity .5 these edges resolved to ~#414650
   and vanished at laptop scale — the bindings have to be visible or there is no graph. */
.link i{{flex:1;height:2px;background:#7A8090;font-style:normal;position:relative}}
.link i::before,.link i::after{{content:"";position:absolute;top:-3px;width:8px;height:8px;
  border-radius:50%;background:#9AA0B0}}
.link i::before{{left:0}} .link i::after{{right:0}}
.link.none{{position:relative}}
.link.none i{{height:3px;background:var(--red);opacity:1;
  -webkit-mask-image:repeating-linear-gradient(90deg,#000 0 7px,transparent 7px 15px);
  mask-image:repeating-linear-gradient(90deg,#000 0 7px,transparent 7px 15px)}}
.link.none i::before,.link.none i::after{{display:none}}
.link.none::after{{content:"no span";position:absolute;left:50%;top:50%;
  transform:translate(-50%,-50%);font-family:var(--mono);font-size:18px;font-weight:800;
  color:#FF8A90;letter-spacing:.04em;white-space:nowrap;background:var(--ground);padding:5px 10px;
  border:1px solid #6A282C}}

.claim{{background:#161A20;border:1px solid #252A32;display:flex;align-items:center;
  gap:13px;padding:0 20px;font-family:var(--mono);font-size:22px;color:#8E939E}}
.claim em{{width:7px;height:7px;border-radius:50%;background:#6A7080;flex:0 0 auto}}
/* Emphasis is structural — fill, keyline, scale, dark moat. No bloom.
   Thumb force: failure type scale is what survives at 400px, not glow. */
/* Failure is glance hit — fits the claim column, no overflow. */
.claim.unbound{{background:#9A1E28;border:6px solid #FF2030;flex-direction:column;
  box-shadow:0 0 0 6px var(--ground);
  align-items:flex-start;justify-content:center;gap:4px;padding:14px 16px;
  overflow:hidden;min-width:0}}
.claim.unbound .t{{color:#FFFFFF;font-size:48px;font-weight:800;letter-spacing:-.02em;
  line-height:1.05;max-width:100%}}
.claim.unbound .v{{font-size:14px;color:#FFF0F1;letter-spacing:.12em;font-weight:700}}

.gate{{display:flex;align-items:center}}
.gate i{{flex:1;height:2px;background:#4A4F58;font-style:normal}}
/* Open circuit: red trace stops at a solid end-cap — no glyph restating HELD. */
.gate.cut{{position:relative}}
.gate.cut i{{height:6px;background:linear-gradient(90deg,#FF2030 0 74%,transparent 74%)}}
.gate.cut::after{{content:"";position:absolute;left:74%;top:50%;width:8px;height:52px;
  transform:translate(-50%,-50%);background:#FF2030;border-radius:1px}}

/* Anchored, not floated: centring three blocks in the tallest plate on the slide left a
   ~130px void top and bottom. space-between seats the amount at the top and lands HELD on
   the plate's own bottom edge, which is where the eye finishes the chain. */
.action{{background:var(--panel);border:1px solid var(--rule);border-left:1px solid #2A2D34;
  padding:30px 24px;display:flex;flex-direction:column;justify-content:space-between;gap:24px}}
.action .lbl{{font-family:var(--mono);font-size:13px;letter-spacing:.2em;color:#61656F}}
.action .amt{{font-family:var(--serif);font-size:52px;font-weight:700;letter-spacing:-.02em;
  line-height:1;margin-top:2px;color:#7E848E}}
.action .route{{font-family:var(--mono);font-size:14px;color:#6E737E;margin-top:8px}}
.action .why{{font-family:var(--mono);font-size:15px;line-height:1.75}}
.action .why u{{display:block;color:#565A64;font-size:12px;letter-spacing:.18em;
  text-decoration:none;text-transform:uppercase}}
.action .why b{{color:#FF5A61;font-weight:800;font-size:16px}}
.action .why span{{color:#8E93A0}}
/* Quieter than the clause card — cause outranks effect (HANDOFF-NEXT). */
/* HELD quieter than clause card — cause outranks effect. */
.held{{border:2px solid #8A3038;background:#2A1014;padding:12px 14px;
  box-shadow:0 0 0 3px var(--ground)}}
.held u{{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.2em;
  color:#A8787C;text-decoration:none;margin-bottom:3px}}
.held b{{font-family:var(--mono);font-size:22px;color:#C8B8B8;font-weight:700;white-space:nowrap}}

.reads{{display:grid;grid-template-columns:{COLS};margin-top:22px}}
/* Each axis label is bracketed to the column it measures by a rule spanning that column's
   full width. As orphan 12px ticks the row read as unfinished; as measured spans it reads
   as axis annotation — and ACTION carrying no rule then parses as deliberate (it is the
   outcome, not an axis) rather than as a fourth label someone forgot to write. */
.read{{font-family:var(--sans);position:relative;padding-top:16px}}
.read::before{{content:"";position:absolute;left:0;top:0;width:100%;height:2px;
  background:#4E535E}}
.read u{{display:block;font-size:12.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--muted);text-decoration:none;margin-bottom:4px}}
.read b{{font-size:20px;font-weight:600;color:var(--ink)}}
.foot{{display:flex;align-items:baseline;justify-content:space-between;margin-top:20px;
  padding-top:16px;border-top:1px solid var(--rule)}}
.foot p{{font-family:var(--serif);font-size:24px;color:var(--muted)}}
.foot p.lead{{color:var(--ink);font-weight:700;margin-bottom:4px}}
.foot p b{{font-weight:700}}
.foot q{{font-family:var(--mono);font-size:13px;letter-spacing:.16em;color:var(--red);quotes:none}}

/* progressive-reveal states: hold the box, hide the ink, so the grid never shifts */
.off{{visibility:hidden}}
.dimmed{{opacity:.16}}
.hot{{opacity:1}}
"""


def _steps(cost_hot: bool, dim: bool, show_cost_count: bool) -> str:
    out = []
    for name, dead in STEPS:
        cls = " dead" if dead else ""
        if dim and not (cost_hot and dead):
            cls += " dimmed"
        out.append(f'<div class="step{cls}"><i></i><span>{name}</span></div>')
    off = "" if show_cost_count else " off"
    out.append(f'<div class="costnote{off}"><span class="aback"></span>'
               '<span><b>4 of 9</b> grounded nothing</span></div>')
    return "".join(out)


def _spans(span_n: int, resp_hot: bool, dim: bool) -> str:
    out = []
    for i, n in enumerate(SPANS):
        cls = "span" + (" off" if i >= span_n else "") + (" dimmed" if dim and not resp_hot else "")
        # Only the first span carries its tag row. The pattern is established once; repeating
        # source/ACL/hash on every card is 12 chips of noise competing with the failure.
        tags = ('<div class="tags"><i class="tag">source</i><i class="tag">ACL</i>'
                '<i class="tag">hash</i></div>') if i == 0 else ''
        out.append(f'<div class="{cls}"><div class="name">{n}</div>{tags}</div>')
    bcls = "span breach" + (" off" if span_n < 5 else "") + (" dimmed" if dim and not resp_hot else "")
    out.append(f'<div class="{bcls}"><div class="name">billing</div><div class="tags">'
               '<i class="tag">ACL risk-team</i><i class="tag neq">&ne;</i>'
               '<i class="tag">CALLER customer</i></div></div>')
    gcls = "ghost" + (" off" if span_n < 5 else "")
    out.append(f'<div class="{gcls}">no span was ever retrieved for this claim</div>')
    return "".join(out)


def _claims(show: bool, perf_hot: bool, dim: bool) -> str:
    d = " dimmed" if dim and not perf_hot else ""
    o = "" if show else " off"
    out = [f'<div class="claim{o}{d}"><em></em>{c}</div>' for c in CLAIMS]
    out.append(f'<div class="claim unbound{o}"><div class="t">clause 7.2</div>'
               '<div class="v">UNSUPPORTED &middot; CATEGORICAL</div></div>')
    return "".join(out)


def s1_body(bound: int = 5, span_n: int = 5, show_claims: bool = True,
            show_action: bool = True, show_gate: bool = True, show_spans: bool = True,
            show_leaders: bool = True, show_cost_count: bool = False,
            highlight: str | None = None, chrome: bool = True) -> str:
    """One drawing, used by both the deck poster and every video Beat-3 frame.

    Hidden elements keep their grid cell (`visibility:hidden`), so the graph builds
    in place across frames instead of reflowing under the viewer.
    """
    hl = highlight or ""
    dim = hl in ("perf", "resp", "cost")
    perf_hot, resp_hot, cost_hot = hl == "perf", hl == "resp", hl == "cost"
    if not show_spans:
        span_n = 0

    links = "".join(
        f'<div class="link{"" if i < bound else " off"}"><i></i></div>' for i in range(5)
    ) + f'<div class="link none{"" if show_claims and bound >= 5 else " off"}"><i></i></div>'
    gates = '<div class="gate"><i></i></div>' * 5 + \
            f'<div class="gate cut{"" if show_gate else " off"}"><i></i></div>'

    def rd(axis, label, value):
        on = show_leaders and (not dim or hl == axis or hl == "all")
        return (f'<div class="read{"" if on else " off"}">'
                f'<u>{label}</u><b>{value}</b></div>')

    head = f'''
  <div class="kicker">It used to be a bad paragraph &nbsp;&middot;&nbsp; it is now an executed transaction</div>
  <h1>An AI response is a set of claims requesting permission to act.</h1>''' if chrome else ""

    foot = f'''
  <div class="foot">
    <div><p class="lead">Three dimensions, one graph.</p>
    <p>The system didn&rsquo;t fail. It was never asked to prove anything.</p></div>
    <q>NO SPAN &rarr; NO EXECUTE &middot; HELD &middot; ESCALATED &middot; PUBLISHED</q>
  </div>''' if chrome else ""

    return f"""
<div class="slide">{head}
  <div class="heads">
    <div class="hd">Step<small>tool &middot; retrieval</small></div><div></div>
    <div class="hd">Span<span class="chip">14</span><small>source &middot; ACL &middot; hash</small><span class="cap-h">&larr; context assembly &mdash; captured here, outside the model</span></div><div></div>
    <div class="hd"><span class="model">model &middot; consumes spans &middot; emits claims</span>Claim<small>default: UNSUPPORTED</small></div><div></div>
    <div class="hd">Action<small>irreversible &middot; R3</small></div>
  </div>

  <div class="body">
    <div class="col steps">{_steps(cost_hot, dim, show_cost_count)}</div>
    <div class="capture"><span>context assembly &mdash; captured here, outside the model</span></div>
    <div class="col spans">{_spans(span_n, resp_hot, dim)}</div>
    <div class="col links">{links}</div>
    <div class="col claims">{_claims(show_claims, perf_hot, dim)}</div>
    <div class="col gates">{gates}</div>
    <div class="action{'' if show_action else ' off'}">
      <div>
        <div class="lbl">REFUND &middot; R3 &middot; IRREVERSIBLE</div>
        <div class="amt">&#8377;1,84,000</div>
        <div class="route">vendor agreement &middot; finance/refund-agent</div>
      </div>
      <div class="why{'' if show_gate else ' off'}">
        <u>gate reason</u><b>clause 7.2 &mdash; no span</b>
        <u style="margin-top:10px">verdict</u><span>UNSUPPORTED &middot; categorical</span>
      </div>
      <div class="held{'' if show_gate else ' off'}"><u>ACTUATOR</u><b>HELD &mdash; not executed</b></div>
    </div>
  </div>

  <div class="reads">
    {rd("cost", "Cost", "Unused Step")}<div></div>
    {rd("resp", "Responsibility", "Unentitled Span")}<div></div>
    {rd("perf", "Performance", "Unbound Claim")}<div></div>
    <div></div>
  </div>
{foot}</div>"""
