"""All 16:9 pages: three posters, video frames, video-slide poster."""

from .tokens import (
    PAGE, INK, PURPLE, MUTED, HAIR, PLATE, PLATE_2, LINE, RED, WHITE, BLUE, BLUE_SOFT,
    AMBER, AMBER_SOFT, RED_SOFT, PASS_BG, PASS_FG, DISPLAY, MONO, VIOLET,
)


def _doc(body, bg=PAGE, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {bg};
    font-family: {DISPLAY}; color: {INK}; -webkit-font-smoothing: antialiased; }}
  {extra}
</style></head>
<body>{body}</body></html>"""


# ---------------------------------------------------------------------------
# Slide 1
# ---------------------------------------------------------------------------

def poster_s1():
    # CSS-grid rebuild. The old SVG renderer placed ~200 coordinates by hand, so
    # every edit opened a void or a collision; s1_page lays the same graph out with
    # a real layout engine, the way poster_s2/poster_s3 below already do.
    from .s1_page import CSS as S1_CSS, s1_body

    return _doc(s1_body(show_cost_count=True), bg="#0E0F12", extra=S1_CSS)


# ---------------------------------------------------------------------------
# Slide 2
# ---------------------------------------------------------------------------

def poster_s2():
    headers = [
        "Contradicted /<br>entitlement violation",
        "Unsupported +<br>categorical",
        "Unsupported +<br>hedged",
        "Unknown",
    ]
    rows = [
        ("R3", "irreversible / regulated",
         [("BLOCK", "b"), ("ESCALATE", "e"), ("ESCALATE", "e"), ("ESCALATE", "e")]),
        ("R2", "reversible write / external",
         [("BLOCK", "b"), ("EDIT", "d"), ("EDIT", "d"), ("ESCALATE", "e")]),
        ("R1", "user-visible · read-only",
         [("EDIT", "d"), ("EDIT", "d"), ("PASS", "p", "+ annotate"), ("PASS", "p", "+ annotate")]),
        ("R0", "internal draft",
         [("PASS", "p", "+ annotate"), ("PASS", "p", "+ annotate"), ("PASS", "p"), ("PASS", "p")]),
    ]

    hd = "".join(f'<div class="hd">{h}</div>' for h in headers)
    # Column-2 bracket is OUTSIDE grid auto-flow (absolute on wrap) so it cannot steal cells.
    grid = ['<div></div>', hd]
    for i, (tier, desc, cells) in enumerate(rows):
        grid.append(f'<div class="rh"><div class="tier">{tier}</div><div class="desc">{desc}</div></div>')
        for j, cell in enumerate(cells):
            label, kind = cell[0], cell[1]
            sub = f"<small>{cell[2]}</small>" if len(cell) > 2 else ""
            punch = " punch" if (i == 0 and j == 1) else ""
            col2 = " col2" if j == 1 else ""
            edge = ""
            if j == 1:
                if i == 0:
                    edge = " c2-top"
                if i == 3:
                    edge += " c2-bot"
            grid.append(f'<div class="c {kind}{col2}{edge}{punch}">{label}{sub}</div>')

    extra = f"""
    .s {{ width:1920px; height:1080px; padding:36px 56px 24px; display:flex; flex-direction:column;
          background:{PLATE}; }}
    .h {{ font-family:Charter,'Iowan Old Style',Georgia,serif; font-size:44px; font-weight:700; color:{WHITE}; line-height:1.04; letter-spacing:-0.02em;
          max-width:1700px; padding-bottom:10px;
          border-bottom:1px solid #2E313A; }}
    .ann {{ margin:14px 0 0; font-size:15px; font-weight:500; color:#9A9690; }}
    .ann b {{ color:{WHITE}; font-weight:700; }}
    .grid-wrap {{
      margin-top:18px;
      flex: 1 1 auto;
      min-height: 0;
      position: relative;
    }}
    .grid {{
      width: 100%;
      height: 100%;
      display:grid;
      grid-template-columns: 220px repeat(4, 1fr);
      grid-template-rows: 52px repeat(4, 1fr);
      gap: 12px;
    }}
    .hd {{ font-size:14px; font-weight:600; color:#9A9690; text-align:center;
            align-self:end; line-height:1.3; padding-bottom:4px; font-family:{MONO}; }}
    .rh {{ display:flex; flex-direction:column; justify-content:center; padding-right:8px; }}
    .tier {{ font-size:32px; font-weight:700; color:{WHITE}; letter-spacing:-0.03em; }}
    .desc {{ font-size:13px; color:#9A9690; margin-top:5px; }}
    .c {{ display:flex; flex-direction:column; align-items:center; justify-content:center;
          font-size:30px; font-weight:700; letter-spacing:0.12em;
          border:1px solid transparent; font-family:{MONO}; border-radius:2px;
          position: relative; }}
    .c small {{ font-size:12px; font-weight:600; letter-spacing:0.06em; margin-top:6px; opacity:0.85; }}
    .b {{ background:#241014; color:#A85A5E; border-color:#33171B; }}
    .e {{ background:#11162C; color:#65739F; border-color:#1A2038; }}
    .d {{ background:#1A170A; color:#94722E; border-color:#2A230F; }}
    .p {{ background:#131519; color:#4E4B54; border-color:#1C1F24; }}
    /* Thin bracket edges on column 2 cells (STAGE4 — proves the headline). */
    .col2 {{ box-shadow: inset 3px 0 0 #C8C6CE; }}
    .c2-top {{ box-shadow: inset 3px 0 0 #C8C6CE, inset 0 3px 0 #C8C6CE; }}
    .c2-bot {{ box-shadow: inset 3px 0 0 #C8C6CE, inset 0 -3px 0 #C8C6CE; }}
    .punch {{ background:#3350F5 !important; color:#FFFFFF !important; font-size:54px;
              border:5px solid {RED} !important; letter-spacing:0.15em; z-index:3;
              box-shadow: 0 0 0 3px #0E0F12, 0 26px 88px rgba(51,80,245,0.70),
                          0 0 70px rgba(232,32,40,0.50),
                          inset 3px 0 0 #C8C6CE, inset 0 3px 0 #C8C6CE !important; }}
    /* Label for the bracket — under col-2 header, proves the headline. */
    .brkt-lab {{
      position: absolute;
      left: calc(220px + 24px + 1.5 * ((100% - 220px - 48px) / 4));
      top: 28px;
      transform: translateX(-50%);
      white-space: nowrap;
      font-family:{MONO}; font-size:12px; font-weight:700; letter-spacing:0.03em;
      color:#E8E6EE; background:rgba(14,15,18,0.96); padding:4px 10px;
      border:1px solid #5A5C64; z-index: 6; pointer-events: none;
    }}
    .foot {{ margin-top:20px; background:#14161C; padding:20px 30px;
             flex: 0 0 auto; border-left:8px solid {RED};
             display:flex; flex-direction:column; justify-content:center; gap:9px; }}
    .foot .k {{ font-size:20px; font-weight:700; color:{WHITE}; letter-spacing:-0.02em; }}
    .foot .pin {{ font-size:15px; color:#C8C6CE; }}
    .foot .pin b {{ color:{RED}; }}
    .foot .law {{ font-size:12.5px; color:#7E7A84; line-height:1.85; }}
    .foot .law b {{ color:#E0DEE6; }}
    """
    body = f"""
    <div class="s">
      <div class="h">The same unproven claim annotates a draft and holds a payment.</div>
      <div class="ann">severity × blast radius · R3 at the top
        &nbsp;·&nbsp; <b>no span → action does not execute</b></div>
      <div class="grid-wrap">
        <div class="grid">{''.join(grid)}</div>
        <div class="brkt-lab">one unproven claim — four outcomes</div>
      </div>
      <div class="foot">
        <div class="k">R3 × Unsupported + categorical = ESCALATE</div>
        <div class="pin"><b>clause 7.2 → escalate · ₹1,84,000 held</b>
          &nbsp;·&nbsp; never “block” the refund</div>
        <div class="law">
          <b>EDIT</b> — strip or re-ground the named span, never a rewrite.
          &nbsp;&nbsp;<b>ESCALATE</b> — inline hold; ships claim + spans + verdict.<br/>
          <b>Bias</b> — counterfactual flip rate, route-level, CI excludes zero.
          &nbsp;&nbsp;<b>Safety</b> — typed interlocks: tool × args × irreversibility.
          &nbsp;&nbsp;Hard gate on actions, not tokens. Text streams with a short hold-back.
        </div>
      </div>
    </div>"""
    return _doc(body, bg=PLATE, extra=extra)


# ---------------------------------------------------------------------------
# Slide 3
# ---------------------------------------------------------------------------

def poster_s3():
    items = [
        ("“We eliminate hallucinations.”",
         "We don’t. Ungrounded claims cannot authorise actions, and we report what we miss."),
        ("“Zero integration — drop it in.”",
         "We hook context assembly. That is real work, and it is the reason this works at all."),
        ("“Zero added latency.”",
         "Verification is budgeted, not free."),
        ("“99% accuracy across bias, safety and risk.”",
         "One number over three failure modes is a demo artifact."),
    ]
    left = "".join(
        f"""<div class="item">
              <div class="mark">REFUSED</div>
              <div class="claim">{c}</div>
              <div class="fix">{f}</div>
            </div>"""
        for c, f in items
    )
    # Closer owns the slide. Refuse + FNR are secondary instruments.
    extra = f"""
    .s {{ width:1920px; height:1080px; display:flex; flex-direction:column; background:{PLATE}; color:{WHITE}; }}
    .top {{ padding:44px 62px 28px; flex:1; min-height:0; display:grid;
            grid-template-columns: 1fr 1.05fr; grid-template-rows: auto auto 1fr;
            column-gap: 58px; }}
    .h {{ grid-column:1 / -1; font-family:Charter,'Iowan Old Style',Georgia,serif; font-size:42px; font-weight:700; color:{WHITE};
          line-height:1.05; letter-spacing:-0.035em; margin-bottom:0; padding-bottom:10px;
          border-bottom:1px solid #2E313A; }}
    .subline {{ grid-column:1 / -1; font-size:15px; color:#9A9690; margin:12px 0 18px; font-weight:500; }}
    .subline b {{ color:{WHITE}; }}
    .col {{ display:flex; flex-direction:column; min-height:0; }}
    .list {{ flex:1; min-height:0; display:grid; grid-template-rows:repeat(4, 1fr); gap:22px; }}
    .item {{ background:transparent; padding:2px 0 2px 22px;
             border-left:3px solid #5A282C;
             display:flex; flex-direction:column; justify-content:center; }}
    .mark {{ font-family:{MONO}; font-size:11.5px; font-weight:700; letter-spacing:0.2em;
             color:{RED}; margin-bottom:4px; }}
    .claim {{ font-size:15px; color:#6A6770; margin-bottom:7px; opacity:0.75; }}
    .fix {{ font-size:20px; font-weight:700; color:{WHITE}; line-height:1.32; }}
    .aside {{ font-size:15px; font-weight:600; color:#9A9690; margin:0 0 12px; }}
    .aside em {{ color:{RED}; font-style:normal; font-weight:700; }}
    .term {{ background:#12141A; flex:1; min-height:0; padding:20px 24px 14px;
             display:flex; flex-direction:column; border:1px solid #2A2D34;
             border-top:4px solid {RED}; }}
    .term h3 {{ font-family:{MONO}; font-size:13px; font-weight:700; color:#C8C6CE;
                margin-bottom:10px; letter-spacing:0.1em; }}
    .rows {{ flex:1; min-height:0; display:grid; grid-template-rows:repeat(6, 1fr); }}
    .term {{ padding:6px 4px; }}
    .row {{ display:grid; grid-template-columns: 1.3fr 1fr; align-items:center;
            font-family:{MONO}; font-size:15px; padding:0 8px;
            border-bottom:1px solid #1E2026; }}
    .row:last-child {{ border-bottom:none; }}
    .kk {{ color:#9A9690; }}
    .vv {{ color:{WHITE}; font-weight:700; }}
    .fnr {{ background:#3A1418; border:1px solid {RED}; margin:2px 0; }}
    .fnr .kk, .fnr .vv {{ color:#FFB0B4; font-size:18px; font-weight:700; }}
    .cap {{ font-size:13px; font-weight:600; color:#E0A030; margin-top:10px; }}
    .closer {{ background:#12141A; height:410px; flex:0 0 410px; display:flex;
                flex-direction:column; justify-content:center; padding:0 56px;
                border-top:1px solid #2A2D34; position:relative; }}
    .closer::before {{ content:""; position:absolute; left:0; top:0; bottom:0; width:14px;
                        background:{RED}; }}
    .closer p {{ font-family:Charter,'Iowan Old Style',Georgia,serif; font-size:84px; white-space:nowrap; font-weight:700; color:{WHITE}; letter-spacing:-0.045em;
                  line-height:1.02; max-width:1740px; }}
    .closer p span {{ color:{RED}; }}
    .closer .proof {{ margin-top:26px; font-size:19px; color:#9A9690; font-weight:500; }}
    .closer .proof b {{ color:{WHITE}; }}
    """
    body = f"""
    <div class="s">
      <div class="top">
        <div class="h">The claims we refuse to make — and the format we publish.</div>
        <div class="subline">We hold, escalate, and publish what we miss.
          &nbsp;·&nbsp; <b>not “99% accuracy” — the miss rate (FNR)</b></div>
        <div class="col">
          <div class="list">{left}</div>
        </div>
        <div class="col">
          <div class="aside">Everyone publishes precision. <em>This is the other number.</em></div>
          <div class="term">
            <h3>PER-ROUTE GATE REPORT — FORMAT</h3>
            <div class="rows">
              <div class="row"><div class="kk">route</div><div class="vv">finance/refund-agent</div></div>
              <div class="row"><div class="kk">gate latency (p50 / p95)</div><div class="vv">&lt;measured&gt; / &lt;measured&gt;</div></div>
              <div class="row"><div class="kk">ungrounded claims caught</div><div class="vv">&lt;measured&gt;</div></div>
              <div class="row fnr"><div class="kk">missed (FNR)</div><div class="vv">&lt;measured&gt; ± &lt;CI&gt;</div></div>
               <div class="row"><div class="kk">entitlement violations</div><div class="vv">100% (deterministic)</div></div>
               <div class="row"><div class="kk">audit sample</div><div class="vv">100% of blocks + escalations · 3% of passes</div></div>
            </div>
            <div class="cap">illustrative format — Round 2 fills this with measured values</div>
          </div>
        </div>
      </div>
      <div class="closer">
        <p>Now nothing acts until it can <span>prove</span> it should.</p>
        <div class="proof"><b>no span → no execution</b>
          &nbsp;·&nbsp; hold / escalate &nbsp;·&nbsp; publish the miss</div>
      </div>
    </div>"""
    return _doc(body, bg=PLATE, extra=extra)


# ---------------------------------------------------------------------------
# Video-slide poster (PPT slide 6)
def poster_video():
    extra = f"""
    .s {{ width:1920px; height:1080px; background:{PLATE}; color:{WHITE};
         padding:22px 48px 16px; display:flex; flex-direction:column; }}
    .k {{ font-size:13px; letter-spacing:0.22em; font-weight:700; color:{VIOLET}; }}
    .h {{ font-size:34px; font-weight:700; letter-spacing:-0.03em; margin-top:4px; line-height:1.06; }}
    .body {{ margin-top:12px; flex:1; min-height:0; display:grid;
             grid-template-rows: 1.2fr 1.15fr 0.9fr; gap:4px; }}
    .band {{ display:flex; align-items:center; padding:0 44px; }}
    .line {{ background:#16181D; font-family:{MONO}; font-size:80px; line-height:1.16; color:{WHITE};
             max-width:none; }}
    .line span {{ max-width:1680px; }}
    .held {{ background:#12182A; font-size:124px; font-weight:700; color:{BLUE}; letter-spacing:-0.025em; }}
    .meta {{ background:#16181D; font-family:{MONO}; font-size:90px; color:{RED}; line-height:1.06; }}
    .meta span {{ display:block; }}
    .meta em {{ display:block; font-style:normal; font-size:36px; font-weight:700;
                letter-spacing:0.22em; margin-top:10px; color:#E07A7C; }}
    .fn {{ margin-top:10px; font-size:15px; color:#8A8790; font-family:{MONO}; }}
    """
    body = f"""
    <div class="s">
      <div class="k">VIDEO  ·  2:58</div>
      <div class="h">The same transaction.<br>One field changed.</div>
      <div class="body">
        <div class="band line"><span>Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.</span></div>
        <div class="band held">held · Tue 14:06 · escalated</div>
        <div class="band meta"><span>clause 7.2 — no span<em>UNSUPPORTED</em></span></div>
      </div>
      <div class="fn">ControlPlane_ControlPlane-ai.mp4</div>
    </div>"""
    return _doc(body, bg=PLATE, extra=extra)


# ---------------------------------------------------------------------------
# Video frames
# ---------------------------------------------------------------------------

def _card(held=False):
    if held:
        stamp, ts, klass = "held · escalated · clause 7.2 — no span", "held · Tue 14:06 · escalated", " held"
        stamp_c = BLUE
    else:
        stamp, ts, klass = "clause 7.2 — no such clause", "executed · Tue 14:06&nbsp;&nbsp; found · Fri 11:20", ""
        stamp_c = RED
    return f"""
    <div class="card{klass}">
      <div class="who">agent · finance/refund-agent</div>
      <div class="line">Approved. Refund of ₹1,84,000 issued under clause 7.2</div>
      <div class="stamp" style="color:{stamp_c}">{stamp}</div>
      <div class="ts">{ts}</div>
    </div>"""


VIDEO_CSS = f"""
  .slide {{ width:1920px; height:1080px; position:relative; background:{PLATE}; color:{WHITE}; }}
  .card {{ position:absolute; top:28px; left:36px; width:560px; z-index:5;
           background:#16181D; border:1px solid #2A2D34; padding:14px 16px; }}
  .card .who {{ font-family:{MONO}; font-size:11px; color:#7A7680; letter-spacing:0.06em; margin-bottom:8px; }}
  .card .line {{ font-family:{MONO}; font-size:13px; color:#C8C6CE; line-height:1.4; }}
  .card .stamp {{ font-family:{MONO}; font-size:12px; font-weight:700; margin-top:8px; }}
  .card .ts {{ font-family:{MONO}; font-size:11px; color:#6A6770; margin-top:6px; }}
  .log {{
    position:absolute; left:160px; top:230px; width:1600px;
    border:1px solid #2A2D34; padding:40px 48px; background:#16181D;
    font-family:{MONO};
  }}
  .log .who {{ font-size:13px; color:#7A7680; letter-spacing:0.08em; margin-bottom:22px; }}
  .log .main {{ font-size:30px; color:{WHITE}; line-height:1.45; }}
  .log .ann {{ font-size:18px; color:#6A6770; margin-top:28px; line-height:1.75; }}
  .log .ann b {{ color:#A8A6AE; font-weight:500; }}
  .log .bad {{ font-size:24px; color:{RED}; font-weight:700; margin-top:32px; }}
  .log .meta {{ font-size:16px; color:#8A8790; margin-top:22px; }}
  .center {{ position:absolute; left:640px; right:80px; top:240px; }}
  .kicker {{ font-size:20px; font-style:italic; color:#8A8790; }}
  .h {{ font-size:44px; font-weight:700; color:#fff; line-height:1.08; letter-spacing:-0.025em; }}
  .h.sm {{ font-size:34px; }}
  .subh {{ font-size:24px; color:#C8C6CE; margin-top:16px; }}
  .dismiss {{ margin-top:36px; }}
  .drow {{ font-size:26px; color:#8A8790; margin:12px 0; }}
  .drow s {{ color:#4A4850; text-decoration-color:{RED}; text-decoration-thickness:2px; }}
  .drow em {{ font-style:normal; color:{WHITE}; }}
  .violet {{ color:{VIOLET}; font-size:15px; font-weight:700; letter-spacing:0.12em; margin-top:36px; }}
  .plate {{ position:absolute; left:36px; right:36px; top:168px; bottom:36px; }}
  .h.dark {{ color:{PURPLE}; }}
  .matrix-wrap {{ position:absolute; left:80px; right:80px; top:150px; }}
  table.mx {{ width:100%; border-collapse:separate; border-spacing:8px; margin-top:12px; }}
  table.mx th {{ font-size:13px; color:{MUTED}; font-weight:700; padding-bottom:4px; }}
  table.mx td {{ height:92px; text-align:center; font-size:20px; font-weight:700; letter-spacing:0.06em; }}
  .block {{ background:{RED_SOFT}; color:{RED}; }}
  .esc {{ background:{BLUE_SOFT}; color:{BLUE}; }}
  .edit {{ background:{AMBER_SOFT}; color:{AMBER}; }}
  .pass {{ background:{PASS_BG}; color:{PASS_FG}; }}
  .rh {{ text-align:left !important; background:transparent !important; color:{INK} !important;
         font-size:22px !important; width:150px; letter-spacing:0 !important; }}
  .pin {{ color:{BLUE}; font-size:18px; font-weight:700; margin-top:6px; }}
  .panel {{ position:absolute; left:640px; right:80px; top:200px; background:#16181D; padding:36px 40px; }}
  .json {{ font-family:{MONO}; font-size:22px; line-height:1.55; color:#C8C6CE; }}
  .json .k {{ color:{VIOLET}; }}
  .json .s {{ color:{WHITE}; }}
  .json .r {{ color:{RED}; }}
  .split {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
  .pane {{ background:#16181D; padding:28px; min-height:420px; }}
  .hold {{ display:inline-block; background:#2A2214; color:#E0A24A; font-size:12px;
           padding:2px 8px; margin-left:8px; font-family:{MONO}; }}
  .report {{ font-family:{MONO}; }}
  .report h3 {{ color:{VIOLET}; font-size:15px; margin-bottom:18px; }}
  .report .r {{ display:grid; grid-template-columns:1.25fr 1fr; padding:8px 0; font-size:16px; }}
  .report .kk {{ color:#8A8790; }}
  .report .vv {{ color:{WHITE}; }}
  .fnr .kk, .fnr .vv {{ color:#E07A7C; }}
  .cap {{ font-size:13px; font-style:italic; color:#8A8790; margin-top:14px; }}
  .closer {{ position:absolute; left:80px; right:80px; top:46%;
             font-size:48px; font-weight:700; letter-spacing:-0.03em; }}
  .mark {{ position:absolute; left:0; right:0; top:48%; text-align:center;
           font-size:44px; font-weight:700; letter-spacing:-0.03em; }}
"""


def _v(body, white=False):
    bg = PAGE if white else PLATE
    return _doc(f'<div class="slide" style="background:{bg}">{body}</div>', bg=bg, extra=VIDEO_CSS)


def _log(stage):
    """stage: line | filters | stamp"""
    filters = ""
    stamp = ""
    if stage in ("filters", "stamp"):
        filters = """<div class="ann">
          policy filter&nbsp;&nbsp;&nbsp;&nbsp;—&nbsp;&nbsp;<b>pass</b><br>
          safety filter&nbsp;&nbsp;&nbsp;&nbsp;—&nbsp;&nbsp;<b>pass</b><br>
          confidence&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;—&nbsp;&nbsp;<b>0.94</b>
        </div>"""
    if stage == "stamp":
        stamp = f"""<div class="bad">clause 7.2 — no such clause</div>
        <div class="meta">executed · Tue 14:06&nbsp;&nbsp;&nbsp;&nbsp;found · Fri 11:20</div>"""
    return f"""
    <div class="log">
      <div class="who">agent · finance/refund-agent&nbsp;&nbsp;·&nbsp;&nbsp;Tue 14:06</div>
      <div class="main">Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.</div>
      {filters}{stamp}
    </div>"""


def video_frames():
    frames = {}
    frames["1a"] = _v(_log("line"))
    frames["1b"] = _v(_log("filters"))
    frames["1c"] = _v(_log("stamp"))

    frames["2a"] = _v(_card() + """
      <div class="center">
        <div class="kicker">It used to be a bad paragraph.</div>
        <div class="h" style="margin-top:14px">It is now an executed transaction.</div>
      </div>""")

    frames["2b"] = _v(_card() + """
      <div class="center">
        <div class="h sm">A set of claims requesting permission to act.</div>
        <div class="dismiss">
          <div class="drow"><s>second model</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>opinion</em></div>
          <div class="drow"><s>filter</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>banned words</em></div>
          <div class="drow"><s>dashboard</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>Friday</em></div>
          <div class="drow"><s>confidence</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>broken instrument</em></div>
        </div>
      </div>""")

    frames["2b1"] = _v(_card() + """
      <div class="center">
        <div class="h sm">A set of claims requesting permission to act.</div>
        <div class="dismiss">
          <div class="drow"><s>second model</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>opinion</em></div>
        </div>
      </div>""")
    frames["2b2"] = _v(_card() + """
      <div class="center">
        <div class="h sm">A set of claims requesting permission to act.</div>
        <div class="dismiss">
          <div class="drow"><s>second model</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>opinion</em></div>
          <div class="drow"><s>filter</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>banned words</em></div>
        </div>
      </div>""")
    frames["2b3"] = _v(_card() + """
      <div class="center">
        <div class="h sm">A set of claims requesting permission to act.</div>
        <div class="dismiss">
          <div class="drow"><s>second model</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>opinion</em></div>
          <div class="drow"><s>filter</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>banned words</em></div>
          <div class="drow"><s>dashboard</s>&nbsp;&nbsp;→&nbsp;&nbsp;<em>Friday</em></div>
        </div>
      </div>""")

    frames["2c"] = _v(_card() + """
      <div class="center">
        <div class="h">Everyone watches the exit.</div>
        <div class="subh">Nobody records the entrance.</div>
        <div class="violet">CONTEXT ASSEMBLY — CAPTURED HERE, OUTSIDE THE MODEL</div>
      </div>""")

    def plate(**kw):
        # Same drawing as the deck poster — the freeze requires deck and video to be
        # literally one graph, so Beat 3 builds s1_page up state by state.
        from .s1_page import CSS as S1_CSS, s1_body

        return _doc(s1_body(chrome=True, **kw), bg="#0E0F12", extra=S1_CSS)

    frames["3a0"] = plate(bound=0, show_claims=False, show_action=False, show_gate=False, show_leaders=False, show_spans=False)
    frames["3a1"] = plate(bound=0, show_claims=False, show_action=False, show_gate=False, show_leaders=False, span_n=1)
    frames["3a2"] = plate(bound=0, show_claims=False, show_action=False, show_gate=False, show_leaders=False, span_n=2)
    frames["3a3"] = plate(bound=0, show_claims=False, show_action=False, show_gate=False, show_leaders=False, span_n=3)
    frames["3a4"] = plate(bound=0, show_claims=False, show_action=False, show_gate=False, show_leaders=False, span_n=4)
    frames["3a5"] = plate(bound=0, show_claims=False, show_action=False, show_gate=False, show_leaders=False, span_n=5)
    frames["3a"] = plate(bound=0, show_claims=False, show_action=False, show_gate=False, show_leaders=False)
    frames["3b0"] = plate(bound=0, show_action=False, show_gate=False, show_leaders=False)
    frames["3b"] = plate(bound=0, show_action=True, show_gate=False, show_leaders=False)
    frames["3c1"] = plate(bound=1, show_gate=False, show_leaders=False)
    frames["3c2"] = plate(bound=2, show_gate=False, show_leaders=False)
    frames["3c3"] = plate(bound=3, show_gate=False, show_leaders=False)
    frames["3c4"] = plate(bound=4, show_gate=False, show_leaders=False)
    frames["3c"] = plate(bound=5, show_gate=True, show_leaders=False)
    frames["3d"] = plate(bound=5, highlight="perf")
    frames["3e"] = plate(bound=5, highlight="resp")
    frames["3f"] = plate(bound=5, highlight="cost", show_cost_count=True)
    frames["3g"] = plate(bound=5, highlight="all")

    frames["4a"] = _v(_card() + f"""
      <div class="matrix-wrap">
        <div class="h dark" style="font-size:30px;margin-bottom:4px">The same unproven claim annotates a draft and holds a payment.</div>
        <table class="mx">
          <tr><th></th><th>Contradicted / entitlement</th><th>Unsupported + categorical</th><th>Unsupported + hedged</th><th>Unknown</th></tr>
          <tr><td class="rh">R3</td><td class="block">BLOCK</td><td class="esc">ESCALATE</td><td class="esc">ESCALATE</td><td class="esc">ESCALATE</td></tr>
          <tr><td class="rh">R2</td><td class="block">BLOCK</td><td class="edit">EDIT</td><td class="edit">EDIT</td><td class="esc">ESCALATE</td></tr>
          <tr><td class="rh">R1</td><td class="edit">EDIT</td><td class="edit">EDIT</td><td class="pass">PASS</td><td class="pass">PASS</td></tr>
          <tr><td class="rh">R0</td><td class="pass">PASS</td><td class="pass">PASS</td><td class="pass">PASS</td><td class="pass">PASS</td></tr>
        </table>
        <div class="pin">clause 7.2 → escalate · ₹1,84,000 held</div>
      </div>""", white=True)

    frames["4b"] = _v(_card() + """
      <div class="panel">
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
      </div>""")

    frames["4c"] = _v(_card() + f"""
      <div class="panel" style="background:transparent;padding:0;top:190px">
        <div class="split">
          <div class="pane">
            <div style="font-size:12px;letter-spacing:0.16em;font-weight:700;color:#8A8790">TEXT</div>
            <div style="margin-top:22px;font-size:22px;line-height:1.45">The refund is being prepared under the vendor agreement.<span class="hold">hold-back</span></div>
            <div style="margin-top:28px;font-size:14px;color:#8A8790">We don't block the text. The user reads the response.</div>
          </div>
          <div class="pane">
            <div style="font-size:12px;letter-spacing:0.16em;font-weight:700;color:#8A8790">ACTION</div>
            <div style="margin-top:22px;border:1.6px solid {WHITE};padding:22px">
              <div style="font-size:12px;color:#8A8790">refund</div>
              <div style="font-size:32px;font-weight:700;margin-top:8px">₹1,84,000</div>
              <div style="color:{RED};font-weight:700;margin-top:16px;font-size:16px">GATE — held</div>
            </div>
            <div style="margin-top:18px;font-size:14px;color:#8A8790">gate on actions, not tokens</div>
          </div>
        </div>
      </div>""")

    frames["4d"] = _v(_card() + """
      <div class="panel">
        <div class="report">
          <h3>per-route gate report — format</h3>
          <div class="r"><div class="kk">route</div><div class="vv">finance/refund-agent</div></div>
          <div class="r"><div class="kk">gate latency (p50 / p95)</div><div class="vv">&lt;measured&gt; / &lt;measured&gt;</div></div>
          <div class="r"><div class="kk">ungrounded caught</div><div class="vv">&lt;measured&gt;</div></div>
          <div class="r fnr"><div class="kk">missed (FNR)</div><div class="vv">&lt;measured&gt; ± &lt;CI&gt;</div></div>
          <div class="r"><div class="kk">entitlement violations</div><div class="vv">100% deterministic</div></div>
        </div>
        <div class="cap">illustrative format — Round 2 fills this with measured values</div>
      </div>""")

    frames["5a"] = _v(f"""
      <div class="log">
        <div class="who">agent · finance/refund-agent&nbsp;&nbsp;·&nbsp;&nbsp;Tue 14:06</div>
        <div class="main">Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement.</div>
        <div class="bad" style="color:{BLUE}">held · Tue 14:06 · escalated</div>
        <div class="meta">clause 7.2 — no span</div>
      </div>""")
    frames["5b"] = _v('<div class="closer">Now nothing acts until it can prove it should.</div>')
    frames["5c"] = _v('<div class="mark">ControlPlane.ai</div>')
    return frames
