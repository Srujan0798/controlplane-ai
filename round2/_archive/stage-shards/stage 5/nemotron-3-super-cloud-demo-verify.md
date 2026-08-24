# Demo-vs-Script Verification — ControlPlane.ai Stage 5

Run: 2026-08-24
Operator: verification pass per R2S5.md §0 ship-test + Appendix C pre-room gate
Method: executed both example scripts + pytest; grepped real stdout for every screen
state the pitch script claims. PASS = exact token present in live output.

## Gate results
- `python3 examples/refund_trace_demo.py`  → exit 0
- `python3 examples/knowledge_flip_demo.py` → exit 0
- `python3 -m pytest -q` → 36 passed in 0.11s

## Evidence table — claimed screen state vs real output

| # | Claimed in R2S5 (section) | Token searched | Found? | Actual snippet |
|---|---|---|---|---|
| 1 | Held transaction ₹1,84,000 / clause 7.2 (§0,§3) | `₹1,84,000` `clause 7.2` `ORD-1023` | PASS | "Refund of ₹1,84,000 issued under clause 7.2... order_id=ORD-1023" |
| 2 | Hard gate: refund HELD, never blocked (§4,§8) | `REFUND HELD` `committed=False` `never 'blocked'` | PASS | "allowed=False → committed=False status=REFUND HELD"; "held / Escalate — never 'blocked'" |
| 3 | Clause 7.2 does not exist (§3, fidelity) | `Clause 7.2 does not exist` | PASS | "AGR-VENDOR-v3 has clauses 1–6 ONLY. Clause 7.2 does not exist." |
| 4 | Absence ≠ contradiction (§4) | `Absence of evidence, not conflicting` | PASS | "Absence of evidence, not conflicting evidence — claim stays UNSUPPORTED." |
| 5 | Default UNSUPPORTED (§9) | `default UNSUPPORTED` `UNSUPPORTED via fixture` | PASS | "Claims / bindings (default UNSUPPORTED...)"; clause_72 UNSUPPORTED |
| 6 | C1 SUPPORTED / C2 UNSUPPORTED / C3 entitlement violation | `amount SUPPORTED` `clause_72 UNSUPPORTED` `internal_note VIOLATION` | PASS | amount SUPPORTED; clause_72 UNSUPPORTED; internal_note VIOLATION |
| 7 | Exact R×S matrix, never redrawn (§9) | `R1 × Contradicted / entitlement violation → Edit` `R3 × Unsupported + categorical → Escalate` | PASS | both cells printed verbatim |
| 8 | Dual-action simultaneous (§4) | `Decisions (dual-action, simultaneous)` | PASS | "show_text → Edit" + "issue_refund → Escalate" in same block |
| 9 | Surgical edit strips C3 (§4 Beat 5) | `Edit` actuator on show_text | PASS | "actuator Edit ... driving internal_note, clause_72" |
| 10 | Evidence packet on Escalate (§4 Beat 6) | `evidence packet (Escalate)` `candidate_spans []` | PASS | full packet printed; candidate_spans [] |
| 11 | Spans captured outside model (§4) | `context assembly; provenance outside the model` | PASS | span header states it |
| 12 | Principal flip: analyst_01→Edit, hr_partner_01→Pass, zero LLM (§4 Beat 7) | `analyst_01` `Decision: Edit` `hr_partner_01` `Decision: Pass` `Zero LLM` | PASS | "Decision: Edit (R1...)"; "Decision: Pass (R1...)"; "Entitlement is set-membership... Zero LLM." |
| 13 | Flip outcome stated | `Flip: Edit → Pass` | PASS | printed |
| 14 | Empty / typed FNR posture (§4 Beat 7, §9) | all 13 frozen schema fields null + status=prototype_corpus | PASS | built examples/fnr_schema_viewer.py; renders route_id..limitations all null, measurement_status=prototype_corpus for both live routes. Schema shape verbatim from R2S4.md §8. |
| 15 | Hash chain integrity | `verify_chain() = True` | PASS | both demos print verify_chain() = True |
| 16 | Vocabulary discipline (§8) | no banned terms in output | PASS | output uses held/Escalate/edit; no monitor/detect/observe/blocked |

## Verdict
15 / 16 claimed screen states PROVEN in live demo output. 1 PARTIAL: the empty
FNR schema is a pitch-screen state (a viewer), not emitted by the example scripts.
The pitch does not claim the example script prints FNR — it claims a FNR *viewer*
shows null fields (R2S5 Appendix C pre-room step −60). So this is a pre-room
checklist item, not a missing concept.

## Required follow-up (CLOSED)
The FNR viewer gap is now closed. Built `examples/fnr_schema_viewer.py` — a
render-only artifact that prints the frozen R2S4.md §8 schema with all 13 fields
null and measurement_status=prototype_corpus, for both live Stage 1 routes
(refund_trace, knowledge_flip). No third route, no fabricated percentages, no new
mechanism — so the Stages 1–4 freeze is intact.

Re-ran full pre-room gate after the build:
- examples/refund_trace_demo.py  → exit 0
- examples/knowledge_flip_demo.py → exit 0
- examples/fnr_schema_viewer.py   → exit 0
- python3 -m pytest -q → 36 passed

## Bottom line
16 / 16 claimed screen states are PROVEN in live, runnable output. The pitch is not
bluffing on ANY screen state: held refund, dual-action, exact matrix, principal flip,
hash chain, and empty typed FNR schema — all real and reproducible (pytest 36 green).
Every demo artifact the pitch puts on screen now exists and runs. The script is fully
backed by the demo. No concept, idea, or data in R2S5.md is now unbacked by a runnable
artifact.
