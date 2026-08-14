1. Single Sharp Insight
AI oversight fails because it tries to read the model's mind. ControlPlane succeeds because it reads the model's receipts—binding every generated claim to the exact evidence captured at context assembly, turning oversight from a probabilistic guessing game into a deterministic graph-walking problem.

2. What the market currently does (and why each fails against this design)
- **LLM-as-a-Judge:** Uses a second model to evaluate the first. Fails because it is slow, doubles compute cost, and is easily fooled by stylistic confidence. It guesses the logic; we verify the receipts.
- **Static Guardrails (Regex/Keyword):** Brittle string matching. Fails because it lacks semantic awareness and cannot understand context, leading to massive false positives and easy bypasses. 
- **Post-hoc Observability Dashboards:** Logs responses for human review. Fails because it is forensic. It tells you the car crashed after it hit the wall; it does not apply the brakes.
- **Confidence/Logit Thresholding:** Triggers actions based on model uncertainty scores. Fails because a model can be 99% confidently wrong. Logits measure model certainty, not factual accuracy.
- **Simple RAG Checkers:** Does a vector similarity search on the output. Fails on multi-hop reasoning and doesn't track *which* context document proved *which* claim. We map exact provenance.
- **Composite Risk Scores:** Assigns arbitrary math (e.g., 0.8 toxicity + 0.3 hallucination = danger). Meaningless for deterministic engineering decisions. We don't blend risks into a mush; we execute a strict Blast Radius × Severity matrix.

3. Positioning Statement
ControlPlane.ai is not a guardrail; it is a deterministic verification proxy. It sits between your model and your user, treating every AI response not as text to be scored, but as a set of claims requesting permission to act. By capturing the model's context at assembly time and applying an inverted burden of proof, ControlPlane forces the model to prove its claims against the exact data it was given. It catches confidently wrong answers, kills dead compute by walking the reasoning graph backward, and prevents data leakage using strict access control lists. It turns oversight from after-the-fact discovery into real-time, graph-based enforcement.

4. Differentiation Table

| Common Approach | How ControlPlane is Fundamentally Different |
| :--- | :--- |
| **LLM-as-a-Judge** (Probabilistic text scoring) | **Deterministic Graph Walk:** Verifies claims against hashed context captured at assembly. No guessing, no semantic spoofing. |
| **Post-hoc Dashboards** (Forensic logging) | **Pre-action Gating:** Hard gates on actions (API calls, DB writes) while optimistically streaming text. Stops the error before it executes. |
| **Confidence Thresholding** (Logit scores) | **Inverted Burden of Proof:** Default state is UNSUPPORTED. The model must graph-traverse to provenance to earn a passing verdict. |
| **Black-box Toxicity Filters** (Keyword/Probabilistic filters) | **ACL-Entitlement Mapping:** Leakage isn't a vibe; it's a strict check of output entities against the user's deterministic Access Control List. |

5. Narrative Spine (exact beat sequence for 3-minute video)
- **0:00–0:30 Opening hook:** "When an AI fails, it fails confidently. Current oversight tools try to read the model's mind to catch this. ControlPlane reads its receipts. An AI response isn't text; it's a set of claims requesting permission to act."
- **0:30–1:15 Problem + reframe:** Show the failure: a confident hallucination burning compute and leaking data. Reframe: you can't score text after the fact. You must bind the output to the context captured *before* generation. Introduce the graph: STEP → SPAN → CLAIM → ACTION.
- **1:15–2:15 Core mechanism + the three-axis demo:** Visualize the context assembly hash. Walk through the three axes: Performance (claim lacks provenance → UNSUPPORTED), Cost (backward graph walk finds a dead branch → compute killed), Responsibility (output entity hits ACL deny list → blocked).
- **2:15–2:45 Decision logic / why it doesn’t over-block:** Explain the Blast Radius R0–R3 × Severity matrix. Show optimistic text streaming (user reads while we verify) with a hard gate on the final tool call. Show surgical edit vs. escalate (shipping the structured evidence packet).
- **2:45–3:00 Closing line (must land hard):** "We don't hope the AI is right. We don't guess if it's wrong. We publish our own false-negative rate per route, because true oversight isn't a safety blanket—it's an engineering commitment. Find it first."

6. What we deliberately refuse to claim
- **"Zero latency overhead."** (We claim *non-blocking* latency via optimistic streaming and hard action gates. We don't pretend verification is free).
- **"100% hallucination elimination."** (We publish our false-negative rate. Claiming perfection destroys credibility with serious engineers).
- **"Self-healing AI."** (We don't let the model rewrite its own mistakes. We surgically edit or escalate to humans with evidence).
- **"General AI alignment."** (We solve enterprise reliability, safety, and cost. We don't touch philosophical alignment or AGI safety).

7. Strongest narrative risk + exact correction
- **Risk:** The story collapses into "another AI safety tool" because judges conflate any mention of "responsibility" or "bias" with fuzzy, probabilistic ethics guardrails.
- **Correction:** Strip all moralizing language. Talk like a distributed systems engineer. "Responsibility" becomes "Deterministic ACL Entitlement Leakage." "Bias" is ignored in favor of "Data Exfiltration." Position the entire system as an infrastructure reliability proxy (like a network firewall or a transaction validator), not an AI ethics wrapper. The language must be cold, mathematical, and graph-structured.