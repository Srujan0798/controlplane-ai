#!/usr/bin/env python3
"""FORM UPLOAD — 3 slides PPTX + PDF ≤20 MB each. High quality, not 0.3 MB mush, not 15 MB empty PNG bloat."""
from __future__ import annotations

import os
import shutil
from io import BytesIO
from pathlib import Path

import img2pdf
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Inches

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent
SUB = ROOT / "submission"
OUT_PPTX = SUB / "ControlPlane_ControlPlane-ai.pptx"
OUT_PDF = SUB / "ControlPlane_ControlPlane-ai.pdf"

POSTERS = [
    ROOT / "posters" / "s1.png",
    ROOT / "posters" / "s2.png",
    ROOT / "posters" / "s3.png",
]
SW, SH = 13.333333, 7.5
# Cap long edge so 8× agent renders still embed cleanly; 3× source stays as-is.
MAX_EDGE = 3840
JPEG_Q = 96


def _to_jpeg(path: Path) -> BytesIO:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    scale = min(1.0, MAX_EDGE / max(w, h))
    if scale < 1.0:
        im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    buf = BytesIO()
    im.save(buf, "JPEG", quality=JPEG_Q, optimize=True, progressive=True, subsampling=0)
    buf.seek(0)
    return buf


def build_pptx() -> int:
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    blank = prs.slide_layouts[6]
    for png in POSTERS:
        assert png.exists(), f"missing {png} — run python3 -m visuals.render"
        slide = prs.slides.add_slide(blank)
        for sh in list(slide.shapes):
            sp = sh._element
            sp.getparent().remove(sp)
        slide.shapes.add_picture(
            _to_jpeg(png), Emu(0), Emu(0), prs.slide_width, prs.slide_height
        )
    assert len(prs.slides) == 3
    SUB.mkdir(exist_ok=True)
    prs.save(OUT_PPTX)
    return OUT_PPTX.stat().st_size


def build_pdf() -> int:
    pages = []
    for png in POSTERS:
        tmp = ROOT / "posters" / f"_pdf_{png.stem}.jpg"
        im = Image.open(png).convert("RGB")
        w, h = im.size
        scale = min(1.0, MAX_EDGE / max(w, h))
        if scale < 1.0:
            im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        im.save(tmp, "JPEG", quality=JPEG_Q, optimize=True, progressive=True, subsampling=0)
        pages.append(str(tmp))
    layout = img2pdf.get_layout_fun(pagesize=(img2pdf.in_to_pt(SW), img2pdf.in_to_pt(SH)))
    data = img2pdf.convert(pages, layout_fun=layout)
    SUB.mkdir(exist_ok=True)
    OUT_PDF.write_bytes(data)
    for p in pages:
        try:
            os.remove(p)
        except OSError:
            pass
    return OUT_PDF.stat().st_size


def sync_video() -> None:
    candidates = [
        ROOT / "video" / "ControlPlane_ControlPlane-ai.mp4",
    ]
    dest = SUB / "ControlPlane_ControlPlane-ai.mp4"
    for c in candidates:
        if c.exists() and c.stat().st_size > 100_000:
            shutil.copy2(c, dest)
            print(f"video: {dest}  {dest.stat().st_size/1e6:.2f} MB  / 20")
            return
    print("video: missing")


def main():
    n = build_pptx()
    m = build_pdf()
    sync_video()
    print(f"slides: 3")
    print(f"PPTX  {OUT_PPTX}  {n/1e6:.2f} MB  / 20")
    print(f"PDF   {OUT_PDF}   {m/1e6:.2f} MB  / 20")
    assert n < 20 * 1024 * 1024 and m < 20 * 1024 * 1024
    assert n > 400_000, "too small — quality crushed"
    print("OK — form upload ready in submission/")


if __name__ == "__main__":
    main()
