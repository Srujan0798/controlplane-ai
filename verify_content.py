"""Verification harness: open each poster HTML, assert required text + layout force."""
from playwright.sync_api import sync_playwright
from pathlib import Path

ROOT = Path("/Users/srujansai/Desktop/SEBI")
HTML = ROOT / "visuals" / "_html"

CHECKS = {
    "s1.html": {
        "must_contain": [
            "It used to be a bad paragraph",
            "An AI response is a set of claims requesting permission to act",
            "MODEL",
            "consumes spans",
            "Three dimensions, one graph",
            "The system didn",
            "clause 7.2",
            "1,84,000",
            "HELD",
            "Unentitled Span",
            "Unbound Claim",
            "Unused Step",
        ],
        "must_not_contain": ["caller may not read", "claim with no span", "blocked"],
    },
    "s2.html": {
        "must_contain": [
            "holds a payment",
            "Contradicted",
            "Unsupported + categorical",
            "BLOCK", "ESCALATE", "EDIT", "PASS",
            "R3", "R2", "R1", "R0",
            "clause 7.2",
            "1,84,000 held",
            "Hard gate on actions",
            "Text streams with a short hold-back",
            # Bias and Safety are two of the brief's three responsibility categories, and
            # this line is the deck's only coverage of them. Round 1 has no Q&A, so anything
            # off-slide is never scored. It was deleted once with no test to catch it.
            "counterfactual flip rate",
            "typed interlocks",
            "40 ms p50",
        ],
        "must_not_contain": ["blocks a payment", "STREAM", "Kill Span"],
    },
    "s3.html": {
        "must_contain": [
            "claims we refuse to make",
            "We eliminate hallucinations",
            "Zero added latency",
            "99% accuracy",
            "per-route gate report",
            "FNR",
            "illustrative format",
            "Now nothing acts until it can prove",
        ],
        "must_not_contain": ["rejected approaches", "first true AI control plane"],
    },
}


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        all_ok = True
        for name, spec in CHECKS.items():
            p = HTML / name
            page.goto(p.resolve().as_uri(), wait_until="load")
            page.wait_for_timeout(60)
            txt = page.inner_text("body")
            for s in spec["must_contain"]:
                ok = s.lower() in txt.lower()
                if not ok:
                    all_ok = False
                print(f"[{'OK ' if ok else 'FAIL'}] {name}: contains {s!r}")
            for s in spec.get("must_not_contain", []):
                bad = s in txt  # banned tokens are case-sensitive
                if bad:
                    all_ok = False
                print(f"[{'BAD ' if bad else 'OK '}] {name}: absent  {s!r}")
        browser.close()
    print("\nALL CONTENT CHECKS:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
