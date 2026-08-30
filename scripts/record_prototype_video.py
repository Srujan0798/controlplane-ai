#!/usr/bin/env python3
"""Rebuild prototype video with professional edge-tts voiceover + ffmpeg loudnorm.
Output: submission/ControlPlane_Round2_Prototype.mp4 (1920x1080, with smooth female VO).
Requires: server on :8787, ffmpeg, edge-tts, playwright chromium.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "submission" / "_video_work" / "v3"
FINAL = ROOT / "submission" / "ControlPlane_Round2_Prototype.mp4"
BASE = "http://127.0.0.1:8787"
UNGATED = (
    "Approved. Refund of INR 1,84,000 issued under clause 7.2 of the vendor agreement. "
    "Customer account flagged for goodwill override."
)

# Chapters: (name, TTS text, card title, card body)
# TTS uses en-IN-NeerjaExpressiveNeural — smooth, natural, expressive Indian English female
CHAPTERS = [
    (
        "01_failure",
        "Approved. Refund of one lakh eighty-four thousand rupees issued under clause seven point two of the vendor agreement. "
        "Confidence zero point nine four. Every filter in the pipeline passed it. The payout cleared on Tuesday morning. "
        "Nobody found it until Friday. "
        "Clause seven point two does not exist. "
        "Not a cap on refunds. Not a denial. Not a coverage gap. "
        "The clause is absent from the vendor agreement — full stop. "
        "There is no clause to cap, to deny, to cover, or to limit. "
        "The company wrongly paid one lakh eighty-four thousand rupees. "
        "The customer did not lose it — the company did. "
        "The system did not fail. It was never asked to prove anything.",
        "The failure",
        "Approved. Refund of INR 1,84,000 under clause 7.2. Confidence 0.94. "
        "Every filter passed. Payout cleared Tuesday. Found Friday. "
        "Clause 7.2 does not exist. Not a cap, not a denial, not a coverage gap. "
        "The company wrongly paid one lakh eighty-four thousand rupees. "
        "The customer did not lose it. The system did not fail — "
        "it was never asked to prove anything.",
    ),
    (
        "02_reframe",
        "Step, span, claim, action. That is the primitive. "
        "Not text to be scored — claims requesting permission to act. "
        "Every AI response that asks permission to issue a refund, "
        "send an email, publish a record — is a set of claims. "
        "Provenance lives outside the model. "
        "We capture every span at context assembly — source, "
        "access control list, content hash, byte offsets — then freeze. "
        "The model cannot invent a span after the fact. "
        "It has no channel to declare a binding. "
        "The interlock is the sole decider. "
        "Default verdict: unsupported. "
        "A claim must earn supported. "
        "Nothing passes because nobody objected. "
        "Absence of evidence is not evidence of absence — "
        "the claim stays unproven. "
        "Unknown never becomes supported. "
        "That single rule is the boundary between a control plane "
        "and false assurance.",
        "STEP → SPAN → CLAIM → ACTION",
        "Step, span, claim, action. The primitive. "
        "Not text to be scored — claims requesting permission to act. "
        "Every response that asks permission to act is a set of claims. "
        "Provenance lives outside the model. "
        "We capture every span at context assembly — "
        "source, ACL, hash, offsets — then freeze. "
        "The model cannot invent a span after the fact. "
        "It has no channel to declare a binding. "
        "The interlock is the sole decider. "
        "Default verdict: unsupported. A claim must earn supported. "
        "Nothing passes because nobody objected. "
        "Unknown never becomes supported.",
    ),
    (
        "03_mechanism",
        "Paste fresh into the gate. No fixtures. The claims extract themselves with types — "
        "numeric, structural, textual, temporal, derived — and hedging. "
        "The amount recomputes under Indian digit grouping — "
        "one lakh eighty-four thousand equals one hundred eighty-four thousand I N R. "
        "The structural symbol table looks for clause seven point two across every span in the provenance set. "
        "Clause seven point two is absent. "
        "Not contradicted — there is nothing to contradict. Unsupported. "
        "The verdict is a set-membership test, not an opinion about finished text. "
        "Show text is R1 — customer-visible. The HR internal note did bind, "
        "but the caller is vendor-public and the span is hr-confidential. "
        "Deterministic entitlement check — set membership on access control list subset of clearance. "
        "R1 times contradicted equals Edit. Surgical, never generative. "
        "Issue refund is R3 — irreversible. One lakh eighty-four thousand rupees. "
        "Driving claim is clause seven point two, still unproven, still categorical. "
        "R3 times unsupported categorical equals Escalate. "
        "Held and escalated with the evidence packet. Not an alert. "
        "The hash chain verifies. Text edited. Money held. Both correct at the same time. "
        "Zero L L M on Lane one. The interlock never redraws. "
        "Proof scales with consequence.",
        "Live gate — clause 7.2 is UNSUPPORTED",
        "Paste fresh into the gate. No fixtures. Claims extract with types — "
        "numeric, structural, textual, temporal, derived — and hedging. "
        "Amount recomputes under Indian digit grouping — "
        "one lakh eighty-four thousand equals one hundred eighty-four thousand I N R. "
        "Clause 7.2 is absent from the provenance set — unsupported, not contradicted. "
        "Show text at R1 becomes Edit — entitlement check, surgical, never generative. "
        "Issue refund at R3 becomes Escalate — held with the evidence packet. "
        "Text edited. Money held. Both correct at the same time. "
        "Zero LLM on Lane one. The interlock never redraws.",
    ),
    (
        "04_numbers",
        "Make eval. We publish false negative rate with a Wilson confidence interval on a self-authored corpus. "
        "Hard negatives included. Production traffic evidence we do not claim. "
        "Every team will claim detection. We publish what we miss.",
        "Publish what we miss",
        "Make eval produces false negative rate with a Wilson confidence interval "
        "on a self-authored corpus. Hard negatives included. "
        "Production traffic evidence we do not claim. "
        "Every team will claim detection. We publish what we miss.",
    ),
    (
        "05_close",
        "That system was never asked to prove anything. "
        "Now nothing acts until it can prove it should. "
        "Held and escalated with the evidence packet.",
        "Nothing acts until it can prove it should.",
        "That system was never asked to prove anything. "
        "Now nothing acts until it can prove it should. "
        "Held and escalated with the evidence packet. "
        "Zero LLM on Lane one.",
    ),
]

VOICE = "en-IN-NeerjaExpressiveNeural"
AUDIO_RATE = 22050  # sample rate for TTS output


def _tts_to_wav(text: str, out_wav: Path) -> float:
    """Run edge-tts, convert to wav, return duration in seconds."""
    # edge-tts writes mp3; convert to wav for ffmpeg concat
    mp3 = out_wav.with_suffix(".mp3")
    subprocess.check_call(
        ["edge-tts", "--voice", VOICE, "--text", text, "--write-media", str(mp3)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.check_call(
        ["ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", str(AUDIO_RATE), str(out_wav)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    mp3.unlink(missing_ok=True)
    # Get duration
    dur = float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(out_wav)],
            text=True,
        ).strip()
    )
    return dur


def _card_html(path: Path, title: str, body: str) -> None:
    path.write_text(
        f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<style>
html,body{{margin:0;height:100%;background:#0b1020;color:#e8edf7;
font-family:ui-monospace,Menlo,monospace}}
.wrap{{display:flex;flex-direction:column;justify-content:center;align-items:center;
height:100%;padding:80px;text-align:center}}
h1{{font-size:64px;margin:0 0 24px;letter-spacing:1px}}
p{{font-size:28px;color:#9aa7c2;max-width:1100px;line-height:1.45;margin:0}}
.tag{{margin-top:36px;color:#4ea1ff;font-size:20px;letter-spacing:2px;
text-transform:uppercase}}
</style></head><body><div class=wrap>
<h1>{title}</h1><p>{body}</p>
<div class=tag>ControlPlane.ai · prototype · held ≠ blocked</div>
</div></body></html>""",
        encoding="utf-8",
    )


