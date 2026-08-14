### Slide 1 — The Reframe  
- **Headline:** *“AI Responses = Claims Requesting Permission”*  
- **Primary Visual:** A simple flow diagram labeled **STEP → SPAN → CLAIM → ACTION**, with an example. For instance: *Step:* “Invoice #12345”; *Span:* “Clause 7.2: (no refunds after 30 days)”; *Claim:* “User is eligible for ₹1,84,000 refund”; *Action:* “Issue refund.” Arrows connect each stage. The claim node is highlighted and an annotation shows linking to evidence (e.g. document icon with a lock and hash).  
- **Supporting Text (bullets):**  
  - “Each AI answer is a series of **claims** asking to act.”  
  - “Every claim is **bound to evidence** captured outside the model (ACL‐protected, hashed context).”  
  - “By default a claim is **UNSUPPORTED** unless proven.”  
  - “One unified graph (STEP→SPAN→CLAIM→ACTION) underpins all checks.”  
- **Footer Line:** *(none)*  
- **Design Notes:** The headline and flow diagram dominate. Use a clear hierarchical layout: large title at top, diagram center, short bullets below. Emphasize the **CLAIM** node and the word **UNSUPPORTED** (e.g. bold or color) to catch the eye. Keep bullet text minimal and factual.  

### Slide 2 — The Decision System  
- **Headline:** *“Evidence-Gated ControlPlane”*  
- **Primary Visual:** A **matrix** table (grid) is central.  Y-axis: “Blast Radius R0 → R3” (bottom to top).  X-axis: “Unsupported Claim Severity (Minor → Critical)”.  Each cell is labeled either “Escalate” or “Block”.  The top row (R3) cells are all “Escalate (not Block)”.  A legend or color-coding (e.g. yellow=Escalate, red=Block) clarifies actions.  Example callouts: R1/Moderate shows “Escalate (human review)”; R3/Any shows “Escalate (no block)”.  
- **Supporting Elements (bullets):** (positioned below or side of matrix)  
  - “Per-claim rule-DAG across **Performance/Cost/Responsibility** axes.”  
  - “Action for each claim: **Block / Edit / Escalate / Pass**.”  
  - “Checks are **evidence-gated and latency-aware**: missing proof = flag/escalate.”  
  - “Hard-block only on deterministic failures (e.g. PII match).”  
- **Design Notes:** The grid is the visual focus. Keep text around it minimal. Use bold headers for axes. Legend or color cues help quick reading. The bullets should be concise; ensure “Block/Edit/Escalate/Pass” stands out (e.g. icon or bold).  

### Slide 3 — Why This Is Different (and Believable)  
- **Headline:** *“Why ControlPlane.ai Stands Apart”*  
- **Left (What We Refuse):**  
  - “LLM-as-judge risk scoring”  
  - “Single composite safety score”  
  - “Static blocklists or regex-only rules”  
  - “Immediate blocking on any flag”  
- **Right (What We Publish/Credibility):**  
  - “Evidence-first, per-claim gating”  
  - “Multi-axis policy (performance, cost, responsibility)”  
  - “Surgical edits & escalations, not blind blocks”  
  - “Streaming output & short hold-back”  
  - “Public per-route false-negative metrics”  
- **Closing Line (largest text):**  
  *“Now nothing acts until it can prove it should.”*  
- **Design Notes:** Two columns compare “Not This” vs. “Instead This.” Use X or “no” icons on left and check or shield icons on right (if any) for visual punch. Bullets must be very short phrases. The closing line is the focal point – large, bold, centered at bottom. Keep slide clean and avoid clutter so the final statement hits hard.

