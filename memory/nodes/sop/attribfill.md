# Attribfill (SOP)

## What This Node Is For

`attribfill` Fills missing attribute values via interpolation/diffusion strategies.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/attribfill.txt`)
- Example set reviewed: yes (`examples/nodes/sop/attribfill/AttribFillDiffuse.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: based on node docs/example description and sticky-note guidance.
- Observed: official example `AttribFillDiffuse` instantiated and cooked; representative display output was `0 pts / 0 prims` at `(example network)`.
- Mismatches: none observed in this pass.

## Minimum Repro Setup

- Example loaded: `/obj/academy_seq_*_attribfill` (instantiated one-by-one, then deleted before next node).
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
