# Adversarial Validation Blueprint: A Buildable Prototype for ControlPlane.ai's Frozen Architecture

## Prototype Goal and Strategic Scope Definition

This document defines the precise, buildable, and demonstrable scope for the ControlPlane.ai Stage 3 prototype, created under the highest adversarial standard to secure victory in the Accenture Innovation Challenge 2026 – Round 2 . The singular mission is not to produce a competent student project but to deliver a winning solution that forces a serious engineer to respect the architecture within an eight-minute live demo . The prototype’s sole purpose is to serve as an unambiguous proof-of-concept for the non-negotiable, frozen Round 1 architecture, centered on four pillars: provenance captured outside the model, an inverted burden of proof, mandatory entitlement checks, and blast-radius pricing . The entire design is ruthlessly optimized to demonstrate the power of a single, enforceable `STEP → SPAN → CLAIM → ACTION` graph that governs a fixed `R×S` matrix across heterogeneous AI use cases, while deliberately excluding all other features to prevent dilution of this core differentiator .

The strategic scope is defined by a hard boundary. The prototype will implement exactly two primary adversarial flows and one clean-path flow to maximize signal-to-noise ratio within the tight demo window. The chosen adversarial flows are the refund dual-action case, which combines a clause 7.2 absence with an entitlement violation, and the internal knowledge principal-flip entitlement case . These are not mere examples but the central proofs of the system's unique value proposition. The third flow demonstrates a clean, supported path where the system correctly validates a claim without triggering any exceptions. This focused approach ensures that every second of the demo serves to reinforce the core thesis: ControlPlane.ai is not a generic guardrail but a hardened control plane enforcing explicit, evidence-based policies .

The following table details the prototype's functional boundaries, clearly delineating what will be implemented, what will be mocked, and what is strictly out of scope. This structure prioritizes mechanisms that can be shown live over those that can only be described, adhering to the principle that depth of demonstration trumps breadth of features .

| Category | Component / Feature | Status | Justification |
| :--- | :--- | :--- | :--- |
| Implemented | Provenance Recorder | Real | Captures context before model inference; foundational to proving provenance is external. |
| Implemented | Evidence Ledger Structure | Real | Stores the full `STEP→SPAN→CLAIM→ACTION` graph; the core artifact of the demo. |
| Implemented | Claim Extractor & Binder | Real | Uses an LLM to identify claims in the model response and bind them to spans of text. |
| Implemented | Re-computation Engine | Real | Verifies numeric claims by re-executing logic from the provenance. |
| Implemented | ACL / Entitlement Service | Real | Enforces access control based on principal identity and resource access rights. |
| Implemented | Policy Decision Engine | Real | Implements the `R×S` matrix as a lookup table to determine disposition. |
| Implemented | Two-Pending-Actions Resolver | Real | An algorithm to resolve conflicting actions into a single, final disposition. |
| Implemented | Evidence Ledger UI | Real | A web dashboard to visualize the generated graph, making it indispensable to the demo. |
| Mocked | Ground Truth Verifier | Thin Mock | Simulates a check against a reliable ground truth source. Not used for primary decisions. |
| Mocked | Bias Measurement Module | Thin Mock | Simulates bias detection. Excluded per initial brief . |
| Mocked | Confidence Scoring System | Thin Mock | Simulates confidence scores. Explicitly excluded per initial brief . |
| Out of Scope | Multi-turn Conversation State Management | Deliberately Excluded | To maintain focus on the core graph and stateless validation. |
| Out of Scope | Dynamic Regulation Updates | Deliberately Excluded | The policy engine is configurable, but dynamic updates are out of scope. |
| Out of Scope | Human-in-the-Loop Escalation UI | Deliberately Excluded | Escalation is demonstrated as a final action, not a process. |

The minimum viable live demonstration consists of the complete, end-to-end execution of the refund dual-action flow, culminating in the Evidence Ledger UI displaying the resolved `R1: Edit Text` and `R3: Escalate` actions derived from the single input. This sequence alone constitutes a powerful proof of the system's capabilities. The addition of the principal-flip and clean-path flows provides supporting evidence, reinforcing the robustness of the underlying architecture rather than simply adding new features . The build order recommendation is critical: foundation components like the Provenance Recorder and Evidence Ledger must be built first, but the primary integration milestone must be achieving a working, visible instance of the dual-action resolution. This ensures the team drives toward the most impactful proof point, preventing premature optimization of less critical paths .

