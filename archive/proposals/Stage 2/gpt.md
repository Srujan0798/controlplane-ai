# ControlPlane.ai: Evidence-Gated AI Safety Architecture

**Core Thesis (Evidence-First Gating).**  The ControlPlane.ai design treats AI answers as *unverified claims* and enforces **evidence coverage** as a primary runtime constraint. Unlike approaches that score output risk via an LLM “judge” (which suffer circular blind spots), ControlPlane.ai only approves responses backed by retrieved or cached evidence.  In practice the control plane acts as an external decision layer: it “decides who may act, judges whether the action was acceptable, and keeps the proof”.  This mirrors networking-style separation of **control plane (slow/complex) vs. data plane (fast/simple)**.  Here, evidence is treated like latency or memory: responses are **passed, edited, blocked or escalated** based on whether verifiable support is found.  In short, *decision-making* is gated on concrete evidence retrieval, not on a model’s ungrounded confidence or a one-size-fits-all risk score.

## Detection Layer: Signals per Dimension

ControlPlane.ai decomposes safety/performance checks into three orthogonal axes, each with its own simple detector(s). This multi-dimensional design avoids collapsing everything into a single risk number.

- **Performance (Hallucinations / Confidence).**  We track *evidence coverage* and claim-proof alignment.  Each assistant response is decomposed into “claim spans” and matched against external sources (search, tools, knowledge) to compute an **Evidence Coverage Score (ECS)** – the fraction of claims with verifiable citations.  Claim–proof *alignment* is measured (e.g. via embeddings or NLI) to check if each cited source actually supports the claim.  A red flag (“confidently wrong”) is raised when the model’s **verbal confidence** is high *but* evidence coverage and alignment are low.  This directly catches high-confidence hallucinations that LLM-as-judge often misses: indeed, recent studies show LLM-judge outputs often agree with correct factual content but *fail to catch structural or evidence gaps*.  In one system-wide evaluation, evidence coverage proved the strongest signal for severe failures.  (By contrast, a single composite risk score would conflate contradictory axes and hide which factor actually triggered a gate.)

- **Cost (Inefficiency).**  We monitor wasteful output patterns.  For example, **Marginal Cost per Useful Token (MCUT)** counts the tokens in a response that correspond to verifiable claims, normalized by total tokens.  A low useful-token ratio, or a high **rework ratio** (user repeating the same request shortly after), indicates inefficiency.  These cost signals are tracked continuously (e.g. z-scored over recent baseline) but *only trigger alerts, not hard blocks*.  The idea is to downgrade the model or issue an operational alert if efficiency anomalies appear, rather than frustrate users.  (Research on AI deployment emphasizes that balancing speed, cost and accuracy is an enterprise concern; latency should be managed as an operating constraint.)  In ControlPlane.ai, cost checks run asynchronously and never block the user path; they simply feed back into monitoring or routing decisions, since repeatedly blocking a user for inefficiency would backfire.

- **Responsibility (Privacy/Safety/Bias).**  Here we use small, fast detectors for obvious violations, with tiered responses:

  - **PII/PHI Leakage.**  Deterministic checks (regex and lightweight NER) scan every token.  This is cheap (under ~10ms in optimized code) and catches names, IDs, credentials etc. exactly.  Leading AI governance guidance stresses that blocking is required for PII leaks – logging alone is ineffective.  ControlPlane implements a **hard block** (suppress output) on any confirmed PII match.  (By blocking early at the gateway, the system “separates technical vs. organizational risk” – the user is never exposed to a privacy breach.)

  - **Harmful Content.**  A distilled safety classifier (e.g. a <1B parameter guard model) flags blatant toxicity, CSAM keywords, or prompt-jailbreak content.  Recent research shows that small specialized detectors, when fine-tuned on internal activation patterns, can outperform brute-force LLM classifiers while being extremely fast.  We use this lightweight model in-line for Tier-1 checks.  Scores above a high threshold trigger a **soft edit or redaction** (rather than immediate block), ensuring we err toward caution but still allow nuance.

  - **Demographic Bias.**  We only trigger when outputs mention protected groups or stereotypes.  Simple statistical tests (e.g. measuring parity or sentiment differences against expected base rates) can flag potential bias.  However, these checks are asynchronous and “flag for review” rather than block.  (The first response to a subtle bias issue is just to note it; only repeated offenses or egregious parity failures would escalate to an intervention.)

