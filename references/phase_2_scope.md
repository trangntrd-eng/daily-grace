# Phase 2: Scope & Classify

**Goal**: Position the feature within the existing system, apply the 80/20 rule to define a core scope, and classify the primary and secondary Techstack Tracks involved.

**Owner**: The **Product Specialist (PS)** leads this phase, with the **Tech Lead (TL)** responsible for validating the track classification.

## Key Steps

### 2.1: Position Within the Product System
Understand how the proposed feature fits into the current product architecture.

- Which module does it belong to?
- Does it overlap with any existing features?
- Which layers, components, or data flows will it touch?
- Are there any stakeholders who need to be involved at this stage?

### 2.2: Apply the 80/20 Rule Early
Identify the core components of the feature that will deliver the most value to users.

- What part of the feature request creates 80% of the user value?
- What parts are nice-to-have and can be deferred to a later version?
- Clearly flag what is **Core** (must-have) versus what is an **Extension** (can be done later).

### 2.3: Classify Techstack Track (🟡 R→C→D - IF COMPLEX)
The R→C→D model is recommended for this step if the feature is cross-track or if the primary track is not obvious.

- **Reasoning**: Which parts of the system does this feature request touch? List all affected components. Which track contains the highest complexity and risk?
- **Critique**: Are any tracks being underestimated? Is the dependency order between tracks being viewed correctly?
- **Decision**: Finalize the primary and secondary tracks. State clearly: "Primary Track: X / Secondary Tracks: Y, Z."

Refer to the `techstack_tracks.md` reference for detailed definitions of each track.

### 2.4: Track Validation (🔵 PRODUCT-TECH CHECKPOINT)
This is a mandatory interaction point between the Product and Tech teams.

- **Input**: The FR Brief from Phase 1 and the preliminary track classification from step 2.3.
- **Roles**:
    - **Product**: Sends the Track Mapping to the Tech Lead of the designated primary track.
    - **Tech Lead**: Conducts a quick review and either confirms or challenges the classification.
- **Tech Lead's Goal**:
    - Is the track classification correct?
    - Are any secondary tracks missing?
    - Is the complexity of any track being underestimated?

## Phase 2 Checkpoint (Product-Tech Aligned)

Before proceeding, ensure the following conditions are met:

- [ ] The feature has been positioned within the product system.
- [ ] The scope has been divided into Core vs. Extension (80/20).
- [ ] The primary and secondary tracks have been validated and confirmed by the Tech Lead.

**Output**: A **Track Mapping Document** that has been validated by the Tech Lead.
