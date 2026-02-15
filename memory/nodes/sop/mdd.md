# MDD (SOP)

## Intent

`mdd` applies point-cache animation from an `.mdd` file onto geometry, or creates point-only geometry directly from the cache when no input is connected. It is used for topology-stable deformation playback across DCC/pipeline boundaries.

## Core Behavior

- Reads point positions per frame from an MDD file and maps them by point number.
- With input geometry, preserves input connectivity and replaces/updates point positions.
- Without input geometry, outputs loose points from the cache (no primitives).
- Requires compatible point numbering; mismatches generate warnings and can produce partial/invalid-looking results.

## Key Parameters

- `file`: MDD cache path.
- `frame`: sample frame in cache (often `$FF`, optionally offset).
- `interp`: inter-frame interpolation mode.
- `coordsys`: right/left-handed conversion handling (can flip Z sign behavior).
- `shiftstart`: offsets cache start to frame 1.
- `reload`: force file reload.

## Typical Workflow

```text
topology-stable mesh -> mdd(file/frame) -> downstream shading/sim/render
```

- Export cache from source geometry with stable point count/order.
- Apply cache to matching topology mesh in `mdd`.
- Validate a few landmark points across frames before production handoff.

## Production Usage

- Treat MDD as a strict point-order contract: use after workflows that do not alter topology.
- Keep a reference branch for quick point-count/order sanity checks.
- Use point-only mode for diagnostics when debugging file contents independent of source connectivity.

Measured outcomes (`SimpleMDD` example + live `/obj/academy_mdd_live`):
- Example file path `/home/tskrivan/output.mdd` was unavailable in this environment; node warned and effectively passed through input.
- Generated a valid test cache via MDD ROP (`/out/academy_mdd_writer`) to `/tmp/academy_anim.mdd` from animated box (`$F*15` Y-rotation).
- With matching box input:
  - frame sampling worked (`frame 1/6/12` changed point 0 from `(-0.6124,-0.5,-0.3536)` to `(-0.5,-0.5,0.5)` to `(0.5,-0.5,0.5)`).
  - connectivity preserved (`8 pts / 6 prims`).
- Without input geometry:
  - produced point-only output (`8 pts / 0 prims`) and tracked the same cache motion.
- Interpolation test at `frame=5.5` changed sampled positions by mode:
  - `interp=0` point0 `(-0.5562,-0.5,0.4268)`
  - `interp=1/2` point0 `(-0.5609,-0.5,0.4304)`.
- Coordinate system test (`frame=8`) flipped Z sign for sampled points:
  - `coordsys=0` point0 `(-0.183,-0.5,-0.683)`
  - `coordsys=1` point0 `(-0.183,-0.5,0.683)`.
- Topology mismatch test (sphere input `162 pts` vs cache `8 pts`):
  - warning: `MDD file and geometry have mismatching point counts.`
  - output still cooked but only a subset moved (`8 of 162` points), showing unsafe partial application.

## Gotchas

- Missing/corrupt file often yields warning + input passthrough; easy to miss without checking node messages.
- Point count mismatch may not hard-error; it can partially affect geometry and produce subtle corruption.
- Any topology change between export/apply invalidates cache intent even if node still cooks.
- `coordsys` differences can silently mirror motion on Z if source DCC handedness differs.

## Companion Nodes

- `out/mdd` ROP writer for cache generation.
- `sort`/topology-check utilities to maintain point-order compatibility.
- `filecache` for local pipeline staging around MDD exchange.

## Study Validation

- ✅ Read docs: `nodes/sop/mdd.txt`
- ✅ Reviewed example: `examples/nodes/sop/mdd/SimpleMDD.txt`
- ✅ Inspected stickies and embedded writer network (`ropnet1/mdd1`)
- ✅ Ran live cache export/import, interpolation, coordinate-system, and mismatch tests in `/obj/academy_mdd_live`
