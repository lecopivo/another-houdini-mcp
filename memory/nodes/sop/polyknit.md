# PolyKnit (SOP)

## Intent

`polyknit` creates bridging/fill polygons between existing polygon edges/points using ordered point-list patterns and meta-edge shortest-path logic.

## Core Behavior

- Builds triangles/quads from specified point sequences.
- Supports meta-triangle/meta-quad modes that infer shortest connected edge paths.
- Can keep original geometry and optionally generate unique points.
- Includes cleanup options for degenerate faces and collapsed quads.

## Key Parameters

- `pointlist`: command-like sequence with mode tokens (`t`, `q`, `T`, `Q`).
- `collapsequads`, `degen`: cleanup of quasi-triangles/degenerate output.
- `flip`: output winding/normal direction control.
- `uniquepts`, `keep`: point reuse and source retention behavior.
- `updatenmls`: normal recomputation support.

## Typical Workflow

```text
open polygon boundaries -> polyknit -> optional smooth/subdivide/topology cleanup
```

- Use zig-zag ordering between opposite boundaries for predictable stitching.
- Validate winding and degeneracy immediately after knit.

## Production Usage

- Useful for quick manual gap fills and edge redefinition in legacy polygon workflows.
- `PolyKnitBasic` example focuses on pattern-dependent output differences and hole/gap filling behavior.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Node is deprecated; prefer `topobuild` or `polyfill` for modern workflows.
- Point ordering strongly dictates result; small list changes can radically alter topology.
- Works best when opposing boundaries have compatible point density.

## Companion Nodes

- `topobuild` / `polyfill` (recommended modern alternatives).
- `polystitch` / `polyloft` for related bridging strategies.
- `subdivide` for post-knit smoothing.

## Study Validation

- ✅ Read docs: `help/nodes/sop/polyknit.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/polyknit/PolyKnitBasic.txt`
- ⏳ Live validation pending
