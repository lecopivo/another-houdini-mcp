# Attribreorient (SOP)

## What This Node Is For

`attribreorient` Reorients vector/orient attributes between spaces or references.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/attribreorient.txt`)
- Example set reviewed: yes (`examples/nodes/sop/attribreorient/CopyUsingOrient.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: based on node docs/example description and sticky-note guidance.
- Observed: official example `CopyUsingOrient` instantiated and cooked; representative display output was `2970 pts / 297 prims` at `copy1`.
- Mismatches: none observed in this pass.

## Minimum Repro Setup

- Example loaded: `/obj/academy_seq_*_attribreorient` (instantiated one-by-one, then deleted before next node).
- Verification: asset installs, instantiates, and display network cooks without errors.

## Key Parameters and Interactions

- Primary behavior is driven by node-specific core parameters shown in the example network.
- Downstream contract is mostly attribute-level for attribute nodes, or deformation/crowd contracts for agent/deformer nodes.

## Gotchas and Failure Modes

- Example-driven study confirms setup viability, but production behavior still depends on consistent upstream attribute naming/types.
- Heavy examples (dense geometry/crowd) can mask performance issues until scaled up.

## Related Nodes

- `attribwrangle`
- `group`
- `merge`
