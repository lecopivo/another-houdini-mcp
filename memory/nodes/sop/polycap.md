# PolyCap (SOP)

## Intent

`polycap` fills open boundary loops by creating cap polygons, typically to close holes or tube ends while preserving or isolating point sharing as needed.

## Core Behavior

- Builds polygons across selected boundary edges.
- Can auto-cap all unshared boundaries when group is empty (`capall`).
- Supports cap orientation reversal, triangle-only caps, and unique-point cap ownership.
- Can recompute existing point normals after capping.

## Key Parameters

- `group`: boundary edges to cap.
- `capall`: if no group, cap all unshared boundaries.
- `reverse`: reverse cap orientation.
- `triangulate`: triangulate generated caps.
- `unique`: use unique points for caps (disconnect cap points from existing shell points).
- `updatenorms`: recompute point normals when present.

## Typical Workflow

```text
open polygon mesh/tube -> polycap -> optional normal/facet cleanup -> downstream ops
```

- Use explicit boundary groups for selective capping (single end, specific holes).
- Keep `capall` enabled for fast full closure on open shells.
- Decide early whether caps should share points with shell (`unique=0`) or be isolated (`unique=1`).

## Production Usage

- Excellent for closing modeling holes before subdivision/simulation/export.
- Useful in procedural tube pipelines to cap one end while leaving another open.
- Prefer explicit grouping in complex meshes to avoid accidental closure of unintended loops.

Measured outcomes (`PolycapTube` + live `/obj/academy_polycap_live`):
- Example behavior:
  - tube source: `20 pts / 10 prims` (open tube sides only).
  - `polycap1` with `group=p8-9`, `capall=0`: `20 pts / 11 prims` (single-end cap).
- Live scope tests:
  - `capall=1`, empty group -> `20 pts / 12 prims` (both ends capped).
  - `capall=0`, empty group -> `20 pts / 10 prims` (no caps).
  - explicit `group=p8-9` -> `20 pts / 11 prims`.
- Triangulation impact:
  - `triangulate=1` increased topology from `12` to `26` primitives on capped tube.
- Unique points impact:
  - `unique=0` -> `20` points,
  - `unique=1` -> `40` points (same primitive count, duplicated cap points).
- Normal recompute behavior with custom seeded normals:
  - `updatenorms=0` preserved upstream-biased average normal,
  - `updatenorms=1` recomputed to balanced average on capped result.

## Gotchas

- Empty `group` behavior depends on `capall`; with `capall=0`, nothing happens.
- `unique=1` can unexpectedly double points and break assumptions about shared topology.
- Triangulated caps may complicate downstream quad-focused workflows.
- Reversing caps changes orientation; verify normal/inside-out expectations.

## Companion Nodes

- `tube` for controlled open-loop sources.
- `normal` / `facet` for post-cap normal/shading cleanup.
- `polyfill` / `ends` as alternative closure tools.

## Study Validation

- ✅ Read docs: `nodes/sop/polycap.txt`
- ✅ Reviewed example: `examples/nodes/sop/polycap/PolycapTube.txt`
- ✅ Inspected sticky note instructions and interactive selection intent
- ✅ Ran live capall/group/triangulate/unique/updatenorms behavior tests in `/obj/academy_polycap_live`
