#!/usr/bin/env python3
"""Write the timed visual frames for the ControlPlane rough cut."""
from pathlib import Path

OUT = Path(__file__).parent / "frames"
CSS = "base.css"

CARD = """
<div class="card{held}">
  <div class="line">Approved. Refund of ₹1,84,000 issued under clause 7.2</div>
  <div class="stamp">{stamp}</div>
  <div class="ts">{ts}</div>
</div>
"""

GRAPH = """
<div class="plate">
  <div class="rail">
    <div>
      <div class="lab">STEP</div>
      <div class="tiny">tool · retrieval</div>
      <div class="ticks{tdim}">
        <div class="tick"></div><div class="tick"></div><div class="tick"></div>
        <div class="tick"></div><div class="tick"></div><div class="tick"></div>
        <div class="tick{dead}"></div><div class="tick{dead}"></div><div class="tick{dead}"></div>
      </div>
      {cost}
    </div>
    <div><div class="dash"></div></div>
    <div>
      <div class="lab">SPAN <span class="chip">14</span></div>
      <div class="tiny mono">source · ACL · hash</div>
      <div class="pills{sdim}">
        <div class="pill">policy.db</div>
        <div class="pill">tickets</div>
        <div class="pill hot">billing</div>
        <div class="pill empty"></div>
        <div class="pill empty"></div>
        <div class="pill empty"></div>
      </div>
      {resp}
    </div>
    <div>
      <div class="lab">CLAIM</div>
      <div class="tiny">default state: UNSUPPORTED</div>
      <div class="dots{cdim}">
        {dots}
        <svg width="22" height="22" style="margin:0 6px"><line x1="2" y1="2" x2="20" y2="20" stroke="#D13438" stroke-width="3"/><line x1="20" y1="2" x2="2" y2="20" stroke="#D13438" stroke-width="3"/></svg>
      </div>
      {perf}
    </div>
    <div>
      <div class="lab">ACTION</div>
      <div class="actbox">
        <div class="tiny">refund</div>
        <div class="amt">₹1,84,000</div>
      </div>
    </div>
  </div>
</div>
"""


def wrap(body, white=False):
    bg = " slide white" if white else " slide"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{CSS}"></head>
<body><div class="{bg.strip()}">{body}</div></body></html>"""


def card(held=False):
    if held:
        return CARD.format(
            held=" held",
            stamp="held · escalated · clause 7.2 — no span",
            ts="held · Tue 14:06 · escalated",
        )
    return CARD.format(
        held="",
        stamp="clause 7.2 — no such clause",
        ts="executed · Tue 14:06 &nbsp;&nbsp; found · Fri 11:20",
    )


def dots(n_red_only=False, bound=False):
    if n_red_only:
        return "".join('<div class="dot red"></div>' for _ in range(6))
    if bound:
        return "".join(
            '<div class="dot red"></div>' if i == 5 else '<div class="dot"></div>'
            for i in range(6)
        )
    return "".join('<div class="dot"></div>' for _ in range(6))


def graph(stage="full", highlight=None):
    dclass = ""
    tdim = sdim = cdim = ""
    dead = ""
    cost = resp = perf = ""
    if stage == "spans":
        dclass = " dim"
        dots_html = ""
        # hide claims/action via dim on later cols - keep structure
        cdim = " dim"
    elif stage == "claims":
        dots_html = dots(n_red_only=True)
    else:
        dots_html = dots(bound=True)
    if highlight == "perf":
        tdim = sdim = " dim"
        perf = '<div class="lead"><span>PERFORMANCE</span>Unbound Claim</div>'
    elif highlight == "resp":
        tdim = cdim = " dim"
        resp = '<div class="lead"><span>RESPONSIBILITY</span>Unentitled Span</div>'
    elif highlight == "cost":
        sdim = cdim = " dim"
        dead = " dead"
        cost = '<div class="lead"><span>COST</span>Unused Step · 4 of 9</div>'
    elif highlight == "all":
        dead = " dead"
        cost = '<div class="lead"><span>COST</span>Unused Step</div>'
        resp = '<div class="lead"><span>RESPONSIBILITY</span>Unentitled Span</div>'
        perf = '<div class="lead"><span>PERFORMANCE</span>Unbound Claim</div>'
    if stage == "spans":
        dots_html = ""
        cdim = " dim"
    g = GRAPH.format(
        tdim=tdim, sdim=sdim, cdim=cdim, dead=dead,
        cost=cost, resp=resp, perf=perf, dots=dots_html,
    )
    return g


frames = {}

frames["1a"] = wrap("""
<div class="term" style="top:340px">
  <div class="main">Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.</div>
