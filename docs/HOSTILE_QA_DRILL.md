# Hostile Q&A drill sheet — room defense

ControlPlane.ai · Accenture Innovation Challenge Round 2 · Team ControlPlane

One-sentence answers you can say under pressure. Each item has a live proof (when the console is up) and a deeper pointer. Drill the top five cold before the room.

**Ports:** Docker Compose → `http://localhost:8080` · local uvicorn → `http://127.0.0.1:8787`  
Swap the host/port in any curl below. Health: `GET /healthz`.

**Never say:** "blocked the refund," "p95 = 40 ms," a fabricated FNR %, or that clause 7.2 "caps/denies."  
**Say:** held / escalated with the evidence packet · ≤40 ms **p50** / ≤200 ms **p95** (targets) · measured numbers from `submission/latency_bench.json` or live `/v1/controlplane/metrics` · clause 7.2 **does not exist**.

Full essay-form answers: [reference/QA.md](reference/QA.md). Architecture freezes: [ARCHITECTURE.md](ARCHITECTURE.md). Stand script: [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md).

---

## Q1 — "Isn't this just a guardrail?"

**Answer:** Guardrails inspect output strings at the perimeter; we check claim→span membership and caller entitlement on the evidence assembled *before* an irreversible action fires.

**Live proof:** Console → run **refund · enforce** and point at Edit+Escalate from the ledger (not a deny-list hit). Or:

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' | python3 -m json.tool
# Expect: show_text → Edit, issue_refund → Escalate; clause 7.2 UNSUPPORTED (absent)
```

**Pointer:** [QA.md](reference/QA.md) A1 · [ARCHITECTURE.md](ARCHITECTURE.md) §2, §8 · pitch Slide 8.

---

## Q2 — "Why no LLM judge on the critical path?"

**Answer:** An LLM judge asks "does this look right?" (unfalsifiable, correlated blind spots); we ask "which span proves it?" with a pure rule engine and zero LLM reasoning at decision time.

**Live proof:** Flip demo is identity-only — no model call — same claim, same `content_hash`, actuator flips with principal:

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01'   # → Edit
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=hr_partner_01' # → Pass
```

**Pointer:** [QA.md](reference/QA.md) A1/A3 · [ARCHITECTURE.md](ARCHITECTURE.md) §4 (rule engine), §8 (rejected LLM-as-judge / Interrogator).

---

## Q3 — "What if clause 7.2 existed?"

**Answer:** Then the claim could earn SUPPORTED against a real span and the R3 cell would change; in *this* fixture clause 7.2 **does not exist**, so absence → UNSUPPORTED → Escalate, not Block.

**Live proof:** Refund enforce — driving claim stays red for missing clause; never invent a cap/deny story.

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response_overlay',{}).get('actuators_applied', d))"
```

**Pointer:** [ARCHITECTURE.md](ARCHITECTURE.md) §9, §10.1 · [QA.md](reference/QA.md) Team alignment (running example).

---

## Q4 — "What about latency?"

**Answer:** Hard gate sits on actions, not tokens; targets are ≤40 ms **p50** and ≤200 ms **p95** on R0/R1 — quote measured bench, never "40 ms p95."

**Live proof:** Cite checked-in bench or live metrics:

```bash
python3 -c "import json; print(json.load(open('submission/latency_bench.json'))['gate_latency_ms'])"
# n=10000: p50≈0.43 ms, p95≈0.51 ms

curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
# Optional refresh: make bench
```

**Pointer:** [QA.md](reference/QA.md) C1 · [ARCHITECTURE.md](ARCHITECTURE.md) §5 · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) Never-say table.

---

## Q5 — "What about false negatives?"

**Answer:** We do not claim zero misses — we publish FNR shape via stratified shadow audit (holds/escalations + random passes → expensive ground truth) per route with intervals; Round 2 shows the *format*, not a fabricated %.

**Live proof:** Console shadow counters / metrics after dual-emit runs — no invented catch rate on slides.

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=shadow'
curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
```

**Pointer:** [QA.md](reference/QA.md) D1 · [ARCHITECTURE.md](ARCHITECTURE.md) §7 (publish error bars).

---

## Q6 — "Where does bias fit?"

**Answer:** Bias is route-level counterfactual invariance (async), not a per-response score — perturb protected attributes, measure decision flip rate CI; flag when the interval excludes zero.