Each sub-detector is tuned for very low false-block rates. For example, regex+NER PII checks are deterministic and rarely false-positive when matched exactly.  Harmful-content detectors use conservative thresholds so that only blatant violations are auto-edited.  ControlPlane.ai also calibrates the evidence threshold in shadow mode to keep unintended blocks <5% of cases.  Crucially, gating signals are tested against human review, *not* another LLM, to avoid circular validation.

## Policy Engine (Rule DAG)

Decisions are made by a versioned **policy engine**, implemented as a directed acyclic graph of independent rules.  Each rule specifies a signal, threshold, action (Block/Edit/Escalate/Pass), and an execution budget.  For example, a PII rule might be `(PII_detected, any, Block, 20ms)`, while a hallucination rule might be `(ECS<20%, HighConfidence, Escalate, 200ms)`.  The DAG structure (rather than nested if-else) lets multiple rules fire simultaneously on different axes.  Crucially, rules are **evidence-gated**: if a claim has no proof yet retrieved, any rule depending on evidence simply defers (flagging to revisit later) rather than guessing.  This “hostile validation” philosophy means the engine never infers missing data – it only acts on confirmed inputs.

Each rule also respects a latency budget. If a check would exceed its allotted time (e.g. a slow retrieval), the engine automatically **downgrades** the action: for example, a planned Block might become an Escalate (human review) or a passive Flag for later, to avoid stalling the chat.  This is intentional: the system prefers occasional missed detections over any risk of breaking the latency SLA.  (In practice, if gating ever violates the budget, the control plane for that request is disabled in-flight to keep the agent responsive.)

The policy DAG itself is treated as code: it is version-controlled and can be canary-deployed.  If human overrides spike (e.g. customers repeatedly disagree with blocks), the system automatically rolls back to the last good version.  In short, ControlPlane.ai enforces a *declarative*, auditable ruleset at runtime, rather than a monolithic learned model, so that each violation path is transparent and testable.

## Latency & Non-Blocking Architecture

ControlPlane.ai is built for **extremely low latency overhead** on user-facing responses.  Key tactics:

- **Sidecar (Out-of-Path) Enforcement.**  The control plane runs as a separate process or “agent gateway” alongside the LLM, not in it. The LLM emits a response immediately once basic checks pass, while deeper validation continues in parallel.  (As Fiddler notes, enforcement should attach at a proxy/gateway that “can hold, redact, or block a call” before it reaches the user.)  In practice we do a speculative release: if Tier-1 safety signals are clean, the user sees the response instantly; Tier-2/Tier-3 checks run asynchronously and can trigger edits or recalls after the fact.  The user always perceives only the LLM’s speed, not the gating.

- **Tiered Checks.**  We classify checks into timing tiers.  Tier-1 (synchronous, ~50ms p50 budget) includes regex/NER PII, obvious safety filters, the user’s token cap, and a quick policy lookup (based on already-collected evidence).  Tier-2 (background, up to ~2s) includes full evidence coverage scoring, claim–proof alignment computations, and MCUT.  Tier-3 (offline, up to ~60s or logged) handles bias parity, cross-session consistency, analytics, and continuous shadow-mode evaluation.  This tiering ensures the fast path only involves ultra-light checks, while heavier analyses do not block the response.

- **Streaming Gate.**  Even in multi-turn conversations, only the first ~50 tokens of a response are gated fully; the rest stream out while evidence for the initial claims is still being gathered.  This bounds the perceived delay even for long completions.

- **Shadow Mode Measurement.**  ControlPlane.ai continuously runs a fraction (e.g. 5%) of traffic in “shadow mode”: for each query, the LLM replies both with and without the gate active, and logs differences.  This is a live A/B test that measures how many additional violations the gate catches versus how much it would have delayed or altered good answers.  As one AI deployment guide emphasizes, shadow deployment is the safest way to validate an AI system in parallel with human/legacy workflows.  By continuously comparing gated vs ungated outcomes in real traffic, we never have to blindly trust our own performance metrics.

**Latency Targets.**  Empirically, ControlPlane.ai aims to add *≤50ms* (p50) and *≤200ms* (p95) to response time.  Everything slower than that automatically slips into a lower tier or is dropped: for instance, if evidence retrieval is slow, the system just flags the response for later review instead of holding the user’s call.  In other words, *meeting latency SLAs is the #1 safety requirement*; if our gate ever risks breaking the SLA, the gate steps back.  As DataRobot warns, latency “is not just an engineering metric; it is an operating constraint with direct business consequences”.  ControlPlane.ai is explicitly designed so that speed is never sacrificed for extra checking.

## Internal Multi-Agent Pipeline

Behind the scenes, ControlPlane.ai is implemented as a miniature pipeline of cooperating components (not debates or self-evaluation).  Each component emits a typed *evidence packet*:

- **Director (Policy Resolver):** Runs the policy DAG rules and decides the final action flags (sync, Tier-1).  
- **Evidence Builder:** Breaks down the LLM response into claims and retrieves supporting passages or documents; attaches evidence to each claim (async, Tier-2).  
- **Performance Watcher:** Computes ECS, claim–proof alignment scores, calibration gaps (async, Tier-2).  
- **Cost Watcher:** Tracks token usage efficiency, rework ratio, etc. (async, Tier-3).  
- **Responsibility Watcher:** Runs the PII/NER filter (sync), harm classifier (sync), and bias checker (async Tier-3) to emit flags or scores.

Each agent runs in parallel but with time-awareness.  If Tier-2 evidence isn’t ready by decision time, downstream checks simply return “insufficient evidence → flag” rather than guess a result.  Fast agents (e.g. the Director or PII filter) *can* block mid-stream if they detect a deterministic violation, whereas slow agents only append to the audit trail or suggest a post-hoc edit.  This asymmetry ensures that quick, certain checks trump anything that comes later – we never go back and undo a fast decision based on a slow check.

## What This *Does Not* Do

ControlPlane.ai deliberately avoids several common pitfalls:

- **Not “LLM-as-Judge.”**  We do *not* rely on another LLM to critique or score the assistant’s output.  Those models are prone to the same blind spots and biases, and can be slow (300ms–2s) and expensive.  Empirical results show LLM-judges often miss structural errors (like latency or missing evidence) that our multi-faceted checks catch.  Instead, we use task-specific detectors and deterministic logic.

- **Not a Monolithic Safety Model.**  There is no single large “safety LLM” at the end of the pipeline.  That would be a single point of failure and latency.  ControlPlane.ai uses many small pieces (regex, classifiers, rule engine), each specialized and fast.

- **Not One Composite Score.**  We avoid collapsing all checks into one “risk score.”  A unified score hides which safety axis failed and makes it hard for developers or users to respond.  ControlPlane.ai’s rule DAG lets different issues be handled by different actions (e.g. a factual gap leads to escalation, whereas a leak leads to block).

- **Not Regex-Only.**  We go far beyond static blocklists.  While we do use regex for PII and known key phrases, all major decisions also involve evidence matching, retrieval caches, or classifier judgments.  This mitigates the brittleness of regex alone.

- **Not Training a New LLM.**  ControlPlane.ai is a **layer on top** of models, not a competitor model.  We do not improve safety by fine-tuning another LLM; we add an orchestration and policy layer.  The innovation is in evidence-based rules, not in a bigger generative model.

- **Not Block-First.**  The default is to try passing or softly editing, not outright blocking.  For example, PII leaks *do* hard-block, but content that is borderline harmful is only soft-edited or flagged for human review.  Over-blocking trains users to disable the safety layer.  Instead, extreme conservatism (hard block) is reserved for **deterministic violations** (e.g. confirmed PII, no evidence at all, or explicit policy breach); everything else prefers to log or escalate.

- **Not Debate/Voting.**  We do not spin up a bunch of agents to argue about safety in real-time.  That approach is useful for analysis but too slow and unpredictable for gating.  Discussion agents only run in offline audit mode (e.g. in Tier-3 replay or compliance checks), not on the critical path.

## Technical Risk & Mitigation

The single greatest risk is **latency becoming the bottleneck**.  If the control plane ever makes the AI feel slower than it really is, users (or product teams) will simply disable it.  To defend this:

1. **Tiered Checks:** Only ultra-fast, deterministic rules are on the hot path.  The rest run in the background.  We hold ourselves to an empirical ceiling of ≤50ms p50 and ≤200ms p95 added latency.  Anything above that is bumped to Tier-2.

2. **Speculative Release:** The user always sees the LLM’s answer immediately after Tier-1.  Deeper checks run in shadow/async.  In effect, the system *never* waits on the gate.  This is akin to “speculative execution” in CPUs or pipelines: do the fast path now, and catch up later if needed.

3. **Continuous Shadow Testing:** The layer measures itself in flight.  By dual-emitting gated vs. ungated results on a small percentage of traffic, we see the real catch-rate vs. real friction.  This closed-loop monitoring ensures we never blindly trust our own numbers.  (As an industry post notes, shadow mode provides real-world feedback on latency and accuracy before committing.)

If the latency bet fails (i.e. if Tier-1 checks ever slip over budget regularly), the control layer degrades itself out of the loop.  In that event, the architecture still stands – it simply falls back to ungated inference, with logs to improve the next version.

