---
name: feature-request-framework
description: "Structured Feature Request framework for Robot Pika integrating product and technical perspectives. Use for: creating feature requests, coordinating Product-Tech teams, defining success criteria, managing cross-track dependencies, ensuring evidence-based decisions."
---

# Feature Request Framework for Robot Pika

## Overview

This skill implements the v5.0 Feature Request (FR) framework for Robot Pika. It provides a structured, 7-phase workflow to guide teams from initial feature discovery to final execution, ensuring that decisions are evidence-based, success is measurable, and Product and Tech teams are aligned throughout the process.

## When to Use

Use this skill for any of the following activities related to Robot Pika:

- **Creating a new feature request**
- **Evaluating an existing feature request**
- **Coordinating work between Product and Tech teams**
- **Defining the scope and success metrics for a feature**
- **Managing cross-track dependencies and technical constraints**

## The 7-Phase Workflow

The framework is divided into seven distinct phases. Each phase has a specific goal, owner, and set of outputs. For detailed instructions on each phase, please refer to the corresponding reference file.

1.  **Phase 1: Understand & Evidence** (`references/phase_1_understand.md`)
2.  **Phase 2: Scope & Classify** (`references/phase_2_scope.md`)
3.  **Phase 3: Constrain** (`references/phase_3_constrain.md`)
4.  **Phase 4: Define Success & Bottleneck** (`references/phase_4_success.md`)
5.  **Phase 5: Design & Diverge** (`references/phase_5_design.md`)
6.  **Phase 6: Validate & Align** (`references/phase_6_validate.md`)
7.  **Phase 7: Specify & Execute** (`references/phase_7_execute.md`)

## Key Concepts

This framework is built on several key concepts that are essential for its successful implementation.

### R→C→D Methodology

The **Reasoning → Critique → Decision (R→C→D)** model is a structured thinking process used at critical steps in the framework to improve decision quality. For a detailed explanation, see `references/r_c_d_methodology.md`.

### Techstack Tracks

All feature requests are classified into one or more of six **Techstack Tracks**. This classification helps to identify the right teams and resources needed for the feature. For a list of all tracks and their definitions, see `references/techstack_tracks.md`.

### Product-Tech Checkpoints

These are mandatory interaction points (marked with a 🔵) between the Product and Tech teams to ensure alignment at critical stages of the process.

### Evidence Gates

The framework enforces a strict **Data Gate** at the beginning of the process. No feature request can proceed without a minimum level of evidence, including both quantitative data and qualitative user feedback.

## Using the Resources

This skill includes a set of resources to help you use the framework effectively.

- **References**: Detailed guides for each phase and key concept. Read these as you progress through the workflow.
- **Templates**: A collection of templates for the outputs of each phase. These are located in the `templates/` directory.
- **Scripts**: A set of scripts to automate repetitive tasks. These are located in the `scripts/` directory.