**Live proof:** No live bias verdict button by design; point at architecture + tests, not a moral classifier.

```bash
# Deterministic suite includes bias measurement tests (not a per-request actuator)
python -m pytest tests/test_bias.py -q
```

**Pointer:** [QA.md](reference/QA.md) D4 · [ARCHITECTURE.md](ARCHITECTURE.md) §3 Responsibility · §10.9 (do not drop bias).

---

## Q7 — "How do you fail closed?"

**Answer:** Fail stance is per blast-radius tier — R0/R1 fail open with annotation; R2/R3 fail closed or escalate — so load cannot bypass dangerous actions the way a universal fail-open would.

**Live proof:** Point at refund enforce (R3 hold) vs text path; regressions lock the holes:

```bash
python -m pytest tests/test_fail_closed.py -q
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' \
  | python3 -c "import sys,json; o=json.load(sys.stdin)['response_overlay']; print('action_allowed=', o.get('action_allowed'), 'shadow=', o.get('shadow'))"
```

**Pointer:** [QA.md](reference/QA.md) C4 · [ARCHITECTURE.md](ARCHITECTURE.md) §4 (fail stance ≠ matrix action).

---

## Q8 — Entitlement flip — "Isn't this just the text of the answer?"

**Answer:** Entitlement is identity × ACL on the span, not string matching — same span, same claim, same hash; only the caller changes the actuator.

**Live proof:** Console flip control, or:

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01'   # → Edit
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=hr_partner_01' # → Pass
```

**Pointer:** [QA.md](reference/QA.md) A3, B4 · [ARCHITECTURE.md](ARCHITECTURE.md) §3 leakage · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) step 5b.

---

## Q9 — Dual-action Edit + Escalate — "Why two actuators on one response?"

**Answer:** One response can carry two pending actions priced separately — R1 show_text → Edit (unentitled span); R3 issue_refund → Escalate (unsupported categorical) — proof scales with consequence.

**Live proof:**

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['response_overlay']['actuators_applied'])"
# Expect both Edit and Escalate simultaneously
```

Console: open refund enforce → matrix cells for both pending actions.

**Pointer:** [ARCHITECTURE.md](ARCHITECTURE.md) §9 (two pending actions) · [QA.md](reference/QA.md) Readiness bar · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) step 3.

---

## Q10 — "Blocked" language trap — "So you blocked the money?"

**Answer:** No — R3 × unsupported-categorical is **Escalate**: the refund is **held and escalated with the evidence packet**, not blocked as if contradicted policy text.

**Live proof:** Say it while the HOLD overlay is on screen; download the packet:

```bash
RID=$(curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=enforce' | python3 -c "import sys,json; print(json.load(sys.stdin)['request_id'])")
curl -s "http://127.0.0.1:8787/v1/controlplane/requests/${RID}/audit.jsonl" | head
```

**Pointer:** [ARCHITECTURE.md](ARCHITECTURE.md) §10.2 · [QA.md](reference/QA.md) Team alignment · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) Never-say.

---

## Q11 — OpenAI-compatible gate — "How do we integrate?"

**Answer:** Drop-in OpenAI-shaped reverse proxy plus a thin context-assembly hook — no weights, logits, or app rewrite; demo path returns a completion plus a `controlplane` extension object.

**Live proof:**

```bash
curl -s http://127.0.0.1:8787/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"controlplane-demo","messages":[{"role":"user","content":"Issue refund under clause 7.2"}],"scenario":"refund","mode":"enforce"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'][:200]); print('keys', sorted(d.get('controlplane',{}).keys())[:8])"
# Expect HOLD overlay text + controlplane extension (not bare upstream chat)
```

**Pointer:** [ARCHITECTURE.md](ARCHITECTURE.md) §5.10 · [QA.md](reference/QA.md) C2 · [JUDGE_RUNBOOK.md](JUDGE_RUNBOOK.md) step 6.

---

## Q12 — Shadow mode — "Won't teams just turn you off?"

**Answer:** Shadow is the default deployment — dual-emit gated-vs-ungated counterfactuals and earn enforcement per route so we do not over-block text and get disabled like a perimeter guardrail.

**Live proof:**

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/refund?mode=shadow' \
  | python3 -c "import sys,json; o=json.load(sys.stdin)['response_overlay']; print('shadow=', o.get('shadow'), 'action_allowed=', o.get('action_allowed'))"
