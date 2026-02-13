# Test Geometry Rubber Toy (SOP)

## What This Node Is For

`testgeometry_rubbertoy` generates built-in complex test geometry for fast tool/sim prototyping.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/testgeometry_rubbertoy.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/testgeometry_rubbertoy/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: provide realistic, non-trivial geometry with optional increased "difficulty" issues.
- Observed: `/obj/academy_testgeometry_rubbertoy_live` outputs production-like dense mesh (`12874 pts / 12854 prims`) with normals/material path. Changing `difficulty` to `1` preserved stable output topology in this build.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_testgeometry_rubbertoy_live/rubbertoy1 -> OUT_TESTGEOM`
- Key parms: `difficulty`, transform/scale.
- Verification: `probe_geometry` count and attribute checks.

## Key Parameters and Interactions

- `difficulty` is useful for stress-testing robustness.
- Built-in shader/material attrs can be leveraged in lookdev tests.

## Gotchas and Failure Modes

- Geometry is relatively heavy; avoid duplicating unnecessarily in large debug scenes.
- Treat it as test asset, not final shipping geometry.

## Related Nodes

- `testgeometry_pighead`
- `testgeometry_shaderball`
- `testgeometry_crag`
