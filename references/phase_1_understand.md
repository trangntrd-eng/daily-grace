# Phase 1: Understand & Evidence

**Goal**: Identify the real problem based on data, separating symptoms from the root problem. This phase aims to establish a solid foundation for the feature request by looking at both the problem and the opportunity it presents.

**Owner**: The **Product Specialist (PS)** is the primary owner of this phase. The Tech Lead (TL) is not typically involved at this stage.

## Key Steps

### 1.1: Collect & Verify Input Data
This initial step focuses on gathering all relevant data from both user and business perspectives. It is critical to answer the following questions before proceeding:

**User-Facing Data:**
- What is the direct feedback from customers? (verbatim quotes are preferred)
- What does the behavior data show? (e.g., drop-off rates, retention, session length, completion rates)
- How many users are affected? Is this an edge case or a majority issue?
- Which user segments are most impacted? (e.g., by age group, learning level, usage frequency)

**Business-Facing Data:**
- Which key metrics are affected? (e.g., DAU, paid conversion, churn, NPS)
- Where did this feature request originate? (e.g., support ticket, sales feedback, internal observation, data anomaly)
- Are there any revenue or retention implications? If so, what are the specific numbers?

> **Data Gate**: Do not proceed without at least **one quantitative data point** and **one qualitative piece of feedback** from an actual user. Assumptions alone are not a sufficient basis for a feature request.

### 1.2: Separate Symptom vs. Root Problem (🔴 R→C→D - MANDATORY)
This is a mandatory step that utilizes the Reasoning → Critique → Decision (R→C→D) model to ensure the team is solving the right problem.

- **Reasoning**: Define the actual problem to be solved, not just the surface-level symptom. List all known facts and assumptions based on the data from step 1.1. Propose 2-3 different interpretations of the problem and the feature that would result from each.
- **Critique**: Challenge the core assumptions. Could the primary interpretation be wrong? Are there any blind spots? Is the data sufficient to distinguish between the different interpretations?
- **Decision**: Clearly state the root problem. Justify the choice based on the available evidence and explain why other interpretations were rejected. Articulate what will change for the user if the feature is successful, in a measurable way.

### 1.3: Opportunity Perspective
Beyond just solving a problem, it's important to understand the opportunity this feature presents.

- If this problem is solved, which metrics will improve and by how much?
- Is this an opportunity for differentiation or just to catch up with the market?
- How are the top 5% of players in the market addressing a similar problem?

### 1.4: Identify User Segment & Behavior Change
Define the target audience and the desired outcome.

- Who is the primary target user segment?
- What is their current behavior?
- What is the desired behavior after the feature is implemented?
- How will this change in behavior be measured?

## Phase 1 Checkpoint (Product Internal)

Before moving to the next phase, ensure the following conditions are met:

- [ ] Real data (both quantitative and qualitative) has been collected.
- [ ] The root problem has been identified and agreed upon using the R→C→D process.
- [ ] The desired behavior change has been described in a measurable way.
- [ ] The user segment and opportunity have been clearly defined.

**Output**: A concise **FR Brief** that summarizes the problem, opportunity, user segment, and desired behavior change.
