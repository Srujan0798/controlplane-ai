"""Emit HTML, screenshot with Playwright, rebuild deck and video."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTERS = ROOT / "posters"
FRAMES = ROOT / "video" / "frames"
HTML_OUT = ROOT / "visuals" / "_html"


def emit():
    from .pages import poster_s1, poster_s2, poster_s3, poster_video, video_frames

    HTML_OUT.mkdir(parents=True, exist_ok=True)
    POSTERS.mkdir(exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)

    posters = {
        "s1": poster_s1(),
        "s2": poster_s2(),
        "s3": poster_s3(),
        "sv": poster_video(),
    }
    for name, html in posters.items():
        (HTML_OUT / f"{name}.html").write_text(html)

    for name, html in video_frames().items():
        (HTML_OUT / f"{name}.html").write_text(html)
    print(f"emitted {len(posters)} posters + {len(video_frames())} frames")


def screenshot():
    from playwright.sync_api import sync_playwright

    jobs = []
    for name in ("s1", "s2", "s3", "sv"):
        jobs.append((HTML_OUT / f"{name}.html", POSTERS / f"{name}.png", 2))
    for p in sorted(HTML_OUT.glob("[0-9]*.html")):
        jobs.append((p, FRAMES / f"{p.stem}.png", 1))

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
        )
        # posters at 2x
        for html, png, scale in jobs:
            if scale != page.viewport_size:
                pass
            if scale == 2:
                if page.evaluate("window.devicePixelRatio") != 2:
                    page.close()
                    page = browser.new_page(
                        viewport={"width": 1920, "height": 1080},
                        device_scale_factor=2,
                    )
            else:
                page.close()
                page = browser.new_page(
                    viewport={"width": 1920, "height": 1080},
                    device_scale_factor=1,
                )
            page.goto(html.resolve().as_uri(), wait_until="load")
            page.wait_for_timeout(80)
            page.screenshot(path=str(png), type="png")
            print("shot", png.relative_to(ROOT))
        browser.close()


def screenshot_grouped():
    """One browser, two pages (2x then 1x) to avoid reopen thrash."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        # 3× retina: sharp for 16:9 judges; 8× was 15360px bloat with no display gain.
        hi = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=3)
        for name in ("s1", "s2", "s3", "sv"):
            html = HTML_OUT / f"{name}.html"
            png = POSTERS / f"{name}.png"
            hi.goto(html.resolve().as_uri(), wait_until="load")
            hi.wait_for_timeout(60)
            hi.screenshot(path=str(png), type="png")
            print("shot", png.relative_to(ROOT), png.stat().st_size)
        hi.close()

        lo = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
        for html in sorted(HTML_OUT.glob("[0-9]*.html")):
            png = FRAMES / f"{html.stem}.png"
            lo.goto(html.resolve().as_uri(), wait_until="load")
            lo.wait_for_timeout(40)
            lo.screenshot(path=str(png), type="png")
            print("shot", png.relative_to(ROOT))
        lo.close()
        browser.close()


def main():
    emit()
    screenshot_grouped()


if __name__ == "__main__":
    main()
