#!/usr/bin/env python3
"""Build excellence prototype mp4: chaptered screen + macOS TTS voiceover.

Output: submission/ControlPlane_Round2_Prototype.mp4 (1920x1080, with audio).
Requires server on :8787 and ffmpeg + say.
"""
from __future__ import annotations

import json
import subprocess
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "submission" / "_video_work" / "v2"
FINAL = ROOT / "submission" / "ControlPlane_Round2_Prototype.mp4"
BASE = "http://127.0.0.1:8787"
UNGATED = (
    "Approved. Refund of ₹1,84,000 issued under clause 7.2 of the vendor agreement. "
    "Customer account flagged for goodwill override."
)

CHAPTERS = [
    (
        "01_failure",
        "Approved. Refund of one lakh eighty four thousand rupees issued under clause seven point two. "
        "Confidence zero point nine four. Money moved Tuesday, found Friday. "
        "Clause seven point two does not exist.",
        175,
    ),
    (
        "02_reframe",
        "Step, span, claim, action. Not text to be scored — claims requesting permission to act. "
        "Provenance lives outside the model. The interlock is the sole decider.",
        175,
    ),
    (
        "03_mechanism",
        "Paste fresh into the gate. Claims extract themselves with types and hedging. "
        "The amount recomputes under Indian digit grouping — one lakh eighty four thousand equals one hundred eighty four thousand I N R. "
        "Clause seven point two is absent from the provenance set — unsupported, not contradicted. "
        "Show text at R1 becomes Edit. Issue refund at R3 becomes Escalate, held with the evidence packet. "
        "Never blocked. Zero L L M on lane one.",
        168,
    ),
    (
        "04_numbers",
        "Make eval. We publish false negative rate with a Wilson confidence interval on a self authored corpus. "
        "Hard negatives included. Production traffic evidence we do not claim. "
        "Every team will claim detection. We publish what we miss.",
        172,
    ),
    (
        "05_close",
        "That system was never asked to prove anything. Now nothing acts until it can prove it should. "
        "Held and escalated with the evidence packet.",
        165,
    ),
]


def _say(text: str, out_wav: Path, rate: int) -> float:
    aiff = out_wav.with_suffix(".aiff")
    subprocess.check_call(["say", "-v", "Samantha", "-r", str(rate), "-o", str(aiff), text])
    subprocess.check_call(
        ["ffmpeg", "-y", "-i", str(aiff), str(out_wav)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(out_wav),
            ],
            text=True,
        ).strip()
    )


