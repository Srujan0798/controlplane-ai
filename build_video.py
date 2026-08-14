#!/usr/bin/env python3
"""Rebuild the submission video from the CURRENT graph frames, timed to the VO."""
from pathlib import Path
import subprocess

ROOT = Path("/Users/srujansai/Desktop/SEBI")
FR = ROOT / "video" / "frames"
VO = ROOT / "video" / "vo"
OUT = ROOT / "video" / "ControlPlane_ControlPlane-ai.mp4"
TARGET = 178.0  # seconds (<= 180 portal cap, 2-3 min)

# Frame order grouped by beat (matches the 5 VO beats).
BEATS = {
    "b1": ["1a", "1b", "1c"],
    "b2": ["2a", "2b", "2b1", "2b2", "2b3", "2c"],
    "b3": ["3a0", "3a1", "3a2", "3a3", "3a4", "3a5", "3a", "3b0", "3b",
           "3c1", "3c2", "3c3", "3c4", "3c", "3d", "3e", "3f", "3g"],
    "b4": ["4a", "4b", "4c", "4d"],
    "b5": ["5a", "5b", "5c"],
}
# Audio duration per beat (seconds) — measured from vo/beat*.wav.
BEAT_AUDIO = {"b1": 29.518688, "b2": 51.822542, "b3": 61.837104,
              "b4": 39.911792, "b5": 9.694667}
TOTAL_AUDIO = sum(BEAT_AUDIO.values())  # 192.784792

# Give the resolution frames a little extra dwell.
EXTRA = {"3g": 1.5, "4d": 1.0, "5b": 1.2, "5c": 0.8, "3c": 1.0, "1c": 0.8}


def frame_durations():
    """Allocate TARGET seconds across frames, proportional to beat audio,
    with small bonuses for key resolution frames."""
    out = []
    extra_total = sum(EXTRA.values())
    # base target after removing bonuses
    base = TARGET - extra_total
    for beat, frames in BEATS.items():
        beat_share = base * (BEAT_AUDIO[beat] / TOTAL_AUDIO)
        per = beat_share / len(frames)
        for f in frames:
            d = per + EXTRA.get(f, 0.0)
            out.append((f, d))
    return out


def main():
    fdirs = frame_durations()
    assert abs(sum(d for _, d in fdirs) - TARGET) < 0.5, sum(d for _, d in fdirs)
    # write concat list
    lst = ROOT / "video" / "_vid_concat.txt"
    lines = []
    for name, dur in fdirs:
        p = FR / f"{name}.png"
        assert p.exists(), f"missing frame {p}"
        lines.append(f"file '{p.resolve()}'")
        lines.append(f"duration {dur:.4f}")
    lst.write_text("\n".join(lines) + "\n")

    # speed audio to TARGET
    awav = ROOT / "video" / "_vo_178.wav"
    atempo = TOTAL_AUDIO / TARGET
    subprocess.run([
        "ffmpeg", "-y", "-i", str(VO / "full.wav"),
        "-filter:a", f"atempo={atempo:.5f}", str(awav),
    ], check=True)

    raw = ROOT / "video" / "_raw.mp4"
    # 4K-native frames (rendered at dpr=2) + a whisper of film grain so x264 has
    # real detail to encode (near-static frames otherwise compress to ~4 MB).
    # This uses the 20 MB budget without softening the type.
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-fps_mode", "vfr", "-pix_fmt", "yuv420p",
        # 1.000 -> 1.035 push across the runtime so nothing reads as a frozen still.
        # fps=25 must come first: zoompan maps 1:1 per input frame, and the concat
        # demuxer only emits one frame per still, so without it the whole video
        # collapses to 34 frames.
        "-vf", ("fps=25,scale=4224:2376,"
                f"zoompan=z='min(1.0+0.035*on/{int(TARGET*25)},1.035)':"
                "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                "d=1:s=3840x2160:fps=25,"
                "noise=alls=5:allf=t"),
        "-c:v", "libx264", "-preset", "medium",
        "-b:v", "1500k", "-maxrate", "2000k", "-bufsize", "4000k",
        str(raw),
    ], check=True)

    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw), "-i", str(awav),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(OUT),
    ], check=True)

    # report
    import os
    dur = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(OUT),
    ]).decode().strip()
    for _tmp in (lst, awav, raw):
        try:
            os.remove(_tmp)
        except OSError:
            pass
    sz = os.path.getsize(OUT) / 1e6
    print(f"VIDEO {OUT.name}: {float(dur):.1f}s  {sz:.2f} MB  (cap 20, 180s)")


if __name__ == "__main__":
    main()
