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

## Related Nodes

- `cylinder` (workflow equivalent in some pipelines)
- `sphere`
- `box`