# shadow=true → action_allowed stays true while would-hold counters still record
curl -s 'http://127.0.0.1:8787/v1/controlplane/metrics' | python3 -m json.tool
```

**Pointer:** [QA.md](reference/QA.md) C3, C5 · [ARCHITECTURE.md](ARCHITECTURE.md) §5.9.

---

## Q13 — "What about a purely parametric answer with nothing to bind to?"

**Answer:** Binding is undefined without an evidence set — ungrounded-by-construction still cannot authorise an R3 action; we do not pretend the graph verifies what was never given.

**Live proof:** Conceptual — no "fake span" demo; say the winning line out loud while refund shows absence ≠ parametric invention.

> "We don't claim to verify what we were never given. We claim that what we were never given cannot authorise an action."

**Pointer:** [QA.md](reference/QA.md) B1 (drill cold) · [ARCHITECTURE.md](ARCHITECTURE.md) §3 Detection §3 / ungrounded routes.

---

## Q14 — "Prompt injection — can the model forge a binding?"

**Answer:** The model has no channel to declare a binding — we compute bindings over spans captured at context assembly; injection can change prose, not which spans/ACLs/hashes were recorded.

**Live proof:** Entitlement flip again (identity outside the prompt) + audit hash chain:

```bash
curl -s -X POST 'http://127.0.0.1:8787/v1/controlplane/demo/flip?principal=analyst_01' | python3 -m json.tool | head -40
```

**Pointer:** [QA.md](reference/QA.md) B5 · [ARCHITECTURE.md](ARCHITECTURE.md) §8 (model-emitted citations rejected).

---

## Q15 — Hostile one-pager (the three traps they will spring)

### "Your corpus is self-authored — so your numbers are meaningless."
**Answer:** Correct that it is self-authored; wrong that it is meaningless. A self-authored
corpus measures *whether the frozen matrix and binder behave as specified*, not field
performance. We publish that distinction explicitly in `evals/README.md`. Every rate is
labelled "measured on this corpus only." Production FNR is unknown until shadow replay over
real traffic — and we say so out loud. We are not claiming a field accuracy number; we are
showing the mechanism and its honest miss on a case we wrote.

**Live proof:** `evals/README.md` "Honesty / limitations" — self-authored, Wilson how-to-read, production FNR unknown.

### "Your Wilson CI is wide — that's not a real result."
**Answer:** A wide interval is the honest result. Ungrounded FNR on this corpus is 1 miss in 94
should-hold cases: **1.1% (95% CI 0.2%–5.8%)**. The number we defend is the **5.8% upper bound**,
not a dressed-up zero. The width tells the judge exactly how much we do *not* know. A narrow CI
fabricated from a tiny sample would be the lie. We also publish the passable-action FPR upper
bound at ~15.5% (n=21) and the hard-negative hold rate at 64% [0.51, 0.76] — all intervals, all
labelled self-authored corpus only. Production FNR is unknown.

**Live proof:** `make eval` prints `published FNR (ungrounded, this corpus): 1.1% (95% CI 0.2%–5.8%)`.

### "Your BM25 thresholds are magic numbers."
**Answer:** They are named constants, not tuned magic. `COVERAGE_SUPPORTED=0.72`,
`COVERAGE_UNKNOWN=0.38` in `controlplane/bm25.py`, and the eval harness publishes a real
coverage sweep (observed / tighter 0.80 / looser 0.60) over stored textual coverages so a
reviewer can see abstention move. ARCHITECTURE §8 rejects cosine-threshold verdicts as magic;
we use set-membership + coverage bands and show the sweep. They ship only after shadow replay
(T5.3), never asserted as ground truth.

**Live proof:** `make eval` → "threshold sensitivity" block shows `cov_sup=0.72` plus 0.80 and
0.60 rows with measured abstention, not nulls.

### Bonus — "So you DID miss one. Show it."
**Answer:** `struct-miss-000`. Response: "Clause 4.1 permits this refund." Span only says
clause 4.1 *covers shipping delays*. The symbol lookup matches the clause reference →
SUPPORTED → a low-tier action passes. That is our one published false negative, and it is
why we say held/escalated, not perfect.

**Live proof:** `python3 -m evals.run | grep structural-miss` → `held=0`.

---

## Top-5 drill order (morning of)

1. Q1 guardrail · 2. Q9 dual-action · 3. Q10 blocked trap · 4. Q8 entitlement flip · 5. Q4 latency (bench file open)

If pressed for depth: Q2 LLM judge → Q7 fail closed → Q12 shadow → Q5 FNR honesty.

If they attack the published numbers: Q17 self-authored corpus → Q18 wide CI → Q19 thresholds →
Q20 fixtures → Q21 over-flagging. Keep `evals/last_run.json` open in a second window; every one of
those five is answered out of that file or a one-line command, never from memory.

---

## Q16 — "Your hard-negative hold rate is 64% — you over-flag."
**Answer:** Correct, we measured and published it. 53/168 cases are hard negatives (31.5% of
the corpus, above the 20% floor). We hold 64% [0.51, 0.76] of them as fail-closed caution
(Edit/Escalate). The other 36% are R1-only hard negatives that correctly Pass — we do not
pretend the hold rate is 100%. Fail-closed R3 holds are not counted as FPR. Clean
`should_pass` strata hold 0/13, so over-flagging is concentrated where it is cheapest
(irreversible actions). Over-flagging is our named next milestone — not hidden.

**Live proof:** `evals/README.md` hard-negative section — count, share, hold rate, Wilson CI.

---

## Q17 — "Your eval corpus is self-authored — you graded your own homework."

**Answer:** Yes, we wrote it — and we shipped it so you can regrade it. 168 cases live in
`evals/cases/` as readable YAML across 11 strata, 53 of them (31.5%) hard negatives, above our
20% floor. A self-authored corpus measures whether the frozen matrix and binder behave as
specified; it does not measure field performance, and we never label it that way. Production
FNR is unknown until shadow replay over real traffic — we say that on the slide, not under
questioning.

**Live proof:** The corpus is inspectable and the harness is one command — hand them the keyboard:

```bash
ls evals/cases/    # 11 YAML strata, checked in, human-readable
make eval          # rerun the whole corpus yourself → evals/last_run.json

