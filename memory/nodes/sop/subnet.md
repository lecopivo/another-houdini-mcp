# Subnet (SOP)

## What This Node Is For

`subnet` encapsulates SOP subgraphs into one macro node, preserving multi-input wiring via subnet inputs/outputs.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/subnet.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/subnet/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: organize and abstract SOP networks without changing flow semantics.
- Observed: `/obj/academy_subnet_live` (`box -> subnet -> output`) passes through geometry as expected (`8 pts / 6 prims`) with default subnet behavior.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_subnet_live/box1 -> subnet1 -> OUT_SUBNET`
- Key parms: labels only; behavior comes from internal subnet wiring.
- Verification: `probe_geometry` on `OUT_SUBNET`.

## Key Parameters and Interactions

- Subnet primarily affects graph organization, not geometry operations.
- Explicit `output` nodes inside subnet help stable external contracts.

## Gotchas and Failure Modes

- Hidden internal display flag changes can confuse debugging if outputs are not explicit.
- Over-nesting can reduce readability if not named/labeled well.

## Related Nodes

- `output`
- `null`
