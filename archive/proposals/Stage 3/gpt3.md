# ControlPlane.ai Positioning and Narrative

## 1. Single Sharp Insight  
AI outputs must be treated as *actionable claims* with attached evidence, not just text to be scored. ControlPlane makes evidence a first-class runtime constraint – each claim in a response is bound to exactly the sources the model saw, and we **gate on that evidence** rather than on an opaque score. This means we stop blind leaps-of-faith (hallucinations or unsafe actions) at the source, instead of hoping a second model or threshold will catch them.

## 2. Current Market Approaches (and Why They Fail)  
- **LLM-as-judge** – Running a second LLM to “critique” the first is expensive and slow. It shares the same blind spots (a model tends to validate its own outputs) and adds hundreds of milliseconds of latency. In practice it’s either too coarse or too costly for real-time gating.  
- **Static rule/keyword blocklists** – Fixed lists or one-time guardrail models might catch simple issues, but by Gödel-style logic they can never cover all adversarial inputs. Real attackers constantly find workarounds (prompt injections, refusal-then-comply hacks) beyond any finite list. Once deployed, “deploy-and-forget” guards quickly become obsolete.  
- **Post-hoc observability** – Dashboards and logs can flag patterns after the fact (e.g. after harmful output), but they don’t **prevent** anything. Being purely retrospective, they have no real-time enforcement. They only tell you something bad happened – not stop it.  
- **Confidence thresholding** – Trusting the model’s own confidence or a simple probability (via its softmax or “are you sure?”) is unreliable. In fact, LLMs are *over-confident* in their hallucinations. Calibration efforts help only a little; models still “blindly trust” wrong answers. You end up either blocking too much or missing dangerous claims.  
- **Simple RAG checkers** – RAG (retrieval-augmented generation) can ground some facts, but even RAG answers still hallucinate. As PaperTrail shows, errors “persist even in RAG systems”. Merely citing sources is not enough if you don’t *verify* that the answer is supported by those sources.  
- **Composite risk scores** – Collapsing all concerns into one number (toxicity + factuality + etc.) is not actionable. It hides trade-offs: a harmless but expensive answer can look the same as a fast but slightly unsafe one. Users and engineers can’t act on one opaque score because it lacks context. 

Each of these popular patterns trades off detail or agility. We need a fundamentally different approach.

## 3. Positioning Statement  
ControlPlane.ai is a **real-time control plane for AI**: it treats every model response as a set of claims requesting permission to act, and requires verifiable evidence for each claim. We bind outputs to the *actual context* (provenance captured at assembly time) and enforce per-claim checks on correctness, cost, and safety. In other words, rather than trusting a single risk score or second-guessing with another LLM, we demand *proof* for what the model says. This matters now because generative AI is advancing faster than our governance: static filters and black-box scores regularly fail, but enterprises still need strong, low-latency control over LLM actions. ControlPlane delivers provable trust: an evidence-anchored pipeline that moves beyond guesswork to deterministic policy enforcement.

## 4. Differentiation Table

| Common Approach                                   | How ControlPlane.ai Is Fundamentally Different            |
|:-------------------------------------------------|:----------------------------------------------------------|
| **Monolithic LLM judge or safety model:** one big model or score that judges an output. | **Evidence-Gated Micro-services:** no second generative model. We decompose outputs into claims, attach real sources, and run small deterministic checks (regex/NER, classifiers) on them. Decisions are rule-based on *evidence presence*, not on another LLM’s guess. |
| **Static blocklists & guardrails:** fixed rules or system prompts intended to always catch bad content. | **Dynamic, Runtime Control:** accepts that no finite ruleset can cover all cases. Instead, we continuously verify evidence and adapt (e.g. shadow mode updates) and never “freeze” safety in code or prompts. |
| **Single composite risk score:** all axes collapsed into one “risk” number. | **Multi-Axis, Per-Claim Decisions:** we split safety into performance (hallucination), cost (efficiency), and responsibility (bias/PII) axes. Each claim is evaluated on each dimension. The policy is a DAG of rules per axis, so we can finely control trade-offs (block vs. edit vs. escalate) instead of lumping them together. |
| **Reactive dashboards & auditing:** tools that log/alert problems after generation. | **Proactive Gatekeeping:** a streaming pipeline with speculative release. Tier‑1 checks run in <50ms to allow safe early tokens; deeper evidence checks run asynchronously. We fix or flag issues before they reach the user (or quickly repair them) rather than just report them later. |
| **One-shot filtering vs. action:** once the model answers, filter or dump. | **Control Plane (“checks & controls”):** we treat each answer as an *operational request*. The policy can *change* the answer mid-stream (surgical edits), escalate with a structured report, or selectively block just the unsupported parts. It’s not a final veto from afar, but an integrated, evidence-backed governance layer. |

## 5. Narrative Spine (3-minute video)

- **0:00–0:30 — Opening Hook:**  
  *“Generative AI can sound confident and credible – until it isn’t. When an AI ‘knows’ something, that knowledge is just a guess unless it’s backed by proof. What if your AI’s answers were *requests for permission* that needed evidence before taking action?*” (Show a provocative example or statistic on costly AI error).  