</div>
""")

frames["1b"] = wrap("""
<div class="term" style="top:280px">
  <div class="main">Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.</div>
  <div class="ann">
    policy filter &nbsp;&nbsp;—&nbsp; <span>pass</span><br>
    safety filter &nbsp;&nbsp;—&nbsp; <span>pass</span><br>
    confidence &nbsp;&nbsp;&nbsp;&nbsp;—&nbsp; <span>0.94</span>
  </div>
</div>
""")

frames["1c"] = wrap("""
<div class="term" style="top:240px">
  <div class="main">Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.</div>
  <div class="ann">
    policy filter &nbsp;&nbsp;—&nbsp; <span>pass</span><br>
    safety filter &nbsp;&nbsp;—&nbsp; <span>pass</span><br>
    confidence &nbsp;&nbsp;&nbsp;&nbsp;—&nbsp; <span>0.94</span>
  </div>
  <div class="bad">clause 7.2 — no such clause</div>
  <div class="meta">executed · Tue 14:06 &nbsp;&nbsp;&nbsp; found · Fri 11:20</div>
</div>
""")

frames["2a"] = wrap(card() + """
<div class="center" style="top:260px;left:620px">
  <div class="kicker">It used to be a bad paragraph.</div>
  <div class="h" style="margin-top:16px">It is now an executed transaction.</div>
</div>
""")

frames["2b"] = wrap(card() + """
<div class="center" style="top:220px;left:620px;right:88px">
  <div class="h" style="font-size:36px">A set of claims requesting permission to act.</div>
  <div class="dismiss">
    <div class="row"><s>second model</s> &nbsp;→&nbsp; <em>opinion</em></div>
    <div class="row"><s>filter</s> &nbsp;→&nbsp; <em>banned words</em></div>
    <div class="row"><s>dashboard</s> &nbsp;→&nbsp; <em>Friday</em></div>
    <div class="row"><s>confidence</s> &nbsp;→&nbsp; <em>broken instrument</em></div>
  </div>
</div>
""")

frames["2c"] = wrap(card() + """
<div class="center" style="top:240px;left:620px">
  <div class="h" style="font-size:40px">Everyone watches the exit.</div>
  <div class="subh">Nobody records the entrance.</div>
  <div class="subh" style="margin-top:36px;color:#C77CFF;font-size:16px;letter-spacing:0.08em;font-weight:700">CONTEXT ASSEMBLY — CAPTURED HERE, OUTSIDE THE MODEL</div>
</div>
""")

frames["3a"] = wrap(card() + graph("spans"))
frames["3b"] = wrap(card() + graph("claims"))
frames["3c"] = wrap(card() + graph("full"))
frames["3d"] = wrap(card() + graph("full", "perf"))
frames["3e"] = wrap(card() + graph("full", "resp"))
frames["3f"] = wrap(card() + graph("full", "cost"))
frames["3g"] = wrap(card() + graph("full", "all"))

frames["4a"] = wrap(card() + """
<div class="center" style="top:160px">
  <div class="h dark" style="font-size:34px;margin-bottom:8px">The same unproven claim annotates a draft and holds a payment.</div>
  <table class="matrix">
    <tr><th></th><th>Contradicted / entitlement</th><th>Unsupported + categorical</th><th>Unsupported + hedged</th><th>Unknown</th></tr>
    <tr><td class="rh">R3</td><td class="block">BLOCK</td><td class="esc">ESCALATE</td><td class="esc">ESCALATE</td><td class="esc">ESCALATE</td></tr>
    <tr><td class="rh">R2</td><td class="block">BLOCK</td><td class="edit">EDIT</td><td class="edit">EDIT</td><td class="esc">ESCALATE</td></tr>
    <tr><td class="rh">R1</td><td class="edit">EDIT</td><td class="edit">EDIT</td><td class="pass">PASS</td><td class="pass">PASS</td></tr>
    <tr><td class="rh">R0</td><td class="pass">PASS</td><td class="pass">PASS</td><td class="pass">PASS</td><td class="pass">PASS</td></tr>
  </table>
  <div class="pin">clause 7.2 → escalate · ₹1,84,000 held</div>
