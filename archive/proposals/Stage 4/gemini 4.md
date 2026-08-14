### Slide 1 — The Reframe

#### Exact Headline

An AI response is not text—it is an unverified request to act.

#### Primary Visual

A central contrasting workflow diagram split horizontally into two stark paths:

* **Top Path (Faded Gray — "Legacy Observability"):**

$$\text{Prompt} \longrightarrow \text{Model Output} \longrightarrow \text{LLM Judge / Dashboard}$$



*(Annotated: "It used to be a bad paragraph.")*
* **Bottom Path (High-Contrast Cyan/White — "ControlPlane Engine"):**

$$\text{Context Assembly (ACL + Hash)} \longrightarrow [\text{STEP} \rightarrow \text{SPAN} \rightarrow \text{CLAIM} \rightarrow \text{ACTION}]$$



*(Annotated: "It is now an executed transaction.")*

#### Supporting text / bullets

* "The system didn’t fail. It was never asked to prove anything."
* **Provenance Captured Outside Model:** Binds context source, ACL permissions, and cryptographic hash at assembly.
* **Inverted Burden of Proof:** Default state for every generated claim is `UNSUPPORTED`.
* **Unified Graph:** Performance, cost, and responsibility are three concurrent reads of the exact same execution trace.

#### Footer line

ControlPlane shifts oversight from post-hoc output scoring to execution-time claim validation.

#### Design notes

The contrast between the two paths must dominate. The top path uses muted, low-opacity gray tones to visually represent outdated paradigms. The bottom path uses bold white text with sharp cyan connectors. The annotations (*"bad paragraph"* vs *"executed transaction"*) must be positioned directly beside their respective output terminals.

---

### Slide 2 — The Decision System

#### Exact Headline

Dynamic execution control: Blast radius governs verification budget and latency.

#### Primary Visual

A sharp $4 \times 4$ **Decision & Actuator Matrix** dominating 70% of the slide canvas:

| Blast Radius ($R_n$) | PASS | UNSUPPORTED | ACL VIOLATION | LOOP / DEAD COMPUTE |
| --- | --- | --- | --- | --- |
| **$R_0$: Pure Text Stream** | Stream Pass | Surgical Redaction | Redact & Flag | Kill Span |
| **$R_1$: Internal Query** | Execute Pass | Hold & Re-verify | Hard Block | Terminate Step |
| **$R_2$: External Comm.** | Execute Pass | Inline Redact | Hard Block | Terminate Step |
| **$R_3$: State Transaction** *(e.g., ₹1,84,000 Refund)* | Hard Gate Pass | Hard Block | Hard Block & Escalate | Kill & Dump Graph |

#### Supporting elements

* **Hard Action Gate ($R_3$):** Total execution lock on financial or state changes until claim hash matches source provenance.
* **Optimistic Text Stream ($R_0$):** Passes tokens immediately while holding back a short 150ms buffer to evaluate low-risk claims without killing user UX.
* **Surgical Edit:** Redacts specific ungrounded sub-claims (e.g., Clause 7.2 override) while permitting verified text to pass.
* **Evidence Packet:** Escalation exports a structured graph snapshot (`STEP → SPAN → CLAIM`) directly to human operators.

#### Design notes

The matrix must be the unambiguous focal point. Color-code the cell actions strictly: Green tint for *Pass*, Amber for *Surgical Edit/Hold*, Solid Dark Red for *Hard Block/Kill*. Avoid cluttering the matrix with long descriptions; use the concise actuator terms shown above.

---

### Slide 3 — Why This Is Different (and Believable)

#### Exact Headline

Deterministic integrity over probabilistic promises.

#### Left side content (What we refuse)

**We Deliberately Refuse:**

* **"100% Hallucination Elimination":** We enforce evidence provenance and gate execution, not alter auto-regressive model weights.
* **Secondary LLM Judges:** No chaining slower LLMs to evaluate faster LLMs (doubling cost and latency on the same failure surface).
* **Zero-Latency Marketing:** Verification requires compute; budget is spent strictly proportional to blast radius ($R_0–R_3$).
* **Opaque Composite Scores:** No averaging safety, cost, and drift into a meaningless single scalar.

#### Right side content (What we publish / Credibility)

**What ControlPlane Publishes Live:**

* **Per-Route False-Negative Rate ($FN_{\text{route}}$):** Published directly by the plane on every route.
* **Context Provenance Logs:** Cryptographic verification status for every context-assembly hash.
* **Dead-Compute Traces:** Exact token waste mapped backward to the originating ungrounded span.
* **Audit-Ready Evidence Packets:** Deterministic proof chains for every blocked or escalated transaction.

#### Closing line

Stop reading what your AI generated after it acts. Control what it is permitted to execute before it fires.

#### Design notes

Use a strict two-column layout separated by a thin vertical rule. The left column ("What We Refuse") uses strike-through or muted red accent headers to signal discipline. The right column ("What We Publish") uses clean tabular bullet points. The closing line must span the entire width of the slide footer in bold, 32pt typography—making it the visual anchor of the final slide.

---

### Tension & Resolution Flag

* **Tension:** The deep system mechanics (ACL hashes, graph walking, $R_0–R_3$ blast radiuses, optimistic hold-backs) risk overwhelming a 3-slide format designed for an 8-second judge scanning time.
* **Resolution:** Content density was reduced by converting explanatory prose into an explicit $4 \times 4$ visual matrix on Slide 2 and a strict binary contrast ("Refuse" vs. "Publish") on Slide 3. Technical depth is conveyed through system terminology (e.g., $FN_{\text{route}}$, $R_0–R_3$, ACL hashes) rather than lengthy descriptions.