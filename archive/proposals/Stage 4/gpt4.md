1. **Single Sharp Insight:** Every AI response is a set of claims asking for permission to act – not a paragraph to trust blindly. ControlPlane forces each claim to *earn* its evidence (captured at context assembly), so overconfident, polished hallucinations become costly “brand debt”.  

2. **What the market currently does (and why it fails):** Today’s solutions focus on scoring or post-hoc checks (e.g. LLM-as-judge, static filters, dashboards).  These fall short.  Alignment/RLHF can’t prevent hallucinations. LLM-as-judge monitors “are not infallible” and share the model’s blind spots.  Confidence thresholds or single composite risk scores often miss confident falsehoods or hide actionable details.  Static lists and rules (regex or blocklists) are brittle and easily bypassed. Dashboards and reports only diagnose problems after the fact, not prevent them. 

3. **Positioning Statement:** *ControlPlane.ai is the first true AI control plane: a real‐time enforcement layer that treats every output as a bundle of claims to be verified. It binds each claim to the source evidence (with ACLs and hashes tracked at context assembly) and gates actions on provable truth. By inverting the burden of proof (default=UNSUPPORTED) and managing performance, cost, and safety on equal footing, ControlPlane stops trusted-seeming errors before they can become “brand debt.”*  

4. **Differentiation Table:**

   | Common approach                  | ControlPlane.ai (Different)                       |
   |----------------------------------|--------------------------------------------------|
   | **LLM-as-judge / composite risk:** a single model or score judges outputs.  | **Evidence-gated policy:** deterministic rules per claim.  No new LLM judge or opaque score – each claim must cite its captured evidence. |
   | **Threshold/blocklist:** static filters or confidence cutoff blocks content. | **Dynamic proof-binding:** every claim links to context (ACL+hash); default=UNSUPPORTED unless proven.  No static blocklists – gates require real evidence. |
   | **Safety dashboard:** post-hoc observability of issues.    | **Inline enforcement:** runtime gating (Tiered, synchronous or async) actively blocks/edits in-flight.  Also publishes our own false-negative rate per route. |
   | **One-size models:** a large safety model or debate chains.  | **Policy DAG:** a lightweight rule DAG (Tier-1/Tier-2/Tier-3) decides Block/Edit/Escalate/Pass by blast radius vs severity.  Fast rules first, slow checks only flag or edit (never guess). |
   | **Draconian blocking:** any flag leads to outright block, training users to disable it. | **Surgical response:** soft edits or human escalation by default, with hard block only on indisputable evidence (e.g. exact PII match).  Optimistic streaming with small hold-back. |

5. **Narrative Spine (3-minute video):**  
   - **0:00–0:30 Opening hook:** Start with a shock scenario (e.g. CFO sees AI confidently execute a wrong transaction). Explain how customer trust is lost not by mistakes but by *confident* mistakes. Introduce the notion of “brand debt” from unchallenged AI claims.  
   - **0:30–1:15 Problem + reframe:** Say: everyone today tries LLM-judges or black-box risk scores to catch problems, but “the system *didn’t* fail – it was never asked to prove anything.”  Cite that RLHF alone can’t stop hallucinations. Emphasize: *We think differently: AI outputs are *permission requests*, not truths.*  
   - **1:15–2:15 Core mechanism + 3-axis demo:** Show the STEP→SPAN→CLAIM→ACTION graph. Explain how each claim is tied to its evidence (captured outside the model). Illustrate the three axes: **Performance** (Evidence Coverage Score, calibration gap), **Cost** (wasted tokens, retries), **Responsibility** (PII/harm/bias). Use a mini demo: e.g. an AI refund request answer is decomposed into claims, each checked. Show how evidence-gated rules operate per claim.  
   - **2:15–2:45 Decision logic / why it doesn’t over-block:** Introduce the Blast-Radius × Severity matrix. Explain Tier-1 (<50ms) vs Tier-2 (≤2s) checks. Emphasize hard-gate only on proven violations, with most flags handled by soft-edit or human review. Stress that slower signals can’t block mid-stream – they only append audit logs or trigger edits later. Convey that this avoids overblocking and keeps latency within budget.  
   - **2:45–3:00 Closing line:** Summarize that this gives a true AI control plane: evidence-bound, measurable, and lean. End with the tagline (largest text): **“It used to be a bad paragraph. It is now an executed transaction.”** 

6. **What we deliberately refuse to claim:** (bold claims to *avoid*) 
   - “100% error-free” or “zero false-negatives/no misses.” 
   - “No human oversight needed ever” or a magic bullet.  
   - “Zero latency overhead” (we acknowledge small trade-offs for safety).  
   - “Our model fixes all possible AI risks” (we target observable violations, not unbounded guarantees).  