</div>
""", white=True)

frames["4b"] = wrap(card() + """
<div class="center" style="top:200px;left:620px;right:80px">
  <div class="json">
    {<br>
    &nbsp;&nbsp;<span class="k">"claim"</span>: <span class="r">"clause 7.2"</span>,<br>
    &nbsp;&nbsp;<span class="k">"verdict"</span>: <span class="r">"UNSUPPORTED"</span>,<br>
    &nbsp;&nbsp;<span class="k">"strength"</span>: <span class="s">"categorical"</span>,<br>
    &nbsp;&nbsp;<span class="k">"blast_radius"</span>: <span class="s">"R3"</span>,<br>
    &nbsp;&nbsp;<span class="k">"actuator"</span>: <span class="s">"ESCALATE"</span>,<br>
    &nbsp;&nbsp;<span class="k">"action"</span>: <span class="s">"refund ₹1,84,000"</span>,<br>
    &nbsp;&nbsp;<span class="k">"packet"</span>: <span class="s">["claim", "spans", "verdict"]</span><br>
    }
  </div>
</div>
""")

frames["4c"] = wrap(card() + """
<div class="center" style="top:220px;left:620px;right:80px">
  <div class="split">
    <div class="pane">
      <div class="tiny" style="letter-spacing:0.12em;font-weight:700">TEXT</div>
      <div style="margin-top:24px;font-size:22px;line-height:1.45">The refund is being prepared under the vendor agreement.<span class="hold">hold-back</span></div>
      <div class="tiny" style="margin-top:28px">We don't block the text. The user reads the response.</div>
    </div>
    <div class="pane">
      <div class="tiny" style="letter-spacing:0.12em;font-weight:700">ACTION</div>
      <div style="margin-top:24px;border:2px solid #F2F2EF;padding:22px">
        <div class="tiny">refund</div>
        <div style="font-size:32px;font-weight:700;margin-top:8px">₹1,84,000</div>
        <div style="color:#D13438;font-weight:700;margin-top:16px;font-size:16px">GATE — held</div>
      </div>
      <div class="tiny" style="margin-top:20px">gate on actions, not tokens</div>
    </div>
  </div>
</div>
""")

frames["4d"] = wrap(card() + """
<div class="center" style="top:200px;left:620px;right:80px">
  <div class="report">
    <h3>per-route gate report — format</h3>
    <div class="r"><div class="kk">route</div><div class="vv">finance/refund-agent</div></div>
    <div class="r"><div class="kk">gate latency (p50 / p95)</div><div class="vv">&lt;measured&gt; / &lt;measured&gt;</div></div>
    <div class="r"><div class="kk">ungrounded claims caught</div><div class="vv">&lt;measured&gt;</div></div>
    <div class="r fnr"><div class="kk">missed (FNR)</div><div class="vv">&lt;measured&gt; ± &lt;CI&gt;</div></div>
    <div class="r"><div class="kk">entitlement violations</div><div class="vv">100% deterministic</div></div>
    <div class="r"><div class="kk">audit sample</div><div class="vv">100% of blocks + escalations · 3% of passes</div></div>
  </div>
  <div class="cap">illustrative format — Round 2 fills this with measured values</div>
</div>
""")

frames["5a"] = wrap("""
<div class="term" style="top:280px">
  <div class="main">Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.</div>
  <div class="bad" style="color:#224BFF">held · Tue 14:06 · escalated</div>
  <div class="meta">clause 7.2 — no span</div>
</div>
""")

frames["5b"] = wrap("""
<div class="closer">Now nothing acts until it can prove it should.</div>
""")

frames["5c"] = wrap("""
<div class="mark">ControlPlane.ai</div>
""")

for name, html in frames.items():
    (OUT / f"{name}.html").write_text(html)
print(f"wrote {len(frames)} frames")