## Synthetic Data and Corpora Blueprint

To achieve maximum impact within the eight-minute demo, the synthetic data and corpora must be meticulously crafted to prioritize depth over breadth, focusing exclusively on creating high-signal adversarial edge cases . The goal is not to cover a wide array of claim types but to create scenarios where the prototype's unique defenses—particularly the inverted burden of proof and entitlement checks—are forced to engage. The data will be enterprise-shaped and contain no real PII, aligning with the project's constraints . The blueprint specifies the minimal datasets required to execute the three core demonstration paths: the refund dual-action case, the internal knowledge principal-flip, and a clean/supported path.

For the **Refund Dual-Action Case**, the synthetic corpus must create a situation where the model synthesizes a plausible but factually unsupported claim, combining information from multiple sources. This requires two distinct documents:
1.  **Document A (Real Policy):** A well-formed internal policy document containing a valid refund policy. Crucially, this document contains a clause 7.2, stating that refunds are subject to a 15% processing fee if requested more than 30 days after purchase.
2.  **Document B (Plausible Fiction):** A separate, plausible document that is otherwise legitimate (e.g., a customer service best practices guide) but contains a fabricated sentence: "Clause 7.2 explicitly states that all refunds are processed immediately at no additional cost."
The LLM prompt for this test will ask about the refund policy. The engineered response will synthesize content from both documents, claiming "per clause 7.2" when discussing fees. This creates a conflict: the claim is grounded in Document B, which is irrelevant to the question, thus satisfying the condition of an entitlement violation on the same response . The control plane must detect this misattribution and trigger the two-pending-actions resolution.

For the **Internal Knowledge Principal-Flip Entitlement Case**, the corpus is structured around a clear access-control boundary. It consists of two sets of documents and two distinct user roles:
1.  **Manager-Accessible Documents:** A set of confidential financial reports and internal strategy memos. All documents in this set are assigned a specific hash identifier (e.g., starting with `MGR_`) and are accessible only to users with the `Manager` role.
2.  **Agent-Accessible Documents:** A larger set of public-facing marketing materials and general product guides. These documents have identifiers starting with `AGT_`.
3.  **Principals:** The demo will be run twice using the same query but with different principals:
    *   First run with principal `user_id="manager_123"` and role `Manager`. This principal has access to both document sets.
    *   Second run with principal `user_id="agent_456"` and role `Agent`. This principal has access only to the `AGT_` documents.
The query will request a summary of a specific detail found only in the `MGR_` documents. The first run (with the Manager) will succeed, grounding its claim in the correct, accessible source. The second run (with the Agent) will fail the entitlement check, even though the factual claim itself is valid. This perfectly demonstrates the enforcement of access control independent of factual accuracy, proving the second core tenet of the frozen architecture .

Finally, to show that the system is not merely a blocker, a **Clean/Supported Path** must be included. This requires a simple, straightforward scenario:
1.  **Document C (Clear Source):** A product description document that explicitly states: "Our premium subscription costs $99 per month."
2.  **Query:** "What is the price of the premium plan?"
The model's response will be a direct quote from Document C. The Claim Extractor will successfully bind the span "$99 per month" to the claim type `price_of_premium_plan`. The provenance will correctly link this span to Document C. The ACL check will pass as the principal has access to the document. The resulting `(R,S)` score will map to a supported action, demonstrating the system's ability to positively validate and approve requests, not just reject them. This clean path provides necessary balance to the adversarial tests, showing the full range of the system's behavior.

This targeted data strategy ensures that every piece of synthetic content serves the primary goal: to force the prototype's core mechanisms into action and make their operation visible and undeniable to the judge.

## Core Component Architecture and Implementation Guidance

The prototype's architecture is a direct translation of the frozen Round 1 design, composed of discrete components with a single line of responsibility each. The implementation strategy is to build these components to be real and functional, except where explicitly marked as a mock to stay within the strict prototype boundary. This section details each component, its role, and its status (Real vs. Mock). The architecture is designed for observability, with every decision point traceable through the Evidence Ledger.

