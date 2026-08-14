"""Full-bleed 1920×1080 LTR graph. Same drawing for Slide 1 and video Beat 3.

Freeze (STAGE4 + ELEVATION production rules):
- STEP: nine untagged TICKS (not boxes — a box is a container that failed to load)
- SPAN: six nodes + 14 chip; only three tags fully legible; chips source·ACL·hash
- CLAIM: six nodes; five bound + clause 7.2 unbound; default UNSUPPORTED
- MODEL: small, offset above CLAIM layer, subordinate
- Leaders: thin lines that TAP the graph; two-word labels only
  Unused Step · Unentitled Span · Unbound Claim
- ACTION: ONE full-height plate (never five empty wells / never range(6) slots)
- Gate: geometric X, not padlock
- Meaning colours: bound (neutral) and unbound (red) only
"""

from .tokens import PLATE, PLATE_2, LINE, BOUND, RED, VIOLET, WHITE, MONO, DISPLAY

W, H = 1920, 1080
# Chrome air (kicker + headline + labels) then graph body then leaders then footer.
ROW0, ROW_H, SPAN_H = 208, 102, 88
BODY_BOT = ROW0 + 5 * ROW_H + SPAN_H  # 806

STEP_X, STEP_W = 56, 148
BOUND_X = 226
SPAN_X, SPAN_W = 248, 466
CLAIM_X, CLAIM_W = 850, 420
GATE_X = 1312
ACT_X, ACT_W = 1372, 492

BAND_Y = 868
N_TICKS = 9
DEAD = {2, 4, 6, 7}
DIM = 0.16
C_COST, C_RESP, C_PERF = "#7FBFA8", "#E0A44C", "#8FA0DC"

SPANS = [
    ("policy.db", "full"),
    ("tickets", "full"),
    ("contract", "ghost"),
    ("ledger", "ghost"),
    ("billing", "acl"),
    (None, "empty"),
]
CLAIMS = ["vendor id", "order date", "amount paid", "return window", "account"]


def _row_y(i):
    return ROW0 + i * ROW_H


def _chips(x, y, labels, ghost=False):
    cw, ch, gap = 138, 30, 8
    ink = "#6A6C74" if ghost else "#E0DEE6"
    fill = "#14161B" if ghost else "#1C1E24"
    stroke = "#2A2C34" if ghost else "#3A3C44"
    out = []
    for i, label in enumerate(labels):
        bx = x + i * (cw + gap)
        out.append(
            f'<rect x="{bx}" y="{y}" width="{cw}" height="{ch}" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{bx + cw / 2:.1f}" y="{y + 20}" font-family="{MONO}" font-size="14" '
            f'font-weight="600" fill="{ink}" text-anchor="middle">{label}</text>'
        )
    return "".join(out)


