1. Core Thesis
Real-time AI oversight is fundamentally a streaming data problem, not a post-processing text analysis problem. ControlPlane.ai operates as an asynchronous reverse-proxy that intercepts token streams, extracting atomic claims as they form and routing them through parallel, evidence-gated validators, allowing us to enforce deterministic safety blocks instantly while evaluating semantic correctness via "shadow validation" that never blocks the user's rendering speed.

2. Detection Layer — one concrete mechanism per axis
- Performance (confidently wrong)
  - Mechanism: Streaming Claim-vs-Proof Extraction. As tokens stream, a lightweight local parser identifies atomic factual claims (dates, entities, causal relationships). 
  - Signals: Embeddings of extracted claims queried against an authorized ground-truth vector DB (RAG context). 
  - Computed: Semantic distance and entailment score. 
  - False Positive Control: We do not block on "unverified" (absence of evidence); we only flag/block on "contradicted" (evidence of absence). A claim is marked confidently wrong only if a hostile validation agent retrieves a directly contradicting fact with >0.85 cosine similarity.
- Cost (waste / rework)
  - Mechanism: Semantic Loop & Velocity Tracker. 
  - Signals: A sliding window (e.g., last 512 tokens) is continuously embedded. We track the delta between consecutive chunks. 
  - Computed: If the semantic cosine similarity between consecutive generation chunks remains >0.92 for 3 consecutive windows, or if the agent makes identical tool calls with identical parameters twice in a row, the model is looping. 
  - False Positive Control: Legitimate repetition (e.g., summarizing a list of identical items) is distinguished from loops by checking if the agent's internal thought/plan state is advancing. If tokens repeat but plan-state fails to transition, it's a loop.
- Responsibility (biased / unsafe / leaking data)
  - Mechanism: Deterministic Regex + Contextual NER Pipeline (Fast-Path).
  - Signals: Raw token byte-stream and structured logit scores (if accessible via provider API).
  - Computed: High-speed regex for strict PII formats (SSNs, credit cards) and a quantized, locally hosted NER model for contextual entities (e.g., names in a medical context). For safety/bias, a lightweight toxicity classifier runs on sentence boundaries.
  - False Positive Control: Strict boundary matching. PII detection requires high-confidence NER tags combined with format validation. No probabilistic "bias scores"—only hard categorical violations of predefined data schemas trigger action.

3. Decision Policy Engine
The engine operates as a hierarchical state machine, strictly gated by evidence and latency budgets:
- Block: Triggered exclusively by deterministic Responsibility violations (PII/Secret leakage) or explicit safety classifier hits. The stream is severed immediately, and a pre-cached fallback message is returned.
- Edit: Triggered by minor Responsibility issues (e.g., echoing back a user's profanity). A streaming string replacement masks the token sequence before it hits the user's UI.
- Escalate: Triggered by Performance contradictions or Cost loops. The response is allowed to pass to the user, but a real-time UI flag ("⚠️ Unverified Claim Detected") is injected, and the session is routed to a human review queue with the contradicting evidence attached.
- Pass: Default state.
Policy Enforcement: The policy is evidence-gated because action requires a retrieved contradicting fact (Performance) or a deterministic regex/NER hit (Responsibility). It is latency-aware because Block/Edit only apply to fast, deterministic checks; semantic checks that take >200ms default to Escalate/Pass.

4. Latency & Non-Blocking Design
- Streaming Reverse Proxy: ControlPlane sits between the user and the LLM API. It forwards tokens to the user instantly while mirroring them to the evaluation agents.
- Fast/Slow Path Split: 
  - Fast Path (<5ms): Regex/NER/Loop detection runs synchronously on the stream buffer. If breached, it drops the connection.
  - Slow Path (Parallel): Claim extraction, embedding, and hostile validation happen asynchronously. 
- Shadow Validation: If the LLM finishes generating before the hostile validator finishes checking claims, the user receives the text, but the UI highlights claims in real-time as they are verified or contradicted post-hoc. We prioritize "finding it first" over "perfect gating" for complex semantic errors.
- Early-Stop Signaling: If the Cost tracker detects a semantic loop, ControlPlane injects an out-of-band stop sequence (`<|control_stop|>`) into the provider API, terminating compute billing instantly.

5. Internal Multi-Agent Structure
Leveraging the team's evidence-gated multi-agent expertise:
- Coordinator (The Proxy): Manages the byte-stream, enforces the latency budget, and executes the Decision Policy. Owns the connection.
- Claim Extractor: A fast, locally quantized model that parses the stream and emits structured JSON claims.
- Hostile Validator: An agent equipped with retrieval tools. It receives claims and actively searches the ground-truth DB to disprove them. It passes back a verdict (Verified/Contradicted/Unverified) with citation pointers.
- Sentinel: A deterministic rules-engine agent monitoring the byte-stream for regex/NER violations and semantic velocity drops.
Coordination: Agents communicate via an in-memory event bus. The Coordinator does not wait for consensus; it operates on a strict time-box. If Sentinel flags a hit, Coordinator blocks. If Hostile Validator finds a contradiction after 400ms, Coordinator escalates. Evidence is passed as structured JSON payloads with direct pointers to source text, ensuring zero-context-loss between agents.

6. What this deliberately does NOT do
- No "LLM-as-a-Judge" for the final output: Running a second LLM to evaluate the first is a latency nightmare, doubles compute cost, and is easily fooled by stylistic confidence. We use deterministic retrieval and lightweight parsers.
- No static, post-hoc guardrails: We do not evaluate the final string. We evaluate the semantic state of the generation as it forms.
- No semantic blocking for performance/cost: We reject the idea of blocking a response because it "might be wrong." False positives on semantic blocking destroy user trust. We edit/block only deterministic safety issues; we warn/escalate semantic issues.
- No assumed access to model weights: The architecture treats the target LLM as a black-box API, relying solely on the observable token stream.

7. Single strongest technical risk in this design
- Risk: The "Streaming Claim Extractor" may fragment atomic claims across token boundaries, causing the Hostile Validator to evaluate incomplete facts, leading to false contradictions and UI flicker.
- Mitigation: The Extractor operates on a sentence-boundary buffer. It holds tokens until punctuation (period, colon, newline) is detected, extracts the complete claim, and then flushes to the Validator. For the UI, validation badges appear at the sentence level, not the token level, ensuring semantic coherence without perceptible user latency. This makes the concept highly demonstrable in a 3-slide pitch (Slide 1: Proxy Architecture, Slide 2: Fast/Slow Path Latency, Slide 3: Live UI Validation Demo).