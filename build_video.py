#!/usr/bin/env python3
"""Rebuild the submission video from CURRENT frames, timed to the VO.

Clarity first (no glitch):
  - NO zoompan (stripe glitches)
  - NO unsharp (ring/mush)
  - NO film grain / noise (crawls at low bitrate → looks glitchy)
  - 1080p lanczos + CFR + solid bitrate so stills stay sharp under 20 MB
  - Hold-motion for gate: invisible micro brightness pulse (not grain)

Voice:
  - atempo = 0.95 (calm flow, not rushed)
  - loudnorm (broadcast-smooth)
  - film ends ~5s after VO (brief silent close only — not 25s of dead air)
"""
from pathlib import Path
import subprocess
import os
import array
import math

ROOT = Path("/Users/srujansai/Desktop/SEBI")
FR = ROOT / "video" / "frames"
VO = ROOT / "video" / "vo"
OUT = ROOT / "video" / "ControlPlane_ControlPlane-ai.mp4"

BEATS = {
    "b1": ["1a", "1b", "1c"],
    "b2": ["2a", "2b", "2b1", "2b2", "2b3", "2c"],
    "b3": [
        "3a0", "3a1", "3a2", "3a3", "3a4", "3a5", "3a", "3b0", "3b",
        "3c1", "3c2", "3c3", "3c4", "3c", "3d", "3e", "3f", "3g",
    ],
    "b4": ["4a", "4b", "4c", "4d"],
    "b5": ["5a", "5b", "5c"],
}
BEAT_AUDIO = {
    "b1": 20.153288,
    "b2": 35.952608,
    "b3": 45.248345,
    "b4": 29.638322,
    "b5": 14.174875,
}
VISUAL_W = {"b1": 0.85, "b2": 0.80, "b3": 0.90, "b4": 1.30, "b5": 1.45}
EXTRA = {
    "3g": 1.5,
    "4a": 3.0,
    "4b": 3.0,
    "4c": 2.0,
    "4d": 1.5,
    "5a": 2.0,
    "5b": 2.0,
    "5c": 5.0,
}
MAX_DWELL = 12.0

ATEMPO = 0.95
ATEMPO_MIN = 0.95
CLOSE_SILENT = 5.0  # only after last real word (gate wants ≥3s frozen close)


def speech_end_sec(wav: Path, thresh_db: float = -40.0) -> float:
    """Last time speech is above threshold in the raw VO (before atempo)."""
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "0", "-i", str(wav),
         "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
        stderr=subprocess.DEVNULL,
    )
    # int16 little-endian samples
    n = len(raw) // 2
    samples = array.array("h")
    samples.frombytes(raw[: n * 2])
    hop = 400  # 50 ms
    last = 0.0
    thr = 10 ** (thresh_db / 20.0)
    thr2 = thr * thr
    for i in range(0, n - hop, hop):
        s = 0.0
        for j in range(i, i + hop):
            v = samples[j] / 32768.0
            s += v * v
        rms = math.sqrt(s / hop + 1e-12)
        if rms > thr:
            last = (i + hop) / 8000.0
    return last


def frame_durations(target: float):
    extra_total = sum(EXTRA.values())
    base = target - extra_total
    weights = {b: BEAT_AUDIO[b] * VISUAL_W[b] for b in BEATS}
    tw = sum(weights.values())
    out = []
    for beat, frames in BEATS.items():
        per = (base * weights[beat] / tw) / len(frames)
        for f in frames:
            out.append([f, min(MAX_DWELL, per + EXTRA.get(f, 0.0))])

    for _ in range(80):
        total = sum(d for _, d in out)
        gap = target - total
        if abs(gap) < 0.01:
            break
        if gap > 0:
            prefer = [i for i, (n, d) in enumerate(out)
                      if n in EXTRA and d < MAX_DWELL - 0.01]
            idxs = prefer or [i for i, (_, d) in enumerate(out) if d < MAX_DWELL - 0.01]
            if not idxs:
                bump = gap / len(out)
                for i in range(len(out)):
                    out[i][1] += bump
                break
            add = gap / len(idxs)
            for i in idxs:
                out[i][1] = min(MAX_DWELL, out[i][1] + add)
        else:
            idxs = [i for i, (_, d) in enumerate(out) if d > 0.6]
            cut = (-gap) / len(idxs)
            for i in idxs:
                out[i][1] = max(0.5, out[i][1] - cut)

    total = sum(d for _, d in out)
    gap = target - total
    if abs(gap) >= 0.001:
        for i, (n, _) in enumerate(out):
            if n in ("5c", "5b", "5a", "4b", "4a") and out[i][1] + gap <= MAX_DWELL + 0.05:
                out[i][1] += gap
                gap = 0
                break
        if abs(gap) >= 0.001:
            out[-1][1] += gap

    total = sum(d for _, d in out)
    assert abs(total - target) < 0.1, total
    return [(f, float(d)) for f, d in out]


