# Tube (SOP)

## What This Node Is For

`tube` creates analytic tube/cone/cylinder-like geometry across multiple primitive types.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/tube.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/tube/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: generate open/closed tubes with configurable primitive type, caps, orientation, and resolution.
- Observed: `/obj/academy_tube_live` default primitive output is analytic (`1 pt / 1 prim`); switching to polygon type and `cols=24` gives explicit mesh (`48 pts / 24 prims`).
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_tube_live/tube1 -> OUT_TUBE`
- Key parms: `type`, `rad1/rad2`, `height`, `rows`, `cols`, `cap`.
- Verification: `probe_geometry` before/after type switch.

## Key Parameters and Interactions

- `type` determines analytic vs explicit topology.
- `rad1/rad2` with one radius near zero gives cone behavior.
- `cap` + `consolidatepts` affect seam/corner topology.

## Gotchas and Failure Modes

- Primitive-type output may be too sparse for downstream SOPs expecting polygonal detail.
- Orientation mismatches are a common source of axis confusion.

## Companion Finding (from PolyCap study)

- For selective end-cap workflows, polygon tube output with `consolidatepts=0` gives stable boundary-edge selections (for example `p8-9` loop in the PolyCap example) so a single tube end can be capped explicitly.
- This pattern is useful when one end must remain open for downstream modeling operations.

## Related Nodes

- `cylinder` (workflow equivalent in some pipelines)
- `sphere`
- `box`