| Component Name | Responsibility | Implementation Status | Key Interaction Points |
| :--- | :--- | :--- | :--- |
| **Provenance Recorder** | Captures the complete input/output context (prompt, retrieved docs, model response) before forwarding to the model. | Real | Receives input from the client application and passes it to the Model Orchestrator. Emits a `STEP` event to the Evidence Ledger. |
| **Evidence Ledger** | A persistent store for the `STEP → SPAN → CLAIM → ACTION` graph. It records the full lineage of the evaluation. | Real | Serves as the central database for the Evidence Ledger UI. Written to by all subsequent components. |
| **Model Orchestrator** | Manages the call to the external LLM API, passing the context and receiving the response. | Real | Invokes the LLM API and passes the raw response to the Claim Extractor. |
| **Claim Extractor & Binder** | Analyzes the model's response text to identify potential claims and attempts to bind them to spans of text using an LLM. | Real | Takes the model response from the Orchestrator and emits `SPAN` and `CLAIM` nodes to the Evidence Ledger. |
| **Recomputation Engine** | For claims involving numerical values, re-executes the calculation logic based on the original provenance to verify correctness. | Real | Consumes `CLAIM` nodes with numeric types from the Evidence Ledger and updates them with a `VERIFIED` or `FAILED` status. |
| **ACL / Entitlement Service** | Checks if a given principal (user) is authorized to access a resource identified by its provenance hash. | Real | Consumes `SPAN` nodes from the Evidence Ledger and returns a boolean authorization result. |
| **Policy Decision Engine** | Implements the `R×S` matrix as a lookup table to map a `(Risk_Rating, Safety_Score)` tuple to a final `(Action, Blast_Radius_Price)`. | Real | Consumes validated `CLAIM` nodes and the results of the ACL check to compute the final disposition. |
| **Two-Pending-Actions Resolver** | An algorithm that detects when the Policy Engine proposes more than one action and resolves them according to predefined rules. | Real | Consumes proposed actions from the Policy Engine and outputs a single, final `ACTION` node to the Evidence Ledger. |
| **Evidence Ledger UI** | A web-based dashboard that visualizes the `STEP→SPAN→CLAIM→ACTION` graph, highlighting bindings, ACL statuses, and the final resolution. | Real | Reads from the Evidence Ledger and presents the interactive graph to the judge. |
| **Ground Truth Verifier** | A thin mock that simulates checking a claim against a trusted, authoritative source. Its output is not used for gating. | Thin Mock | Simulates an external verification process. |
| **Bias Measurement Module** | A thin mock that simulates the detection of demographic biases in the model's output. | Thin Mock | Simulates a bias analysis. Excluded per initial brief . |
| **Confidence Scoring System** | A thin mock that simulates generating a confidence score for the overall response. | Thin Mock | Simulates a confidence assessment. Excluded per initial brief . |

The recommended build order is foundational-first, with the ultimate goal of achieving the first runnable success path being the end-to-end dual-action resolution flow. This sequence ensures that the team builds the necessary infrastructure before attempting complex integrations, and that the most impressive feature is delivered early.

1.  **Foundation Layer:** Begin by building the `Provenance Recorder`, `Evidence Ledger` (database schema), and the `Model Orchestrator`. These form the backbone of the system. Unit tests should validate that the recorder captures the expected context and the ledger can persist the basic graph structure.
2.  **Core Logic Layer:** Develop the `Claim Extractor & Binder` and the `ACL / Entitlement Service`. These components perform the primary analytical work. They can be unit-tested independently by feeding them synthetic responses and principal/resource pairs.
3.  **Decision Layer:** Implement the `Policy Decision Engine` and the `Two-Pending-Actions Resolver`. These components apply the frozen `R×S` matrix and its special rules. They should be tested with various `(R,S)` inputs to ensure they return the correct actions.
4.  **Integration and Demonstration:** Finally, integrate all components. The priority here is to get the refund dual-action flow working end-to-end. This involves wiring the `Provenance Recorder` to the `Orchestrator`, the `Orchestrator` to the `Claim Extractor`, and so on, until the `Evidence Ledger UI` displays the full, resolved graph for this adversarial case. Only after this milestone is achieved should time be spent polishing the secondary flows or the UI.