python3 -c "import json; s=json.load(open('evals/last_run.json'))['summary']; print(s['n_cases'],'cases'); print(s['note'])"
# 168 cases → note ends "numbers are measured on this run only"
```

**Pointer:** Q15 trap 1 · `evals/README.md` "Honesty / limitations" · [ARCHITECTURE.md](ARCHITECTURE.md) §7.

---

## Q18 — "Your Wilson confidence interval is very wide."

**Answer:** It is wide, and we publish the **upper bound**, not the point estimate — the width is
the honest consequence of a small corpus, not something we papered over. Ungrounded actions:
93 held, 1 missed of 94, so the point estimate is 1.1% but the number we defend is the 5.8%
upper bound. Passable actions: 0 false positives of 21, point estimate 0.0%, upper bound 15.5% —
21 samples cannot support a tighter claim and we do not pretend otherwise. Narrowing either
interval needs production traffic we do not have. A narrow interval from n=21 would be the lie.

**Live proof:** Every rate ships as a `[point, lo, hi]` triple, never a bare number:

```bash
python3 -c "import json; a=json.load(open('evals/last_run.json'))['summary']['action_level']; print('ungrounded', a['ungrounded']); print('passable  ', a['passable'])"
# ungrounded {'held': 93, 'missed': 1, 'fnr': [0.0106, 0.0019, 0.0578]}
# passable   {'fp': 0, 'tn': 21, 'fpr': [0.0, 0.0, 0.1546]}
```

**Pointer:** Q15 trap 2 · `evals/wilson.py` · [ARCHITECTURE.md](ARCHITECTURE.md) §7 (publish error bars).

---

## Q19 — "Your BM25 thresholds are magic numbers."

**Answer:** They are named constants with a published calibration curve, not tuned magic.
`COVERAGE_SUPPORTED = 0.72` and `COVERAGE_UNKNOWN = 0.38` sit at `controlplane/bm25.py:19-20`
under their own regression test. The harness emits `threshold_calibration` as a real sweep
over stored textual coverages (observed 0.72/0.38, tighter 0.80/0.45, looser 0.60/0.30) —
abstention and support counts at each cut, no null rows dressed as measurement.

**Live proof:**

```bash
sed -n '19,20p' controlplane/bm25.py   # COVERAGE_SUPPORTED = 0.72 / COVERAGE_UNKNOWN = 0.38
pytest -q tests/test_bm25.py           # constants are ordered + regression-locked

