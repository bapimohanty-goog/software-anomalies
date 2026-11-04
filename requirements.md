# Software Anomaly Assessment & "Anomaly Thought Partner" Requirements (`requirements.md`)

## 1. Executive Summary & Purpose

This document defines the functional, domain, non-functional, and rollout requirements for the **Software Health Hazard Assessment (SW HHA) Anomaly Process** and its AI-guided implementation, the **SW Anomaly Thought Partner**.

These requirements synthesize two foundational proposals:
1. **Proposal for a more Effective/Efficient Process to Assess/Address SW Anomalies (March 2026)**: Defines the complete 8-part domain framework for assessing software anomalies, estimating risk ($\text{Risk} = \text{Frequency} \times \text{Severity}$), and conducting mandatory retrospectives for continuous improvement.
2. **Proposal: Progressive Rollout of the "Anomaly Thought Partner"**: Defines a 3-phase **"Crawl, Walk, Run"** conversational AI rollout strategy that eliminates blank-form friction, guides engineers sequentially through anomaly documentation, and progressively expands into full technical state capture, risk estimation, and root-cause analysis.

---

## 2. Stakeholders & User Roles

| Role | Responsibilities & Needs |
| :--- | :--- |
| **QA Engineer (Primary Author)** | Leads authoring of comprehensive anomaly assessments; ensures technical context, reproducibility, and risk inputs are complete before QAC submission. |
| **SW Test Engineer / SW Engineer** | Logs discovered anomalies rapidly during active testing or debugging; provides device/OS state, trigger sequences, root-cause understanding, and fix reproducibility. |
| **Product Manager (PM)** | Collaborates on anomaly impact, user perception, severity framing, and prioritization of fixes. |
| **Quality Assurance & Compliance (QAC)** | Reviews submitted recommendation reports for rapid confirmation (or rapid revision, where need for revision should be the exception). |
| **Engineering & Product Leadership** | Reviews mandatory retrospective findings to address systemic/general root causes related to ways-of-working, processes, and organizational factors outside the immediate team's control. |

---

## 3. Domain Requirements: Comprehensive SW Anomaly Assessment Framework

To produce a clear, vivid (self-explanatory) summary description and recommendation for QAC rapid confirmation, the end-to-end anomaly assessment process MUST capture the following eight domain dimensions with clarity, completeness, and conciseness:

### DR-1: Discovery Context (Empathy & Framing)
* **Requirement**: Capture how the anomaly was discovered as the opening context so an uninformed reader can immediately empathize with the team and understand the operational context.
* **Required Classifications**:
  * **Active Testing**: e.g., automated unit testing, integration testing, user acceptance testing (UAT).
  * **Passive Observation**: e.g., user reports, customer complaints, or application analytics such as Crashlytics.

### DR-2: User Manifestation & Severity Basis
* **Requirement**: Describe clearly how the anomaly manifests (shows up) to the end-user, including what the user sees, perceives, or experiences.
* **Downstream Usage**: Serves as the direct basis for assessing **Severity**.

### DR-3: Pre-Anomaly System State (At Time of Anomaly)
* **Requirement**: Document the exact state of the system immediately prior to the anomaly.
* **Required Details**:
  * **Device & OS Permutations**: Specific iOS and/or Android hardware models and OS versions affected.
  * **Operating Circumstances & Resource Constraints**: Environmental or runtime conditions such as limited available memory, low battery power, background wearable data syncing, or the smart device executing a computationally intensive task that makes it susceptible to a race condition with a triggering task/event.

### DR-4: Triggering Event Taxonomy
* **Requirement**: Identify the exact triggering event or sequence of events that causes the anomaly, categorized into one of three trigger sources:
  1. **External Trigger** (neither user action nor application/system action): e.g., a smart device OS update. Must document whether and how the user is made aware.
  2. **User Action Trigger**: Given the state of the App, the exact sequence of user actions that triggers the anomaly, and what the user perceives at each step.
  3. **Application / System Action Trigger**: e.g., an App update or the arrival of a data packet from the wearable to the App. Must document whether and how the user is made aware.