def _card_html_live(path: Path, title: str, body: str) -> None:
    """Live gate card — matches the gate page styling."""
    path.write_text(
        f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<style>
html,body{{margin:0;height:100%;background:#0b1020;color:#e8edf7;
font-family:Menlo,monospace;padding:40px}}
pre{{background:#121a30;padding:24px;border-radius:12px;font-size:20px;
line-height:1.5;white-space:pre-wrap;word-break:break-all}}
h1{{color:#4ea1ff;margin:0 0 20px}}
p{{font-size:18px;color:#9aa7c2;max-width:1200px;line-height:1.5;margin:0 0 12px}}
.escalate{{color:#ff6b6b;font-size:28px;font-weight:800;margin:16px 0}}
.edit{{color:#ffb454;font-size:28px;font-weight:800;margin:16px 0}}
.tag{{margin-top:30px;color:#4ea1ff;font-size:18px;letter-spacing:2px;
text-transform:uppercase}}
</style></head><body>
<h1>{title}</h1>
<p>{body}</p>
<p class=escalate>issue_refund → Escalate (held with evidence packet)</p>
<p class=edit>show_text → Edit (entitlement / ACL)</p>
<div class=tag>ControlPlane.ai · prototype · held ≠ blocked</div>
</body></html>""",
        encoding="utf-8",
    )


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    audio_dir = WORK / "audio"
    audio_dir.mkdir(exist_ok=True)
    cards = WORK / "cards"
    cards.mkdir(exist_ok=True)

    # 1. Generate all TTS audio first (so we know exact durations)
    print("=== Generating TTS voiceover ===")
    durs = {}
    for name, text, _, _ in CHAPTERS:
        wav = audio_dir / f"{name}.wav"
        durs[name] = _tts_to_wav(text, wav)
        print(f"  VO {name}: {durs[name]:.2f}s (voice: {VOICE})")

    # 2. Build FNR numbers card
    fnr = "measured"
    ci = ""
    last = ROOT / "evals" / "last_run.json"
    if last.exists():
        data = json.loads(last.read_text())
        s = data.get("summary") or data
        uw = s.get("ungrounded_fnr_wilson")
        if uw and len(uw) >= 3:
            fnr = f"{uw[0]:.1%}"
            ci = f"{uw[1]:.1%}–{uw[2]:.1%}"
        else:
            fnr = s.get("published_fnr", "n/a")
            ci = s.get("published_fnr_wilson_95") or s.get("published_fnr_ci") or ""

    # 3. Write HTML cards
    print("=== Writing HTML cards ===")
    _card_html(cards / "01_failure.html",
              CHAPTERS[0][2], CHAPTERS[0][3])
    _card_html(cards / "02_reframe.html",
              CHAPTERS[1][2], CHAPTERS[1][3])
    _card_html_live(cards / "03_live.html",
                    CHAPTERS[2][2], CHAPTERS[2][3])
    _card_html(cards / "04_numbers.html",
              CHAPTERS[3][2], CHAPTERS[3][3])
    _card_html(cards / "05_close.html",
              CHAPTERS[4][2], CHAPTERS[4][3])

    # 4. Record video chapters with Playwright
    print("=== Recording video chapters ===")
    from playwright.sync_api import sync_playwright

    chapter_mp4s: list[Path] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        def capture_card(html_file: Path, seconds: float, out: Path) -> None:
            """Record a card page for the given duration."""
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
            # Preload the page before recording starts
            page.goto(html_file.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(500)  # let fonts/render settle
            ctx.close()
            # Re-open for actual recording
            ctx2 = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                record_video_dir=str(vdir),
                record_video_size={"width": 1920, "height": 1080},
            )
            page2 = ctx2.new_page()
            page2.goto(html_file.as_uri(), wait_until="networkidle")
            page2.wait_for_timeout(300)
            # Hold for the requested duration
            page2.wait_for_timeout(int((seconds + 1.0) * 1000))
            ctx2.close()
            webms = list(vdir.glob("*.webm"))
            if not webms:
                raise RuntimeError(f"no webm produced for {out}")
            # Transcode to mp4 with GOOD quality (not stripped audio — we add VO later)
            subprocess.check_call(
                ["ffmpeg", "-y", "-i", str(webms[0]),
                 "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                 "-pix_fmt", "yuv420p", "-an", str(out)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            webms[0].unlink(missing_ok=True)

        def capture_live_gate(seconds: float, out: Path) -> None:
            """Record the live gate page with scenario loaded."""
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
            page.goto(f"{BASE}/gate", wait_until="networkidle")
            page.wait_for_timeout(500)
            # Click scenario loader
            page.click("#loadScenario")
            page.wait_for_timeout(1000)
            # Click run
            page.click("#run")
            page.wait_for_timeout(5000)
            # Scroll to show full results
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, 0)")
            # Hold for remaining time
            hold_ms = max(3000, int(seconds * 1000) - 10000)
            if hold_ms > 0:
                page.wait_for_timeout(hold_ms)
            ctx.close()
            webms = list(vdir.glob("*.webm"))
            if not webms:
                raise RuntimeError(f"no webm for live gate {out}")
            subprocess.check_call(
                ["ffmpeg", "-y", "-i", str(webms[0]),
                 "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                 "-pix_fmt", "yuv420p", "-an", str(out)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            webms[0].unlink(missing_ok=True)

        # Record each chapter
        for i, (name, _, _, _) in enumerate(CHAPTERS):
            out = WORK / f"{name}.mp4"
            card_file = cards / f"{name}.html"
            if name == "03_mechanism":
                capture_live_gate(durs[name] + 8.0, out)
            else:
                capture_card(card_file, durs[name] + 1.5, out)
            chapter_mp4s.append(out)
            print(f"  Recorded {name}: {out.stat().st_size:,} bytes")

        browser.close()

    # 5. Concatenate video chapters
    print("=== Concatenating video ===")
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in chapter_mp4s), encoding="utf-8")
    silent = WORK / "video_silent.mp4"
    subprocess.check_call(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(silent)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # 6. Concatenate audio with 0.3s gaps between chapters
    print("=== Building audio track with gaps ===")
    parts = [audio_dir / f"{n}.wav" for n, _, _, _ in CHAPTERS]
    # Create short silence between chapters
    gap_sil = audio_dir / "gap.wav"
    subprocess.check_call(
        ["ffmpeg", "-y", "-f", "lavfi", "-i",
         f"anullsrc=r={AUDIO_RATE}:cl=mono", "-t", "0.3", str(gap_sil)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    alst = WORK / "audio_concat.txt"
    lines = []
    for i, p in enumerate(parts):
        lines.append(f"file '{p.resolve()}'\n")
        if i < len(parts) - 1:
            lines.append(f"file '{gap_sil.resolve()}'\n")
    alst.write_text("".join(lines), encoding="utf-8")
    vo_full = audio_dir / "vo_full.wav"
    subprocess.check_call(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(alst),
         "-c", "copy", str(vo_full)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # 7. Mux video + audio with loudnorm for professional loudness
    print("=== Muxing with loudnorm ===")
    vdur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(silent)], text=True).strip())
    adur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(vo_full)], text=True).strip())
    print(f"  Video: {vdur:.1f}s, Audio: {adur:.1f}s")

    # Pad video if shorter than audio (shouldn't happen, but safety)
    target = max(vdur, adur)
    if vdur < adur:
        pad_extra = adur - vdur
        padded = WORK / "video_padded.mp4"
        subprocess.check_call(
            ["ffmpeg", "-y", "-i", str(silent),
             "-vf", f"tpad=stop_mode=clone:stop_duration={pad_extra}",
             "-c:v", "libx264", "-crf", "18", "-preset", "medium",
             "-pix_fmt", "yuv420p", str(padded)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        vdur = adur
    else:
        padded = silent

    # Pad audio to match video
    apadded = WORK / "audio_padded.wav"
    subprocess.check_call(
        ["ffmpeg", "-y", "-i", str(vo_full),
         "-af", f"apad=whole_dur={vdur}",
         str(apadded)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Final mux with loudnorm (broadcast loudness: -16 LUFS for video)
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        ["ffmpeg", "-y",
         "-i", str(padded),
         "-i", str(apadded),
         "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-shortest",
         "-movflags", "+faststart",
         str(FINAL)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    final_dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(FINAL)], text=True).strip())
    print(f"=== DONE: {FINAL} ===")
    print(f"  Duration: {final_dur:.1f}s")
    print(f"  Size: {FINAL.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
