# Mirror (SOP)

## Intent

`mirror` duplicates geometry across a configurable plane and optionally clips, stitches, and groups the mirrored side. It is a foundational symmetry tool for modeling/rig prep and procedural half-to-full mesh workflows.

## Core Behavior

- Mirrors selected primitives from input geometry across a plane.
- `operation` controls full duplication vs clip-and-mirror behavior.
- Plane orientation can be authored by explicit direction/origin or by transform-style translate/rotate controls.
- Supports seam consolidation and output grouping of mirrored primitives.

## Key Parameters

- Selection and mode:
  - `group` to limit which primitives are mirrored.
  - `operation`: `Mirror All Primitives` or `Clip Primitives and Mirror`.
- Plane control:
  - `dirtype`: `Direction` (`origin`, `dir`, `dist`) vs `Transform` (`t`, `r`).
- Topology handling:
  - `keepOriginal` to retain source side.
  - `consolidatepts` + `consolidatetol` (+ `consolidateunshared`) for seam welding.
- Output management:
  - `createoutputgroup` + `outputgroup` to isolate mirrored faces.

## Typical Workflow

```text
half/partial mesh -> mirror -> (optional facet/normal cleanup) -> downstream modeling
```

- Cut or isolate a half mesh first when building symmetric assets.
- Channel-reference mirror plane distance to upstream clip/cut distance when using procedural slicing.
- Consolidate seam once plane placement is final.

## Production Usage

- Prefer `Clip Primitives and Mirror` for clean one-sided authoring pipelines.
- Use output groups to keep mirrored regions selectable for UV/material/tweak passes.
- Keep plane controls in one mode (direction or transform) during setup to avoid mixed-intent edits.

Measured outcomes (`MirrorSpout` example + live `/obj/academy_mirror_live`):
- Example (`mirror1`) mirrors clip output and references `dist` from upstream `clip1` (`-0.08`) for aligned center seam behavior.
- Baseline mirror-all (`keepOriginal=1`) doubled a box from `6 -> 12` primitives (`8 -> 16` points).
- `keepOriginal=0` produced only mirrored result (`6 prims`, mirrored-center output).
- `operation=Clip Primitives and Mirror` reduced primitive count in tested setup (`12 -> 10` prims), confirming cut-before-mirror behavior.
- Seam consolidation interaction (clip+mirror case, centered box):
  - `consolidatepts=0` -> `16 pts / 10 prims`
  - `consolidatepts=1` -> `12 pts / 10 prims`.
- Plane authoring mode interaction:
  - `dirtype=Transform` with rotation/translation changed final bounds/center significantly versus direction-mode defaults.
  - direction mode with `dist=0.25` shifted mirrored extent and output center predictably.
- Group-limited mirror test:
  - full group (`""`) -> `12` prims,
  - subset group (`"0-2"`) -> `9` prims.
- Output-group test:
  - enabling `createoutputgroup` produced prim group `mirrored_half` containing mirrored-side primitives (`6` in tested mesh).

## Gotchas

- Mirroring a full mesh with `keepOriginal=1` can create overlapping internal geometry unless clipped first.
- Seam consolidation only helps when points are near the mirror plane within tolerance; wrong tolerance can miss welds or over-weld.
- Group filtering mirrors only selected primitives; easy to misread as node failure if group is too narrow.
- Plane controls in `Direction` vs `Transform` modes represent different authoring mental models; avoid mixing without intent.

## Companion Nodes

- `clip` to prepare half geometry and drive mirror `dist`.
- `facet`/normal tools for post-mirror shading cleanup.
- `group` tools for targeted mirroring and downstream mirrored-region operations.

## Study Validation

- ✅ Read docs: `nodes/sop/mirror.txt`
- ✅ Reviewed example: `examples/nodes/sop/mirror/MirrorSpout.txt`
- ✅ Inspected sticky note guidance (distance channel reference to clip)
- ✅ Ran live operation/plane/group/consolidation/output-group interaction tests in `/obj/academy_mirror_live`
