# Remesh to Grid (SOP)

## Intent

`remeshgrid` rebuilds polygon topology via an intermediate volume representation to regularize mesh structure, close small defects, and remove interior artifacts.

## Core Behavior

- Converts input polygons to a volumetric representation, then remeshes back to polygons.
- Topology density is primarily controlled by voxel size (`divisionsize`) and simplification (`adaptivity`).
- Surface interpretation (`surfacetype`) changes whether input is treated as closed volume or thin sheet.
- Optional smoothing, dilation/erosion, and feature sharpening substantially affect output shape and counts.

## Key Parameters

- `divisionsize`: primary resolution/density control.
- `adaptivity`: variable polygon sizing in flatter regions.
- `surfacetype`, `surfoffset`: closed-volume vs thin-plate reconstruction contract.
- `dilateerode`, `smoothingiterations`: volumetric shape-conditioning controls.
- `sharpenfeatures`, `edgetolerance`, `project`, `postsmooth`: edge/detail preservation controls.

## Typical Workflow

```text
irregular polygon mesh -> remeshgrid -> (optional attr transfer/project cleanup)
```

- Tune base density first (`divisionsize`), then adaptivity.
- Only after baseline is acceptable, adjust smoothing/sharpening and thin-plate offsets.

## Production Usage

- Strong fit for photogrammetry cleanup and topology regularization before sculpting/simulation.
- Use thin-plate mode for open/sheet-like scans; closed-volume for watertight solids.

Measured outcomes (official asset + live `/obj/academy_remeshgrid_live`):
- Live baseline: `996 pts / 994 prims / 3976 verts`.
- Resolution sweep:
  - `divisionsize 0.05 -> 0.1 -> 0.2` gave `4074 -> 996 -> 240` points.
- Adaptivity sweep at `divisionsize=0.1`:
  - `adaptivity 0.0 -> 0.1 -> 0.5` gave `996 -> 787 -> 401` points.
- Surface type behavior:
  - closed-volume (`surfacetype=0`) maintained compact shell,
  - thin-plate (`surfacetype=1`) with `surfoffset 0.03/0.1/0.2` produced larger/thicker reconstructions and changed density (`1459/1306/566` points).
- Volumetric conditioning:
  - `dilateerode -0.03/0/0.03` shifted extents and counts (`371/401/363` points).
  - `smoothingiterations=5` heavily simplified this test mesh (`40 pts / 48 prims`).
- `sharpenfeatures=1` restored much denser feature-preserving output in this setup (`995 pts / 994 prims` vs `401/475` when off).

## Gotchas

- UVs are not preserved by default through volumetric remesh workflows.
- High smoothing iterations can aggressively collapse detail.
- Thin-plate + large offset can alter silhouette more than expected.

## Companion Nodes

- `vdbfrompolygons` / `convertvdb` (conceptual equivalent pipeline).
- `attribtransfer` for post-remesh UV/attribute restoration.
- `normal`/`facet` for downstream shading cleanup after heavy remesh changes.

## Study Validation

- ✅ Read docs: `nodes/sop/remeshgrid.txt`
- ✅ Reviewed example: `examples/nodes/sop/remeshgrid/AdaptiveRemeshToGrid.txt`
- ✅ Inspected example and built editable live remesh test network
- ✅ Ran live resolution/adaptivity/surface-type/smoothing/sharpen sweeps with measured outputs
