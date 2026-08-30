#!/usr/bin/env python3
"""Render docs/reference/architecture.png — the architecture + blast-radius matrix hero diagram.

Used by scripts/build_readme_pdf.py and round2/CONTROLPLANE_R2_FINAL.md (proposal).
Brand colors match submission/ControlPlane_Round2_Pitch.js (dark theme, rust accent).
No external deps beyond Pillow (already in the venv).
"""
from __future__ import annotations

import pathlib
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "reference" / "architecture.png"

W, H = 1600, 1040

BG          = (11, 15, 26)
PANEL       = (15, 21, 37)
PANEL_HI    = (22, 32, 50)
BORDER      = (30, 42, 61)
BORDER_HI   = (45, 58, 82)
RUST        = (201, 162, 39)
CREAM       = (245, 240, 235)
WARM        = (208, 200, 184)
AMBER       = (212, 175, 55)
MUTED       = (136, 146, 176)
RED_BG      = (42, 12, 8)
AMBER_BG    = (50, 28, 8)
HI_BG       = (58, 22, 10)


def _font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    f_title = _font(40)
    f_sub = _font(18)
    f_eyebrow = _font(14)
    f_node = _font(30)
    f_node_sub = _font(15)
    f_mat_hdr = _font(17)
    f_mat_row = _font(22)
    f_mat_cell = _font(22)
    f_foot = _font(16)
    f_center = _font(16)

    # ---- Title ----
    d.text((W // 2, 38), "CONTROLPLANE.AI", fill=RUST, font=f_eyebrow, anchor="mm")
    d.text(
        (W // 2, 80),
        "Architecture  &  Blast-Radius Matrix",
        fill=CREAM,
        font=f_title,
        anchor="mm",
    )
    d.text(
        (W // 2, 128),
        "Provenance outside the model  ·  default UNSUPPORTED  ·  entitlement as set-membership  ·  hard gate on the commit path",
        fill=MUTED,
        font=f_sub,
        anchor="mm",
    )

    # ---- Pipeline: STEP -> SPAN -> CLAIM -> ACTION ----
    nodes = [
        ("STEP",    "produces",   "Tool call, retrieval,\nmodel turn."),
        ("SPAN",    "binds",      "Chunk, tool row, DB record.\nsource · ACL · hash · offsets."),
        ("CLAIM",   "authorises", "Typed atomic proposition\nfrom the output stream."),
        ("ACTION",  "executes",   "Pending side effect:\ntool + args + irreversibility."),
    ]
    ny = 180
    bw = 320
    bh = 210
    arrow_w = 60
    total = 4 * bw + 3 * arrow_w
    start_x = (W - total) // 2
    for i, (name, verb, desc) in enumerate(nodes):
        x = start_x + i * (bw + arrow_w)
        border = RUST if i == 3 else BORDER_HI
        d.rectangle([x, ny, x + bw, ny + bh], fill=PANEL, outline=border, width=2)
        d.text((x + bw // 2, ny + 38), f"0{i + 1}", fill=RUST, font=f_eyebrow, anchor="mm")
        d.text((x + bw // 2, ny + 78), name, fill=CREAM, font=f_node, anchor="mm")
        d.text((x + bw // 2, ny + 118), verb, fill=RUST, font=f_node_sub, anchor="mm")
        d.multiline_text(
            (x + bw // 2, ny + 160),
            desc,
            fill=WARM,
            font=f_node_sub,
            anchor="ma",
            align="center",
        )
        if i < 3:
            ax0 = x + bw + 6
            ax1 = x + bw + arrow_w - 6
            ay = ny + bh // 2
            d.line([(ax0, ay), (ax1, ay)], fill=RUST, width=3)
            d.polygon(
                [(ax1, ay - 10), (ax1 + 12, ay), (ax1, ay + 10)],
                fill=RUST,
            )

    # ---- Matrix ----
    mx0 = 80
    my0 = 470
    n_cols = 5
    n_rows = 5  # header + R3..R0
    cell_w = (W - 2 * mx0) // n_cols
    cell_h = 86

    cols = [
        "",
        "Contradicted /\nentitlement violation",
        "Unsupported\n+ categorical",
        "Unsupported\n+ hedged",
        "Unknown",
    ]
    rows = ["R3", "R2", "R1", "R0"]
    actuators = [
        ["Block", "Escalate", "Escalate", "Escalate"],
        ["Block", "Edit",     "Edit",     "Escalate"],
        ["Edit",  "Edit",     "Pass+ann", "Pass+ann"],
        ["Pass+ann","Pass+ann","Pass",   "Pass"],
    ]
    centerpieces = {(0, 1), (2, 0), (3, 1)}

    # header row
    for c, txt in enumerate(cols):
        x = mx0 + c * cell_w
        d.rectangle([x, my0, x + cell_w, my0 + cell_h], fill=PANEL_HI, outline=BORDER, width=1)
        if txt:
            d.multiline_text(
                (x + cell_w // 2, my0 + cell_h // 2),
                txt,
                fill=MUTED,
                font=f_mat_hdr,
                anchor="mm",
                align="center",
            )

    # data rows
    for r in range(4):
        y = my0 + (r + 1) * cell_h
        # row label
        d.rectangle([mx0, y, mx0 + cell_w, y + cell_h], fill=PANEL, outline=BORDER, width=1)
        d.text((mx0 + cell_w // 2, y + cell_h // 2), rows[r], fill=CREAM, font=f_mat_row, anchor="mm")
        for c in range(4):
            x = mx0 + (c + 1) * cell_w
            act = actuators[r][c]
            if act == "Block":
                bg, color = RED_BG, RUST
            elif act == "Escalate":
                bg, color = PANEL, AMBER
            elif act == "Edit":
                bg, color = PANEL, CREAM
            else:
                bg, color = PANEL, MUTED
            if (r, c) in centerpieces:
                bg = HI_BG
                color = RUST if act in ("Block", "Edit") else AMBER
            d.rectangle([x, y, x + cell_w, y + cell_h], fill=bg, outline=BORDER, width=1)
            d.text(
                (x + cell_w // 2, y + cell_h // 2),
                act,
                fill=color,
                font=f_mat_cell,
                anchor="mm",
            )

    # ---- Footer / legend ----
    fy = H - 70
    d.text(
        (W // 2, fy),
        "Same plane  ·  three reads (Performance, Cost, Responsibility)  ·  actuators: Block · Edit · Escalate · Pass · Pass+annotate",
        fill=MUTED,
        font=f_foot,
        anchor="mm",
    )
    d.text(
        (W // 2, fy + 30),
        "Centrepiece:  R3 × Unsupported+categorical → Escalate (held)   ·   R1 × Contradicted → Edit   ·   R2 × Unsupported+categorical → Edit",
        fill=RUST,
        font=f_center,
        anchor="mm",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {W}x{H})")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