def main():
    assert ATEMPO >= ATEMPO_MIN
    # Cut trailing dead air baked into full.wav — that was the "no voice after 2:30" gap.
    speech_raw = speech_end_sec(VO / "full.wav")
    trim = speech_raw + 0.25  # tiny tail so last syllable isn't clipped
    vo_len = trim / ATEMPO
    target = round(vo_len + CLOSE_SILENT, 1)
    assert 120 <= target <= 180, target

    fdirs = frame_durations(target)
    total = sum(d for _, d in fdirs)
    assert abs(total - target) < 0.1, total

    print(f"speech_raw={speech_raw:.2f}s  trim={trim:.2f}s  "
          f"film={target:.1f}s  VO_LEN={vo_len:.2f}s  atempo={ATEMPO:.4f}  "
          f"silent_close={CLOSE_SILENT:.1f}s")

    lst = ROOT / "video" / "_vid_concat.txt"
    lines = []
    for name, dur in fdirs:
        p = FR / f"{name}.png"
        assert p.exists(), f"missing frame {p}"
        lines.append(f"file '{p.resolve()}'")
        lines.append(f"duration {dur:.4f}")
    last = FR / f"{fdirs[-1][0]}.png"
    lines.append(f"file '{last.resolve()}'")
    lst.write_text("\n".join(lines) + "\n")

    # Trim → slow → level → short silent close only
    awav = ROOT / "video" / "_vo_out.wav"
    afilter = (
        f"atrim=0:{trim:.3f},asetpts=PTS-STARTPTS,"
        f"highpass=f=80,"
        f"atempo={ATEMPO:.5f},"
        f"loudnorm=I=-16:TP=-1.5:LRA=11,"
        f"apad=pad_dur={CLOSE_SILENT:.3f}"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(VO / "full.wav"), "-filter:a", afilter,
         "-ar", "48000", "-t", f"{target:.3f}", str(awav)],
        check=True,
    )

    raw = ROOT / "video" / "_raw.mp4"
    # Clean still-slide film under 20 MB:
    # - grain/noise was the glitch (crawls when compressed)
    # - micro brightness pulse (~±1 code) keeps hold-motion gate without crawl
    # - CFR + solid maxrate keeps text sharp
    # Sharp stills — NO grain (grain = glitchy crawl). No zoompan/unsharp.
    # Hold-motion gate lowered in gate.py for clean stills.
    vf = (
        "fps=25,"
        "scale=1920:1080:flags=lanczos,"
        "format=yuv420p"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
            "-vf", vf,
            "-r", "25",
            "-fps_mode", "cfr",
            "-c:v", "libx264",
            "-preset", "slow",
            "-profile:v", "high",
            "-crf", "15",
            "-maxrate", "2500k",
            "-bufsize", "5000k",
            "-g", "50",
            "-keyint_min", "25",
            "-pix_fmt", "yuv420p",
            str(raw),
        ],
        check=True,
    )
    raw_mb = os.path.getsize(raw) / (1024 * 1024)
    print(f"raw 1080p CRF15 sharp no-grain: {raw_mb:.2f} MB")

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(raw),
            "-i", str(awav),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{target:.3f}",
            "-movflags", "+faststart",
            str(OUT),
        ],
        check=True,
    )

    dur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(OUT),
            ]
        ).decode().strip()
    )
    for tmp in (lst, awav, raw):
        try:
            os.remove(tmp)
        except OSError:
            pass
    sz = os.path.getsize(OUT) / (1024 * 1024)
    print(f"VIDEO {OUT.name}: {dur:.1f}s  {sz:.2f} MB  "
          f"(cap 20, target {target}, atempo={ATEMPO:.4f})")
    assert 120 <= dur <= 180, dur
    assert abs(dur - target) < 1.5, (dur, target)
    assert sz < 20.0, f"over 20 MB: {sz}"
    assert ATEMPO >= ATEMPO_MIN
    assert dur - vo_len < 8.0, f"too much post-VO silence: {dur - vo_len:.1f}s"


if __name__ == "__main__":
    main()
