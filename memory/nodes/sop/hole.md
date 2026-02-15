# Hole (SOP)

## Intent

Create or remove topological holes by bridging enclosed polygon/Bezier regions. It is most useful when interior cut geometry is offset or rotated and simple planar delete workflows are not robust.

## Core Behavior

- Works as a bridge constructor/remover on polygon and Bezier inputs.
- Uses proximity and angular compatibility gates to decide whether regions can be connected.
- Can align off-plane interior outlines to host geometry (`snap`) before finalizing the bridge.
- Can reverse the operation (`break`) to restore previously bridged holes.

## Key Parameters

- `dist`: maximum spatial gap allowed between candidate interior/exterior regions.
- `angle`: maximum relative orientation difference allowed for joining.
- `snap`: projects/rotates interior shape to be flush with host outline when bridge is created.
- `break`: un-bridges existing holes (reverse mode).
- `removeunusedpoints`: cleans up residual points after bridge changes.

## Typical Workflow

```
grid + circle -> merge -> hole -> OUT
```

- Build host and cutter as polygon/Bezier.
- Start with default `dist`/`angle`; increase only as needed.
- Enable `snap` if cutter is intentionally off-plane and should become flush.
- Use `break=1` as a cleanup/recovery pass on already holed geometry.

## Production Usage

- Use `dist` as the first control for translated cutters.
- Use `angle` as the first control for rotated cutters.
- Keep `removeunusedpoints=1` in production to avoid stale point clutter.

Measured example outcomes (`/obj/academy_HoleBasic`):
- Baseline make-hole: `2 prims / 14 verts` -> `1 prim / 16 verts`.
- Distance gate: `dist=0.05` no bridge (`2/14`), `dist=0.3` bridge (`1/16`).
- Angle gate: raising `angle` to `80` enabled bridge in rotated case.
- Snap check: `snap=0` kept depth (`z span ~0.437`), `snap=1` flattened to plane (`z span 0.0`).
- Reverse mode: `break=1` restored filled result (`2/14`), `break=0` kept bridged hole (`1/16`).

## Gotchas

- Unchanged output usually means tolerance gates are too strict, not that the node failed.
- Off-plane cutters may appear wrong until `snap` is enabled.
- NURBS are converted internally; prefer explicit polygon/Bezier authoring when topology expectations are strict.

## Companion Nodes

- `grid`, `circle`, `merge`, `xform` for host/cutter construction and test offsets.
- `polycap`/`polyextrude` for post-hole modeling operations.

## Study Validation

- ✅ Read docs: `nodes/sop/hole.txt`
- ✅ Reviewed example: `examples/nodes/sop/hole/HoleBasic.txt`
- ✅ Inspected all key example branches (`make_hole`, `distance_tolerance`, `angle_tolerance`, `remove_hole`)
- ✅ Ran live parameter probes for `dist`, `angle`, `snap`, and `break`
