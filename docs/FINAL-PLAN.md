# Final plan — submit & present

**Repo tip:** current `main` · **Tag:** `v0.2.0-round2`  
**Status after PDF rebuild:** Proposal PDF is regenerated from `round2/CONTROLPLANE_R2_FINAL.md`.

---

## A. Submission pack (check these files)

| File | Role | Status |
|---|---|---|
| `submission/ControlPlane_Round2_Proposal.pdf` | **Upload** — business proposal | Regenerated from FINAL (15 pages). Stage Check + 10 invariants = PASS. Uses “held/never blocked”. INR amounts render correctly. |
| `submission/ControlPlane_Round2_Pitch.pptx` | **Upload** — pitch deck (13 slides) | OK: admission-control, matrix, 7.2, Escalate/Edit, no “blocked”, no “40ms p95”. |
| `submission/latency_bench.json` | Evidence (optional attach) | gate p50≈0.073 ms · p95≈0.09 ms |
| `submission/sbom-pip-freeze.txt` | Supply-chain freeze | Present |
| Live repo demo | Working prototype | `make run` / Docker |

Canon MDs (do **not** upload unless asked): `CONTROLPLANE_R2_FINAL.md`, `R2S5.md`.

---

## B. What you do tomorrow (order)

1. **Preflight** — `bash scripts/preflight-lite.sh` (must PASS).  
2. **Demo once** — autorun refund; confirm Edit + Escalate; flip Edit→Pass.  
3. **Upload** to Accenture portal: Proposal PDF + Pitch PPTX (+ any form fields they ask).  
4. **Present** with one flow: speak `R2S5` → click Clearance → defend `HOSTILE_QA_DRILL`.  
5. **Do not** invent FNR %, logos, or quote 40ms as p95.

---

## C. Optional polish (only if time)

| Item | Why | Command / note |
|---|---|---|
| Rebuild pitch from JS | Keep PPTX synced with `ControlPlane_Round2_Pitch.js` | Only if you changed pitch copy |
| Cosmetic PDF arrows | `STEP → SPAN` still shows ■ for some unicode arrows | Content is correct; optional font fix later |
| Push remote | If you have GitHub | `git push origin main && git push origin v0.2.0-round2` |

---

## D. Architecture (one slide worth)

```text
STEP → SPAN → CLAIM → ACTION
outside-model provenance · entitlement ACL · frozen MATRIX · dual Edit+Escalate
```

Full: `docs/ARCHITECTURE.md`.