* **Downstream Usage**: Combined with Pre-Anomaly System State (DR-3) to estimate **Occurrence Frequency**.

### DR-5: Post-Anomaly System State & Recovery Behavior
* **Requirement**: Document the state of the system immediately after the anomaly occurs.
* **Required Details**:
  * **Recurrence Potential**: Can the anomaly re-occur? Will it repeatedly re-occur under the same conditions described in DR-3 and DR-4?
  * **One-and-Done / Recovery Path**: If the anomaly will not re-occur ("one-and-done"), specify what the user can expect afterward (e.g., whether the app crashes on upgrade but performs normally after an uninstall/reinstall or restart).

### DR-6: Reproducibility, Root Cause & Fix Verification
* **Requirement**: Establish technical certainty around reproducing and resolving the issue.
* **Required Details**:
  * Exact steps to reliably reproduce the anomaly.
  * Whether the underlying root cause is understood and well-defined.
  * Whether a fix to the root cause is well-defined and reproducible.

### DR-7: Defendable Risk Estimation ($\text{Risk} = \text{Frequency} \times \text{Severity}$)
* **Requirement**: Formulate a defendable initial Risk Estimate for QAC review:
  * **Frequency Estimate**: Derived from the required pre-anomaly system state (DR-3) and triggering event (DR-4), corroborated or "calibrated" against real-world analytics (e.g., Crashlytics) and/or complaint data when available.
  * **Severity Estimate**: Derived directly from how the anomaly manifests to the user (DR-2).
  * **Risk Calculation**: Compute and present $\text{Risk} = \text{Frequency} \times \text{Severity}$.

