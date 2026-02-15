# Node Study Template

Use this for each `memory/nodes/<context>/<node>.md` note.

Target style: model notes after `memory/nodes/sop/heightfield_erode-2.0.md` (rich, practical, production-oriented).

## Workflow Reference

Use `memory/houdini_ai_academy.md` section `Workflow (Per Node)` as the canonical end-to-end process.

## Required Note Structure

Use these sections and order unless a section is genuinely not applicable.

### 1) Title

- `# <node_name> (<CONTEXT>)`

### 2) Intent

- 1-3 sentences: what the node is for, where it fits, and why you would choose it.

### 3) Core Behavior

- Short bullets describing runtime behavior and data contract (topology/attrs/time dependence/modes).

### 4) Key Parameters

- Group by tabs/subsystems when relevant.
- Explain high-impact parameters and interactions, not every single parm.

### 5) Typical Workflow

- Include at least one canonical mini graph.

Example:

```text
input -> target_node -> OUT
```

- Give concise, practical operation steps.

### 6) Production Usage

- Document practical heuristics and "first-pass" defaults when useful.
- Include measured outcomes from live validation (counts, attrs, mode changes, etc.).

### 7) Gotchas

- Transferable failure modes + detection + fix.

### 8) Companion Nodes

- List meaningful companion nodes and what role they play.

### 9) Optional Sections (Use When Valuable)

- `Version Notes`
- `Related Nodes`
- `Practical Use Cases`

### 10) Study Validation

- Checklist bullets showing evidence of completion.

Suggested format:

- `✅ Read docs: ...`
- `✅ Reviewed example(s): ...`
- `✅ Inspected internals/comments/stickies`
- `✅ Ran live parameter/behavior tests`

## Quality Rules

- Prefer reusable guidance over chronological logs.
- Record observed behavior, not only expected behavior.
- Include concrete measured evidence from this Houdini build.
- Explicitly note mismatches between docs/examples and observed behavior.
- Keep prose concise but sufficiently detailed for future reuse.

## Academy QA Checklist

- [ ] Official docs reviewed
- [ ] Example files reviewed
- [ ] OTL instantiated/unlocked and internals inspected
- [ ] Node comments read
- [ ] Sticky notes read
- [ ] Behavior validated with observed tests
- [ ] Measured outcomes captured (counts/attrs/mode behavior)
- [ ] Mismatches documented when present
- [ ] Context and progress files updated
