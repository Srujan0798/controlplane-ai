# GATE.md — what "done" actually means

**A green test suite is not done.** On 2026-08-29 the suite reported 333 passing while
the gate held **100% of all inputs** on two of three routes. Every test was green. The
system did not work.

Tests prove the code does what the test says. These numbers prove the system does what
it claims. **No task closes on a green suite alone. It closes when its number below is met.**

Quote the actual measured value in your completion report. "Tests pass" is not a
completion report and will be rejected.

---

## 1. The gate quality bar — blocks everything downstream

Measured by `make eval`, read from `evals/last_run.json`, **per route** (numeric,
structural, textual — not averaged, the worst route governs).

| Metric | Bar | 2026-08-29 actual | Verdict |
|---|---|---|---|
| **Precision** | **≥ 0.85** | 0.34 · 0.33 · 0.71 | ✗ two of three holds are wrong |
| **FPR** | **≤ 0.10** | 1.00 · 1.00 · 0.42 | ✗ holds every negative case |
| **True negatives** | **≥ 30 per route** | 0 · 0 · 19 | ✗ nothing to measure FPR against |
| **Recall** | **≥ 0.90** | 1.00 | ✓ — but see below |
| **FNR** | **reported with Wilson CI, and NOT 0.0%** | 0.0% | ✗ see §1.1 |
| **Abstention rate** | **> 0.02** | 0.000 | ✗ the UNKNOWN band never fires |

### 1.1 Why FNR 0.0% is a failure, not a success

A gate that holds everything has zero false negatives **by construction**. `FNR = 0.00`
sitting next to `FPR = 1.00` is not detection quality — it is the arithmetic of a system
that never releases anything.

Publishing "FNR 0.0%" is worse than publishing a bad number. It reads as *"we catch
everything"* — the single most attackable claim in the submission, and the exact claim
`ARCHITECTURE.md`'s own refuse-to-claim list forbids.

**If FNR comes back 0.0%, the corpus is too easy.** Add cases until the system genuinely
misses something, then publish the real figure with its interval. A published FNR of 8%
with a tight CI beats 0% every time, in the room and on the page.

### 1.2 `tn = 0` means the corpus is broken, not that the gate is perfect

T3.1 required **≥20% hard negatives** — inputs that look wrong but are correct. Two
routes have **zero** true negatives, so FPR is undefined and reported as 1.00 by default.
Fix the corpus before touching thresholds; you cannot calibrate against nothing.

---

## 2. Mechanism bars — each must be demonstrated, not asserted

| # | Bar | How it is proven |
|---|---|---|
| 2.1 | All **16** matrix cells reached through the **real** pipeline | `pytest -q tests/test_matrix_coverage.py` — no hand-built `Binding` objects anywhere in it |
| 2.2 | Every `Verdict` member has a **production** producer | grep shows a non-test, non-fixture caller for each |
| 2.3 | **Zero** `allow_fixtures=True` outside `tests/` | `grep -rn allow_fixtures controlplane/ examples/` returns nothing |
| 2.4 | **Zero** `fixture_map` in any demo path | `grep -rn fixture_map controlplane/pipeline.py controlplane/scenarios/` returns nothing |
| 2.5 | Refund demo yields **Edit + Escalate (held)** with no fixtures | `python3 examples/refund_trace_demo.py` |
| 2.6 | Flip demo flips on **caller identity alone**, no fixtures | `analyst_01` → Edit, `hr_partner_01` → Pass |
| 2.7 | Clause 7.2 fails via the **symbol table**, printable as evidence | the table lists 4.1, 4.3, 9.1 and not 7.2 |
| 2.8 | A **slow Lane 2** still lands the decision in budget via `UNKNOWN` | `pytest -q tests/test_lanes.py` |
| 2.9 | Jurisdiction **changes actuators**, not just annotations | same request, `eu` vs `in` pack → different actuator |
| 2.10 | Bias reports a **flip rate with an interval**, per route | never per response, never a matrix cell |
| 2.11 | Same input → **byte-identical ledger hash** across processes | `pytest -q tests/test_determinism.py` |

---

## 3. Submission bars

| # | Bar | How it is proven |
|---|---|---|
| 3.1 | `make verify` **green** — zero drift between printed and quoted numbers | `make verify` |
| 3.2 | Full suite green, **zero** failures, zero xfails hiding a defect | `pytest -q` |
| 3.3 | **Clean clone runs.** Fresh directory, follow the README PDF verbatim | `git clone <url> /tmp/x && cd /tmp/x && <README steps>` |
| 3.4 | Content laws green over code, docs, **the built PDF**, and **the deck** | `pytest -q tests/test_content_laws.py` |
| 3.5 | Every number in the PDF and deck traceable to a command that prints it | `make verify` diffs them |
| 3.6 | Proposal carries all **seven** of the brief's asks, titled as such | problem framing · solution design · target users · business case · impact · phased roadmap · risks with mitigations |
| 3.7 | README PDF capability ledger marks every mechanism honestly | *implemented and tested* / *prototype-grade* / *designed, not built* |
| 3.8 | The word **"blocked"** never describes the refund — in code, docs, PDF, deck, or the video's audio | content laws for text; listen-back for the video |
| 3.9 | All **five** portal uploads exist and are within type and size limits | public repo link · video · README PDF · proposal PDF · deck PPTX |

---

## 4. Process bars

| # | Bar |
|---|---|
| 4.1 | **Never commit on a red suite.** If `pytest -q` shows a failure, fix or revert — do not commit on top of it. |
| 4.2 | **TDD with a witnessed red.** If you did not see the test fail for the right reason, you did not test it. Delete and redo. |
| 4.3 | **Stay inside your `Owns`.** Touching a file another task owns is a protocol breach regardless of outcome. |
| 4.4 | **Never write the frozen set:** `docs/ARCHITECTURE.md` · `controlplane/interlock.py` · the `Actuator`/`BlastTier` enums · `AGENTS.md`. |
| 4.5 | **A weaker demo is a failed task.** If removing a shortcut makes a beat worse, fix the mechanism — never restore the shortcut. Report instead of shipping the weaker version. |
| 4.6 | **Report the measured number**, not the test result. "Precision 0.91 on numeric, 0.88 structural, 0.93 textual" is a report. "All tests pass" is not. |

---

## 5. Completion report template

Every agent finishing a task must produce this. Anything less is not a completion.

```
TASK: T<id>
FILES WRITTEN: <exact list — must match Owns>
BAR: <the numeric bar this task had to clear>
MEASURED: <the actual value>
COMMAND: <the command that printed it>
OUTPUT:
<paste the real output>
SUITE: <pytest -q final line>
KNOWN GAPS: <anything you did not finish, or "none">
```

**"Done" without a measured number is rejected.**