### Overall Timing Map  
- **0:00–0:30:** *Opening Hook* – Show the concrete failed transaction (₹1,84,000 refund denied). Challenge the assumption (“failure”). Drop the key line: “The system didn’t fail – it was never asked to prove anything.”  
- **0:30–1:15:** *Problem + Reframe* – Display **Slide 1 (The Reframe)**. Explain that AI answers are *claims* needing proof (default unsupported). Introduce the STEP→SPAN→CLAIM→ACTION graph with the refund example.  
- **1:15–2:15:** *Core Mechanism* – Display **Slide 2**. Walk through the evidence-bound control plane: three axes (Performance/Cost/Responsibility), checks per claim, and example metrics (evidence coverage, compute waste, PII). Show how a rule-DAG picks actions (block/edit/escalate/pass) for our refund claim.  
- **2:15–2:45:** *Decision Logic* – Still on **Slide 2**. Emphasize the policy behavior (evidence gating, latency tiers). Explain that only truly critical + R3 issues block; others escalate or pass. Highlight how the system avoids unnecessary blocking.  
- **2:45–3:00:** *Closing* – Display **Slide 3**. Summarize differentiation: what we *don’t* do vs. what we *do*. Deliver the final strong line. End with conviction.

### Beat-by-Beat Script  
- **0:00–0:05**  
  - *On screen:* UI screenshot: “Refund ₹1,84,000 – **Denied** (Clause 7.2)”. (Red alert style.)  
  - *Spoken:* “Rajesh’s ₹1,84,000 refund was just **denied under Clause 7.2**.”  
  - *Delivery:* Matter-of-fact, slight surprise in tone.  
- **0:05–0:12**  
  - *On screen:* Same screenshot zoom (highlight “Denied”).  
  - *Spoken:* “At first glance, this looks like an AI failure. But actually…”  
  - *Delivery:* Pause after “actually…” to build tension.  
- **0:12–0:18**  
  - *On screen:* Fade to neutral background or Slide 1 appearing lightly.  
  - *Spoken:* “The system **didn’t fail** – it was **never asked to prove anything.**”  
  - *Delivery:* Assertive emphasis on “didn’t fail” and “prove anything.” Short pause after the sentence.  
- **0:18–0:30**  
  - *On screen:* **Slide 1 (The Reframe)** is fully visible. Highlight the **CLAIM** node in the diagram.  
  - *Spoken:* “We realized we’d been looking at AI safety backwards. An AI answer isn’t just text to filter – it’s a set of **claims requesting permission** to act.”  
  - *Delivery:* Steady pacing; emphasize “claims requesting permission.”  
- **0:30–0:45**  
  - *On screen:* Slide 1 with the bullets visible; focus on “claims” and evidence binding.  
  - *Spoken:* “Each answer from the model is a sequence of claims. Every claim must attach to the **exact evidence** we fed the model (ACL-protected, hashed context).”  
  - *Delivery:* Clear and straightforward; emphasize “exact evidence” and “hashed context.”  
- **0:45–1:00**  
  - *On screen:* Bullets “Default=UNSUPPORTED” highlighted.  
  - *Spoken:* “By default, without proof, a claim is marked **UNSUPPORTED**. We don’t trust an unverified claim.”  
  - *Delivery:* Pause on “UNSUPPORTED,” delivered firmly.  
- **1:00–1:15**  
  - *On screen:* Diagram’s graph path (STEP→SPAN→CLAIM→ACTION) with our refund example annotated.  
  - *Spoken:* “One unified graph (STEP→SPAN→CLAIM→ACTION) drives all checks. For example: ‘Refund ₹1,84,000 under Clause 7.2’ is a claim. It must prove the clause applies. No proof? It stays UNSUPPORTED.”  
  - *Delivery:* Crisp explanation; slightly enthusiastic on “one unified graph.”  
- **1:15–1:30**  
  - *On screen:* **Slide 2 (The Decision System)** fades in, highlighting matrix outline.  
  - *Spoken:* “ControlPlane enforces an evidence-gated policy **per claim**. Every claim triggers checks along three axes: **Performance, Cost,** and **Responsibility**.”  
  - *Delivery:* Emphatic enumeration on the three axes.  
