### Overall Timing Map
- **0:00–0:25 | The Failure:** Establish the stakes by showing a specific, executed transaction that should have been impossible.
- **0:25–0:55 | The Reframe:** Shift the mental model from scoring text to authorizing actions via a directed graph.
- **0:55–1:45 | The Mechanism:** Trace the refund through the graph, proving how one graph yields three distinct reads.
- **1:45–2:30 | The Decision:** Show the matrix and the hard gate. Explain the escalation path without blocking text.
- **2:30–3:00 | The Credibility & Close:** Establish engineering rigor through published false-negative rates, then deliver the final blow.

### Beat-by-Beat Script

**Beat 1: The Failure**
- **Exact time range:** 0:00–0:25
- **Visual:** Screen recording of a clean enterprise console. Text streams rapidly: *"Based on Clause 7.2, I have processed a refund of ₹1,84,000 to the customer."* A green checkmark appears next to the text: `Transaction Executed`. 
- **Spoken words:** "An AI just authorized a refund of ₹1,84,000. The policy explicitly caps refunds at ₹50,000 under Clause 7.2. The system didn’t fail. It was never asked to prove anything."
- **Delivery notes:** Cold, deliberate pace. Pause for one second after "Transaction Executed" on screen. Hit the word "prove" hard.

**Beat 2: The Reframe**
- **Exact time range:** 0:25–0:55
- **Visual:** Cut to Slide 1. The paragraph of text shatters, rearranging into the directed graph: STEP → SPAN → CLAIM → ACTION. A lock icon glows on the ACTION node. 
- **Spoken words:** "We stop reading text. An AI response is a set of claims requesting permission to act. Before generation, we capture context outside the model. Source, access control list, hash. Every claim defaults to UNSUPPORTED. The model must bind to the hash to earn a passing verdict."
- **Delivery notes:** Faster, systems-engineer rhythm. Emphasize "outside the model" and "UNSUPPORTED".

**Beat 3: The Mechanism**
- **Exact time range:** 0:55–1:45
- **Visual:** Graph zooms in. Node lights up: `CLAIM: ₹1,84,000 refund`. A red line draws backward from the claim to a hashed document node labeled `Clause 7.2`. The graph pulses, splitting into three distinct color-coded reads: Performance (Red), Cost (Orange), Responsibility (Yellow).
- **Spoken words:** "Watch the refund. The model streams the claim. Default state: UNSUPPORTED. The system walks the graph backward to the hashed context. Clause 7.2 contradicts the amount. One graph, read three ways. Performance: Contradicted. Cost: Downstream tool calls are dead compute, compute killed. Responsibility: The user lacks the ACL for this amount."
- **Delivery notes:** Relentless logic. No pauses until the three reads are complete. Show, do not explain.

**Beat 4: The Decision**
- **Exact time range:** 1:45–2:30
- **Visual:** Cut to Slide 2. The Blast Radius × Severity matrix flashes on screen. Camera pushes in rapidly on the intersection of `R3: External Action` and `Categorical Contradiction`. The cell populates with `ESCALATE`.
- **Spoken words:** "Decision logic. Blast Radius R3. External action. Verdict: categorical contradiction. We do not block the text. The user reads the response. But the action hits a hard gate. The transaction is refused. ControlPlane escalates a structured evidence packet to a human. The exact contradicting clause, linked."
- **Delivery notes:** Authoritative. Stress "do not block the text" to contrast with legacy guardrails. 

**Beat 5: The Credibility & Close**
- **Exact time range:** 2:30–3:00
- **Visual:** Cut to Slide 3. Left column (what we refuse) is dim. Right column highlights: `Per-route false-negative rates published`. The text fades, leaving only the closing line in massive, heavy typeface.
- **Spoken words:** "We do not guess. We publish our own per-route false-negative rate. It used to be a bad paragraph. It is now an executed transaction. Now nothing acts until it can prove it should."
- **Delivery notes:** Dead slow. Total silence after "should." Cut to black immediately.

### Closing Discipline
- **Exact final spoken line:** "Now nothing acts until it can prove it should."
- **What happens visually in the last 5–8 seconds:** All other text dissolves. The closing line fills the frame in a heavy, stark typeface. It holds for 3 seconds in absolute silence, then hard-cuts to black.
- **What is deliberately left unsaid:** We do not say "AI safety." We do not say "guardrails." We do not promise zero hallucinations. We do not apologize for the model's behavior; we simply route the evidence.

### Rules Applied
1. **One-trace rule:** The ₹1,84,000 refund under Clause 7.2 is the only scenario shown, end-to-end.
2. **Vocabulary bans:** Zero uses of monitor, detect, observe, guard, or trust score. Replaced exclusively with authorize, prove, bind, refuse, hold, and walk.
3. **No abstract risk:** Opened on a specific, executed financial transaction, never on the concept of "risk."
4. **Matrix brevity:** The matrix appeared for less than 10 seconds to establish the R3 escalation logic, then was discarded so as not to lecture the grid.
5. **Hard cut ending:** No fade-out, no soft music trailing, no summary sentence. The final word hits and the video stops.