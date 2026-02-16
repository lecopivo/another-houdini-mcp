# Subdivide (SOP)

## What This Node Is For

`subdivide` smooths polygonal meshes by recursively refining faces (Catmull-Clark/OpenSubdiv variants), and can limit refinement to selected regions for local detail.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/subdivide.txt`)
- Example set reviewed: yes (`examples/nodes/sop/subdivide/SubdivideCrease.txt`)
- Example OTL internals inspected: yes (`SubdivideCrease.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Use depth-based subdivision for smoother surfaces, and keep hard features using crease workflows.
  - Example demonstrates two crease strategies: explicit `crease` SOP before `subdivide`, and procedural crease geometry via second input.
- Observed (live scene/params/geometry):
  - In `/obj/academy_subdivide_live`, full-mesh subdivision scales quickly with depth:
    - `iterations=1` -> `26 pts / 24 prims`
    - `iterations=2` -> `98 pts / 96 prims`
    - `iterations=3` -> `386 pts / 384 prims`
  - Local subdivision works as expected: setting `subdivide="0"` (single primitive group) reduced processed scope and produced `89 pts / 69 prims` instead of global refine.
  - Official example network `/obj/academy_SubdivideCrease/box_object1` confirms both direct crease and second-input crease patterns in one setup.
- Mismatches:
  - None observed.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_subdivide_live/box1 -> subdivide1 -> OUT_SUBDIVIDE`
- Key parameter names and values:
  - `subdivide1.iterations = 1/2/3`
  - `subdivide1.subdivide = ""` (global) vs `"0"` (local primitive)
  - `subdivide1.algorithm = 2` (default OpenSubdiv Catmull-Clark in this build)
- Output verification method:
  - `probe_geometry` on `OUT_SUBDIVIDE` after each parameter change.

## Key Parameters and Interactions

- `iterations` is exponential-cost in practice; treat values above 2 cautiously on production meshes.
- `subdivide` (group) is the most practical control for localized detail.
- Second input + `creases` lets you proceduralize crease masks instead of hand-picking edges.
- `overridecrease` and `creaseweight` are useful for globally forcing sharpness without editing upstream crease attributes.

## Practical Use Cases

1. Add viewport/render smoothing to low-res model cages while preserving selected hard edges.
2. Add local detail only in deformation-critical regions (face/hands/impact zones) without globally increasing topology.

## Gotchas and Failure Modes

- High `iterations` can explode topology and slow all downstream SOPs.
- If crease topology does not match main mesh point numbering, second-input crease matching fails.
- Mixed local/global subdivision near boundaries can produce visible transition artifacts if crack-closing options are not chosen intentionally.

## Companion Finding (from Peak study)

- Subdividing immediately after localized peak deformation is an effective artifact-cleanup pattern for accent edits.
- In `PeakEars`, `subdivide` (`algorithm=0`, `iterations=2`) preserved core attrs (`P`,`uv`) while increasing resolution significantly (`1302 -> 19818` points), smoothing the peaked ear region.

## Related Nodes

- `crease`
- `divide`
- `smooth`
- `tridivide`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