- **0:30–1:15 — Problem + Reframe:**  
  - The problem: current safety tools fail to catch real issues in real time. We mention quick examples: “LLM-as-judge and fancy risk scores are **too slow** and still **hallucinate**. Static filters are **always one step behind** bad prompts.”  
  - Reframe: “We realized the mistake is treating AI outputs as mere text. Instead, *each output is a set of action-items* needing permission. We flip the burden of proof: **default = not allowed**. Only with evidence do we let the AI proceed.”  

- **1:15–2:15 — Core Mechanism + 3-Axis Demo:**  
  - **Evidence Capture:** “At prompt time we record every piece of evidence the model sees (documents, tool outputs, etc.). When it speaks, we split its answer into claim spans.”  
  - **Performance Axis:** “We check each claim’s *Evidence Coverage Score* (how many claims have real sources) and *Claim-Proof Alignment*. If the model *confidently* makes a claim with low coverage, that’s a red flag.”  
  - **Cost Axis:** “We measure waste too – the *Marginal Cost per Useful Token* and if the user keeps re-asking the same question. If an answer rambles or loops, the cost watcher knows it.”  
  - **Responsibility Axis:** “We instantly run small fast detectors on the token stream for PII, obvious toxicity, and bias parity. Only PII matches cause hard blocks; others just soften or flag.”  
  - **Action:** “Each of these axes feeds rules in a **Policy DAG**. E.g., low evidence = block or rewrite, high waste = downgrade or alert, toxic phrase = edit in place. The key is *per-claim, per-axis decisions*. The video could sketch a flow: user query → model answers → claim extractor → evidence builder → policy rules → block/edit/escalate/pass.”  

- **2:15–2:45 — Decision Logic / No Over-blocking:**  
  - “Notice: it’s *not* all block vs. allow. Actions include Edit (fix it), Escalate (human review or alternate path), or Pass. We only ever Block on deterministic facts (e.g. exact PII leak or zero evidence). Everything else starts as a soft flag or rewrite.”  
  - “We built in fallbacks: each rule has a latency budget, so if it’s running late it will defer to a lighter action (e.g. escalate vs block). We’d rather release a plausible answer and fix it in the background than freeze user experience. Most checks happen asynchronously (Tier‑2 after initial answer, Tier‑3 offline).”  
  - “Importantly, we continuously monitor ourselves. Shadow-mode dual-emits let us see how many issues we missed or mis-handled. If human overrides spike, we auto-roll-back policy changes. We prefer **human trust** over false positives.”  

- **2:45–3:00 — Closing (Hard Landing):**  
  - “In short: we’ve changed the lens. We don’t “score text”; we **control actions**. ControlPlane ties every claim to proof. It’s the only way to truly govern AI at scale without grinding it to a halt. If you want **trust that’s provable**, not hopeful, ControlPlane.ai is the inevitable answer.”  
  - (Closing tagline on screen, e.g. “ControlPlane.ai – Because AI actions need permission.”)

## 6. Claims We *Refuse* to Make  
- **100% Coverage or Safety:** We do *not* claim we catch *every* hallucination or adversarial trick (impossible by theory). Occasional false negatives will happen, and human-in-the-loop oversight is part of the design.  
- **Magical AI Fix:** We are not a new generative model or a self-healing system for all AI ills. We explicitly avoid “LLM-as-judge” or vague AI-reasoning claims. We do *not* claim to **fix the base model**; we simply police its outputs with logic and evidence.  
- **Zero Overhead:** We will not promise 0ms overhead or unlimited scale. We acknowledge our gating adds latency (which we minimize via tiering) and some extra compute (which we track with our cost signals). We don’t claim a free lunch – just a smart one.  
- **No Human Needed:** We won’t say this replaces human governance or that it makes review obsolete. Complex or new cases still escalate. We only claim to automate the **easy, verifiable parts**; judgment calls stay human.

## 7. Strongest Narrative Risk and Correction  
- **Risk:** The pitch could easily sound like “yet another AI safety tool.” Judges might think we’re just adding one more scanner or LLM-evaluator to the pipeline. This would flatten our value to “an alternative guardrail system,” missing our core novelty.  
- **Correction:** We must *constantly* emphasize the control-plane paradigm. Stress phrases like *“claim=action request”*, *“evidence primitive”*, and *“per-axis gating”*. When describing what we do, avoid generic buzzwords like “safety” or “governance” without context. Instead say: “we built a low-level control system that ties claims to proof and enforces policy rules *at runtime*, rather than relying on static lists or a catch-all risk model.” A key line might be:  
  > “This isn’t an LLM filter – it’s an action permissioning engine. We don’t just guess whether an answer is safe; we *verify each fact with the very data the model had*, and then decide in code. It’s enterprise-grade control, not guesswork.”  

  By framing ControlPlane.ai as a *systems architecture* (with latency budgets, agent roles, evidence graphs) rather than a “security bolt-on,” we steer judges away from thinking it’s a trivial add-on or hype. (If they ask, our response is: “Think of us like the CPU’s privilege mode for AI: we enforce every operation can prove its legitimacy.”) In other words, keep pounding the theme of **evidence-backed, multi-agent control**, and avoid falling back on standard “AI safety” tropes.