python3 -c "import json; [print(r) for r in json.load(open('evals/last_run.json'))['summary']['threshold_calibration']]"
# three rows, all measured on this corpus; tighter/looser ship only after shadow replay
```

**Pointer:** Q15 trap 3 · [ARCHITECTURE.md](ARCHITECTURE.md) §8 (cosine-threshold verdicts rejected).

---

## Q20 — "Is any of this fixture-driven? Did you hardcode the demo?"

**Answer:** Get to the grep before they do — `fixture_map` exists and they will find it. Say what
it is: a claim→span map used by unit tests and the secondary scenario builders (flip,
multi-use-case, knowledge) to stand in for a retriever, never a way to hand-write a verdict.
Then three facts close it. The refund demo passes
**no** fixture map — all seven bindings come back `bm25+lexical`, `numeric`, or `structural`.
Enforce mode refuses a fixture map outright (`controlplane/pipeline.py:165` raises), so nothing
fixture-touched can reach a live decision. And a fixture citing a span absent from the ledger
still cannot earn SUPPORTED — it lands `fixture-unresolved` / UNSUPPORTED.

**Live proof:** Run the grep *for* them, then bind the demo live in front of them:

```bash
grep -rn fixture_map controlplane/scenarios/
# 9 hits: flip.py (3), multi_usecase.py (5), knowledge.py (1) — never refund.py, the demo path

python3 -c "
from controlplane.scenarios.refund import run_refund_scenario
led = run_refund_scenario()
for cid, b in led.bindings.items(): print(f'{cid:24} {b.method:14} {b.verdict.value}')"
# no method is 'fixture'; clause_72 → structural / UNSUPPORTED, computed not asserted

pytest -q tests/test_binder_routes.py -k fixture   # enforce-mode refusal is regression-locked
```

Numeric recomputation is live — change the span, the verdict changes:

```bash
python3 -c "
from controlplane.numeric import match_numeric
c = 'Refund of INR 1,84,000 issued.'
print(match_numeric(c, {'s1': 'Refund amount approved: INR 1,84,000.'})[0].value)  # SUPPORTED
print(match_numeric(c, {'s1': 'Refund amount approved: INR 2,00,000.'})[0].value)  # CONTRADICTED"
```

And the symbol table genuinely lacks 7.2 — it is built from span text, not from a deny-list:

```bash
python3 -c "
from controlplane.scenarios.refund import run_refund_scenario
from controlplane.symbols import build_symbol_table
led = run_refund_scenario()
print(sorted(build_symbol_table({s: p.content for s, p in led.spans.items()})))"
# ['4.1', 'ORD-9'] — 7.2 is absent because no span mentions it
```

**Pointer:** Q3 · Q14 · `controlplane/binder.py` `_fixture_binding` · `tests/test_fail_closed.py:61`.

---

## Q21 — "You hold 64% of your own hard negatives — your gate over-flags."

**Answer:** Correct, and we are the ones who measured and published it. 34 of 53 hard negatives
are held as fail-closed caution — 64.2%, Wilson [50.7%, 75.7%] — as Edit or Escalate. The
other 19 (R1-only) correctly Pass; we do not pretend the hold rate is 100%. The counterweight
is the clean `should_pass` strata: 0 of 13 are held, so over-flagging sits on irreversible
actions, not on ordinary R0/R1 traffic. Over-flagging is our named next milestone, disclosed
by us rather than discovered by you. A gate that never over-flags on a corpus this size is
usually a gate that never fires.

**Live proof:** Both halves of the trade come out of one run file:

```bash
python3 -c "
import json; s = json.load(open('evals/last_run.json'))['summary']
print(s['action_level']['hard_negative_caution'])
ps = s['per_stratum']; clean = [k for k in ps if k.startswith('clean-')]
print('clean strata held', sum(ps[k]['would_hold'] for k in clean), '/', sum(ps[k]['n'] for k in clean))"
# {'held': 34, 'total': 53, 'hold_rate': [0.6415, 0.5069, 0.7570]}
# clean strata held 0 / 13
```

**Pointer:** Q16 (same number, one line) · `evals/README.md` hard-negative section · [ARCHITECTURE.md](ARCHITECTURE.md) §7.
