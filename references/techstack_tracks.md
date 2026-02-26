# Techstack Tracks for Robot Pika

This document provides a reference for the six different techstack tracks used to classify feature requests for Robot Pika. Each track has a specific set of concerns and constraint questions that need to be addressed during the feature development process.

## Track A: Orchestration
- **Definition**: Changes to the queue, triggers, or routing of tasks between different agents.
- **Example**: "The robot should automatically suggest a new lesson when it detects that the child is idle."
- **Constraint Questions**:
    - Is the trigger condition supported by the backend? If not, what needs to be implemented?
    - Will the queue management logic change? What is the impact?
    - Which Friendship Phase will be affected?
    - Are there dependencies on other tracks? What is the required sequence?

## Track B: Conversation/AI
- **Definition**: Changes to how Pika speaks, remembers information, or processes language.
- **Example**: "Pika should remember the child's favorite color."
- **Constraint Questions**:
    - Do we need to create a new agent or extend an existing one?
    - Is the Mem0 schema sufficient, or do we need to add new fields?
    - Will the ASR latency meet the UX requirements?
    - What updates are needed for the LLM prompt?
    - Do the guardrails need to be modified?

## Track C: Robot Hardware
- **Definition**: Changes to the robot's physical actions, such as GIFs, servo movements, LED states, or sensor behaviors.
- **Example**: "The robot should wave its arm when the child completes a lesson."
- **Constraint Questions**:
    - Should we create a new GIF or reuse an existing asset?
    - Which servo commands are needed? Are there any potential conflicts?
    - Is a new LED state required? Which sensor will trigger it?
    - Is the backend listening for this sensor event?
    - Will any screen overlay exceed 20% of the screen?

## Track D: Learning System
- **Definition**: Changes to the learning path, assessment logic, or adaptive algorithms.
- **Example**: "The difficulty of the lessons should adjust based on the child's performance."
- **Constraint Questions**:
    - Does this affect the Path Registry, Progress Tracker, or Next Lesson Selector?
    - How will the content be scaled?
    - Does this conflict with the current LPE recommendations?
    - Will the assessment logic change?

## Track E: Parent App
- **Definition**: Changes to the parent-facing mobile app, including the UI, notifications, remote control features, or data display.
- **Example**: "The app should display a dashboard with the child's learning statistics."
- **Constraint Questions**:
    - Are we displaying new data or just changing the UI?
    - Is the necessary API endpoint already exposed?
    - What are the trigger, frequency, and opt-out options for notifications?
    - Does the remote control command conflict with the robot's current state?

## Track F: Cross-system
- **Definition**: Features that span multiple tracks and require significant coordination.
- **Example**: "When a lesson is completed, the robot should wave its arm and the parent app should send a notification."
- **Constraint Questions**:
    - What is the dependency order between the systems?
    - What are the risks if the tracks do not sync properly?
    - Who is the coordination owner?
