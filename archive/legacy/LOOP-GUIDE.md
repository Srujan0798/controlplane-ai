# ControlPlane — builder guide (form-locked)

Read **FINAL-FORM.md** first. Portal is law.

## Form (only what judges upload)

- **PPTX:** 2–3 slides, ≤20 MB  
- **PDF:** same 2–3 slides, ≤20 MB  
- **Video:** 2–3 min, ≤20 MB  

Not 7 slides. Cover/Team/Thank You are **not** the form package.

## Build order

1. Edit `visuals/graph.py` / `visuals/pages.py`  
2. `python3 -m visuals.render`  
3. `python3 build_submission.py`  
4. Upload from `submission/`

## Greps

```bash
grep -c "for i in range(6)" visuals/graph.py   # → 0
grep -c "vendor id" visuals/graph.py           # → 1
```

ACTION = one full-height plate. Escalate/hold, never “blocked” for the refund.

## Quality

Use the **20 MB budget**. Full-bleed 2× posters. Do not crush to 0.3 MB.

## Frozen

Never rewrite `archive/docs/*`.
