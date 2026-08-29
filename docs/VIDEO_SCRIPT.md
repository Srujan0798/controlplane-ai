# Prototype Video Script — ControlPlane.ai (T7.5)

1920x1080, screen capture + voiceover, target 3:30–4:00. Prototype, not pitch.
System running only — no narrated slides. Large terminal font. Nothing personal in
frame, no notifications, no home paths.

NEVER say "blocked" about the refund. Say "held and escalated with the evidence packet."

## Beats

**0:00–0:20 — THE FAILURE**
On screen: the ungated response.
Voiceover:
"Approved. Refund of one lakh eighty-four thousand rupees issued under clause
seven point two. Confidence zero point nine four. Money moved Tuesday, found
Friday. Clause seven point two does not exist."

**0:20–0:40 — THE REFRAME**
On screen: STEP → SPAN → CLAIM → ACTION.
Voiceover:
"Step, span, claim, action. Not text to be scored — claims requesting
permission to act."

**0:40–2:00 — MECHANISM LIVE**
On screen: run `examples/refund_trace_demo.py` live.
Voiceover:
"Paste fresh. Six claims extract themselves. The symbol table prints four point
one, four point three, nine point one — no seven point two. The amount
recomputes. The HR span ACL excludes the caller. Two pending actions: show text,
R1, becomes Edit; issue refund, R3, becomes Escalate, held. Zero LLM."

**2:00–2:30 — THE FLIP**
On screen: same span, same claim, same graph; change only the caller (grant
hr-confidential clearance) → show_text Edit → Pass.
Voiceover:
"Same span, same claim, same graph — change only the caller. Edit becomes Pass."

**2:30–3:10 — THE NUMBERS**
On screen: `make eval` summary — FNR 0.0% with its 95% interval, dead compute
~0.47ms.
Voiceover:
"Make eval. False-negative rate, with its interval. Dead compute. Every team will
claim detection. We publish what we miss."

**3:10–3:30 — CLOSE**
On screen: closing line on black.
Voiceover:
"That system was never asked to prove anything. Now nothing acts until it can
prove it should."

## Recording notes
- Captured region: 1920x1080, Terminal at 24pt Menlo.
- Voiceover recorded separately, muxed in post (ffmpeg).
- Output: `submission/ControlPlane_Round2_Prototype.mp4` (silent capture; mux voiceover from this script in post).

Regenerate: start server on :8787 then `python3 scripts/record_prototype_video.py`.
