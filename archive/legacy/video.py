"""Voice + timed slideshow → 1080p submission video."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO = ROOT / "video" / "vo"
FRAMES = ROOT / "video" / "frames"
OUT = ROOT / "ControlPlane_ControlPlane-ai.mp4"
VOICE = "Reed (English (UK))"
CAP = 178.0  # hard length cap; tempo-fit audio, never rewrite VO

# Frozen beat map. Frames listed in order inside each beat.
BEATS = {
    1: ["1a", "1b", "1c"],
    2: ["2a", "2b1", "2b2", "2b3", "2b", "2c"],
    3: [
        "3a0", "3a1", "3a2", "3a3", "3a4", "3a5", "3a",
        "3b0", "3b", "3c1", "3c2", "3c3", "3c4", "3c",
        "3d", "3e", "3f", "3g",
    ],
    4: ["4a", "4b", "4c", "4d"],
    5: ["5a", "5b", "5c"],
}

# How to split a beat's duration across its frames (weights).
WEIGHTS = {
    1: [0.28, 0.28, 0.44],
    2: [0.22, 0.10, 0.10, 0.10, 0.18, 0.30],
    3: [
        0.04, 0.018, 0.018, 0.016, 0.016, 0.022, 0.030,
        0.055, 0.045, 0.045, 0.045, 0.045, 0.045, 0.100,
        0.11, 0.12, 0.13, 0.10,
    ],
    4: [0.24, 0.26, 0.24, 0.26],
    5: [0.38, 0.34, 0.28],
}


def run(cmd, **kw):
    subprocess.check_call(cmd, **kw)


def say_beat(n: int) -> Path:
    src = VO / f"beat{n}.txt"
    aiff = VO / f"beat{n}.aiff"
    wav = VO / f"beat{n}.wav"
    rate = 128 if n == 5 else 150
    run(["say", "-v", VOICE, "-r", str(rate), "-f", str(src), "-o", str(aiff)])
    run(
        [
            "ffmpeg", "-y", "-i", str(aiff),
            "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le",
            str(wav),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return wav


def duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nk=1:nw=1", str(path),
        ],
        text=True,
    )
    return float(out.strip())


def concat_audio(wavs: list[Path], dest: Path) -> float:
    lst = VO / "_concat.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in wavs))
    run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c:a", "pcm_s16le", str(dest),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return duration(dest)


def recut():
    """Assemble from current frames + existing full.wav. Does not re-speak."""
    wavs = [VO / f"beat{n}.wav" for n in range(1, 6)]
    full = VO / "full.wav"
    for w in [*wavs, full]:
        if not w.exists():
            raise SystemExit(f"missing {w}")
    durs = [duration(w) for w in wavs]
    total = duration(full)
    print("beat durs", [round(d, 2) for d in durs], "sum", round(sum(durs), 2))
    print("audio", round(total, 2))

    fit = min(1.0, CAP / total) if total > 0 else 1.0
    target = total * fit

    entries = []
    for n in range(1, 6):
        names = BEATS[n]
        weights = WEIGHTS[n]
        assert len(names) == len(weights)
        s = sum(weights)
        slice_d = [durs[n - 1] * w / s * fit for w in weights]
        for name, d in zip(names, slice_d):
            png = FRAMES / f"{name}.png"
            if not png.exists():
                raise SystemExit(f"missing frame {png}")
            entries.append((png, d))

    drift = target - sum(d for _, d in entries)
    entries[-1] = (entries[-1][0], entries[-1][1] + drift)

    lst = FRAMES / "list.txt"
    lines = []
    for png, d in entries:
        lines.append(f"file '{png.resolve()}'\n")
        lines.append(f"duration {d:.3f}\n")
    lines.append(f"file '{entries[-1][0].resolve()}'\n")
    lst.write_text("".join(lines))

    tmp = ROOT / "video" / "_video.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-i", str(full),
        "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p,fps=30",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        "-t", f"{CAP:.3f}",
    ]
    if fit < 1.0:
        cmd[cmd.index("-c:a"):cmd.index("-c:a")] = ["-af", f"atempo={1.0 / fit:.8f}"]
    cmd.append(str(tmp))
    run(cmd)

    cap = ROOT / "video" / "ControlPlane_ControlPlane-ai.mp4"
    run(["cp", str(tmp), str(cap)])
    run(["cp", str(tmp), str(OUT)])
    info = subprocess.check_output(
        ["ffprobe", "-hide_banner", str(OUT)], stderr=subprocess.STDOUT, text=True
    )
    print(info)
    print("wrote", OUT, OUT.stat().st_size)


def build():
    wavs = [say_beat(n) for n in range(1, 6)]
    concat_audio(wavs, VO / "full.wav")
    recut()


if __name__ == "__main__":
    recut()