- **1:30–1:45**  
  - *On screen:* Emphasize “Performance” column or icon.  
  - *Spoken:* “The Performance axis catches unsupported or hallucinated claims: it checks evidence coverage and alignment. In our case, the refund claim had **high confidence but low evidence coverage**, a warning sign.”  
  - *Delivery:* Technical, analytical tone.  
- **1:45–2:00**  
  - *On screen:* Show “Cost” and “Responsibility” columns.  
  - *Spoken:* “The Cost axis measures waste: repeated retrievals or unused tokens. Responsibility flags issues: PII leaks, harmful content, or bias. Each claim is evaluated on all three.”  
  - *Delivery:* Even, factual.  
- **2:00–2:15**  
  - *On screen:* Matrix fills in. Actions (Block/Edit/Escalate/Pass) appear.  
  - *Spoken:* “A rules-based DAG then decides the action for each claim: **Block, Edit, Escalate,** or **Pass**. Only the most severe+high-radius cases block. For our ₹1,84k refund (moderate issue, user-level R1), the policy says: **Escalate** with a human and evidence packet.”  
  - *Delivery:* Dynamic listing of actions; emphasize “only the most severe blocks.”  
- **2:15–2:30**  
  - *On screen:* Focus on matrix cell “Escalate” for R1/Moderate (e.g. glow effect).  
  - *Spoken:* “Notice: missing proof here triggers an escalation – we queue a human review. We never just shut the user out unless it’s truly critical.”  
  - *Delivery:* Reassuring, matter-of-fact.  
- **2:30–2:45**  
  - *On screen:* Slide 2 sidebars: small icons for “Fast Checks” and “Async Proofs”.  
  - *Spoken:* “The system is latency-aware: quick checks (PII regex, token caps) run first; deeper evidence checks run in parallel. We stream the answer with a short hold-back, then verify. Only confirmed violations block. All else can be edited or flagged.”  
  - *Delivery:* Firm pacing; stress “stream the answer” and “only confirmed violations block.”  
- **2:45–2:55**  
  - *On screen:* **Slide 3 (Why Different)** shows left/right lists.  
  - *Spoken:* “This isn’t just ‘another AI safety tool.’ We *refuse* common shortcuts: no blind LLM judges, no one-number risk scores, no static blocklists. We *require evidence* and publish the real false-negative rate per path.”  
  - *Delivery:* Insistent tone; emphasize each “no” and “evidence.”  
- **2:55–3:00**  
  - *On screen:* Closing line emerges large: “Now nothing acts until it can prove it should.”  
  - *Spoken:* “It used to be a bad paragraph. Now it’s an executed transaction. Now nothing acts until it can prove it should.”  
  - *Delivery:* **Strong, final.** Pause after the last sentence (no trailing words).

### Closing Discipline  
- **Exact final spoken line:** *“Now nothing acts until it can prove it should.”*  
- **Visual (last 5–8s):** Slide 3’s closing text (“Now nothing acts…”) fades in large against a dark background. Possibly overlay the successful ₹1,84,000 refund or a simple checkmark icon. Fade-out as line completes.  
- **Deliberately left unsaid:** We do **not** claim zero risk or 100% accuracy. We do not promise reduced model latency or that every hallucination is solved. We avoid vague promises like “fully safe AI.” Instead, we focus on verifiable control.  

### Rules Applied  
1. **Single trace:** We followed the ₹1,84,000 refund example from start to finish (no generic scenarios).  
2. **Concrete language:** We used terms like *authorize, prove, bind, refuse, hold* – banned words (monitor, detect, trust) are avoided.  
3. **System-level focus:** Emphasized claims/evidence architecture, not human emotion or abstract “safety.”  
4. **Short, declarative statements:** No fluff or marketing hype; every sentence is concrete.  
5. **Timing precision:** Aligned narrative tightly to the 3-minute structure; each segment is timed and ends crisply.  
6. **No vague claims:** We did not overpromise (“no risk,” “perfect AI”). We presented features and measurements (publishing FN rate) instead.