def graph_svg(
    bound=5,
    show_claims=True,
    show_action=True,
    show_spans=True,
    show_gate=True,
    highlight=None,
    show_leaders=True,
    show_cost_count=False,
    chrome=False,
    span_n=None,
):
    dim_step = highlight in ("perf", "resp")
    dim_span = highlight in ("perf", "cost")
    dim_claim = highlight in ("resp", "cost")
    dim_act = highlight in ("perf", "resp", "cost")
    glance = highlight == "all"
    # Bound system readable; unbound still first kill.
    GLANCE_DIM = 0.72

    p = [
        f'<svg viewBox="0 0 {W} {H}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">',
        f"<rect width='{W}' height='{H}' fill='{PLATE}'/>",
    ]

    if chrome:
        p.append(
            f'<text x="56" y="38" font-family="{DISPLAY}" font-size="17" font-style="italic" '
            f'fill="#9A9690">It used to be a bad paragraph. It is now an executed transaction.</text>'
            f'<text x="56" y="82" font-family="{DISPLAY}" font-size="36" font-weight="700" '
            f'fill="{WHITE}" letter-spacing="-1.0">An AI response is a set of claims requesting '
            f'permission to act.</text>'
            f'<line x1="56" y1="98" x2="920" y2="98" stroke="#2E313A" stroke-width="1.2"/>'
        )

    def lab(x, title, sub):
        return (
            f'<text x="{x}" y="128" font-family="{DISPLAY}" font-size="14" font-weight="700" '
            f'letter-spacing="2.4" fill="#E8E6EE">{title}</text>'
            f'<text x="{x}" y="148" font-family="{MONO}" font-size="12" fill="#9A9690">{sub}</text>'
        )

    p.append(lab(STEP_X, "STEP", "tool · retrieval"))
    p.append(lab(SPAN_X, "SPAN", "source · ACL · hash"))
    p.append(lab(CLAIM_X, "CLAIM", "default: UNSUPPORTED"))
    # MODEL — small, offset above CLAIM (STAGE4). Subordinate.
    if show_claims:
        p.append(
            f'<text x="{CLAIM_X + CLAIM_W - 8}" y="128" font-family="{MONO}" font-size="11" '
            f'font-weight="700" letter-spacing="2" fill="#6A6770" text-anchor="end">MODEL</text>'
            f'<text x="{CLAIM_X + CLAIM_W - 8}" y="144" font-family="{MONO}" font-size="10" '
            f'fill="#5A5860" text-anchor="end">consumes spans · emits claims</text>'
        )
    p.append(lab(ACT_X, "ACTION", "irreversible · R3"))
    p.append(
        f'<rect x="{SPAN_X + 92}" y="118" width="28" height="16" fill="{VIOLET}"/>'
        f'<text x="{SPAN_X + 106}" y="130" font-family="{MONO}" font-size="11" font-weight="700" '
        f'fill="#100E14" text-anchor="middle">14</text>'
    )
    for x in (STEP_X + 152, CLAIM_X - 52, ACT_X - 48):
        p.append(
            f'<path d="M {x} 124 H {x+28}" stroke="#5A5C64" stroke-width="1.5"/>'
            f'<path d="M {x+20} 118 L {x+30} 124 L {x+20} 130" fill="none" stroke="#5A5C64" '
            f'stroke-width="1.5"/>'
        )

    p.append(
        f'<line x1="{BOUND_X}" y1="{ROW0 - 6}" x2="{BOUND_X}" y2="{BODY_BOT}" stroke="{VIOLET}" '
        f'stroke-width="2" stroke-dasharray="6 8"/>'
        f'<text x="{BOUND_X + 12}" y="{ROW0 - 8}" font-family="{DISPLAY}" font-size="13" '
        f'font-weight="700" fill="{VIOLET}">context assembly — captured here, outside the model</text>'
    )

    # ---- STEP: nine labelled TICKS (ELEVATION). Not boxes.
    top = DIM if dim_step else (GLANCE_DIM if glance else 1)
    tstep = (BODY_BOT - ROW0 - 12) / (N_TICKS - 1)
    tick_w, tick_h = 52, 11
    tick_x = STEP_X + (STEP_W - tick_w) / 2
    STEP_LABELS = [
        "search_policy", "fetch_tickets", "read_contract",
        "read_ledger", "query_billing", "fetch_notes",
        "validate_refund", "compute_amount", "authorize"
    ]
    for i in range(N_TICKS):
        y = ROW0 + i * tstep
        dead = i in DEAD
        fill = "#3A3C44" if dead else "#D4D4DC"
        p.append(
            f'<rect x="{tick_x:.1f}" y="{y:.1f}" width="{tick_w}" height="{tick_h}" '
            f'rx="1" fill="{fill}" opacity="{top}"/>'
        )
        # label
        p.append(
            f'<text x="{tick_x + tick_w/2:.1f}" y="{y + tick_h/2 + 4:.1f}" '
            f'font-family="{MONO}" font-size="10" font-weight="600" '
            f'fill="{"#5A5C64" if dead else "#1A1A1A"}" text-anchor="middle" opacity="{top}">'
            f'{STEP_LABELS[i]}</text>'
        )
        if dead:
            # strong 3px diagonal strike
            p.append(
                f'<line x1="{tick_x + 4}" y1="{y + tick_h - 4:.1f}" x2="{tick_x + tick_w - 4}" '
                f'y2="{y + 4:.1f}" stroke="#6E7079" stroke-width="3" opacity="{top}"/>'
            )
    if show_leaders and highlight in (None, "cost", "all"):
        ay = BODY_BOT + 14
        p.append(
            f'<path d="M {STEP_X + STEP_W - 20} {ay} H {STEP_X + 18}" stroke="{C_COST}" stroke-width="2.2"/>'
            f'<path d="M {STEP_X + 30} {ay - 6} L {STEP_X + 16} {ay} L {STEP_X + 30} {ay + 6}" '
            f'fill="none" stroke="{C_COST}" stroke-width="2.2"/>'
            f'<text x="{STEP_X}" y="{BODY_BOT + 38}" font-family="{MONO}" font-size="12" '
            f'fill="#8A8790">4 of 9 grounded nothing</text>'
        )

    # ---- SPAN column
    if show_spans:
        limit = len(SPANS) if span_n is None else max(0, span_n)
        for i, (name, kind) in enumerate(SPANS):
            if i >= limit:
                continue
            y = _row_y(i)
            d = dim_span and not (highlight == "resp" and kind == "acl")
            op = DIM if d else 1
            if glance and kind in ("full", "ghost"):
                op = GLANCE_DIM
            elif glance and kind == "acl":
                op = 0.95
            if kind == "empty":
                mid = y + SPAN_H / 2
                p.append(
                    f'<g opacity="{1 if not d else 0.16}">'
                    f'<line x1="{SPAN_X}" y1="{mid}" x2="{SPAN_X + SPAN_W}" '
                    f'y2="{mid}" stroke="{RED}" stroke-width="3.2" stroke-dasharray="6 6"/>'
                    f'<text x="{SPAN_X + SPAN_W / 2}" y="{mid + 6:.1f}" font-family="{MONO}" '
                    f'font-size="26" font-weight="700" fill="{RED}" text-anchor="middle">no span</text></g>'
                )
                continue
            if kind == "acl":
                p.append(
                    f'<g opacity="{op}">'
                    f'<rect x="{SPAN_X}" y="{y}" width="{SPAN_W}" height="{SPAN_H}" fill="#1A1214" '
                    f'stroke="{RED}" stroke-width="2.4"/>'
                    f'<text x="{SPAN_X+18}" y="{y+24}" font-family="{MONO}" font-size="17" '
                    f'font-weight="700" fill="{RED}">{name}</text>'
                    f'<rect x="{SPAN_X+18}" y="{y+36}" width="186" height="34" fill="#2C1A1D"/>'
                    f'<text x="{SPAN_X+28}" y="{y+58}" font-family="{MONO}" font-size="14" '
                    f'font-weight="700" fill="{WHITE}">ACL  risk-team</text>'
                    f'<text x="{SPAN_X+214}" y="{y+60}" font-family="{DISPLAY}" font-size="26" '
                    f'font-weight="700" fill="{RED}">≠</text>'
                    f'<rect x="{SPAN_X+238}" y="{y+36}" width="200" height="34" fill="#2C1A1D"/>'
                    f'<text x="{SPAN_X+248}" y="{y+58}" font-family="{MONO}" font-size="14" '
                    f'font-weight="700" fill="{WHITE}">CALLER  customer</text>'
                    f"</g>"
                )
                continue
            ghost = kind == "ghost"
            p.append(
                f'<g opacity="{op}">'
                f'<rect x="{SPAN_X}" y="{y}" width="{SPAN_W}" height="{SPAN_H}" fill="{PLATE_2}" '
                f'stroke="{LINE}"/>'
                f'<text x="{SPAN_X+18}" y="{y+28}" font-family="{MONO}" font-size="26" '
                f'font-weight="700" fill="{"#9C9AA3" if ghost else "#E8E6EE"}">{name}</text>'
                f'{_chips(SPAN_X + 18, y + 42, ["source", "ACL", "hash"], ghost=ghost)}'
                f"</g>"
            )

    # ---- bindings
    if show_claims and bound > 0:
        for i in range(min(bound, 5)):
            y = _row_y(i) + SPAN_H / 2
            d = dim_claim or dim_span
            if highlight == "resp" and i == 4:
                d = False
            if highlight == "perf":
                d = True
            col = RED if i == 4 else "#6E7079"
            o = DIM if d else (GLANCE_DIM if glance else 1)
            p.append(
                f'<line x1="{SPAN_X + SPAN_W}" y1="{y}" x2="{CLAIM_X}" y2="{y}" stroke="{col}" '
                f'stroke-width="{2.6 if i == 4 else 1.8}" opacity="{o}"/>'
                f'<circle cx="{SPAN_X + SPAN_W + 6}" cy="{y}" r="4" fill="{col}" opacity="{o}"/>'
                f'<circle cx="{CLAIM_X - 6}" cy="{y}" r="4" fill="{col}" opacity="{o}"/>'
            )
        if bound >= 5:
            uy = _row_y(5) + SPAN_H / 2
            p.append(
                f'<line x1="{SPAN_X + SPAN_W}" y1="{uy}" x2="{CLAIM_X}" y2="{uy}" stroke="{RED}" '
                f'stroke-width="5.5" stroke-dasharray="8 7"/>'
                f'<circle cx="{SPAN_X + SPAN_W + 6}" cy="{uy}" r="5" fill="{RED}"/>'
                f'<circle cx="{CLAIM_X - 6}" cy="{uy}" r="5" fill="{RED}"/>'
            )

    # ---- CLAIM column (named claims — never anonymous red circles)
    if show_claims:
        for i, _label in enumerate([*CLAIMS, None]):
            y = _row_y(i)
            cy = y + SPAN_H / 2
            is_clause = i == 5
            is_red = is_clause or i >= bound
            d = dim_claim and not (highlight == "perf" and is_red)
            if is_red and highlight in ("resp", "cost"):
                d = True
            op = DIM if d else 1
            if is_clause:
                p.append(
                    f'<g opacity="{op}">'
                    f'<rect x="{CLAIM_X}" y="{y}" width="{CLAIM_W}" height="{SPAN_H}" '
                    f'fill="#2E1116" stroke="{RED}" stroke-width="5"/>'
                    f'<rect x="{CLAIM_X}" y="{y}" width="12" height="{SPAN_H}" fill="{RED}"/>'
                    f'<text x="{CLAIM_X+28}" y="{y+34}" font-family="{MONO}" font-size="26" '
                    f'font-weight="700" fill="{RED}">clause 7.2</text>'
                    f'<text x="{CLAIM_X+28}" y="{y+62}" font-family="{MONO}" font-size="17" '
                    f'font-weight="700" fill="{RED}">no span — UNSUPPORTED</text>'
                    f"</g>"
                )
            elif i >= bound:
                p.append(
                    f'<g opacity="{op}">'
                    f'<rect x="{CLAIM_X}" y="{y}" width="{CLAIM_W}" height="{SPAN_H}" '
                    f'fill="#1A1214" stroke="{RED}" stroke-width="3"/>'
                    f'<text x="{CLAIM_X+20}" y="{y+36}" font-family="{MONO}" font-size="26" '
                    f'font-weight="700" fill="{RED}">{CLAIMS[i]}</text>'
                    f'<text x="{CLAIM_X+20}" y="{y+62}" font-family="{MONO}" font-size="17" '
                    f'fill="{RED}">UNSUPPORTED</text>'
                    f"</g>"
                )
            else:
                bop = (0.78 if glance else 0.9) if op == 1 else op
                p.append(
                    f'<g opacity="{bop}">'
                    f'<rect x="{CLAIM_X}" y="{y}" width="{CLAIM_W}" height="{SPAN_H}" '
                    f'fill="{PLATE_2}" stroke="{LINE}"/>'
                    f'<rect x="{CLAIM_X}" y="{y}" width="8" height="{SPAN_H}" fill="{BOUND}"/>'
                    f'<circle cx="{CLAIM_X+32}" cy="{cy}" r="7" fill="{BOUND}"/>'
                    f'<text x="{CLAIM_X+52}" y="{cy+7}" font-family="{MONO}" font-size="26" '
                    f'font-weight="600" fill="#E0DEE6">{CLAIMS[i]}</text>'
                    f"</g>"
                )

    if show_claims and bound >= 5 and show_gate:
        cy = _row_y(5) + SPAN_H / 2
        op = DIM if highlight in ("resp", "cost") else 1
        p.append(
            f'<g opacity="{op}">'
            f'<line x1="{CLAIM_X + CLAIM_W}" y1="{cy}" x2="{GATE_X - 20}" y2="{cy}" stroke="{RED}" '
            f'stroke-width="7"/>'
            f'<line x1="{GATE_X-22}" y1="{cy-22}" x2="{GATE_X+22}" y2="{cy+22}" stroke="{RED}" '
            f'stroke-width="9"/>'
            f'<line x1="{GATE_X+22}" y1="{cy-22}" x2="{GATE_X-22}" y2="{cy+22}" stroke="{RED}" '
            f'stroke-width="9"/></g>'
        )

    # ---- ACTION: ONE full-height plate. Never five empty wells. Never range(6).
    if show_action:
        op = 0.22 if dim_act else 1
        held_y = _row_y(5) + SPAN_H / 2
        rail_x = ACT_X + 40
        p.append(
            f'<g opacity="{op}">'
            f'<rect x="{ACT_X}" y="{ROW0}" width="{ACT_W}" height="{BODY_BOT - ROW0}" '
            f'fill="#16181F" stroke="#3A3C48" stroke-width="2"/>'
            f'<rect x="{ACT_X}" y="{ROW0}" width="10" height="{BODY_BOT - ROW0}" fill="{RED}"/>'
            f'<text x="{ACT_X + 36}" y="{ROW0 + 40}" font-family="{MONO}" font-size="14" '
            f'font-weight="700" letter-spacing="2" fill="#9A9690">REFUND · R3 · IRREVERSIBLE</text>'
            f'<text x="{ACT_X + 36}" y="{ROW0 + 108}" font-family="{DISPLAY}" font-size="72" '
            f'font-weight="700" fill="{WHITE}" letter-spacing="-1.8">₹1,84,000</text>'
            f'<text x="{ACT_X + 36}" y="{ROW0 + 140}" font-family="{MONO}" font-size="17" '
            f'fill="#C8C6CE">vendor agreement · finance/refund-agent</text>'
            f'<text x="{ACT_X + 36}" y="{ROW0 + 196}" font-family="{MONO}" font-size="14" '
            f'fill="#9A9690">gate reason</text>'
            f'<text x="{ACT_X + 36}" y="{ROW0 + 226}" font-family="{MONO}" font-size="26" '
            f'font-weight="700" fill="{RED}">clause 7.2 — no span</text>'
            f'<text x="{ACT_X + 36}" y="{ROW0 + 254}" font-family="{MONO}" font-size="17" '
            f'fill="#E0DEE6">verdict  UNSUPPORTED · categorical</text>'
            f'<line x1="{rail_x}" y1="{ROW0 + 280}" x2="{rail_x}" y2="{held_y - 44:.1f}" '
            f'stroke="#6A3036" stroke-width="3" stroke-dasharray="5 7"/>'
            f'<rect x="{ACT_X + 16}" y="{held_y - 36:.1f}" width="{ACT_W - 32}" height="72" '
            f'fill="#3A1014" stroke="{RED}" stroke-width="3.5"/>'
            f'<text x="{ACT_X + 36}" y="{held_y + 2:.1f}" font-family="{MONO}" font-size="14" '
            f'font-weight="700" letter-spacing="1.5" fill="#F0A0A4">ACTUATOR</text>'
            f'<text x="{ACT_X + 36}" y="{held_y + 28:.1f}" font-family="{DISPLAY}" font-size="28" '
            f'font-weight="700" fill="{RED}">HELD — not executed</text>'
            f"</g>"
        )

    # ---- Three leader LINES tapping the graph (STAGE4 pre-flight #5). Never panels.
    if show_leaders:
        def leader_line(x1, y1, x2, y2, axis, label, on, col):
            o = 1 if on else 0.12
            return (
                f'<g opacity="{o}">'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
                f'stroke-width="1.6"/>'
                f'<circle cx="{x1}" cy="{y1}" r="3.5" fill="{col}"/>'
                f'<text x="{x2 + 8}" y="{y2 - 6}" font-family="{DISPLAY}" font-size="11" '
                f'font-weight="700" letter-spacing="1.8" fill="{col}">{axis}</text>'
                f'<text x="{x2 + 8}" y="{y2 + 16}" font-family="{DISPLAY}" font-size="26" '
                f'font-weight="700" fill="{WHITE}">{label}</text></g>'
            )

        p.append(leader_line(
            STEP_X + STEP_W / 2, BODY_BOT - 8,
            STEP_X, BAND_Y + 28,
            "COST", "Unused Step",
            highlight in (None, "cost", "all"), C_COST,
        ))
        bill_y = _row_y(4) + SPAN_H / 2
        p.append(leader_line(
            SPAN_X + SPAN_W - 20, bill_y,
            SPAN_X + 40, BAND_Y + 28,
            "RESPONSIBILITY", "Unentitled Span",
            highlight in (None, "resp", "all"), C_RESP,
        ))
        claim_y = _row_y(5) + SPAN_H
        p.append(leader_line(
            CLAIM_X + CLAIM_W / 2, claim_y - 8,
            CLAIM_X + 40, BAND_Y + 28,
            "PERFORMANCE", "Unbound Claim",
            highlight in (None, "perf", "all"), C_PERF,
        ))

    if chrome:
        p.append(
            f'<text x="56" y="1004" font-family="{DISPLAY}" font-size="26" font-weight="700" '
            f'fill="{WHITE}">Three dimensions, one graph.</text>'
            f'<text x="56" y="1038" font-family="{DISPLAY}" font-size="24" font-weight="600" '
            f'fill="#C8C6CE">The system didn’t fail. It was never asked to prove anything.</text>'
        )

    p.append("</svg>")
    return "".join(p)