### DR-8: Mandatory Continuous Improvement Retrospective
* **Requirement**: Conduct a structured retrospective following each anomaly to drive continuous improvement.
* **Required Analysis**:
  1. **Immediate Root Cause Classification**: Determine whether the root cause resulted from:
     * *Requirements / Specifications Failure*: Insufficient or misunderstood requirements or specifications (or validation failure where the solution itself was specified wrong relative to customer needs).
     * *Verification / Implementation Failure*: Insufficient verification of specifications to requirements (the specific solution was built wrong).
     * *Other technical or operational factors*.
  2. **Systemic / General Root Cause Escalation**: Assess whether the anomaly is a symptom of a broader, more "general" root cause and how that general root cause can be systematically addressed (recognizing that systemic issues often relate to ways-of-working, ineffective/inefficient processes, or circumstances outside the team's control that require engaged Leadership intervention).

---

## 4. Functional Requirements: AI "Anomaly Thought Partner"

To prevent Day-1 adoption friction from presenting all 8 assessment dimensions as a static blank form, the system SHALL be implemented as an interactive conversational AI agent (**SW Anomaly Thought Partner**) rolled out across three progressive phases.

### 4.1 Core Conversational Engine Requirements

* **FR-CONV-1 (Sequential Single-Question Interviewing)**: The AI agent MUST ask questions sequentially—one question at a time—and MUST wait for the user's response before proceeding to the next question.
* **FR-CONV-2 (Brevity Detection & Clarifying Follow-Up)**: If a user's answer to a question is too brief or lacks critical detail, the AI agent SHALL gently ask for one clarifying detail before moving on to the next step.
* **FR-CONV-3 (Contextual Coaching & Suggestions)**: When interviewing on complex analytical topics (such as Risk Estimation or Root Cause / Retrospective analysis in Phase 3), if the user struggles, the AI agent SHALL offer helpful, context-aware suggestions synthesized from the user's previous answers and assist in calculating $\text{Risk} = \text{Frequency} \times \text{Severity}$.
* **FR-CONV-4 (Structured Report Synthesis)**: Once all steps in the active phase's interview are answered, the AI agent MUST synthesize the conversation into a clean, standardized Markdown report tailored to the active phase.
* **FR-CONV-5 (Post-Report Tweak & Ticketing Handoff)**: After generating the report, the AI agent SHALL ask the user whether they are ready to copy the output into their ticketing/QAC system or if they want to tweak/revise any details.

---

### 4.2 Phase 1 Requirements: Core Triage ("Crawl" — Weeks 1–2)

* **Objective**: Capture the most critical information required to understand and reproduce the anomaly while proving to engineers that the AI reduces documentation time.
* **Focus Areas**: Manifestation, Triggering Event, and Reproducibility.

#### FR-P1-1: Phase 1 Interview Flow (3-Step Core Triage)
The agent SHALL guide the user sequentially through the following three questions:
1. **Manifestation**: *"What exactly does the user see or experience when this anomaly happens?"*
2. **Triggering Event**: *"What specific user action, OS event, or app update triggered this?"*
3. **Reproducibility**: *"Can you reliably reproduce this? If so, what are the exact steps?"*

#### FR-P1-2: Phase 1 Output Specification ("Core Bug Report")
Upon completion of the 3 steps, the agent SHALL generate a **Core Bug Report** containing:
* `Issue Summary`
* `Manifestation`
* `Trigger`
* `Steps to Reproduce`
* Follow-up prompt asking if the user wants to copy the report for their ticketing system or tweak any details.

#### FR-P1-3: Phase 1 Baseline System Prompt
```text
You are the SW Anomaly Thought Partner. Your job is to help engineers rapidly and accurately log software anomalies. You must act as a helpful guide, making their job easier and faster.

INSTRUCTIONS:
You will ask the user exactly THREE questions to understand the anomaly. Ask them sequentially—do NOT ask the next question until the user has answered the current one. If their answer is too brief, gently ask for one clarifying detail before moving on.

THE 3-STEP CORE Triage:
1. Manifestation: Ask, "What exactly does the user see or experience when this anomaly happens?"
2. Triggering Event: Ask, "What specific user action, OS event, or app update triggered this?"
3. Reproducibility: Ask, "Can you reliably reproduce this? If so, what are the exact steps?"

FINAL OUTPUT:
Once all 3 steps are answered, synthesize the conversation into a clean, highly readable "Core Bug Report" containing:
- Issue Summary
- Manifestation
- Trigger
- Steps to Reproduce
Ask the user if they want to copy this for their ticketing system or if they need to tweak any details.
```

---

### 4.3 Phase 2 Requirements: Contextual SW Depth ("Walk" — Weeks 3–4)

* **Objective**: Expand scope to capture the technical environment and pre/post-anomaly system states, reducing back-and-forth clarification cycles between QA and developers.
* **Persona**: Senior QA guide ensuring no technical context is missed.
* **Focus Areas**: Phase 1 + Discovery Method + System State (Pre and Post).

#### FR-P2-1: Phase 2 Interview Flow (5-Step Contextual Assessment)
The agent SHALL guide the user sequentially (one question at a time) through the following five questions:
1. **Discovery & Manifestation**: *"How was this discovered (active testing vs. Crashlytics), and what exactly does the end-user experience?"*
2. **Pre-Anomaly System State**: *"What was the system state right before this happened? (e.g., iOS/Android version, low battery, high memory load, wearable data syncing?)"*
3. **Triggering Event**: *"What was the precise sequence of events or specific action that triggered the anomaly?"*
4. **Post-Anomaly System State**: *"What happens immediately after? Does the app crash? Does it require a reinstall, or does it recover?"*
5. **Reproducibility**: *"What are the exact steps to reproduce this issue reliably?"*

#### FR-P2-2: Phase 2 Output Specification ("Detailed Technical Anomaly Report")
Upon completion of the 5 steps, the agent SHALL synthesize the answers into a **Detailed Technical Anomaly Report** featuring:
* Clear headings corresponding to each of the 5 assessment areas (`Discovery & Manifestation`, `Pre-Anomaly System State`, `Triggering Event`, `Post-Anomaly System State`, `Reproducibility`).
* An objective, highly technical tone suitable for engineering and QA handoff.

#### FR-P2-3: Phase 2 Baseline System Prompt
```text
You are the SW Anomaly Thought Partner. Your job is to help engineers log comprehensive software anomalies. Act as a senior QA guide, ensuring no technical context is missed.

INSTRUCTIONS:
You will guide the user through a 5-step interview. Ask one question at a time. Wait for their response before proceeding.

THE 5-STEP CONTEXTUAL ASSESSMENT:
1. Discovery & Manifestation: Ask, "How was this discovered (active testing vs. Crashlytics), and what exactly does the end-user experience?"
2. Pre-Anomaly System State: Ask, "What was the system state right before this happened? (e.g., iOS/Android version, low battery, high memory load, wearable data syncing?)"
3. Triggering Event: Ask, "What was the precise sequence of events or specific action that triggered the anomaly?"
4. Post-Anomaly System State: Ask, "What happens immediately after? Does the app crash? Does it require a reinstall, or does it recover?"
5. Reproducibility: Ask, "What are the exact steps to reproduce this issue reliably?"

FINAL OUTPUT:
Synthesize the answers into a "Detailed Technical Anomaly Report" with clear headings for each of the 5 areas. Ensure the tone is objective and highly technical.
```

---

### 4.4 Phase 3 Requirements: The True "Thought Partner" ("Run" — Week 5+)

* **Objective**: Act as a strategic partner guiding the user to think critically about risk estimation, root cause, and continuous improvement before submitting to Quality Assurance & Compliance (QAC).
* **Focus Areas**: Phase 2 + Risk Estimation + Retrospective (streamlined into a 4-part interview for speed).

#### FR-P3-1: Phase 3 Interview Flow (4-Step Full QAC Assessment)
The agent SHALL interview the user step-by-step (one question at a time) through the following four consolidated questions:
1. **The Core Issue** *(Combined for speed)*: *"To start, how does this anomaly manifest to the user, and what are the exact steps/triggers to reproduce it?"*
2. **The Environment**: *"What was the system state before the anomaly (OS, device, memory), and what was the state immediately after?"*
3. **Risk Estimation**: *"Based on what you've described, how would you estimate the Frequency and the Severity of this issue for our users?"* (Assist the user in calculating $\text{Risk} = \text{Frequency} \times \text{Severity}$ and calibrating with analytics/complaint data if needed).
4. **Retrospective & Root Cause**: *"Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Does this point to a broader systemic issue we need to fix?"*

#### FR-P3-2: Phase 3 Output Specification ("Comprehensive QAC Recommendation Report")
Upon completion of the 4 steps, the agent SHALL generate a **Comprehensive QAC Recommendation Report**:
* Formatted cleanly in standardized Markdown so Quality Assurance & Compliance (QAC) can rapidly review, confirm, or (in exceptional cases) revise the Risk Estimate and Root Cause analysis.
* Includes executive summary description, discovery/manifestation context, pre/post-anomaly system states and triggers, reproducibility & fix status, defendable Risk Estimate ($\text{Frequency} \times \text{Severity}$), and Retrospective Root Cause classification (Requirements vs. Verification vs. Systemic/Process).

#### FR-P3-3: Phase 3 Baseline System Prompt
```text
You are the SW Anomaly Thought Partner. Your role is to elevate the quality of software anomaly reporting by guiding engineers through a structured root-cause and risk assessment.

INSTRUCTIONS:
Interview the user step-by-step. Ask one question at a time. If the user struggles with Risk or Root Cause, offer helpful suggestions based on their previous answers.

THE FULL ASSESSMENT:
1. The Core Issue: "To start, how does this anomaly manifest to the user, and what are the exact steps/triggers to reproduce it?" (Combine for speed).
2. The Environment: "What was the system state before the anomaly (OS, device, memory), and what was the state immediately after?"
3. Risk Estimation: "Based on what you've described, how would you estimate the Frequency and the Severity of this issue for our users?" (Help them calculate Risk = Frequency x Severity if needed).
4. Retrospective & Root Cause: "Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Does this point to a broader systemic issue we need to fix?"

FINAL OUTPUT:
Generate a "Comprehensive QAC Recommendation Report". Format it cleanly so Quality Assurance & Compliance can rapidly review the Risk Estimate and Root Cause analysis to confirm or revise the findings.
```

---

## 5. Non-Functional Requirements (NFRs)

* **NFR-1 (Security & Confidentiality)**: All anomaly interviews and report generation MUST run within an approved secure AI chat environment capable of handling confidential information, proprietary software architecture details, and Health Hazard Assessment (HHA) data.
* **NFR-2 (Low Cognitive Load & Conversational Ergonomics)**: The user experience MUST avoid overwhelming reporters with multi-page forms or walls of text; prompts must remain concise and conversational.
* **NFR-3 (Output Standardization & Rapid Reviewability)**: Generated reports MUST follow a consistent, predictable Markdown structure so QAC reviewers and PMs can rapidly locate manifestation, system state, risk calculations, and retrospective conclusions without re-formatting.
* **NFR-4 (Seamless Phase Upgradeability)**: The system architecture ("brain"/system prompt configuration) MUST support updating from Phase 1 to Phase 2 and Phase 3 centrally without requiring engineers to learn a new tool or interface.

---

## 6. Success Metrics & Evaluation Requirements

Baseline metrics MUST be recorded prior to launching the Phase 1 pilot and measured at the conclusion of each phase:

### 6.1 Quantitative Productivity Gains (Efficiency Metrics)

| Metric ID | Metric Name | Measurement Definition | Target / Goal |
| :--- | :--- | :--- | :--- |
| **KPI-QUANT-1** | **Time-to-Log (TTL)** | Average time an engineer spends drafting an anomaly report using the traditional blank-form method vs. the AI conversational interview. | **30–40% reduction** in time spent documenting. |
| **KPI-QUANT-2** | **First-Pass Quality ("QA Bounce Rate")** | Percentage/frequency of submitted anomalies kicked back to the reporter due to missing reproduction steps or system state details. | **50%+ reduction** in QA-to-Dev clarification pings. |
| **KPI-QUANT-3** | **Time-to-Resolution (TTR) Impact** | Downstream cycle time for Designers, PMs, and QAC to assess reports and assign fixes using standardized AI-generated QAC reports. | Measurable reduction in triage-to-assignment latency. |

### 6.2 Qualitative Experience Improvements (Satisfaction Metrics)

| Metric ID | Metric Name | Measurement Definition | Target / Goal |
| :--- | :--- | :--- | :--- |
| **KPI-QUAL-1** | **Cognitive Load Reduction (Reporter Experience)** | 1-to-5 scale survey issued to the pilot group: *"How much effort did logging this anomaly require compared to our old process?"* | High reporter satisfaction / lower perceived effort vs. blank form. |
| **KPI-QUAL-2** | **Reviewer Satisfaction (QAC/PM Experience)** | Poll of QAC and PM reviewers receiving AI-generated reports on whether standardized Markdown formatting and structure streamline confirming/revising risk estimates. | Positive QAC endorsement; revision becomes the exception. |
| **KPI-QUAL-3** | **Organic Adoption Rate** | Voluntary, unmandated usage across SW engineering, test, and QA teams during Phase 1 prior to mandating Phase 2. | Demonstrated organic growth across teams. |

---

## 7. Rollout & Phase-Gate Governance Requirements

1. **GATE-1: Live Demonstration ("Show, Don't Tell")**
   * Conduct a live sync demonstration by pasting the Phase 1 System Prompt into the secure AI chat and roleplaying a realistic software bug (e.g., *"The app crashed when syncing data"*), demonstrating sequential question pacing.
2. **GATE-2: Phase 1 "Tiger Team" Pilot (Weeks 1–2)**
   * Authorize a small cross-functional Tiger Team (**3–5 users across SW, Test, and QA**) to use the Phase 1 prompt on live anomalies for **5–7 days**.
3. **GATE-3: Baseline vs. Pilot Metrics Review**
   * Evaluate generated reports and pilot survey feedback against baseline metrics (TTL, QA Bounce Rate, Reporter Cognitive Load) to authorize transitioning the agent to **Phase 2 (Weeks 3–4)** and subsequently **Phase 3 (Week 5+)**.

---

## 8. Requirements Traceability Matrix

| Requirement ID | Requirement Summary | Source Proposal |
| :--- | :--- | :--- |
| **DR-1** | Discovery method capture (Active testing vs. Passive observation/Crashlytics) | March 2026 SW HHA Process Proposal (p. 1); Progressive Rollout Proposal (Phase 2) |
| **DR-2** | User manifestation capture & Severity assessment basis | March 2026 SW HHA Process Proposal (pp. 1–2); Progressive Rollout Proposal (Phases 1–3) |
| **DR-3** | Pre-anomaly system state (iOS/Android permutations, memory, battery, race conditions) | March 2026 SW HHA Process Proposal (p. 1); Progressive Rollout Proposal (Phases 2–3) |
| **DR-4** | Triggering event taxonomy (External OS, User action sequence, App/wearable packet) | March 2026 SW HHA Process Proposal (p. 1); Progressive Rollout Proposal (Phases 1–3) |
| **DR-5** | Post-anomaly system state (Recurrence vs. one-and-done, uninstall/reinstall recovery) | March 2026 SW HHA Process Proposal (p. 1); Progressive Rollout Proposal (Phases 2–3) |
| **DR-6** | Reproducibility, root-cause understanding, and reproducible fix definition | March 2026 SW HHA Process Proposal (p. 1); Progressive Rollout Proposal (Phases 1–3) |
| **DR-7** | Defendable Risk Estimate ($\text{Risk} = \text{Frequency} \times \text{Severity}$) calibrated with analytics/complaints | March 2026 SW HHA Process Proposal (p. 2); Progressive Rollout Proposal (Phase 3) |
| **DR-8** | Mandatory retrospective (Requirements vs. Verification vs. Systemic/Leadership root cause) | March 2026 SW HHA Process Proposal (p. 2); Progressive Rollout Proposal (Phase 3) |
| **FR-CONV-1..5** | Sequential 1-at-a-time questioning, clarifying follow-ups, coaching, Markdown synthesis | Progressive Rollout Proposal (pp. 1–3) |
| **FR-P1-1..3** | Phase 1 Core Triage (Weeks 1–2) 3-step interview & Core Bug Report | Progressive Rollout Proposal (pp. 1–2) |
| **FR-P2-1..3** | Phase 2 Contextual SW Depth (Weeks 3–4) 5-step interview & Detailed Technical Anomaly Report | Progressive Rollout Proposal (p. 2) |
| **FR-P3-1..3** | Phase 3 True Thought Partner (Week 5+) 4-step interview & Comprehensive QAC Report | Progressive Rollout Proposal (pp. 2–3) |
| **KPI-QUANT / QUAL** | TTL (30–40%), QA Bounce Rate (50%+), TTR, Cognitive Load survey, Reviewer satisfaction, Adoption | Progressive Rollout Proposal (pp. 3–4) |
| **GATE-1..3** | Live Demo, 3–5 user Tiger Team (5–7 days), Phase-gate metrics review | Progressive Rollout Proposal (p. 4) |