This disciplined, adversarial-first approach guarantees that the prototype's most powerful feature is not an afterthought but the culmination of the engineering effort, maximizing its impact on the judges .

## Adversarial Demo Flows and Evidence Ledger Visualization

The eight-minute demo is the ultimate proving ground for the prototype. Every element must be choreographed to relentlessly demonstrate the system's architectural superiority. The primary flow will be the refund dual-action case, constructed backward from the action gate to ensure the most impressive mechanics are front-loaded. The secondary flow will be the principal-flip entitlement case. The Evidence Ledger UI is not a supplementary display; it is the star of the show, mandated by the requirement that "if the judge can remove the graph from the screen and the demo still looks the same, the scope has already failed" . Therefore, the UI must dominate the screen and visually enforce the relationships within the `STEP→SPAN→CLAIM→ACTION` graph.

**Primary Demo Flow: Refund Dual-Action Resolution**

This flow will be executed in a single, continuous sequence, narrated by the presenter to explain each step as it happens in the Evidence Ledger.

1.  **Initiation:** The presenter clicks a button labeled "Run Refund Dual-Action Test." The UI shows a pre-filled form with a query: "I want to know about your refund policy for my premium subscription." The selected use case is "Customer Support Assistant," which has a low latency budget and high blast-radius tiers for irreversible actions.
2.  **Provenance Capture (STEP):** In the Evidence Ledger UI, a new `STEP` node appears automatically. It is populated with the raw query, the hashes of the two synthetic documents (one containing the real clause 7.2, one the fake one), and the model's final response, which has been synthesized to reference the fake clause. This instantaneously proves `provenance is captured outside the model`.
3.  **Claim Binding and Span Identification:** The Claim Extractor processes the model's response. The UI now populates with `SPAN` nodes, highlighting the phrase "per clause 7.2" and the figure "$15 fee." Below, `CLAIM` nodes appear, stating `claim_type: 'refund_policy_applies'` and `claim_type: 'processing_fee_amount'`. The UI visually links the `SPAN` for "clause 7.2" to the first `CLAIM`.
4.  **Entitlement Check Failure:** The system now attempts to bind the `SPAN` "clause 7.2" to its source document. The UI highlights this binding attempt. The ACL service is called. Because the claim is grounded in the fictional document (which the simulated user lacks access to), the ACL check fails. The UI instantly changes the color of the `SPAN` node and its associated `CLAIM` node to red and adds a label: `ENTITLEMENT VIOLATION`.
5.  **Inverted Burden of Proof Engaged:** The presenter explains that because the entitlement check failed, the claim is `UNSUPPORTED`. The UI reflects this, setting the disposition of that `CLAIM` to `UNSUPPORTED`.
6.  **Proposed Actions and Resolution:** The Policy Engine evaluates the remaining valid claim (`processing_fee_amount`). Based on the `R×S` matrix for this use case, it determines a `Risk_Rating` of `R3` (High) due to the unresolved entitlement issue. This maps to two possible actions: `R1: Edit Text` and `R3: Escalate`. The Two-Pending-Actions Resolver activates. The UI now clearly shows two proposed actions. The resolver then applies its rule: if an `R3` action is proposed, the final disposition is always `R3: Escalate`. The UI collapses the two proposals into a single, final `ACTION` node with the value `Escalate` and a reason: "High-risk entitlement violation detected."
7.  **Final Disposition:** The top of the UI displays the final verdict: `DISPOSITION: UNSUPPORTED (RESOLVED TO ESCALATE)`. The presenter concludes by emphasizing that the system did not block the response entirely but intelligently escalated it for human review, demonstrating blast-radius pricing in action [[49]].

**Secondary Demo Flow: Internal Knowledge Principal-Flip**

This flow will be shown as a quick contrast to the first.

