# Channel (SOP)

## What This Node Is For

`channel` Imports CHOP channel data into SOP attributes/parameters.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/channel.txt`)
- Example set reviewed: yes (`examples/nodes/sop/channel/BlobbySphere.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: based on node docs/example description and sticky-note guidance.
- Observed: official example `BlobbySphere` instantiated and cooked; representative display output was `100 pts / 1 prims` at `channel1`.
- Mismatches: none observed in this pass.

## Minimum Repro Setup

- Example loaded: `/obj/academy_seq2_*_channel` (instantiated one-by-one, then deleted before next node).
- Verification: asset installs, instantiates, and display network cooks without errors.

## Key Parameters and Interactions

- Primary behavior is driven by node-specific core parameters shown in the example network.
- Loop/deform/sim nodes depend strongly on upstream attribute naming, topology stability, and expected class contracts.

## Gotchas and Failure Modes

- Dense/sim examples can hide expensive cooks until scaled; validate with probes early.
- For loop nodes, wrong block wiring/order can appear as silent logic errors.

## Related Nodes

- `attribwrangle`
- `group`
- `merge`