def _card_html(path: Path, title: str, body: str) -> None:
    path.write_text(
        f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<style>
html,body{{margin:0;height:100%;background:#0b1020;color:#e8edf7;font-family:Menlo,monospace}}
.wrap{{display:flex;flex-direction:column;justify-content:center;align-items:center;height:100%;padding:80px;text-align:center}}
h1{{font-size:56px;margin:0 0 28px}} p{{font-size:26px;color:#9aa7c2;max-width:1200px;line-height:1.5}}
.tag{{margin-top:40px;color:#4ea1ff;letter-spacing:2px;text-transform:uppercase;font-size:18px}}
</style></head><body><div class=wrap>
<h1>{title}</h1><p>{body}</p>
<div class=tag>ControlPlane.ai · prototype · held ≠ blocked</div>
</div></body></html>""",
        encoding="utf-8",
    )


def _record_page(page, url: str, seconds: float, out_webm: Path) -> None:
    # Playwright records whole context; we capture per-chapter by separate contexts
    pass


def main() -> int:
    from playwright.sync_api import sync_playwright

    WORK.mkdir(parents=True, exist_ok=True)
    audio_dir = WORK / "audio"
    audio_dir.mkdir(exist_ok=True)
    cards = WORK / "cards"
    cards.mkdir(exist_ok=True)

    # TTS
    durs = {}
    for name, text, rate in CHAPTERS:
        wav = audio_dir / f"{name}.wav"
        durs[name] = _say(text, wav, rate)
        print(f"VO {name}: {durs[name]:.2f}s")

    # FNR from eval
    fnr = "measured"
    ci = ""
    last = ROOT / "evals" / "last_run.json"
    if last.exists():
        s = json.loads(last.read_text()).get("summary") or json.loads(last.read_text())
        fnr = s.get("published_fnr", fnr)
        ci = s.get("published_fnr_wilson_95") or s.get("published_fnr_ci") or ""

    _card_html(
        cards / "01_failure.html",
        "The failure",
        "Approved. Refund of ₹1,84,000 under clause 7.2. Confidence 0.94. Clause 7.2 does not exist.",
    )
    _card_html(
        cards / "02_reframe.html",
        "STEP → SPAN → CLAIM → ACTION",
        "Not text to be scored — claims requesting permission to act.",
    )
    _card_html(
        cards / "04_numbers.html",
        "Publish what we miss",
        f"make eval → published FNR = {fnr} (95% CI {ci}). Self-authored corpus. Production FNR unknown.",
    )
    _card_html(
        cards / "05_close.html",
        "Nothing acts until it can prove it should.",
        "Held and escalated with the evidence packet. Zero LLM on Lane 1.",
    )

    chapter_mp4s: list[Path] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        def capture(html_or_url: str, seconds: float, out: Path, live: bool = False) -> None:
            vdir = WORK / f"cap_{out.stem}"
            if vdir.exists():
                import shutil

                shutil.rmtree(vdir)
            vdir.mkdir()
            ctx = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                record_video_dir=str(vdir),
                record_video_size={"width": 1920, "height": 1080},
            )
            page = ctx.new_page()
            if live:
                page.goto(html_or_url, wait_until="networkidle")
                page.wait_for_timeout(800)
                page.fill("#text", "")
                page.type("#text", UNGATED, delay=12)
                if page.locator("#actionTier").count():
                    page.select_option("#actionTier", "R3")
                page.click("#run")
                page.wait_for_timeout(2500)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                # hold remaining
                hold_ms = max(1000, int(seconds * 1000) - 6000)
                page.wait_for_timeout(hold_ms)
            else:
                page.goto(html_or_url if html_or_url.startswith("http") else Path(html_or_url).as_uri())
                page.wait_for_timeout(int(seconds * 1000))
            ctx.close()
            webms = list(vdir.glob("*.webm"))
            if not webms:
                raise RuntimeError(f"no webm for {out}")
            subprocess.check_call(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(webms[0]),
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-an",
                    str(out),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        # 01 failure
        out = WORK / "01_failure.mp4"
        capture(str(cards / "01_failure.html"), durs["01_failure"] + 1.5, out)
        chapter_mp4s.append(out)

        # 02 reframe
        out = WORK / "02_reframe.mp4"
        capture(str(cards / "02_reframe.html"), durs["02_reframe"] + 1.2, out)
        chapter_mp4s.append(out)

        # 03 live gate — pad to VO length
        out = WORK / "03_mechanism.mp4"
        capture(f"{BASE}/gate", durs["03_mechanism"] + 8.0, out, live=True)
        chapter_mp4s.append(out)

        # 04 numbers
        out = WORK / "04_numbers.mp4"
        capture(str(cards / "04_numbers.html"), durs["04_numbers"] + 1.5, out)
        chapter_mp4s.append(out)

        # 05 close
        out = WORK / "05_close.mp4"
        capture(str(cards / "05_close.html"), durs["05_close"] + 2.0, out)
        chapter_mp4s.append(out)

        browser.close()

    # Concat video
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in chapter_mp4s), encoding="utf-8")
    silent = WORK / "silent.mp4"
    subprocess.check_call(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c",
            "copy",
            str(silent),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Build full VO with pads matching chapter extras roughly
    # Simpler: concat wavs with 1.0s silence between, then mux and stretch video if needed
    parts = [audio_dir / f"{n}.wav" for n, _, _ in CHAPTERS]
    vo = audio_dir / "vo_full.wav"
    # use ffmpeg concat demuxer for audio
    alst = WORK / "ac.txt"
    lines = []
    for i, p in enumerate(parts):
        lines.append(f"file '{p.resolve()}'\n")
        if i < len(parts) - 1:
            # generate silence file once
            sil = audio_dir / "sil.wav"
            if not sil.exists():
                subprocess.check_call(
                    [
                        "ffmpeg",
                        "-y",
                        "-f",
                        "lavfi",
                        "-i",
                        "anullsrc=r=22050:cl=mono",
                        "-t",
                        "1.0",
                        str(sil),
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            lines.append(f"file '{sil.resolve()}'\n")
    alst.write_text("".join(lines), encoding="utf-8")
    subprocess.check_call(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(alst), "-c", "copy", str(vo)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Mux: shortest ends when video ends; pad video to audio if audio longer
    vdur = float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(silent),
            ],
            text=True,
        ).strip()
    )
    adur = float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(vo),
            ],
            text=True,
        ).strip()
    )
    print(f"video {vdur:.1f}s audio {adur:.1f}s")
    # Pad video to at least 210s (3:30) with tpad if needed
    target = max(210.0, adur + 2.0, vdur)
    padded = WORK / "padded.mp4"
    pad_extra = max(0.0, target - vdur)
    if pad_extra > 0.5:
        subprocess.check_call(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(silent),
                "-vf",
                f"tpad=stop_mode=clone:stop_duration={pad_extra}",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                str(padded),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        padded = silent

    # Pad audio to video length
    apadded = WORK / "vo_padded.wav"
    subprocess.check_call(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(vo),
            "-af",
            f"apad=whole_dur={target}",
            str(apadded),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    FINAL.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(padded),
            "-i",
            str(apadded),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            "-movflags",
            "+faststart",
            str(FINAL),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    final_dur = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(FINAL),
        ],
        text=True,
    ).strip()
    print("Wrote", FINAL, "duration", final_dur, "size", FINAL.stat().st_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