1.  **Initiation:** The presenter clicks "Run Principal-Flip Test." The query is: "Summarize Q4 financial performance." The principal is initially set to `Manager`.
2.  **Successful Execution (Manager):** The UI shows the `STEP`, followed by `SPAN`s and `CLAIM`s correctly bound to a `MGR_` document. The ACL check passes (green checkmark). The `R×S` matrix yields a safe disposition of `Text View`. The final verdict is `SUPPORTED`.
3.  **Principal Switch and Re-run:** The presenter quickly changes the principal to `Agent` in the UI form and re-runs the identical query.
4.  **Entitlement Check Failure (Agent):** The UI shows the same initial steps, but when the binding occurs, the ACL check for the `MGR_` document fails. The `SPAN` and `CLAIM` turn red with an `ENTITLEMENT VIOLATION` label. The final disposition becomes `UNSUPPORTED`. The presenter uses this to drive home the point that the system's decision is based on who is asking, not just what is true.

**Evidence Ledger UI Requirements:**

*   **Dominant Visual:** The graph visualization must occupy at least 70% of the screen.
*   **Legibility:** Nodes must be large enough to read labels for `STEP`, `SPAN`, `CLAIM`, `ACTION`, and their properties (e.g., `claim_type`, `disposition`, `principal_role`).
*   **Color Coding:** Use a consistent color scheme: green for passed checks (ACL, Recompute), red for failures (ACL, Entitlement), and neutral gray for pending or informational items.
*   **Annotations:** The UI must have a small, non-obtrusive panel that explains the meaning of the colors and the relationships (e.g., "A solid arrow means 'is bound to'").
*   **Interactive Elements (Nice-to-Have):** While not mandatory, allowing a click on a `SPAN` to highlight its corresponding text in the model's response and a click on a `CLAIM` to show its source `SPAN`s would significantly enhance clarity without requiring extensive development time.

By making the graph the undeniable center of attention, the demo transforms from a simple product walkthrough into a compelling forensic examination of the system's logic, fulfilling the core research goal .

## Verification Framework: Mapping Success Criteria to Implementation Checks

To satisfy the judges, every abstract success criterion from the initial scope (R2S1.md §5) must be mapped to a concrete, observable implementation or runtime check within the prototype . This framework translates the high-level goals into verifiable technical requirements, ensuring that the prototype's claims can be objectively assessed. The following table provides this direct mapping, forming the basis for the judging rubric.

| R2S1 Success Criterion | Description | Implementation Check / Runtime Verification |
| :--- | :--- | :--- |
| **Provenance Outside the Model** | The system's evidence base originates from the interaction with the AI model, not from inside the model itself. | The `Provenance Recorder` component is a real implementation that captures the prompt, retrieved documents, and model's raw response *before* the model processes the request. The Evidence Ledger UI must display this captured context as the root `STEP` node. |
| **Default Disposition is UNSUPPORTED** | The system assumes a claim is invalid until sufficient evidence is provided. | If the Claim Extractor finds no valid bindings or if all claims fail subsequent checks (ACL, Recomputation), the Policy Decision Engine's final output for that claim is `UNSUPPORTED`. The UI must explicitly render this disposition. |
| **Entitlement Check is Enforced** | Access control is a mandatory, non-bypassable gatekeeper for claims grounded in protected resources. | For every `SPAN` that is bound to a resource (document), the `ACL / Entitlement Service` is invoked. If the service returns false, the binding is invalidated, and the associated `CLAIM` is marked `UNSUPPORTED`. The UI must visually highlight this failure. |
| **The Exact R×S Matrix is Applied** | The decision-making process uses a predefined, configurable matrix to map risk and safety scores to actions. | The `Policy Decision Engine` is implemented as a static lookup table (dictionary/hashmap) representing the frozen `R×S` matrix. The final action chosen is determined by looking up the `(Risk_Rating, Safety_Score)` tuple in this table. The UI should indicate which cell was accessed. |
| **Hard Gate on Actions, Not Tokens** | The system gates on whether an action is permitted, not on the number of tokens generated or a generic confidence score. | The core logic never considers token counts or proprietary model confidence scores. Decisions are made based on the outcomes of the `CLAIM` binding and `ACL` checks, which then feed into the `R×S` matrix to select an action. The UI focuses on actions, not token limits. |
| **FNR is Published as a Format** | The system acknowledges and defines a structure for reporting its False Negative Rate, even if production numbers are not available. | The prototype includes a schema definition (e.g., a JSON Schema file) for a False Negative Report. The Evidence Ledger UI can display an empty instance of this schema, demonstrating that the format is published and understood. |
| **Two-Pending-Actions Resolution Works** | When the policy engine identifies multiple potential actions, a specific resolver mechanism chooses one. | The `Two-Pending-Actions Resolver` is a real algorithm that inspects the list of proposed actions from the Policy Engine. It applies a deterministic rule (e.g., "if R3 is present, choose R3") and outputs a single, final action. The UI must show both proposed actions before resolution and the single final action after. |
| **No LLM-as-Judge on Critical Path** | No secondary LLM is used to make a final judgment on the primary claim. | The `Claim Extractor` is an LLM, but its output is treated as a hypothesis to be verified by deterministic checks (ACL, Recomputation). No other LLM is invoked to decide the final disposition. The entire decision path is rule-based after the initial extraction. |

