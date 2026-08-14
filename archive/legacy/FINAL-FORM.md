# ControlPlane.ai — FINAL FORM LAW (locked)

**Portal (Round 1) is the only authority for what you upload.**

| Upload | Spec | Cap |
|--------|------|-----|
| **PPTX** | **Exactly 2–3 solution slides** | ≤ **20 MB** |
| **PDF** | **Same 2–3 slides** | ≤ **20 MB** |
| **Video** | **2–3 minutes** MP4/MOV | ≤ **20 MB** |

Three separate caps → **60 MB total capacity**.  
Do **not** starve quality at 0.3 MB. Target **sharp** posters (2–3× retina) while staying under each cap.

## What is NOT the form upload

- Official AIC 7-slide wrapper (Cover · Team · 3 · Video · Thank You) is **optional / archive only**.
- Do not submit 7 slides if the portal asks for 2–3.

## Slide order (content only)

1. **S1 Graph** — STEP → SPAN → CLAIM → ACTION (the argument)
2. **S2 Matrix** — frozen decision surface + full quiet strip
3. **S3 Refuse + FNR + closer** — credibility

## Product sentence (every pixel serves this)

> An AI response is a set of claims requesting permission to act.  
> If a claim has no span, the action does not execute.  
> We hold, escalate, and publish what we miss.

## Frozen docs (never rewrite)

`archive/docs/FINAL-ARCHITECTURE.md` · `STAGE3` · `STAGE4` · `STAGE5` · `ELEVATION` · `SUBMISSION-PACKAGE`

## Build

```bash
python3 -m visuals.render          # emit + screenshot posters
python3 build_submission.py        # → submission/ControlPlane_ControlPlane-ai.{pptx,pdf}
# video: submission/ControlPlane_ControlPlane-ai.mp4 (copy from video/)
```

## Upload paths (only these)

```
submission/ControlPlane_ControlPlane-ai.pptx
submission/ControlPlane_ControlPlane-ai.pdf
submission/ControlPlane_ControlPlane-ai.mp4
```

## Hierarchy

```
SEBI/
  FINAL-FORM.md          ← this file
  LOOP-GUIDE.md
  build_submission.py    ← form builder ONLY
  visuals/               ← poster + graph source
  posters/               ← rendered s1/s2/s3 (and video helpers)
  submission/            ← **UPLOAD THIS FOLDER**
  video/                 ← frames, VO, encode
  archive/               ← frozen docs, template, optional 7-slide tools
```

## Greps before ship

```bash
grep -c "for i in range(6)" visuals/graph.py   # 0
grep -c "vendor id" visuals/graph.py           # 1
# refund language: held/escalate, never "blocked" for the money
```
