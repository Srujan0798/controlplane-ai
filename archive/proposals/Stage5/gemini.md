### Overall Timing Map

| Beat | Time Range | Beat Title | Single Job |
| --- | --- | --- | --- |
| **Beat 1** | **0:00–0:30** | The Failed Transaction | Reframe output from harmless text to executed action via the ₹1,84,000 refund failure. |
| **Beat 2** | **0:30–1:15** | Provenance Capture & Inverted Burden | Establish context-assembly evidence binding and the default `UNSUPPORTED` state. |
| **Beat 3** | **1:15–2:15** | Walking the Trace: Three Reads | Execute the ₹1,84,000 trace across the unified `STEP → SPAN → CLAIM → ACTION` graph. |
| **Beat 4** | **2:15–2:45** | Decision Logic & Actuation | Show $R_3 \times \text{UNSUPPORTED}$ triggering an `ESCALATE` hold with a structured evidence packet. |
| **Beat 5** | **2:45–3:00** | Closing Land & Stance | Land the hard final stance and publish the per-route false-negative rate format. |

---

### Beat-by-Beat Script

#### Beat 1: The Failed Transaction (0:00–0:30)

* **On Screen:**
Split screen matching Slide 1 layout. Left: Customer support chat interface showing model output: `"Refunding ₹1,84,000 under Clause 7.2 policy override."` Right: Banking API terminal firing a webhook: `POST /v1/transact - 200 OK - TRANS_ID_883921`.
* **Spoken Script:**
> "An enterprise AI agent just issued an unauthorized refund of ₹1,84,000. It cited Clause 7.2—a clause that does not exist in the contract. The model logged the string. The API executed the payment. The system didn’t fail. It was never asked to prove anything. It used to be a bad paragraph. It is now an executed transaction."


* **Delivery Notes:**
Flat, deliberate pacing. No dramatic inflection. Let the contrast between text logging and money moving do the work. Pause for 1 full second after *"never asked to prove anything."*

#### Beat 2: Provenance Capture & Inverted Burden (0:30–1:15)

* **On Screen:**
Slide 1 bottom path animates. Context assembly pipeline ingests `contract_v2.pdf`, assigns ACL `[ROLE: SUPPORT_L1]`, and emits a cryptographic hash `0x9f4a...` outside the model. The graph sequence lights up: `STEP → SPAN → CLAIM → ACTION`.
* **Spoken Script:**
> "ControlPlane shifts execution authority. An AI response is not text—it is a set of claims requesting permission to act. Before the model generates a single token, ControlPlane captures evidence outside the model at context assembly, binding the source, ACL permissions, and cryptographic hash. When the model outputs a claim, its default state is UNSUPPORTED. It receives zero authority until bound to provenance."


* **Delivery Notes:**
Increase tempo slightly on mechanics. Emphasize **`UNSUPPORTED`** with a hard stress.

#### Beat 3: Walking the Trace: Three Reads (1:15–2:15)

* **On Screen:**
Unified execution graph animating the ₹1,84,000 refund trace in three distinct passes:
1. *Performance:* `CLAIM` node ("Clause 7.2") attempts match against Context Hash `0x9f4a...`. Highlight: `NO_MATCH`.
2. *Cost:* `SPAN` node loops twice retrying the claim. The backward trace highlights dead-compute tokens returning to the origin.
3. *Responsibility:* `ACTION` node (`POST /api/v1/refund`) checks ACL `[ROLE: SUPPORT_L1]`. Max limit: ₹10,000. Attempted: ₹1,84,000. Highlight: `ACL_EXCEEDED`.


* **Spoken Script:**
> "Watch one trace read three ways across the same execution graph: STEP, SPAN, CLAIM, ACTION. First, performance: the claim cites Clause 7.2. ControlPlane checks the context hash—no match found. Status remains UNSUPPORTED. Second, cost: the model loops to force the claim. ControlPlane walks the graph backward, identifies zero state velocity, and terminates the dead compute. Third, responsibility: the action requests a ₹1,84,000 payout under an L1 token. Deterministic ACL check refuses the entitlement."


* **Delivery Notes:**
Maintain rhythmic cadence across the three reads. Clear pause between *First*, *Second*, and *Third*.

#### Beat 4: Decision Logic & Actuation (2:15–2:45)

* **On Screen:**
Slide 2 Matrix appears for 2 seconds. The camera clips directly to row $R_3$ (State Transaction) $\times$ `UNSUPPORTED`. Matrix cell flashes: `ESCALATE & HOLD`. UI transitions to an operator terminal displaying a structured JSON evidence packet containing the exact ungrounded claim node and context hash gap.
* **Spoken Script:**
> "We don't blind-block every error. Verification budget scales with blast radius. For low-risk text at R0, we stream optimistically with a short hold-back. But at R3—a state transaction of ₹1,84,000—an unsupported claim triggers an immediate hold and escalates a structured evidence packet to a human operator. The action is gated; the evidence is proven."


* **Delivery Notes:**
Firm, precise. Treat $R_0$ vs $R_3$ as a clean operational trade-off, not a feature list.

#### Beat 5: Closing Land & Stance (2:45–3:00)

* **On Screen:**
Slide 3 right column populates. Live terminal output displays the plane telemetry header: `ROUTE: /v1/finance/refund | FN_ROUTE: 0.0000% | STATUS: ACTIVE`. The final sentence replaces all graphics, rendered in 36pt stark typography.
* **Spoken Script:**
> "We publish our own per-route false-negative rate live. Stop reading what your AI generated after it acts. Now nothing acts until it can prove it should."


* **Delivery Notes:**
Drop tone slightly. Speak the final sentence with absolute finality. Do not speed up. Stop speaking precisely at 2:58.

---

### Closing Discipline

* **Exact Final Spoken Line:**
> "Now nothing acts until it can prove it should."


* **Visual in Last 5–8 Seconds:**
All diagrams wipe. Screen cuts to pure black background with white, centered, un-styled text: **Now nothing acts until it can prove it should.** Below it in small, gray 14pt monospaced text: `ControlPlane.ai | FN_route published live`.
* **What Is Deliberately Left Unsaid:**
* No mention of "saving money" or general enterprise AI ROI.
* No pitch about how easy it is to integrate or install.
* No call to action ("Visit our website", "Contact us", "Vote for us").
* No generic statements about making AI safe for humanity.



---

### Rules Applied

1. **Single-Trace Strictness:** The entire 3 minutes strictly follows the ₹1,84,000 refund / Clause 7.2 transaction. No secondary examples (e.g., healthcare, code generation) were introduced.
2. **Watching Vocabulary Ban Enforced:** The words *monitor*, *detect*, *observe*, *guard*, and *trust score* were entirely excluded. Replaced with *authorize*, *prove*, *bind*, *refuse*, *hold*, and *gate*.
3. **No Action-Oriented Opening on "Safety":** Opened immediately on a concrete transaction failure (₹1,84,000 bank payout) rather than high-level statements about AI risk.
4. **Matrix Minimization:** The $R_0–R_3$ decision grid was displayed for under 3 seconds to establish mechanics without lecturing the slide.
5. **Hard Stop Closing:** The audio terminates abruptly on a sharp, monosyllabic cadence at 2:58 without soft trailing summary sentences or call-to-action slide fluff.