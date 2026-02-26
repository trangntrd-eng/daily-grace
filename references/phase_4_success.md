# Phase 4: Define Success & Bottleneck

**Goal**: For the Product and Tech teams to jointly define measurable success criteria and identify the core bottlenecks that could impede success.

**Owners**: The **Product Specialist (PS)** leads the definition of success criteria, while the **Tech Lead (TL)** leads the identification of bottlenecks. The **Data Team** should be consulted for input.

## Key Steps

### 4.1: Define Success Criteria (🔴 R→C→D - MANDATORY)
This is a mandatory step to ensure that success is defined in measurable terms before development begins.

- **Reasoning**: The goal is to define success using metrics that can be measured and compared against a baseline. List all possible metrics for this feature request. Classify them into:
    - **Primary Metric**: Directly reflects the success of the feature.
    - **Secondary Metrics**: Confirm that there are no negative side effects.
    - **Guardrail Metrics**: Metrics that must not get worse.
- **Critique**: Does the primary metric truly reflect the desired behavior change, or is it just an easy-to-measure proxy? Are any important metrics being missed? Is the baseline realistic and measurable? Is the timeframe for measurement long enough to see a real signal?
- **Decision**: Finalize the primary metric with a specific baseline and target. Finalize the secondary and guardrail metrics. Agree on the timeframe for measurement.

### 4.2: Identify Bottleneck (🔴 R→C→D - MANDATORY)
This mandatory step focuses on proactively identifying and addressing potential roadblocks.

- **Reasoning**: What is the single biggest bottleneck that could prevent this feature from succeeding? Consider technical, user experience, and go-to-market factors. What is the riskiest assumption we are making?
- **Critique**: Are we focusing on the right bottleneck? Are there any hidden bottlenecks that we are not considering? What evidence do we have that this is the primary bottleneck?
- **Decision**: Clearly state the primary bottleneck and the riskiest assumption. Define a plan to de-risk the bottleneck before full-scale development.

### 4.3: Risk Assessment & Mitigation
Based on the identified bottleneck, conduct a more thorough risk assessment.

- What are the top 3 risks associated with this feature?
- What is the potential impact of each risk?
- What is the mitigation plan for each risk?

## Phase 4 Checkpoint (Product-Tech Aligned)

Before proceeding, ensure the following conditions are met:

- [ ] Measurable success criteria (primary, secondary, guardrail) have been defined and agreed upon.
- [ ] The primary bottleneck and riskiest assumption have been identified.
- [ ] A risk mitigation plan is in place.

**Output**: A **Success & Bottleneck Document** that clearly outlines the success metrics, the primary bottleneck, and the associated risks and mitigation plans.
