# Box (SOP)

## What This Node Is For

`box` creates box/cage geometry and can also auto-bound input geometry for envelope/lattice workflows.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/box.txt`)
- Example set reviewed: yes (`examples/nodes/sop/box/BoxSpring.txt`)
- Example OTL internals inspected: yes (`BoxSpring.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: create boxes across primitive types and support cage/bounding use cases.
- Observed:
  - Live repro `/obj/academy_box_live`: enabling `dodivs=1` and setting `divs=5,5,5` increases topology (`8/6 -> 216/108`, pts/prims).
  - Example `/obj/academy_BoxSpring` shows two key production patterns: animated bounding proxy and box+lattice+spring deformation cage.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_box_live/box1 -> OUT_BOX`
- Key parms: `type`, `size*`, `dodivs`, `divs*`, `rebar`, input-bound behavior.
- Verification: `probe_geometry` count deltas from division changes.

## Key Parameters and Interactions

- `dodivs/divs*` is the main control for lattice-compatible cages.
- Input-connected mode turns Box into auto-bounds generator.
- `rebar` adds lattice crossbars useful for spring-like stabilization workflows.

## Gotchas and Failure Modes

- Wrong division parity versus downstream lattice can destabilize deformation quality.
- Oriented bounding behavior depends on valid point hull geometry.

## Related Nodes

- `bound`
- `lattice`
- `spring`
