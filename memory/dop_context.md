# DOP Context Basics

This is the DOP (Dynamics Operators) companion to `memory/sop_context.md`.

It compresses core DOP-network concepts and keeps short rolling notes for DOP nodes as they are studied.

## 1. What DOP Context Is

DOPs are simulation operators.

- They advance state over time/substeps.
- Nodes operate on simulation data (objects, geometry, constraints, fields, forces), not just static geometry.
- A DOP network is a directed simulation graph where order/wiring affects evaluation.

## 2. Core Mental Model

Think in four layers:

1. **State**: simulated data (for Vellum: Geometry + ConstraintGeometry + patch metadata).
2. **Sources/Creation**: nodes that inject or create state.
3. **Modification/Solve**: microsolvers/properties/forces update state each step.
4. **Output/Bridge**: pass results back to SOP level for post-process, cache, render.

## 3. Time and Evaluation

- DOPs can run per frame or per substep.
- Emission/update frequency is a major quality vs cost dial.
- If behavior looks unstable, inspect:
  - substeps
  - iteration counts
  - per-frame vs per-substep creation/updates

## 4. Data Binding and Names

Many DOP nodes target data by name (for example `Geometry`, `ConstraintGeometry`).

Practical rule:
- Always verify the node is modifying the intended data stream.

For Vellum specifically:
- Surface points and constraints are paired and should stay in sync.
- Stream names and patch names are key for per-source isolation.

## 5. SOP <-> DOP Workflow Pattern

Common loop:

1. Build/configure geometry+constraints in SOPs.
2. Solve/modify over time in DOPs.
3. Return to SOPs for post process and caching.

This keeps modeling/authoring in SOPs and time-dependent logic in DOPs.

## 6. Common DOP Gotchas

- Correct node but wrong update frequency.
- Modifying wrong bound geometry stream.
- Creating new constraints when you meant to edit existing ones (or vice versa).
- Assuming a source emits once when it is set to emit each frame/substep.
- Debugging only end frame; always inspect multiple frames/substeps.

## 7. DOP Node Notes (Rolling)

Add concise notes here for each studied DOP node.

### 7.1 vellumsource

- Emits full Vellum patches (geometry + constraints bookkeeping), not just points.
- Emission mode is the primary behavior switch (`Only Once`, `Each Frame`, `Each Substep`, `Instance on Points`).
- Patch naming/stream naming are essential for targeting and downstream control.

### 7.2 vellumconstraintproperty

- Best for editing **existing** constraints during solve (stiffness, damping, rest, break, remove).
- Use Vellum Constraints (SOP/DOP) for creating constraints; use this node to animate/tune them.
- VEX mode is high leverage for targeted per-constraint control.

### 7.3 vellumrestblend

- Blends rest states toward simulation or external targets over time.
- Update frequency strongly affects behavior and performance.
- Useful for plasticity-like effects and directed retargeting of cloth/hair rest shapes.

## 8. How To Extend This File

For each new DOP node studied, append a subsection under **DOP Node Notes (Rolling)**:

- node name
- 2-4 bullets: behavior, key parameters, one gotcha
- one line about where it fits in SOP<->DOP workflow
