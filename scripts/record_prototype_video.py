#!/usr/bin/env python3
"""Record a prototype demo video of the live ControlPlane gate (T7.5).

Produces submission/ControlPlane_Round2_Prototype.mp4 via Playwright screen capture
of the running console + title cards. No voiceover (add separately per VIDEO_SCRIPT).

Requires: server on http://127.0.0.1:8787 and playwright chromium.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "submission" / "_video_work"
FINAL = ROOT / "submission" / "ControlPlane_Round2_Prototype.mp4"
BASE = "http://127.0.0.1:8787"

UNGATED = (
    "Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement. "
    "Customer account flagged for goodwill override."
)


def _write_card(path: Path, title: str, body: str) -> None:
    path.write_text(
        f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<style>
html,body{{margin:0;height:100%;background:#0b1020;color:#e8edf7;
font-family:ui-monospace,Menlo,monospace}}
.wrap{{display:flex;flex-direction:column;justify-content:center;align-items:center;
height:100%;padding:80px;text-align:center}}
h1{{font-size:64px;margin:0 0 24px;letter-spacing:1px}}
p{{font-size:28px;color:#9aa7c2;max-width:1100px;line-height:1.45;margin:0}}
.tag{{margin-top:36px;color:#4ea1ff;font-size:20px;letter-spacing:2px;text-transform:uppercase}}
</style></head><body><div class=wrap>
<h1>{title}</h1><p>{body}</p>
<div class=tag>ControlPlane.ai · prototype · held ≠ blocked</div>
</div></body></html>""",
        encoding="utf-8",
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cards = OUT_DIR / "cards"
    cards.mkdir(exist_ok=True)
    _write_card(
        cards / "01_failure.html",
        "The failure",
        "Approved. Refund of ₹1,84,000 under clause 7.2. Confidence 0.94. "
        "Money moved Tuesday. Clause 7.2 does not exist.",
    )
    _write_card(
        cards / "02_reframe.html",
        "STEP → SPAN → CLAIM → ACTION",
        "Not text to be scored — claims requesting permission to act.",
    )
    _write_card(
        cards / "03_close.html",
        "Nothing acts until it can prove it should.",
        "Held and escalated with the evidence packet. Zero LLM on Lane 1. "
        "We publish the false-negative rate — including what we miss.",
    )

    from playwright.sync_api import sync_playwright

    raw_webm = OUT_DIR / "gate_capture"
    if raw_webm.exists():
        import shutil

        shutil.rmtree(raw_webm)
    raw_webm.mkdir()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(raw_webm),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()

        # Title cards (paced for ~3:30 target with voiceover room)
        for name, hold in [
            ("01_failure.html", 18.0),
            ("02_reframe.html", 16.0),
        ]:
            page.goto((cards / name).as_uri())
            page.wait_for_timeout(int(hold * 1000))

        # Live gate — type slowly so the judge sees the paste
        page.goto(f"{BASE}/gate", wait_until="networkidle")
        page.wait_for_timeout(2500)
        page.click("#text")
        page.fill("#text", "")
        page.type("#text", UNGATED, delay=18)
        page.wait_for_timeout(2000)
        if page.locator("#actionTier").count():
            page.select_option("#actionTier", "R3")
        page.wait_for_timeout(1200)
        page.click("#run")
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(12000)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(4000)

        # Also hit refund demo JSON briefly via overlay page
        demo = page.evaluate(
            """async () => {
              const r = await fetch('/v1/controlplane/demo/refund?mode=enforce', {method:'POST'});
              return await r.json();
            }"""
        )
        overlay = OUT_DIR / "demo_overlay.html"
        acts = {
            k: (v.get("actuator") if isinstance(v, dict) else v)
            for k, v in (demo.get("decisions") or demo.get("actuators") or {}).items()
        }
        # public_dict shape varies — also check response_overlay
        if not acts and isinstance(demo.get("response_overlay"), dict):
            acts = demo["response_overlay"].get("actuators_would_apply") or {}
        overlay.write_text(
            f"""<!DOCTYPE html><html><head><meta charset=utf-8><style>
body{{margin:0;background:#0b1020;color:#e8edf7;font-family:Menlo,monospace;padding:60px}}
h1{{color:#4ea1ff}} .Escalate{{color:#ff6b6b;font-size:42px;font-weight:800}}
.Edit{{color:#ffb454;font-size:42px;font-weight:800}}
pre{{background:#121a30;padding:24px;border-radius:12px;font-size:20px;line-height:1.5}}
</style></head><body>
<h1>Refund demo — enforce mode (live API)</h1>
<p>Amount binds via <b>numeric</b> normalize — not fixtures. Clause 7.2 absent → UNSUPPORTED.</p>
<pre>{json.dumps({"request_id": demo.get("request_id"), "would_hold": demo.get("would_hold"), "actuators": acts}, indent=2)}</pre>
<p class=Escalate>issue_refund → Escalate (held with evidence packet)</p>
<p class=Edit>show_text → Edit (entitlement / ACL)</p>
</body></html>""",
            encoding="utf-8",
        )
        page.goto(overlay.as_uri())
        page.wait_for_timeout(18000)

        # Eval numbers card from last_run if present
        last = ROOT / "evals" / "last_run.json"
        fnr = "n/a"
        ci = ""
        if last.exists():
            data = json.loads(last.read_text())
            s = data.get("summary") or data
            fnr = s.get("published_fnr", s.get("fnr", "n/a"))
            ci = s.get("published_fnr_wilson_95") or s.get("published_fnr_ci") or ""
        nums = cards / "02b_numbers.html"
        _write_card(
            nums,
            "Published miss rate",
            f"make eval → published FNR = {fnr} (95% CI {ci}). Self-authored corpus. "
            "We publish what we miss.",
        )
        page.goto(nums.as_uri())
        page.wait_for_timeout(20000)

        page.goto((cards / "03_close.html").as_uri())
        page.wait_for_timeout(16000)

        context.close()
        browser.close()

    # Find recorded webm
    videos = list(raw_webm.glob("*.webm"))
    if not videos:
        print("No playwright webm produced", file=sys.stderr)
        return 1
    webm = videos[0]
    # Transcode to mp4
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(webm),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-an",
        str(FINAL),
    ]
    print("Running", " ".join(cmd))
    subprocess.check_call(cmd)
    print("Wrote", FINAL, "size", FINAL.stat().st_size)
    return 0


if __name__ == "__main__":
    # small delay so server is ready
    time.sleep(0.5)
    raise SystemExit(main())