This verification framework is the technical contract that binds the prototype's design to its stated goals. By implementing and exposing each of these checks, the team provides the judges with an unimpeachable record of the system's behavior, moving the conversation from theoretical architecture to provable engineering . The fidelity self-check in the final section of this document will confirm that this specification holds firm against all frozen principles.

## Risk Mitigation and Fidelity Assurance

The single greatest scope risk for this prototype is that the eight-minute demo will fail to communicate the system's core value proposition, instead appearing as a generic, opaque "AI guardrail." This risk arises from a lack of focus on the Evidence Ledger, causing the judge to see a successful outcome without understanding the intricate, evidence-based reasoning that produced it. The mitigation for this risk is absolute and unwavering adherence to the principle that the `STEP→SPAN→CLAIM→ACTION` graph is the indispensable artifact of the demo . Every component, every flow, and every UI element must be designed to serve this graph, making its construction and resolution the central narrative of the presentation. The Evidence Ledger UI will not be an appendix; it will be the main stage.

Before delivering the final specification, a rigorous fidelity self-check is conducted to ensure that the prototype remains true to the non-negotiable, frozen Round 1 architecture . This check explicitly confirms that the proposed design does not soften, weaken, or remove any of the core principles.

| Fidelity Principle | Status | Rationale |
| :--- | :--- | :--- |
| **Default = UNSUPPORTED** | Preserved | The Policy Decision Engine is designed to default to `UNSUPPORTED` if no valid bindings exist or if any check (ACL, etc.) fails. This is a core tenant of the inverted burden of proof. |
| **Entitlement / ACL Check** | Preserved | The `ACL / Entitlement Service` is a real, mandatory component. Its failure directly invalidates a claim's grounding, regardless of the claim's factual accuracy. This is a primary proof point of the demo. |
| **Exact R×S Matrix** | Preserved | The `Policy Decision Engine` is implemented as a lookup table based on the frozen matrix. The demo explicitly shows this mapping from `(R,S)` to a final action. |
| **Hard Gate on Actions** | Preserved | The system's decision is based on a combination of claim validity and the `R×S` matrix, not on soft metrics like token count or a secondary LLM's confidence score. The final output is a single, gated `ACTION`. |
| **Published Own FNR as a Format** | Preserved | The prototype includes a schema definition for a False Negative Report, demonstrating that the concept is understood and formalized, even without production data. |
| **Two-Pending-Actions Resolution** | Preserved | A dedicated `Two-Pending-Actions Resolver` component implements a deterministic rule to collapse multiple proposed actions into a single final disposition, as required by the freeze. |
| **No LLM-as-Judge on Critical Path** | Preserved | The primary LLM is used solely for claim extraction. All subsequent judgments are made by deterministic, rule-based checks (ACL, Recomputation) and the `R×S` matrix. No secondary LLM makes the final call. |
| **Bias as Per-Response Verdict** | Preserved | The prototype deliberately excludes any mechanism that would turn bias into a live, per-response verdict, as specified in the initial research goal. |

This specification represents the final, rigorously vetted definition for the ControlPlane.ai Stage 3 prototype. It is buildable, demonstrable, and, most importantly, a weaponized proof of the system's architectural superiority. By focusing with surgical precision on the core differentiator and executing flawlessly within the defined scope, this prototype is positioned not just to participate, but to win .