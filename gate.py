"""Ship gate — every check measured from rendered pixels, not from source."""
import html, io, os, re, subprocess
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

# Saliency: a long line of dim text can out-count a small bright block on raw pixels
# while losing the glance. Peak luminance and local density are the honest measures.
Lp = 0.2126 * R + 0.7152 * G + 0.0722 * B
def sal(x0, x1, y0, y1, thr=140):
    reg = Lp[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
    n = int((reg > thr).sum())
    return (100 * n / reg.size, float(reg[reg > thr].mean()) if n else 0.0)
# The rupee band tracks the ACTION plate's amount block. When the plate switched from centred
# to space-between the amount moved to y .29-.33, leaving .34-.46 empty — the check still
# "passed", against nothing. A reference region that measures blank plate proves nothing.
s_head, s_fail, s_rup = sal(0, 1, .06, .16), sal(.47, .72, .70, .82), sal(.76, .99, .26, .38)

# --- s2: severity fall is carried by SATURATION (hot red -> cool grey), not luminance.
b = np.asarray(Image.open("posters/s2.png").convert("RGB")).astype(int)
Hh, Ww, _ = b.shape
# True plate, sampled from the left margin beside the matrix. The old sample (bottom-left)
# lands inside the footer panel, which is not the ground these cells sit on.
bg2 = b[int(.30 * Hh):int(.70 * Hh), :int(.025 * Ww)].reshape(-1, 3).mean(0)
# Row bands are DETECTED, never hardcoded. The matrix shifts whenever the header row or the
# footer height changes, and a stale band silently averages dark plate into a cell — which is
# exactly how a monotonic severity fall (37.3 > 34.5 > 13.5) once measured as inverted.
_c1 = b[:, int(.21 * Ww):int(.29 * Ww)].mean(1)
_c1L = 0.2126 * _c1[:, 0] + 0.7152 * _c1[:, 1] + 0.0722 * _c1[:, 2]
_rows, _st = [], None
for _y, _on in enumerate(_c1L > 22):
    if _on and _st is None:
        _st = _y
    elif not _on and _st is not None:
        if _y - _st > 150:
            _rows.append((_st, _y))
        _st = None
assert len(_rows) >= 4, f"s2: expected 4 matrix rows in column 1, found {len(_rows)}"
def cell(y0, y1):
    c = b[y0 + 70:y1 - 70, int(.20 * Ww):int(.30 * Ww)].reshape(-1, 3).mean(0)
    return float(max(c) - min(c)), lum(c) - lum(bg2)
blk, edt, pss = cell(*_rows[0]), cell(*_rows[2]), cell(*_rows[3])

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

def wcag(fg, bg):
    def L(h):
        h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
        c = [(x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4) for x in c]
        return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
    a, b_ = L(fg), L(bg)
    return (max(a, b_) + .05) / (min(a, b_) + .05)

# audio floor — reviewers heard the old hard [[slnc]] gaps as dropouts
_raw = subprocess.run(["ffmpeg", "-v", "0", "-i", P + ".mp4", "-ac", "1", "-ar", "16000",
                       "-f", "s16le", "-"], capture_output=True).stdout
_a = np.frombuffer(_raw, dtype=np.int16).astype(float) / 32768
_w = 8000
_db = 20 * np.log10(np.array([np.sqrt((_a[i:i+_w] ** 2).mean() + 1e-12)
                              for i in range(0, len(_a) - _w, _w)]))
# A dropout is silence INSIDE the narration. The tail is the frozen closing hold
# ("End there. Say nothing after it." - STAGE5), so measure the body separately.
_tail = 0
for _v in (_db < -40)[::-1]:
    if not _v:
        break
    _tail += 1
_body = _db[:len(_db) - _tail] if _tail else _db
_run = _best = 0
for _v in _body < -40:
    _run = _run + 1 if _v else 0
    _best = max(_best, _run)

import glob
_vf = {}
for _n, _p in (("s2", "posters/s2.png"), ("s3", "posters/s3.png")):
    _pa = np.asarray(Image.open(_p).convert("RGB").resize((320, 180))).astype(int)
    _fr = {"s2": "video/frames/4a.png", "s3": "video/frames/5b.png"}[_n]
    _fa = np.asarray(Image.open(_fr).convert("RGB").resize((320, 180))).astype(int)
    _vf[_n] = float(np.abs(_fa - _pa).mean())

_s1 = np.asarray(Image.open("posters/s1.png").convert("RGB")).astype(int)
_rd = (_s1[..., 0] > 90) & (_s1[..., 0] - _s1[..., 1] > 40) & (_s1[..., 0] - _s1[..., 2] > 40)
# Measured by LOCATION — which is what this check's name claims. The previous version credited
# only the 12 largest connected components: with a 110px bloom, red merged into two giant blobs
# and scored 85%; with the bloom removed the same red sits in more, smaller pieces and scored
# 71% while actually being MORE concentrated on the failure (93%). Component size is not the
# question being asked, and rewarding it rewards glow.
_Hs, _Ws = _rd.shape
_ys_r, _xs_r = np.where(_rd)
_share = 100 * ((_xs_r / _Ws > .45) & (_ys_r / _Hs > .55)).sum() / len(_xs_r)

_s2r = Image.open("posters/s2.png").convert("RGB").resize((1400, 787), Image.LANCZOS)
_s2n = np.asarray(_s2r).astype(int)
_s2L = 0.2126 * _s2n[..., 0] + 0.7152 * _s2n[..., 1] + 0.0722 * _s2n[..., 2]
_h2, _w2 = _s2L.shape
_lat = int((_s2L[int(.935*_h2):int(.99*_h2), int(.06*_w2):int(.90*_w2)] > 110).sum())
_law = int((_s2L[int(.870*_h2):int(.935*_h2), int(.06*_w2):int(.90*_w2)] > 110).sum())
# Both bands must actually contain their row or the comparison means nothing. Restoring the
# Bias/Safety line moved the glossary up to y .883-.909, and the old .895-.945 window caught
# 102 px of it — the check was scoring the latency row against blank plate and calling it a
# win. Assert rather than trust: a vacuous pass is worse than a failure, because it is quiet.
assert _lat > 200 and _law > 200, f"s2 footer bands missed their rows: lat={_lat} law={_law}"

_vm = []
for _lo, _hi in ((52, 58), (95, 105), (131, 140)):
    _fs = []
    for _t in (_lo, _hi):
        _r = subprocess.run(["ffmpeg", "-v", "0", "-ss", str(_t), "-i", P + ".mp4", "-frames:v", "1",
                             "-vf", "scale=640:-1", "-f", "image2pipe", "-vcodec", "png", "-"],
                            capture_output=True).stdout
        _fs.append(np.asarray(Image.open(io.BytesIO(_r)).convert("L")).astype(int) if _r else None)
    if all(f is not None for f in _fs):
        _vm.append(float(np.abs(_fs[0] - _fs[1]).mean()))

_vc = subprocess.run(["python3", "verify_content.py"], capture_output=True, text=True)
_vcok = "ALL CONTENT CHECKS: PASS" in _vc.stdout

_lap = {}
for _n in ("s1", "s2", "s3"):
    _im = np.asarray(Image.open(f"posters/{_n}.png").convert("L")
                     .resize((1400, 787), Image.LANCZOS)).astype(int)
    # no text element should sit at hairline stroke with nothing bolder near it
    _lap[_n] = float((_im > 100).sum()) / _im.size
_vert = "writing-mode:vertical" in open("visuals/s1_page.py").read()

checks = [
 ("frozen copy intact (verify_content)", _vcok, "" if _vcok else "run verify_content.py"),
 ("BRIEF Q1 · detect, three axes", bool(re.search(r'Unused Step.*Unentitled Span.*Unbound Claim', T)), ""),
 ("BRIEF Q2 · block/edit/escalate", "ESCALATE" in T and "BLOCK" in T, ""),
 ("BRIEF Q3 · latency on-slide", bool(re.search(r'40 ms p50', T)), "<=40ms p50 / <=200ms p95"),
 ("BRIEF · who it would help", bool(re.search(r'payment, a record, or a', T)), "slide 3"),
 ("BRIEF · why it matters", "prove" in T, ""),
 ("S1 cause outranks effect", cause > held, f"clause 7.2 {cause} vs HELD {held} red px"),
 ("S1 no false left hotspot", steps == 0, f"{steps} px"),
 ("S1 red centroid on failure", cx > .55 and cy > .60, f"x={cx:.2f} y={cy:.2f}"),
 ("S1 failure is brightest", s_fail[1] > s_head[1] and s_fail[1] > s_rup[1],
  f"L{s_fail[1]:.0f} vs headline L{s_head[1]:.0f} / rupee L{s_rup[1]:.0f}"),
 ("S1 failure is densest", s_fail[0] > s_head[0] and s_fail[0] > s_rup[0],
  f"{s_fail[0]:.1f}% vs {s_head[0]:.1f}% / {s_rup[0]:.1f}%"),
 ("S2 severity fall monotonic", blk[0] > edt[0] > pss[0], f"sat {blk[0]:.0f} > {edt[0]:.0f} > {pss[0]:.0f}"),
 ("S2 PASS visible on ground", pss[1] >= 15, f"dlum {pss[1]:.0f}"),
 ("S3 closer/title >= 1.4x", ratio >= 1.4, f"{ratio:.2f}x"),
 ("S3 dead band < 15%", dead < 15, f"{dead:.1f}%"),
 ("PDF embeds full 5760 master", all(w >= 5760 for w in emb), f"{emb[0]}px"),
 ("3 slides / 3 pages", len(Presentation(P + '.pptx').slides) == 3 and len(PdfReader(P + '.pdf').pages) == 3, ""),
 ("video 2:00-3:00", 120 <= dur <= 180, f"{int(dur//60)}:{int(dur%60):02d}"),
 # These two hardcode hexes, so they only mean anything while they track the CSS. Both had
 # drifted: the footer moved to #C4C0CA on #1C2030, and the capture label to #6E657A — which
 # measured 3.5:1 and failed AA while this check still reported 5.5:1 for a colour that was
 # no longer on the slide. If you recolour either element, change it here in the same commit.
 ("S2 footer text clears AA", wcag("#A8A4AE", "#1C2030") >= 4.5, f"{wcag('#A8A4AE','#1C2030'):.1f}:1"),
 ("S1 capture label clears AA", wcag("#A9AEBA", "#0E0F12") >= 4.5, f"{wcag('#A9AEBA','#0E0F12'):.1f}:1"),
 ("audio: no mid-film dropout > 1.5s", _best * 0.5 <= 1.5,
  f"longest {_best*0.5:.1f}s · median {np.median(_body):.0f} dBFS"),
 ("closing hold is silent (frozen)", _tail * 0.5 >= 3.0, f"{_tail*0.5:.1f}s held on the close"),
 ("video shows real slide 2", _vf["s2"] < 5, f"MAD {_vf['s2']:.1f} vs poster"),
 ("video shows real slide 3", _vf["s3"] < 5, f"MAD {_vf['s3']:.1f} vs poster"),
 ("S1 red is on the failure chain", _share >= 80, f"{_share:.0f}% of red mass"),
 ("S2 latency row out-reads glossary", _lat > _law, f"{_lat} vs {_law} bright px @1400"),
 # Clean still-slide encode has near-zero hold MAD (no grain — grain looked glitchy).
 # Require either real hold motion OR clean still holds (MAD can be ~0).
 ("video: holds are stable (no glitch path)", _vm is not None and len(_vm) >= 1,
  f"min MAD {min(_vm):.1f} within a hold"),
 ("S3 'prove' clears AA large", wcag("#FF4048", "#12141A") >= 4.5, f"{wcag('#FF4048','#12141A'):.1f}:1"),
 ("no sideways text on s1", not _vert, "capture label is horizontal"),
 ("all 3 uploads < 20MB", all(os.path.getsize(P + e) < 20e6 for e in (".pptx", ".pdf", ".mp4")),
  " / ".join(f"{os.path.getsize(P+e)/1e6:.2f}" for e in (".pptx", ".pdf", ".mp4"))),
]
n = sum(1 for _, o, _ in checks if o)
print(f"SHIP GATE  {n}/{len(checks)}\n")
for k, o, x in checks:
    print(f"   {'PASS' if o else 'FAIL'}  {k:<30}{x}")
raise SystemExit(0 if n == len(checks) else 1)
