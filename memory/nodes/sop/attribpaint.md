# Attribpaint (SOP)

## What This Node Is For

`attribpaint` Interactive painting of attributes on geometry surfaces.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/attribpaint.txt`)
- Example set reviewed: yes (`examples/nodes/sop/attribpaint/PaintingAttributes.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: based on node docs/example description and sticky-note guidance.
- Observed: official example `PaintingAttributes` instantiated and cooked; representative display output was `12874 pts / 12854 prims` at `mask_to_Cd`.
- Mismatches: none observed in this pass.

## Minimum Repro Setup

- Example loaded: `/obj/academy_seq_*_attribpaint` (instantiated one-by-one, then deleted before next node).
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
