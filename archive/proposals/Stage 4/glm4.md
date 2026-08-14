### Slide 1 — The Reframe
- Exact Headline (max 12 words)
  An AI response is not text. It is a request to act.
- Primary Visual (precise description of what appears in the centre)
  A split-screen visual. Left: a blurred paragraph of generated text. Right: that same paragraph decomposed into a directed graph: STEP → SPAN → CLAIM → ACTION. A glowing lock icon sits on the ACTION node.
- Supporting text / bullets (maximum 4 short lines)
  - Evidence (source, ACL, hash) captured outside the model at context assembly.
  - Default state for any claim: UNSUPPORTED.
  - The model must graph-traverse to provenance to earn a passing verdict.
  - Three axes (Performance, Cost, Responsibility) are three reads of one graph.
- Footer line (if any)
  "The system didn’t fail. It was never asked to prove anything."
- Design notes (what must dominate, what must stay secondary)
  The graph on the right must dominate the center. The blurred text on the left is visually suppressed (muted colors, lower opacity) to emphasize the death of "text scoring." The bullets must be high-contrast but ruthlessly short. 

### Slide 2 — The Decision System
- Exact Headline
  Enforcement: Blast Radius × Verdict Severity
- Primary Visual (the matrix must be the dominant object)
  A 4x3 grid acting as the decision matrix. 
  X-axis: Blast Radius (R0: Read-only → R1: Write → R2: Integrated → R3: External/Action). 
  Y-axis: Verdict Severity (P: Contradicted, C: Dead Compute, R: ACL Leakage). 
  Cells contain deterministic outcomes: Pass, Surgical Edit, Escalate (Ship Evidence Packet), Hard Block. R3/P and R3/R cells are highlighted in red as Hard Gates.
- Supporting elements (actuators, latency principles, etc.)
  - Text streams optimistically; Actions hit hard gates.
  - Short hold-back buffer for surgical edits.
  - Escalations ship structured evidence packets, not vague alerts.
- Design notes
  The matrix is the hero. No other graphics. The transition from text (optimistic) to action (gated) must be visually obvious—perhaps an arrow from the text stream hitting a hard stop at the R3 column. Keep the supporting text to the absolute margins.

### Slide 3 — Why This Is Different (and Believable)
- Exact Headline
  Deterministic Verification, Not Probabilistic Guessing
- Left side content (what we refuse)
  - LLM-as-a-Judge (spoofable, slow)
  - Post-hoc dashboards (forensic, not live)
  - Composite risk scores (meaningless for engineering)
- Right side content (what we publish / credibility)
  - Graph-walked provenance per claim.
  - Per-route false-negative rates published transparently.
  - Zero-context-loss evidence packets on escalation.
- Closing line (must be the largest text element on the slide)
  It used to be a bad paragraph. It is now an executed transaction.
- Design notes
  The closing line must anchor the bottom of the slide in a heavy, unignorable typeface. The left and right columns are secondary, structured as tight, opposing lists. The visual weight should pull the eye directly from the headline down to the closing line, leaving the lists as supporting proof.