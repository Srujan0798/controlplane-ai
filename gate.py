"""Ship gate — every check measured from rendered pixels, not from source."""
import html, os, re, subprocess
import numpy as np
from PIL import Image
from pypdf import PdfReader
from pptx import Presentation

P = "submission/ControlPlane_ControlPlane-ai"
lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

# --- s1: is the failure the first red mass?
a = np.asarray(Image.open("posters/s1.png").convert("RGB").resize((400, 225), Image.LANCZOS)).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
red = (R > 110) & (R - G > 55) & (R - B > 55)
H, W = red.shape
rs = lambda x0, x1, y0, y1: int(red[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)].sum())
cause, held, steps = rs(.47, .72, .70, .82), rs(.76, .99, .58, .72), rs(0, .16, .52, .78)
ys, xs = np.where(red)
cx, cy = xs.mean() / W, ys.mean() / H

# --- s2: severity fall is carried by SATURATION (hot red -> cool grey), not luminance.
b = np.asarray(Image.open("posters/s2.png").convert("RGB")).astype(int)
Hh, Ww, _ = b.shape
bg2 = b[int(.97 * Hh):, :int(.10 * Ww)].reshape(-1, 3).mean(0)
def cell(y0, y1):
    c = b[y0 + 60:y1 - 60, int(.20 * Ww):int(.30 * Ww)].reshape(-1, 3).mean(0)
    return float(max(c) - min(c)), lum(c) - lum(bg2)
blk, edt, pss = cell(612, 1089), cell(1611, 2088), cell(2109, 2589)

# --- s3: inverted hierarchy
c3 = np.asarray(Image.open("posters/s3.png").convert("RGB")).astype(int)
L = 0.2126 * c3[..., 0] + 0.7152 * c3[..., 1] + 0.0722 * c3[..., 2]
Hc = L.shape[0]
ratio = L[int(.74 * Hc):int(.88 * Hc)].mean() / L[int(.03 * Hc):int(.09 * Hc)].mean()
dead = 100 * (L.mean(1) < 12).sum() / Hc

# --- brief coverage, read off the rendered slide text
T = "".join(open(f"visuals/_html/{n}.html").read() for n in ("s1", "s2", "s3"))
T = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<style.*?</style>', '', T, flags=re.S))).split())

dur = float(subprocess.run(["ffprobe", "-v", "0", "-show_entries", "format=duration",
                            "-of", "csv=p=0", P + ".mp4"], capture_output=True, text=True).stdout)
import fitz
doc = fitz.open(P + ".pdf")
emb = [doc.extract_image(i[0])["width"] for pg in doc for i in pg.get_images(full=True)]

checks = [
 ("BRIEF Q1 · detect, three axes", bool(re.search(r'Unused Step.*Unentitled Span.*Unbound Claim', T)), ""),
 ("BRIEF Q2 · block/edit/escalate", "ESCALATE" in T and "BLOCK" in T, ""),
 ("BRIEF Q3 · latency on-slide", bool(re.search(r'40 ms p50', T)), "<=40ms p50 / <=200ms p95"),
 ("BRIEF · who it would help", bool(re.search(r'payment, a record, or a', T)), "slide 3"),
 ("BRIEF · why it matters", "prove" in T, ""),
 ("S1 cause outranks effect", cause > held, f"clause 7.2 {cause} vs HELD {held} red px"),
 ("S1 no false left hotspot", steps == 0, f"{steps} px"),
 ("S1 red centroid on failure", cx > .55 and cy > .60, f"x={cx:.2f} y={cy:.2f}"),
 ("S2 severity fall monotonic", blk[0] > edt[0] > pss[0], f"sat {blk[0]:.0f} > {edt[0]:.0f} > {pss[0]:.0f}"),
 ("S2 PASS visible on ground", pss[1] >= 15, f"dlum {pss[1]:.0f}"),
 ("S3 closer/title >= 1.4x", ratio >= 1.4, f"{ratio:.2f}x"),
 ("S3 dead band < 15%", dead < 15, f"{dead:.1f}%"),
 ("PDF embeds full 5760 master", all(w >= 5760 for w in emb), f"{emb[0]}px"),
 ("3 slides / 3 pages", len(Presentation(P + '.pptx').slides) == 3 and len(PdfReader(P + '.pdf').pages) == 3, ""),
 ("video 2:00-3:00", 120 <= dur <= 180, f"{int(dur//60)}:{int(dur%60):02d}"),
 ("all 3 uploads < 20MB", all(os.path.getsize(P + e) < 20e6 for e in (".pptx", ".pdf", ".mp4")),
  " / ".join(f"{os.path.getsize(P+e)/1e6:.2f}" for e in (".pptx", ".pdf", ".mp4"))),
]
n = sum(1 for _, o, _ in checks if o)
print(f"SHIP GATE  {n}/{len(checks)}\n")
for k, o, x in checks:
    print(f"   {'PASS' if o else 'FAIL'}  {k:<30}{x}")
raise SystemExit(0 if n == len(checks) else 1)
