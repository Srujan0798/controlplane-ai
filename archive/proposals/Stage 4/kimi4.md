### Slide 1 — The Reframe

**Exact Headline (10 words)**  
The system didn't fail. It was never asked to prove anything.

**Primary Visual**  
A split before/after diagram.  
- **Left (muted, ~30% width):** "TEXT SCORING" — a paragraph flows into a box labeled "Quality Score: 0.92" with a green checkmark. Rendered at 30% opacity gray.  
- **Right (dominant, ~70% width):** "EXECUTION BOUNDARY" — the same paragraph is decomposed into three nodes (CLAIM-1, CLAIM-2, CLAIM-3). Each node has a tether line down to a horizontal PROVENANCE bar containing `source | ACL | hash`. CLAIM-1 and CLAIM-2 are green with the label "SUPPORTED." CLAIM-3 is red with the label "UNSUPPORTED" and is physically blocked by a hard-gate icon from reaching an ACTION node.

**Supporting text / bullets (4 lines)**  
- AI output is not text to score. It is a transaction requesting permission.  
- Evidence captured at context-assembly: source, ACL, hash. Outside the model.  
- Default: UNSUPPORTED. Inverted burden of proof.  
- One graph. Three reads. STEP → SPAN → CLAIM → ACTION.

**Footer line**  
ControlPlane.ai — Execution boundary layer

**Design notes**  
The right side must carry at least 70% of visual weight. Left side should feel like a ghosted legacy approach. Use monospace for the PROVENANCE bar and the graph chain. The hard-gate icon should be the only decorative element—geometric, not illustrative. No gradients.

---

### Slide 2 — The Decision System

**Exact Headline (8 words)**  
Spend verification budget in proportion to blast radius.

**Primary Visual**  
A 4×3 grid matrix centered on the slide.  
- **Y-axis (left):** BLAST RADIUS — R0 at bottom, R3 at top.  
- **X-axis (top):** VERDICT — SUPPORTED | UNCERTAIN | UNSUPPORTED.  
- **Cell contents (single word, monospace):**  
  - R0: STREAM | STREAM | EDIT  
  - R1: STREAM | EDIT | ESCALATE  
  - R2: STREAM | EDIT | BLOCK  
  - R3: STREAM | ESCALATE | BLOCK  
- The **R3 × UNSUPPORTED** cell is solid red fill with white "BLOCK" text and a small annotation arrow: *"e.g., ₹1,84,000 refund / clause 7.2 — HARD GATE."*  
- The **R0 × SUPPORTED** cell is solid green fill.  
- All other cells use flat, high-contrast fills (pale green, yellow, orange). No gradients.

**Supporting elements (3 lines)**  
- Actions: hard gate. Text: optimistic stream with short hold-back.  
- Surgical edit only. Escalate ships structured evidence packet.  
- Deterministic checks <5ms. Probabilistic async with circuit breaker.

**Design notes**  
The matrix must occupy the center 60% of the slide and be readable from 10 feet. Rows grow taller as blast radius increases; R3 should feel visually heaviest. Y-axis labels aligned hard left. Cell borders should be thin, sharp, and black. The red BLOCK cell must be the immediate focal point.

---

### Slide 3 — Why This Is Different (and Believable)

**Exact Headline (6 words)**  
What we refuse. What we prove.

**Left side content (what we refuse)**  
- No LLM-as-judge. No infinite regress.  
- No composite risk scores. Risk is not a scalar.  
- No "zero latency" claims. We hold back where it matters.  
- No fully autonomous promises. Humans get evidence packets.

**Right side content (what we publish / credibility)**  
- Per-route false-negative rate. Published. Auditable.  
- Provenance captured outside the model. ACL + hash.  
- Deterministic entitlement checks. No pattern decay.  
- One graph. Three reads. No separate tools.

**Closing line (largest text element on the slide)**  
it used to be a bad paragraph. It is now an executed transaction.

**Design notes**  
Left column in muted gray. Right column in solid black. Thin vertical divider between them. The closing line spans the full slide width at the bottom, set in the largest type size on the deck (minimum 32pt equivalent), with **"executed transaction"** rendered in a single accent color. The words "refuse" and "prove" in the headline should be bolded to carry the structural weight.

---

### Tension Flags & Resolutions

1. **Graph chain density:** STEP → SPAN → CLAIM → ACTION is architecturally central but visually dense for a single slide.  
   *Resolution:* Reduced to a single typographic chain on Slide 1, not a separate diagram. The visual dominance is reserved for the before/after reframe.

2. **Action vs. text dual-path:** The distinction between hard-gating actions and optimistically streaming text risks splitting the matrix into two visuals.  
   *Resolution:* The matrix shows unified verdict logic; the action/text split is handled in one supporting line beneath the matrix, keeping the grid clean and singular.

3. **False-negative rate as credibility anchor:** Publishing per-route false-negative rates is a key differentiator but can feel like a footnote.  
   *Resolution:* Placed as the lead item in Slide 3's right-hand column, ensuring it is read as a primary credibility mechanism, not an afterthought.