## Adversarial Review Scenarios

**Q: “What if the evidence matching fails? Can’t the model still hallucinate unsupported claims?”**  
Yes, claim decomposition and retrieval are not perfect.  That’s why ControlPlane.ai flags low-ECS responses as uncertain.  In practice, the system may either block or escalate any reply with *zero* evidence coverage.  For non-zero but low coverage, the response might be passed with a note or sent to a lightweight “editor” LLM that must ground every claim.  The evidence-gating primitive itself is studied in recent work: e.g. DeepSciVerify shows that a tiered approach (initial abstract check, then full-text) lets most claims be verified quickly with early exit.  Similarly, ControlPlane.ai uses conservative rules: no evidence → no trust.  Moreover, the 7-day shadow mode will statistically reveal any patterns of undetected hallucinations, so thresholds can be adjusted.

**Q: “How do you set thresholds (e.g. ECS %) without blocking too much valid output?”**  
We auto-calibrate in production.  ControlPlane.ai runs in shadow mode on ~5% of real traffic, comparing gate decisions to human judgments.  This allows us to tune each rule’s threshold (say, evidence score or classifier probability) to hit a target false-positive rate (e.g. ≤5% blocks).  In one evaluation of a multi-dimensional gate, disagreements between an LLM-judge and system gate had κ=0.13; structural failures (like latency) caused most gate blocks, not content errors.  This suggests we can catch many issues without unduly flagging good answers.  Still, any threshold can be adjusted: if shadow logs show we’re flagging non-issues, we relax the rule.

**Q: “Is 50ms gating realistic in a real networked system?”**  
It is challenging, but we mitigate network cost by caching and side-channel telemetry.  Many checks (regex, NER, simple policy lookup) are entirely in-memory and complete in microseconds.  Only lookups (e.g. retrieval or NLI) risk exceeding 50ms.  In practice, if a lookup is slow, we abort and mark evidence stale.  Remember, the user isn’t waiting: if evidence arrives too late, we simply *flag and continue*.  If the system ever finds Tier-1 taking too long under load, it can dynamically disable optional checks.  This trade-off (prefer missed detections over SLA breaches) is by design: as one AI guide notes, “push for speed without understanding [cost/accuracy], and you either overspend or simplify until it’s faster but less useful”.  ControlPlane.ai opts to simplify (by skipping a slow check) rather than ever block the user.

**Q: “What about the 5% tolerated false-positive rate on blocks? Users won’t accept random rejections.”**  
The 5% cap is carefully controlled: it applies to *true* blocks (e.g. PII or policy violations).  All other issues default to *soft flags or edits*.  In early deployment, we monitor user behavior: if they start ignoring or disabling the gate, we dial back.  The system is designed so that users only see a block for very clear violations.  For everything else we might show an annotated answer (“edited for clarity” or “see below for sources”), which is less abrasive.  And since we’re continuously in shadow, we detect if even 5% is harming engagement.

**Q: “Couldn’t an attacker just trick the gating signals or exploit soft filters?”**  
Any deterministic filter (PII regex, tool permission lists) could be probed, but these are hardened (blocks on precise PII match, tools require auth).  For classifier-based checks, we tune thresholds conservatively.  Also, policy violations can be externally audited from the audit trail.  In essence, ControlPlane.ai does not promise absolute prevention of a malicious user, but it ensures there is *evidence* for every decision.  The independent control plane architecture itself (as industry analysis argues) must be trustworthy and separate from the model vendor; if needed, auditors can examine the log to verify a claimed violation.  Finally, nothing stops us from updating rules: if new attack patterns appear (e.g. steganographic PII), we can patch the regex or add a classifier rule without retraining the whole system.

In summary, this architecture emphasizes **practicality over perfection**.  It leverages multiple simple detectors (with known failure modes) and careful monitoring to catch errors without slowing down the AI.  The design has been stress-tested conceptually against known pitfalls of LLM safety (hallucinations, biases, leakage) and against performance constraints.  Continuous shadow evaluation and human oversight serve as safety valves, ensuring that even in adversarial conditions the system can adapt or fail fast.  

**Sources:** Recent AI control-plane designs and evaluations inform this architecture: ResearchLoop’s evidence-gating framework; quality-gate studies highlighting evidence coverage as key; industry reviews on AI control plane separation; PII and content-safety best practices; fairness metrics surveys; and deployment guides for latency and shadow testing.  These underscore that a **tiered, evidence-driven control plane** can catch real-world AI risks within strict latency budgets, unlike monolithic or one-dimensional approaches.