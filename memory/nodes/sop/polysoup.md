# PolySoup (SOP)

## Intent

`polysoup` compacts polygon primitives into polygon-soup primitives for memory/storage/runtime efficiency, especially on very large meshes.

## Core Behavior

- Converts eligible polygons into one or more `PolySoup` primitives.
- Preserves primitive attributes/groups by splitting soups when needed.
- Can optionally ignore primitive attrs/groups to maximize merging.
- `mergeverts` controls whether identical soup vertices are shared.

## Key Parameters

- `ignoreattribs`: ignore primitive-attribute differences when deciding soup partitions.
- `ignoregroups`: ignore primitive-group membership when partitioning.
- `minpolys`: minimum polygon count required to form soup; below threshold keeps regular polygons.
- `mergeverts`: share identical vertices inside soup (major memory/vertex-count impact).
- `convex`, `usemaxsides`, `maxsides`: optional convexing/splitting controls during conversion.

## Typical Workflow

```text
high-res polygon geo -> polysoup -> (optional switch for debug) -> export/render/cache
```

- Keep modeling/editing upstream as regular polygons.
- Apply `polysoup` near end of pipeline for output optimization.
- Optionally keep a switch branch for raw-poly vs polysoup diagnostics.

## Production Usage

- Use on heavy static or deformation-ready geometry before disk export/render handoff.
- Keep `ignoreattribs/groups` off unless you explicitly accept semantic grouping/attribute partition changes.
- Use `mergeverts=1` when vertex uniqueness is not required by downstream vertex-attribute edits.

Measured outcomes (`PolysoupTorus` example + live `/obj/academy_polysoup_live`):
- Official example high-res torus:
  - raw branch: `4,000,000 pts / 4,000,000 prims / 16,000,000 verts`.
  - polysoup branch: `4,000,000 pts / 1 prim / 4,000,000 verts`.
- Live partitioning test (two boxes with different primitive attrs/groups):
  - baseline preserve attrs/groups: `2` polysoup prims.
  - `ignoreattribs=1` alone: still `2` soups (group split remains).
  - `ignoreattribs=1` + `ignoregroups=1`: merged to `1` soup.
- `minpolys` threshold behavior:
  - `minpolys=1`: soup output (`1` polysoup prim).
  - `minpolys=200` (above local polygon count): reverted to regular polygons (`108` polygon prims).
- `mergeverts` effect (same input):
  - `mergeverts=0` -> soup with `432` vertices.
  - `mergeverts=1` -> soup with `112` vertices.

## Gotchas

- Many distinct primitive attributes/groups can negate polysoup compression benefits.
- Not all SOPs are ideal for polygon-soup editing; use late-stage optimization pattern.
- Converting back to polygons can change primitive order while remaining topologically equivalent.
- `ignoregroups/ignoreattribs` can improve merge rate but may break intended semantic partitions.

## Companion Nodes

- `convert` for reverting soup to polygons when needed.
- `switch` for raw-vs-optimized branch comparison in heavy scenes.
- `divide` when convexing/tri splitting is required before final export.

## Study Validation

- ✅ Read docs: `nodes/sop/polysoup.txt`
- ✅ Reviewed example: `examples/nodes/sop/polysoup/PolysoupTorus.txt`
- ✅ Inspected stickies and branch setup (`torus1 -> polysoup1 -> switch1`)
- ✅ Ran live tests for attrs/groups partitioning, minimum threshold fallback, and vertex merging behavior