7. **Strongest narrative risk + correction:**  
   - *Risk:* Judges might dismiss this as just “another AI safety/guardrail tool,” expecting more ML hype. It could blend in with existing products.  
   - *Correction:* Emphasize the systems angle: we’re *not* a new neural model or simple checklist. Highlight our evidence-first architecture and metric-driven discipline. Stress we solve business-meaningful axes (performance/cost/trust) with explicit rules and audit logs. Call out that this is an inevitable “runtime OS” for AI (think WAF or firewall analogy from) – a fundamentally different substrate, not just marketing.  

### Slide 1 — The Reframe  
- **Exact Headline:** AI answers = claims requesting permission, not facts to trust.  
- **Primary Visual:** A horizontal flow diagram: *Step (user intent)* → *Span (statement pieces)* → *Claim (each with attached evidence source)* → *Action*. Each Claim node is linked to an evidence document (ACL+hash icon). An Action node is gated (lock icon) based on evidence. The **Step→Span→Claim→Action** pipeline is front-and-center.  
- **Supporting text / bullets:** (4 short lines)  
  - Bind each claim to its evidence captured at context assembly (with ACL & hash tracking).  
  - Inverted burden of proof: default=UNSUPPORTED unless context proves the claim.  
  - Treat each output as an action-request: hard-gate on actions, not on words.  
  - Evidence-guided policy enforces trust: “the system didn’t fail; it was never asked to prove anything.”  
- **Footer line (if any):** *“The system didn’t fail. It was never asked to prove anything.”* (smaller text at bottom)  
- **Design notes:** The **Step→Span→Claim→Action** pipeline graphic dominates the slide. Keep text minimal around it. Emphasize the evidence link and lock/gate on the Action node. The headline and one-sentence footer can be in smaller font; the flow diagram is the focal point.  

### Slide 2 — The Decision System  
- **Exact Headline:** The ControlPlane Decision System  
- **Primary Visual:** A **Blast Radius × Severity matrix** dominates the center (4 rows labeled R0–R3; 3 columns as severity levels or actions). Each cell is color-coded with the resulting action (Pass/Edit/Escalate/Block). For example, high severity & high blast radius leads to Block. The matrix is annotated: “Allow = green, Edit=yellow, Escalate=orange, Block=red”.  
- **Supporting elements (actuators, latency principles):**  
  - **Tier-1 (sync ≤50ms):** deterministic gates (PII regex, exact-match safety, token cap) → immediate Pass or Block while streaming.  
  - **Tier-2 (async ≤2s):** Evidence Builder + Watchers attach proofs, compute ECS/Alignment and MCUT, then may Edit or Escalate post-emit.  
  - **Tier-3 (offline):** Analytics agents run bias parity checks, cost audits, shadow-mode evals (≤60s).  
  - **Decision logic:** Director agent resolves each rule (signal+threshold) in the DAG. If evidence is missing, that rule just flags (no guess). Slow checks degrade to Escalate/Flag to avoid latency issues.  
- **Design notes:** The matrix is the focal point, big and central. Use clear labels R0–R3 (blast radius) and actions. Surrounding text (tier bullets) should be secondary, small. Show one example (e.g. “R3: Block on high severity”) to illustrate. The idea: fast rules first (Tier-1), deeper checks in background. Keep the layout clean (matrix plus 3–4 bullet lines, not a busy flowchart).  

### Slide 3 — Why This Is Different (and Believable)  
- **Exact Headline:** Why This Is Different (and Believable)  
- **Left side content (What we refuse):**  
  - No LLM-as-judge or opaque composite risk score.  
  - No single giant safety model; no static regex/blocklist-only approach.  
  - No overblocking on soft flags (we don’t block first and ask questions later).  
  - No “guessing” without evidence (we don’t allow unverified claims to pass).  
- **Right side content (What we publish / guarantee):**  
  - Publish per-route false-negative rate (continuous self-audit, 5% shadow mode).  
  - Evidence-first gating: each claim is anchored by a captured source (ACL+hash) for full traceability.  
  - Hard block **only** on deterministic violations (e.g. exact PII match, ECS=0). Soft-edit or human escalation otherwise.  
  - Transparent policy updates and analytics (bias parity, cost) with audit logs of every decision.  
- **Closing line:** *(largest text, centered bottom)* **“It used to be a bad paragraph. It is now an executed transaction.”**  
- **Design notes:** Split the slide into two clean columns under the headline. Left column titled “What we don’t claim/do,” right column “What we guarantee/publish.” Use concise bullet phrases (no long sentences). The closing line should be the boldest element – placed prominently (e.g. bottom center) as the kicker. Avoid any extra graphics; focus on clear contrast between left and right points and the final tagline.